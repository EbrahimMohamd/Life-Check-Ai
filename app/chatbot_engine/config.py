import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# LLM (اختياري)
USE_LLM = False
LLM_MODEL = "microsoft/Phi-3-mini-4k-instruct"

# RAG
EMBEDDING_MODEL = os.path.join(BASE_DIR, "local_models", "all-MiniLM-L6-v2")
TOP_K = 3

# thresholds
FUZZY_THRESHOLD = 85
CONF_MIN_FOR_MATCH = 0.2
HIGH_RISK_THRESHOLD = 0.6
MED_RISK_THRESHOLD = 0.3

# follow-up questions (عند نقص الأعراض)
FOLLOWUP_QUESTIONS = [
    "هل في حمى أو سخونية؟",
    "هل في ألم في الصدر أو ضيق تنفس؟",
    "هل في غثيان أو قيء؟",
    "هل الأعراض مستمرة من قد إيه؟",
    "هل في فقدان وزن غير مبرر؟"
]