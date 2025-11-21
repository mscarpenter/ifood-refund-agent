#!/usr/bin/env python3
from dotenv import load_dotenv
import os

load_dotenv()

token = os.getenv('TELEGRAM_BOT_TOKEN')
print(f"TOKEN carregado: {token}")
print(f"Tamanho: {len(token) if token else 0}")
print(f"Tem aspas? {token[0] if token else 'N/A'}")
