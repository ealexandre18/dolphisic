#!/bin/bash

cd "$(dirname "$0")"

echo "======================================"
echo "    DolphiSIC - Démarrage"
echo "======================================"
echo ""

echo "[1/2] Démarrage du Backend sur le port 5001..."
cd backend
export DOLPHISIC_PORT=5001
python3 server.py > backend.log 2>&1 &
BACKEND_PID=$!
cd ..

sleep 2

echo "[2/2] Démarrage du Frontend sur le port 3005..."
export NODE_OPTIONS="--no-deprecation"
npm run start &
FRONTEND_PID=$!

cleanup() {
    echo -e "\n\nArrêt des serveurs..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    echo "Serveurs arrêtés."
    exit 0
}

trap cleanup SIGINT

echo ""
echo "======================================"
echo "  DolphiSIC est en cours d'exécution !"
echo "  Accès : http://localhost:3005"
echo "  [CTRL+C pour arrêter]"
echo "======================================"
echo ""

wait
