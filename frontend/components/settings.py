import streamlit as st
from services.api_client import change_password, clear_history, delete_account

def render_settings():
    st.markdown("<h1 style='text-align:center;'>⚙️ Account Settings</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color: var(--text-muted); margin-bottom: 2rem;'>Manage your security and data preferences.</p>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 6, 1])
    with col2:
        # --- Security Settings ---
        st.markdown("### 🔒 Security")
        with st.form("password_change_form"):
            old_pw = st.text_input("Current Password", type="password")
            new_pw = st.text_input("New Password", type="password")
            confirm_pw = st.text_input("Confirm New Password", type="password")
            submitted = st.form_submit_button("Update Password", type="primary", use_container_width=True)
            
            if submitted:
                if not old_pw or not new_pw or not confirm_pw:
                    st.error("Please fill in all fields.")
                elif new_pw != confirm_pw:
                    st.error("New passwords do not match.")
                elif len(new_pw) < 6:
                    st.error("Password must be at least 6 characters.")
                else:
                    with st.spinner("Updating password..."):
                        res = change_password(old_pw, new_pw)
                        if "error" in res:
                            st.error(f"Failed: {res['error']}")
                        else:
                            st.success("Password updated successfully! You will be securely logged out.")
                            import time
                            time.sleep(2)
                            st.session_state.clear()
                            st.rerun()

        st.markdown("<hr style='border-color: var(--border); margin: 30px 0;'>", unsafe_allow_html=True)

        # --- Danger Zone ---
        st.markdown("### ⚠️ Danger Zone")
        st.markdown("<p style='color: var(--danger); font-size: 0.9em; margin-bottom: 20px;'>These actions are destructive and cannot be undone. Please proceed with caution.</p>", unsafe_allow_html=True)

        # Clear History Button
        if st.button("🗑️ Clear Medical History", use_container_width=True):
            confirm_clear_history()

        st.markdown("<div style='margin-bottom: 10px;'></div>", unsafe_allow_html=True)

        # Delete Account Button
        if st.button("🚨 Delete My Account Permanently", use_container_width=True, type="secondary"):
            confirm_delete_account()

@st.dialog("Are you absolutely sure?")
def confirm_clear_history():
    st.warning("This will permanently wipe all your medical AI scan records and cardiovascular analyses. This action cannot be undone.")
    if st.button("Yes, clear my history now", type="primary", use_container_width=True):
        with st.spinner("Wiping records..."):
            res = clear_history()
            if "error" in res:
                st.error(f"Error: {res['error']}")
            else:
                st.success("History cleared successfully.")
                import time
                time.sleep(1.5)
                st.rerun()
    if st.button("Cancel"):
        st.rerun()

@st.dialog("Delete Account Permanently?")
def confirm_delete_account():
    st.error("⚠️ WARNING: Deleting your account will destroy all your profile data and historical records. You will lose access immediately.")
    st.text_input("Type 'DELETE' to confirm", key="delete_confirm_text")
    
    if st.button("Permanently Delete Account", type="primary", use_container_width=True):
        if st.session_state.get("delete_confirm_text") == "DELETE":
            with st.spinner("Deleting account..."):
                res = delete_account()
                if "error" in res:
                    st.error(f"Error: {res['error']}")
                else:
                    st.success("Account deleted. Logging out...")
                    import time
                    time.sleep(2)
                    st.session_state.clear()
                    st.rerun()
        else:
            st.error("Please type 'DELETE' in all caps to confirm.")
    if st.button("Cancel"):
        st.rerun()
