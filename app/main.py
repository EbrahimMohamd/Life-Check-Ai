from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import chat, diabetes, heart, lung, auth, patient
from app.db.database import engine
from app.db import models

# Initialize the database tables if they do not exist
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="LifeCheck AI API")

# Add CORS middleware to allow all origins since Streamlit runs on a different port locally
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(chat.router)
app.include_router(diabetes.router)
app.include_router(heart.router)
app.include_router(lung.router)
app.include_router(auth.router)
app.include_router(patient.router)

@app.get("/")
def root():
    return {"message": "Welcome to LifeCheck AI API Backend!"}