import streamlit as st
import requests
import uuid
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Jarvis AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern styling
st.markdown("""
<style>
    /* Main container styling */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
    }
    
    /* Header styling */
    .header-container {
        padding: 2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }
    
    .header-title {
        font-size: 2.5em;
        font-weight: bold;
        margin: 0;
        background: linear-gradient(135deg, #fff 0%, #f0f0f0 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .header-subtitle {
        font-size: 1.1em;
        margin-top: 0.5rem;
        opacity: 0.9;
        color: white;
    }
    
    /* Message styling */
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 12px;
        padding: 12px 16px;
        margin: 8px 0;
        box-shadow: 0 2px 10px rgba(102, 126, 234, 0.2);
        word-wrap: break-word;
        text-align: right;
    }
    
    .assistant-message {
        background: white;
        color: #333;
        border-radius: 12px;
        padding: 12px 16px;
        margin: 8px 0;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        border-left: 4px solid #667eea;
        word-wrap: break-word;
    }
    
    /* Input styling */
    .stChatInput {
        border-radius: 12px !important;
        border: 2px solid #667eea !important;
        box-shadow: 0 2px 10px rgba(102, 126, 234, 0.1) !important;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border-radius: 8px !important;
        padding: 10px 24px !important;
        font-weight: 500 !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3) !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4) !important;
    }
    
    /* Sidebar styling */
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #f8f9ff 0%, #f0f4ff 100%);
    }
    
    /* Info box */
    .info-box {
        background: rgba(102, 126, 234, 0.1);
        border-left: 4px solid #667eea;
        border-radius: 8px;
        padding: 16px;
        margin: 16px 0;
        color: #333;
    }
</style>
""", unsafe_allow_html=True)

# API endpoint
API = "http://localhost:8000/chat"

# Initialize session state
if "session" not in st.session_state:
    st.session_state.session = str(uuid.uuid4())
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 New Chat", use_container_width=True):
            st.session_state.session = str(uuid.uuid4())
            st.session_state.messages = []
            st.rerun()
    
    with col2:
        if st.button("🗑️ Clear", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
    
    st.divider()
    
    st.markdown("### 📊 Session Info")
    st.markdown(f"**Session ID:**")
    st.code(st.session_state.session[:8] + "...", language="text")
    st.markdown(f"**Messages:** {len(st.session_state.messages)}")
    st.markdown(f"**Time:** {datetime.now().strftime('%H:%M:%S')}")
    
    st.divider()
    
    st.markdown("### 💡 Tips")
    st.markdown("""
    - Ask questions about your documents
    - Use natural language
    - Be specific for better results
    """)

# Main content
col1, col2, col3 = st.columns([1, 8, 1])
with col2:
    st.markdown("""
    <div class="header-container">
        <h1 class="header-title">🤖 Jarvis AI Assistant</h1>
        <p class="header-subtitle">Your intelligent document assistant powered by AI</p>
    </div>
    """, unsafe_allow_html=True)

# Chat messages container
st.markdown("### 💬 Conversation")
chat_container = st.container()

with chat_container:
    if st.session_state.messages:
        for m in st.session_state.messages:
            if m["role"] == "user":
                with st.chat_message("user", avatar="👤"):
                    st.markdown(f"**You:** {m['content']}")
            else:
                with st.chat_message("assistant", avatar="🤖"):
                    st.markdown(f"**Jarvis:** {m['content']}")
    else:
        st.markdown("""
        <div class="info-box">
            <p style="margin: 0; color: #667eea; font-weight: 500;">
                👋 Welcome! Start a conversation by typing a question below.
            </p>
        </div>
        """, unsafe_allow_html=True)

# Chat input
prompt = st.chat_input("Type your question here...", key="chat_input")

if prompt:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Show loading state
    with chat_container:
        with st.chat_message("user", avatar="👤"):
            st.markdown(f"**You:** {prompt}")
        
        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("🤔 Thinking..."):
                try:
                    res = requests.post(API, json={
                        "message": prompt,
                        "session_id": st.session_state.session
                    }).json()
                    
                    response_text = res.get("message", "Sorry, I couldn't process that request.")
                    st.markdown(f"**Jarvis:** {response_text}")
                    st.session_state.messages.append(
                        {"role": "assistant", "content": response_text}
                    )
                except Exception as e:
                    st.error(f"❌ Error: Could not connect to the API. Make sure it's running.")
                    st.session_state.messages.pop()  # Remove the user message if request fails
    
    st.rerun()
