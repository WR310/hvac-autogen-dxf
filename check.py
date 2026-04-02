import os
import google.generativeai as genai

current_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(current_dir, ".env")

api_key = None
with open(env_path, "r") as f:
    for line in f:
        if line.startswith("GEMINI_API_KEY="):
            api_key = line.split("=", 1)[1].strip()
            break

genai.configure(api_key=api_key)

print("Доступные модели:")
for m in genai.list_models():
    if "generateContent" in m.supported_generation_methods:
        print(m.name)
