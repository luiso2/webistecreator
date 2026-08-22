#!/bin/bash
# Refresca las piezas del repo que el worker empaqueta (correr antes de railway up)
cd "$(dirname "$0")"
cp ../scripts/research_ig.py ../scripts/maps_research.py ../scripts/maps_discover.py ../scripts/build_maps_site.py ../scripts/derive.py ../scripts/gate.py scripts/
cp ../config.json config.json
mkdir -p templates/dark-v2 templates/assets
cp ../templates/dark-v2/index.html templates/dark-v2/
cp ../templates/.assetsignore-template templates/
cp ../templates/assets/tailwind.js templates/assets/
echo "paquete actualizado"
