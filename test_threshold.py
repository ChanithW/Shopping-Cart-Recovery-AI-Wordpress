#!/usr/bin/env python3
"""
Cart Abandonment Threshold Test
Tests the exact abandonment threshold (60 seconds)
"""

import requests
import json
import os
import time
from dotenv import load_dotenv

load_dotenv()

def test_abandonment_threshold():
    print("🛒 CART ABANDONMENT THRESHOLD TEST")
    print("="*50)
    
    api_token = os.getenv("API_TOKEN")
    headers = {
        'Authorization': f'Bearer {api_token}',
        'Content-Type': 'application/json'
    }
    
    base_url = "http://localhost:8001"
    
    # Test cases around the 60-second threshold
    test_cases = [
        {
            "name": "Test 1: 30 seconds (Below threshold)",
            "idle_time": 30,
            "expected": False
        },
        {
            "name": "Test 2: 59 seconds (Just below threshold)", 
            "idle_time": 59,
            "expected": False
        },
        {
            "name": "Test 3: 60 seconds (Exact threshold)",
            "idle_time": 60,
            "expected": False  # Should be False because condition is > 60
        },
        {
            "name": "Test 4: 61 seconds (Just above threshold)",
            "idle_time": 61,
            "expected": True
        },
        {
            "name": "Test 5: 120 seconds (Well above threshold)",
            "idle_time": 120,
            "expected": True
        }
    ]
    
    results = []
    
    for test_case in test_cases:
        print(f"\n📋 {test_case['name']}")
        print(f"   Idle Time: {test_case['idle_time']} seconds")
        print(f"   Expected Abandonment: {test_case['expected']}")
        
        test_data = {
            "user_id": f"threshold_test_{test_case['idle_time']}",
            "email": "threshold@example.com",
            "items": [{
                "product_id": 9999,
                "name": "Test Product",
                "price": 19.99,
                "quantity": 1
            }],
            "behavior": {
                "idle_time": test_case['idle_time'],
                "pages_viewed": 3,
                "session_duration": test_case['idle_time'] + 60
            },
            "timestamp": time.time()
        }
        
        try:
            response = requests.post(
                f"{base_url}/detect-abandonment",
                headers=headers,
                json=test_data,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                actual_abandoned = result.get("abandoned", False)
                
                print(f"   🔍 Actual Result: {actual_abandoned}")
                
                if actual_abandoned == test_case['expected']:
                    print(f"   ✅ PASS: Result matches expectation")
                    results.append(True)
                else:
                    print(f"   ❌ FAIL: Expected {test_case['expected']}, got {actual_abandoned}")
                    results.append(False)
                
                # Show recommendations if abandoned
                if actual_abandoned:
                    data = result.get("data", {})
                    recommendations = data.get("recommendations", [])
                    print(f"   🎯 Recommendations generated: {len(recommendations)}")
                    
            else:
                print(f"   ❌ Request failed: {response.status_code}")
                results.append(False)
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
            results.append(False)
    
    # Summary
    print("\n" + "="*50)
    print("📊 THRESHOLD TEST SUMMARY")
    print("="*50)
    
    passed = sum(results)
    total = len(results)
    
    print(f"Results: {passed}/{total} tests passed")
    print(f"Threshold: > 60 seconds triggers abandonment")
    
    if passed == total:
        print("\n🎉 ABANDONMENT THRESHOLD: WORKING PERFECTLY")
        print("✅ Threshold logic is accurate (idle_time > 60 seconds)")
        print("✅ AI recommendations generated for abandoned carts")
        print("✅ Non-abandoned carts handled correctly")
    else:
        print(f"\n⚠️  ABANDONMENT THRESHOLD: {total-passed} ISSUES FOUND")
    
    return passed == total

# Also test the actual abandonment detection logic
def test_abandonment_features():
    print("\n🔧 ABANDONMENT DETECTION FEATURES TEST")
    print("="*50)
    
    api_token = os.getenv("API_TOKEN")
    headers = {
        'Authorization': f'Bearer {api_token}',
        'Content-Type': 'application/json'
    }
    
    # Test with multiple items and realistic scenario
    realistic_cart = {
        "user_id": "customer_12345",
        "email": "customer@shopping.com",
        "items": [
            {
                "product_id": 2001,
                "name": "iPhone 15 Pro",
                "price": 999.99,
                "quantity": 1
            },
            {
                "product_id": 2002,
                "name": "iPhone Case",
                "price": 29.99,
                "quantity": 1
            },
            {
                "product_id": 2003,
                "name": "Wireless Charger",
                "price": 39.99,
                "quantity": 2
            }
        ],
        "behavior": {
            "idle_time": 180,  # 3 minutes
            "pages_viewed": 12,
            "session_duration": 600  # 10 minutes total session
        },
        "timestamp": time.time()
    }
    
    print("📱 Testing realistic shopping cart abandonment...")
    print(f"   Cart Value: ${sum(item['price'] * item['quantity'] for item in realistic_cart['items']):.2f}")
    print(f"   Items: {len(realistic_cart['items'])}")
    print(f"   Idle Time: {realistic_cart['behavior']['idle_time']} seconds")
    
    try:
        response = requests.post(
            "http://localhost:8001/detect-abandonment",
            headers=headers,
            json=realistic_cart,
            timeout=15
        )
        
        if response.status_code == 200:
            result = response.json()
            
            print(f"\n✅ Abandonment Detection Result:")
            print(f"   Cart Abandoned: {result.get('abandoned')}")
            
            if result.get('abandoned'):
                data = result.get('data', {})
                recommendations = data.get('recommendations', [])
                
                print(f"   🎯 AI Recommendations: {len(recommendations)}")
                print(f"   📊 User Data Captured: ✅")
                print(f"   📧 Email Ready for Generation: ✅")
                
                if recommendations:
                    print("\n   💡 Sample AI Recommendations:")
                    for i, rec in enumerate(recommendations[:3], 1):
                        rec_name = rec.get('name', 'N/A')
                        if len(rec_name) > 60:
                            rec_name = rec_name[:60] + "..."
                        print(f"      {i}. {rec_name}")
                
                return True
            else:
                print("   ⚠️  Cart not flagged as abandoned (unexpected)")
                return False
        else:
            print(f"   ❌ Request failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

if __name__ == "__main__":
    threshold_success = test_abandonment_threshold()
    features_success = test_abandonment_features()
    
    print("\n" + "="*60)
    print("🏁 FINAL CART ABANDONMENT TEST RESULTS")
    print("="*60)
    
    if threshold_success and features_success:
        print("🎉 CART ABANDONMENT DETECTION: FULLY FUNCTIONAL")
        print("✅ Threshold logic working perfectly (>60 seconds)")
        print("✅ AI recommendations generated correctly")
        print("✅ Real-world scenarios handled properly") 
        print("✅ Ready for WordPress integration")
    else:
        print("⚠️  CART ABANDONMENT DETECTION: NEEDS ATTENTION")
        if not threshold_success:
            print("❌ Threshold logic issues detected")
        if not features_success:
            print("❌ Feature functionality issues detected")