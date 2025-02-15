import streamlit as st
import re
import matplotlib.pyplot as plt
import numpy as np
from openai import OpenAI
import json

# AIML API Setup
base_url = "https://api.aimlapi.com/v1"
api_key = "39d93d91365e40fd916a0cfc3e79e929"  # Replace with your actual API key

api = OpenAI(api_key=api_key, base_url=base_url)

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
        
        st.subheader("Analysis Result:")
        st.write(analysis_result)
if uploaded_file is not None:
    chat_text = uploaded_file.read().decode("utf-8")
    messages = parse_whatsapp_chat(chat_text)
    if st.button("Analyze Chat"):
        with st.spinner("Analyzing chat..."):
            sentiment_data = analyze_chat("\n".join([f"{ts} - {user}: {msg}" for ts, user, msg in messages]))
        if sentiment_data:
            st.subheader("Sentiment Analysis Over Time:")
            timestamps = [item['timestamp'] for item in sentiment_data]
            sentiments = [1 if item['sentiment'] == 'positive' else -1 for item in sentiment_data]
            plt.figure(figsize=(10, 5))
            plt.plot(timestamps, sentiments, marker='o')
            plt.xlabel('Time')
            plt.ylabel('Sentiment (Positive=1, Negative=-1)')
            plt.title('Sentiment Variation Over Time')
            plt.xticks(rotation=45)
            plt.grid(True)
            st.pyplot(plt)

st.warning("Ensure that the API key is set in Streamlit secrets or provide a default one.")
