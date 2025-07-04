import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai
import time

# Load environment variables
load_dotenv()

# Configure Streamlit page settings
st.set_page_config(
    page_title="My AI Chatbot",
    page_icon="🤖",
    layout="centered"
)

# Simple CSS styling
st.markdown("""
<style>
    .main-header {
        background-color: #4CAF50;
        color: white;
        padding: 20px;
        text-align: center;
        border-radius: 5px;
        margin-bottom: 20px;
    }
    
    .info-box {
        background-color: #e7f3ff;
        border: 1px solid #b3d9ff;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    
    .stat-box {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        padding: 10px;
        margin: 5px 0;
        border-radius: 3px;
    }
</style>
""", unsafe_allow_html=True)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Set up Google Gemini AI model
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# Function to translate roles between Gemini and Streamlit terminology
def translate_role_for_streamlit(user_role):
    if user_role == "model":
        return "assistant"
    else:
        return user_role

# Initialize chat session and stats
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])
if "message_count" not in st.session_state:
    st.session_state.message_count = 0
if "start_time" not in st.session_state:
    st.session_state.start_time = time.time()

# Simple Header
st.markdown("""
<div class="main-header">
    <h1>🤖 My AI Chatbot</h1>
    <p>Ask me anything!</p>
</div>
""", unsafe_allow_html=True)

# Simple sidebar
st.sidebar.title("📋 Information")

# Show basic stats
st.sidebar.markdown("**Chat Info:**")
st.sidebar.markdown(f"Messages: {st.session_state.message_count}")

session_time = int(time.time() - st.session_state.start_time)
minutes = session_time // 60
seconds = session_time % 60
st.sidebar.markdown(f"Time: {minutes}m {seconds}s")

st.sidebar.markdown("Model: Gemini Flash")

# Simple clear button
if st.sidebar.button("Clear Chat"):
    st.session_state.chat_session = model.start_chat(history=[])
    st.session_state.message_count = 0
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.markdown("**How to use:**")
st.sidebar.markdown("• Type your question below")
st.sidebar.markdown("• Press Enter to send")
st.sidebar.markdown("• Wait for AI response")

# Welcome message
if len(st.session_state.chat_session.history) == 0:
    st.markdown("""
    <div class="info-box">
        <h3>👋 Hello!</h3>
        <p>Welcome to my AI chatbot. I can help you with questions, homework, coding, and more!</p>
        <p><strong>Try asking:</strong> "What is Python?" or "Help me with math"</p>
    </div>
    """, unsafe_allow_html=True)

# Display chat history
for message in st.session_state.chat_session.history:
    with st.chat_message(translate_role_for_streamlit(message.role)):
        st.markdown(message.parts[0].text)

# Input for user message
user_prompt = st.chat_input("Type your message here...")

if user_prompt:
    # Update message count
    st.session_state.message_count += 1
    
    # Show user message
    st.chat_message("user").markdown(user_prompt)

    # Get AI response
    try:
        with st.spinner("AI is thinking..."):
            gemini_response = st.session_state.chat_session.send_message(user_prompt)
        
        # Show AI response
        with st.chat_message("assistant"):
            st.markdown(gemini_response.text)
            
    except Exception as e:
        if "ResourceExhausted" in str(e) or "429" in str(e):
            st.error("Too many requests! Please wait and try again.")
        else:
            st.error(f"Error: {str(e)}")

# Simple footer
st.markdown("---")
st.markdown("*Made with Streamlit and Google AI* 🚀")