from fpdf import FPDF
from services.api_client import get_patient_profile, get_patient_records
import json

class PDFReport(FPDF):
    def header(self):
        import os
        logo_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'logo.jpg')
        if os.path.exists(logo_path):
            self.image(logo_path, 10, 8, 12)  # x, y, width
        
        # Shift text to the right to avoid overlapping the logo
        self.set_font('helvetica', 'B', 15)
        self.set_text_color(37, 99, 235) # blue
        self.cell(15) # Spacing for logo
        self.cell(0, 10, 'LifeCheck AI - Confidential Medical Report', border=False, ln=1, align='C')
        self.set_draw_color(37, 99, 235)
        self.line(10, 22, 200, 22)
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 8)
        self.set_text_color(128)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def get_clinical_suggestion(record_type, data_dict):
    """Generate dynamic clinical advice based on AI findings."""
    rt = str(record_type).lower()

    # ── Extract the result dict (handles nested or flat structures) ──
    # Stored as: {"payload": {...}, "result": {"risk_level": "High", ...}}
    # OR lung:   {"filename": "...", "AI_Diagnostics": {"prediction": "Malignant", ...}}
    result = data_dict.get("result", {})
    ai_diag = data_dict.get("AI_Diagnostics", {})

    risk_level = str(result.get("risk_level", data_dict.get("risk_level", ""))).lower()
    prediction = str(
        ai_diag.get("prediction",
        result.get("prediction",
        data_dict.get("prediction", "")))
    ).lower()

    # ── Combine signals ──
    signal = risk_level + " " + prediction

    # ── LUNG CANCER — 3 classes ──
    if "lung" in rt:
        if "malignant" in signal:
            return (
                "[URGENT] ONCOLOGY REFERRAL REQUIRED. High probability of malignant neoplasm detected. "
                "Recommend immediate contrast-enhanced CT scan, PET-CT imaging, and pulmonology consult "
                "for potential biopsy and staging workup. Do not delay."
            )
        elif "benign" in signal:
            return (
                "[CAUTION] Non-malignant findings detected. While no active malignancy is indicated, "
                "recommend a follow-up chest X-Ray or CT in 3-6 months to confirm stability. "
                "Discuss with a pulmonologist if respiratory symptoms persist."
            )
        else:  # Normal
            return (
                "[CLEAR] Normal lung parenchyma - no concerning opacities or nodules detected. "
                "Continue routine annual chest screening, especially if you are a smoker or "
                "have occupational exposure to carcinogens."
            )

    # ── DIABETES — High / Low ──
    elif "diabetes" in rt:
        if "high" in signal:
            return (
                "[HIGH RISK] Endocrinology consult strongly recommended. "
                "Initiate daily blood glucose monitoring and fasting HbA1c test. "
                "Restrict simple carbohydrates and processed sugars. "
                "Evaluate pharmacological intervention (e.g., Metformin) with your doctor. "
                "Target 150+ minutes of aerobic exercise per week."
            )
        else:  # Low
            return (
                "[LOW RISK] Low diabetes risk based on your current lifestyle profile. "
                "Maintain a balanced diet rich in whole grains, vegetables, and lean protein. "
                "Keep BMI in a healthy range and stay physically active. "
                "Annual blood glucose check is still recommended as a preventive measure."
            )

    # ── HEART DISEASE — High / Low ──
    elif "heart" in rt:
        if "high" in signal:
            return (
                "[HIGH RISK] Schedule an urgent cardiology consultation. "
                "Recommend stress ECG test, lipid panel, and echocardiogram. "
                "Avoid extreme physical exertion until medically cleared. "
                "Review blood pressure medications if applicable. "
                "Adopt a Mediterranean diet and eliminate smoking immediately."
            )
        else:  # Low
            return (
                "[LOW RISK] Low cardiovascular risk based on your lifestyle assessment. "
                "Maintain current healthy habits: regular exercise, balanced diet low in saturated fats, "
                "and no smoking. Annual blood pressure and cholesterol checks are advised. "
                "Continue monitoring BMI and sleep quality."
            )

    return "Please consult with your primary healthcare provider to review these AI diagnostic results."


