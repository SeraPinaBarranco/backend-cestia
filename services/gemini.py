from pathlib import Path
from groq import Groq
import os, json, base64
from dotenv import load_dotenv
from models.ticket import TicketResponse

load_dotenv(Path(__file__).parent.parent / ".env")
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

PROMPT = """
Eres un experto en tickets de supermercado españoles.
Analiza la imagen y devuelve ÚNICAMENTE un JSON con esta estructura exacta, sin markdown ni explicaciones:

{
  "supermercado": "nombre o null",
  "fecha": "DD/MM/YYYY o null",
  "productos": [
    {
      "nombre": "nombre del producto",
      "cantidad": número o null,
      "unidad": "kg/ud/l o null",
      "precio_unitario": número o null,
      "precio_total": número
    }
  ],
  "subtotal": número o null,
  "iva": número o null,
  "total": número o null
}
"""

async def analyze_ticket(image_bytes: bytes) -> TicketResponse:
    b64 = base64.b64encode(image_bytes).decode("utf-8")

    response = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[{
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{b64}"}
                },
                {
                    "type": "text",
                    "text": PROMPT
                }
            ]
        }],
        max_tokens=1000
    )

    text = response.choices[0].message.content.strip()

    # Limpiar si el modelo añade bloques markdown
    if "```" in text:
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]

    data = json.loads(text.strip())
    return TicketResponse(**data)