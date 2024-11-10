# 1. Gerekli Modüllerin İçe Aktarılması
import os
from tqdm import tqdm
from docx import Document
from langchain.document_loaders import PyPDFLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Pinecone as LangchainPinecone 
from langchain.llms import HuggingFacePipeline
from langchain.chains import RetrievalQA
from pinecone import Pinecone, ServerlessSpec
import hashlib
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from huggingface_hub import login
import pinecone
from dotenv import load_dotenv

# .env dosyasıdan çevre değişkenlerini yükle
load_dotenv()

# Pinecone API keys ve Hugging Face token getir
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT")
HUGGING_FACE_TOKEN = os.getenv("HUGGING_FACE_TOKEN")

"""# 2. Dosyaların Yüklenmesi ve Metadata İşlenmesi

Bu bölüm PDF ve DOCX dosyalarının sayfa bazlı ayrımını yapar ve metadata ekler.
"""

def load_documents(path):
    documents = []

    # Belirtilen klasördeki dosyaları tarayın
    for doc in os.listdir(path):
        file_path = os.path.join(path, doc)

        # PDF dosyalarını işleme
        if doc.endswith(".pdf"):
            loader = PyPDFLoader(file_path)
            pages = loader.load_and_split()
            for i, page in enumerate(pages):
                # "Fizyosoft" kelimelerini "Becure" ile değiştirin
                content = page.page_content.replace("\n", "")
                metadata = {"pdf_name": doc, "page_number": i + 1}
                documents.append({"content": content, "metadata": metadata})

        # DOCX dosyalarını işleme
        elif doc.endswith(".docx"):
            document = Document(file_path)
            doc_text = "\n".join([para.text for para in document.paragraphs if para.text])
            metadata = {"docx_name": doc}
            documents.append({"content": doc_text, "metadata": metadata})

    return documents

# Kullanım
documents = load_documents("rag_dataset")
print(f"{len(documents)} documents uploaded.")

"""# 3. Pinecone Bağlantısı ve İndeks Oluşturma

Pinecone’u başlatıp gerekli ayarları yapıyoruz.
"""

# Pinecone API anahtarlarını ayarla
os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
os.environ["PINECONE_ENVIRONMENT"] = PINECONE_ENVIRONMENT

# Pinecone'u başlat
pc = Pinecone(api_key=PINECONE_API_KEY)

# İndeks kontrolü ve oluşturma
index_name = "lea-rag-llm-db"
if index_name in pc.list_indexes().names():
    print(f"Index {index_name} already exists.")
elif index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=384,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1")
    )
    print(f"Index {index_name} created.")

# Vektör mağazasına bağlanma
index = pc.Index(index_name)

"""# 4. Embedding İşlemi ve Pinecone'a Yükleme

Belge içeriğini embedding'e çevirip Pinecone’a ekliyoruz.
"""
# Hugging Face token'inizi kullanarak giriş yapın
login(token=HUGGING_FACE_TOKEN)

# Embedding Model Seçimi
ALL_MINILM_L6_V2= "sentence-transformers/all-MiniLM-L6-v2"
ALL_MINILM_L12_V2= "sentence-transformers/all-MiniLM-L12-v2"
E5_LARGE_V2= "intfloat/e5-large-v2"
MPNET_BASE_V2= "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"

# Embedding modeli yükleme
embedding_model_name = ALL_MINILM_L12_V2 
embedding_model = HuggingFaceEmbeddings(model_name=embedding_model_name)


def hash_document(doc):
    """Belgeyi SHA256 ile hashle."""
    return hashlib.sha256(doc.encode()).hexdigest()

# Belgeleri Pinecone'a ekleme işlemi
checked_doc_count, new_doc_count = 0, 0

for doc in tqdm(documents, desc="Belgeler işleniyor", unit="belge"):
    content, metadata = doc["content"], doc["metadata"]
    doc_id = hash_document(content)

    # Önceki kayıt kontrolü
    existing_record = index.fetch([doc_id])

    if existing_record and existing_record.get("vectors"):
        checked_doc_count += 1
    else:
        vector = embedding_model.embed_query(content)
        # Metadata'yı kontrol edin
        if content:
            index.upsert([(doc_id, vector, {"content": content, **metadata})])
            new_doc_count += 1
        else:
            print(f"Belge boş: {doc_id}")

# Print summary
if new_doc_count == 0:
    print(f"{checked_doc_count} documents were checked. No new documents added.")
else:
    print(f"{checked_doc_count} documents checked. {new_doc_count} new documents added.")

"""# 5. Retrieval QA Yapılandırma

Modeli tanımlayıp, sorgu işlemleri için RAG yapısını kuruyoruz.
"""


# LLM Model seçimi
LLAMA_3_2_1B= "meta-llama/Llama-3.2-1B"
LLAMA_3_2_3B= "meta-llama/Llama-3.2-3B"
LLAMA_3_2_1B_INSTURCT= "meta-llama/Llama-3.2-1B-Instruct"
LLAMA_3_2_3B_INSTURCT= "meta-llama/Llama-3.2-3B-Instruct"
LLAMA_3_2_1B_INSTURCT_QLORA_INT4_EO8= "meta-llama/Llama-3.2-1B-Instruct-QLORA_INT4_EO8"
LLAMA_3_2_3B_INSTURCT_QLORA_INT4_EO8= "meta-llama/Llama-3.2-3B-Instruct-QLORA_INT4_EO8"
LLAMA_3_2_1B_INSTURCT_SPINQUANT_INT4_EO8= "meta-llama/Llama-3.2-1B-Instruct-SpinQuant_INT4_EO8"
LLAMA_3_2_3B_INSTURCT_SPINQUANT_INT4_EO8= "meta-llama/Llama-3.2-3B-Instruct-SpinQuant_INT4_EO8"

# Model ve tokenizer yükleme
model_name = LLAMA_3_2_1B_INSTURCT 
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype=torch.float16)

# Modeli GPU'ya taşı (varsa)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model.to(device)
print(f"Model will run on {device}.")

# Text generation pipeline oluştur
generator = pipeline("text-generation", model=model, tokenizer=tokenizer, device=0, max_new_tokens=500)

# Langchain LLM oluşturma
hf_llm = HuggingFacePipeline(pipeline=generator)

# Vektör mağazası ve retriever yapılandırma
vectorstore = LangchainPinecone(index=index,
                       text_key="content",
                       embedding=lambda text: embedding_model.embed_query(text))

retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

# Retrieval QA zinciri oluşturma
qa = RetrievalQA.from_chain_type(llm=hf_llm, chain_type="stuff", retriever=retriever, return_source_documents=True)
print("RetrievalQA zinciri başarıyla oluşturuldu!")


"""# 6. Sorgu Çalıştırma ve Yanıt Alma"""

# Kullanıcı sorgusunu işleme
def get_completion(prompt):
    # Gerçek sorgu işlemi, invoke metodunu kullanarak
    response = qa.invoke({"query": prompt, "max_new_tokens": 500})
    return response

## if-else + Prompt Engineering
# İçeriğe göre istemi dinamik olarak oluşturma işlevi
def generate_prompt(prompt):
    if "TOEFL" in prompt or "toefl" in prompt or "Toefl" in prompt:
        return f"Give an in-depth overview of TOEFL IBT exam: {prompt}"
    else:
        # Varsayılan istem davranışı
        return prompt
