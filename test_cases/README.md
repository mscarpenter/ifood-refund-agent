# Test Cases - Sistema de Contestação Automatizada

## Visão Geral

Este diretório contém 10 casos de teste sintéticos que cobrem **todos os cenários** da matriz de regras de cancelamento e reembolso do iFood.

Cada arquivo JSON representa um pedido real com:
- Timestamps detalhados
- Histórico de chat
- Dados de GPS/telemetria
- Evidências de entrega
- **Resultado esperado** (para validação do agente)

---

## Índice de Casos

| Arquivo | Cenário | Ação Esperada | Complexidade |
|---------|---------|---------------|--------------|
| `01_pre_confirmacao.json` | Cancelamento antes da loja aceitar | Aceitar (sem custo) | ⭐ |
| `02_preparo_no_prazo.json` | Cancelamento durante preparo (no prazo) | Loja pode recusar | ⭐⭐ |
| `03_preparo_atrasado_10min.json` | **Caso de borda**: Exatos 10min de atraso | Aceitar (limite da regra) | ⭐⭐⭐ |
| `04_preparo_atrasado_15min.json` | Atraso claro (20min) no preparo | Aceitar (culpa do restaurante) | ⭐⭐ |
| `05_entrega_no_prazo.json` | Cancelamento durante entrega (no prazo) | Aceitar sem reembolso | ⭐⭐ |
| `06_entrega_atrasada_culpa_loja.json` | Atraso por despacho tardio | Aceitar (culpa do restaurante) | ⭐⭐⭐ |
| `07_entrega_atrasada_culpa_logistica.json` | Atraso por logística iFood | **CONTESTAR** (culpa da plataforma) | ⭐⭐⭐⭐ |
| `08_pos_entrega_pin_validado.json` | Cliente reclama MAS PIN foi validado | **CONTESTAR** (fraude provável) | ⭐⭐⭐⭐⭐ |
| `09_pos_entrega_sem_pin.json` | Cliente ausente (15min de espera) | **CONTESTAR** (cliente não atendeu) | ⭐⭐⭐⭐ |
| `10_fraude_suspeita.json` | Padrão de fraude (53% de reembolsos) | **CONTESTAR** (histórico suspeito) | ⭐⭐⭐⭐⭐ |

---

## Como Usar

### Testar um caso específico:
```bash
cd python_brain
./venv/bin/python reimbursement_brain.py "$(cat ../test_cases/08_pos_entrega_pin_validado.json)"
```

### Rodar todos os casos (script de validação):
```bash
# TODO: Criar script test_all_cases.sh
```

---

## Estrutura do JSON

Cada caso segue este schema:

```json
{
  "order_id": "UNIQUE-ID",
  "reason_code": "ITEM_NOT_RECEIVED | QUALITY_ISSUE | TAKING_TOO_LONG | CHANGED_MIND",
  "financial_impact": 125.00,
  "timestamps": {
    "created_at": "ISO8601",
    "confirmed_at": "ISO8601 ou null",
    "eta_max": "ISO8601",
    "dispatched_at": "ISO8601 ou null",
    "actual_arrival_at": "ISO8601 ou null"
  },
  "delivery_evidence": {
    "gps_logs": [...],
    "delivery_pin_validated": true/false,
    "pin_validated_at": "ISO8601 ou null",
    "contact_attempts": 0-5
  },
  "chat_history": [...],
  "expected_result": {
    "action": "CONTESTAR | ACEITAR_CANCELAMENTO | RECUSAR_CANCELAMENTO",
    "reason": "Justificativa técnica",
    "should_contest": true/false,
    "confidence": 0.0-1.0
  }
}
```

---

## Casos Críticos para Demonstração

Para uma apresentação impactante, recomendo focar nestes 3:

1. **`08_pos_entrega_pin_validado.json`**: Mostra o agente detectando fraude (PIN validado)
2. **`07_entrega_atrasada_culpa_logistica.json`**: Mostra análise de GPS para isentar o restaurante
3. **`10_fraude_suspeita.json`**: Mostra análise de padrão comportamental

---

## Próximos Passos

- [ ] Criar script `test_all_cases.sh` para validação automatizada
- [ ] Adicionar mais variações (ex: acordos informais no chat)
- [ ] Incluir casos com imagens (Fase 3 do plano)
