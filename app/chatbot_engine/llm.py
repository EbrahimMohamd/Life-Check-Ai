from transformers import AutoTokenizer, AutoModelForCausalLM
from app.chatbot_engine.config import LLM_MODEL, USE_LLM

_tokenizer = None
_model = None

def _load():
    global _tokenizer, _model
    if _tokenizer is None or _model is None:
        _tokenizer = AutoTokenizer.from_pretrained(LLM_MODEL)
        _model = AutoModelForCausalLM.from_pretrained(LLM_MODEL)

def refine(text: str) -> str:
    if not USE_LLM:
        return text
    _load()
    prompt = f"Improve clarity and tone without adding new medical facts:\n{text}"
    inputs = _tokenizer(prompt, return_tensors="pt")
    out = _model.generate(**inputs, max_new_tokens=200)
    return _tokenizer.decode(out[0], skip_special_tokens=True)