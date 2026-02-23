import streamlit as st
import requests

API_BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Document QnA RAG", layout="wide")

st.title("📄 Document QnA - RAG System")

# Upload PDF
st.header("Upload PDF")

uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

if uploaded_file:
    with st.spinner("Uploading and processing..."):
        files = {"file": uploaded_file.getvalue()}
        response = requests.post(f"{API_BASE_URL}/upload-pdf", files={"file": uploaded_file})

        if response.status_code == 200:
            st.success("PDF uploaded and processed successfully!")
            st.json(response.json())
        else:
            st.error("Upload failed.")
            st.json(response.json())

# Ask Question 
st.header("Ask a Question")

question = st.text_input("Enter your question")

if st.button("Ask"):
    if question:
        with st.spinner("Generating answer..."):
            response = requests.post(
                f"{API_BASE_URL}/ask",
                params={"question": question}
            )

            if response.status_code == 200:
                answer = response.json()["answer"]
                st.success("Answer:")
                st.write(answer)
            else:
                st.error("Error while fetching answer.")
                st.json(response.json())