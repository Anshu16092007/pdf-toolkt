import streamlit as st
import requests
import json
import time
from datetime import datetime

# Page config (WhatsApp Look)
st.set_page_config(page_title="WhatsApp Live Chat", page_icon="💬", layout="centered")

# CSS for Chat View
st.markdown("""
    <style>
    .stApp { background-color: #efeae2; }
    .chat-bubble { padding: 10px 15px; border-radius: 10px; margin: 6px 0; max-width: 75%; word-wrap: break-word; font-family: sans-serif; display: block;}
    .my-msg { background-color: #d9fdd3; margin-left: auto; border-top-right-radius: 0px; box-shadow: 0 1px 0.5px rgba(0,0,0,0.13); text-align: left; }
    .other-msg { background-color: #ffffff; margin-right: auto; border-top-left-radius: 0px; box-shadow: 0 1px 0.5px rgba(0,0,0,0.13); text-align: left; }
    .chat-time { font-size: 0.70em; color: #667781; text-align: right; margin-top: 4px; }
    .user-tag { font-weight: bold; font-size: 0.80em; color: #111b21; margin-bottom: 2px; }
    </style>
""", unsafe_allow_html=True)

BASE_URL = "https://kvdb.io/MN86S8pYg7gUqLpU8Xv6b9/anshu_final_chat_room"

def get_chat_id(u1, u2):
    return "_".join(sorted([u1.lower(), u2.lower()]))

def load_chats(chat_id):
    try:
        res = requests.get(f"{BASE_URL}_{chat_id}", timeout=3)
        if res.status_code == 200: return res.json()
        return []
    except: return []

def save_chats(chat_id, history):
    try: requests.post(f"{BASE_URL}_{chat_id}", json=history, timeout=3)
    except: pass

# Sidebar Setup
st.sidebar.header("👤 Profile Setup")
current_user = st.sidebar.text_input("Apna Naam Likhein:", value="Anshu").strip()
chat_with = st.sidebar.text_input("Dost Ka Naam Likhein:", value="Dost").strip()

if not current_user or not chat_with:
    st.sidebar.error("Kripya dono naam fill karein!")
    st.stop()

st.title(f"📱 Live Chat: {current_user} ↔️ {chat_with}")
room_id = get_chat_id(current_user, chat_with)

# Input Form
with st.form("message_form", clear_on_submit=True):
    msg_text = st.text_input("Type a message...", placeholder="Yahan apna message likhein...")
    submit = st.form_submit_button("Send 🚀")

if submit and msg_text.strip():
    current_history = load_chats(room_id)
    new_msg = {
        "sender": current_user,
        "text": msg_text.strip(),
        "timestamp": datetime.now().strftime("%I:%M %p")
    }
    current_history.append(new_msg)
    save_chats(room_id, current_history)
    st.rerun()

# Load Live Chats
live_messages = load_chats(room_id)

st.write("---")
if not live_messages:
    st.info("Yahan koi purani chat nahi hai. Shuruat kijiye!")
else:
    for msg in live_messages:
        if msg['sender'].lower() == current_user.lower():
            st.markdown(f"""
                <div class="chat-bubble my-msg"><div class="user-tag">You</div>
                <div>{msg['text']}</div><div class="chat-time">{msg['timestamp']}</div></div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div class="chat-bubble other-msg"><div class="user-tag">{msg['sender']}</div>
                <div>{msg['text']}</div><div class="chat-time">{msg['timestamp']}</div></div>
            """, unsafe_allow_html=True)

time.sleep(2)
st.rerun()