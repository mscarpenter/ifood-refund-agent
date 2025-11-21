from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
import os

load_dotenv()

# Caminho do documento que criamos
POLICY_PATH = "politica_ifood_reembolso.txt"
# Nome da pasta onde o ChromaDB irá salvar os vetores
VECTOR_DB_DIR = "chroma_db_ifood" 

def ingest_data():
    """Carrega o documento e o indexa no ChromaDB."""
    print("--- 1. Carregando e Separando Documento (Chunking) ---")
    
    # Carrega o documento de texto
    loader = TextLoader(POLICY_PATH)
    documents = loader.load()
    
    # Simplesmente usamos o documento inteiro para este teste, 
    # mas em produção usaríamos um TextSplitter.
    docs = documents

    # O embedding do Google é necessário para transformar texto em vetores
    if not os.getenv("GOOGLE_API_KEY"):
         raise ValueError("GOOGLE_API_KEY não encontrada no .env. RAG precisa dela.")
         
    embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
    
    print("--- 2. Criando o Banco Vetorial (ChromaDB) ---")
    
    # Cria a instância do ChromaDB e popula com os documentos e embeddings
    db = Chroma.from_documents(
        docs, 
        embeddings, 
        persist_directory=VECTOR_DB_DIR
    )
    db.persist()
    print(f"✅ Sucesso! {len(docs)} documento(s) indexado(s) em {VECTOR_DB_DIR}")

if __name__ == "__main__":
    ingest_data()