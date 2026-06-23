@echo off
pushd "%~dp0"
title DolphiSIC Redesign Launcher

if not exist node_modules (
  echo Installation des dependances frontend...
  call npm install
  if errorlevel 1 goto :error
)

if not exist ".next\BUILD_ID" (
  echo Preparation initiale du frontend...
  call npm run build
  if errorlevel 1 goto :error
)

echo Lancement backend sur http://localhost:5001...
start "DolphiSIC Redesign Backend" cmd /k "cd /d ""%~dp0backend"" && set DOLPHISIC_PORT=5001 && python server.py"

echo Lancement frontend sur http://localhost:3005...
start "DolphiSIC Redesign Frontend" cmd /k "cd /d ""%~dp0"" && set NODE_OPTIONS=--no-deprecation && npm run start"

timeout /t 2 /nobreak >nul
start http://localhost:3005/
exit /b 0

:error
echo Installation impossible. Verifiez Node.js et npm.
pause
exit /b 1
