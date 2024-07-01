import streamlit as st
import os
import tempfile
from PyPDF2 import PdfReader
from docx import Document
from googlesearch import search

# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    with open(pdf_file, 'rb') as f:
        pdf = PdfReader(f)
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    return text

# Function to extract text from DOCX
def extract_text_from_docx(docx_file):
    doc = Document(docx_file)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return '\n'.join(full_text)

# Function to count words and characters
def count_words_characters(text):
    words = text.split()
    return len(words), len(text)

# Function to search for keywords in text
def search_keywords(text, keyword):
    return text.lower().count(keyword.lower())

# Function to get meaning of a word using Google search
def get_word_meaning(word):
    try:
        urls = search(f"meaning of {word}", num_results=1)
        return next(urls)
    except StopIteration:
        return "Meaning not found"

# Main function to run Streamlit app
def main():
    st.title("Document Information Extractor")
    st.sidebar.title("Upload Options")
    uploaded_file = st.sidebar.file_uploader("Choose a file", type=['pdf', 'docx'])

    if uploaded_file is not None:
        # Save uploaded file to a temporary location
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        temp_file.close()
        with open(temp_file.name, 'wb') as f:
            f.write(uploaded_file.read())

        # Display file details in the sidebar
        st.sidebar.header("File Details:")
        st.sidebar.markdown(f"**Filename:** {uploaded_file.name}")
        st.sidebar.markdown(f"**FileType:** {uploaded_file.type}")

        # Check file type and perform appropriate actions
        if uploaded_file.type == "application/pdf":
            text = extract_text_from_pdf(temp_file.name)
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            text = extract_text_from_docx(temp_file.name)
        else:
            st.sidebar.error("Unsupported file type")
            st.stop()  # Stop execution if file type is unsupported

        # Display extracted text
        st.header("Extracted Information:")
        st.text_area("Text from Document", text, height=400)

        # Additional functionalities
        st.header("Additional Information:")
        words_count, characters_count = count_words_characters(text)
        st.write(f"Number of Words: {words_count}")
        st.write(f"Number of Characters: {characters_count}")

        # Keyword search functionality
        st.header("Keyword Search:")
        keyword = st.text_input("Enter a keyword to search in the text:")
        if keyword:
            occurrences = search_keywords(text, keyword)
            st.write(f"Occurrences of '{keyword}': {occurrences}")

        # Search for word meaning using Google search
        st.header("Word Meaning Search:")
        word_to_search = st.text_input("Enter a word to find its meaning:")
        if word_to_search:
            meaning = get_word_meaning(word_to_search)
            if meaning == "Meaning not found":
                st.error(meaning)
            else:
                st.write(f"Meaning of '{word_to_search}': {meaning}")

        # Download option for extracted text
        st.markdown("---")
        st.header("Download Extracted Text:")
        st.markdown(get_download_link(text, uploaded_file.name), unsafe_allow_html=True)

        # Clean up temporary file
        os.remove(temp_file.name)

def get_download_link(text, filename):
    # Create a download link for the extracted text
    temp_filename = f"{filename.split('.')[0]}_extracted.txt"
    with open(temp_filename, 'w', encoding='utf-8') as f:
        f.write(text)
    with open(temp_filename, 'rb') as f:
        data = f.read()
    return f'<a href="data:application/octet-stream;base64,{data}" download="{temp_filename}">Click here to download</a>'

if __name__ == "__main__":
    main()
