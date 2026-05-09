import streamlit as st
from services.api_client import login, register

def render_auth_ui():
    import os
    import base64
    def _get_b64(path):
        if os.path.exists(path):
            with open(path, 'rb') as f: return base64.b64encode(f.read()).decode()
        return ""
    
    logo_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static", "logo.jpg")
    l_bg = _get_b64(logo_path)
    
    if l_bg:
        st.markdown(f"<h1 style='text-align: center; color: #1e40af; margin-top: 50px;'><img src='data:image/png;base64,{l_bg}' width='50' style='vertical-align: middle; margin-right: 15px;'>LifeCheck AI</h1>", unsafe_allow_html=True)
    else:
        st.markdown("<h1 style='text-align: center; color: #1e40af; margin-top: 50px;'>🧬 LifeCheck AI</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: #64748b; margin-bottom: 2rem;'>Secure Patient Portal</h4>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        tab1, tab2 = st.tabs(["🔒 Patient Login", "📝 New Registration"])

        with tab1:
            with st.form("login_form", border=False):
                username = st.text_input("Username")
                password = st.text_input("Password", type="password")
                submit = st.form_submit_button("Sign In", type="primary", use_container_width=True)
                
                if submit:
                    if not username or not password:
                        st.error("Please enter both username and password")
                    else:
                        res = login(username.strip().lower(), password)
                        if "error" in res:
                            st.error(f"Login failed: {res['error']}")
                        else:
                            st.session_state.auth_token = res["access_token"]
                            st.session_state.user_id = res["user_id"]
                            st.session_state.full_name = res["full_name"]
                            st.session_state.page = "Dashboard"
                            st.rerun()

        with tab2:
            with st.form("register_form", border=False):
                new_username = st.text_input("Username*")
                new_email = st.text_input("Email*", help="Used for your medical records.")
                
                colP1, colP2 = st.columns(2)
                new_password = colP1.text_input("Password*", type="password")
                confirm_password = colP2.text_input("Confirm Password*", type="password")
                
                full_name = st.text_input("Full Name (For official PDF Report)*")
                
                colA, colB = st.columns(2)
                age = colA.number_input("Age", min_value=1, max_value=120, value=30)
                gender = colB.selectbox("Gender", ["Male", "Female", "Other"])
                
                submit_reg = st.form_submit_button("Create Patient Profile", type="primary", use_container_width=True)

                if submit_reg:
                    if not new_username or not new_password or not confirm_password or not new_email or not full_name:
                        st.error("Please fill all required fields (*)")
                    elif new_password != confirm_password:
                        st.error("Registration failed: Passwords do not match!")
                    else:
                        data = {
                            "username": new_username.strip().lower(),
                            "password": new_password,
                            "email": new_email.strip().lower(),
                            "full_name": full_name,
                            "age": age,
                            "gender": gender
                        }
                        res = register(data)
                        if "error" in res:
                            # Render the exact error so the user isn't stuck guessing!
                            # E.g. "value is not a valid email address" or "Username already registered"
                            st.error(f"Registration failed: {res['error']}")
                        else:
                            st.success("Account created successfully! Logging you in...")
                            st.session_state.auth_token = res["access_token"]
                            st.session_state.user_id = res["user_id"]
                            st.session_state.full_name = res["full_name"]
                            st.session_state.page = "Dashboard"
                            st.rerun()
