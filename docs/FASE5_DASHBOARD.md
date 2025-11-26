# 📊 Dashboard de Métricas

O **iFood Refund Agent** inclui um dashboard automático no Google Sheets para monitoramento em tempo real do ROI (Retorno sobre Investimento) e eficiência do sistema.

## 🎯 Visão Geral

O dashboard é dividido em duas abas principais:
1. **Dashboard**: Visualização consolidada com métricas, KPIs e tabelas dinâmicas.
2. **Relatório_ROI_iFood**: Base de dados bruta com o registro de todas as contestações geradas.

## 📈 Métricas Monitoradas

### KPIs Principais
- **Total de Contestações**: Volume total de casos processados.
- **Valor Total Recuperado (R$)**: Soma do impacto financeiro de todas as contestações ganhas/geradas.
- **Ticket Médio**: Valor médio por contestação.
- **Maior/Menor Valor**: Extremos financeiros processados.

### Análise Temporal
- **Hoje**: Contestações geradas no dia atual.
- **Esta Semana**: Volume acumulado na semana corrente.
- **Este Mês**: Volume acumulado no mês corrente.

### Top 5 Maiores Valores
Uma tabela dinâmica que lista automaticamente os 5 pedidos com maior valor financeiro contestado, útil para priorização de acompanhamento.

## 🛠️ Como Funciona

### Atualização Automática
O script `create_dashboard.py` configura a planilha com fórmulas do Google Sheets (`=SUM`, `=COUNTIF`, `=QUERY`). Isso significa que:
- O Python **não** precisa calcular as métricas a cada execução.
- O Python apenas adiciona uma nova linha na aba de dados (`Relatório_ROI_iFood`).
- O Google Sheets recalcula instantaneamente todas as métricas e gráficos no Dashboard.

### Estrutura de Dados (`Relatório_ROI_iFood`)

| Coluna | Campo | Descrição |
# 📊 Dashboard de Métricas

O **iFood Refund Agent** inclui um dashboard automático no Google Sheets para monitoramento em tempo real do ROI (Retorno sobre Investimento) e eficiência do sistema.

## 🎯 Visão Geral

O dashboard é dividido em duas abas principais:
1. **Dashboard**: Visualização consolidada com métricas, KPIs e tabelas dinâmicas.
2. **Relatório_ROI_iFood**: Base de dados bruta com o registro de todas as contestações geradas.

## 📈 Métricas Monitoradas

### KPIs Principais
- **Total de Contestações**: Volume total de casos processados.
- **Valor Total Recuperado (R$)**: Soma do impacto financeiro de todas as contestações ganhas/geradas.
- **Ticket Médio**: Valor médio por contestação.
- **Maior/Menor Valor**: Extremos financeiros processados.

### Análise Temporal
- **Hoje**: Contestações geradas no dia atual.
- **Esta Semana**: Volume acumulado na semana corrente.
- **Este Mês**: Volume acumulado no mês corrente.

### Top 5 Maiores Valores
Uma tabela dinâmica que lista automaticamente os 5 pedidos com maior valor financeiro contestado, útil para priorização de acompanhamento.

## 🛠️ Como Funciona

### Atualização Automática
O script `create_dashboard.py` configura a planilha com fórmulas do Google Sheets (`=SUM`, `=COUNTIF`, `=QUERY`). Isso significa que:
- O Python **não** precisa calcular as métricas a cada execução.
- O Python apenas adiciona uma nova linha na aba de dados (`Relatório_ROI_iFood`).
- O Google Sheets recalcula instantaneamente todas as métricas e gráficos no Dashboard.

### Estrutura de Dados (`Relatório_ROI_iFood`)

| Coluna | Campo | Descrição |
|--------|-------|-----------|
| A | Order ID | Identificador único do pedido |
| B | Valor (R$) | Valor financeiro contestado |
| C | Data | Data da contestação (AAAA-MM-DD) |
| D | Defesa | Texto da defesa gerada pela IA |

## 🚀 Como Rodar o Dashboard
 
O novo dashboard é uma aplicação web moderna rodando em Flask. Para acessá-lo:
 
1. Instale a dependência:
```bash
pip install flask
```
 
2. Execute o servidor:
```bash
python dashboard/server.py
```
 
3. Abra no navegador:
`http://127.0.0.1:5000`
 
O dashboard atualizará automaticamente a cada 30 segundos.
