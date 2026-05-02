@echo off
TITLE MedReport Intelligence Platform - Launcher
echo ===================================================
echo   MEDREPORT INTELLIGENCE PLATFORM - LOCAL DEPLOY
echo ===================================================
echo.

:: Check for backend venv
if not exist "backend\venv" (
    echo [ERROR] Backend virtual environment not found in backend\venv.
    echo Please run 'cd backend && python -m venv venv' first.
    pause
    exit /b
)

:: Start Backend in a new window
echo [SYSTEM] Launching FastAPI Backend (Port 8000)...
start "MedReport-Backend" cmd /k "cd backend && venv\Scripts\activate && python -m uvicorn app:app --host 0.0.0.0 --port 8000 --reload"

:: Start Frontend in a new window
echo [SYSTEM] Launching Vite Frontend (Port 5173)...
start "MedReport-Frontend" cmd /k "cd frontend-react && npm run dev"

echo.
echo ===================================================
echo   SERVICES INITIALIZED SUCCESSFULLY
echo ===================================================
echo   Frontend: http://localhost:5173
echo   Backend API: http://localhost:8000/docs
echo ===================================================
echo.
echo Close the individual terminal windows to stop services.
pause