def generate_patient_pdf():
    profile = get_patient_profile()
    records = get_patient_records()
    
    pdf = PDFReport()
    pdf.add_page()
    
    # --- HEADER / PROFILE SECTION ---
    pdf.set_font("helvetica", 'B', 14)
    pdf.set_text_color(15, 23, 42) # Slate 900
    pdf.cell(0, 10, "Patient Demographics & Profile", ln=1)
    
    pdf.set_font("helvetica", '', 11)
    pdf.set_fill_color(248, 250, 252) # Soft Slate 50
    pdf.set_draw_color(203, 213, 225) # Border Slate 300
    
    profile_text = (
        f"  Full Name:   {profile.get('full_name', 'N/A')}\n"
        f"  Age:         {profile.get('age', 'N/A')} Years Old\n"
        f"  Biological Sex: {profile.get('gender', 'N/A')}\n"
        f"  Contact Email: {profile.get('email', 'N/A')}"
    )
    pdf.multi_cell(0, 8, profile_text, fill=True, border=1)
    pdf.ln(10)
    
    # --- DIAGNOSTIC HISTORY ---
    pdf.set_font("helvetica", 'B', 14)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(0, 10, "AI Diagnostic History & Clinical Advisory", ln=1)
    pdf.ln(2)
    
    if not records:
        pdf.set_font("helvetica", 'I', 11)
        pdf.cell(0, 10, "No medical records found on your profile.", ln=1)
    else:
        for rec in records:
            # Title for each record
            pdf.set_font("helvetica", 'B', 12)
            pdf.set_text_color(37, 99, 235) # Blue Primary
            
            rt = str(rec.get('record_type', 'Unknown')).upper()
            date_str = str(rec.get('created_at', ''))[:10]
            pdf.cell(0, 8, f"-> {rt} ASSESSMENT (Date: {date_str})", ln=1)
            
            # Parse JSON data
            data_dict = {}
            try:
                data_dict = json.loads(rec.get('data_json', '{}'))
            except:
                pass
            
            # Print core metrics
            pdf.set_font("helvetica", '', 10)
            pdf.set_text_color(51, 65, 85) # Slate 700
            
            for k, v in data_dict.items():
                if isinstance(v, dict):
                    pdf.set_font("helvetica", 'B', 10)
                    pdf.cell(0, 6, f"  {str(k).upper()} METRICS:", ln=1)
                    pdf.set_font("helvetica", '', 10)
                    for sub_k, sub_v in v.items():
                        safe_val = str(sub_v).encode('ascii', 'ignore').decode()
                        pdf.cell(10) # indent
                        pdf.cell(0, 6, f"- {sub_k}: {safe_val}", ln=1)
                else:
                    safe_val = str(v).encode('ascii', 'ignore').decode()
                    if k.lower() in ['prediction', 'risk_level']:
                         # highlight primary finding
                         pdf.set_font("helvetica", 'B', 10)
                         pdf.set_text_color(220, 38, 38) if 'high' in safe_val.lower() or 'malignant' in safe_val.lower() else pdf.set_text_color(15, 23, 42)
                         pdf.cell(0, 6, f"  > Diagnostic Result: {safe_val}", ln=1)
                         pdf.set_text_color(51, 65, 85)
                         pdf.set_font("helvetica", '', 10)
                    else:
                         pdf.cell(0, 6, f"  {str(k).replace('_', ' ').title()}: {safe_val}", ln=1)
            
            # --- AI SUGGESTION BLOCK ---
            pdf.ln(2)
            pdf.set_font("helvetica", 'B', 10)
            pdf.set_text_color(15, 118, 110) # Teal 700 for medical advice
            pdf.cell(0, 6, "  [+] Clinical Recommendation & Plan:", ln=1)
            
            suggestion = get_clinical_suggestion(rt, data_dict)
            pdf.set_font("helvetica", 'I', 10)
            pdf.set_text_color(15, 23, 42)
            # Indent block using multi_cell X offset roughly
            pdf.set_x(15)
            pdf.multi_cell(0, 6, f'"{suggestion}"')
            
            # Separator Line
            pdf.ln(5)
            self_draw_line = pdf.get_y()
            pdf.set_draw_color(226, 232, 240) # Slate 200 light separator
            pdf.line(10, self_draw_line, 200, self_draw_line)
            pdf.ln(6)
            
    # Final Disclaimer Footer
    pdf.ln(10)
    pdf.set_font("helvetica", 'I', 8)
    pdf.set_text_color(100, 116, 139)
    pdf.multi_cell(0, 4, "DISCLAIMER: This document is generated by an Artificial Intelligence (LifeCheck AI). It does NOT constitute an official medical diagnosis. Always consult a licensed healthcare professional before making any medical decisions.", align='C')
    
    return pdf.output(dest='S').encode('latin-1')
