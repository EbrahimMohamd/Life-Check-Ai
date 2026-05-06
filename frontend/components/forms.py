import streamlit as st
from frontend.services.api_client import predict_diabetes, predict_heart
from frontend.services.pdf_generator import get_clinical_suggestion

def display_result_card(result, model_type=""):
    if "error" in result:
        st.error(f"Error: {result['error']}")
        return

    level = result.get("risk_level", "Unknown")
    
    if level == "Low":
        color = "var(--success)"
        bg    = "var(--success-bg)"
        border= "var(--success-bdr)"
    elif level == "Medium":
        color = "var(--warn)"
        bg    = "var(--warn-bg)"
        border= "var(--warn-bdr)"
    else:
        color = "var(--danger)"
        bg    = "var(--danger-bg)"
        border= "var(--danger-bdr)"
        
    suggestion = get_clinical_suggestion(model_type, result)
    
    html_content = f"""
<div style="padding: 22px; border-radius: var(--radius-md); background-color: {bg}; border: 1.5px solid {border}; border-left: 5px solid {color}; margin-top: 20px; box-shadow: var(--shadow-card);">
    <h3 style="color: {color}; margin-bottom: 8px; font-weight: 700;">Risk Level: {level}</h3>
    <p style="font-size: 1.05em; margin-bottom: 5px; color: var(--text-body);"><strong>Confidence:</strong> {result.get('confidence', 0)*100:.1f}%</p>
    <p style="font-size: 1.05em; margin-bottom: 12px; color: var(--text-body);"><strong>Advisory:</strong> {result.get('prediction', '')}</p>
    <div style="background-color: var(--bg-input); padding: 12px; border-radius: 6px; border-left: 4px solid var(--primary);">
        <strong style="color: var(--primary);">⚕️ Clinical Plan:</strong> <span style="color: var(--text-muted);">{suggestion}</span>
    </div>
</div>
"""
    st.markdown(html_content, unsafe_allow_html=True)

def render_diabetes_form():
    st.title("🩸 Diabetes Risk Assessment (BRFSS Lifestyle)")
    st.markdown("Evaluate your potential risk for diabetes based on your **behavioral and lifestyle factors** using our trained XGBoost model.")

    AGE_OPTIONS = ['18-24','25-29','30-34','35-39','40-44','45-49',
                   '50-54','55-59','60-64','65-69','70-74','75-79','80 or older']
    GENHEALTH_OPTIONS = ['Excellent', 'Very Good', 'Good', 'Fair', 'Poor']

    with st.form("diabetes_form"):
        st.subheader("🧬 Section 1: Demographics & Physical")
        c1, c2, c3 = st.columns(3)
        with c1:
            sex = st.selectbox("Gender", ["Female", "Male"])
            age_category = st.selectbox("Age Group", AGE_OPTIONS, index=6)
        with c2:
            bmi = st.number_input("Body Mass Index (BMI)", min_value=10.0, max_value=80.0, value=25.0, step=0.1)
            gen_hlth = st.selectbox("General Health", GENHEALTH_OPTIONS, index=2)
        with c3:
            phys_hlth = st.number_input("Days of Poor Physical Health (past 30 days)", min_value=0.0, max_value=30.0, value=0.0, step=1.0)
            ment_hlth = st.number_input("Days of Poor Mental Health (past 30 days)", min_value=0.0, max_value=30.0, value=0.0, step=1.0)

        st.subheader("🏃 Section 2: Lifestyle Habits")
        c4, c5, c6 = st.columns(3)
        with c4:
            smoker = st.selectbox("Have you smoked ≥100 cigarettes in your life?", ["No", "Yes"])
            hvy_alcohol = st.selectbox("Heavy Alcohol Drinker?", ["No", "Yes"])
        with c5:
            phys_activity = st.selectbox("Physical Activity in Past 30 Days?", ["No", "Yes"])
            diff_walk = st.selectbox("Difficulty Walking or Climbing Stairs?", ["No", "Yes"])
        with c6:
            high_bp = st.selectbox("Have you been told you have High Blood Pressure?", ["No", "Yes"])
            high_chol = st.selectbox("Have you been told you have High Cholesterol?", ["No", "Yes"])

        st.subheader("🏥 Section 3: Medical History")
        c7, c8 = st.columns(2)
        with c7:
            heart_disease = st.selectbox("History of Coronary Heart Disease or MI?", ["No", "Yes"])
        with c8:
            stroke = st.selectbox("Ever Had a Stroke?", ["No", "Yes"])

        submitted = st.form_submit_button("🔍 Analyze Diabetes Risk", use_container_width=True)

        if submitted:
            payload = {
                "high_bp": 1 if high_bp == "Yes" else 0,
                "high_chol": 1 if high_chol == "Yes" else 0,
                "bmi": float(bmi),
                "smoker": 1 if smoker == "Yes" else 0,
                "stroke": 1 if stroke == "Yes" else 0,
                "heart_disease": 1 if heart_disease == "Yes" else 0,
                "phys_activity": 1 if phys_activity == "Yes" else 0,
                "hvy_alcohol": 1 if hvy_alcohol == "Yes" else 0,
                "gen_hlth": gen_hlth,
                "diff_walk": 1 if diff_walk == "Yes" else 0,
                "phys_hlth": float(phys_hlth),
                "sex": sex,
                "age_category": age_category,
                "ment_hlth": float(ment_hlth),
            }
            with st.spinner("Analyzing your lifestyle profile for diabetes risk..."):
                res = predict_diabetes(payload)
                display_result_card(res, model_type="diabetes")

