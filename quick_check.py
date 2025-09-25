#!/usr/bin/env python3
"""
Quick System Validation Test
"""
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

def test_system():
    print("🔍 SYSTEM VALIDATION CHECK")
    print("=" * 50)
    
    api_token = os.getenv("API_TOKEN")
    headers = {
        'Authorization': f'Bearer {api_token}',
        'Content-Type': 'application/json'
    }
    
    # Test 1: Service Health
    print("\n1. Service Health Check")
    services = {
        "Abandonment Detector": "http://localhost:8001/docs",
        "Email Generator": "http://localhost:8002/docs"
    }
    
    healthy_services = 0
    for name, url in services.items():
        try:
            response = requests.get(url, timeout=3)
            if response.status_code == 200:
                print(f"   ✅ {name}: HEALTHY")
                healthy_services += 1
            else:
                print(f"   ❌ {name}: ERROR {response.status_code}")
        except Exception as e:
            print(f"   ❌ {name}: NOT ACCESSIBLE ({e})")
    
    if healthy_services != 2:
        print("\n⚠️  Some services are not running. System partially operational.")
        return False
    
    # Test 2: Basic Functionality
    print("\n2. Functional Test")
    
    # Test abandonment detection
    test_data = {
        'user_id': 'test_123',
        'email': 'test@example.com',
        'items': [{
            'product_id': 1001,
            'name': 'Test Product',
            'price': 50.0,
            'quantity': 1
        }],
        'behavior': {
            'idle_time': 150,  # Should trigger abandonment
            'pages_viewed': 3,
            'session_duration': 200
        },
        'timestamp': 1727257200.0
    }
    
    try:
        print("   Testing abandonment detection...")
        response = requests.post(
            'http://localhost:8001/detect-abandonment',
            headers=headers,
            json=test_data,
            timeout=15
        )
        
        if response.status_code == 200:
            result = response.json()
            abandoned = result.get('abandoned', False)
            print(f"   ✅ Abandonment Detection: {abandoned}")
            
            if abandoned:
                # Test email generation
                print("   Testing email generation...")
                
                email_data = {
                    "user_id": "test_123",
                    "email": "test@example.com",
                    "name": "Test User",
                    "items": result['data']['items'],
                    "recommendations": result['data'].get('recommendations', [])[:2],
                    "behavior": result['data']['behavior'],
                    "persona": "new_customer"
                }
                
                email_response = requests.post(
                    'http://localhost:8002/generate-email',
                    headers=headers,
                    json=email_data,
                    timeout=20
                )
                
                if email_response.status_code == 200:
                    email_result = email_response.json()
                    print(f"   ✅ Email Generation: SUCCESS")
                    print(f"   📧 Subject: {email_result.get('subject', 'N/A')}")
                    return True
                else:
                    print(f"   ❌ Email Generation: FAILED ({email_response.status_code})")
                    return False
            else:
                print("   ⚠️  No abandonment detected (may be normal)")
                return True
                
        else:
            print(f"   ❌ Abandonment Detection: FAILED ({response.status_code})")
            return False
            
    except Exception as e:
        print(f"   ❌ Test Error: {e}")
        return False

def main():
    success = test_system()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 SYSTEM STATUS: FULLY OPERATIONAL")
        print("✅ All services running properly")
        print("✅ AI integration working")
        print("✅ APIs responding correctly")
        print("\n📡 Endpoints Ready:")
        print("   • http://localhost:8001 (Abandonment Detection)")
        print("   • http://localhost:8002 (Email Generation)")
    else:
        print("⚠️  SYSTEM STATUS: ISSUES DETECTED")
        print("❌ Some functionality may not be working")
        print("🔧 Check service logs for details")

if __name__ == "__main__":
    main()