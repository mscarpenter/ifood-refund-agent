# 🤝 Guia de Contribuição

Obrigado por considerar contribuir para o iFood Refund Agent! 🎉

## 📋 Código de Conduta

Este projeto segue o [Contributor Covenant](https://www.contributor-covenant.org/). Ao participar, você concorda em manter um ambiente respeitoso e acolhedor.

## 🚀 Como Contribuir

### 1. Reportar Bugs

Encontrou um bug? Abra uma [issue](https://github.com/seu-usuario/ifood-refund-agent/issues) com:

- **Título claro**: Descreva o problema em uma frase
- **Passos para reproduzir**: Como chegou ao erro?
- **Comportamento esperado**: O que deveria acontecer?
- **Comportamento atual**: O que está acontecendo?
- **Ambiente**: SO, versão do Python, etc.
- **Logs**: Cole os logs relevantes

### 2. Sugerir Melhorias

Tem uma ideia? Abra uma issue com a tag `enhancement`:

- Descreva o problema que a melhoria resolve
- Explique a solução proposta
- Liste alternativas consideradas
- Adicione mockups se aplicável

### 3. Contribuir com Código

#### Setup do Ambiente

```bash
# 1. Fork o repositório
# 2. Clone seu fork
git clone https://github.com/SEU-USUARIO/ifood-refund-agent.git
cd ifood-refund-agent

# 3. Crie uma branch
git checkout -b feature/minha-feature

# 4. Configure o ambiente
cd python_brain
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 5. Rode os testes
pytest
```

#### Padrões de Código

- **Python**: Siga PEP 8
- **Docstrings**: Use formato Google
- **Type Hints**: Sempre que possível
- **Testes**: Cobertura mínima de 80%

Exemplo:

```python
def analyze_chat_context(chat_history: List[dict], order_details: dict) -> dict:
    """
    Analisa o histórico de chat para detectar nuances importantes.
    
    Args:
        chat_history: Lista de mensagens do chat
        order_details: Detalhes do pedido para contexto
    
    Returns:
        dict com findings, sentiment, e red_flags
        
    Raises:
        ValueError: Se chat_history estiver vazio
    """
    pass
```

#### Commit Messages

Use [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: adiciona análise de GPS
fix: corrige erro no parse de JSON
docs: atualiza README com exemplos
test: adiciona testes para chat analysis
refactor: simplifica lógica de decisão
```

#### Pull Request

1. Atualize o README se necessário
2. Adicione testes para novas funcionalidades
3. Garanta que todos os testes passam
4. Atualize a documentação
5. Descreva suas mudanças claramente

Template de PR:

```markdown
## Descrição
Breve descrição das mudanças

## Tipo de Mudança
- [ ] Bug fix
- [ ] Nova funcionalidade
- [ ] Breaking change
- [ ] Documentação

## Como Testar
1. Passo 1
2. Passo 2

## Checklist
- [ ] Código segue os padrões do projeto
- [ ] Testes adicionados/atualizados
- [ ] Documentação atualizada
- [ ] Todos os testes passam
```

## 🎯 Áreas para Contribuir

### Prioridade Alta
- [ ] Testes unitários completos
- [ ] Botões interativos no Telegram
- [ ] API REST para integração
- [ ] Documentação de API

### Prioridade Média
- [ ] Gráficos no dashboard
- [ ] Suporte a múltiplos idiomas
- [ ] Análise de vídeos
- [ ] Cache de embeddings

### Prioridade Baixa
- [ ] Interface web
- [ ] Mobile app
- [ ] Integração com outros marketplaces

## 📚 Recursos

- [Documentação LangChain](https://python.langchain.com/)
- [Gemini API Docs](https://ai.google.dev/docs)
- [n8n Documentation](https://docs.n8n.io/)

## 💬 Dúvidas?

- Abra uma [Discussion](https://github.com/seu-usuario/ifood-refund-agent/discussions)
- Entre no [Discord](#) (se houver)
- Envie um email para: seu-email@example.com

## 🙏 Agradecimentos

Todos os contribuidores serão adicionados ao README!

---

**Obrigado por contribuir! 🚀**
