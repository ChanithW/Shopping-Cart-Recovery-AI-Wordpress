import requests
import json
import os
from dotenv import load_dotenv
load_dotenv()

headers = {
    'Authorization': f'Bearer {os.getenv("API_TOKEN")}',
    'Content-Type': 'application/json'
}

# Test email generation
email_data = {
    "user_id": "test_user_123",
    "email": "test@example.com",
    "name": "John Doe",
    "items": [
        {
            "product_id": 1001,
            "name": "Wireless Headphones",
            "price": 99.99,
            "quantity": 1
        }
    ],
    "recommendations": [
        {
            "product_id": 2001,
            "name": "Bluetooth Speaker",
            "price": 79.99,
            "relevance_score": 0.85
        }
    ],
    "behavior": {
        "idle_time": 120,
        "pages_viewed": 5,
        "session_duration": 300
    },
    "persona": "loyal"
}

print('📧 Testing Email Generator...')
try:
    r = requests.post('http://localhost:8002/generate-email', headers=headers, json=email_data, timeout=30)
    print(f'Status: {r.status_code}')
    if r.status_code == 200:
        result = r.json()
        print('✅ SUCCESS!')
        print(f'Subject: {result.get("subject")}')
        print(f'Body length: {len(result.get("body", ""))} characters')
        print(f'Offers: {len(result.get("offers", []))}')
        print(f'First 200 chars of body: {result.get("body", "")[:200]}...')
        if result.get("offers"):
            print(f'First offer: {result["offers"][0]}')
    else:
        print(f'❌ Error: {r.text}')
except Exception as e:
    print(f'❌ Exception: {e}')