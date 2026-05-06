from app.chatbot_engine.utils_language import detect_language

def guard(text: str):
    lang = detect_language(text)

    emergencies = ["chest pain", "heart attack", "كحة بدم", "ألم شديد"]

    for e in emergencies:
        if e in text.lower():
            if lang == "ar":
                return "⚠️ هذه حالة خطيرة، توجه إلى أقرب طوارئ فورًا"
            else:
                return "⚠️ This is a serious condition. Go to the nearest emergency immediately."

    return None