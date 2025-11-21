#!/bin/bash

# Script para testar múltiplos casos e popular o dashboard

echo "🧪 TESTE EM MASSA - Populando Dashboard"
echo "========================================"
echo ""

# Array de casos para testar
cases=(08 13 14)

for case_num in "${cases[@]}"; do
    echo "📋 Testando caso #$case_num..."
    ./test_case.sh "$case_num" 2>&1 | grep -E "(🤖|✅|📝|Pedido:)"
    echo ""
    sleep 2  # Pausa para não sobrecarregar a API
done

echo "✅ Teste concluído!"
echo "📊 Acesse o dashboard: https://docs.google.com/spreadsheets/d/14qM34cpPSK8rPcIfjQhY1kI1ysJBAdkaGa_xGX3TKao"
