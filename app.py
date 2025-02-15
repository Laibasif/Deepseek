import streamlit as st
import re
from openai import OpenAI

# AIML API Setup
base_url = "https://api.aimlapi.com/v1"
api_key = "f614cad0fabe42bd8f287a921066b771"  # Replace with your actual API key

api = OpenAI(api_key="f614cad0fabe42bd8f287a921066b771", base_url="https://api.aimlapi.com/v1")
# ... existing code ...

# Function to evaluate relationship chat and analyze behavior statistics
# ... existing code ...

# Function to clean and extract messages from WhatsApp chat
def parse_whatsapp_chat(chat_text):
    try:
        messages = re.findall(r'\d{1,2}/\d{1,2}/\d{2,4},? \d{1,2}:\d{2} [APap][Mm] - (.*?): (.*)', chat_text)
        formatted_messages = "\n".join([f"{user}: {msg}" for user, msg in messages])
        return formatted_messages
    except Exception as e:
        st.error(f"Error parsing chat: {e}")
        return ""

# Streamlit App UI
st.title("WhatsApp Relationship Chat Analyzer")
st.write("Upload a WhatsApp chat to analyze potential red flags, toxicity, and areas for improvement.")

uploaded_file = st.file_uploader("Upload WhatsApp Chat (.txt)", type=["txt"])

if uploaded_file is not None:
    try:
        chat_text = uploaded_file.read().decode("utf-8")
        st.write("Chat text loaded successfully.")
    except Exception as e:
        st.error(f"Error reading file: {e}")
        chat_text = ""

    if chat_text:
        cleaned_chat = parse_whatsapp_chat(chat_text)
        
        if st.button("Analyze Chat"):
            with st.spinner("Analyzing chat..."):
                analysis_result, behavior_stats = analyze_chat(cleaned_chat)
            
            st.subheader("Analysis Result:")
            st.write(analysis_result)
            
            st.subheader("Behavior Statistics:")
            st.write("Respectful: ", behavior_stats["respectful"])
            st.write("Toxic: ", behavior_stats["toxic"])
            st.write("Angry: ", behavior_stats["angry"])
            st.write("Kind: ", behavior_stats["kind"])
