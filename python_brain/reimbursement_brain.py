import os
import json
import sys # Importa para ler argumentos de linha de comando (n8n)
import time # Para data
import gspread # Para Google Sheets
import traceback # Para debug de erros
from datetime import datetime, timedelta
from typing import Optional, List

# Bibliotecas (Google e LangChain)
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain_core.prompts import ChatPromptTemplate

# --- NOVO: FUNÇÃO DE ESCRITA DE ROI ---
def log_roi_to_sheet(data):
    """Autentica e anexa uma linha de dados à planilha."""
    try:
        # 1. Autenticação (usa o client_secret.json na pasta)
        # O arquivo client_secret.json deve estar na mesma pasta do script
        json_creds = os.path.join(os.path.dirname(__file__), 'client_secret.json')
        gc = gspread.service_account(filename=json_creds)
        
        # 2. Abre a planilha pelo ID (mais seguro que nome)
        spreadsheet = gc.open_by_key("14qM34cpPSK8rPcIfjQhY1kI1ysJBAdkaGa_xGX3TKao")
        
        # 3. Seleciona a primeira aba
        worksheet = spreadsheet.sheet1
        
        # 4. Dados para anexar (Append Row)
        row = [
            data.get("order_id"),
            data.get("financial_impact"),
            time.strftime("%Y-%m-%d"), # Data formatada
            data.get("generated_defense")[:500] # Limita a 500 caracteres para não quebrar a célula
        ]
        
        worksheet.append_row(row)
        print("✅ Dados de ROI registrados com sucesso via Gspread!", file=sys.stderr)
        return True
        
    except Exception as e:
        print(f"❌ ERRO GRAVE NO GSHEETS: {str(e)}", file=sys.stderr)
        print(traceback.format_exc(), file=sys.stderr)
        return False

# --- NOVO: ANÁLISE DE IMAGENS COM GEMINI VISION ---
def analyze_image_evidence(image_path: str, claim_type: str, order_details: dict) -> dict:
    """
    Analisa evidência fotográfica usando Gemini 2.0 Flash Vision.
    
    Args:
        image_path: Caminho local ou URL da imagem
        claim_type: Tipo de reclamação (QUALITY_ISSUE, WRONG_ITEM, etc)
        order_details: Detalhes do pedido para contexto
    
    Returns:
        dict com verdict, confidence e reasoning
    """
    try:
        print(f"🔍 Analisando evidência fotográfica para {claim_type}...", file=sys.stderr)
        
        # Inicializa o modelo com capacidade de visão
        vision_model = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash-exp",
            temperature=0.1  # Baixa temperatura para análise objetiva
        )
        
        # Monta o prompt de análise forense
        analysis_prompt = f"""
Você é um perito forense especializado em análise de evidências visuais para casos de reembolso de delivery.

CONTEXTO DO PEDIDO:
- Order ID: {order_details.get('order_id', 'N/A')}
- Alegação do Cliente: {claim_type}
- Valor Financeiro: R$ {order_details.get('financial_impact', 0):.2f}

TAREFA:
Analise a imagem fornecida e determine:

1. **Autenticidade**: A foto parece genuína ou há sinais de manipulação/encenação?
2. **Consistência**: A alegação do cliente é visualmente comprovada pela imagem?
3. **Gravidade**: Se o problema existe, qual a severidade (leve/moderada/grave)?

RESPONDA EM JSON:
{{
    "verdict": "ACEITAR_REEMBOLSO" ou "NEGAR_REEMBOLSO" ou "ANALISE_HUMANA",
    "confidence": 0.0 a 1.0,
    "reasoning": "Explicação técnica detalhada",
    "red_flags": ["lista de sinais suspeitos, se houver"]
}}

SEJA RIGOROSO: Fraudes são comuns. Busque inconsistências.
"""
        
        # Se for caminho local, lê a imagem
        if os.path.exists(image_path):
            import base64
            from langchain_core.messages import HumanMessage
            
            with open(image_path, "rb") as img_file:
                image_data = base64.b64encode(img_file.read()).decode('utf-8')
                
            # Gemini aceita imagens em base64 via HumanMessage
            message = HumanMessage(
                content=[
                    {"type": "text", "text": analysis_prompt},
                    {
                        "type": "image_url",
                        "image_url": f"data:image/jpeg;base64,{image_data}"
                    }
                ]
            )
            response = vision_model.invoke([message])
        else:
            # Se for URL, passa direto
            from langchain_core.messages import HumanMessage
            
            message = HumanMessage(
                content=[
                    {"type": "text", "text": analysis_prompt},
                    {"type": "image_url", "image_url": image_path}
                ]
            )
            response = vision_model.invoke([message])
        
        # Parse da resposta JSON
        result = json.loads(response.content)
        print(f"✅ Análise de imagem concluída: {result['verdict']}", file=sys.stderr)
        return result
        
    except Exception as e:
        print(f"❌ ERRO na análise de imagem: {str(e)}", file=sys.stderr)
        print(traceback.format_exc(), file=sys.stderr)
        # Em caso de erro, escala para humano
        return {
            "verdict": "ANALISE_HUMANA",
            "confidence": 0.0,
            "reasoning": f"Erro técnico na análise: {str(e)}",
            "red_flags": ["erro_sistema"]
        }

