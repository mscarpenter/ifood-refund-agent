# 🎬 Roteiro para Vídeo de Demonstração
## iFood Refund Agent - Sistema Inteligente de Contestação

**Duração Total**: 2-3 minutos  
**Objetivo**: Demonstrar o valor e funcionamento do sistema

---

## 🎯 Estrutura do Vídeo

### INTRO (15 segundos)
**Visual**: Logo + Título animado

**Narração**:
> "Você sabia que restaurantes parceiros do iFood perdem até 30 minutos contestando cada reembolso manualmente? Apresento o iFood Refund Agent - um sistema de IA que automatiza todo esse processo."

---

### PARTE 1: O PROBLEMA (20 segundos)
**Visual**: Tela mostrando o Portal do Parceiro iFood

**Narração**:
> "O processo atual é burocrático: o restaurante precisa analisar chats, verificar fotos, entender regras complexas e preencher formulários. Tudo isso enquanto deveria estar focado em preparar comida."

**Mostrar**:
- Formulário de contestação manual
- Múltiplas abas abertas
- Relógio marcando tempo

---

### PARTE 2: A SOLUÇÃO (30 segundos)
**Visual**: Diagrama de arquitetura animado

**Narração**:
> "O iFood Refund Agent usa Inteligência Artificial Generativa para analisar automaticamente:
> - Validação de PIN de entrega
> - Análise de sentimento do chat
> - Verificação de fotos com visão computacional
> - E aplica as regras oficiais do iFood"

**Mostrar**:
- Fluxo: Webhook → Python → Gemini → Decisão
- Ícones de cada tecnologia

---

### PARTE 3: DEMONSTRAÇÃO AO VIVO (60 segundos)

#### Cena 1: Caso Simples - PIN Validado (20s)
**Visual**: Terminal + Telegram lado a lado

**Ação**:
```bash
./test_case.sh 08
```

**Narração**:
> "Vamos testar um caso real: cliente reclama que não recebeu o pedido, mas o PIN foi validado."

**Mostrar**:
1. Comando sendo executado
2. Log mostrando análise
3. Notificação chegando no Telegram
4. Defesa legal gerada

**Destacar**:
- "🤖 analisando Pedido..."
- "✅ PIN validado às 20:11"
- "⚡ CONTESTAR"
- Notificação no Telegram

---

#### Cena 2: Caso Complexo - Análise de Chat (20s)
**Visual**: JSON do caso + Resultado

**Ação**:
```bash
./test_case.sh 13
```

**Narração**:
> "Agora um caso mais complexo: sem PIN, mas o chat mostra que o cliente estava ausente."

**Mostrar**:
1. Chat history no JSON
2. "💬 Analisando 5 mensagens..."
3. "✅ 3 descobertas: cliente ausente"
4. Decisão: CONTESTAR

---

#### Cena 3: Dashboard Atualizado (20s)
**Visual**: Google Sheets com dashboard

**Narração**:
> "E tudo é registrado automaticamente em um dashboard com métricas em tempo real."

**Mostrar**:
1. Abrir Google Sheets
2. Aba "Dashboard"
3. Métricas atualizadas:
   - Total: 8 contestações
   - Valor recuperado: R$ 1.245,50
   - Top 5 maiores valores

---

### PARTE 4: IMPACTO (20 segundos)
**Visual**: Gráfico de comparação

**Narração**:
> "O resultado? 95% de redução no tempo de contestação. O que levava 30 minutos agora leva 30 segundos. E o restaurante pode focar no que realmente importa: servir bem seus clientes."

**Mostrar**:
- Antes: 30 minutos ⏰
- Depois: 30 segundos ⚡
- Gráfico de barras comparativo

---

### ENCERRAMENTO (15 segundos)
**Visual**: GitHub + Contato

**Narração**:
> "Projeto open-source, desenvolvido com Gemini 2.0, LangChain e n8n. Link na descrição. Obrigado!"

**Mostrar**:
- Logo do GitHub
- Badges (Python, Gemini, LangChain)
- QR Code para o repositório

