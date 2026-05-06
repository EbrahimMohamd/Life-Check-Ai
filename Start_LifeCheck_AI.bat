@echo off
title LifeCheck AI - System Launcher
color 0B

echo ===================================================
echo           🧬 LIFECHECK AI PLATFORM 🧬
echo ===================================================
echo.
echo [1/2] Booting up the AI Backend (FastAPI)...
start "LifeCheck AI Backend Server" cmd /k "title LifeCheck Backend && python run.py"

echo.
echo Waiting for the Backend to fully load AI Models...
echo (It is scanning the server port. Please wait...)

:: Loop until the FastAPI server responds on port 8000
:wait_for_server
curl -s http://127.0.0.1:8000/docs > nul
if %errorlevel% neq 0 (
    timeout /t 1 /nobreak > nul
    goto wait_for_server
)

echo.
echo ✅ Backend Startup Complete! The AI is fully loaded into memory.
echo.
echo [2/2] Launching the User Interface (Streamlit)...
start "LifeCheck AI Frontend UI" cmd /k "title LifeCheck Frontend && python -m streamlit run frontend/app.py"

echo.
echo ===================================================
echo ✅ System is successfully running!
echo 🌐 The browser will open automatically.
echo ⚠️  Please DO NOT close the black terminal windows.
echo ===================================================
timeout /t 3 > nul
exit
