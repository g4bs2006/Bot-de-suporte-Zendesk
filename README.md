# Bot de Suporte Inteligente com IA e Integração Zendesk

Este projeto consiste em uma solução completa de automação de atendimento (Nível 1), desenvolvida para atuar como um primeiro ponto de contato eficiente entre empresas e clientes via WhatsApp. A arquitetura foi projetada para simular um ambiente corporativo real, integrando processamento de linguagem natural (LLMs), bases de conhecimento dinâmicas e sistemas de gestão de tickets.

## Visão Geral e Arquitetura

O núcleo do sistema é construído em **Python** utilizando o framework **FastAPI**, escolhido pela sua alta performance em microsserviços assíncronos. A inteligência do bot é provida pelo **Google Gemini (versão 2.5 Flash Lite)**, que opera em conjunto com uma estratégia de **RAG (Retrieval Augmented Generation)**. Isso permite que a IA leia e interprete um manual técnico proprietário (`faq.txt`) antes de responder ao usuário, garantindo respostas fundamentadas e livres de alucinações comuns em modelos genéricos.

Para a comunicação externa, o sistema utiliza a API do **Twilio** para conectar-se ao WhatsApp. A orquestração do atendimento segue um fluxo híbrido robusto:
1.  O bot tenta resolver a dúvida do cliente automaticamente usando a base de conhecimento.
2.  Caso identifique complexidade ou solicitação explícita, o sistema inicia o protocolo de transbordo.
3.  O transbordo tenta criar um ticket na plataforma **Zendesk**.
4.  Como mecanismo de segurança (*fallback*), caso a API do Zendesk esteja indisponível, o sistema dispara automaticamente um e-mail formatado em HTML para a equipe de suporte, assegurando que nenhuma solicitação seja perdida.

## Tecnologias Utilizadas

O projeto foi construído sobre uma stack moderna e escalável:
* **Linguagem:** Python 3.9+
* **Backend:** FastAPI & Uvicorn
* **Inteligência Artificial:** Google Gemini AI (via `google-generativeai`)
* **Integração de Mensageria:** Twilio (WhatsApp API)
* **Gestão de Chamados:** Zendesk API & SMTP (Gmail/Email Fallback)

## Guia de Instalação e Execução

Para executar este projeto localmente, é necessário clonar o repositório e configurar o ambiente virtual. O sistema depende de variáveis de ambiente para autenticação segura, portanto, é imprescindível configurar o arquivo `.env` com suas chaves de API (Google AI Studio e Twilio).

Após a configuração das credenciais, a instalação das dependências é feita via `pip install -r requirements.txt`. O servidor de desenvolvimento pode ser iniciado com o comando `uvicorn main:app --reload`, que expõe a aplicação na porta 8000 localmente.

### Modos de Operação

O sistema oferece dois modos de operação distintos para facilitar o desenvolvimento e testes:

1.  **Modo Simulação (Terminal):** Executando o script `scripts/simulation.py`, é possível interagir com a lógica do bot diretamente pelo terminal, sem custos de API do WhatsApp ou necessidade de conexão de rede externa. Ideal para validar o RAG e o fluxo de tickets.
2.  **Modo Produção (WhatsApp Real):** Utilizando um túnel reverso (como Ngrok ou Localhost.run), o servidor local é exposto para a internet, permitindo que o webhook do Twilio envie mensagens reais do WhatsApp para a aplicação processar.

## Personalização da Base de Conhecimento

A inteligência do bot não é estática. Toda a base de conhecimento reside no arquivo `data/knowledge_base/faq.txt`. Para adaptar o bot a um novo cenário de negócio (ex: clínica médica, e-commerce, etc.), basta substituir o texto deste arquivo. O sistema carrega as novas regras automaticamente na próxima reinicialização, sem necessidade de alterar o código-fonte.

---
**Desenvolvido por Gabriel Rodrigues**
*Engenharia de Software e Automação com IA*
