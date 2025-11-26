# Guia de Uso

Este documento fornece instruções detalhadas sobre como operar e configurar o iFood Refund Agent.

## 🚀 Executando Localmente

### Pré-requisitos
Certifique-se de ter o ambiente virtual ativado e as dependências instaladas (veja `README.md`).

### 1. Indexação da Base de Conhecimento
Antes de rodar qualquer análise, é necessário indexar as políticas do iFood no ChromaDB.

```bash
cd python_brain
python indexer.py
```
Isso lerá o arquivo `politica_ifood_reembolso.txt` e criará o banco vetorial em `chroma_db_ifood/`.

### 2. Executando um Caso de Teste
Você pode testar o sistema com os arquivos JSON na pasta `test_cases/`.

```bash
# Sintaxe: ./test_case.sh <numero_do_caso>
./test_case.sh 08
```
Isso executará o script `reimbursement_brain.py` com o JSON correspondente.

### 3. Executando em Lote
Para validar todos os cenários de uma vez:

```bash
./test_batch.sh
```

## 🤖 Integração com n8n

O n8n atua como o orquestrador, recebendo webhooks (simulando o iFood) e chamando o script Python.

1. **Importe o Workflow**: Use o arquivo `n8n_workflow.json` (se disponível) ou crie um workflow com um nó "Webhook" e um nó "Execute Command".
2. **Configure o Webhook**: Defina o método como POST e o caminho como `/ifood-refund`.
3. **Nó Execute Command**:
   - Comando: `/path/to/venv/bin/python /path/to/python_brain/reimbursement_brain.py`
   - Argumentos: Passe o JSON recebido pelo webhook como argumento (ou salve em arquivo temporário).

## 📊 Dashboard

O dashboard no Google Sheets é atualizado automaticamente a cada execução bem-sucedida.

- **Aba 'Dados'**: Contém o registro bruto de todas as contestações.
- **Aba 'Dashboard'**: Contém métricas e gráficos.

Para visualizar o dashboard em tempo real:
 
```bash
# A partir da raiz do projeto
python dashboard/server.py
```
 
Acesse `http://127.0.0.1:5000` no seu navegador.

## 📱 Telegram

O bot do Telegram enviará mensagens para o `CHAT_ID` configurado no `.env`.
- As mensagens contêm o resumo do pedido, a decisão da IA e a justificativa.
- Em versões futuras, haverá botões para aprovar/rejeitar a contestação diretamente pelo chat.
