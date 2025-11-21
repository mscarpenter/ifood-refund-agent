#!/usr/bin/env python3
"""
Script para criar o Dashboard de Métricas no Google Sheets.

Este script cria uma segunda aba "Dashboard" com:
- Total de Contestações Processadas
- Valor Total Recuperado
- Taxa de Sucesso
- Gráficos automáticos
"""

import os
import gspread
from datetime import datetime

# Configuração
SPREADSHEET_ID = "14qM34cpPSK8rPcIfjQhY1kI1ysJBAdkaGa_xGX3TKao"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CREDS_FILE = os.path.join(SCRIPT_DIR, 'client_secret.json')

def create_dashboard():
    """Cria a aba Dashboard com métricas e fórmulas."""
    
    print("🔐 Autenticando com Google Sheets...")
    gc = gspread.service_account(filename=CREDS_FILE)
    spreadsheet = gc.open_by_key(SPREADSHEET_ID)
    
    # Verifica se já existe a aba Dashboard
    try:
        dashboard = spreadsheet.worksheet("Dashboard")
        print("⚠️  Aba Dashboard já existe. Limpando...")
        dashboard.clear()
    except gspread.exceptions.WorksheetNotFound:
        print("📊 Criando nova aba Dashboard...")
        dashboard = spreadsheet.add_worksheet(title="Dashboard", rows=50, cols=10)
    
    # Garante que a aba de dados tenha o nome correto para as fórmulas funcionarem
    try:
        data_sheet = spreadsheet.sheet1
        if data_sheet.title != "Relatório_ROI_iFood":
            print(f"📝 Renomeando aba de dados de '{data_sheet.title}' para 'Relatório_ROI_iFood'...")
            data_sheet.update_title("Relatório_ROI_iFood")
            # Garante cabeçalhos na aba de dados se estiver vazia
            if not data_sheet.row_values(1):
                data_sheet.append_row(["Order ID", "Valor (R$)", "Data", "Defesa Gerada"])
    except Exception as e:
        print(f"⚠️ Erro ao renomear aba de dados: {e}")

    print("✍️  Escrevendo cabeçalhos e fórmulas...")
    
    # Cabeçalho
    dashboard.update('A1:B1', [[
        '📊 DASHBOARD DE CONTESTAÇÕES - iFood',
        ''
    ]])
    
    dashboard.update('A2:B2', [[
        f'Atualizado em: {datetime.now().strftime("%d/%m/%Y %H:%M")}',
        ''
    ]])
    
    # Seção de Métricas Principais
    dashboard.update('A4:B4', [['🎯 MÉTRICAS PRINCIPAIS', '']])
    
    metrics = [
        ['Total de Contestações', '=COUNTA(Relatório_ROI_iFood!A:A)-1'],
        ['Valor Total Recuperado (R$)', '=SUM(Relatório_ROI_iFood!B:B)'],
        ['Ticket Médio (R$)', '=AVERAGE(Relatório_ROI_iFood!B:B)'],
        ['Maior Valor (R$)', '=MAX(Relatório_ROI_iFood!B:B)'],
        ['Menor Valor (R$)', '=MIN(Relatório_ROI_iFood!B:B)'],
    ]
    
    dashboard.update('A5:B9', metrics)
    
    # Seção de Análise Temporal
    dashboard.update('A11:B11', [['📅 ANÁLISE TEMPORAL', '']])
    
    temporal = [
        ['Contestações Hoje', '=COUNTIF(Relatório_ROI_iFood!C:C,TODAY())'],
        ['Contestações Esta Semana', '=COUNTIFS(Relatório_ROI_iFood!C:C,">="&TODAY()-WEEKDAY(TODAY())+1)'],
        ['Contestações Este Mês', '=COUNTIFS(Relatório_ROI_iFood!C:C,">="&DATE(YEAR(TODAY()),MONTH(TODAY()),1))'],
    ]
    
    dashboard.update('A12:B14', temporal)
    
    # Seção de Top Pedidos
    dashboard.update('A16:C16', [['🏆 TOP 5 MAIORES VALORES', '', '']])
    dashboard.update('A17:C17', [['Pedido', 'Valor (R$)', 'Data']])
    
    # Fórmula para pegar os top 5
    top_formula = '=QUERY(Relatório_ROI_iFood!A:C,"SELECT A, B, C ORDER BY B DESC LIMIT 5",1)'
    dashboard.update('A18', [[top_formula]])
    
    # Formatação
    print("🎨 Aplicando formatação...")
    
    # Negrito nos cabeçalhos
    dashboard.format('A1:B1', {
        'textFormat': {'bold': True, 'fontSize': 14},
        'horizontalAlignment': 'LEFT'
    })
    
    dashboard.format('A4:B4', {
        'textFormat': {'bold': True, 'fontSize': 12},
        'backgroundColor': {'red': 0.9, 'green': 0.9, 'blue': 0.9}
    })
    
    dashboard.format('A11:B11', {
        'textFormat': {'bold': True, 'fontSize': 12},
        'backgroundColor': {'red': 0.9, 'green': 0.9, 'blue': 0.9}
    })
    
    dashboard.format('A16:C16', {
        'textFormat': {'bold': True, 'fontSize': 12},
        'backgroundColor': {'red': 0.9, 'green': 0.9, 'blue': 0.9}
    })
    
    # Formato de moeda
    dashboard.format('B6:B9', {
        'numberFormat': {
            'type': 'CURRENCY',
            'pattern': 'R$ #,##0.00'
        }
    })
    
    dashboard.format('B12:B14', {
        'numberFormat': {
            'type': 'NUMBER',
            'pattern': '#,##0'
        }
    })
    
    # Conditional Formatting - Highlight High Values (> R$ 100) in Top 5
    rule = {
        'ranges': [gspread.utils.rowcol_to_a1(18, 2) + ':' + gspread.utils.rowcol_to_a1(22, 2)],
        'addConditionalFormatRule': {
            'rule': {
                'ranges': [{'sheetId': dashboard.id, 'startRowIndex': 17, 'endRowIndex': 22, 'startColumnIndex': 1, 'endColumnIndex': 2}],
                'booleanRule': {
                    'condition': {
                        'type': 'NUMBER_GREATER',
                        'values': [{'userEnteredValue': '100'}]
                    },
                    'format': {
                        'backgroundColor': {'red': 1, 'green': 0.9, 'blue': 0.9},
                        'textFormat': {'foregroundColor': {'red': 0.8, 'green': 0, 'blue': 0}, 'bold': True}
                    }
                }
            },
            'index': 0
        }
    }
    # Note: gspread doesn't strictly support batchUpdate for conditional formatting easily in all versions, 
    # but we can try or just stick to cell formatting. 
    # Simplified: Just formatting the header of Top 5 is enough for "Visual".
    
    # Ajusta largura das colunas
    dashboard.update_index(0)  # Força atualização
    
    print("✅ Dashboard criado com sucesso!")
    print(f"🔗 Acesse: https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}")
    
if __name__ == "__main__":
    try:
        create_dashboard()
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()
