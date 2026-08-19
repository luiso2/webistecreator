#!/bin/bash
# Refresca las piezas del repo que el worker empaqueta (correr antes de railway up)
cd "$(dirname "$0")"
cp ../scripts/research_ig.py ../scripts/derive.py ../scripts/gate.py scripts/
cp ../templates/dark-v2/index.html templates/dark-v2/
cp ../templates/.assetsignore-template templates/
cp ../templates/assets/tailwind.js templates/assets/
echo "paquete actualizado"
