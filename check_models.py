import os
import sys
try:
    import truststore
    truststore.inject_into_ssl()
except Exception:
    pass

import requests
from dotenv import load_dotenv

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

load_dotenv()

api_key = os.getenv("MISTRAL_API_KEY")

if not api_key:
    print("[ERROR] MISTRAL_API_KEY not found in environment or .env file.")
    sys.exit(1)

print(f"[INFO] Testing Mistral API with key: {api_key[:6]}...{api_key[-4:] if len(api_key) > 10 else ''}")

try:
    response = requests.get(
        "https://api.mistral.ai/v1/models",
        headers={"Authorization": f"Bearer {api_key}"},
        timeout=10
    )
    if response.status_code == 200:
        data = response.json()
        models = [m["id"] for m in data.get("data", [])]
        print(f"\n[SUCCESS] Successfully connected to Mistral API! Found {len(models)} models.")
        print("Available models:")
        for m in sorted(models):
            print(f"  - {m}")
            
        recommended = [
            "mistral-small-latest",
            "mistral-large-latest",
            "open-mistral-7b",
            "ministral-8b-latest",
            "ministral-3b-latest",
            "open-mixtral-8x7b"
        ]
        
        test_model = None
        for r in recommended:
            if r in models:
                test_model = r
                break
        if not test_model and models:
            test_model = models[0]
            
        if test_model:
            print(f"\n[TEST] Testing completion with model: '{test_model}'...")
            chat_resp = requests.post(
                "https://api.mistral.ai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": test_model,
                    "messages": [{"role": "user", "content": "Hello, respond with 'Mistral is working!'"}]
                },
                timeout=10
            )
            if chat_resp.status_code == 200:
                content = chat_resp.json()["choices"][0]["message"]["content"]
                print(f"[SUCCESS] Model '{test_model}' response: {content.strip()}")
            else:
                print(f"[ERROR] Error testing model '{test_model}': {chat_resp.status_code} - {chat_resp.text}")
    else:
        print(f"[ERROR] Failed to fetch models: {response.status_code} - {response.text}")
except Exception as e:
    print(f"[ERROR] Exception occurred: {str(e)}")
