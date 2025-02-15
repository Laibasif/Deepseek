import streamlit as st
import re
import pandas as pd

# Function to clean and extract messages from WhatsApp chat
def parse_whatsapp_chat(chat_text):
    messages = re.findall(r'\d{1,2}/\d{1,2}/\d{2,4},? \d{1,2}:\d{2} [APap][Mm] - (.*?): (.*)', chat_text)
    data = []
    for user, msg in messages:
        date = re.search(r'\d{1,2}/\d{1,2}/\d{2,4}', chat_text).group()
        data.append((date, user, msg))
    return pd.DataFrame(data, columns=['Date', 'User', 'Message'])

# Streamlit App UI
st.title("WhatsApp Relationship Chat Analyzer")
st.write("Upload a WhatsApp chat to analyze potential red flags, toxicity, and areas for improvement.")

uploaded_file = st.file_uploader("Upload WhatsApp Chat (.txt)", type=["txt"])

if uploaded_file is not None:
    chat_text = uploaded_file.read().decode("utf-8")
    df = parse_whatsapp_chat(chat_text)

    if st.button("Show Chat Statistics"):
        st.subheader("Chat Statistics:")
        st.write(df.groupby(['Date', 'User']).size().reset_index(name='Message Count'))
