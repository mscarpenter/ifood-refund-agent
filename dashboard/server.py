from flask import Flask, render_template, jsonify
import gspread
import pandas as pd
import os
from datetime import datetime
from dotenv import load_dotenv

app = Flask(__name__)

# Configuração
load_dotenv()
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")

def get_data():
    try:
        # Busca credenciais
        possible_paths = [
            os.path.join(os.path.dirname(os.path.dirname(__file__)), 'python_brain', 'client_secret.json'),
            'client_secret.json',
            '../python_brain/client_secret.json'
        ]
        
        creds_path = None
        for path in possible_paths:
            if os.path.exists(path):
                creds_path = path
                break
        
        if not creds_path:
            return None

        gc = gspread.service_account(filename=creds_path)
        
        if SPREADSHEET_ID:
            sh = gc.open_by_key(SPREADSHEET_ID)
        else:
            sh = gc.open_by_key("14qM34cpPSK8rPcIfjQhY1kI1ysJBAdkaGa_xGX3TKao")

        try:
            ws = sh.worksheet("Relatório_ROI_iFood")
        except:
            ws = sh.sheet1
            
        data = ws.get_all_records()
        df = pd.DataFrame(data)
        
        # Limpeza de Dados Robusta
        if 'Valor (R$)' in df.columns:
            def clean_currency(x):
                # Se for número (int/float), aplica heurística de correção de decimal perdido
                if isinstance(x, (int, float)):
                    # Se for inteiro e parecer muito alto (ex: 1255 -> 125.5), divide por 10
                    # Isso corrige o erro de inserção onde 125.5 virou 1255
                    if x > 100 and isinstance(x, int): 
                         return float(x) / 10.0
                    return float(x)
                
                if isinstance(x, str):
                    clean = x.replace('R$', '').strip()
                    if ',' in clean and '.' in clean: # 1.000,00
                        clean = clean.replace('.', '').replace(',', '.')
                    elif ',' in clean: # 1000,00
                        clean = clean.replace(',', '.')
                    return float(clean) if clean else 0.0
                return 0.0
                
            df['Valor_Clean'] = df['Valor (R$)'].apply(clean_currency)
        
        if 'Data' in df.columns:
            df['Data_Clean'] = pd.to_datetime(df['Data'], errors='coerce')
            
        return df
    except Exception as e:
        print(f"Erro: {e}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/metrics')
def metrics():
    df = get_data()
    if df is None or df.empty:
        return jsonify({"error": "No data"})
        
    # KPIs
    total = len(df)
    valor_total = df['Valor_Clean'].sum()
    ticket_medio = df['Valor_Clean'].mean()
    
    # Gráfico Diário
    daily = df.groupby(df['Data_Clean'].dt.strftime('%Y-%m-%d'))['Valor_Clean'].sum().reset_index()
    
    # Top 5
    top5 = df.nlargest(5, 'Valor_Clean')[['Order ID', 'Valor_Clean']].to_dict('records')
    
    # Recentes - Formatando o valor para garantir consistência visual (R$ X.XXX,XX)
    def format_brl(val):
        return f"R$ {val:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    df['Valor_Formatado'] = df['Valor_Clean'].apply(format_brl)
    
    recent = df.sort_values('Data_Clean', ascending=False).head(10)[['Order ID', 'Data', 'Valor_Formatado', 'Defesa Gerada']].to_dict('records')

    return jsonify({
        "kpis": {
            "total": total,
            "valor_total": f"R$ {valor_total:,.2f}",
            "ticket_medio": f"R$ {ticket_medio:,.2f}"
        },
        "daily": {
            "labels": daily['Data_Clean'].tolist(),
            "values": daily['Valor_Clean'].tolist()
        },
        "top5": {
            "labels": [x['Order ID'] for x in top5],
            "values": [x['Valor_Clean'] for x in top5]
        },
        "recent": recent
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
