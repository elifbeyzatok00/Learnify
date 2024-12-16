### Lea RAG Model README

This directory contains the files and configuration needed for the **Lea RAG Model** application. The application utilizes a Retrieval-Augmented Generation (RAG) model to provide answers to questions about the TOEFL IBT exam based on a dataset of documents.

---

#### Files:

1. **`lea_rag_model/`**:
   - Contains the main files for the Lea RAG Model application.

2. **`rag_dataset/`**:
   - Directory containing the dataset documents (PDFs and DOCX files) used for the model.
   - The dataset is processed and indexed into Pinecone for efficient retrieval during queries.

3. **`README.md`**:
   - This README file provides an overview of the Lea RAG Model application and its components.

4. **`lea.py`**:
   - Contains the core functionality of the Lea RAG Model.
   - Functions include document loading and processing, Pinecone indexing, and embedding.
   - Configures the RAG setup, including the choice of model and tokenizer for text generation.

5. **`lea_gr.py`**:
   - Contains the Gradio interface for the Lea RAG Model.
   - Provides a simple web-based user interface to input questions about the TOEFL IBT exam.
   - Interacts with `lea.py` to process questions and generate responses.

6. **lea_st.py**:
- Contains additional supporting scripts for the Lea RAG Model.
- Typically includes utility functions and configurations specific to the model setup.
- Originally designed to support a Streamlit UI, but it is not currently used in the project.

7. **`requirements.txt`**:
   - Lists the necessary Python packages required to run the Lea RAG Model application.
   - Install these dependencies using `pip install -r requirements.txt` before running the application.

---

#### Usage:

1. **Environment Setup**:
   - Ensure you have Python installed.
   - Install the required packages listed in `requirements.txt`.
   - Create a `.env` file in the root directory to store environment variables (`PINECONE_API_KEY`, `PINECONE_ENVIRONMENT`, `HUGGING_FACE_TOKEN`).

2. **Running the Application**:
   - Run `lea.py` to process the documents and configure the Pinecone index.
   - Launch `lea_gr.py` to start the Gradio interface, which allows users to input questions about the TOEFL IBT exam.
   - The Gradio interface will be accessible at the URL provided by `gr.Blocks().launch()`.

3. **Customization**:
   - You can modify the `lea.py` file to customize the embedding model, the Pinecone index settings, and the RAG setup.
   - Adjust the Gradio interface in `lea_gr.py` to change the appearance and behavior of the web application.

#### Additional Notes:
- The Lea RAG Model is built using a combination of document processing, embedding, and a retrieval-augmented generation setup, utilizing the capabilities of Pinecone and Hugging Face.
- For any issues or contributions, please refer to the code files and the README for guidance on how to extend and enhance the model.
