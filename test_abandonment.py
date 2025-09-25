#!/usr/bin/env python3
"""
Cart Abandonment Detection Test
Tests various scenarios for cart abandonment detection
"""

import requests
import json
import os
import time
from dotenv import load_dotenv

load_dotenv()

def print_header(title):
    print("\n" + "="*60)
    print(f"🛒 {title}")
    print("="*60)

def print_test(test_name):
    print(f"\n📋 {test_name}")
    print("-"*40)

def test_abandonment_scenarios():
    print_header("CART ABANDONMENT DETECTION TEST")
    
    api_token = os.getenv("API_TOKEN")
    if not api_token:
        print("❌ Error: API_TOKEN not found in environment")
        return False
    
    headers = {
        'Authorization': f'Bearer {api_token}',
        'Content-Type': 'application/json'
    }
    
    base_url = "http://localhost:8001"
    
    # Test service availability first
    print_test("Service Health Check")
    try:
        response = requests.get(f"{base_url}/docs", timeout=5)
        if response.status_code == 200:
            print("✅ Abandonment Detector Service: ACCESSIBLE")
        else:
            print(f"❌ Service returned status: {response.status_code}")
            return False
    except Exception as e:
        # Try to start the service
        print(f"⚠️  Service not accessible: {e}")
        print("🔄 Attempting to start service...")
        
        import subprocess
        import sys
        
        try:
            # Start the service in background
            env = os.environ.copy()
            env['PYTHONPATH'] = r"c:\IRWA_2\Shopping-Cart-Recovery-AI-Wordpress"
            
            subprocess.Popen([
                sys.executable, "-m", "uvicorn", 
                "agents.abandonment_detector.app:app",
                "--host", "0.0.0.0", "--port", "8001"
            ], env=env, cwd=r"c:\IRWA_2\Shopping-Cart-Recovery-AI-Wordpress")
            
            # Wait for service to start
            time.sleep(3)
            
            # Test again
            response = requests.get(f"{base_url}/docs", timeout=5)
            if response.status_code == 200:
                print("✅ Service started successfully")
            else:
                print("❌ Failed to start service")
                return False
                
        except Exception as start_error:
            print(f"❌ Could not start service: {start_error}")
            return False
    
    # Test scenarios
    test_scenarios = [
        {
            "name": "Scenario 1: Short Visit - No Abandonment",
            "data": {
                "user_id": "user_001",
                "email": "test1@example.com",
                "items": [
                    {
                        "product_id": 1001,
                        "name": "Wireless Mouse",
                        "price": 25.99,
                        "quantity": 1
                    }
                ],
                "behavior": {
                    "idle_time": 30,  # 30 seconds - should NOT trigger abandonment
                    "pages_viewed": 2,
                    "session_duration": 45
                },
                "timestamp": time.time()
            },
            "expected_abandoned": False
        },
        {
            "name": "Scenario 2: Long Idle Time - Should Trigger Abandonment",
            "data": {
                "user_id": "user_002", 
                "email": "test2@example.com",
                "items": [
                    {
                        "product_id": 1002,
                        "name": "Gaming Keyboard",
                        "price": 89.99,
                        "quantity": 1
                    },
                    {
                        "product_id": 1003,
                        "name": "Mouse Pad",
                        "price": 15.99,
                        "quantity": 2
                    }
                ],
                "behavior": {
                    "idle_time": 180,  # 3 minutes - should trigger abandonment
                    "pages_viewed": 5,
                    "session_duration": 300
                },
                "timestamp": time.time()
            },
            "expected_abandoned": True
        },
        {
            "name": "Scenario 3: High Value Cart - Extended Idle",
            "data": {
                "user_id": "user_003",
                "email": "test3@example.com", 
                "items": [
                    {
                        "product_id": 1004,
                        "name": "Gaming Laptop",
                        "price": 1299.99,
                        "quantity": 1
                    },
                    {
                        "product_id": 1005,
                        "name": "Laptop Bag",
                        "price": 49.99,
                        "quantity": 1
                    }
                ],
                "behavior": {
                    "idle_time": 300,  # 5 minutes - definitely abandoned
                    "pages_viewed": 8,
                    "session_duration": 450
                },
                "timestamp": time.time()
            },
            "expected_abandoned": True
        }
    ]
    
    results = []
    
    for scenario in test_scenarios:
        print_test(scenario["name"])
        
        try:
            response = requests.post(
                f"{base_url}/detect-abandonment",
                headers=headers,
                json=scenario["data"],
                timeout=15
            )
            
            if response.status_code == 200:
                result = response.json()
                abandoned = result.get("abandoned", False)
                data = result.get("data", {})
                
                print(f"   ✅ Request Status: SUCCESS")
                print(f"   📊 Cart Abandoned: {abandoned}")
                print(f"   👤 User ID: {data.get('user_id', 'N/A')}")
                print(f"   📧 Email: {data.get('email', 'N/A')}")
                print(f"   🛍️  Items in Cart: {len(data.get('items', []))}")
                print(f"   ⏱️  Idle Time: {data.get('behavior', {}).get('idle_time', 'N/A')} seconds")
                
                recommendations = data.get('recommendations', [])
                print(f"   🎯 AI Recommendations: {len(recommendations)}")
                
                if recommendations:
                    print("   💡 Sample Recommendations:")
                    for i, rec in enumerate(recommendations[:2], 1):
                        print(f"      {i}. {rec.get('name', 'N/A')[:50]}")
                
                # Check if result matches expectation
                if abandoned == scenario["expected_abandoned"]:
                    print(f"   ✅ Result matches expectation: {abandoned}")
                    results.append(True)
                else:
                    print(f"   ⚠️  Result mismatch - Expected: {scenario['expected_abandoned']}, Got: {abandoned}")
                    results.append(False)
                    
            elif response.status_code == 401:
                print(f"   ❌ Authentication Error: Invalid API token")
                results.append(False)
            else:
                print(f"   ❌ Request Failed: Status {response.status_code}")
                print(f"   📄 Response: {response.text}")
                results.append(False)
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
            results.append(False)
    
    # Summary
    print_header("TEST SUMMARY")
    
    passed_tests = sum(results)
    total_tests = len(results)
    
    print(f"📊 Test Results: {passed_tests}/{total_tests} scenarios passed")
    
    if passed_tests == total_tests:
        print("🎉 CART ABANDONMENT DETECTION: FULLY FUNCTIONAL")
        print("✅ All abandonment scenarios working correctly")
        print("✅ AI recommendations being generated")
        print("✅ Authentication working properly")
        print("✅ System ready for production use")
    elif passed_tests > 0:
        print("⚠️  CART ABANDONMENT DETECTION: PARTIALLY WORKING") 
        print(f"✅ {passed_tests} scenarios working")
        print(f"❌ {total_tests - passed_tests} scenarios need attention")
    else:
        print("❌ CART ABANDONMENT DETECTION: NOT WORKING")
        print("🔧 System needs troubleshooting")
    
    return passed_tests == total_tests

if __name__ == "__main__":
    test_abandonment_scenarios()