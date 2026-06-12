import streamlit as st
import time
from datetime import datetime

# Page Configuration (WhatsApp Look)
st.set_page_config(page_title="WhatsApp Live Chat", page_icon="💬", layout="centered")

# Custom CSS for Perfect Left/Right Chat Alignment
st.markdown("""
    <style>
    .stApp { background-color: #efeae2; }
    .chat-container { display: flex; flex-direction: column; width: 100%; }
    .chat-bubble { padding: 10px 15px; border-radius: 10px; margin: 5px 0; max-width: 70%; word-wrap: break-word; font-family: sans-serif; display: block; }
    .my-msg { background-color: #d9fdd3; margin-left: auto; border-top-right-radius: 0px; box-shadow: 0 1px 0.5px rgba(0,0,0,0.13); text-align: left; }
    .other-msg { background-color: #ffffff; margin-right: auto; border-top-left-radius: 0px; box-shadow: 0 1px 0.5px rgba(0,0,0,0.13); text-align: left; }
    .chat-time { font-size: 0.70em; color: #667781; text-align: right; margin-top: 4px; }
    .user-tag { font-weight: bold; font-size: 0.80em; color: #111b21; margin-bottom: 2px; }
    </style>
""", unsafe_allow_html=True)

# In-memory Storage Initialize (Bina kisi lag ke chalne ke liye)
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Sidebar Setup
st.sidebar.header(" Anshu's WhatsApp Setup")
current_user = st.sidebar.text_input("Apna Naam Likhein:", value="Anshu").strip()
chat_with = st.sidebar.text_input("Dost Ka Naam Likhein:", value="Dost").strip()

if not current_user or not chat_with:
    st.warning("Sidebar mein dono naam fill kariye!")
    st.stop()

st.title(f"📱 Live Chat: {current_user} ↔️ {chat_with}")

# Input Box for Typing Message
with st.form("chat_input_form", clear_on_submit=True):
    message_text = st.text_input("Type a message...", placeholder="Yahan apna message likhein...")
    send_btn = st.form_submit_button("Send 🚀")

# Message Send Logic
if send_btn and message_text.strip():
    new_msg = {
        "sender": current_user,
        "receiver": chat_with,
        "text": message_text.strip(),
        "timestamp": datetime.now().strftime("%I:%M %p")
    }
    st.session_state.chat_history.append(new_msg)
    st.rerun()

st.write("---")

# Filter Messages for current chat room
filtered_messages = [
    msg for msg in st.session_state.chat_history
    if (msg['sender'].lower() == current_user.lower() and msg['receiver'].lower() == chat_with.lower()) or
       (msg['sender'].lower() == chat_with.lower() and msg['receiver'].lower() == current_user.lower())
]

# Display Chat History
if not filtered_messages:
    st.info("Koi purani chat nahi hai. Message bhej kar shuruat karein!")
else:
    for msg in filtered_messages:
        if msg['sender'].lower() == current_user.lower():
            # Agar aapne bheja toh Right Side Green Bubble
            st.markdown(f"""
                <div class="chat-bubble my-msg">
                    <div class="user-tag">You</div>
                    <div>{msg['text']}</div>
                    <div class="chat-time">{msg['timestamp']}</div>
                </div>
            """, unsafe_allow_html=True)
        else:
            # Agar samne wale ne bheja toh Left Side White Bubble
            st.markdown(f"""
                <div class="chat-bubble other-msg">
                    <div class="user-tag">{msg['sender']}</div>
                    <div>{msg['text']}</div>
                    <div class="chat-time">{msg['timestamp']}</div>
                </div>
            """, unsafe_allow_html=True)

# Auto Refresh to keep UI live
time.sleep(1)
st.rerun()