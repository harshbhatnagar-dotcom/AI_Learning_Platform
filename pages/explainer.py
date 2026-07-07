import streamlit as st

from utils.llm import llm
from utils.vectordb import search
from utils.sidebarhider import hide_sidebar
from utils.navigation import home_button

hide_sidebar()

st.set_page_config(
    page_title="Concept Explainer",
    page_icon="💡"
)

st.title("💡 AI Concept Explainer")

# Check if document exists
if "document_text" not in st.session_state:
    st.warning("⚠️ Please upload a document first.")
    st.stop()

concept = st.text_input(
    "Enter the concept you want to understand",
    placeholder="e.g. Gradient Descent"
)

explanation_style = st.selectbox(
    "Explanation Style",
    [
        "Beginner",
        "Intermediate",
        "Advanced",
        "Step-by-Step",
        "Real-Life Example",
        "Exam Oriented"
    ]
)


if st.button("Explain"):

    if not concept.strip():
        st.warning("Enter a concept.")
        st.stop()

    with st.spinner("Searching your notes..."):

        # Retrieve relevant chunks
        retrieved_chunks = search(concept)

        system_prompt="""You are an expert tutor. We are working on explaining the concepts to the students in easy way with example.\
You will receive certain text and you have to explain the concept only according to the information present in the text an with \
accordance to the query the student has passed.
If the information is not present in the text for what the user has asked for said 'No Information is present in your document'.\
Give examples with real life. Use this Context

Context:

{context}
"""
        context = "\n\n".join(
        f"Extract from {chunk['metadata']['source']}:\n{chunk['text']}"
        for chunk in retrieved_chunks
        )
        system_prompt = system_prompt.format(context=context)

        user_prompt = f"""
Question:

Explain {concept} in {explanation_style} style.
"""

        answer = llm(user_prompt,system_prompt)

        st.success("Done!")

        st.markdown(answer)

home_button()