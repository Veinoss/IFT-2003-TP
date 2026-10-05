#!/usr/bin/env bash
set -e

echo "=========================================="
echo "Installation des dépendances du projet"
echo "=========================================="

python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt

echo ""
echo "Installation terminée avec succès."
