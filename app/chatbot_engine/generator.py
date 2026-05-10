FOLLOWUP_QUESTIONS_AR = [
    "هل تعاني من حمى؟",
    "هل يوجد فقدان في الوزن؟",
    "هل تعاني من ألم في الصدر؟",
    "هل الأعراض مستمرة منذ فترة طويلة؟"
]

FOLLOWUP_QUESTIONS_EN = [
    "Do you have fever?",
    "Do you have weight loss?",
    "Do you have chest pain?",
    "How long have you had these symptoms?"
]


def compose(profile, symptoms_data, tri, docs, memory, lang="ar"):

    # CASE 1: insufficient symptoms
    if tri.get("status") == "insufficient":
        if lang == "ar":
            return "الأعراض غير كافية لتحديد حالة واضحة.\n" + "\n".join(FOLLOWUP_QUESTIONS_AR)
        else:
            return "Symptoms are not sufficient to determine a condition.\n" + "\n".join(FOLLOWUP_QUESTIONS_EN)

    # CASE 2: no match
    if tri.get("status") == "no_match":
        if lang == "ar":
            return "الأعراض الحالية لا تشير إلى مرض واضح. قد تكون الحالة بسيطة."
        else:
            return "Your symptoms do not clearly indicate a specific disease. It may be a mild condition."

    # CASE 3: valid result
    lines = []

    if lang == "ar":
        lines.append("📊 التشخيص المتوقع:")
    else:
        lines.append("📊 Possible conditions:")

    for c, s in tri["top"]:
        #FIX
        name = c["name_ar"] if lang == "ar" else c["name_en"]
        lines.append(f"- {name} (~{round(s*100)}%)")

    top_condition = tri["top"][0][0]

    # Advice
    if lang == "ar":
        lines.append("\n💡 التوصيات:")
        for a in top_condition["advice_ar"]:
            lines.append(f"- {a}")
    else:
        lines.append("\n💡 Recommendations:")
        for a in top_condition["advice_en"]:
            lines.append(f"- {a}")

    # RAG info
    if docs:
        if lang == "ar":
            lines.append("\n📚 معلومات:")
        else:
            lines.append("\n📚 Info:")

        for d in docs[:1]:
            lines.append(f"- {d['text']}")

    # Memory
    if memory:
        if lang == "ar":
            lines.append("\n🧠 من المحادثة السابقة:")
        else:
            lines.append("\n🧠 From previous messages:")

        lines.append(", ".join(memory[-5:]))

    # Disclaimer
    if lang == "ar":
        lines.append("\n⚠️ هذا تقييم أولي وليس تشخيصًا طبيًا.")
    else:
        lines.append("\n⚠️ This is a preliminary assessment, not a medical diagnosis.")

    return "\n".join(lines)