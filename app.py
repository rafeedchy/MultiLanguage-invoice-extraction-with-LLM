from dotenv import load_dotenv

load_dotenv() # loads all the environment variables from the.env file

import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Function to load gemini pro vision model
model= genai.GenerativeModel('gemini_pro_vision')

def get_gemini_response(input, image, prompt):
    response = model.generate_content([input, image[0], prompt])
    return response.text

## Initialize streamlit app

st.set_page_config(page_title="Gemini Image Invoice Extractor")

st.header("Multi Language Image Invoice Extractor")
input = st.text_input("Input Prompt: ", key="input")
uploaded_file = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])
image = ""

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

submit = st.button("Extract Invoice")

