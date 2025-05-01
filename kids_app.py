import streamlit as st
import requests

# Replace this with your actual OpenRouter API key
API_KEY = "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"

st.set_page_config(page_title="Children's Story Generator")
st.title("📖 AI-Generated Children's Story")

# Prompt input
prompt = st.text_input("Enter a fun story idea for a child (e.g., 'a robot who learns to dance'): ")

if prompt:
    with st.spinner("Generating your story..."):
        # OpenRouter API call
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": "openai/gpt-3.5-turbo",  # You can change the model here
                "messages": [
                    {"role": "system", "content": "You are a friendly storyteller who writes fun, imaginative stories for kids aged 5-10."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.8
            }
        )

        if response.status_code == 200:
            story = response.json()["choices"][0]["message"]["content"]
            st.subheader("🌟 Your Story:")
            st.write(story)
        else:
            st.error(f"Something went wrong! Error code: {response.status_code}")
