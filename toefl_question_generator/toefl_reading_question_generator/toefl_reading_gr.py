import gradio as gr
from toefl_reading_practise_test.py import (
    generate_toefl_text,
    generate_question,
    generate_explanations_answers,
    generate_toefl_pdf,
    question_types_count
)

def generate_toefl_reading_practise_test(topic, prose_summary_or_fill_table, factual_info, neg_factual_info, inference, rhetorical_purpose, vocabulary, reference, sentence_simplification):
    # Step 1: Generate TOEFL text
    generated_text = generate_toefl_text(topic)

    # Define question types based on user input
    q_type_counts = question_types_count(
        prose_summary_or_fill_table,
        factual_info,
        neg_factual_info,
        inference,
        rhetorical_purpose,
        vocabulary,
        reference,
        sentence_simplification
    )

    # Step 2: Generate Questions
    generated_questions = generate_question(generated_text, q_type_counts)

    # Step 3: Generate Explanations and Answers
    generated_explanations_answers = generate_explanations_answers(generated_text, generated_questions)

    # Step 4: Generate PDF and save path
    pdf_path = generate_toefl_pdf(generated_text, generated_questions, generated_explanations_answers, q_type_counts)

    return generated_text, generated_questions, generated_explanations_answers, pdf_path

# Gradio Interface
with gr.Blocks() as demo:
    gr.Markdown("# TOEFL Reading Question Generator")
    
    topic_input = gr.Textbox(label="Enter a topic for the reading passage")
    
    prose_summary_or_fill_table = gr.Dropdown(
        label="Prose Summary or Fill in a Table Question (Choose One)",
        choices=["Prose Summary", "Fill in a Table"]
    )
    factual_info = gr.Slider(2, 5, label="Number of Factual Information Questions", step=1)
    neg_factual_info = gr.Slider(0, 2, label="Number of Negative Factual Information Questions", step=1)
    inference = gr.Slider(1, 2, label="Number of Inference Questions", step=1)
    rhetorical_purpose = gr.Slider(1, 2, label="Number of Rhetorical Purpose Questions", step=1)
    vocabulary = gr.Slider(1, 2, label="Number of Vocabulary Questions", step=1)
    reference = gr.Slider(0, 2, label="Number of Reference Questions", step=1)
    sentence_simplification = gr.Slider(0, 1, label="Number of Sentence Simplification Questions", step=1)

    generate_button = gr.Button("Generate TOEFL Content")

    generated_text_output = gr.Textbox(label="Generated TOEFL Reading Passage", interactive=False)
    generated_questions_output = gr.Textbox(label="Generated Questions", interactive=False)
    explanations_answers_output = gr.Textbox(label="Explanations and Answers", interactive=False)
    pdf_download = gr.File(label="Download TOEFL PDF", interactive=False)

    # Link the function to Gradio interface
    generate_button.click(
        generate_toefl_content,
        inputs=[
            topic_input,
            prose_summary_or_fill_table,
            factual_info,
            neg_factual_info,
            inference,
            rhetorical_purpose,
            vocabulary,
            reference,
            sentence_simplification,
        ],
        outputs=[
            generated_text_output,
            generated_questions_output,
            explanations_answers_output,
            pdf_download
        ]
    )

# Launch the app
demo.launch()
