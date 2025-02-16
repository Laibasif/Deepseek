import streamlit as st
import re
from openai import OpenAI

# AIML API Setup
base_url = "https://api.aimlapi.com/v1"
api_key = "f614cad0fabe42bd8f287a921066b771"  # Replace with your actual API key

api = OpenAI(api_key="f614cad0fabe42bd8f287a921066b771", base_url="https://api.aimlapi.com/v1")
# ... existing code ...

# ... existing code ...

# Function to extract behavior statistics from analysis
def extract_behavior_statistics(analysis_content):
    # This is a placeholder function. You need to implement logic to parse
    # the analysis_content and extract statistics for each behavior type.
    # For example, you might use regex or NLP techniques to count occurrences
    # of keywords related to each behavior type.
    behavior_stats = {
        "respectful": 0,
        "toxic": 0,
        "angry": 0,
        "kind": 0
    }
    # Implement logic to fill behavior_stats based on analysis_content
    # Example: Count occurrences of specific keywords
    behavior_stats["respectful"] = analysis_content.lower().count("respectful")
    behavior_stats["toxic"] = analysis_content.lower().count("toxic")
    behavior_stats["angry"] = analysis_content.lower().count("angry")
    behavior_stats["kind"] = analysis_content.lower().count("kind")
    
    return behavior_stats

# Streamlit App UI
st.title("WhatsApp Relationship Chat Analyzer")
st.write("Upload a WhatsApp chat to analyze potential red flags, toxicity, and areas for improvement.")

uploaded_file = st.file_uploader("Upload WhatsApp Chat (.txt)", type=["txt"])

if uploaded_file is not None:
    chat_text = uploaded_file.read().decode("utf-8")
    cleaned_chat = parse_whatsapp_chat(chat_text)
    
    if st.button("Analyze Chat"):
        with st.spinner("Analyzing chat..."):
            analysis_result = analyze_chat(cleaned_chat)
            behavior_stats = extract_behavior_statistics(analysis_result)
        
        st.subheader("Analysis Result:")
        st.write(analysis_result)
        
        st.subheader("Behavior Statistics:")
        st.write("Respectful: ", behavior_stats["respectful"])
        st.write("Toxic: ", behavior_stats["toxic"])
        st.write("Angry: ", behavior_stats["angry"])
        st.write("Kind: ", behavior_stats["kind"])
