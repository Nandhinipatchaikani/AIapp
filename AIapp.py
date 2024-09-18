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
bg_image_path = "nan ai (5).png"
bg_image_base64 = get_base64_image(bg_image_path)

# CSS to add background image, center buttons, and move them down
page_bg_img = f'''
<style>
.stApp {{
    background-image: url("data:image/png;base64,{bg_image_base64}");
    background-size: cover;
    background-repeat: no-repeat;
    background-attachment: fixed;
}}

button {{
    margin-top: 2cm; /* Move buttons 3 cm down */
}}

.center-container {{
    display: flex;
    justify-content: center;
    align-items: center;
    margin-top: 1.7cm; /* Adjust this value to move the buttons down */
}}

.stButton button {{
    width: 200px;
    height: 50px;
    font-size: 18px;
}}
</style>
'''

# Inject the CSS
st.markdown(page_bg_img, unsafe_allow_html=True)

def query_flux(payload):
    response = requests.post(API_URL_FLUX, headers=headers, json=payload)
    return response.content
