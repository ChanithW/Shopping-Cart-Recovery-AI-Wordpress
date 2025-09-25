#!/usr/bin/env python3
"""
Quick API Test for Shopping Cart Recovery AI
Tests basic functionality with proper timeouts
"""

import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")
headers = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}

def test_quick():
    print("🔍 Quick System Test\n")
    
    # Test abandonment detection with proper data
    print("Testing Abandonment Detection...")
    test_data = {
        "user_id": "test_user_123",
        "email": "test@example.com",
        "items": [
            {
                "product_id": 1001,
                "name": "Wireless Headphones",
                "price": 99.99,
                "quantity": 1
            }
        ],
        "behavior": {
            "idle_time": 120,
            "pages_viewed": 5,
            "session_duration": 300
        },
        "timestamp": 1727257200.0
    }
    
    try:
        print("Sending request to abandonment detector...")
        response = requests.post(
            "http://localhost:8001/detect-abandonment",
            headers=headers,
            json=test_data,
            timeout=30
        )
        
        print(f"Response Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print("✅ SUCCESS!")
            print(f"Abandoned: {result.get('abandoned')}")
            if result.get('data'):
                data = result['data']
                print(f"User ID: {data.get('user_id')}")
                recommendations = data.get('recommendations', [])
                print(f"Recommendations: {len(recommendations)} items")
                if recommendations:
                    print(f"First recommendation: {recommendations[0] if recommendations else 'None'}")
        else:
            print(f"❌ FAILED: {response.text}")
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
    
    print("\n" + "-" * 50)
    
    # Test email generation  
    print("Testing Email Generation...")
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
    
    try:
        print("Sending request to email generator...")
        response = requests.post(
            "http://localhost:8002/generate-email",
            headers=headers,
            json=email_data,
            timeout=30
        )
        
        print(f"Response Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print("✅ SUCCESS!")
            print(f"Subject: {result.get('subject', 'N/A')}")
            print(f"Body length: {len(result.get('body', ''))} chars")
            offers = result.get('offers', [])
            print(f"Offers: {len(offers)}")
            if offers:
                print(f"First offer: {offers[0]}")
        else:
            print(f"❌ FAILED: {response.text}")
            
    except Exception as e:
        print(f"❌ ERROR: {e}")

if __name__ == "__main__":
    test_quick()