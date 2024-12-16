### README

This directory contains the files and configuration needed for the **Learnify** application using Gradio. The application provides various tools and functionalities for language learning and exam preparation.

---

#### Files:

1. **`learnify_gr.py`**:
   - This is the main script for the Learnify application.
   - It sets up the user interface using Gradio and HTML.
   - Defines the base URL for the application’s images.
   - Creates interactive buttons for different features:
     - **TOEFL Reading**, **TOEFL Listening**, **TOEFL Speaking**, **TOEFL Writing** - each with a corresponding image and link to the respective generators.
     - **Lea** - A language model for answering TOEFL IBT questions.
     - **Mirai** - A model for sentiment analysis and generating motivational sentences.
   - Launches the main page with Gradio’s `share=True` option to make the application accessible via a shareable link.

2. **`button_images/`**:
   - Contains the image files used for the buttons.
   - Images are linked via the base URL defined in `learnify_gr.py`.

3. **`requirements.txt`**:
   - Lists the necessary Python packages required to run the Learnify application.
   - Ensure to install these dependencies using `pip install -r requirements.txt` before running `learnify_gr.py`.

#### Usage:
1. Make sure you have Python installed.
2. Install the required packages listed in `requirements.txt`.
3. Run `learnify_gr.py` to start the application.
4. The application will be available at the link provided by Gradio.

#### Customization:
- You can customize the button images and URLs in `learnify_gr.py` to suit your requirements.
- Modify the button HTML templates if you need different styling or additional features.
- Adjust the Gradio blocks or the Markdown content to add more functionalities or information to the main page.
