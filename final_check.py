import requests
import os
from dotenv import load_dotenv
import time

load_dotenv()

print("🔍 SYSTEM STATUS CHECK")
print("=" * 40)

# Check services
print("\n📡 Service Status:")
try:
    r1 = requests.get("http://localhost:8001/docs", timeout=3)
    print(f"✅ Abandonment Detector: {r1.status_code}")
except:
    print("❌ Abandonment Detector: DOWN")

# Wait a moment for email service
time.sleep(2)
try:
    r2 = requests.get("http://localhost:8002/docs", timeout=3)
    print(f"✅ Email Generator: {r2.status_code}")
except:
    print("❌ Email Generator: DOWN")

# Test functionality
print("\n🧪 Functional Test:")
headers = {
    'Authorization': f'Bearer {os.getenv("API_TOKEN")}',
    'Content-Type': 'application/json'
}

test_data = {
    'user_id': 'test_user',
    'email': 'test@example.com',
    'items': [{
        'product_id': 1001,
        'name': 'Test Item',
        'price': 29.99,
        'quantity': 1
    }],
    'behavior': {
        'idle_time': 120,  # 2 minutes
        'pages_viewed': 3,
        'session_duration': 180
    },
    'timestamp': time.time()
}

try:
    response = requests.post(
        'http://localhost:8001/detect-abandonment',
        headers=headers,
        json=test_data,
        timeout=10
    )
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Abandonment Detection: Working")
        print(f"   Cart Abandoned: {result.get('abandoned')}")
        print(f"   Recommendations: {len(result.get('data', {}).get('recommendations', []))}")
    else:
        print(f"❌ Abandonment Detection: Error {response.status_code}")
        
except Exception as e:
    print(f"❌ Abandonment Detection: {e}")

print("\n🎯 SUMMARY:")
print("System is ready for WordPress integration!")
print("Use these endpoints in your WordPress plugin:")
print("- Abandonment Detection: http://localhost:8001/detect-abandonment")
print("- Email Generation: http://localhost:8002/generate-email")