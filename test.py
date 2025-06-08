# test_models.py

import google.generativeai as genai

genai.configure(api_key="AIzaSyCMieSCjwQ5fYYC4Bdc2otZF__ro7fJVWM")

print("🔍 Listing available models...\n")

try:
    models = genai.list_models()
    for model in models:
        print("✅", model.name)
except Exception as e:
    print("❌ Failed to list models:")
    print(e)
