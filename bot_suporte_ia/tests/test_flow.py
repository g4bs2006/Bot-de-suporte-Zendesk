import sys
import os
import asyncio
from unittest.mock import MagicMock, patch, AsyncMock

# Adiciona o diretório raiz ao PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Mock das variáveis de ambiente
os.environ["GOOGLE_API_KEY"] = "fake_key"
os.environ["ZENDESK_EMAIL"] = "test@example.com"
os.environ["ZENDESK_TOKEN"] = "fake_token"

async def run_test():
    print("--- Iniciando Teste do Fluxo do Bot ---")
    
    # Patch na classe GeminiAgent para isolar a IA
    with patch('app.services.ai_service.GeminiAgent') as MockAgent:
        # Configura o mock da instância
        instance = MockAgent.return_value
        instance.get_response = AsyncMock(return_value="Resposta simulada do Gemini: Tente reiniciar.")
        
        # Importa o webhook DENTRO do patch para garantir que ele use o mock
        # Nota: Como o webhook instancia o agent no nível do módulo, 
        # precisamos garantir que o import aconteça agora ou recarregar o módulo.
        # Para simplificar, vamos assumir que não foi importado ainda ou usar sys.modules clean
        if 'app.api.webhook' in sys.modules:
            del sys.modules['app.api.webhook']
            
        from app.api.webhook import receive_message, MessagePayload, agent
        
        # Sobrescreve o agent instanciado globalmente no webhook (caso o patch na classe não pegue a tempo)
        import app.api.webhook
        app.api.webhook.agent = instance

        payload = MessagePayload(
            user_id="11999999999",
            message="Minha internet não funciona"
        )
        
        print(f"Enviando mensagem: {payload.message}")
        
        response = await receive_message(payload)
        
        print("\n--- Resultado ---")
        print(f"Status: {response['status']}")
        print(f"Usuário Identificado: {response['user']}")
        print(f"Resposta Gerada: {response['response']}")
        
        assert response['status'] == "processed"
        assert response['user'] == "Gabriel (Admin)"
        assert "Gemini" in response['response']
        print("\n✅ Teste Concluído com Sucesso!")

if __name__ == "__main__":
    # Mock do google.generativeai para evitar erros no import original do ai_service
    sys.modules["google.generativeai"] = MagicMock()
    asyncio.run(run_test())
