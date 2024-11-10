import streamlit as st
from lea import *  # Tüm fonksiyonları miras al

# Streamlit başlığı
st.title("Lea RAG LLM Q&A App")

# Kullanıcıdan prompt al
prompt = st.text_input("Please write your question about TOEFL IBT exam here:")


# Butona tıklayınca işlem başlasın
if st.button("Send"):
    if prompt:
        with st.spinner("Thinking..."):
            # fonksiyon kullanarak modified prompt üret
            modified_prompt = generate_prompt(prompt)
            response = get_completion(modified_prompt)  # Daha önce tanımladığınız sorgu işleme fonksiyonu
        
         # Tüm yanıtı al
        full_result = response["result"]

        # "Helpful Answer" kısmını ayıklamak için filtreleme yap
        start_index = full_result.find("Helpful Answer:")
        if start_index != -1:
            start_index += len("Helpful Answer:")
            
            # Tüm bitiş noktalarını listeleyelim
            possible_endings = [
                #full_result.find("\n", start_index),
                full_result.find('",', start_index),
                full_result.find("Inaccurate Answer:", start_index),
                full_result.find("Correct Answer:", start_index),
                full_result.find("Unhelpful Answer:", start_index),
                full_result.find("Don't know:", start_index),
                full_result.find("I don't know:", start_index),
                full_result.find("Informed Answer:", start_index),
                full_result.find("The best answer is", start_index),
                full_result.find("Unknown Answer:", start_index),
                full_result.find("Note:", start_index),
                full_result.find("Answer:", start_index),
                full_result.find("Answer to the question:", start_index),
                full_result.find("Question:", start_index)
                #full_result.find("\n\n", start_index),
            ]

            # Geçerli olan bitiş noktalarını seçip en küçüğünü bul
            valid_endings = [end for end in possible_endings if end != -1]
            if valid_endings:
                end_index = min(valid_endings)
            else:
                end_index = len(full_result)  # Eğer hiçbiri bulunmazsa metnin sonuna kadar al

            helpful_answer = full_result[start_index:end_index].strip()
        else:
            helpful_answer = "No helpful answer found."

        # Helpful Answer kısmını ekrana yazdır
        st.subheader("Answer:")
        st.write(helpful_answer)
        
        
        # Kaynak belgeleri göster
        if "source_documents" in response:
            st.subheader("Source Documents:")
            for doc in response["source_documents"]:
                st.write(f"**Content:** {doc.page_content[:200]}...")
                st.write(f"**Metadata:** {doc.metadata}")
    else:
        st.warning("Please write a question about TOEFL IBT exam.")