# --- NOVO: ANÁLISE DE SENTIMENTO E CONTEXTO DO CHAT ---
def analyze_chat_context(chat_history: List[dict], order_details: dict) -> dict:
    """
    Analisa o histórico de chat para detectar nuances importantes.
    
    Args:
        chat_history: Lista de mensagens do chat
        order_details: Detalhes do pedido para contexto
    
    Returns:
        dict com findings, sentiment, e red_flags
    """
    try:
        if not chat_history or len(chat_history) == 0:
            return {
                "has_chat": False,
                "findings": [],
                "sentiment": "neutral",
                "red_flags": []
            }
        
        print(f"💬 Analisando {len(chat_history)} mensagens do chat...", file=sys.stderr)
        
        # Formata o chat para análise
        chat_text = "\n".join([
            f"{msg.get('timestamp', 'N/A')} - {msg.get('sender', 'unknown')}: {msg.get('text', '')}"
            for msg in chat_history
        ])
        
        # Prompt de análise
        analysis_prompt = f"""
Você é um analista especializado em comunicação de delivery e detecção de fraudes.

CONTEXTO DO PEDIDO:
- Order ID: {order_details.get('order_id', 'N/A')}
- Motivo da Reclamação: {order_details.get('reason_code', 'N/A')}

HISTÓRICO DO CHAT:
{chat_text}

TAREFA:
Analise o chat e identifique:

1. **Acordos Informais**: O cliente fez algum acordo sobre local de entrega? (ex: "deixa na portaria", "deixa com o vizinho")
2. **Cliente Ausente**: Há evidências de que o cliente não respondeu tentativas de contato?
3. **Tentativas de Contato**: Quantas vezes o entregador/restaurante tentou contato?
4. **Tom da Conversa**: Cordial, neutro, agressivo, ou suspeito?
5. **Sinais de Fraude**: Mudança abrupta de comportamento, reclamação tardia sem mencionar problema antes, etc.

RESPONDA EM JSON:
{{
    "has_chat": true,
    "informal_agreement": {{
        "exists": true/false,
        "details": "descrição do acordo, se houver"
    }},
    "customer_absent": {{
        "likely": true/false,
        "evidence": "evidências, se houver"
    }},
    "contact_attempts": 0-10,
    "sentiment": "cordial" ou "neutral" ou "agressivo" ou "suspeito",
    "findings": ["lista de descobertas importantes"],
    "red_flags": ["lista de sinais suspeitos"]
}}

SEJA OBJETIVO E BASEADO EM FATOS.
"""
        
        # Chama o LLM para análise
        response = llm.invoke(analysis_prompt)
        
        # Parse da resposta JSON (pode vir dentro de ```json```)
        response_text = response.content.strip()
        
        # Se vier em markdown, extrai o JSON
        if response_text.startswith("```"):
            # Remove ```json e ```
            response_text = response_text.split("```")[1]
            if response_text.startswith("json"):
                response_text = response_text[4:].strip()
        
        result = json.loads(response_text)
        print(f"✅ Análise de chat concluída: {len(result.get('findings', []))} descobertas", file=sys.stderr)
        return result
        
    except Exception as e:
        print(f"❌ ERRO na análise de chat: {str(e)}", file=sys.stderr)
        print(traceback.format_exc(), file=sys.stderr)
        return {
            "has_chat": True,
            "findings": [],
            "sentiment": "unknown",
            "red_flags": ["erro_analise"],
            "error": str(e)
        }

