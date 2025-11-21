# Perguntas Frequentes (FAQ)

## Configuração

### Como obtenho minha API Key do Gemini?
Acesse o [Google AI Studio](https://aistudio.google.com/), crie um novo projeto e gere uma API Key.

### Como descubro meu Chat ID do Telegram?
1. Inicie uma conversa com o seu bot.
2. Envie qualquer mensagem.
3. Acesse `https://api.telegram.org/bot<SEU_TOKEN>/getUpdates`.
4. Procure pelo campo `chat.id` no JSON de resposta.
Alternativamente, use o script auxiliar:
```bash
python python_brain/get_telegram_chat_id.py
```

### Onde coloco o arquivo `client_secret.json`?
O arquivo de credenciais da Service Account do Google deve ser colocado dentro da pasta `python_brain/`. Certifique-se de que ele tenha exatamente esse nome.

## Erros Comuns

### `ModuleNotFoundError: No module named ...`
Você provavelmente não ativou o ambiente virtual ou não instalou as dependências.
Execute:
```bash
source venv/bin/activate
pip install -r python_brain/requirements.txt
```

### `ChromaDB Error` ou `Index not found`
Você precisa rodar o indexador antes de fazer consultas.
Execute:
```bash
python python_brain/indexer.py
```

### O Dashboard não atualiza
Verifique se você compartilhou a planilha do Google Sheets com o e-mail da Service Account (encontrado no `client_secret.json`).

## Funcionamento

### O sistema contesta automaticamente no iFood?
Atualmente, o sistema gera a defesa legal e notifica. A integração direta com a API de contestação do iFood (escrita) seria o próximo passo, mas requer credenciais de parceiro oficiais.

### Posso adicionar novas regras?
Sim! As regras são baseadas principalmente no prompt do sistema em `reimbursement_brain.py` e nos documentos indexados no RAG. Adicione novas políticas ao arquivo de texto e re-indexe, ou ajuste o prompt.
