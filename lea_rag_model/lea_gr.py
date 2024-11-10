import gradio as gr
from lea import *  # Import all necessary functions

def process_question(prompt):
    if not prompt:
        return "Please write a question about TOEFL IBT exam."

    # Generate the modified prompt and get the completion
    modified_prompt = generate_prompt(prompt)
    response = get_completion(modified_prompt)  # Defined query processing function

    # Extract the full result
    full_result = response["result"]

    # Extract the "Helpful Answer" part
    start_index = full_result.find("Helpful Answer:")
    if start_index != -1:
        start_index += len("Helpful Answer:")
        
        # List all possible endings
        possible_endings = [
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
        ]

        # Find the smallest valid ending
        valid_endings = [end for end in possible_endings if end != -1]
        end_index = min(valid_endings) if valid_endings else len(full_result)
        helpful_answer = full_result[start_index:end_index].strip()
    else:
        helpful_answer = "No helpful answer found."

    # Prepare the answer and source documents to display
    sources = ""
    if "source_documents" in response:
        for doc in response["source_documents"]:
            sources += f"**Content:** {doc.page_content[:200]}...\n**Metadata:** {doc.metadata}\n\n"

    return helpful_answer, sources

# Set up Gradio interface
with gr.Blocks() as demo:
    gr.Markdown("# Lea RAG LLM Q&A App")
    prompt_input = gr.Textbox(label="Please write your question about TOEFL IBT exam here:")
    helpful_answer_output = gr.Textbox(label="Answer:")
    source_docs_output = gr.Textbox(label="Source Documents:")

    submit_button = gr.Button("Send")
    submit_button.click(process_question, inputs=prompt_input, outputs=[helpful_answer_output, source_docs_output])

demo.launch()
