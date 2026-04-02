import os
import json
import pdfplumber
from google import genai
from google.genai import types

current_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(current_dir, ".env")

# Читаем ключ напрямую из файла, игнорируя кэш Windows
api_key = None
with open(env_path, "r") as f:
    for line in f:
        if line.startswith("GEMINI_API_KEY="):
            api_key = line.split("=", 1)[1].strip()
            break

if not api_key:
    raise ValueError("Ключ не найден в файле .env!")

client = genai.Client(api_key=api_key)


def extract_data(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"

    prompt = """
    Ты инженер-проектировщик. Найди в тексте спецификации элементы вентиляционных систем.
    КРИТИЧЕСКИЕ ПРАВИЛА:
    1. Каждая система (П-1, В-1, ВЕ-1) должна быть отдельным объектом в массиве systems.
    2. Если в тексте указана группа оборудования (например, "ВЕ системы 38 шт" зонтов), ты обязан разбить её математически на 38 отдельных систем: ВЕ-1, ВЕ-2, ВЕ-3 и так далее до ВЕ-38. Внутри каждой должен лежать 1 зонт (quantity: 1).
    3. Строго игнорируй раздел "Общее оборудование" и любые решетки, диффузоры или маты, если в тексте прямо не написано, к какой именно системе (например, к П-1) они относятся. Не угадывай аэродинамику.
    Верни результат строго в JSON формате:
    {"systems": [{"name": "П-1", "equipment": [{"title": "Вентилятор...", "quantity": 1}]}]}
    Текст:
    """ + text

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json", temperature=0.1
        ),
    )

    return json.loads(response.text)
