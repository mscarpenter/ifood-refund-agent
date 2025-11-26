import os
import sys
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from dotenv import load_dotenv

# Força o output a aparecer imediatamente (sem buffer)
sys.stdout.reconfigure(encoding='utf-8')

print("🚀 Iniciando sistema de teste...", flush=True)

try:
    load_dotenv()
    
    if not os.getenv("GOOGLE_API_KEY"):
        print("❌ ERRO: GOOGLE_API_KEY não encontrada no .env", flush=True)
        sys.exit(1)

    print("🔌 Conectando ao ChromaDB...", flush=True)
    embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
    rag_db = Chroma(persist_directory="chroma_db_ifood", embedding_function=embeddings)
    
    print("🧠 Carregando LLM (Gemini 2.0 Flash)...", flush=True)
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0)

    retriever = rag_db.as_retriever()
    rag_chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)

    # A Pergunta Exata do Cenário
    query = "O cliente quer reembolso, mas o pedido já saiu para entrega. Ainda é permitido? Explique as regras de tempo e tolerância."

    print(f"\n❓ PERGUNTA ENVIADA AO AGENTE:\n'{query}'\n", flush=True)
    print("⏳ Processando resposta (consultando base de conhecimento)...", flush=True)
    
    response = rag_chain.invoke(query)
    
    print("\n" + "="*50)
    print("🤖 RESPOSTA REAL DO AGENTE:")
    print("="*50)
    print(response['result'])
    print("="*50 + "\n")

except Exception as e:
    print(f"\n❌ ERRO FATAL: {str(e)}", flush=True)
    import traceback
    traceback.print_exc()