# --- NOVO: NOTIFICAÇÃO VIA TELEGRAM PARA APROVAÇÃO HUMANA ---
def send_telegram_approval(contestation_data: dict) -> dict:
    """
    Envia notificação no Telegram para aprovação humana.
    
    Args:
        contestation_data: Dados da contestação gerada
    
    Returns:
        dict com status do envio
    """
    try:
        import requests
        
        # Carrega credenciais do Telegram do .env
        telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")
        telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID")
        
        if not telegram_token or not telegram_chat_id:
            print("⚠️ Telegram não configurado. Pulando aprovação humana.", file=sys.stderr)
            return {"sent": False, "reason": "not_configured"}
        
        # Formata a mensagem
        message = f"""
🤖 **Contestação Pronta para Revisão**

🎯 **Pedido:** `{contestation_data.get('order_id')}`
💰 **Valor:** R$ {contestation_data.get('financial_impact', 0):.2f}
⚖️ **Ação:** {contestation_data.get('action')}
🎯 **Confiança:** {contestation_data.get('confidence', 0)*100:.0f}%

📝 **Defesa Gerada:**
{contestation_data.get('generated_defense', 'N/A')[:500]}...

✅ Aprovar e enviar?
🚫 Rejeitar?
        """
        
        # Envia via Telegram Bot API
        url = f"https://api.telegram.org/bot{telegram_token}/sendMessage"
        payload = {
            "chat_id": telegram_chat_id,
            "text": message,
            "parse_mode": "Markdown"
        }
        
        response = requests.post(url, json=payload, timeout=10)
        
        if response.status_code == 200:
            print("✅ Notificação enviada no Telegram!", file=sys.stderr)
            return {"sent": True, "message_id": response.json().get("result", {}).get("message_id")}
        else:
            print(f"❌ Erro ao enviar Telegram: {response.text}", file=sys.stderr)
            return {"sent": False, "error": response.text}
            
    except Exception as e:
        print(f"❌ ERRO no Telegram: {str(e)}", file=sys.stderr)
        print(traceback.format_exc(), file=sys.stderr)
        return {"sent": False, "error": str(e)}

# Imports para o RAG
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings 
from langchain.chains import RetrievalQA

# Carregar variáveis de ambiente (.env)
load_dotenv()

# === 1. CONFIGURAÇÃO DO LLM ===
if not os.getenv("GOOGLE_API_KEY"):
    # Se a chave não estiver no .env, levanta um erro claro
    raise ValueError("A chave GOOGLE_API_KEY não foi encontrada no arquivo .env")

# O modelo Gemini 2.0 Flash é o que está funcionando para você
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash", 
    temperature=0,
    max_retries=2,
)

# --- CONFIGURAÇÃO DO RAG ---
VECTOR_DB_DIR = "chroma_db_ifood"
embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004") 

# Carrega o banco vetorial persistente
rag_db = Chroma(persist_directory=VECTOR_DB_DIR, embedding_function=embeddings)

# Cria a Cadeia de Recuperação (Retrieval Chain)
# O Gemini agora pode consultar a política de reembolso
retriever = rag_db.as_retriever()
rag_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever
)
# --- FIM CONFIGURAÇÃO DO RAG ---

