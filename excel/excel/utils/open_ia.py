import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

# OPENIA
def extrair_com_ia(titulo):
    try:
        prompt = f"""
Extraia a marca e o modelo de um carro.

Titulo: "{titulo}"

Responda SOMENTE em JSON:
{{
  "marca": "...",
  "modelo": "..."
}}
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        texto = response.choices[0].message.content

        import json
        data = json.loads(texto)

        return data.get("marca"), data.get("modelo")

    except:
        return None, None