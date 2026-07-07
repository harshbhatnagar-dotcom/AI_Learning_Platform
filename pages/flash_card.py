import streamlit as st

from utils.vectordb import search
from utils.llm import llm
from utils.pydantic import Flashcards
from utils.sidebarhider import hide_sidebar
from utils.navigation import home_button


hide_sidebar()

st.set_page_config(
    page_title="Flashcards",
    page_icon="🃏"
)

st.title("🃏 AI Flashcards")

topic = st.text_input(
    "Topic",
    placeholder="e.g. Transformers"
)

num_cards = st.slider(
    "Number of Flashcards",
    min_value=5,
    max_value=20,
    value=10
)

if st.button("Generate Flashcards"):

    if not topic.strip():
        st.warning("Please enter a topic.")
        st.stop()

    with st.spinner("Creating Flashcards..."):

        flash_chunks = search(topic)

        system_prompt="""You are an expert flashcard maker. We have to make flashcards. You will receive certain chunks of 
text which will be according to the users topic. Yiu have to generate the flashcard from those chunks only and according
to users topic. You have to make quetions for front and answer for back.

Context=

{context}
"""

        context = "\n\n".join(
                f"Extract from {chunk['metadata']['source']}:\n{chunk['text']}"
                for chunk in flash_chunks
        )
        system_prompt = system_prompt.format(context=context)

        user_prompt=f"Make the flash cards of the topic {topic} and number of flash cards should be {num_cards}"

        flashcards = llm(
            user_prompt=user_prompt,
            system_prompt=system_prompt,
            response_format=Flashcards
        )

        st.session_state.flashcards = flashcards

# ---------------- Display Flashcards ---------------- #
if "flashcards" in st.session_state:

    st.header("Generated Flashcards")

    for i, card in enumerate(st.session_state.flashcards.flashcards, start=1):

        with st.expander(f"🃏 Flashcard {i}"):

            st.write(f"**Question:** {card.question}")

            with st.expander("Show Answer"):

                st.success(card.answer)

    flashcards_md = "# 🃏 AI Flashcards\n\n"

    for i, card in enumerate(st.session_state.flashcards.flashcards, start=1):

        flashcards_md += f"## Flashcard {i}\n\n"

        flashcards_md += f"### Front\n"
        flashcards_md += f"{card.question}\n\n"

        flashcards_md += f"### Back\n"
        flashcards_md += f"{card.answer}\n\n"

        flashcards_md += "---\n\n"
    

    st.download_button(
        "📕 Download Flashcards",
        flashcards_md,
        "flashcards.md",
        "text/markdown"
    )

home_button()