import gspread
import os

# Caminho para as credenciais
creds_path = 'client_secret.json'
if not os.path.exists(creds_path):
    creds_path = os.path.join('python_brain', 'client_secret.json')

print("🔄 Conectando ao Google Sheets...")
gc = gspread.service_account(filename=creds_path)
sh = gc.open_by_key("14qM34cpPSK8rPcIfjQhY1kI1ysJBAdkaGa_xGX3TKao")
ws = sh.worksheet("Relatório_ROI_iFood")

# Dados corretos para corrigir a bagunça
updates = [
    {"id": "IF-99281", "val": 125.50},
    {"id": "IF-33211", "val": 45.90},
    {"id": "IF-88123", "val": 210.00},
    {"id": "IF-11029", "val": 89.90},
    {"id": "IF-55432", "val": 320.00},
    {"id": "IF-77654", "val": 15.00},
    {"id": "IF-22331", "val": 67.80}
]

print("🛠️ Corrigindo valores...")

# Pega todos os dados para encontrar as linhas certas
records = ws.get_all_records()

# Cria uma lista de células para atualizar em lote (mais rápido e seguro)
cells_to_update = []

for i, record in enumerate(records):
    row_num = i + 2 # +2 porque i começa em 0 e tem cabeçalho
    order_id = record.get("Order ID")
    
    for update in updates:
        if update["id"] == order_id:
            # Atualiza a coluna B (Valor)
            # gspread usa (row, col)
            print(f"   -> Ajustando {order_id}: de {record.get('Valor (R$)')} para {update['val']}")
            ws.update_cell(row_num, 2, update['val'])

print("✅ Valores corrigidos na planilha!")