# === 2. ESTRUTURAS DE DADOS (MODELOS Pydantic) ===
class Timestamps(BaseModel):
    # Campos que exigem tratamento de data/hora
    eta_max: datetime
    actual_arrival_at: Optional[datetime] = None

class DeliveryEvidence(BaseModel):
    gps_logs: List[dict]
    delivery_pin_validated: bool = False 
    pin_validated_at: Optional[datetime] = None

class OrderData(BaseModel):
    order_id: str
    reason_code: str
    financial_impact: Optional[float] = 0.0
    timestamps: Timestamps
    delivery_evidence: DeliveryEvidence
    chat_history: List[dict]
    photo_evidence_url: Optional[str] = None  # URL ou caminho da foto de evidência

# === 3. PROMPT DO CONSULTOR (Didático e Transparente) ===
# O LLM será usado para gerar a comunicação, não apenas a decisão
communication_prompt = ChatPromptTemplate.from_template("""
Você é um **Consultor de Conciliação Financeira do iFood** e especialista em Políticas de Cancelamento, focado em educação e transparência para o Parceiro (Restaurante).

OBJETIVO DA RESPOSTA: Gerar a comunicação oficial que será enviada para o restaurante.

SITUAÇÃO DO CASO: {situation}
EVIDÊNCIA CHAVE: {evidence}
REGRA OFICIAL (Base de Conhecimento): {rule_official}

CONTEXTO:
Pedido ID: {order_id}. O cliente alegou: "{customer_claim}"

TAREFA:
1. Mantenha o tom profissional, claro e educacional.
2. Explique em um parágrafo curto se a contestação do cliente foi **ACATADA** ou **NEGADA**, citando a regra oficial e a evidência de forma didática.
3. Se a ação é CONTESTAR (ou seja, NEGADA para o cliente, acatada para o parceiro), termine reforçando a importância do procedimento de PIN como prova.
4. Se a ação é ACEITAR CANCELAMENTO (ou seja, PERDIDA para o parceiro), termine sugerindo a revisão dos processos internos (logística/preparo) para evitar futuras perdas.

Resposta:
""")


