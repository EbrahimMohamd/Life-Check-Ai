import streamlit as st
import os
import base64
from components.auth_ui import render_auth_ui
from components.chat_ui import render_chat_interface
from components.forms import render_diabetes_form, render_heart_form
from components.uploader import render_lung_uploader
from components.settings import render_settings
from services.pdf_generator import generate_patient_pdf


import os
logo_path_icon = os.path.join(os.path.dirname(__file__), "static", "logo.png")
st.set_page_config(page_title="LifeCheck AI", page_icon=logo_path_icon if os.path.exists(logo_path_icon) else "🧬", layout="wide", initial_sidebar_state="collapsed")

def get_base64_of_bin_file(bin_file):
    if os.path.exists(bin_file):
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    return ""

bot_icon_path = os.path.join(os.path.dirname(__file__), "assets", "bot_icon.png")
bot_bg = f"data:image/png;base64,{get_base64_of_bin_file(bot_icon_path)}"

logo_path = os.path.join(os.path.dirname(__file__), "static", "logo.png")
logo_bg = f"data:image/png;base64,{get_base64_of_bin_file(logo_path)}"



if "theme" not in st.session_state:
    st.session_state.theme = "dark"

is_light = st.session_state.theme == "light"

v_bg_page = "#F8FAFC" if is_light else "#0B1120"
v_bg_card = "rgba(255, 255, 255, 0.85)" if is_light else "rgba(30, 41, 59, 0.88)"
v_bg_subtle = "#F1F5F9" if is_light else "#0F172A"
v_bg_input = "#FFFFFF" if is_light else "#0F172A"
v_border = "#E2E8F0" if is_light else "#334155"
v_text_heading = "#000000" if is_light else "#F8FAFC"
v_text_body = "#000000" if is_light else "#E2E8F0"
v_text_muted = "#333333" if is_light else "#94A3B8"
v_watermark_opacity = "0.08" if is_light else "0.15"
v_blend_mode = "multiply" if is_light else "screen"
v_filter = "invert(1)" if is_light else "none"

