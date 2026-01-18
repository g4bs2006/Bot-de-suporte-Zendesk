import google.generativeai as genai
import os
import sys
from dotenv import load_dotenv
from pathlib import Path

# Adiciona o diretório raiz ao path para garantir importações se necessário
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

# Carrega o .env da raiz do projeto
env_path = PROJECT_ROOT / ".env"
load_dotenv(env_path)

api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print(f"❌ Erro: Chave de API não encontrada em {env_path}")
else:
    print(f"🔑 Chave encontrada: {api_key[:5]}...")
    genai.configure(api_key=api_key)

    print("\n🔍 Listando modelos disponíveis:")
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f" - {m.name}")
    except Exception as e:
        print(f"❌ Erro ao listar modelos: {e}")