# === 4. MOTOR HÍBRIDO (Estrutura Corrigida para RAG) ===
def process_refund_request(json_data: str):
    try:
        order = OrderData(**json.loads(json_data))
        print(f"Gemini 🤖 analisando Pedido: {order.order_id}...", file=sys.stderr)
        
        action = "PENDING"
        
        # --- LÓGICA DE TRATAMENTO DE REGRAS RÍGIDAS (HARD RULES) ---
        
        # REGRA A: Validação do PIN (Caso Ganho do Parceiro - Prioridade Máxima)
        if order.delivery_evidence.delivery_pin_validated:
            action = "CONTESTAR"
            
            # Buscamos a regra oficial do PIN no RAG para justificar
            rag_query = "Regra de comprovação de entrega e uso do PIN"
            situation = "A contestação do cliente é improcedente, pois o pedido foi recebido pelo titular da conta."
            evidence = f"Código PIN validado com sucesso às {order.delivery_evidence.pin_validated_at}."
        
        # REGRA C: Análise de Imagem para Reclamações de Qualidade (ANTES da Regra B)
        elif order.reason_code == "QUALITY_ISSUE" and hasattr(order, 'photo_evidence_url') and order.photo_evidence_url:
            print("📸 Detectada reclamação de qualidade com evidência fotográfica...", file=sys.stderr)
            
            # Chama a análise de imagem
            image_analysis = analyze_image_evidence(
                image_path=order.photo_evidence_url,
                claim_type=order.reason_code,
                order_details={
                    "order_id": order.order_id,
                    "financial_impact": order.financial_impact
                }
            )
            
            # Decide com base no veredito da IA
            if image_analysis["verdict"] == "NEGAR_REEMBOLSO":
                action = "CONTESTAR"
                rag_query = "Regra sobre reclamações de qualidade sem evidência comprovada"
                situation = f"A contestação do cliente foi NEGADA. Análise da imagem: {image_analysis['reasoning']}"
                evidence = f"Confiança da análise: {image_analysis['confidence']*100:.0f}%. Red flags: {', '.join(image_analysis.get('red_flags', []))}"
            
            elif image_analysis["verdict"] == "ACEITAR_REEMBOLSO":
                action = "ACEITAR_CANCELAMENTO"
                rag_query = "Regra sobre vícios de qualidade comprovados"
                situation = f"A contestação do cliente foi ACATADA. Problema de qualidade confirmado visualmente."
                evidence = f"Análise da imagem: {image_analysis['reasoning']}"
            
            else:  # ANALISE_HUMANA
                return {
                    "action": "PENDING",
                    "order_id": order.order_id,
                    "financial_impact": order.financial_impact,
                    "image_analysis": image_analysis,
                    "error": "Análise de imagem inconclusiva. Requer revisão humana."
                }
            
        # REGRA B: Tolerância de Atraso (Caso Perdido do Parceiro)
        # Verifica se há tempo de chegada e se o PIN não foi validado (caso contrário, a REGRA A já teria resolvido)
        elif order.timestamps.actual_arrival_at:
            tolerance_limit = order.timestamps.eta_max + timedelta(minutes=15)
            
            if order.timestamps.actual_arrival_at > tolerance_limit:
                action = "ACEITAR_CANCELAMENTO"
                
                # Buscamos a regra oficial de atraso no RAG para justificar
                rag_query = "Qual a regra oficial sobre o cancelamento durante a entrega por atraso?"
                situation = "A contestação do cliente foi acatada. O atraso logístico excedeu o limite máximo de 15 minutos."
                evidence = f"A entrega ocorreu em {order.timestamps.actual_arrival_at.time()}, excedendo o limite de {tolerance_limit.time()}."

            else:
                # Se chegou a tempo, mas não tem PIN, analisa o chat para entender o contexto
                print("🔍 Entrega no prazo sem PIN. Analisando chat para contexto...", file=sys.stderr)
                
                chat_analysis = analyze_chat_context(
                    chat_history=order.chat_history,
                    order_details={
                        "order_id": order.order_id,
                        "reason_code": order.reason_code
                    }
                )
                
                # Se o cliente estava ausente (não respondeu), o restaurante pode contestar
                if chat_analysis.get("customer_absent", {}).get("likely", False):
                    action = "CONTESTAR"
                    rag_query = "Regra sobre responsabilidade quando o cliente não atende o entregador"
                    situation = f"A contestação do cliente foi NEGADA. O cliente estava ausente no momento da entrega."
                    evidence = f"Análise do chat: {chat_analysis.get('customer_absent', {}).get('evidence', 'Cliente não respondeu')}. Tentativas de contato: {chat_analysis.get('contact_attempts', 0)}"
                
                # Se houve acordo informal (ex: deixar na portaria), depende do contexto
                elif chat_analysis.get("informal_agreement", {}).get("exists", False):
                    # Se o cliente fez acordo informal E reclama que não recebeu, é suspeito
                    if order.reason_code == "ITEM_NOT_RECEIVED":
                        action = "CONTESTAR"
                        rag_query = "Regra sobre acordos de entrega em local alternativo"
                        situation = f"A contestação do cliente foi NEGADA. Houve acordo informal de entrega."
                        evidence = f"Acordo detectado: {chat_analysis.get('informal_agreement', {}).get('details', 'N/A')}"
                    else:
                        # Outros motivos com acordo informal precisam de análise humana
                        return {
                            "action": "PENDING",
                            "order_id": order.order_id,
                            "financial_impact": order.financial_impact,
                            "chat_analysis": chat_analysis,
                            "error": "Acordo informal detectado. Requer análise humana."
                        }
                
                # Se não há evidências claras, precisa de análise humana
                else:
                    return {
                        "action": "PENDING",
                        "order_id": order.order_id,
                        "financial_impact": order.financial_impact,
                        "chat_analysis": chat_analysis,
                        "error": "Análise de chat inconclusiva. Requer revisão humana."
                    }

        else:
            # Caso não tenha dados de chegada
            return {
                "action": "PENDING",
                "order_id": order.order_id,
                "financial_impact": order.financial_impact,
                "error": "Dados de timestamp incompletos."
            }

        
        # --- EXECUÇÃO DA CADEIA RAG/GEMINI PARA COMUNICAÇÃO ---
        if action != "PENDING":
            print("🧠 Consultando base de política para obter texto oficial...", file=sys.stderr)
            # Chamada principal do RAG com a query específica
            rag_response = rag_chain.run(rag_query)
            
            print(f"⚡ Regra detectada: {action}. Gerando Comunicação...", file=sys.stderr)
            
            # Formatamos o prompt com os dados e a resposta do RAG
            final_communication = communication_prompt.format(
                situation=situation,
                evidence=evidence,
                rule_official=rag_response, # Usamos o texto recuperado do RAG
                order_id=order.order_id,
                customer_claim=order.reason_code
            )
            
            # Chamamos o LLM final para escrever o texto didático
            defense_text = llm.invoke(final_communication)

            if action == "CONTESTAR":
                # Se a ação for CONTESTAR, envia notificação no Telegram para aprovação
                telegram_result = send_telegram_approval({
                    "order_id": order.order_id,
                    "financial_impact": order.financial_impact,
                    "action": action,
                    "confidence": 1.0,
                    "generated_defense": defense_text.content
                })
                
                # Se houver sucesso, registra a linha na planilha
                print("📝 Registrando contestação na planilha...", file=sys.stderr)
                data_to_log = {
                    "order_id": order.order_id,
                    "financial_impact": order.financial_impact,
                    "generated_defense": defense_text.content
                }
                log_roi_to_sheet(data_to_log)

            # Retorna o resultado final
            return {
                "action": action,
                "order_id": order.order_id,
                "financial_impact": order.financial_impact,
                "confidence": 1.0,
                "model_used": "Gemini 2.0 Flash (RAG Ativo)",
                "generated_defense": defense_text.content
            }
        
        # Se action for PENDING (que só acontece se a lógica 'else' falhar)
        return {
            "action": action,
            "order_id": order.order_id,
            "financial_impact": order.financial_impact,
            "confidence": 0.5,
            "generated_defense": "Requer análise humana."
        }


    except Exception as e:
        # Se houver erro de Pydantic ou JSON malformado
        return {"action": "ERROR", "error": str(e)}