---

## 🎥 Dicas de Gravação

### Setup Técnico
- **Resolução**: 1920x1080 (Full HD)
- **FPS**: 30 ou 60
- **Software**: OBS Studio (gratuito)
- **Edição**: DaVinci Resolve (gratuito)

### Visual
- **Terminal**: Use tema escuro com fonte grande (16-18pt)
- **Destaque**: Use `bat` ou `highlight` para colorir JSON
- **Zoom**: Dê zoom nos pontos importantes
- **Cursor**: Use ferramenta de destaque de cursor

### Áudio
- **Microfone**: Qualquer microfone USB decente
- **Ambiente**: Silencioso, sem eco
- **Música de Fundo**: Música corporativa suave (YouTube Audio Library)

---

## 📝 Script Completo (Texto)

```
[INTRO]
Você sabia que restaurantes parceiros do iFood perdem até 30 minutos contestando cada reembolso manualmente?

Apresento o iFood Refund Agent - um sistema de IA que automatiza todo esse processo.

[PROBLEMA]
O processo atual é burocrático: o restaurante precisa analisar chats, verificar fotos, entender regras complexas e preencher formulários.

Tudo isso enquanto deveria estar focado em preparar comida.

[SOLUÇÃO]
O iFood Refund Agent usa Inteligência Artificial Generativa para analisar automaticamente:
- Validação de PIN de entrega
- Análise de sentimento do chat
- Verificação de fotos com visão computacional
- E aplica as regras oficiais do iFood

[DEMO 1]
Vamos testar um caso real: cliente reclama que não recebeu o pedido, mas o PIN foi validado.

[Executar comando]

Veja: o sistema detectou automaticamente que o PIN foi validado às 20:11, gerou uma defesa legal profissional e enviou notificação no Telegram para aprovação humana.

[DEMO 2]
Agora um caso mais complexo: sem PIN, mas o chat mostra que o cliente estava ausente.

[Executar comando]

O sistema analisou 5 mensagens do chat, detectou que o cliente não respondeu 3 tentativas de contato, e decidiu contestar automaticamente.

[DEMO 3]
E tudo é registrado automaticamente em um dashboard com métricas em tempo real.

[Mostrar Google Sheets]

Total de 8 contestações processadas, R$ 1.245,50 recuperados, com ticket médio de R$ 155,69.

[IMPACTO]
O resultado? 95% de redução no tempo de contestação.

O que levava 30 minutos agora leva 30 segundos.

E o restaurante pode focar no que realmente importa: servir bem seus clientes.

[ENCERRAMENTO]
Projeto open-source, desenvolvido com Gemini 2.0, LangChain e n8n.

Link na descrição. Obrigado!
```

---

## 🎬 Checklist de Produção

### Pré-Produção
- [ ] Testar todos os casos antes de gravar
- [ ] Limpar terminal (histórico)
- [ ] Preparar Google Sheets com dados de exemplo
- [ ] Configurar OBS com cenas
- [ ] Testar áudio

### Gravação
- [ ] Gravar intro
- [ ] Gravar demonstração (múltiplas takes se necessário)
- [ ] Gravar encerramento
- [ ] Gravar B-roll (telas extras)

### Pós-Produção
- [ ] Editar no DaVinci Resolve
- [ ] Adicionar música de fundo
- [ ] Adicionar legendas (opcional)
- [ ] Adicionar zoom nos pontos importantes
- [ ] Exportar em Full HD

### Publicação
- [ ] Upload no YouTube
- [ ] Título: "iFood Refund Agent - IA para Automação de Contestações"
- [ ] Descrição com link do GitHub
- [ ] Tags: IA, Gemini, LangChain, iFood, Automação
- [ ] Thumbnail atrativo

---

## 🎨 Sugestões de Thumbnail

**Elementos**:
- Logo do iFood
- Ícone de robô/IA
- Texto: "95% MAIS RÁPIDO"
- Cores: Verde (iFood) + Azul (Tech)
- Expressão: Profissional mas impactante