def render_heart_form():
    st.title("🫀 Heart Disease Risk Assessment")
    st.markdown("Evaluate your cardiovascular risk based on your **lifestyle and health habits** using our trained Random Forest model (BRFSS Survey Data).")

    AGE_OPTIONS = ['18-24','25-29','30-34','35-39','40-44','45-49',
                   '50-54','55-59','60-64','65-69','70-74','75-79','80 or older']
    GENHEALTH_OPTIONS = ['Excellent', 'Very good', 'Good', 'Fair', 'Poor']

    with st.form("heart_form"):
        st.subheader("🧬 Section 1: Demographics & Physical")
        c1, c2, c3 = st.columns(3)
        with c1:
            sex = st.selectbox("Gender", ["Female", "Male"])
            age_category = st.selectbox("Age Group", AGE_OPTIONS, index=6)
        with c2:
            bmi = st.number_input("Body Mass Index (BMI)", min_value=10.0, max_value=80.0, value=27.0, step=0.1)
            sleep_time = st.number_input("Average Sleep Time (hours/day)", min_value=1.0, max_value=24.0, value=7.0, step=0.5)
        with c3:
            gen_health = st.selectbox("General Health", GENHEALTH_OPTIONS, index=2)
            physical_health = st.number_input("Days of Poor Physical Health (past 30 days)", min_value=0.0, max_value=30.0, value=0.0, step=1.0)

        st.subheader("🏃 Section 2: Lifestyle Habits")
        c4, c5, c6 = st.columns(3)
        with c4:
            smoking = st.selectbox("Have you smoked ≥100 cigarettes in your life?", ["No", "Yes"])
            alcohol_drinking = st.selectbox("Heavy Alcohol Drinker?", ["No", "Yes"])
        with c5:
            physical_activity = st.selectbox("Physical Activity in Past 30 Days?", ["No", "Yes"])
            mental_health = st.number_input("Days of Poor Mental Health (past 30 days)", min_value=0.0, max_value=30.0, value=0.0, step=1.0)
        with c6:
            diff_walking = st.selectbox("Difficulty Walking or Climbing Stairs?", ["No", "Yes"])

        st.subheader("🏥 Section 3: Medical History")
        c7, c8, c9 = st.columns(3)
        with c7:
            diabetic = st.selectbox("Do you have Diabetes?", ["No", "Yes"])
            stroke = st.selectbox("Ever Had a Stroke?", ["No", "Yes"])
        with c8:
            asthma = st.selectbox("Do you have Asthma?", ["No", "Yes"])
            kidney_disease = st.selectbox("Do you have Kidney Disease?", ["No", "Yes"])
        with c9:
            skin_cancer = st.selectbox("Do you have Skin Cancer?", ["No", "Yes"])

        submitted = st.form_submit_button("🔍 Assess My Heart Risk", use_container_width=True)

        if submitted:
            payload = {
                "bmi": float(bmi),
                "smoking": 1 if smoking == "Yes" else 0,
                "alcohol_drinking": 1 if alcohol_drinking == "Yes" else 0,
                "stroke": 1 if stroke == "Yes" else 0,
                "physical_health": float(physical_health),
                "mental_health": float(mental_health),
                "diff_walking": 1 if diff_walking == "Yes" else 0,
                "sex": sex,
                "age_category": age_category,
                "diabetic": 1 if diabetic == "Yes" else 0,
                "physical_activity": 1 if physical_activity == "Yes" else 0,
                "gen_health": gen_health,
                "sleep_time": float(sleep_time),
                "asthma": 1 if asthma == "Yes" else 0,
                "kidney_disease": 1 if kidney_disease == "Yes" else 0,
                "skin_cancer": 1 if skin_cancer == "Yes" else 0,
            }
            with st.spinner("Analyzing your lifestyle profile for cardiovascular risk..."):
                res = predict_heart(payload)
                display_result_card(res, model_type="heart")

