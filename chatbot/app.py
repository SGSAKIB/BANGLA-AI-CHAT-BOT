import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

# 🔑 Load API Key
load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")

if not API_KEY:
    st.error("❌ OPENAI_API_KEY পাওয়া যায়নি। দয়া করে `.env` ফাইলে API key লিখুন।")
    st.stop()

client = OpenAI(api_key=API_KEY)

# Streamlit Config
st.set_page_config(page_title="বাংলা এআই চ্যাটবট 🤖", page_icon="🤖", layout="centered")

# Custom Dark CSS
st.markdown("""
    <style>
        .stApp {
            background-color: #121212;
            font-family: 'Noto Sans Bengali', sans-serif;
            color: #f1f1f1;
        }
        .chat-bubble-user {
            background-color: #1e88e5;
            color: white;
            padding: 12px 16px;
            border-radius: 18px;
            margin: 6px 0;
            text-align: right;
            display: inline-block;
            max-width: 75%;
            box-shadow: 0px 3px 6px rgba(0,0,0,0.3);
        }
        .chat-bubble-ai {
            background-color: #2c2c2c;
            color: #f1f1f1;
            padding: 12px 16px;
            border-radius: 18px;
            margin: 6px 0;
            text-align: left;
            display: inline-block;
            max-width: 75%;
            border: 1px solid #444;
            box-shadow: 0px 3px 6px rgba(0,0,0,0.3);
        }
        .chat-container {
            max-height: 65vh;
            overflow-y: auto;
            padding: 12px;
            border-radius: 12px;
            background-color: #1a1a1a;
            margin-bottom: 10px;
        }
        .stTextInput input {
            font-size: 16px;
            padding: 10px;
            border-radius: 8px;
            background-color: #2c2c2c;
            color: #f1f1f1;
            border: 1px solid #444;
        }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown("<h2 style='text-align:center; color:#90caf9;'>🤖 বাংলা এআই চ্যাটবট BY SAKIB </h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:gray;'>💬 বাংলায় প্রশ্ন করো, এআই উত্তর দেবে</p>", unsafe_allow_html=True)

# Sidebar options
st.sidebar.title("⚙️ Options")

# Clear Chat
if st.sidebar.button("🗑️ Clear Chat"):
    st.session_state.messages = [
        {"role": "system", "content": "তুমি একজন সহায়ক AI অ্যাসিস্ট্যান্ট, সব উত্তর বাংলায় দেবে।"}
    ]
    st.rerun()


# Export Chat
if st.sidebar.button("📄 Export Chat"):
    if "messages" in st.session_state and len(st.session_state.messages) > 1:
        chat_text = ""
        for msg in st.session_state.messages[1:]:
            speaker = "👤 User" if msg["role"] == "user" else "🤖 AI"
            chat_text += f"{speaker}: {msg['content']}\n\n"

        st.download_button(
            label="⬇️ Download Chat (TXT)",
            data=chat_text,
            file_name="chat_history.txt",
            mime="text/plain"
        )
    else:
        st.sidebar.warning("⚠️ কোনো চ্যাট পাওয়া যায়নি!")

# Initialize session
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "তুমি একজন সহায়ক AI অ্যাসিস্ট্যান্ট, সব উত্তর বাংলায় দেবে।"}
    ]

# Show chat
st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
for msg in st.session_state.messages[1:]:
    if msg["role"] == "user":
        st.markdown(f"<div class='chat-bubble-user'>👤 {msg['content']}</div>", unsafe_allow_html=True)
    elif msg["role"] == "assistant":
        st.markdown(f"<div class='chat-bubble-ai'>🤖 {msg['content']}</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# Input
prompt = st.chat_input("এখানে লিখুন...")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.markdown(f"<div class='chat-bubble-user'>👤 {prompt}</div>", unsafe_allow_html=True)

    # AI উত্তর (streaming)
    reply = ""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=st.session_state.messages,
        stream=True
    )

    reply_placeholder = st.empty()
    for chunk in response:
        if chunk.choices[0].delta.content:
            text = chunk.choices[0].delta.content
            reply += text
            reply_placeholder.markdown(f"<div class='chat-bubble-ai'>🤖 {reply}</div>", unsafe_allow_html=True)

    st.session_state.messages.append({"role": "assistant", "content": reply})
