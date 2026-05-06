def detect_language(text: str) -> str:
    """
    Detect Arabic or English
    """
    for char in text:
        if '\u0600' <= char <= '\u06FF':
            return "ar"
    return "en"