import os
import streamlit as st

from utils.parser import extract_text
from utils.chunking import create_chunks
from utils.vectordb import store_to_vectordb, clear_db
from utils.sidebarhider import hide_sidebar
from utils.navigation import home_button

hide_sidebar()

st.set_page_config(
    page_title="Upload Documents",
    page_icon="📄"
)

st.title("📄 Upload Study Material")

st.write(
    "Upload one or more PDF, DOCX or PPTX files. "
    "All uploaded files will be treated as a single knowledge base."
)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def clear_uploads():
    if not os.path.exists(UPLOAD_FOLDER):
        return

    for file in os.listdir(UPLOAD_FOLDER):
        file_path = os.path.join(UPLOAD_FOLDER, file)

        if os.path.isfile(file_path):
            os.remove(file_path)

uploaded_files = st.file_uploader(
    "Choose Documents",
    type=["pdf", "docx", "pptx"],
    accept_multiple_files=True
)


if uploaded_files:

    if st.button("Process Documents"):

        with st.spinner("Processing documents..."):

            # Start a fresh study session
            clear_db()
            clear_uploads()

            combined_text = ""
            total_chunks = 0

            for uploaded_file in uploaded_files:

                save_path = os.path.join(
                    UPLOAD_FOLDER,
                    uploaded_file.name
                )

                # Save file
                with open(save_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())

                # Extract text
                text = extract_text(save_path)

                # Keep complete text for Summary page
                combined_text += (
                    f"\n\n========== {uploaded_file.name} ==========\n\n"
                )
                combined_text += text

                # Chunk the document
                chunks = create_chunks(text)

                # Store chunks in ChromaDB
                store_to_vectordb(
                    chunks=chunks,
                    filename=uploaded_file.name
                )

                total_chunks += len(chunks)

            # Save complete text in session
            st.session_state["document_text"] = combined_text
            st.session_state["uploaded_files"] = [
                file.name for file in uploaded_files
            ]

            st.success(
                f"Successfully processed {len(uploaded_files)} document(s)."
            )

            st.info(f"Total Chunks Stored: {total_chunks}")

            with st.expander("Preview Extracted Text"):
                st.write(combined_text[:3000])


home_button()
