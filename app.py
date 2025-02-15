import streamlit as st
import re
from openai import OpenAI
import pandas as pd
import matplotlib.pyplot as plt
from textblob import TextBlob

# AIML API Setup
base_url = "https://api.aimlapi.com/v1"
api_key = "f614cad0fabe42bd8f287a921066b771"  # Replace with your actual API key

api = OpenAI(api_key="f614cad0fabe42bd8f287a921066b771", base_url="https://api.aimlapi.com/v1")

def parse_whatsapp_chat(chat_text):
    messages = re.findall(r'\d{1,2}/\d{1,2}/\d{2,4},? \d{1,2}:\d{2} [APap][Mm] - (.*?): (.*)', chat_text)
    formatted_messages = "\n".join([f"{user}: {msg}" for user, msg in messages])
    return formatted_messages

def analyze_chat(chat_text):
    system_prompt = "You are a relationship counselor. Analyze the given WhatsApp conversation and provide insights on potential red flags, toxicity, and room for improvement in behavior."
    user_prompt = f"Here is a WhatsApp chat: \n\n{chat_text}\n\nProvide a structured analysis."
    completion = api.chat.completions.create(
        model="mistralai/Mistral-7B-Instruct-v0.2",
    fig, ax = plt.subplots()
    ax.plot(sentiment_over_time.index, sentiment_over_time.values, marker='o')
    ax.set_xlabel('Date')
    ax.set_ylabel('Sentiment Score')
    ax.set_title('Sentiment Trend Over Time')
    st.pyplot(fig)

    if sentiment_over_time.iloc[-1] > sentiment_over_time.iloc[0]:
        st.success("Overall, the behavior showed a **positive change** over time! 😊")
    else:
        st.error("The behavior showed a **negative change** over time. 😔")

# This function can be called after parsing the chat to display statistics.
