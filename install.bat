@echo off
echo ==========================================
echo Installation des dependances du projet
echo ==========================================
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
if %ERRORLEVEL% equ 0 (
    echo.
    echo Installation terminee avec succes.
) else (
    echo.
    echo Une erreur est survenue lors de l'installation.
)
pause
