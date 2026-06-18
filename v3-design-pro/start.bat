@echo off
:: Se placer dans le répertoire du .bat, quelle que soit l'origine du lancement
pushd "%~dp0"

title DolphiSIC Web App Launcher
echo ======================================================
echo    DolphiSIC - Gestion de Parc Radio ^& Cartographie
echo ======================================================
echo.

echo [1/2] Verification des dependances Python...
python -c "import flask, flask_cors" 2>NUL
if errorlevel 1 (
    echo Flask ou Flask-CORS manquant. Installation...
    pip install flask flask-cors
) else (
    echo Dependances Python OK.
)

echo.
echo [2/2] Recuperation de l'adresse IP locale...
for /f "tokens=*" %%i in ('python -c "import socket; s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM); s.connect((chr(56)+chr(46)+chr(56)+chr(46)+chr(56)+chr(46)+chr(56),80)); print(s.getsockname()[0]); s.close()"') do set LOCAL_IP=%%i

echo.
echo ======================================================
echo   DolphiSIC Web est pret !
echo.
echo   Sur cet ordinateur  : http://localhost:5000
echo   Sur le reseau local : http://%LOCAL_IP%:5000
echo.
echo   --> Partagez l'URL reseau aux autres appareils
echo       connectes sur le meme Wi-Fi / reseau
echo ======================================================
echo.

echo Lancement du serveur DolphiSIC...
start "DolphiSIC Server" /min cmd /c "cd /d "%~dp0" && python server.py"

echo Attente du demarrage (2 secondes)...
timeout /t 2 /nobreak >nul

echo Ouverture dans le navigateur...
start http://localhost:5000/

echo.
echo ======================================================
echo  [Appuyez sur une touche pour arreter le serveur]
echo ======================================================
pause >nul

echo.
echo Arret du serveur...
taskkill /fi "windowtitle eq DolphiSIC Server*" /f >nul 2>&1
echo Serveur arrete.
timeout /t 1 >nul
