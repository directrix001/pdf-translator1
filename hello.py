import streamlit as st
import fitz  # PyMuPDF
import tempfile
from googletrans import Translator
import os

# Function to translate text using Google Translate
def translate_text(text, target_language):
    translator = Translator()
    translated = translator.translate(text, dest=target_language)
    return translated.text

# Function to translate text in a PDF file and save the translated PDF
def translate_pdf_and_save(pdf_path, target_language):
    translated_pdf_path = f"translated_document_{target_language}.pdf"
    translated_doc = fitz.open()
    
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text = page.get_text()
            translated_text = translate_text(text, target_language)
            translated_page = translated_doc.new_page(width=page.rect.width, height=page.rect.height)
            translated_page.insert_text((10, 10), translated_text)
    
    translated_doc.save(translated_pdf_path)
    return translated_pdf_path

# Streamlit app
def main():
    st.title('PDF Translator 📃')
    st.write('Upload a PDF file and select the target language for translation.')

    uploaded_file = st.file_uploader("Choose a PDF file", type=['pdf'])

    target_language = st.selectbox('Select Target Language', ['english', 'fr', 'de', 'es'], index=0)

    if uploaded_file is not None:
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(uploaded_file.getvalue())
            temp_file_path = temp_file.name

        st.write('Translating... Please wait.')
        translated_pdf_path = translate_pdf_and_save(temp_file_path, target_language)
        st.write('Translation complete!')

        st.write('Translated PDF:')
        st.write(translated_pdf_path)

        # Downloadable button for the translated PDF
        download_button = st.download_button(
            label="Download Translated PDF",
            data=open(translated_pdf_path, "rb").read(),
            file_name="translated_document.pdf",
            mime="application/pdf"
        )

        temp_file.close()  
        os.unlink(temp_file_path) 

if __name__ == "__main__":
