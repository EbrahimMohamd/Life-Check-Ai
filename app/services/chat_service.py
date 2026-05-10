import os, json
from app.chatbot_engine.extractor import extract
from app.chatbot_engine.triage import run
from app.chatbot_engine.rag import search
from app.chatbot_engine.generator import compose
from app.chatbot_engine.safety import guard
from app.chatbot_engine.utils_language import detect_language
from app.schemas.chat_schema import ChatReq, ChatRes

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
data_path = os.path.join(BASE_DIR, "data", "conditions.json")
try:
    CONDITIONS = json.load(open(data_path, encoding="utf-8"))
except FileNotFoundError:
    print(f"Warning: Could not load conditions from {data_path}. Initializing empty conditions.")
    CONDITIONS = []

USER_MEMORY = {}

def get_profile(uid):
    return {"name": "User", "BMI": 32, "glucose": 150, "age": 40}

def process_chat(req: ChatReq) -> ChatRes:

    lang = detect_language(req.message)


    g = guard(req.message)
    if g:
        return ChatRes(reply=g)

    profile = get_profile(req.user_id)


    mem = USER_MEMORY.setdefault(req.user_id, [])

  
    symptoms_data = extract(req.message)
    active_syms = [s["symptom"] for s in symptoms_data if not s["negated"]]


    mem.extend(active_syms)


    tri = run(symptoms_data, CONDITIONS, profile)


    docs = search(req.message, lang)


    reply = compose(profile, symptoms_data, tri, docs, mem, lang)

    return ChatRes(reply=reply)