# === 5. EXECUÇÃO (MODO HÍBRIDO: LOCAL OU VIA N8N) ===
if __name__ == "__main__":
    
    # Este bloco lê o input que vem do n8n (sys.argv[1]) ou usa o JSON de teste
    # Verifica se foi passado argumento E se não é uma string vazia
    use_mock = True
    if len(sys.argv) > 1 and sys.argv[1].strip():
        try:
            # Tenta validar se é um JSON válido (evita erro com "undefined")
            json.loads(sys.argv[1])
            json_input = sys.argv[1]
            use_mock = False
        except ValueError:
            pass # Input inválido, usa mock
            
    if use_mock:
        # Dados de teste para quando rodar sem argumentos ou com string vazia
        json_input = json.dumps({
            "order_id": "FINAL-SUCCESS-ROI",
            "reason_code": "ITEM_NOT_RECEIVED",
            "financial_impact": 125.00,
            "timestamps": {
                "eta_max": "2025-11-20T20:00:00Z",
                "actual_arrival_at": "2025-11-20T19:55:00Z"
            },
            "delivery_evidence": {
                "gps_logs": [],
                "delivery_pin_validated": True,
                "pin_validated_at": "2025-11-20T19:56:00Z"
            },
            "chat_history": []
        })

    # Processa e imprime APENAS o JSON final no stdout
    result = process_refund_request(json_input)
    
    # Imprime o JSON final para o n8n capturar via stdout
    print(json.dumps(result, indent=2, ensure_ascii=False))