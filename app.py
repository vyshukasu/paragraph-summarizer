import streamlit as st
from transformers import pipeline
from PIL import Image
import pytesseract
from transformers import BlipProcessor, BlipForConditionalGeneration

# Load pre-trained model for question-answering
qa_pipeline = pipeline('question-answering', model='distilbert-base-uncased-distilled-squad')

# Function to answer questions based on the context
def answer_question(context, question):
    response = qa_pipeline(question=question, context=context)
    return response['answer']

# Function to extract text from image using Tesseract OCR
def extract_text_from_image(image):
    try:
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        return str(e)

# Function to generate caption for image using BLIP model
def generate_image_caption(image):
    try:
        processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
        model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

        inputs = processor(image, return_tensors="pt")
        caption_ids = model.generate(**inputs)
        caption = processor.decode(caption_ids[0], skip_special_tokens=True)
        return caption
    except Exception as e:
        return str(e)

# Streamlit UI elements
st.title("Text and Image Summarization App")

# Text Summarization Section
st.header("Text-Based Question Answering")
context = st.text_area("Context", placeholder="Enter the context here...", height=200)
question = st.text_input("Question", placeholder="Enter your question here...")

if st.button("Get Answer"):
    if context and question:
        answer = answer_question(context, question)
        st.write(f"**Answer:** {answer}")
    else:
        st.write("Please provide both context and question.")

# Image Summarization Section
st.header("Image Summarization")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_column_width=True)
    
    st.write("Summarizing the image...")
    
    text = extract_text_from_image(image)
    caption = generate_image_caption(image)
    
    st.subheader("Extracted Text:")
    st.write(text)

    st.subheader("Generated Caption:")
    st.write(caption)


