import streamlit as st
import time
from services.api_client import predict_lung

def render_lung_uploader():
    st.title("🫁 Lung Cancer Clinical Diagnostics")
    st.markdown("Upload a chest X-Ray scan to receive a rapid, highly secure clinical evaluation of potential lung malignancies using advanced visual overlays.")
    
    uploaded_file = st.file_uploader("Upload Medical Scan (.jpg/png)", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        if st.button("Analyze Scan Data", type="primary", use_container_width=True):
            with st.spinner("Processing medical diagnosis securely..."):
                bytes_data = uploaded_file.getvalue()
                res = predict_lung(bytes_data, uploaded_file.name, uploaded_file.type)
                
                if "error" in res:
                    st.error(res["error"])
                else:
                    
                    # ============================
                    # DIAGNOSTIC REPORT CARD
                    # ============================
                    st.markdown("<hr>", unsafe_allow_html=True)
                    st.markdown("### 🔬 Automated Diagnostic Report", unsafe_allow_html=True)
                    
                    prediction = res.get("prediction", "Unknown")
                    conf = res.get("confidence", 0.0) * 100
                    
                    if prediction == "Malignant":
                        color = "var(--danger)"; bg_card = "var(--danger-bg)"; border_card = "var(--danger-bdr)"
                    elif prediction == "Normal":
                        color = "var(--success)"; bg_card = "var(--success-bg)"; border_card = "var(--success-bdr)"
                    else:
                        color = "var(--warn)"; bg_card = "var(--warn-bg)"; border_card = "var(--warn-bdr)"
                    
                    st.markdown(f"""
                    <div style="background-color: {bg_card}; padding: 22px; border-radius: var(--radius-md); border: 1.5px solid {border_card}; border-left: 5px solid {color}; margin-bottom: 25px; box-shadow: var(--shadow-card);">
                        <h2 style="margin: 0; color: var(--text-heading);">Detected Diagnosis: <span style="color: {color}">{prediction}</span></h2>
                        <h4 style="margin: 0; color: var(--text-muted); margin-top: 6px;">Analysis Confidence: {conf:.2f}%</h4>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # ============================
                    # GRAD-CAM: EXPLAINABLE AI
                    # ============================
                    st.markdown("---")

                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("**📷 Original Scan**")
                        st.image(f"data:image/jpeg;base64,{res['original']}", use_container_width=True, caption="Uploaded X-Ray (unmodified)")
                    
                    with col2:
                        st.markdown("**🌡️ Grad-CAM Overlay**")
                        st.image(f"data:image/jpeg;base64,{res['heatmap']}", use_container_width=True, caption="Heatmap superimposed on scan")
                    
                    # Color legend
                    st.markdown("""
                    <div style="background: var(--bg-input); border: 1px solid var(--border); border-radius: var(--radius-sm); padding: 15px; margin-top: 10px;">
                        <p style="color: var(--text-body); margin: 0; font-size: 0.9em;">
                            <b>📊 Heatmap Color Legend:</b><br>
                            🔴 <span style="color: var(--danger)">Red / Warm</span> — High AI attention: regions the model considers most suspicious or diagnostically significant<br>
                            🟡 <span style="color: var(--warn)">Yellow</span> — Moderate attention zones<br>
                            🔵 <span style="color: var(--primary)">Blue / Cool</span> — Low attention: regions not influencing the diagnostic decision
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    from services.pdf_generator import get_clinical_suggestion
                    suggestion = get_clinical_suggestion("lung", res)
                    
                    if prediction == "Malignant":
                        st.error(f"⚠️ **Clinical Advisory:** {suggestion}")
                    elif prediction == "Benign":
                        st.warning(f"📋 **Clinical Note:** {suggestion}")
                    else:
                        st.success(f"✅ **Clinical Note:** {suggestion}")
                    
