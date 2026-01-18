import google.generativeai as genai
from app.core.config import settings

class GeminiAgent:
    def __init__(self):
        genai.configure(api_key=settings.GOOGLE_API_KEY)
        
        # Modelo Configurado: Gemini 2.5 Flash Lite
        self.model = genai.GenerativeModel('gemini-2.5-flash-lite')

    async def get_response(self, context, user_message, context_docs=None):
        docs_text = "\n".join(context_docs) if context_docs else "Nenhum documento relevante encontrado."
        
        prompt = f"""
        Você é um assistente de suporte inteligente.
        Documentos: {docs_text}
        Histórico: {context}
        Usuário: {user_message}
        """
        
        try:
            # Geração de resposta assíncrona
            response = await self.model.generate_content_async(prompt)
            return response.text
        except Exception as e:
            return f"Erro na IA: {str(e)}"
