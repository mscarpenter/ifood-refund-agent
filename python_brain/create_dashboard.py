#!/usr/bin/env python3
"""
Script para criar o Dashboard de Métricas no Google Sheets com Design Premium (Inspirado no iFood).
"""

import os
import gspread
from datetime import datetime
from dotenv import load_dotenv

# Configuração
load_dotenv()
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CREDS_FILE = os.path.join(SCRIPT_DIR, 'client_secret.json')

# --- PALETA DE CORES IFOOD (Baseada na Referência) ---
IFOOD_RED_PRIMARY = {'red': 0.917, 'green': 0.113, 'blue': 0.141} # #EA1D2C (Vermelho Vibrante)
IFOOD_RED_DARK = {'red': 0.6, 'green': 0.0, 'blue': 0.0} # Vinho/Bordô (Rodapé da imagem)
BG_OFF_WHITE = {'red': 0.98, 'green': 0.98, 'blue': 0.98} # Fundo quase branco
CARD_WHITE = {'red': 1.0, 'green': 1.0, 'blue': 1.0}
TEXT_DARK = {'red': 0.1, 'green': 0.1, 'blue': 0.1} # Preto suave
TEXT_GRAY = {'red': 0.4, 'green': 0.4, 'blue': 0.4} # Cinza texto

