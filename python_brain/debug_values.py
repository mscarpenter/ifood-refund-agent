import gspread
import pandas as pd
import os

# Caminho para as credenciais
creds_path = 'client_secret.json'
if not os.path.exists(creds_path):
    creds_path = os.path.join('python_brain', 'client_secret.json')

print(f"Lendo credenciais de: {creds_path}")
gc = gspread.service_account(filename=creds_path)
sh = gc.open_by_key("14qM34cpPSK8rPcIfjQhY1kI1ysJBAdkaGa_xGX3TKao")
ws = sh.worksheet("Relatório_ROI_iFood")

data = ws.get_all_records()
df = pd.DataFrame(data)

print("\n--- AMOSTRA DE DADOS ---")
print(df[['Order ID', 'Valor (R$)']].head(10))

print("\n--- TIPOS DE DADOS ---")
print(df['Valor (R$)'].apply(type).head(10))

print("\n--- VALORES BRUTOS ---")
for val in df['Valor (R$)'].head(10):
    print(f"Valor: {val!r} | Tipo: {type(val)}")
