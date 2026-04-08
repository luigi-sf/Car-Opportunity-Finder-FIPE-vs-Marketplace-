import schedule
import time
import subprocess
from excel.utils.analisar_excel import analisar
from excel.utils.email_sender import enviar_email


def rodar_scrapy():
    print("🕷️ Rodando scraping...")
    subprocess.Popen(["poetry", "run", "scrapy", "crawl", "excel"])


def rodar_analise():
    print("📊 Rodando análise...")
    arquivo, total = analisar()

    if arquivo:
        enviar_email(arquivo, total)
        print(f"📩 Email enviado com {total} oportunidades")
    else:
        print("⚠️ Nenhuma oportunidade")


# EXECUÇÃO IMEDIATA
print("🚀 Rodando execução inicial...")
rodar_scrapy()
time.sleep(10)  # espera scraping começar
rodar_analise()


# AGENDAMENTO

# scraping 1x por dia
schedule.every().day.at("09:00").do(rodar_scrapy)

# análise a cada 1h
schedule.every(1).hours.do(rodar_analise)


print("⏰ Automação iniciada...")

while True:
    schedule.run_pending()
    time.sleep(5)