st.markdown(f"""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

  /* ═══════════════════════════════════════
     1. CSS VARIABLES (Single Source of Truth)
     ═══════════════════════════════════════ */
  :root {{
    --bg-page:      {v_bg_page};
    --bg-card:      {v_bg_card}; /* Premium Glassmorphism */
    --bg-subtle:    {v_bg_subtle};
    --bg-input:     {v_bg_input};

    --border:       {v_border};
    --border-focus: #3B82F6;

    --primary:      #3B82F6;
    --primary-dark: #2563EB;
    --primary-glow: rgba(59, 130, 246, 0.25);

    --text-heading: {v_text_heading};
    --text-body:    {v_text_body};
    --text-muted:   {v_text_muted};
    --text-on-primary: #FFFFFF;

    --success:      #10B981;
    --success-bg:   rgba(16, 185, 129, 0.1);
    --success-bdr:  rgba(16, 185, 129, 0.3);

    --warn:         #F59E0B;
    --warn-bg:      rgba(245, 158, 11, 0.1);
    --warn-bdr:     rgba(245, 158, 11, 0.3);

    --danger:       #EF4444;
    --danger-bg:    rgba(239, 68, 68, 0.1);
    --danger-bdr:   rgba(239, 68, 68, 0.3);

    --radius-sm:    8px;
    --radius-md:    14px;
    --radius-lg:    20px;
    --shadow-card:  0 4px 20px rgba(0, 0, 0, 0.4);
    --shadow-btn:   0 4px 12px rgba(59, 130, 246, 0.3);
  }}

  /* ═══════════════════════════════════════
     2. GLOBAL BASE
     ═══════════════════════════════════════ */
  html, body, [class*="css"], .stApp {{
    font-family: 'Inter', sans-serif !important;
    background-color: var(--bg-page) !important;
    color: var(--text-body) !important;
  }}
  
  /* The elegant Watermark using pseudo-element and blend modes */
  .stApp::before {{
    content: "";
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background-image: url("{logo_bg}");
    background-size: 50vw;
    background-position: center;
    background-repeat: no-repeat;
    opacity: {v_watermark_opacity};
    mix-blend-mode: {v_blend_mode};
    filter: {v_filter};
    pointer-events: none;
    z-index: 0;
  }}
  
  /* Force text colors across Streamlit elements securely */
  .stMarkdown p, .stText p, label, li, span {{
      color: var(--text-body);
  }}
  h1, h2, h3, h4, h5, h6 {{
      color: var(--text-heading) !important;
  }}
  .stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"] {{
      background-color: var(--bg-input) !important;
      color: var(--text-heading) !important;
      border-color: var(--border) !important;
  }}
  

  
  [data-testid="collapsedControl"] {{ display: none !important; }}
  [data-testid="stSidebar"]        {{ display: none !important; }}
  header                           {{ display: none !important; height: 0px !important; margin: 0 !important; padding: 0 !important; }}
  
  /* Destroy all native Streamlit top padding and invisible style elements */
  .block-container {{
      padding-top: 1.5rem !important;
      margin-top: 0 !important;
  }}
  div.element-container:has(style), div.element-container:has(iframe) {{
      display: none !important;
      margin: 0 !important;
      padding: 0 !important;
  }}

  /* Main white card container */
  .main .block-container {{
    background-color: var(--bg-card) !important;
    backdrop-filter: blur(12px) !important;
    -webkit-backdrop-filter: blur(12px) !important;
    border-radius: var(--radius-lg) !important;
    box-shadow: var(--shadow-card) !important;
    border: 1px solid rgba(51, 65, 85, 0.5) !important;
    padding: 0.5rem 3rem 2.5rem 3rem !important; 
    max-width: 1200px !important;
  }}

  /* ═══════════════════════════════════════
     3. TYPOGRAPHY
     ═══════════════════════════════════════ */
  h1 {{
    font-family: 'Inter', sans-serif !important;
    font-size: 2rem !important;
    font-weight: 800 !important;
    color: var(--text-heading) !important;
    letter-spacing: -0.5px !important;
    line-height: 1.2 !important;
  }}
  h2 {{
    font-family: 'Inter', sans-serif !important;
    font-weight: 700 !important;
    color: var(--text-heading) !important;
  }}
  h3 {{
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    color: var(--text-heading) !important;
    font-size: 1.1rem !important;
  }}
  h4 {{
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    color: var(--text-body) !important;
  }}
  p, .stMarkdown p {{
    color: var(--text-body) !important;
    line-height: 1.65 !important;
  }}
  label, .stSelectbox label, .stTextInput label,
  .stNumberInput label, .stRadio label {{
    color: var(--text-body) !important;
    font-weight: 500 !important;
    font-size: 0.9rem !important;
  }}

  /* ═══════════════════════════════════════
     4. FEATURE CARDS (Dashboard)
     ═══════════════════════════════════════ */
  .feature-card {{
    background: var(--bg-card);
    padding: 2.2rem 1.8rem;
    border-radius: var(--radius-md);
    box-shadow: var(--shadow-card);
    border: 1.5px solid var(--border);
    text-align: center;
    height: 100%;
    margin-bottom: 16px;
    transition: transform 0.22s ease, box-shadow 0.22s ease, border-color 0.22s ease;
    cursor: pointer;
  }}
  .feature-card:hover {{
    transform: translateY(-5px);
    box-shadow: 0 12px 32px var(--primary-glow);
    border-color: var(--primary);
  }}
  .feature-card h2 {{
    color: var(--primary) !important;
    font-size: 1.7rem !important;
    margin-bottom: 10px !important;
  }}
  .feature-card p {{
    color: var(--text-muted) !important;
    font-size: 1rem !important;
    line-height: 1.6 !important;
  }}

  /* ═══════════════════════════════════════
     5. BUTTONS
     ═══════════════════════════════════════ */
  .stButton > button {{
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    border-radius: var(--radius-sm) !important;
    padding: 0.55rem 1.3rem !important;
    transition: all 0.2s ease !important;
    letter-spacing: 0.01em !important;
  }}
  /* Primary */
  .stButton > button[kind="primary"] {{
    background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%) !important;
    border: none !important;
    color: var(--text-on-primary) !important;
    box-shadow: var(--shadow-btn) !important;
  }}
  .stButton > button[kind="primary"]:hover {{
    opacity: 0.92 !important;
    box-shadow: 0 6px 20px var(--primary-glow) !important;
    transform: translateY(-1px) !important;
  }}
  /* Secondary */
  .stButton > button[kind="secondary"] {{
    background: var(--bg-card) !important;
    border: 1.5px solid var(--border) !important;
    color: var(--primary) !important;
  }}
  .stButton > button[kind="secondary"]:hover {{
    background: var(--bg-subtle) !important;
    border-color: var(--primary) !important;
  }}
  /* Form submit buttons */
  .stFormSubmitButton > button {{
    background: linear-gradient(135deg, var(--primary), var(--primary-dark)) !important;
    border: none !important;
    color: white !important;
    font-weight: 600 !important;
    border-radius: var(--radius-sm) !important;
    box-shadow: var(--shadow-btn) !important;
  }}

  /* ═══════════════════════════════════════
     6. FORM INPUTS
     ═══════════════════════════════════════ */
  .stTextInput > div > div > input,
  .stNumberInput > div > div > input,
  .stPasswordInput > div > div > input {{
    background: var(--bg-input) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--text-heading) !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.95rem !important;
    padding: 0.5rem 0.85rem !important;
  }}
  .stTextInput > div > div > input:focus,
  .stNumberInput > div > div > input:focus {{
    border-color: var(--border-focus) !important;
    box-shadow: 0 0 0 3px var(--primary-glow) !important;
    outline: none !important;
  }}
  /* Selectbox */
  .stSelectbox > div > div {{
    background: var(--bg-input) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--text-heading) !important;
  }}
  .stSelectbox > div > div > div[data-baseweb="select"] > div {{
    color: var(--text-heading) !important;
    background: var(--bg-input) !important;
  }}

  /* ═══════════════════════════════════════
     7. TABS
     ═══════════════════════════════════════ */
  .stTabs [data-baseweb="tab-list"] {{
    background: var(--bg-subtle) !important;
    border-radius: var(--radius-sm) !important;
    padding: 5px !important;
    gap: 3px !important;
    border: 1px solid var(--border) !important;
  }}
  .stTabs [data-baseweb="tab"] {{
    border-radius: 6px !important;
    color: var(--text-muted) !important;
    font-weight: 500 !important;
    font-size: 0.9rem !important;
    padding: 8px 22px !important;
    background: transparent !important;
    border: none !important;
  }}
  .stTabs [aria-selected="true"] {{
    background: var(--primary) !important;
    color: white !important;
    box-shadow: 0 2px 8px var(--primary-glow) !important;
  }}

  /* ═══════════════════════════════════════
     8. ALERTS / INFO BOXES
     ═══════════════════════════════════════ */
  .stAlert {{
    border-radius: var(--radius-sm) !important;
    border: 1px solid transparent !important;
    font-size: 0.92rem !important;
  }}

  /* ═══════════════════════════════════════
     9. DIVIDER & SPINNER
     ═══════════════════════════════════════ */
  hr {{ border-color: var(--border) !important; margin: 1.5rem 0 !important; }}
  .stSpinner > div {{ border-top-color: var(--primary) !important; }}

  /* ═══════════════════════════════════════
     10. EXPANDER
     ═══════════════════════════════════════ */
  .streamlit-expanderHeader {{
    background: var(--bg-subtle) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--text-body) !important;
    font-weight: 600 !important;
  }}
  .streamlit-expanderContent {{
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-top: none !important;
  }}

  /* ═══════════════════════════════════════
     11. FLOATING CHAT AVATAR
     ═══════════════════════════════════════ */
  div.element-container:has(#floating-robot-marker) + div.element-container {{
    position: fixed !important;
    bottom: 30px !important;
    right: 30px !important;
    z-index: 999999 !important;
    width: 76px !important;
    height: 76px !important;
  }}
  div.element-container:has(#floating-robot-marker) + div.element-container button {{
    position: absolute !important;
    inset: 0 !important;
    width: 76px !important;
    height: 76px !important;
    border-radius: 50% !important;
    background-color: var(--bg-card) !important;
    background-image: url("{bot_bg}") !important;
    background-size: cover !important;
    background-position: center !important;
    border: 3px solid var(--primary) !important;
    box-shadow: 0 4px 20px var(--primary-glow) !important;
    color: transparent !important;
    padding: 0 !important;
    animation: float-pulse 2.2s ease-in-out infinite !important;
    cursor: pointer !important;
    transition: all 0.3s ease !important;
  }}
  div.element-container:has(#floating-robot-marker) + div.element-container button:hover {{
    transform: scale(1.1) translateY(-4px) !important;
    box-shadow: 0 8px 28px rgba(59,110,248,0.5) !important;
    animation: none !important;
  }}
  div.element-container:has(#floating-robot-marker) + div.element-container button p {{
    display: none !important;
  }}
  @keyframes float-pulse {{
    0%, 100% {{ box-shadow: 0 4px 20px var(--primary-glow); transform: translateY(0); }}
    50%       {{ box-shadow: 0 8px 28px rgba(59,110,248,0.35); transform: translateY(-4px); }}
  }}

  /* ═══════════════════════════════════════
     12. SCROLLBAR
     ═══════════════════════════════════════ */
  ::-webkit-scrollbar {{ width: 6px; height: 6px; }}
  ::-webkit-scrollbar-track {{ background: var(--bg-page); }}
  ::-webkit-scrollbar-thumb {{ background: var(--border); border-radius: 99px; }}
  ::-webkit-scrollbar-thumb:hover {{ background: var(--primary); }}
</style>
""", unsafe_allow_html=True)



