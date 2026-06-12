import streamlit as st
import requests
import json
import time
from datetime import datetime

# Page configuration
st.set_page_config(page_title="WhatsApp Live", page_icon="💬", layout="centered")

# Custom CSS for UI
st.markdown("""
    <style>
    .stApp { background-color: #efeae2; }
    .chat-container { display: flex; flex-direction: column; }
    .chat-bubble { padding: 10px 15px; border-radius: 10px; margin: 4px 0; max-width: 75%; word-wrap: break-word; font-family: sans-serif; }
    .sender-bubble { background-color: #d9fdd3; align-self: flex-end; margin-left: auto; border-top-right-radius: 0px; box-shadow: 0 1px 0.5px rgba(0,0,0,0.13); }
    .receiver-bubble { background-color: #ffffff; align-self: flex-start; margin-right: auto; border-top-left-radius: 0px; box-shadow: 0 1px 0.5px rgba(0,0,0,0.13); }
    .chat-time { font-size: 0.70em; color: #667781; text-align: right; margin-top: 4px; }
    .user-tag { font-weight: bold; font-size: 0.80em; color: #111b21; margin-bottom: 2px; }
    </style>
""", unsafe_allow_html=True)

# Cloud Database URL (Ek unique key de di hai taaki data mix na ho)
BIN_URL = "https://kvdb.io/MN86S8pYg7gUqLpU8Xv6b9/anshu_chat_secure_box"

def load_chat_history():
    try:
        response = requests.get(BIN_URL, timeout=3) # Timeout lagaya taaki app hang na ho
        if response.status_code == 200:
            return response.json()
        return []
    except:
        return []

def save_chat_history(history):
    try:
        requests.post(BIN_URL, json=history, timeout=3)
    except:
        pass

# Sidebar Settings
st.sidebar.header("👤 Profile Setup")
current_user = st.sidebar.text_input("Apna Naam:", value="Anshu").strip()
chat_with = st.sidebar.text_input("Dost Ka Naam:", value="Dost").strip()

if not current_user or not chat_with:
    st.warning("Sidebar mein naam bharein!")
    st.stop()

st.title(f"📱 Live Chat: {current_user} ↔️ {chat_with}")

# Local state sync taaki chat instant loading dikhaye
if "local_chats" not in st.session_state:
    st.session_state.local_chats = load_chat_history()

# Form Input for sending messages
with st.form("chat_input_form", clear_on_submit=True):
    message_text = st.text_input("Type a message...", placeholder="Yahan apna message likhein...")
    send_btn = st.form_submit_button("Send 🚀")

if send_btn and message_text.strip():
    new_msg = {
        "sender": current_user,
        "receiver": chat_with,
        "text": message_text.strip(),
        "timestamp": datetime.now().strftime("%I:%M %p")
    }
    
    # Pehle instantly local screen par dikhao (No waiting!)
    st.session_state.local_chats.append(new_msg)
    
    # Phir cloud par save karo background mein
    save_chat_history(st.session_state.local_chats)
    st.rerun()

# Har 2 second mein database se naye messages pull karna
all_messages = load_chat_history()
if all_messages:
    st.session_state.local_chats = all_messages

# Filtering and displaying chat
relevant_messages = [
    msg for msg in st.session_state.local_chats 
    if (msg['sender'] == current_user and msg['receiver'] == chat_with) or 
       (msg['sender'] == chat_with and msg['receiver'] == current_user)
]

st.write("---")
if not relevant_messages:
    st.info("Koi purani chat nahi hai. Chating shuru karein!")
else:
    for msg in relevant_messages:
        if msg['sender'] == current_user:
            st.markdown(f"""
                <div class="chat-bubble sender-bubble">
                    <div class="user-tag">You</div>
                    <div>{msg['text']}</div>
                    <div class="chat-time">{msg['timestamp']}</div>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div class="chat-bubble receiver-bubble">
                    <div class="user-tag">{msg['sender']}</div>
                    <div>{msg['text']}</div>
                    <div class="chat-time">{msg['timestamp']}</div>
                </div>
            """, unsafe_allow_html=True)

# Screen automatic live refresh logic
time.sleep(2)
st.rerun()