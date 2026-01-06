import streamlit as st
import google.generativeai as genai

# タイトル
st.title("私のAIアプリ")

# 秘密の鍵を読み込む設定
api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

# 入力欄
user_input = st.text_input("AIに聞きたいことを入力してね")

# ボタンを押したら実行
if st.button("送信"):
    response = model.generate_content(user_input)
    st.write(response.text)