def set_page(page_name):
    st.query_params["page"] = page_name
    st.rerun()

@st.dialog("📄 Prepare Medical Report")
def report_modal():
    st.info("Compiling your medical history securely from the server...", icon="🔒")
    with st.spinner("Generating PDF..."):
        pdf_bytes = generate_patient_pdf()
    
    st.success("Your medical report is fully compiled!")
    st.download_button(
        label="📥 Download PDF Now",
        data=pdf_bytes,
        file_name="LifeCheck_Report.pdf",
        mime="application/pdf",
        type="primary",
        use_container_width=True
    )

def render_header():
    st.markdown("""
    <style>
    .header-title {
        color: var(--text-heading);
        margin: 0;
        font-size: 19px;
        font-weight: 700;
        font-family: 'Inter', sans-serif;
        letter-spacing: -0.2px;
    }
    .header-tag {
        color: var(--primary);
        font-size: 11px;
        font-weight: 600;
        margin: 0;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        font-family: 'Inter', sans-serif;
    }
    </style>
    """, unsafe_allow_html=True)
    
    col_logo, col_info, col_spacer, col_btn_home, col_btn_export, col_btn_settings, col_btn_logout, col_btn_theme = st.columns([0.05, 0.25, 0.38, 0.05, 0.12, 0.05, 0.05, 0.05], vertical_alignment="center")
    
    with col_logo:
        import os
        logo_path = os.path.join(os.path.dirname(__file__), "static", "logo.png")
        if os.path.exists(logo_path):
            l_bg = f"data:image/png;base64,{get_base64_of_bin_file(logo_path)}"
            st.markdown(f"<img src='{l_bg}' width='42' style='display: block; margin: 0 auto;'>", unsafe_allow_html=True)
        else:
            st.markdown("<h1 style='margin:0; font-size:2rem;'>🧬</h1>", unsafe_allow_html=True)
            
    with col_info:
        st.markdown(f"<p class='header-tag'>Verified Patient</p><p class='header-title'>{st.session_state.get('full_name', 'Patient')}</p>", unsafe_allow_html=True)
        
    with col_btn_home:
        if st.button("🏠", use_container_width=True, help="Dashboard", type="tertiary"):
            set_page("Dashboard")
            
    with col_btn_export:
        if st.button("📄 Export", use_container_width=True, type="tertiary"):
            report_modal()
            
    with col_btn_settings:
        if st.button("⚙️", use_container_width=True, help="Settings", type="tertiary"):
            set_page("Settings")
            
    with col_btn_logout:
        if st.button("🚪", use_container_width=True, help="Logout", type="tertiary"):
            st.session_state.clear()
            st.rerun()
            
    with col_btn_theme:
        theme_icon = "🌙" if is_light else "☀️"
        if st.button(theme_icon, help="Toggle Theme", use_container_width=True, type="tertiary"):
            st.session_state.theme = "dark" if is_light else "light"
            st.rerun()
            
    st.markdown("<hr style='margin-top: -20px; margin-bottom: 15px; border-color: var(--border);'>", unsafe_allow_html=True)

