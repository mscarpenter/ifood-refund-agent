#!/bin/bash

# Script para testar casos de teste do sistema de contestação

cd "$(dirname "$0")"

if [ -z "$1" ]; then
    echo "Uso: ./test_case.sh <numero_do_caso>"
    echo "Exemplo: ./test_case.sh 08"
    exit 1
fi

CASE_FILE="test_cases/${1}*.json"

if [ ! -f $CASE_FILE ]; then
    echo "Erro: Caso $1 não encontrado"
    exit 1
fi

echo "🧪 Testando caso: $CASE_FILE"
echo "================================"

python_brain/venv/bin/python python_brain/reimbursement_brain.py "$(cat $CASE_FILE)"
