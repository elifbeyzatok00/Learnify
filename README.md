# Learnify

Learnify is a comprehensive project designed to facilitate learning through various tools and resources. It focuses on providing support for TOEFL exam preparation and other language learning tasks.

## Features

- **TOEFL Reading Question Generator**:

  - Generates TOEFL-style reading passages, questions, and explanations using advanced AI models.
  - Provides customizable question types and allows export to PDF.

- **Lea RAG Model**:

  - Answers student questions about the TOEFL IBT exam and provides language exam preparation techniques using a Retrieval-Augmented Generation (RAG) model.

- **Learnify Website**:
  - A Gradio-powered interface to access and navigate between the tools easily.

---

## Video

[Project UI Video](https://drive.google.com/file/d/1wNj_IrGTSx-3KhoQtOoPwxCnNhNzznx4/view?usp=sharing)

---

## Installation

To install all dependencies, run the following command in the project root:

```bash
pip install -r requirements.txt
```

---

## Project Structure

```plaintext
- interface/
    - button_images
    - learnify_gr.py
    - requirements.txt
- lea_rag_model/
    - rag_dataset
    - README.md
    - lea.py
    - lea_gr.py
    - lea_st.py
    - requirements.txt
- toefl_question_generator/toefl_reading_question_generator/
    - assets
    - datasets
    - README.md
    - TOEFL_Reading_Content.pdf
    - model.ipynb
    - requirements.txt
    - toefl_reading_gr.py
    - toefl_reading_practise.py
- .env.sample
- .gitignore
- LICENSE
- README.md
```

---

## Usage

### Install Dependencies

Ensure you have all the required dependencies installed by running:

```bash
pip install -r requirements.txt
```

### Run the Project

Navigate to the appropriate directory and run the necessary scripts as follows:

1. **Start the RAG Model**:

   ```bash
   cd lea_rag_model
   python lea_gr.py
   ```

2. **Start the Question Generator Model**:

   ```bash
   cd toefl_question_generator/toefl_reading_question_generator
   python toefl_reading_gr.py
   ```

3. **Start the Learnify Website**:

   ```bash
   python learnify_gr.py
   ```

---

## License

This project is proprietary, and all rights are reserved by the author. It is not licensed for external use.

---

## Contact

For any questions or feedback, please contact us at elifbeyzatok@gmail.com.
