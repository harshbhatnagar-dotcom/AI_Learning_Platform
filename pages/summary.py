import streamlit as st

from utils.chunking import create_chunks
from utils.llm import llm
from utils.sidebarhider import hide_sidebar
from utils.navigation import home_button

hide_sidebar()

st.set_page_config(
    page_title="AI Summary",
    page_icon="📝"
)

st.title("📝 AI Summary")

if "document_text" not in st.session_state:
    st.warning("Please upload a document first.")
    st.stop()

document = st.session_state["document_text"]

summary_type = st.selectbox(
    "Summary Type",
    [
        "Short Summary",
        "Detailed Summary",
        "Bullet Points",
        "Revision Notes"
    ]
)

if st.button("Generate Summary"):

    chunks = create_chunks(document)

    progress = st.progress(0)

    partial_summaries = []

    total_chunks = len(chunks)

    for i, chunk in enumerate(chunks):

        system_prompt=f"You are an expert tutor .We are working on creating the summary of the study material.\
        You create the summaries of {summary_type} type. Dont miss the important concepts."

        user_prompt=f"""Create the summary of the following content.\
                   Content :

                   {chunk}"""

        summary=llm(user_prompt,system_prompt)

        partial_summaries.append(summary)
        progress.progress((i + 1) / total_chunks)

    st.info("Creating final summary...")

    system_prompt=f"You are an expert note maker. You will have the part of summaries from the same document.\
You have to create the notes by combining all the summaries . DO not add your information. Dont miss the important concepts. \
You will give answer in beautifull markdown without markdown code block"
    
    user_prompt=f"Make the notes from the following part of summaries:\
    {partial_summaries}"

    final_summary = llm(user_prompt,system_prompt)

    st.success("Summary Generated!")


    st.markdown(final_summary)

    st.session_state["summary"] = final_summary


    st.download_button(
        label="📄 Download Summary",
        data=final_summary,
        file_name="summary.md",
        mime="text/markdown"
    )

home_button()