#!/bin/bash

# Se déplacer dans le dossier du script
cd "$(dirname "$0")"

echo "======================================================"
echo "    DolphiSIC Legacy - Démarrage sous Linux"
echo "======================================================"
echo ""

echo "Lancement du serveur DolphiSIC..."
python3 server.py
