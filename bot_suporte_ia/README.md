# Bot Suporte IA + Zendesk

Este projeto é um bot de suporte inteligente integrado ao Zendesk e WhatsApp (via Twilio), desenvolvido com FastAPI e Google Gemini.

## Funcionalidades

- **Integração WhatsApp**: Recebe mensagens via webhook (Twilio ou simulador).
- **Inteligência Artificial**: Utiliza Google Gemini para gerar respostas contextuais baseadas em documentos de suporte.
- **Integração Zendesk**: Cria tickets automaticamente e consulta usuários.
- **Simulação Local**: Script para testar o fluxo de conversas no terminal.

## Estrutura do Projeto

```
bot_suporte_ia/
├── app/
│   ├── api/            # Rotas da API (Webhooks)
│   ├── core/           # Configurações
│   └── services/       # Lógica de negócios (IA, Zendesk)
├── scripts/            # Scripts utilitários e de teste
├── .env                # Variáveis de ambiente (não versionado)
├── main.py             # Ponto de entrada da aplicação
└── requirements.txt    # Dependências do projeto
```

## Como Executar

1. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure o ambiente:**
   Crie um arquivo `.env` na raiz baseado nas configurações necessárias (Google API Key, Zendesk Credentials, etc.).

3. **Inicie o servidor:**
   ```bash
   uvicorn main:app --reload
   ```

4. **Simule uma conversa (Opcional):**
   Em outro terminal, execute:
   ```bash
   python scripts/simulation.py
   ```
