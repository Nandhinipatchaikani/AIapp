import requests
import streamlit as st
from PIL import Image
import io
import google.generativeai as genai
import base64  # To encode the image for inline display

# API URLs and headers
API_URL_FLUX = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-schnell"
API_URL_IMAGE_CAPTIONING = "https://api-inference.huggingface.co/models/nlpconnect/vit-gpt2-image-captioning"

headers = {"Authorization": "Bearer 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"}

genai.configure(api_key="AIzaSyAuRvJW_U07AUx3BACR8NggK0L1ZAxcA-g")


# Function to load and encode the background image in base64
def get_base64_image(file_path):
    with open(file_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()


# Use a local image file path
bg_image_path = "Ai (2).png"
bg_image_base64 = get_base64_image(bg_image_path)

# CSS to add background image
page_bg_img = f'''
<style>
.stApp {{
    background-image: url("data:image/png;base64,{bg_image_base64}");
    background-size: cover;
    background-repeat: no-repeat;
    background-attachment: fixed;
}}
</style>
'''

# Inject the CSS
st.markdown(page_bg_img, unsafe_allow_html=True)

def query_flux(payload):
    response = requests.post(API_URL_FLUX, headers=headers, json=payload)
    return response.content

def query_image_captioning(file):
    data = file.read()
    response = requests.post(API_URL_IMAGE_CAPTIONING, headers=headers, data=data)
    return response.json()[0]["generated_text"]

def text_to_image():
    prompt = st.text_input("Enter your Imagination : ")
    image_bytes = query_flux({"inputs": prompt})
    image = Image.open(io.BytesIO(image_bytes))
    if st.button("Generate Image"):
        st.image(image)
    if st.button("Back to Home"):
        st.session_state['page'] = 'home'
        st.rerun()

def image_to_text():
    st.title("Image Captioning")
    st.write("Upload an image file to get its caption")
    uploaded_file = st.file_uploader("Choose an image file", type=["jpg", "png", "jpeg"])
    if uploaded_file:
        st.image(uploaded_file)
        output = query_image_captioning(uploaded_file)
        st.write("Picture says:")
        st.markdown(f"<font face='Times New Roman' color='white'>{output.capitalize()}</font>", unsafe_allow_html=True)
    if st.button("Back to Home"):
        st.session_state['page'] = 'home'
        st.rerun()

def ask_question():
    model = genai.GenerativeModel('gemini-pro')
    chat = model.start_chat(history=[])
    text = st.text_input("Enter your question")
    if st.button("Ask Question"):
        response = chat.send_message(text)
        st.write(response.text)
    if st.button("Back to Home"):
        st.session_state['page'] = 'home'
        st.rerun()

def navigation():
    if 'page' not in st.session_state:
        st.session_state['page'] = 'home'
    if st.session_state['page'] == 'home':
        show_home()
    elif st.session_state['page'] == 'analysis':
        text_to_image()
    elif st.session_state['page'] == 'contact':
        image_to_text()
    elif st.session_state['page'] == 'ask_question':
        ask_question()

def show_home():
    col1, col2, col3 = st.columns(3)
    if col1.button("Ask Question"):
        st.session_state['page'] = 'ask_question'
        st.rerun()
    if col2.button("Text to Image"):
        st.session_state['page'] = 'analysis'
        st.rerun()
    if col3.button("Image to Text"):
        st.session_state['page'] = 'contact'
        st.rerun()

navigation()
