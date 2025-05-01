import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load API key securely
load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="Children's Story Generator")

# ✅ Add header image/logo
st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/2/2f/Storybook_Logo.svg/512px-Storybook_Logo.svg.png", width=150)

# ✅ Fancy headers
st.markdown("## 🌈 Welcome to StoryBuddy!")
st.markdown("Write a story idea and let the magic begin ✨")

# User input
prompt = st.text_input("🎨 Enter your story idea (e.g., 'a robot who learns to dance'): ")

if prompt:
    with st.spinner("Generating your magical story..."):
        # ✅ Generate story
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": "openai/gpt-3.5-turbo",
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a friendly storyteller who writes fun, imaginative stories for kids aged 5–10."
                    },
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.8
            }
        )

        if response.status_code == 200:
            story = response.json()["choices"][0]["message"]["content"]

            # ✅ Nicely formatted story
            st.markdown("#### 📚 Your Story:")
            st.markdown(f"```markdown\n{story}\n```")

            # ✅ Generate illustration
            st.subheader("🖼️ Story Illustration")
            image_prompt = f"A fun, colorful children's illustration of: {prompt}"
            image_response = requests.post(
                "https://openrouter.ai/api/v1/images/generations",
                headers={
                    "Authorization": f"Bearer {API_KEY}",
                    "Content-Type": "application/json",
                },
                json={
                    "prompt": image_prompt,
                    "n": 1,
                    "size": "512x512"
                }
            )

            if image_response.status_code == 200:
                image_url = image_response.json()["data"][0]["url"]
                st.image(image_url, caption="✨ AI-Generated Illustration", use_column_width=True)
            else:
                st.warning("Could not generate an illustration. Try again later.")
        else:
            st.error("Story generation failed. Try again.")