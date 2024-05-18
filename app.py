import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
load_dotenv()
from PIL import Image

# Configuration for Google Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Define the layout
st.set_page_config(page_title="All in One Ai Assistant")

# Create menu using sidebar
menu = ["Calorie Calculator", "Speech to Text", "Text to Speech", "Image to Text", "Chat Bot"]
choice = st.sidebar.radio("Select a task", menu)

def calorie_calculator():
    st.header("Calories Advisor APP")
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image.", use_column_width=True)

    submit = st.button("Calculate calories")

    input_prompt = """
    You are an expert nutritionist. See the food items from the image 
    and calculate the total calories. Provide details of
    every food item with calorie intake in the following format:

    1. Item 1 - number of calories
    2. Item 2 - number of calories
    ----
    ----
    Finally, mention whether the food is healthy or not and the percentage split of 
    carbohydrates, fats, fiber, sugar, and other components required in our diet.

    If there is no food item, say "Sorry, no food item present." 
    """

    if submit:
        image_data = input_image_setup(uploaded_file)
        response = get_gemini_response_for_image(input_prompt, image_data)
        st.header("The Response is")
        st.write(response)

def input_image_setup(uploaded_file):
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
        raise FileNotFoundError("No file uploaded")

def get_gemini_response_for_image(input_prompt, image):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input_prompt, image[0]])
    return response.text

# Placeholder functions for other tasks
def speech_to_text():
    st.header("Speech to Text Converter")
    # Implement your Speech to Text logic here

def text_to_speech():
    st.header("Text to Speech Converter")
    # Implement your Text to Speech logic here

def image_to_text():
    st.header("Image to Text Converter")
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image.", use_column_width=True)

    submit = st.button("Extract Text from Image")

    input_prompt = """
    You are an expert in image processing. Extract the text content from the image.
    If there is no text, say "Sorry, no text found in the image." 
    """

    if submit:
        image_data = input_image_setup(uploaded_file)
        response = get_gemini_response_for_image(input_prompt, image_data)
        st.header("Extracted Text")
        st.write(response)

def chat_bot():
    st.header("Chat Bot")
    # Implement your Chat Bot logic here

# Render the selected task
if choice == "Calorie Calculator":
    calorie_calculator()
elif choice == "Speech to Text":
    speech_to_text()
elif choice == "Text to Speech":
    text_to_speech()
elif choice == "Image to Text":
    image_to_text()
elif choice == "Chat Bot":
    chat_bot()
