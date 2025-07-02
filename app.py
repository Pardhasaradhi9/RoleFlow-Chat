import streamlit as st
import requests
import json
from dotenv import load_dotenv
import os
from datetime import datetime
import html
import re

# Load environment variables
load_dotenv()

# FastAPI backend URL
API_BASE_URL = "http://localhost:8000"

# Page configuration
st.set_page_config(
    page_title="RoleFlow Chat",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #1f77b4;
        padding: 1rem 0;
        border-bottom: 2px solid #e6f3ff;
        margin-bottom: 2rem;
    }
    
    .user-info-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .conversation-block {
        background: linear-gradient(135deg, #1f2937 0%, #374151 100%);
        color: white;
        padding: 1rem;
        border-radius: 12px;
        margin: 0.75rem 0;
        border: 1px solid #4b5563;
        box-shadow: 0 3px 6px rgba(0, 0, 0, 0.15);
    }
    
    .user-message {
        background: linear-gradient(135deg, #1a365d 0%, #2d5a87 100%);
        color: white;
        padding: 0.75rem;
        border-radius: 8px;
        margin-bottom: 0.75rem;
        border-left: 4px solid #17a2b8;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    .department-badge {
        background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 15px;
        font-size: 0.8rem;
        margin-right: 0.5rem;
        font-weight: 600;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    }
    
    .source-item {
        background: linear-gradient(135deg, #374151 0%, #4b5563 100%);
        color: #e5e7eb;
        padding: 0.5rem;
        border-radius: 6px;
        margin: 0.25rem 0;
        font-size: 0.85rem;
        border: 1px solid #6b7280;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }
    
    .login-form {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    
    .status-indicator {
        display: inline-block;
        width: 10px;
        height: 10px;
        border-radius: 50%;
        margin-right: 8px;
    }
    
    .status-online {
        background-color: #28a745;
    }
    
    .status-offline {
        background-color: #dc3545;
    }

    .sources-section {
        background: linear-gradient(135deg, #374151 0%, #4b5563 100%);
        color: #e5e7eb;
        padding: 0.75rem;
        border-radius: 8px;
        margin-top: 0.75rem;
        border: 1px solid #6b7280;
    }
    
    .chat-input-container {
        max-width: 70%;
        margin-bottom: 1rem;
    }
    
    /* New Assistant Response Styles */
    .assistant-response-card {
        background: linear-gradient(135deg, #2a4365 0%, #3b5998 100%);
        color: #f9fafb;
        padding: 1rem;
        border-radius: 10px;
        margin-top: 0.5rem;
        border-left: 4px solid #60a5fa;
        box-shadow: 0 3px 6px rgba(0, 0, 0, 0.15);
    }
    
    .assistant-response-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.5rem;
    }
    
    .assistant-response-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #60a5fa;
    }
    
    .assistant-response-timestamp {
        font-size: 0.85rem;
        color: #d1d5db;
    }
    
    .assistant-response-content {
        line-height: 1.6;
        font-size: 0.95rem;
        margin: 0;
        padding: 0;
    }
    
    .assistant-response-content p {
        margin: 0.1rem 0;
    }
    
    .assistant-response-content ul, .assistant-response-content ol {
        margin: 0.1rem 0;
        padding-left: 1.5rem;
    }
    
    .assistant-response-content li {
        margin: 0.1rem 0;
        line-height: 1.5;
    }
    
    .assistant-response-content h1, .assistant-response-content h2, .assistant-response-content h3,
    .assistant-response-content h4, .assistant-response-content h5, .assistant-response-content h6 {
        font-size: 1.15rem;
        /* color: #f59e0b;  Yellow color for main headings only */
        margin: 0.3rem 0;
        font-weight: 600;
        line-height: 1.3;
    }
    
    .assistant-response-content strong {
        font-weight: 700;
        color: #f9fafb; /* Default text color for bold */
    }
    
    .assistant-response-content em {
        font-style: italic;
        color: #93c5fd; /* Light blue for italics */
    }
    
    .assistant-response-content code {
        background-color: #1e3a8a;
        padding: 0.2rem 0.5rem;
        border-radius: 4px;
        font-family: 'Courier New', monospace;
        font-size: 0.9rem;
    }
    
    .sources-section ul, .sources-section ol {
        margin: 0.25rem 0;
        padding-left: 1rem;
    }
    
    .sources-section li {
        margin: 0.125rem 0;
        font-size: 0.85rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'jwt_token' not in st.session_state:
    st.session_state.jwt_token = None
if 'user_data' not in st.session_state:
    st.session_state.user_data = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'available_departments' not in st.session_state:
    st.session_state.available_departments = []

# Function to fetch available departments
def fetch_available_departments():
    try:
        response = requests.get(f"{API_BASE_URL}/available-departments")
        if response.status_code == 200:
            return response.json()
        else:
            return ["Business", "Compliance", "Data", "Design", "Finance", "HR", "Marketing", "Operations", "Product", "Quality Assurance", "Risk", "Sales", "Technology"]
    except:
        return ["Business", "Compliance", "Data", "Design", "Finance", "HR", "Marketing", "Operations", "Product", "Quality Assurance", "Risk", "Sales", "Technology"]

# Function to safely escape HTML content (for user input only)
def safe_html_escape(text):
    """Escape HTML characters to prevent rendering issues"""
    if isinstance(text, str):
        return html.escape(text)
    return str(text)

# Function to convert markdown-style formatting to HTML
def convert_markdown_to_html(text):
    """Convert basic markdown formatting to HTML with reduced spacing and proper list handling"""
    if not isinstance(text, str):
        return str(text)
    
    # Escape HTML first to prevent XSS
    text = html.escape(text)
    
    # Convert ### Heading to <h3>
    text = re.sub(r'###\s*(.*?)(?=\n|$)', r'<h3>\1</h3>', text)
    
    # Split text into lines and process each line
    lines = text.split('\n')
    result_lines = []
    in_ordered_list = False
    in_unordered_list = False
    
    for line in lines:
        line = line.strip()
        if not line:
            if in_ordered_list:
                result_lines.append('</ol>')
                in_ordered_list = False
            elif in_unordered_list:
                result_lines.append('</ul>')
                in_unordered_list = False
            continue
        
        # Handle numbered lists (e.g., "1. Item")
        if re.match(r'^\d+\.\s+', line):
            if not in_ordered_list:
                if in_unordered_list:
                    result_lines.append('</ul>')
                    in_unordered_list = False
                result_lines.append('<ol>')
                in_ordered_list = True
            content = re.sub(r'^\d+\.\s+', '', line)
            result_lines.append(f'<li>{content}</li>')
        # Handle unordered lists (e.g., "- Item" or "• Item")
        elif re.match(r'^[-•]\s+', line):
            if not in_unordered_list:
                if in_ordered_list:
                    result_lines.append('</ol>')
                    in_ordered_list = False
                result_lines.append('<ul>')
                in_unordered_list = True
            content = re.sub(r'^[-•]\s+', '', line)
            result_lines.append(f'<li>{content}</li>')
        else:
            if in_ordered_list:
                result_lines.append('</ol>')
                in_ordered_list = False
            elif in_unordered_list:
                result_lines.append('</ul>')
                in_unordered_list = False
            if line:
                result_lines.append(line)
    
    if in_ordered_list:
        result_lines.append('</ol>')
    if in_unordered_list:
        result_lines.append('</ul>')
    
    text = '\n'.join(result_lines)
    
    # Convert **bold** to <strong>
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
    
    # Convert *italic* to <em>
    text = re.sub(r'\*(.*?)\*', r'<em>\1</em>', text)
    
    # Convert `code` to <code>
    text = re.sub(r'`(.*?)`', r'<code>\1</code>', text)
    
    # Convert double newlines to <br><br> for paragraph breaks
    text = text.replace('\n\n', '<br><br>')
    
    return text

# Main header
st.markdown('<h1 class="main-header">🤖 RoleFlow Chat</h1>', unsafe_allow_html=True)

# Sidebar for user authentication and info
with st.sidebar:
    st.markdown("### 🔐 Authentication")
    # Check if user is logged in
    if st.session_state.jwt_token and st.session_state.user_data:
        # User info display
        st.markdown(f"""
        <div class="user-info-card">
            <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                <span class="status-indicator status-online"></span>
                <strong>Online</strong>
            </div>
            <h4>👤 {safe_html_escape(st.session_state.user_data['full_name'])}</h4>
            <p><strong>ID Number:</strong> {safe_html_escape(st.session_state.user_data.get('employee_id', 'N/A'))}</p>
            <p><strong>Department:</strong> {safe_html_escape(st.session_state.user_data.get('department', 'N/A'))}</p>
            <p><strong>Role:</strong> {safe_html_escape(st.session_state.user_data.get('role', 'N/A'))}</p>
            <p><strong>Attendance:</strong> {safe_html_escape(st.session_state.user_data.get('attendance_pct', 'N/A'))}</p>
            <p><strong>Leaves Remaining:</strong> {safe_html_escape(st.session_state.user_data.get('leave_balance', 'N/A'))}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Accessible folders
        st.markdown("### 📁 Accessible Folders")
        accessible_folders = st.session_state.user_data.get('accessible_folders', [])
        if accessible_folders:
            for folder in accessible_folders:
                st.markdown(f"• **{safe_html_escape(folder)}**")
        else:
            st.info("No accessible folders assigned")
        
        st.markdown("---")
        
        # Logout button
        if st.button("🚪 Logout", type="secondary", use_container_width=True):
            st.session_state.jwt_token = None
            st.session_state.user_data = None
            st.session_state.chat_history = []
            st.rerun()
            
        # Chat history management
        st.markdown("### 💬 Chat Options")
        if st.button("🗑️ Clear Chat History", use_container_width=True):
            st.session_state.chat_history = []
            st.success("Chat history cleared!")
            
    else:
        # Fetch available departments if not already loaded
        if not st.session_state.available_departments:
            st.session_state.available_departments = fetch_available_departments()
        
        # Login form
        st.markdown('<div class="login-form">', unsafe_allow_html=True)
        
        with st.form("login_form"):
            st.markdown("**Please enter your credentials:**")
            full_name = st.text_input("👤 Full Name", placeholder="Enter your full name")
            department = st.selectbox(
                "🏢 Department", 
                options=[""] + st.session_state.available_departments,
                index=0,
                placeholder="Select your department"
            )
            
            login_submitted = st.form_submit_button("🔑 Login", type="primary", use_container_width=True)
            
            if login_submitted:
                if full_name and department:
                    try:
                        with st.spinner("Authenticating..."):
                            response = requests.post(
                                f"{API_BASE_URL}/login",
                                json={"full_name": full_name, "department": department}
                            )
                            response.raise_for_status()
                            data = response.json()
                            
                            st.session_state.jwt_token = data["token"]
                            st.session_state.user_data = data["user_data"]
                            
                            st.success("✅ Login successful!")
                            st.rerun()
                            
                    except requests.RequestException as e:
                        st.error(f"❌ Login failed: {str(e)}")
                else:
                    st.warning("⚠️ Please fill in all fields")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Connection status
        st.markdown("### 🌐 Connection Status")
        try:
            # Simple health check
            response = requests.get(f"{API_BASE_URL}/health", timeout=5)
            if response.status_code == 200:
                st.markdown('<span class="status-indicator status-online"></span>**Connected**', unsafe_allow_html=True)
            else:
                st.markdown('<span class="status-indicator status-offline"></span>**Disconnected**', unsafe_allow_html=True)
        except:
            st.markdown('<span class="status-indicator status-offline"></span>**Disconnected**', unsafe_allow_html=True)

# Main chat interface
if st.session_state.jwt_token and st.session_state.user_data:
    # Create two columns for better layout
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown("### 🙏🏾 Welcome to RoleFlow Chat, your secure chatbot for accessing role-specific data and insights tailored to your department's needs")
        
        # Chat input with constrained width
        st.markdown('<div class="chat-input-container">', unsafe_allow_html=True)
        with st.form("chat_form", clear_on_submit=True):
            user_query = st.text_area(
                "How can I make your day easier ?",
                placeholder="Enter your query here...",
                height=80,
                key="chat_input"
            )
            
            col_send, col_clear = st.columns([1, 1])
            with col_send:
                send_button = st.form_submit_button("📤 Send", type="primary", use_container_width=True)
            with col_clear:
                if st.form_submit_button("🔄 New Chat", use_container_width=True):
                    st.session_state.chat_history = []
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Process query
        if send_button and user_query.strip():
            timestamp = datetime.now().strftime("%H:%M:%S")
            
            try:
                with st.spinner("🔍 Searching for answers..."):
                    response = requests.post(
                        f"{API_BASE_URL}/query",
                        headers={"Authorization": f"Bearer {st.session_state.jwt_token}"},
                        json={"query": user_query}
                    )
                    response.raise_for_status()
                    result = response.json()
                    
                    # Add conversation to history
                    st.session_state.chat_history.append({
                        "user_query": user_query,
                        "bot_response": result,
                        "timestamp": timestamp
                    })
                    
            except requests.RequestException as e:
                st.error(f"❌ Query failed: {str(e)}")

        # Display chat history
        if st.session_state.chat_history:
            st.markdown("### 📝 Conversation History")
            
            for i, conversation in enumerate(reversed(st.session_state.chat_history[-10:])):
                # User message (still escaped for security)
                st.markdown(f"""
                <div class="conversation-block">
                    <div class="user-message">
                        <strong>👤 You ({conversation['timestamp']}):</strong><br>
                        <div style="margin-top: 0.5rem; font-size: 0.95rem;">
                            {safe_html_escape(conversation['user_query'])}
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                
                # Assistant response - new design
                bot_response_text = conversation['bot_response'].get('response', 'No response available')
                
                # Convert markdown to HTML for proper formatting
                formatted_response = convert_markdown_to_html(bot_response_text)
                
                st.markdown(f"""
                    <div class="assistant-response-card">
                        <div class="assistant-response-header">
                            <span class="assistant-response-title">🤖 Assistant</span>
                            <span class="assistant-response-timestamp">{conversation['timestamp']}</span>
                        </div>
                        <div class="assistant-response-content">
                            {formatted_response}
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                
                # Sources section
                sources = conversation['bot_response'].get('sources', [])
                if sources:
                    st.markdown("""
                        <div class="sources-section">
                            <strong style="color: #a78bfa; font-size: 0.9rem;">📚 Sources:</strong>
                    """, unsafe_allow_html=True)
                    
                    for idx, source in enumerate(sources, 1):
                        st.markdown(f"""
                            <div class="source-item">
                                <span style="color: #34d399; font-size: 0.8rem;">📄 {idx}.</span> 
                                <span style="font-size: 0.85rem;">{safe_html_escape(str(source))}</span>
                            </div>
                        """, unsafe_allow_html=True)
                    
                    st.markdown("""
                        </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("""
                    </div>
                </div>
                """, unsafe_allow_html=True)

    
    with col2:
        st.markdown("### 📊 Session Info")
        st.info(f"**Active since:** {datetime.now().strftime('%H:%M')}")
        st.info(f"**Messages sent:** {len(st.session_state.chat_history)}")
        
        # Quick actions
        st.markdown("### ⚡ Quick Actions")
        if st.button("📋 Export Chat", use_container_width=True):
            chat_export = json.dumps(st.session_state.chat_history, indent=2)
            st.download_button(
                label="💾 Download Chat History",
                data=chat_export,
                file_name=f"chat_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True
            )

else:
    # Welcome screen for non-authenticated users
    st.markdown("""
    <div style="text-align: center; padding: 1rem 1rem;">
        <h2 style="color: #f9fafb; margin-bottom: 1rem;">🔒 Authentication Required</h2>
        <p style="font-size: 1.1rem; color: #9ca3af; margin-bottom: 1rem; line-height: 1.6;">
            Please log in using the sidebar to access the RoleFlow Chatbot.
        </p>
        <div style="background: linear-gradient(135deg, #1f2937 0%, #374151 100%); padding: 1rem; border-radius: 15px; margin: 1rem 0; border: 1px solid #4b5563; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
            <h3 style="color: #60a5fa; margin-bottom: 1rem; text-align: center;">🌟 Features</h3>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; text-align: left;">
                <div style="background: linear-gradient(135deg, #374151 0%, #4b5563 100%); padding: 1.5rem; border-radius: 10px; border: 1px solid #6b7280;">
                    <h4 style="color: #34d399; margin-bottom: 0.5rem;">🔒 Role-Based Access</h4>
                    <p style="color: #d1d5db; margin: 0; line-height: 1.5;">Secure access control based on your department and role</p>
                </div>
                <div style="background: linear-gradient(135deg, #374151 0%, #4b5563 100%); padding: 1.5rem; border-radius: 10px; border: 1px solid #6b7280;">
                    <h4 style="color: #60a5fa; margin-bottom: 0.5rem;">🤖 AI-Powered Responses</h4>
                    <p style="color: #d1d5db; margin: 0; line-height: 1.5;">Get intelligent answers from your organization's knowledge base</p>
                </div>
                <div style="background: linear-gradient(135deg, #374151 0%, #4b5563 100%); padding: 1.5rem; border-radius: 10px; border: 1px solid #6b7280;">
                    <h4 style="color: #fbbf24; margin-bottom: 0.125rem;">📁 Document Access</h4>
                    <p style="color: #d1d5db; margin: 0; line-height: 1.5;">Access only the documents you're authorized to view</p>
                </div>
                <div style="background: linear-gradient(135deg, #374151 0%, #4b5563 100%); padding: 1.5rem; border-radius: 10px; border: 1px solid #6b7280;">
                    <h4 style="color: #a78bfa; margin-bottom: 0.5rem;">💬 Interactive Chat</h4>
                    <p style="color: #d1d5db; margin: 0; line-height: 1.5;">Natural conversation interface with chat history</p>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666; padding: 1rem;'>"
    "🤖 RoleFlow Chat | Powered by AI"
    "</div>",
    unsafe_allow_html=True)