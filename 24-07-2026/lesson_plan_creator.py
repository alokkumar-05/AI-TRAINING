import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate

import os
from dotenv import load_dotenv
load_dotenv()

# Ensure the Groq API key is set
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

# Initialize the model
model = ChatGroq(model="llama-3.1-8b-instant")

# Streamlit UI Header
st.header("AI Lesson Plan Generator for Educators")
st.subheader("Easily craft structured lesson plans for any topic.")

# User Inputs
topic_input = st.text_input(
    "Enter the Topic/Concept", 
    placeholder="e.g., Photosynthesis, Newton's Laws of Motion, Introduction to Python Lists"
)

grade_input = st.selectbox(
    "Select Target Audience / Grade Level", 
    ["Elementary School", "Middle School", "High School", "Undergraduate", "Postgraduate"]
)

duration_input = st.selectbox(
    "Select Class Duration", 
    ["30 Minutes", "45 Minutes", "60 Minutes", "90 Minutes"]
)

# Prepare input dictionary
input_variables = {
    "topic": topic_input,
    "grade": grade_input,
    "duration": duration_input
}

# Prompt template tailored for lesson planning
template = PromptTemplate(
    template='''
    You are an expert curriculum developer and educator. Generate a detailed, highly structured lesson plan based on the following details:
    - Topic: "{topic}"
    - Target Audience/Grade Level: "{grade}"
    - Total Duration: "{duration}"

    The lesson plan must include the following sections:
    1. **Learning Objectives**: Define 2-3 clear, measurable learning outcomes (using Bloom's Taxonomy where applicable) appropriate for this grade level.
    2. **Prerequisites**: Briefly state what students should already know before this lesson.
    3. **Materials Needed**: List specific teaching aids, tools, or resources required.
    4. **Time Breakdown & Script**: Divide the total duration ({duration}) into realistic blocks (e.g., Introduction, Core Lecture/Activity, Guided Practice, Wrap-up/Quiz). For each block, provide a brief "Teacher's Script" or talking points.
    5. **Engagement Strategy**: Include at least one interactive activity, question, or analogy to keep the specific grade level engaged.
    6. **Assessment/Check for Understanding**: Suggest a quick method to verify that students grasped the concept at the end of the class.

    If the topic is too vague or impossible to teach, politely ask for more specific input. Maintain an encouraging, professional, and pedagogical tone.
    ''',
    input_variables=list(input_variables.keys())
)

# Execution Button
if st.button("Generate Lesson Plan"):
    if not topic_input.strip():
        st.error("Please enter a topic to generate the lesson plan.")
    else:
        with st.spinner("Designing your lesson plan..."):
            # Construct the LangChain chain
            chain = template | model
            result = chain.invoke(input_variables)
            
            st.success("Lesson Plan Generated!")
            st.markdown("---")
            st.subheader(f" Lesson Plan: {topic_input}")
            
            # Displaying the final text output
            st.write(result.content)