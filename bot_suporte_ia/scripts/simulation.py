import requests
import time
import sys

# Configuração da API local
API_URL = "http://localhost:8000/webhook/whatsapp" 

# Cores para o terminal 
class Colors:
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def typing_effect(text):
    """Simula o efeito de digitação"""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.01) 
    print()

def main():
    print(f"{Colors.BOLD}--- SIMULADOR WHATSAPP CORPORATIVO ---{Colors.RESET}")
    print("Conectando ao servidor em localhost:8000...")
    
    # Identificação simulada do usuário
    user_phone = "556299999999"
    
    print(f"\n{Colors.YELLOW}Bot:{Colors.RESET} Olá! Sou o assistente virtual. Como posso ajudar hoje?")

    while True:
        try:
            # Input do usuário
            user_msg = input(f"\n{Colors.BLUE}Você:{Colors.RESET} ")
            
            if user_msg.lower() in ['sair', 'exit', 'tchau']:
                print(f"{Colors.YELLOW}Bot:{Colors.RESET} Até logo! 👋")
                break

            # Envia para a sua API (FastAPI)
            payload = {
                "user_id": user_phone,
                "message": user_msg
            }
            
            # Mostra status de "Enviando..."
            print(f"{Colors.RESET}(Enviando...)", end="\r")
            
            start_time = time.time()
            response = requests.post(API_URL, json=payload)
            elapsed = time.time() - start_time

            if response.status_code == 200:
                data = response.json()
                bot_response = data.get("response", "Erro: Sem resposta")
                
                # Limpa a linha de "Enviando..."
                print(" " * 20, end="\r")
                
                print(f"{Colors.YELLOW}Bot:{Colors.RESET} ", end="")
                typing_effect(bot_response)
                
                # Debug de performance (pra você avaliar latência)
                print(f"{Colors.RESET}⏱️  (Tempo de resposta: {elapsed:.2f}s)")
                
                if "humano" in bot_response.lower():
                    print(f"\n{Colors.BOLD}[SISTEMA] 🔔 TICKET ABERTO NO ZENDESK!{Colors.RESET}")
            else:
                print(f"\n❌ Erro na API: {response.status_code} - {response.text}")

        except requests.exceptions.ConnectionError:
            print(f"\n❌ {Colors.BOLD}ERRO CRÍTICO:{Colors.RESET} Não consegui conectar no localhost:8000.")
            print("💡 DICA: Você rodou o comando 'uvicorn main:app --reload' em outro terminal?")
            break
        except KeyboardInterrupt:
            print("\nEncerrando simulação.")
            break

if __name__ == "__main__":
    main()
