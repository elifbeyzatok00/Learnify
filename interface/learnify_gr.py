import os
import gradio as gr

# Define the base URL for the images
base_url = "http://localhost:8000"

with gr.Blocks() as main_page:
    gr.Markdown("# I Learnify Study") 

    # HTML ile özelleştirilmiş butonlar
    toefl_reading_button_html = f"""
    <button onclick="window.open('http://127.0.0.1:7861')" style="border:none; background-color:transparent;">
        <img src="{base_url}/reading_button_image.png" alt="TOEFL Reading Question Generator" width="580" height="704">
    </button>
    """
    toefl_listening_button_html = f"""
    <button onclick="window.open('#')" style="border:none; background-color:transparent;">
        <img src="{base_url}/off_listening_button_image.png" alt="TOEFL Listening Question Generator" width="580" height="704">
    </button>
    """
    toefl_speaking_button_html = f"""
    <button onclick="window.open('#')" style="border:none; background-color:transparent;">
        <img src="{base_url}/off_speaking_button_image.png" alt="TOEFL Speaking Question Generator" width="580" height="704">
    </button>
    """
    toefl_writing_button_html = f"""
    <button onclick="window.open('#')" style="border:none; background-color:transparent;">
        <img src="{base_url}/off_writing_button_image.png" alt="TOEFL Writing Question Generator" width="580" height="704">
    </button>
    """
    
    lea_button_html = f"""
    <button onclick="window.open('http://127.0.0.1:7860')" style="border:none; background-color:transparent;">
        <img src="{base_url}/Lea_button_image.png" alt="Lea RAG Model" width="923" height="739">
    </button>
    """
    
    mirai_button_html = f"""
    <button onclick="window.open('http://127.0.0.1:7861')" style="border:none; background-color:transparent;">
        <img src="{base_url}/off_mirai_button_image.png" alt="Mirai Sentiment Analysis Motivation Sentence Generator" width="1032" height="581">
    </button>
    """

    gr.Markdown("## Generate your own TOEFL exam questions and get answers:")
    # Butonları göster
    with gr.Row():
        gr.HTML(toefl_reading_button_html)
        gr.HTML(toefl_listening_button_html)
        gr.HTML(toefl_speaking_button_html)
        gr.HTML(toefl_writing_button_html)
        

    gr.Markdown("## Lea 🐝")
    gr.Markdown("Lea is a language model that can answer your questions about the TOEFL IBT exam.")
    # Butonları göster
    with gr.Row():
        gr.HTML(lea_button_html)
        
    gr.Markdown("## Mirai ✨")
    gr.Markdown("Mirai analyzes your emotions in your prompt and generates personalized motivational sentences for you.")
    # Butonları göster
    with gr.Row():
        gr.HTML(mirai_button_html)
        

# Ana sayfa çalıştırılıyor
main_page.launch(share=True)
