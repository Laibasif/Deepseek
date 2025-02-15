import streamlit as st
import re
import json
from openai import OpenAI

# AIML API Setup
base_url = "https://api.aimlapi.com/v1"
api_key = "39d93d91365e40fd916a0cfc3e79e929"  # Replace with your actual API key

api = OpenAI(api_key=api_key, base_url=base_url)

# Function to clean and extract messages from WhatsApp chat
def parse_whatsapp_chat(chat_text):
    messages = re.findall(r'\d{1,2}/\d{1,2}/\d{2,4},? \d{1,2}:\d{2} [APap][Mm] - (.*?): (.*)', chat_text)
    formatted_messages = "\n".join([f"{user}: {msg}" for user, msg in messages])
    return formatted_messages

# Function to evaluate relationship chat and extract emotional metrics
def analyze_chat_with_metrics(chat_text):
    system_prompt = "You are an AI relationship counselor. Analyze the WhatsApp chat and provide a JSON object with percentages for respect, loyalty, kindness, selfishness, and overall emotional tone. Ensure the output is valid JSON format without additional text."
    user_prompt = f"Here is a WhatsApp chat: \n\n{chat_text}\n\nProvide the output as a JSON object with keys 'respect', 'loyalty', 'kindness', 'selfishness', and 'emotions'. Ensure it is valid JSON."

    completion = api.chat.completions.create(
        model="mistralai/Mistral-7B-Instruct-v0.2",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.7,
        max_tokens=500,
    )

    return json.loads(completion.choices[0].message.content)

# Streamlit App UI
st.title("WhatsApp Relationship Chat Analyzer with Emotional Graph")
st.write("Upload a WhatsApp chat to analyze potential relationship metrics like respect, loyalty, kindness, selfishness, and overall emotions.")

uploaded_file = st.file_uploader("Upload WhatsApp Chat (.txt)", type=["txt"])

if uploaded_file is not None:
    chat_text = uploaded_file.read().decode("utf-8")
    cleaned_chat = parse_whatsapp_chat(chat_text)

    if st.button("Analyze Chat"):
        with st.spinner("Analyzing chat..."):
            metrics = analyze_chat_with_metrics(cleaned_chat)

        st.subheader("Analysis Result:")
        st.write(metrics)

        st.subheader("Emotional Metrics:")
        for key, value in metrics.items():
            st.metric(label=key.capitalize(), value=f"{value}%")

        st.success("Analysis completed successfully.")
