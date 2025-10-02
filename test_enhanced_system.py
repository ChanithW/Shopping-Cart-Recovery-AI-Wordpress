#!/usr/bin/env python3
"""
Comprehensive test script for the enhanced Shopping Cart Recovery AI system.
Tests dynamic offers, TF-IDF recommendations, and personalized email generation.
"""

import requests
import json
import time
from typing import Dict, List, Any

class SCRSystemTester:
    """Test the Shopping Cart Recovery AI system end-to-end."""
    
    def __init__(self, detector_url: str = "http://localhost:8005", 
                 email_url: str = "http://localhost:8002",
                 api_token: str = "d405b55571c2b2471760c4ccfc6a62a9d8e8ee5e15a3cccd6a576cf69939f379"):
        self.detector_url = detector_url
        self.email_url = email_url
        self.headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json"
        }
    
    def test_smartphone_cart(self) -> Dict:
        """Test with smartphone-focused cart."""
        cart_data = {
            "user_id": "test_user_1",
            "email": "tech@example.com",
            "items": [
                {
                    "product_id": 1,
                    "name": "iPhone 15 Pro Max 256GB",
                    "description": "Experience the ultimate iPhone with titanium design, advanced camera system, and A17 Pro chip for unmatched performance.",
                    "price": 1299.99,
                    "quantity": 1,
                    "category": "smartphone",
                    "stock_quantity": 45
                },
                {
                    "product_id": 25,
                    "name": "Apple AirPods Pro 2nd Gen",
                    "description": "Premium wireless earbuds with active noise cancellation, spatial audio, and personalized listening experience.",
                    "price": 249.99,
                    "quantity": 1,
                    "category": "smartphone",
                    "stock_quantity": 128
                }
            ],
            "timestamp": time.time(),
            "behavior": {
                "pages_viewed": 8,
                "idle_time": 45,
                "session_duration": 320
            }
        }
        return cart_data
    
    def test_running_cart(self) -> Dict:
        """Test with running shoes focused cart."""
        cart_data = {
            "user_id": "test_user_2",
            "email": "runner@example.com",
            "items": [
                {
                    "product_id": 76,
                    "name": "Nike Air Zoom Pegasus 40",
                    "description": "Iconic running shoe with responsive Zoom Air units, breathable mesh upper, and reliable traction for daily miles.",
                    "price": 129.99,
                    "quantity": 1,
                    "category": "shoes",
                    "stock_quantity": 87
                },
                {
                    "product_id": 121,
                    "name": "Balega Hidden Comfort No-Show",
                    "description": "Premium running socks with seamless toe closure, moisture-wicking fabric, and blister prevention technology.",
                    "price": 14.99,
                    "quantity": 3,
                    "category": "shoes",
                    "stock_quantity": 456
                }
            ],
            "timestamp": time.time(),
            "behavior": {
                "pages_viewed": 12,
                "idle_time": 120,
                "session_duration": 600
            }
        }
        return cart_data
    
    def test_high_value_cart(self) -> Dict:
        """Test with high-value cart for premium discount."""
        cart_data = {
            "user_id": "test_user_3",
            "email": "premium@example.com",
            "items": [
                {
                    "product_id": 8,
                    "name": "Samsung Galaxy S24 Ultra 512GB",
                    "description": "Premium Android flagship with S Pen, 200MP camera, AI-enhanced photography, and stunning 6.8-inch Dynamic AMOLED display.",
                    "price": 1399.99,
                    "quantity": 2,
                    "category": "smartphone",
                    "stock_quantity": 29
                },
                {
                    "product_id": 15,
                    "name": "Samsung Galaxy Z Fold5 512GB",
                    "description": "Revolutionary foldable phone that transforms into a tablet with multitasking capabilities and S Pen support.",
                    "price": 1899.99,
                    "quantity": 1,
                    "category": "smartphone",
                    "stock_quantity": 15
                }
            ],
            "timestamp": time.time(),
            "behavior": {
                "pages_viewed": 15,
                "idle_time": 60,
                "session_duration": 900
            }
        }
        return cart_data
    
    def test_abandonment_detection(self, cart_data: Dict) -> Dict:
        """Test the abandonment detector API."""
        print(f"🔍 Testing abandonment detection for user: {cart_data['user_id']}")
        
        try:
            response = requests.post(
                f"{self.detector_url}/detect-abandonment",
                headers=self.headers,
                json=cart_data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Abandonment detected: {result.get('abandoned', False)}")
                return result
            else:
                print(f"❌ Abandonment API error: {response.status_code} - {response.text}")
                return {}
                
        except Exception as e:
            print(f"❌ Abandonment API exception: {str(e)}")
            return {}
    
    def test_email_generation(self, cart_data: Dict, name: str, persona: str = "valued_customer") -> Dict:
        """Test the email generation API."""
        print(f"📧 Testing email generation for: {name}")
        
        email_data = {
            "user_id": cart_data["user_id"],
            "email": cart_data["email"],
            "name": name,
            "items": cart_data["items"],
            "recommendations": [],
            "behavior": cart_data["behavior"],
            "persona": persona
        }
        
        try:
            response = requests.post(
                f"{self.email_url}/generate-email",
                headers=self.headers,
                json=email_data,
                timeout=45
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Email generated successfully")
                print(f"   Subject: {result.get('subject', 'N/A')}")
                print(f"   Offers: {result.get('offers', [])}")
                print(f"   Total Savings: ${result.get('total_savings', 0):.2f}")
                print(f"   Final Amount: ${result.get('final_amount', 0):.2f}")
                return result
            else:
                print(f"❌ Email API error: {response.status_code} - {response.text}")
                return {}
                
        except Exception as e:
            print(f"❌ Email API exception: {str(e)}")
            return {}
    
    def test_offer_calculations(self, cart_data: Dict) -> None:
        """Test offer calculation logic."""
        print(f"💰 Testing offer calculations")
        
        total = sum(item['price'] * item['quantity'] for item in cart_data['items'])
        print(f"   Cart total: ${total:.2f}")
        
        # Expected discount logic
        if total >= 500:  # $50000 in cents
            expected_discount = 20
        elif total >= 100:  # $10000 in cents
            expected_discount = 10
        elif total >= 50:   # $5000 in cents
            expected_discount = 5
        else:
            expected_discount = 0
        
        print(f"   Expected discount: {expected_discount}%")
        
        discount_amount = total * (expected_discount / 100)
        final_total = total - discount_amount
        total_savings = discount_amount + 9.99  # Include free shipping
        
        print(f"   Expected savings: ${total_savings:.2f}")
        print(f"   Expected final: ${final_total:.2f}")
    
    def run_comprehensive_test(self) -> None:
        """Run comprehensive test suite."""
        print("🚀 Starting Shopping Cart Recovery AI System Test")
        print("=" * 60)
        
        # Test cases
        test_cases = [
            {
                "name": "Tech Enthusiast Sarah",
                "cart": self.test_smartphone_cart(),
                "persona": "tech_enthusiast_apple"
            },
            {
                "name": "Runner Mike",
                "cart": self.test_running_cart(),
                "persona": "running_enthusiast"
            },
            {
                "name": "Premium Customer Alex",
                "cart": self.test_high_value_cart(),
                "persona": "valued_customer"
            }
        ]
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n📋 Test Case {i}: {test_case['name']}")
            print("-" * 40)
            
            # Test offer calculations
            self.test_offer_calculations(test_case['cart'])
            
            # Test abandonment detection
            abandonment_result = self.test_abandonment_detection(test_case['cart'])
            
            # Test email generation
            email_result = self.test_email_generation(
                test_case['cart'], 
                test_case['name'], 
                test_case['persona']
            )
            
            # Brief pause between tests
            time.sleep(2)
        
        print("\n🎉 Test suite completed!")
        print("=" * 60)
    
    def test_health_endpoints(self) -> None:
        """Test health check endpoints."""
        print("🏥 Testing health endpoints")
        
        try:
            # Test email service health
            response = requests.get(f"{self.email_url}/health", timeout=10)
            if response.status_code == 200:
                print("✅ Email service healthy")
            else:
                print(f"❌ Email service unhealthy: {response.status_code}")
        except Exception as e:
            print(f"❌ Email service unreachable: {str(e)}")

def main():
    """Main test execution."""
    print("Shopping Cart Recovery AI - Enhanced System Test")
    print("Testing dynamic offers, TF-IDF recommendations, and personalized emails")
    print()
    
    tester = SCRSystemTester()
    
    # Test health first
    tester.test_health_endpoints()
    print()
    
    # Run comprehensive tests
    tester.run_comprehensive_test()

if __name__ == "__main__":
    main()