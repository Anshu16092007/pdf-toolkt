import streamlit as st
import requests
import json
import time
from datetime import datetime

# Page Configuration (WhatsApp look dene ke liye)
st.set_page_config(page_title="WhatsApp Clone", page_icon="💬", layout="centered")

# WhatsApp Theme ke liye Custom CSS Styling
st.markdown("""
    <style>
    .stApp {
        background-color: #efeae2;
    }
    .chat-bubble {
        padding: 10px 15px;
        border-radius: 10px;
        margin: 5px 0;
        max-width: 75%;
        word-wrap: break-word;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
    .sender-bubble {
        background-color: #d9fdd3;
        align-self: flex-end;
        margin-left: auto;
        border-top-right-radius: 0px;
        box-shadow: 0 1px 0.5px rgba(0,0,0,0.13);
    }
    .receiver-bubble {
        background-color: #ffffff;
        align-self: flex-start;
        margin-right: auto;
        border-top-left-radius: 0px;
        box-shadow: 0 1px 0.5px rgba(0,0,0,0.13);
    }
    .chat-time {
        font-size: 0.75em;
        color: #667781;
        text-align: right;
        margin-top: 4px;
    }
    .user-tag {
        font-weight: bold;
        font-size: 0.85em;
        color: #111b21;
        margin-bottom: 2px;
    }
    </style>
""", unsafe_allow_html=True)

# Free cloud server storage to sync messages instantly between separate phones
BIN_URL = "https://kvdb.io/MN86S8pYg7gUqLpU8Xv6b9/whatsapp_chat_history_anshu"

def load_chat_history():
    try:
        response = requests.get(BIN_URL)
        if response.status_code == 200:
            return response.json()
        return []
    except:
        return []

def save_chat_history(history):
    try:
        requests.post(BIN_URL, json=history)
    except:
        pass

# App Headers
st.title("📱 Real-Time WhatsApp Chat")
st.write("Dono phones par ek sath live chat chalegi aur history safe rahegi.")

# Sidebar Settings: Sender aur Receiver setup karne ke liye
st.sidebar.header("👤 Profile Settings")
current_user = st.sidebar.text_input("Apna Naam Likhein:", value="Anshu").strip()
chat_with = st.sidebar.text_input("Kisse Chat Karni Hai?:", value="Dost").strip()

# Auto Refresh Time Control (Taki dusre phone ka message apne aap bina page reload kiye aa jaye)
st.sidebar.write("---")
st.sidebar.subheader("🔄 Live Sync Interval")
refresh_rate = st.sidebar.slider("Refresh Speed (Seconds)", 2, 10, 3)

if not current_user or not chat_with:
    st.warning("Kripya Sidebar mein apna aur apne dost ka naam set karein!")
    st.stop()

st.sidebar.success(f"Logged in as: **{current_user}**")
st.sidebar.info(f"Chatting with: **{chat_with}**")

st.write(f"### 💬 Conversation: {current_user} ↔️ {chat_with}")

# Chat messages display screen area
chat_placeholder = st.empty()

# Input messaging field at bottom
with st.form("chat_form", clear_on_submit=True):
    message_text = st.text_input("Type a message...", key="msg_input")
    send_btn = st.form_submit_button("Send 🚀")

if send_btn and message_text.strip():
    current_history = load_chat_history()
    
    # New chat data block
    new_msg = {
        "sender": current_user,
        "receiver": chat_with,
        "text": message_text.strip(),
        "timestamp": datetime.now().strftime("%I:%M %p")
    }
    
    current_history.append(new_msg)
    save_chat_history(current_history)
    st.rerun()

# Load and visually filter messages for this exact sender-receiver pair
all_messages = load_chat_history()

with chat_placeholder.container():
    relevant_messages = [
        msg for msg in all_messages 
        if (msg['sender'] == current_user and msg['receiver'] == chat_with) or 
           (msg['sender'] == chat_with and msg['receiver'] == current_user)
    ]
    
    if not relevant_messages:
        st.info("Yahan abhi tak koi chat nahi hui hai. Pehla message bhejiye!")
    else:
        for msg in relevant_messages:
            if msg['sender'] == current_user:
                # Green bubble for you
                st.markdown(f"""
                    <div class="chat-bubble sender-bubble">
                        <div class="user-tag">You</div>
                        <div>{msg['text']}</div>
                        <div class="chat-time">{msg['timestamp']}</div>
                    </div>
                """, unsafe_allow_html=True)
            else:
                # White bubble for the other person
                st.markdown(f"""
                    <div class="chat-bubble receiver-bubble">
                        <div class="user-tag">{msg['sender']}</div>
                        <div>{msg['text']}</div>
                        <div class="chat-time">{msg['timestamp']}</div>
                    </div>
                """, unsafe_allow_html=True)

# background infinite loop emulation to trigger instant live refresh
time.sleep(refresh_rate)
st.rerun()