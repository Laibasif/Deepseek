import streamlit as st
import re
from openai import OpenAI
from textblob import TextBlob
import pandas as pd
import matplotlib.pyplot as plt

# AIML API Setup
base_url = "https://api.aimlapi.com/v1"
api_key = "39d93d91365e40fd916a0cfc3e79e929"  # Replace with your actual API key

api = OpenAI(api_key=api_key, base_url=base_url)

# Function to clean and extract messages from WhatsApp chat
def parse_whatsapp_chat(chat_text):
    messages = re.findall(r'\d{1,2}/\d{1,2}/\d{2,4},? \d{1,2}:\d{2} [APap][Mm] - (.*?): (.*)', chat_text)
    data = []
    for user, msg in messages:
        date = re.search(r'\d{1,2}/\d{1,2}/\d{2,4}', chat_text).group()
        data.append((date, user, msg, TextBlob(msg).sentiment.polarity))
    return pd.DataFrame(data, columns=['Date', 'User', 'Message', 'Sentiment'])

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

# Plot sentiment over time
def plot_sentiment(df):
    df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y')
    df_grouped = df.groupby('Date').mean()
    plt.figure(figsize=(10, 5))
    plt.plot(df_grouped.index, df_grouped['Sentiment'], marker='o', linestyle='-', color='b')
    plt.title('Sentiment Trend Over Time')
    plt.xlabel('Date')
    plt.ylabel('Sentiment Score')
    plt.grid(True)
    st.pyplot(plt)

# Streamlit App UI
st.title("WhatsApp Relationship Chat Analyzer")
st.write("Upload a WhatsApp chat to analyze potential red flags, toxicity, and areas for improvement.")

uploaded_file = st.file_uploader("Upload WhatsApp Chat (.txt)", type=["txt"])

if uploaded_file is not None:
    chat_text = uploaded_file.read().decode("utf-8")
    df = parse_whatsapp_chat(chat_text)

    if st.button("Analyze Chat"):
        with st.spinner("Analyzing chat..."):
            analysis_result = analyze_chat(chat_text)
        
        st.subheader("Analysis Result:")
        st.write(analysis_result)
        
        st.subheader("Sentiment Analysis Over Time:")
        plot_sentiment(df)
