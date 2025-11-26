import streamlit as st
import pandas as pd
import gspread
import plotly.express as px
import os
from datetime import datetime

# Configuração da Página
st.set_page_config(
    page_title="iFood Refund Agent Dashboard",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS Personalizado para Estilo Premium ---
# --- CSS Personalizado para Estilo Premium (Dark Mode iFood) ---
st.markdown("""
<style>
    /* Fundo Geral */
    .stApp {
        background-color: #121212;
        color: #ffffff;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #1e1e1e;
        border-right: 1px solid #333;
    }
    
    /* Métricas (Cards) */
    div[data-testid="metric-container"] {
        background-color: #1e1e1e;
        border: 1px solid #333;
        padding: 20px;
        border-radius: 8px;
        border-bottom: 3px solid #ea1d2c; /* Detalhe vermelho */
        transition: transform 0.2s;
    }
    div[data-testid="metric-container"]:hover {
        transform: translateY(-5px);
        box-shadow: 0 4px 15px rgba(234, 29, 44, 0.2);
    }
    
    /* Textos das Métricas */
    [data-testid="metric-container"] label {
        color: #aaaaaa;
        font-size: 0.9rem;
    }
    [data-testid="metric-container"] div[data-testid="stMetricValue"] {
        color: #ffffff;
        font-size: 1.8rem;
        font-weight: 700;
    }
    
    /* Títulos */
    h1, h2, h3 {
        color: #ffffff !important;
        font-family: 'Segoe UI', sans-serif;
    }
    
    /* Tabelas */
    [data-testid="stDataFrame"] {
        background-color: #1e1e1e;
        border-radius: 8px;
        padding: 10px;
    }
    
    /* Botões e Inputs */
    .stDateInput > div > div > input {
        color: #ffffff;
        background-color: #2d2d2d;
    }
</style>
""", unsafe_allow_html=True)

# --- Função de Carregamento de Dados ---
# @st.cache_data(ttl=60) # Cache removido temporariamente para debug
def load_data():
    try:
        # Caminho para as credenciais (ajuste conforme necessário)
        # Assumindo que estamos rodando da raiz do projeto ou da pasta dashboard
        # Tenta pegar do .env primeiro (mais seguro)
        from dotenv import load_dotenv
        load_dotenv()
        
        spreadsheet_id = os.getenv("SPREADSHEET_ID")
        
        # Caminho para as credenciais
        # Tenta achar o client_secret.json em vários lugares possíveis
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
            st.error("Arquivo client_secret.json não encontrado.")
            return pd.DataFrame()
             
        gc = gspread.service_account(filename=creds_path)
        
        if spreadsheet_id:
             sh = gc.open_by_key(spreadsheet_id)
        else:
             # Fallback para o ID antigo se não tiver no env (apenas para garantir retrocompatibilidade)
             sh = gc.open_by_key("14qM34cpPSK8rPcIfjQhY1kI1ysJBAdkaGa_xGX3TKao")
             
        # Tenta abrir a aba correta, se falhar tenta a primeira
        try:
            ws = sh.worksheet("Relatório_ROI_iFood")
        except:
            ws = sh.sheet1
        
        # Pega todos os dados
        data = ws.get_all_records()
        df = pd.DataFrame(data)
        
        # DEBUG: Mostra os dados brutos no app se necessário (comentado para produção)
        # st.write("Raw Data Sample:", df.head())
        
        # Limpeza e Conversão de Tipos
        if 'Valor (R$)' in df.columns:
            # Se já for numérico, não faz nada
            if not pd.api.types.is_numeric_dtype(df['Valor (R$)']):
                # Se for string, limpa R$, pontos de milhar e ajusta vírgula decimal
                df['Valor (R$)'] = df['Valor (R$)'].astype(str).str.replace('R$', '', regex=False).str.strip()
                
                # Função segura para converter
                def clean_currency(x):
                    if isinstance(x, str):
                        # Se tem vírgula, assume formato BR (1.000,00)
                        if ',' in x:
                            x = x.replace('.', '').replace(',', '.')
                        # Se não tem vírgula mas tem ponto, assume formato US (1000.00)
                        # (Nenhum tratamento especial necessário além do float())
                    return float(x)

                df['Valor (R$)'] = df['Valor (R$)'].apply(clean_currency)
            
        # Converte Data
        if 'Data' in df.columns:
            df['Data'] = pd.to_datetime(df['Data'])
            
        return df
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        return pd.DataFrame()

# --- Sidebar ---
st.sidebar.image("https://logodownload.org/wp-content/uploads/2017/05/ifood-logo-0.png", width=150)
st.sidebar.title("Filtros")

df = load_data()

if not df.empty:
    # Filtro de Data
    min_date = df['Data'].min().date()
    max_date = df['Data'].max().date()
    
    date_range = st.sidebar.date_input(
        "Período",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    
    # Filtra o DataFrame
    if len(date_range) == 2:
        mask = (df['Data'].dt.date >= date_range[0]) & (df['Data'].dt.date <= date_range[1])
        df_filtered = df.loc[mask]
    else:
        df_filtered = df

    # --- KPIs Principais ---
    st.title("🤖 Dashboard de Contestações")
    st.markdown(f"*Última atualização: {datetime.now().strftime('%d/%m/%Y %H:%M')}*")
    
    col1, col2, col3, col4 = st.columns(4)
    
    total_contestacoes = len(df_filtered)
    valor_total = df_filtered['Valor (R$)'].sum()
    ticket_medio = df_filtered['Valor (R$)'].mean()
    maior_valor = df_filtered['Valor (R$)'].max()
    
    col1.metric("Total Contestações", total_contestacoes, delta_color="off")
    col2.metric("Valor Recuperado", f"R$ {valor_total:,.2f}", delta_color="normal")
    col3.metric("Ticket Médio", f"R$ {ticket_medio:,.2f}")
    col4.metric("Maior Valor", f"R$ {maior_valor:,.2f}")
    
    st.markdown("---")
    
    # --- Gráficos ---
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.subheader("📈 Evolução Diária")
        # Agrupa por dia
        daily_data = df_filtered.groupby(df_filtered['Data'].dt.date)['Valor (R$)'].sum().reset_index()
        fig_line = px.line(daily_data, x='Data', y='Valor (R$)', markers=True, line_shape='spline')
        
        # Estilização Dark Mode para Plotly
        fig_line.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#ffffff',
            xaxis=dict(showgrid=False, color='#aaaaaa'),
            yaxis=dict(showgrid=True, gridcolor='#333333', color='#aaaaaa')
        )
        fig_line.update_traces(line_color='#ea1d2c', line_width=3)
        st.plotly_chart(fig_line, use_container_width=True)
        
    with col_right:
        st.subheader("🏆 Top 5 Maiores Valores")
        top_5 = df_filtered.nlargest(5, 'Valor (R$)')
        fig_bar = px.bar(top_5, x='Order ID', y='Valor (R$)', color='Valor (R$)', 
                         color_continuous_scale=[[0, '#ffcccc'], [1, '#ea1d2c']]) # Gradiente vermelho
        
        # Estilização Dark Mode para Plotly
        fig_bar.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#ffffff',
            xaxis=dict(showgrid=False, color='#aaaaaa'),
            yaxis=dict(showgrid=True, gridcolor='#333333', color='#aaaaaa'),
            coloraxis_showscale=False
        )
        st.plotly_chart(fig_bar, use_container_width=True)
        
    # --- Tabela de Detalhes ---
    st.subheader("📋 Detalhamento das Contestações")
    st.dataframe(
        df_filtered[['Order ID', 'Data', 'Valor (R$)', 'Defesa Gerada']].sort_values('Data', ascending=False),
        use_container_width=True,
        hide_index=True
    )

else:
    st.warning("Nenhum dado encontrado na planilha. Verifique a conexão ou se a planilha está vazia.")
