#!/usr/bin/env python3
"""
System Test Script for Shopping Cart Recovery AI
Tests both abandonment detector and email generator services
"""

import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")
BASE_URL_DETECTOR = "http://localhost:8001"
BASE_URL_EMAIL = "http://localhost:8002"

headers = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}

def test_service_health():
    """Test if both services are running"""
    print("🔍 Testing Service Health...")
    
    try:
        # Test abandonment detector
        response = requests.get(f"{BASE_URL_DETECTOR}/docs", timeout=5)
        if response.status_code == 200:
            print("✅ Abandonment Detector Service: RUNNING")
        else:
            print(f"❌ Abandonment Detector Service: ERROR {response.status_code}")
    except Exception as e:
        print(f"❌ Abandonment Detector Service: NOT ACCESSIBLE - {e}")
    
    try:
        # Test email generator
        response = requests.get(f"{BASE_URL_EMAIL}/docs", timeout=5)
        if response.status_code == 200:
            print("✅ Email Generator Service: RUNNING")
        else:
            print(f"❌ Email Generator Service: ERROR {response.status_code}")
    except Exception as e:
        print(f"❌ Email Generator Service: NOT ACCESSIBLE - {e}")

def test_abandonment_detection():
    """Test abandonment detection endpoint"""
    print("\n🛒 Testing Abandonment Detection...")
    
    test_data = {
        "user_id": "test_user_123",
        "email": "test@example.com",
        "items": [
            {
                "product_id": 1001,
                "name": "Wireless Headphones",
                "price": 99.99,
                "quantity": 1
            },
            {
                "product_id": 1002, 
                "name": "Phone Case",
                "price": 24.99,
                "quantity": 2
            }
        ],
        "behavior": {
            "idle_time": 120,  # 2 minutes - should trigger abandonment
            "pages_viewed": 5,
            "session_duration": 300
        },
        "timestamp": 1727257200.0  # Unix timestamp
    }
    
    try:
        response = requests.post(
            f"{BASE_URL_DETECTOR}/detect-abandonment",
            headers=headers,
            json=test_data,
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Abandonment Detection: SUCCESS")
            print(f"   Abandoned: {result.get('abandoned', 'N/A')}")
            if result.get('data'):
                print(f"   User ID: {result['data'].get('user_id', 'N/A')}")
                print(f"   Recommendations: {len(result['data'].get('recommendations', []))} items")
            return result
        else:
            print(f"❌ Abandonment Detection: ERROR {response.status_code}")
            print(f"   Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Abandonment Detection: FAILED - {e}")
        return None

def test_email_generation():
    """Test email generation endpoint"""
    print("\n📧 Testing Email Generation...")
    
    test_data = {
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
        response = requests.post(
            f"{BASE_URL_EMAIL}/generate-email",
            headers=headers,
            json=test_data,
            timeout=15
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Email Generation: SUCCESS")
            print(f"   Subject: {result.get('subject', 'N/A')[:50]}...")
            print(f"   Content Length: {len(result.get('content', ''))} chars")
            if result.get('offers'):
                print(f"   Offers: {len(result['offers'])} generated")
            return result
        else:
            print(f"❌ Email Generation: ERROR {response.status_code}")
            print(f"   Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Email Generation: FAILED - {e}")
        return None

def test_authentication():
    """Test API authentication"""
    print("\n🔐 Testing Authentication...")
    
    # Test with valid token
    try:
        response = requests.post(
            f"{BASE_URL_DETECTOR}/detect-abandonment",
            headers=headers,
            json={"user_id": "test", "items": [], "behavior": {"idle_time": 10, "pages_viewed": 1, "session_duration": 60}, "timestamp": 1727257200.0},
            timeout=5
        )
        if response.status_code != 401:
            print("✅ Authentication: Valid token accepted")
        else:
            print("❌ Authentication: Valid token rejected")
    except Exception as e:
        print(f"❌ Authentication test failed: {e}")
    
    # Test with invalid token
    invalid_headers = headers.copy()
    invalid_headers["Authorization"] = "Bearer invalid_token"
    
    try:
        response = requests.post(
            f"{BASE_URL_DETECTOR}/detect-abandonment",
            headers=invalid_headers,
            json={"user_id": "test", "items": [], "behavior": {"idle_time": 10, "pages_viewed": 1, "session_duration": 60}, "timestamp": 1727257200.0},
            timeout=5
        )
        if response.status_code == 401:
            print("✅ Authentication: Invalid token properly rejected")
        else:
            print("❌ Authentication: Invalid token not rejected")
    except Exception as e:
        print(f"❌ Authentication test failed: {e}")

def main():
    print("=" * 60)
    print("🚀 SHOPPING CART RECOVERY AI - SYSTEM TEST")
    print("=" * 60)
    
    # Run all tests
    test_service_health()
    test_authentication()
    abandonment_result = test_abandonment_detection()
    email_result = test_email_generation()
    
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    tests_passed = 0
    total_tests = 4
    
    if abandonment_result:
        tests_passed += 1
        print("✅ Abandonment Detection: PASSED")
    else:
        print("❌ Abandonment Detection: FAILED")
        
    if email_result:
        tests_passed += 1
        print("✅ Email Generation: PASSED")
    else:
        print("❌ Email Generation: FAILED")
    
    print(f"\n🎯 Overall Result: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("🎉 System is working properly!")
    else:
        print("⚠️  System has issues that need attention.")

if __name__ == "__main__":
    main()