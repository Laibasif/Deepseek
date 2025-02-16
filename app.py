import streamlit as st
import re
from openai import OpenAI
import matplotlib.pyplot as plt

# AIML API Setup
base_url = "https://api.aimlapi.com/v1"
api_key = "f614cad0fabe42bd8f287a921066b771"  # Replace with your actual API key

api = OpenAI(api_key="f614cad0fabe42bd8f287a921066b771", base_url="https://api.aimlapi.com/v1")

# Function to clean and extract messages from WhatsApp chat
def parse_whatsapp_chat(chat_text):
    messages = re.findall(r'\d{1,2}/\d{1,2}/\d{2,4},? \d{1,2}:\d{2} [APap][Mm] - (.*?): (.*)', chat_text)
    formatted_messages = "\n".join([f"{user}: {msg}" for user, msg in messages])
    return formatted_messages

# Function to evaluate relationship chat
def analyze_chat(chat_text):
    system_prompt = "You are a relationship counselor. Analyze the given WhatsApp conversation and provide insights on potential red flags, toxicity, and room for improvement in behavior."
    user_prompt = f"Here is a WhatsApp chat: \n\n{chat_text}\n\nProvide a structured analysis."

    completion = api.chat.completions.create(
        model="mistralai/Mistral-7B-Instruct-v0.2",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.7,
        max_tokens=500,
    )

    return completion.choices[0].message.content

# Function to extract behavior statistics from analysis
def extract_behavior_statistics(analysis_content):
    behavior_stats = {
        "respectful": 0,
        "toxic": 0,
        "angry": 0,
        "kind": 0
    }
    # Example: Count occurrences of specific keywords
    behavior_stats["respectful"] = analysis_content.lower().count("respectful")
    behavior_stats["toxic"] = analysis_content.lower().count("toxic")
    behavior_stats["angry"] = analysis_content.lower().count("angry")
    behavior_stats["kind"] = analysis_content.lower().count("kind")
    
    return behavior_stats

# Streamlit App UI
st.set_page_config(page_title="WhatsApp Relationship Chat Analyzer", layout="wide")
st.title("📱 WhatsApp Relationship Chat Analyzer")
st.write("Upload a WhatsApp chat to analyze potential red flags, toxicity, and areas for improvement.")

uploaded_file = st.file_uploader("Upload WhatsApp Chat (.txt)", type=["txt"])

if uploaded_file is not None:
    chat_text = uploaded_file.read().decode("utf-8")
    cleaned_chat = parse_whatsapp_chat(chat_text)
    
    if st.button("Analyze Chat"):
        with st.spinner("Analyzing chat..."):
            analysis_result = analyze_chat(cleaned_chat)
            behavior_stats = extract_behavior_statistics(analysis_result)
        
        st.subheader("🔍 Analysis Result:")
        st.write(analysis_result)
        
        st.subheader("📊 Behavior Statistics:")
        st.write("Respectful: ", behavior_stats["respectful"])
        st.write("Toxic: ", behavior_stats["toxic"])
        st.write("Angry: ", behavior_stats["angry"])
        st.write("Kind: ", behavior_stats["kind"])
        
        # Plotting behavior statistics
        fig, ax = plt.subplots()
        ax.bar(behavior_stats.keys(), behavior_stats.values(), color=['green', 'red', 'orange', 'blue'])
        ax.set_ylabel('Count')
        ax.set_title('Behavior Statistics')
        st.pyplot(fig)
