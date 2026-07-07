import streamlit as st
from utils.sidebarhider import hide_sidebar

hide_sidebar()

st.set_page_config(
    page_title="AI Study Platform",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 AI Study Platform")
st.subheader("Your Personal AI Learning Assistant")

st.markdown("---")

st.markdown("""
Upload your study material and let AI help you learn faster.

### Features
- 📄 Upload Documents
- 📝 AI Summary
- 💡 Concept Explainer
- ❓ Quiz Generator
- 🃏 Flashcards
- 📅 Study Planner
- 💬 Chat with Notes (RAG)
""")

st.markdown("---")

st.header("🚀 Quick Navigation")

col1, col2 = st.columns(2)

with col1:

    if st.button("📄 Upload Documents", use_container_width=True):
        st.switch_page("pages/upload.py")

    if st.button("📝 AI Summary", use_container_width=True):
        st.switch_page("pages/summary.py")

    if st.button("💡 Concept Explainer", use_container_width=True):
        st.switch_page("pages/explainer.py")

    if st.button("❓ Quiz Generator", use_container_width=True):
        st.switch_page("pages/quiz.py")

with col2:

    if st.button("🃏 Flashcards", use_container_width=True):
        st.switch_page("pages/flash_card.py")

    if st.button("📅 Study Planner", use_container_width=True):
        st.switch_page("pages/study_planner.py")

st.markdown("---")

st.header("📊 Current Session")

col1, col2 = st.columns(2)

with col1:
    uploaded = "✅ Yes" if "document_text" in st.session_state else "❌ No"
    st.metric("Document Uploaded", uploaded)

with col2:
    if "document_text" in st.session_state:
        st.metric(
            "Characters Loaded",
            len(st.session_state["document_text"])
        )
    else:
        st.metric("Characters Loaded", 0)

st.markdown("---")

st.info(
    "💡 Tip: Start by uploading a document. Once processed, you can use "
    "Summary, Quiz, Flashcards, Study Planner, and Chat with Notes."
)