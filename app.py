import streamlit as st
import requests
import time
from datetime import datetime

# Page configuration for true WhatsApp feel
st.set_page_config(page_title="WhatsApp Live Chat", page_icon="💬", layout="centered")

# CSS Styling for Perfect Layout
st.markdown("""
    <style>
    .stApp { background-color: #efeae2; }
    .chat-bubble { padding: 10px 15px; border-radius: 10px; margin: 5px 0; max-width: 75%; word-wrap: break-word; font-family: sans-serif; display: block; }
    .my-msg { background-color: #d9fdd3; margin-left: auto; border-top-right-radius: 0px; box-shadow: 0 1px 0.5px rgba(0,0,0,0.13); text-align: left; }
    .other-msg { background-color: #ffffff; margin-right: auto; border-top-left-radius: 0px; box-shadow: 0 1px 0.5px rgba(0,0,0,0.13); text-align: left; }
    .chat-time { font-size: 0.70em; color: #667781; text-align: right; margin-top: 4px; }
    .user-tag { font-weight: bold; font-size: 0.80em; color: #111b21; margin-bottom: 2px; }
    </style>
""", unsafe_allow_html=True)

# Dedicated Free Online Server Database for Anshu's App
DB_URL = "https://kvdb.io/MN86S8pYg7gUqLpU8Xv6b9/anshu_final_perfect_chat"

def load_messages():
    try:
        response = requests.get(DB_URL, timeout=2)
        if response.status_code == 200: return response.json()
        return []
    except: return []

def save_messages(history):
    try: requests.post(DB_URL, json=history, timeout=2)
    except: pass

# Sidebar Setup
st.sidebar.header("👤 Profile Setup")
current_user = st.sidebar.text_input("Apna Naam Likhein:", value="Anshu").strip()
chat_with = st.sidebar.text_input("Dost Ka Naam Likhein:", value="Dost").strip()

if not current_user or not chat_with:
    st.warning("Sidebar mein dono naam likhna zaroori hai!")
    st.stop()

st.title(f"📱 Live Chat: {current_user} ↔️ {chat_with}")

# Form to send data
with st.form("chat_form", clear_on_submit=True):
    message_text = st.text_input("Type a message...", placeholder="Yahan apna message likhein...")
    send_btn = st.form_submit_button("Send 🚀")

if send_btn and message_text.strip():
    current_history = load_messages()
    new_msg = {
        "sender": current_user,
        "receiver": chat_with,
        "text": message_text.strip(),
        "timestamp": datetime.now().strftime("%I:%M %p")
    }
    current_history.append(new_msg)
    save_messages(current_history)
    st.rerun()

# Load and Filter Messages
all_messages = load_messages()
st.write("---")

filtered_messages = [
    msg for msg in all_messages
    if (msg['sender'].lower() == current_user.lower() and msg['receiver'].lower() == chat_with.lower()) or
       (msg['sender'].lower() == chat_with.lower() and msg['receiver'].lower() == current_user.lower())
]

if not filtered_messages:
    st.info("Abhi tak koi message nahi hai. Pehla message bhejiye!")
else:
    for msg in filtered_messages:
        if msg['sender'].lower() == current_user.lower():
            st.markdown(f"""
                <div class="chat-bubble my-msg">
                    <div class="user-tag">You</div>
                    <div>{msg['text']}</div>
                    <div class="chat-time">{msg['timestamp']}</div>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div class="chat-bubble other-msg">
                    <div class="user-tag">{msg['sender']}</div>
                    <div>{msg['text']}</div>
                    <div class="chat-time">{msg['timestamp']}</div>
                </div>
            """, unsafe_allow_html=True)

# 2 Seconds Auto Refresh loop to get new messages instantly
time.sleep(2)
st.rerun()