def create_dashboard():
    print("🔐 Autenticando com Google Sheets...")
    
    if not SPREADSHEET_ID:
        raise ValueError("SPREADSHEET_ID não encontrado no arquivo .env")

    gc = gspread.service_account(filename=CREDS_FILE)
    spreadsheet = gc.open_by_key(SPREADSHEET_ID)
    
    # --- 1. PREPARAÇÃO DAS ABAS ---
    try:
        dashboard = spreadsheet.worksheet("Dashboard")
        print("⚠️  Aba Dashboard já existe. Limpando para recriar...")
        dashboard.clear()
        # Reset de formatação
        dashboard.format("A1:Z100", {"backgroundColor": BG_OFF_WHITE})
    except gspread.exceptions.WorksheetNotFound:
        print("📊 Criando nova aba Dashboard...")
        dashboard = spreadsheet.add_worksheet(title="Dashboard", rows=60, cols=15)
    
    # Garante aba de dados
    try:
        data_sheet = spreadsheet.worksheet("Relatório_ROI_iFood")
    except gspread.exceptions.WorksheetNotFound:
        print("📝 Criando aba de dados...")
        data_sheet = spreadsheet.add_worksheet(title="Relatório_ROI_iFood", rows=1000, cols=10)
        data_sheet.append_row(["Order ID", "Valor (R$)", "Data", "Defesa Gerada"])

    # --- 2. ESTRUTURA E FÓRMULAS ---
    print("🎨 Construindo layout premium iFood...")

    updates = []
    
    # CABEÇALHO (Hero Section)
    updates.append({'range': 'B2', 'values': [['iFood Refund Agent']]})
    updates.append({'range': 'B3', 'values': [[f'Painel de Controle Financeiro • Atualizado: {datetime.now().strftime("%d/%m/%Y %H:%M")}']]})

    # KPIS (Métricas Chave)
    # Vamos usar uma linha de cards limpos
    kpi_titles = ['TOTAL CONTESTADO', 'RECUPERADO (R$)', 'TICKET MÉDIO', 'HOJE']
    kpi_formulas = [
        '=COUNTA(Relatório_ROI_iFood!A:A)-1',
        '=SUM(Relatório_ROI_iFood!B:B)',
        '=IFERROR(AVERAGE(Relatório_ROI_iFood!B:B), 0)',
        '=COUNTIF(Relatório_ROI_iFood!C:C,TODAY())'
    ]
    
    # Posicionamento dos KPIs: B5, E5, H5, K5 (Espaçamento maior)
    col_map = ['B', 'E', 'H', 'K']
    
    for i, title in enumerate(kpi_titles):
        updates.append({'range': f'{col_map[i]}5', 'values': [[title]]})
        updates.append({'range': f'{col_map[i]}6', 'values': [[kpi_formulas[i]]]})

    # TABELA TOP 5 (Lado Esquerdo)
    updates.append({'range': 'B10', 'values': [['MAIORES RECUPERAÇÕES']]})
    updates.append({'range': 'B11:D11', 'values': [['PEDIDO', 'VALOR', 'DATA']]})
    updates.append({'range': 'B12', 'values': [['=QUERY(Relatório_ROI_iFood!A:C,"SELECT A, B, C ORDER BY B DESC LIMIT 5",1)']]})

    # TABELA RECENTES (Lado Direito)
    updates.append({'range': 'H10', 'values': [['ÚLTIMAS ATIVIDADES']]})
    updates.append({'range': 'H11:J11', 'values': [['PEDIDO', 'VALOR', 'DATA']]})
    # Query para pegar os últimos 5 (assumindo ordem de inserção, pegamos do fim)
    # Como QUERY não tem OFFSET reverso fácil sem coluna de ID sequencial, vamos ordenar por data DESC
    updates.append({'range': 'H12', 'values': [['=QUERY(Relatório_ROI_iFood!A:C,"SELECT A, B, C ORDER BY C DESC LIMIT 5",1)']]})

    # Aplica os dados
    dashboard.batch_update(updates)

    # --- 3. FORMATAÇÃO VISUAL (ESTILO IFOOD) ---
    print("✨ Aplicando identidade visual...")

    # 3.1 Cabeçalho (Fundo Vermelho iFood)
    dashboard.merge_cells("A1:O4")
    dashboard.format("A1:O4", {
        "backgroundColor": IFOOD_RED_PRIMARY,
        "verticalAlignment": "MIDDLE"
    })
    
    # Texto do Título
    dashboard.format("B2", {
        "textFormat": {"foregroundColor": CARD_WHITE, "fontSize": 28, "bold": True, "fontFamily": "Montserrat"},
        "horizontalAlignment": "LEFT"
    })
    # Subtítulo
    dashboard.format("B3", {
        "textFormat": {"foregroundColor": CARD_WHITE, "fontSize": 11},
        "horizontalAlignment": "LEFT"
    })

    # 3.2 Cards de KPI (Estilo "Flutuante")
    # Para cada KPI, vamos formatar um bloco de 3x3 células (ex: B5:C7)
    # Mas como estamos usando colunas espaçadas (B, E, H, K), vamos formatar o bloco de 2 colunas
    
    kpi_ranges = [("B", "C"), ("E", "F"), ("H", "I"), ("K", "L")]
    
    for start, end in kpi_ranges:
        # Fundo Branco e Borda Suave
        rng = f"{start}5:{end}7"
        dashboard.merge_cells(rng)
        dashboard.format(rng, {
            "backgroundColor": CARD_WHITE,
            "borders": {
                "bottom": {"style": "SOLID", "width": 3, "color": IFOOD_RED_PRIMARY}, # Detalhe vermelho embaixo
            },
            "horizontalAlignment": "CENTER",
            "verticalAlignment": "MIDDLE"
        })
        
        # Título (Pequeno, Cinza) - Precisamos reinserir o texto pois o merge limpa visualmente se não for o top-left
        # Como mesclamos B5:C7, o valor deve estar em B5.
        # Ajuste: Vamos escrever Título em B5 e Valor em B6, mas mesclar tudo? Não.
        # Melhor: Mesclar B5:C5 (Título) e B6:C7 (Valor)
        
        dashboard.unmerge_cells(rng) # Desfaz o merge total
        
        # Título
        dashboard.merge_cells(f"{start}5:{end}5")
        dashboard.format(f"{start}5", {
            "backgroundColor": CARD_WHITE,
            "horizontalAlignment": "LEFT",
            "padding": {"left": 10},
            "textFormat": {"fontSize": 9, "foregroundColor": TEXT_GRAY, "bold": True}
        })
        
        # Valor
        dashboard.merge_cells(f"{start}6:{end}7")
        dashboard.format(f"{start}6", {
            "backgroundColor": CARD_WHITE,
            "horizontalAlignment": "LEFT",
            "padding": {"left": 10},
            "textFormat": {"fontSize": 22, "foregroundColor": TEXT_DARK, "bold": True},
            "borders": {
                 "bottom": {"style": "SOLID", "width": 3, "color": IFOOD_RED_PRIMARY}
            }
        })

    # Formatação de Moeda nos KPIs
    dashboard.format("E6", {"numberFormat": {"type": "CURRENCY", "pattern": "R$ #,##0.00"}})
    dashboard.format("H6", {"numberFormat": {"type": "CURRENCY", "pattern": "R$ #,##0.00"}})

    # 3.3 Tabelas (Clean Design)
    # Cabeçalhos
    table_headers = ["B11:D11", "H11:J11"]
    for rng in table_headers:
        dashboard.format(rng, {
            "backgroundColor": CARD_WHITE,
            "textFormat": {"foregroundColor": IFOOD_RED_PRIMARY, "bold": True, "fontSize": 10},
            "borders": {"bottom": {"style": "SOLID", "width": 1, "color": IFOOD_RED_PRIMARY}},
            "horizontalAlignment": "LEFT"
        })
    
    # Títulos das Seções
    dashboard.format("B10", {"textFormat": {"fontSize": 14, "bold": True, "foregroundColor": TEXT_DARK}})
    dashboard.format("H10", {"textFormat": {"fontSize": 14, "bold": True, "foregroundColor": TEXT_DARK}})

    # Dados das Tabelas
    dashboard.format("B12:D17", {"backgroundColor": CARD_WHITE, "textFormat": {"fontSize": 10, "foregroundColor": TEXT_GRAY}})
    dashboard.format("H12:J17", {"backgroundColor": CARD_WHITE, "textFormat": {"fontSize": 10, "foregroundColor": TEXT_GRAY}})
    
    # Coluna de Valor em Negrito e Moeda
    dashboard.format("C12:C17", {"textFormat": {"bold": True, "foregroundColor": TEXT_DARK}, "numberFormat": {"type": "CURRENCY", "pattern": "R$ #,##0.00"}})
    dashboard.format("I12:I17", {"textFormat": {"bold": True, "foregroundColor": TEXT_DARK}, "numberFormat": {"type": "CURRENCY", "pattern": "R$ #,##0.00"}})

    # --- 4. GRÁFICOS ---
    print("📊 Gerando gráficos...")
    
    # Gráfico de Colunas (Top 5) - Usando cores do iFood
    chart_spec = {
        "requests": [
            {
                "addChart": {
                    "chart": {
                        "spec": {
                            "title": "Performance de Recuperação",
                            "basicChart": {
                                "chartType": "COLUMN",
                                "legendPosition": "NO_LEGEND",
                                "axis": [
                                    {"position": "BOTTOM_AXIS", "title": "Pedido"},
                                    {"position": "LEFT_AXIS", "title": "Valor Recuperado"}
                                ],
                                "domains": [{"domain": {"sourceRange": {"sources": [{"sheetId": dashboard.id, "startRowIndex": 11, "endRowIndex": 16, "startColumnIndex": 1, "endColumnIndex": 2}]}}}],
                                "series": [{"series": {"sourceRange": {"sources": [{"sheetId": dashboard.id, "startRowIndex": 11, "endRowIndex": 16, "startColumnIndex": 2, "endColumnIndex": 3}]}}, "targetAxis": "LEFT_AXIS", "color": IFOOD_RED_PRIMARY}]
                            }
                        },
                        "position": {
                            "overlayPosition": {
                                "anchorCell": {"sheetId": dashboard.id, "rowIndex": 20, "columnIndex": 1}, # B21
                                "widthPixels": 450,
                                "heightPixels": 300
                            }
                        }
                    }
                }
            },
             {
                "addChart": {
                    "chart": {
                        "spec": {
                            "title": "Tendência Temporal",
                            "basicChart": {
                                "chartType": "AREA", # Área para ficar mais bonito
                                "legendPosition": "NO_LEGEND",
                                "axis": [
                                    {"position": "BOTTOM_AXIS", "title": "Data"},
                                    {"position": "LEFT_AXIS", "title": "Volume"}
                                ],
                                "domains": [{"domain": {"sourceRange": {"sources": [{"sheetId": dashboard.id, "startRowIndex": 11, "endRowIndex": 16, "startColumnIndex": 9, "endColumnIndex": 10}]}}}], # Data da tabela 2
                                "series": [{"series": {"sourceRange": {"sources": [{"sheetId": dashboard.id, "startRowIndex": 11, "endRowIndex": 16, "startColumnIndex": 8, "endColumnIndex": 9}]}}, "targetAxis": "LEFT_AXIS", "color": IFOOD_RED_DARK}]
                            }
                        },
                        "position": {
                            "overlayPosition": {
                                "anchorCell": {"sheetId": dashboard.id, "rowIndex": 20, "columnIndex": 7}, # H21
                                "widthPixels": 450,
                                "heightPixels": 300
                            }
                        }
                    }
                }
            }
        ]
    }

    try:
        spreadsheet.batch_update(chart_spec)
        print("✅ Gráficos adicionados!")
    except Exception as e:
        print(f"⚠️ Erro ao criar gráficos: {e}")

    # Rodapé (Inspirado na imagem - Fundo Vermelho Escuro)
    dashboard.merge_cells("A40:O42")
    dashboard.format("A40:O42", {
        "backgroundColor": IFOOD_RED_DARK,
        "horizontalAlignment": "CENTER",
        "verticalAlignment": "MIDDLE"
    })
    dashboard.update("B41", [["Desenvolvido com IA Generativa • iFood Refund Agent"]])
    dashboard.format("B41", {"textFormat": {"foregroundColor": CARD_WHITE, "fontSize": 10}})

    # Ajuste final
    dashboard.update_index(0)
    print("✅ Dashboard Premium iFood Style criado com sucesso!")
    print(f"🔗 Acesse: https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}")

if __name__ == "__main__":
    try:
        create_dashboard()
    except Exception as e:
        print(f"❌ Erro: {e}")
