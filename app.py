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

def input_image_details(uploaded_file):
    if uploaded_file is not None:

        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise Exception("Please upload an image")

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

input_prompt= """
You are an expert at understanding invoices. We will upload an image as invoice and you will have to answere questions based on the uploaded invoice image. The language of the invoice could be non english but you will answer in English"""


# if submit button is clicked
if submit:
    image_data = input_image_details(uploaded_file)
    response = get_gemini_response(input_prompt, image_data, input)
    st.subheader("Gemini Response about the invoice: ")
    st.write(response)