def render_dashboard():
    import os
    logo_path = os.path.join(os.path.dirname(__file__), "static", "logo.png")
    
    if os.path.exists(logo_path):
        l_bg = f"data:image/png;base64,{get_base64_of_bin_file(logo_path)}"
        st.markdown(f"<h1 style='text-align:center;'><img src='{l_bg}' width='50' style='vertical-align: middle; margin-right: 15px;'>Welcome to LifeCheck AI</h1>", unsafe_allow_html=True)
    else:
        st.markdown("<h1 style='text-align:center;'>Welcome to LifeCheck AI</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; font-size:1.05rem; color: var(--text-muted); margin-bottom:2.5rem;'>Your advanced medical AI platform for predictive health analysis.</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h2>🩸 Diabetes</h2>
            <p>Evaluate your risk using vital indicators.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Start Diabetes Check", use_container_width=True, type="primary"):
            set_page("Diabetes")

    with col2:
        st.markdown("""
        <div class="feature-card">
            <h2>🫀 Heart</h2>
            <p>Predict your cardiovascular health status.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Start Heart Check", use_container_width=True, type="primary"):
            set_page("Heart")

    with col3:
        st.markdown("""
        <div class="feature-card">
            <h2>🫁 Lung Cancer</h2>
            <p>Upload a chest X-Ray for instantaneous screening.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Start Lung Scan", use_container_width=True, type="primary"):
            set_page("Lung Cancer")




@st.dialog("💬 Medical AI Assistant")
def chat_modal():
    render_chat_interface()

def main():
    import streamlit.components.v1 as components

    
    _ra = st.query_params.get("_ra", "")
    _rn = st.query_params.get("_rn", "")
    if _ra and "auth_token" not in st.session_state:
        st.session_state.auth_token = _ra
        st.session_state.full_name  = _rn
        del st.query_params["_ra"]
        del st.query_params["_rn"]
        st.rerun()

    
    if "auth_token" not in st.session_state:
        st.markdown("<style>#floating-robot-marker { display: none !important; }</style>", unsafe_allow_html=True)
        render_auth_ui()
        return

    
    render_header()

    current_page = st.query_params.get("page", "Dashboard")

   
    _prev = st.session_state.get("_nav_prev", None)
    _token = st.session_state.get("auth_token", "")
    _name  = st.session_state.get("full_name", "").replace("'", "\\'")

    if _prev is not None and _prev != current_page:
        components.html(f"""<script>
(function() {{
    // Push the PREVIOUS page so back button can return to it
    window.parent.history.pushState({{page:'{_prev}'}}, '', '?page={_prev}');
    // Replace with the CURRENT page (where we actually are)
    window.parent.history.replaceState({{page:'{current_page}'}}, '', '?page={current_page}');

    // One-time popstate listener for back/forward
    if (!window.parent.__lcPop) {{
        window.parent.__lcPop = true;
        window.parent.addEventListener('popstate', function() {{
            var auth = window.parent.sessionStorage.getItem('lc_auth')||'';
            var name = window.parent.sessionStorage.getItem('lc_name')||'';
            var url  = new URL(window.parent.location.href);
            if (auth) {{ url.searchParams.set('_ra', auth); url.searchParams.set('_rn', name); }}
            window.parent.location.assign(url.toString());
        }});
    }}
}})();
</script>""", height=0)

  
    components.html(f"""<script>
(function() {{
    if ('{_token}') {{
        window.parent.sessionStorage.setItem('lc_auth', '{_token}');
        window.parent.sessionStorage.setItem('lc_name', '{_name}');
    }}
    if (!window.parent.__lcPop) {{
        window.parent.__lcPop = true;
        window.parent.addEventListener('popstate', function() {{
            var auth = window.parent.sessionStorage.getItem('lc_auth')||'';
            var name = window.parent.sessionStorage.getItem('lc_name')||'';
            var url  = new URL(window.parent.location.href);
            if (auth) {{ url.searchParams.set('_ra', auth); url.searchParams.set('_rn', name); }}
            window.parent.location.assign(url.toString());
        }});
    }}
}})();
</script>""", height=0)

    st.session_state["_nav_prev"] = current_page
    
    if current_page == "Dashboard":
        render_dashboard()
    elif current_page == "Diabetes":
        render_diabetes_form()
    elif current_page == "Heart":
        render_heart_form()
    elif current_page == "Lung Cancer":
        render_lung_uploader()
    elif current_page == "Settings":
        render_settings()

    
    
    st.markdown("<span id='floating-robot-marker'></span>", unsafe_allow_html=True)
     
    if st.button("chat_hidden", key="floating_bot_hook", type="secondary"):
        chat_modal()

if __name__ == "__main__":
    main()
