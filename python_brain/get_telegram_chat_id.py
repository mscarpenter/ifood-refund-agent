#!/usr/bin/env python3
"""
Script para obter o CHAT_ID do Telegram.

Como usar:
1. Coloque seu BOT_TOKEN no .env
2. Envie uma mensagem qualquer para o bot no Telegram
3. Rode este script: python get_telegram_chat_id.py
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not BOT_TOKEN:
    print("❌ TELEGRAM_BOT_TOKEN não encontrado no .env")
    print("Adicione: TELEGRAM_BOT_TOKEN=seu_token_aqui")
    exit(1)

print(f"✅ TOKEN carregado: {BOT_TOKEN[:10]}... (tamanho: {len(BOT_TOKEN)})")


print(f"🔍 Buscando atualizações do bot...")
url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"

response = requests.get(url)

if response.status_code != 200:
    print(f"❌ Erro: {response.text}")
    exit(1)

data = response.json()

if not data.get("result"):
    print("⚠️ Nenhuma mensagem encontrada!")
    print("Envie uma mensagem para o bot no Telegram e rode este script novamente.")
    exit(0)

# Pega a última mensagem
last_message = data["result"][-1]
chat_id = last_message["message"]["chat"]["id"]
username = last_message["message"]["chat"].get("username", "N/A")
first_name = last_message["message"]["chat"].get("first_name", "N/A")

print("\n✅ CHAT_ID encontrado!")
print(f"📱 Nome: {first_name}")
print(f"👤 Username: @{username}")
print(f"🆔 CHAT_ID: {chat_id}")
print(f"\nAdicione ao .env:")
print(f"TELEGRAM_CHAT_ID={chat_id}")
