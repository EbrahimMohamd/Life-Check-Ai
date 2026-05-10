import requests
import streamlit as st
import json

BASE_URL = "http://localhost:8000" 

def get_headers():
    token = st.session_state.get("auth_token")
    if token:
        return {"Authorization": f"Bearer {token}"}
    return {}

def login(username, password):
    try:
        response = requests.post(f"{BASE_URL}/auth/login", json={"username": username.strip(), "password": password})
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        try:
            return {"error": response.json().get("detail", str(e))}
        except Exception:
            return {"error": str(e)}
    except Exception as e:
        return {"error": str(e)}

def register(data: dict):
    try:
        response = requests.post(f"{BASE_URL}/auth/register", json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        try:
            return {"error": response.json().get("detail", str(e))}
        except Exception:
            return {"error": str(e)}
    except Exception as e:
        return {"error": str(e)}

def save_record(record_type: str, data_dict: dict):
    try:
        payload = {"record_type": record_type, "data_json": json.dumps(data_dict)}
        requests.post(f"{BASE_URL}/patient/records", json=payload, headers=get_headers())
    except Exception:
        pass

def get_patient_records():
    try:
        response = requests.get(f"{BASE_URL}/patient/records", headers=get_headers())
        response.raise_for_status()
        return response.json()
    except Exception:
        return []

def get_patient_profile():
    try:
        response = requests.get(f"{BASE_URL}/patient/profile", headers=get_headers())
        response.raise_for_status()
        return response.json()
    except Exception:
        return {}

def clear_history():
    try:
        response = requests.delete(f"{BASE_URL}/patient/records", headers=get_headers())
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        return {"error": response.json().get("detail", str(e))}
    except Exception as e:
        return {"error": str(e)}

def delete_account():
    try:
        response = requests.delete(f"{BASE_URL}/patient/account", headers=get_headers())
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        return {"error": response.json().get("detail", str(e))}
    except Exception as e:
        return {"error": str(e)}

def change_password(old_password, new_password):
    try:
        payload = {"old_password": old_password, "new_password": new_password}
        response = requests.put(f"{BASE_URL}/patient/password", json=payload, headers=get_headers())
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        return {"error": response.json().get("detail", str(e))}
    except Exception as e:
        return {"error": str(e)}

def send_chat_message(user_id: int, message: str) -> str:
    try:
        response = requests.post(f"{BASE_URL}/chat", json={"user_id": user_id, "message": message}, headers=get_headers())
        response.raise_for_status()
        res = response.json()

        return res.get("reply", "")
    except Exception as e:
        return f"Error communicating with chatbot: {str(e)}"

def predict_diabetes(payload: dict):
    try:
        response = requests.post(f"{BASE_URL}/predict/diabetes", json=payload, headers=get_headers())
        response.raise_for_status()
        res = response.json()
        save_record("Diabetes", {"payload": payload, "result": res})
        return res
    except Exception as e:
        return {"error": str(e)}

def predict_heart(payload: dict):
    try:
        response = requests.post(f"{BASE_URL}/predict/heart", json=payload, headers=get_headers())
        response.raise_for_status()
        res = response.json()
        save_record("Heart", {"payload": payload, "result": res})
        return res
    except Exception as e:
        return {"error": str(e)}

def predict_lung(image_bytes: bytes, filename: str, content_type: str):
    try:
        files = {"file": (filename, image_bytes, content_type)}
        response = requests.post(f"{BASE_URL}/predict/lung", files=files, headers=get_headers())
        response.raise_for_status()
        res = response.json()
        
        save_payload = {
            "prediction": res.get("prediction", "Error"),
            "confidence": res.get("confidence", 0.0)
        }
        save_record("Lung X-Ray", {"filename": filename, "AI_Diagnostics": save_payload})
        
        return res
    except requests.exceptions.HTTPError as e:
        try:
            return {"error": response.json().get("detail", str(e))}
        except Exception:
            return {"error": str(e)}
    except Exception as e:
        return {"error": str(e)}
