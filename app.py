import streamlit as st
from transformers import pipeline

# Load pre-trained model for question-answering
qa_pipeline = pipeline('question-answering', model='distilbert-base-uncased-distilled-squad')

# Function to answer questions based on the context
def answer_question(context, question):
    response = qa_pipeline(question=question, context=context)
    return response['answer']

# Streamlit UI elements
st.title("Question-Answering Model")
st.write("Provide a context and a question. The model will give an answer based on the context.")

# Input fields for context and question
context = st.text_area("Context", placeholder="Enter the context here...", height=200)
question = st.text_input("Question", placeholder="Enter your question here...")

# Button to get the answer
if st.button("Get Answer"):
    if context and question:
        answer = answer_question(context, question)
        st.write(f"**Answer:** {answer}")
    else:
        st.write("Please provide both context and question.")

