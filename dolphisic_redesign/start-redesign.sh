#!/bin/bash

# Se déplacer dans le dossier du script
cd "$(dirname "$0")"

echo "======================================================"
echo "    DolphiSIC Redesign - Démarrage sous Linux"
echo "======================================================"
echo ""

# 1. Démarrer le backend en arrière-plan
echo "[1/2] Démarrage du Backend sur le port 5001..."
cd backend
export DOLPHISIC_PORT=5001
python3 server.py > backend.log 2>&1 &
BACKEND_PID=$!
cd ..

# Attendre 2 secondes
sleep 2

# 2. Démarrer le frontend
echo "[2/2] Démarrage du Frontend sur le port 3005..."
export NODE_OPTIONS="--no-deprecation"
npm run start &
FRONTEND_PID=$!

# Gérer l'arrêt propre avec Ctrl+C
cleanup() {
    echo -e "\n\nArrêt des serveurs..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    echo "Serveurs arrêtés."
    exit 0
}

trap cleanup SIGINT

# Garder le script actif pour intercepter le Ctrl+C
echo ""
echo "======================================================"
echo "  DolphiSIC est en cours d'exécution !"
echo "  Accès site : http://localhost:3005"
echo "  [Appuyez sur CTRL+C pour arrêter les serveurs]"
echo "======================================================"
echo ""

wait
