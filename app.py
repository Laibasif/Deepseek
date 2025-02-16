import streamlit as st
import re
from openai import OpenAI

# AIML API Setup
base_url = "https://api.aimlapi.com/v1"
api_key = "f614cad0fabe42bd8f287a921066b771"  # Replace with your actual API key

api = OpenAI(api_key="f614cad0fabe42bd8f287a921066b771", base_url="https://api.aimlapi.com/v1")

# Function to clean and extract messages from WhatsApp chat
def parse_whatsapp_chat(chat_text):
    messages = re.findall(r'\d{1,2}/\d{1,2}/\d{2,4},? \d{1,2}:\d{2} [APap][Mm] - (.*?): (.*)', chat_text)
    formatted_messages = "\n".join([f"{user}: {msg}" for user, msg in messages])
    return formatted_messages

# ... existing code ...

# Function to evaluate relationship chat
def analyze_chat(chat_text):
    system_prompt = (
        "You are a highly skilled relationship counselor. "
        "Analyze the given WhatsApp conversation with a focus on identifying "
        "communication patterns, emotional tone, and potential areas for improvement. "
        "Provide a detailed and structured analysis with examples."
    )
    user_prompt = f"Here is a WhatsApp chat: \n\n{chat_text}\n\nProvide a comprehensive analysis."

    completion = api.chat.completions.create(
        model="mistralai/Mistral-7B-Instruct-v0.2",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.5,  # Lower temperature for more deterministic responses
        max_tokens=750,   # Increase max tokens for more detailed responses
    )

    return completion.choices[0].message.content

# Function to extract behavior statistics from analysis
def extract_behavior_statistics(analysis_content):
    behavior_stats = {
        "respectful": 0,
        "toxic": 0,
        "angry": 0,
        "kind": 0,
        "supportive": 0,  # New category
        "dismissive": 0   # New category
    }
    # Improved keyword matching with context consideration
    behavior_stats["respectful"] = analysis_content.lower().count("respectful")
    behavior_stats["toxic"] = analysis_content.lower().count("toxic")
    behavior_stats["angry"] = analysis_content.lower().count("angry")
    behavior_stats["kind"] = analysis_content.lower().count("kind")
    behavior_stats["supportive"] = analysis_content.lower().count("supportive")
    behavior_stats["dismissive"] = analysis_content.lower().count("dismissive")
    
    return behavior_stats

