import streamlit as st

from utils.vectordb import search
from utils.llm import llm
from utils.pydantic import Questions
from utils.sidebarhider import hide_sidebar
from utils.navigation import home_button

hide_sidebar()

st.set_page_config(
    page_title="AI Quiz Generator",
    page_icon="❓"
)

st.title("❓ AI Quiz Generator")

topic = st.text_input(
    "Topic",
    placeholder="e.g. Neural Networks"
)

num_questions = st.slider(
    "Number of Questions",
    min_value=5,
    max_value=20,
    value=10
)

difficulty = st.selectbox(
    "Difficulty",
    ["Easy", "Medium", "Hard"]
)

# ---------------- Generate Quiz ---------------- #

if st.button("Generate Quiz"):

    if not topic.strip():
        st.warning("Please enter a topic.")
        st.stop()

    with st.spinner("Generating Quiz..."):

        quiz_chunks = search(topic)

        system_prompt=""""You are an expert quiz maker. We are working on generating the quiz. You have to generate the quiz 
from the given chunks only which are selected according to users topic. Do not include concepts which are not present 
in the chunks and also do not include the topic other then for what user asked for.You have to provide the
4 options and the correct option also

Only include question according to the topic provided only. not with according to all the chunks but with according to topic.
context:

{context}
"""

        context = "\n\n".join(
        f"Extract from {chunk['metadata']['source']}:\n{chunk['text']}"
        for chunk in quiz_chunks
        )
        system_prompt = system_prompt.format(context=context)

        user_prompt=f"""Genarate the quiz with {num_questions} number of quetions with difficulty {difficulty} 
        on the topic {topic}.Provide quiz on this topic only"""

        quiz = llm(user_prompt,system_prompt,response_format=Questions)

        st.session_state.quiz = quiz
        st.session_state.submitted = False

# ---------------- Display Quiz ---------------- #

if "quiz" in st.session_state:

    st.divider()

    st.header("Quiz")

    quiz = st.session_state.quiz

    for i, q in enumerate(quiz.questions, start=1):

        st.subheader(f"Question {i}")

        st.write(q.question)

        st.radio(
            "Choose one option",
            q.options,
            key=f"answer_{i}"
        )

    if st.button("Submit Quiz"):

        st.session_state.submitted = True

# ---------------- Show Score ---------------- #

if st.session_state.get("submitted", False):

    score = 0

    st.divider()

    st.header("Results")

    quiz = st.session_state.quiz

    for i, q in enumerate(quiz.questions, start=1):

        selected = st.session_state[f"answer_{i}"]

        if selected == q.answer:
            score += 1
            st.success(f"✅ Question {i}: Correct")
        else:
            st.error(f"❌ Question {i}: Incorrect")

        st.write(f"**Question:** {q.question}")

        st.write(f"**Your Answer:** {selected}")

        st.write(f"**Correct Answer:** {q.answer}")

        st.divider()

    st.metric(
        "Final Score",
        f"{score}/{len(quiz.questions)}"
    )

    percentage = score / len(quiz.questions) * 100

    if percentage >= 80:
        st.balloons()
        st.success("🎉 Excellent!")
    elif percentage >= 60:
        st.info("👍 Good Job!")
    else:
        st.warning("📚 Keep practicing!")

home_button()