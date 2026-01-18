import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
from app.core.config import settings

class ZendeskService:
    def __init__(self):
        self.base_url = settings.ZENDESK_API_URL
        # Cache do FAQ na memória RAM (Otimização que discutimos)
        self.faq_cache = self._load_faq_from_disk()
        
        # Configuração de E-mail para Fallback
        self.email_sender = os.getenv("EMAIL_SENDER")
        self.email_password = os.getenv("EMAIL_PASSWORD")
        self.email_receiver = os.getenv("EMAIL_RECEIVER")

    def _load_faq_from_disk(self):
        """Carrega o FAQ do disco apenas uma vez na inicialização."""
        try:
            current_dir = Path(__file__).parent
            project_root = current_dir.parent.parent
            file_path = project_root / "data" / "knowledge_base" / "faq.txt"
            
            if not file_path.exists():
                return "Erro: Arquivo FAQ não encontrado."
                
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            return f"Erro ao carregar FAQ: {e}"

    def get_user_by_phone(self, phone: str):
        # Simulação de base de clientes
        return {
            "id": 12345,
            "name": "Gabriel (Admin)", 
            "phone": phone,
            "email": self.email_receiver or "admin@exemplo.com"
        }

    def search_articles(self, query: str):
        return [self.faq_cache]

    def create_ticket(self, user_id, subject, description):
        """
        Tenta criar ticket no Zendesk. Se falhar ou não configurado, envia E-mail.
        """
        ticket_data = {
            "ticket": {
                "subject": subject,
                "comment": {"body": description},
                "priority": "normal"
            }
        }

        # 1. Tentativa de Integração Real (Zendesk)
        # 1. Tentativa de Integração Real (Zendesk)
        # if settings.ZENDESK_TOKEN and "fake" not in settings.ZENDESK_TOKEN:
        #     # Aqui entraria o requests.post real
        #     # response = requests.post(...)
        #     print(f"[Zendesk Real] 🎫 Tentando criar ticket via API...")
        #     pass 
        
        print("[DEBUG] Forçando fallback de e-mail (Zendesk desabilitado temporariamente)")
        
        # 2. Fallback: Simulação via E-mail
        print(f"[Sistema] 📧 Disparando notificação por e-mail para a equipe...")
        self._send_email_notification(subject, description)
        
        return {"id": 999, "status": "open", "via": "email_fallback"}

    def _send_email_notification(self, subject, body):
        """Envia um e-mail formatado simulando um ticket aberto."""
        if not self.email_sender or not self.email_password:
            print("⚠️ AVISO: Credenciais de e-mail não configuradas no .env")
            return

        try:
            msg = MIMEMultipart()
            msg['From'] = self.email_sender
            msg['To'] = self.email_receiver
            msg['Subject'] = f"[NOVO TICKET] {subject}"

            html_body = f"""
            <html>
              <body>
                <h2 style="color: #2E86C1;">🎫 Novo Chamado de Suporte</h2>
                <p><strong>Origem:</strong> WhatsApp Bot (IA)</p>
                <hr>
                <h3>Descrição do Problema:</h3>
                <pre style="background-color: #f4f4f4; padding: 10px; border-radius: 5px;">{body}</pre>
                <hr>
                <p style="font-size: 0.8em; color: #666;">Este é um e-mail automático do seu sistema de portfólio.</p>
              </body>
            </html>
            """
            
            msg.attach(MIMEText(html_body, 'html'))

            # Conexão SMTP com Gmail (Porta 465 SSL - Mais segura e evita bloqueios 10060)
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(self.email_sender, self.email_password)
                text = msg.as_string()
                server.sendmail(self.email_sender, self.email_receiver, text)
            
            print(f"✅ E-mail enviado com sucesso para {self.email_receiver}")
            
        except smtplib.SMTPAuthenticationError:
            print("❌ Erro de Autenticação: Verifique se EMAIL_PASSWORD é uma 'Senha de App' válida.")
        except Exception as e:
            print(f"❌ Erro ao enviar e-mail: {str(e)}")

zendesk_service = ZendeskService()
