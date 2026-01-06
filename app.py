import streamlit as st
from google import genai

st.title("私のAIアプリ")

# 秘密の鍵を読み込む
api_key = st.secrets["GEMINI_API_KEY"]
client = genai.Client(api_key=api_key)

# ---------------------------------------------------------
# 【ここが重要！】AI Studioの「System Instructions」を以下に貼り付けます
# ---------------------------------------------------------
my_instruction = """
ここにAI Studioからコピーした文章をそのまま貼り付けてください
"""
# ---------------------------------------------------------

user_input = st.text_input("AIに聞きたいことを入力してね")

if st.button("送信"):
    if user_input:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            config={'system_instruction': my_instruction},
            contents=user_input
        )
        st.write(response.text)
    else:
        st.warning("何か文字を入力してください")
