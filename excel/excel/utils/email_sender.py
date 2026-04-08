import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv

load_dotenv() 

def enviar_email(arquivo, total=0):
    
    # CREDENCIAIS
    email_remetente = os.getenv("EMAIL_REMETENTE")
    senha = os.getenv("SUA_SENHA_APP")
    email_destino = os.getenv("EMAIL_DESTINO")

    # CABECALHO
    msg = EmailMessage()
    msg["Subject"] = "🚗 Oportunidades abaixo da FIPE encontradas!"
    msg["From"] = email_remetente
    msg["To"] = email_destino

    # BODY 
    msg.set_content(f"""
🚨 RELATÓRIO DE OPORTUNIDADES - CARROS 🚗

🔥 {total} oportunidades encontradas abaixo da FIPE!

Critérios utilizados:
✔ Preço abaixo da tabela FIPE
✔ Desconto mínimo de 10%
✔ Quilometragem até 80.000 km
✔ Ano a partir de 2018

📊 O arquivo em anexo contém os melhores carros encontrados hoje.

⏱ Este relatório é gerado automaticamente.

Fique atento — essas oportunidades somem rápido!

---
Sistema automático de monitoramento 🚀
""")

    # ANEXO DINÂMICO
    with open(arquivo, "rb") as f:
        msg.add_attachment(
            f.read(),
            maintype="application",
            subtype="octet-stream",
            filename=arquivo
        )

    # ENVIO
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(email_remetente, senha)
        smtp.send_message(msg)

    print("Email enviado! 📧")