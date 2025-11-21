# Guia de Configuração do Telegram Bot

## Passo 1: Criar o Bot

1. Abra o Telegram
2. Procure por `@BotFather`
3. Envie `/newbot`
4. Escolha um nome: `iFood Refund Agent`
5. Escolha um username: `ifood_refund_bot` (ou outro disponível)
6. **Copie o TOKEN** que ele vai te dar

## Passo 2: Adicionar o TOKEN ao .env

Edite o arquivo `python_brain/.env` e adicione:

```
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
```

## Passo 3: Obter o CHAT_ID

1. Abra o Telegram e procure pelo seu bot (pelo username que você escolheu)
2. Envie uma mensagem qualquer para ele (ex: "Olá")
3. Rode o script:

```bash
cd python_brain
./venv/bin/python get_telegram_chat_id.py
```

4. Copie o CHAT_ID que aparecer
5. Adicione ao `.env`:

```
TELEGRAM_CHAT_ID=123456789
```

## Passo 4: Testar

Rode um caso de teste que gera contestação:

```bash
cd ..
./test_case.sh 08
```

Você deve receber uma notificação no Telegram! 🎉

## Estrutura Final do .env

```env
GEMINI_API_KEY=sua_chave_aqui
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
TELEGRAM_CHAT_ID=123456789
```

## Troubleshooting

### "Telegram não configurado"
- Verifique se o `.env` tem as duas variáveis
- Rode `source .env` ou reinicie o terminal

### "Erro 404 Not Found"
- O TOKEN está incorreto
- Crie um novo bot com @BotFather

### "Erro 400 Bad Request"
- O CHAT_ID está incorreto
- Rode novamente o `get_telegram_chat_id.py`
