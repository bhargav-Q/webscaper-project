@echo off
echo =======================================================
echo          Starting Quantana Web Scraper...
echo =======================================================

:: Start the Python FastAPI backend in a new command window
echo [1/2] Booting up Python Backend (Port 8000)...
start "Quantana Backend" cmd /k ".venv\Scripts\activate && uvicorn main:app --reload --port 8000"

:: Navigate to frontend and start the React app in a new command window
echo [2/2] Booting up React Frontend (Port 5173)...
cd frontend
start "Quantana Frontend" cmd /k "npm run dev"

echo.
echo All systems go! 🚀
echo The frontend will be available at http://localhost:5173
echo Close the two new terminal windows when you want to stop the servers.
echo.
pause
