import streamlit as st
import os
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Groq Client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Page Configuration
st.set_page_config(page_title="AI Code Review & Rewrite Agent 🤖", layout="wide")

st.title("AI Code Review & Rewrite Agent 🤖")
st.markdown("---")

# Sidebar for inputs
with st.sidebar:
    st.header("Settings")
    language = st.selectbox("Select Language", ["Python", "JavaScript", "Java", "C++", "Other"])
    
    # Focus areas as per project requirements [cite: 289, 295]
    focus_areas = st.multiselect(
        "Focus Areas",
        ["Bugs & Errors", "Security Risks", "Performance Optimization", "Best Practices"],
        default=["Bugs & Errors"]
    )
    
    review_button = st.button("Analyze Code")
    rewrite_button = st.button("Rewrite & Optimize")

# Main Input Area
code_input = st.text_area("Paste your code here:", height=300, placeholder="Enter your code snippet...")

def get_ai_response(prompt):
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile", # Required model [cite: 234]
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3, # Optimized for precision [cite: 235]
            max_tokens=2000,
            top_p=0.9
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

# Logic for Review [cite: 122, 291]
if review_button:
    if code_input.strip():
        with st.spinner("Analyzing your code..."):
            focus_str = ", ".join(focus_areas)
            # Structured prompt as per project specifications [cite: 291]
            prompt = f"""
            You are an expert code reviewer with 15+ years of experience. 
            Analyze the following {language} code focusing on: {focus_str}.
            
            Please provide your review in the following structured format:
            ### Critical Issues
            ### High Priority
            ### Medium Priority
            ### Low Priority
            
            Code to analyze:
            ```{language}
            {code_input}
            ```
            """
            response = get_ai_response(prompt)
            st.subheader("Code Review Results")
            st.markdown(response)
    else:
        st.warning("Please paste some code first!")

# Logic for Rewriting [cite: 125, 126]
# Logic for Rewriting
if rewrite_button:
    if code_input.strip():
        with st.spinner("Refactoring..."):
            # Updated prompt to be strictly code-focused
            prompt = f"""
            Rewrite and optimize the following {language} code. 
            Fix bugs, improve efficiency, and follow best practices.
            
            IMPORTANT: Provide ONLY the rewritten code. 
            Do NOT include explanations, comments about changes, or 'Security/Performance' sections.
            
            Code to rewrite:
            ```{language}
            {code_input}
            ```
            """
            response = get_ai_response(prompt)
            st.subheader("Optimized Code")
            # This displays the code in a clean box with a copy button
            st.code(response.replace("```python", "").replace("```", ""), language=language.lower())
    else:
        st.warning("Please paste some code first!")