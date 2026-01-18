from fastapi import APIRouter, Form, Response
from pydantic import BaseModel
from app.services.zendesk_service import zendesk_service
from app.services.ai_service import GeminiAgent

router = APIRouter()
agent = GeminiAgent()

# Memória simples em tempo de execução
conversation_history = {}

# --- ROTA 1: API SIMULAÇÃO / TESTE ---
class MessagePayload(BaseModel):
    user_id: str
    message: str

@router.post("/webhook/whatsapp")
async def receive_message(payload: MessagePayload):
    # Endpoint para testes locais (ex: scripts/simulation.py)
    return await process_message(payload.user_id, payload.message)

# --- ROTA 2: INTRAÇÃO REAL (TWILIO/WHATSAPP) ---
@router.post("/webhook/twilio")
async def receive_twilio_message(
    From: str = Form(...),  # O Twilio manda o número neste campo
    Body: str = Form(...)   # O Twilio manda a mensagem neste campo
):
    # Limpa o número (remove o prefixo "whatsapp:")
    user_phone = From.replace("whatsapp:", "")
    
    # print(f"📩 [Twilio] Recebido de {user_phone}: {Body}") # DEBUG
    
    # Processa a mensagem usando a mesma inteligência
    result = await process_message(user_phone, Body)
    
    # Vamos usar uma resposta TwiML básica XML para o Twilio entender que deve responder ao usuário
    xml_response = f"""<?xml version="1.0" encoding="UTF-8"?>
    <Response>
        <Message>{result['response']}</Message>
    </Response>"""
    
    return Response(content=xml_response, media_type="application/xml")

# --- LÓGICA COMPARTILHADA (CORE) ---
async def process_message(user_id: str, message: str):
    """Coração do Bot: Funciona tanto para simulação quanto para real."""
    
    # 1. Recupera/Inicia Histórico
    if user_id not in conversation_history:
        conversation_history[user_id] = []
    
    # Adiciona mensagem atual do usuário
    conversation_history[user_id].append(f"Usuário: {message}")
    
    # Limita histórico (últimas 10 interações)
    history_context = "\n".join(conversation_history[user_id][-10:])
    
    # 2. Busca Dados
    user = zendesk_service.get_user_by_phone(user_id)
    docs = zendesk_service.search_articles(message)
    
    # 3. Gerar Resposta via IA
    response_text = await agent.get_response(
        context=f"Perfil: {user['name']}\nHistórico Recente:\n{history_context}", 
        user_message=message,
        context_docs=docs
    )
    
    # Adiciona resposta do Bot ao histórico
    conversation_history[user_id].append(f"Bot: {response_text}")
    
    # 4. Verifica se precisa de ticket
    # Trigger 1: Palavras-chave do USUÁRIO (ex: "falar com atendente")
    user_intent_ticket = any(term in message.lower() for term in ["atendente", "cancelar", "humano", "suporte"])
    
    # Trigger 2: IA sugeriu ticket (ex: "Vou abrir um chamado")
    ai_intent_ticket = any(term in response_text.lower() for term in ["ticket", "encaminh", "abrir chamado"])

    if user_intent_ticket or ai_intent_ticket:
         print(f"⚡ IA ou Usuário indicou necessidade de ticket. Criando...")
         zendesk_service.create_ticket(
            user_id=user['id'], 
            subject=f"Solicitação via WhatsApp - {user['name']}", 
            description=f"Histórico da Conversa:\n{history_context}\n\nÚltima Resposta IA: {response_text}"
        )

    return {
        "status": "processed",
        "user": user['name'],
        "response": response_text
    }
