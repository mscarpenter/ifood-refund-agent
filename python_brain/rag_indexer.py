import os
import shutil
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Configurações
PDF_PATH = "docs/politica_reembolso_ifood.pdf" # Caminho do PDF (vamos criar essa pasta)
CHROMA_PATH = "chroma_db" # Onde o banco de dados vai ficar salvo

def main():
    # 1. Verificar se o PDF existe
    if not os.path.exists(PDF_PATH):
        print(f"❌ Erro: O arquivo {PDF_PATH} não foi encontrado.")
        return

    # 2. Carregar o PDF
    print("📄 Carregando PDF...")
    loader = PyPDFLoader(PDF_PATH)
    docs = loader.load()
    print(f"   - {len(docs)} páginas carregadas.")

    # 3. Quebrar o texto em pedaços menores (Chunks)
    print("✂️  Dividindo texto em chunks...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, # Tamanho de cada pedaço
        chunk_overlap=200 # Sobreposição para não perder contexto
    )
    chunks = text_splitter.split_documents(docs)
    print(f"   - {len(chunks)} chunks criados.")

    # 4. Criar Embeddings e Salvar no ChromaDB
    print("💾 Salvando no Banco Vetorial (Isso pode demorar um pouco)...")
    
    # Se o banco já existir, vamos limpar para recriar do zero (opcional, mas bom para testes)
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)

    # Usando o modelo de embeddings do Google
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

    # Criando o banco
    db = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_PATH
    )
    
    print(f"✅ Sucesso! Banco de dados criado em '{CHROMA_PATH}'.")

if __name__ == "__main__":
    main()
