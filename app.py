import streamlit as st
import re
import matplotlib.pyplot as plt
import numpy as np
from openai import OpenAI
import json

# AIML API Setup
base_url = "https://api.aimlapi.com/v1"
api_key = st.secrets["API_KEY"]  # Use Streamlit secrets for secure API key storage

api = OpenAI(api_key=api_key, base_url=base_url)

def parse_whatsapp_chat(chat_text):
    messages = re.findall(r'(\d{1,2}/\d{1,2}/\d{2,4},? \d{1,2}:\d{2} [APap][Mm]) - (.*?): (.*)', chat_text)
    return messages

def analyze_chat(chat_text):
    system_prompt = "You are a relationship counselor. Analyze the given WhatsApp conversation and provide sentiment (positive or negative) for each message timestamp in JSON format."
    user_prompt = f"Here is a WhatsApp chat: \n\n{chat_text}\n\nProvide the output as JSON with keys 'timestamp' and 'sentiment'."
    try:
        completion = api.chat.completions.create(
            model="gpt-3.5-turbo",  # Changed to a supported model
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.7,
            max_tokens=1000,
        )
        return json.loads(completion.choices[0].message.content)
    except Exception as e:
        st.error(f"Error during API call: {e}")
        return []

st.title("WhatsApp Relationship Chat Analyzer with Sentiment Timeline")
st.write("Upload a WhatsApp chat to analyze sentiment variations over time.")

uploaded_file = st.file_uploader("Upload WhatsApp Chat (.txt)", type=["txt"])

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
