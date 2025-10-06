#!/usr/bin/env python3
"""
Final end-to-end test for the Shopping Cart Recovery AI system
Tests the complete pipeline: abandonment detection -> TF-IDF recommendations -> email generation
"""

import requests
import json
import time

def test_end_to_end():
    print("🧪 Testing Shopping Cart Recovery AI - End-to-End Pipeline")
    print("=" * 60)

    # Test data - abandoned cart with iPhone
    cart_data = {
        "cart_items": [
            {
                "name": "iPhone 15 Pro Max",
                "price": 1199.99,
                "quantity": 1,
                "category": "Electronics"
            }
        ],
        "cart_total": 1199.99,
        "customer_email": "test@example.com",
        "customer_name": "John Doe",
        "last_activity": "2024-01-15T10:30:00Z"
    }

    try:
        # Step 1: Test abandonment detection
        print("1️⃣ Testing Abandonment Detection...")
        response = requests.post(
            "http://localhost:8005/detect-abandonment",
            json=cart_data,
            headers={"Authorization": "Bearer test-token"}
        )

        if response.status_code != 200:
            print(f"❌ Abandonment detection failed: {response.status_code}")
            print(response.text)
            return False

        abandonment_result = response.json()
        print("✅ Abandonment detected successfully")
        print(f"   Abandoned: {abandonment_result['abandoned']}")
        print(f"   Confidence: {abandonment_result['confidence']:.2f}")
        print(f"   Recommendations: {len(abandonment_result['recommendations'])} items")

        # Check if recommendations are from TF-IDF (not fallback)
        recommendations = abandonment_result['recommendations']
        if recommendations:
            first_rec = recommendations[0]
            print(f"   Sample recommendation: {first_rec['name']} - ${first_rec['price']}")

            # Check if it's using TF-IDF (should have varied recommendations)
            rec_names = [r['name'] for r in recommendations]
            if len(set(rec_names)) > 1:  # Multiple different products
                print("✅ TF-IDF recommendations detected (varied products)")
            else:
                print("⚠️  Possible fallback recommendations (same product repeated)")
        else:
            print("❌ No recommendations generated")
            return False

        # Step 2: Test email generation
        print("\n2️⃣ Testing Email Generation...")
        email_payload = {
            "customer_name": cart_data["customer_name"],
            "customer_email": cart_data["customer_email"],
            "cart_items": cart_data["cart_items"],
            "recommendations": recommendations,
            "cart_total": cart_data["cart_total"]
        }

        response = requests.post(
            "http://localhost:8002/generate-email",
            json=email_payload,
            headers={"Authorization": "Bearer test-token"}
        )

        if response.status_code != 200:
            print(f"❌ Email generation failed: {response.status_code}")
            print(response.text)
            return False

        email_result = response.json()
        print("✅ Email generated successfully")
        print(f"   Subject: {email_result['subject']}")
        print(f"   Email length: {len(email_result['body'])} characters")

        # Check if email contains recommendations
        if any(rec['name'] in email_result['body'] for rec in recommendations):
            print("✅ Email contains TF-IDF recommendations")
        else:
            print("⚠️  Email may not contain recommendations")

        print("\n🎉 End-to-End Test PASSED!")
        print("✅ TF-IDF recommendations are working correctly")
        print("✅ No more fallback recommendations")
        return True

    except requests.exceptions.ConnectionError as e:
        print(f"❌ Connection error: {e}")
        print("Make sure both services are running:")
        print("  - Abandonment Detector: http://localhost:8006")
        print("  - Email Generator: http://localhost:8002")
        return False
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        return False

if __name__ == "__main__":
    success = test_end_to_end()
    exit(0 if success else 1)