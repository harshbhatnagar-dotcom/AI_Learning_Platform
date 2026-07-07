import streamlit as st

from utils.vectordb import search
from utils.pydantic import Topics
from utils.llm import llm
from utils.sidebarhider import hide_sidebar
from utils.navigation import home_button


hide_sidebar()

st.set_page_config(
    page_title="Study Plan",
    page_icon="📅"
)

st.title("📅 AI Study Planner")

goal = st.selectbox(
    "Study Goal",
    [
        "Learn from Scratch",
        "Revision",
        "Exam Preparation"
    ]
)

days = st.number_input(
    "Number of Days",
    min_value=1,
    max_value=365,
    value=30
)

hours = st.number_input(
    "Study Hours Per Day",
    min_value=1,
    max_value=12,
    value=2
)

focus = st.text_input(
    "Focus Topic (Optional)",
    placeholder="e.g. Transformers"
)

summary_text=st.session_state.setdefault("summary", "")

if st.button("Generate Study Plan"):

    with st.spinner("Generating Study Plan..."):   

        # ---------------- Generate Topics ---------------- #

        system_prompt="You will be give a set of notes from whoch you will generate the list of all topics. Do not give any explaination \
just generate the list of topics."

        user_prompt=f"""
            These are the notes

            {summary_text}

            You will generate the list of all the topics
            """

        topics=llm(system_prompt,user_prompt,response_format=Topics)

        # ---------------- Generate Study Plan ---------------- #

        system_prompt="""
You are an expert study planner. You have to generate the study plan for the topics provided to you . 

- Follow the topic order.
- Allocate more time to difficult topics and what the student have provided to make more focus on.
- Include revision days.
- Include practice sessions.
- Include quiz days.
- Balance the workload.
"""

        user_prompt=f"""
Create a study plane on the topics {topics.topics} and for {days} days for {hours} hours daily and the focus topic is {focus}
"""

        study_plan=llm(system_prompt,user_prompt)
        st.success("Study Plan Generated!")

        st.markdown(study_plan)


        st.download_button(
        label="📄 Download",
        data=study_plan,
        file_name="study_plan.md",
        mime="text/markdown"
    )

home_button()