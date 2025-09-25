import requests
import json
import os
from dotenv import load_dotenv
load_dotenv()

headers = {
    'Authorization': f'Bearer {os.getenv("API_TOKEN")}',
    'Content-Type': 'application/json'
}

data = {
    'user_id': 'test',
    'email': 'test@example.com',
    'items': [{
        'product_id': 1001,
        'name': 'Test Product',
        'price': 99.99,
        'quantity': 1
    }],
    'behavior': {
        'idle_time': 120,
        'pages_viewed': 5,
        'session_duration': 300
    },
    'timestamp': 1727257200.0
}

print('🔍 Testing Abandonment Detector...')
try:
    r = requests.post('http://localhost:8001/detect-abandonment', headers=headers, json=data, timeout=25)
    print(f'Status: {r.status_code}')
    if r.status_code == 200:
        result = r.json()
        print('✅ SUCCESS!')
        print(f'Abandoned: {result.get("abandoned")}')
        print(f'Full Result: {json.dumps(result, indent=2)}')
    else:
        print(f'❌ Error: {r.text}')
except Exception as e:
    print(f'❌ Exception: {e}')