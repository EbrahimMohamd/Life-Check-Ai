import streamlit as st
from services.api_client import send_chat_message

def render_chat_interface():
    # Inject Custom Chat CSS for a beautiful, scrollable, native layout
    st.markdown("""
    <style>
    /* Modify dialog container so it's a fixed elegant size */
    div[role="dialog"] .stDialog {
        border-radius: 16px !important;
        border: 1px solid var(--border) !important;
        padding: 0 !important;
        background-color: var(--bg-card) !important;
        backdrop-filter: blur(12px) !important;
        -webkit-backdrop-filter: blur(12px) !important;
    }
    
    /* Make chat input stick cleanly */
    div[data-testid="stChatInput"] {
        padding-bottom: 10px;
    }
    
    /* Chat bubbles styling for a modern app look */
    div[data-testid="stChatMessage"] {
        background-color: var(--bg-subtle);
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 12px;
        border: 1px solid var(--border);
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        color: var(--text-body);
    }
    
    /* Color distinct avatars */
    div[data-testid="stChatMessageAvatarUser"] {
        background-color: #3b82f6 !important;
    }
    div[data-testid="stChatMessageAvatarAssistant"] {
        background-color: #10b981 !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "user_id" not in st.session_state:
        import random
        st.session_state.user_id = random.randint(1000, 9999)

    # Use a fixed-height container for messages so it scrolls internally perfectly.
    # This fully resolves the "dropping down" un-professional page expansion bug!
    chat_box = st.container(height=450, border=False)

    with chat_box:
        # Display chat messages from history on app rerun
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("Write your symptoms or discuss with the doctor..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message in chat message container
        with chat_box:
            with st.chat_message("user"):
                st.markdown(prompt)

            # Display assistant response in chat message container
            with st.chat_message("assistant"):
                with st.spinner("Analyzing..."):
                    response = send_chat_message(st.session_state.user_id, prompt)
                    st.markdown(response)
            
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
