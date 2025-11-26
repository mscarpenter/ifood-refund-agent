import gspread
import os
import random
from datetime import datetime, timedelta

# Configuração
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CREDS_FILE = os.path.join(SCRIPT_DIR, 'client_secret.json')
SPREADSHEET_ID = "14qM34cpPSK8rPcIfjQhY1kI1ysJBAdkaGa_xGX3TKao"

def populate():
    print("🔐 Autenticando...")
    gc = gspread.service_account(filename=CREDS_FILE)
    sh = gc.open_by_key(SPREADSHEET_ID)
    
    # Tenta pegar a aba correta
    try:
        ws = sh.worksheet('Relatório_ROI_iFood')
    except:
        ws = sh.sheet1
        
    print(f"📝 Escrevendo na aba: {ws.title}")

    # Dados de exemplo
    data = [
        ['IF-99281', 125.50, (datetime.now() - timedelta(days=0)).strftime('%Y-%m-%d'), 'Contestação por PIN validado com sucesso.'],
        ['IF-33211', 45.90, (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d'), 'Cliente ausente no chat comprovado.'],
        ['IF-88123', 210.00, (datetime.now() - timedelta(days=2)).strftime('%Y-%m-%d'), 'Pedido não entregue (fraude suspeita).'],
        ['IF-11029', 89.90, (datetime.now() - timedelta(days=3)).strftime('%Y-%m-%d'), 'Item errado na entrega, evidência visual.'],
        ['IF-55432', 320.00, (datetime.now() - timedelta(days=4)).strftime('%Y-%m-%d'), 'Pedido grande cancelado indevidamente.'],
        ['IF-77654', 15.00, (datetime.now() - timedelta(days=0)).strftime('%Y-%m-%d'), 'Taxa de entrega reembolsada.'],
        ['IF-22331', 67.80, (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d'), 'Atraso justificado por chuva intensa.']
    ]

    for row in data:
        ws.append_row(row)
        print(f'✅ Adicionado: {row[0]} - R$ {row[1]}')

if __name__ == "__main__":
    populate()
