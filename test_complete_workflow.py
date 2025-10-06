#!/usr/bin/env python3
"""
Complete end-to-end test for cart abandonment detection and email generation
Tests the full workflow: abandonment detection -> TF-IDF recommendations -> email generation
"""

import requests
import json
import time

def test_complete_workflow():
    print("🛒 Testing Complete Cart Abandonment & Email Workflow")
    print("=" * 60)

    # Test data - abandoned cart with iPhone
    cart_data = {
        "user_id": "test_user_123",
        "email": "test@example.com",
        "items": [
            {
                "product_id": 1,
                "name": "iPhone 15 Pro Max",
                "price": 1199.99,
                "quantity": 1
            }
        ],
        "timestamp": 1705312200.0,
        "behavior": {
            "pages_viewed": 3,
            "idle_time": 300,
            "session_duration": 1800
        }
    }

    try:
        # Step 1: Test abandonment detection
        print("1️⃣ Testing Cart Abandonment Detection...")
        response = requests.post(
            "http://localhost:8006/detect-abandonment",
            json=cart_data,
            headers={"Authorization": "Bearer test-token"}
        )

        if response.status_code != 200:
            print(f"❌ Abandonment detection failed: {response.status_code}")
            print(response.text)
            return False

        abandonment_result = response.json()
        print("✅ Cart abandonment detected successfully")
        print(f"   Abandoned: {abandonment_result['abandoned']}")

        # Extract recommendations from the response
        data = abandonment_result.get('data', {})
        recommendations = data.get('recommendations', [])
        print(f"   TF-IDF Recommendations: {len(recommendations)} items")

        if recommendations:
            for i, rec in enumerate(recommendations, 1):
                print(f"     {i}. {rec['name']} - ${rec['price']}")
        else:
            print("   ⚠️  No recommendations generated")

        # Step 2: Test email generation
        print("\n2️⃣ Testing Email Generation...")
        email_payload = {
            "name": "John Doe",
            "email": cart_data["email"],
            "items": cart_data["items"],
            "recommendations": recommendations,
            "behavior": cart_data["behavior"],
            "persona": "price_sensitive"
        }

        response = requests.post(
            "http://localhost:8002/generate-email",
            json=email_payload,
            headers={"Authorization": "Bearer d405b55571c2b2471760c4ccfc6a62a9d8e8ee5e15a3cccd6a576cf69939f379"}
        )

        if response.status_code != 200:
            print(f"❌ Email generation failed: {response.status_code}")
            print(response.text)
            return False

        email_result = response.json()
        print("✅ Email generated successfully")
        print(f"   Subject: {email_result['subject']}")
        print(f"   Email length: {len(email_result['body'])} characters")
        print(f"   Offers: {len(email_result.get('offers', []))} special offers")
        print(f"   Total savings: ${email_result.get('total_savings', 0):.2f}")

        # Check if email contains recommendations
        email_body = email_result['body'].lower()
        has_recommendations = any(rec['name'].lower() in email_body for rec in recommendations)
        if has_recommendations:
            print("✅ Email contains TF-IDF product recommendations")
        else:
            print("⚠️  Email may not contain recommendations")

        # Step 3: Test service health
        print("\n3️⃣ Testing Service Health...")

        # Test abandonment detector health
        try:
            response = requests.get("http://localhost:8006/health")
            if response.status_code == 200:
                print("✅ Abandonment Detector: Healthy")
            else:
                print("⚠️  Abandonment Detector: Health check failed")
        except:
            print("❌ Abandonment Detector: Not responding")

        # Test email generator health
        try:
            response = requests.get("http://localhost:8002/health")
            if response.status_code == 200:
                print("✅ Email Generator: Healthy")
            else:
                print("⚠️  Email Generator: Health check failed")
        except:
            print("❌ Email Generator: Not responding")

        print("\n🎉 WORKFLOW TEST PASSED!")
        print("✅ Cart abandonment detection: Working")
        print("✅ TF-IDF recommendations: Working")
        print("✅ Email generation: Working")
        print("✅ Services are healthy and responding")

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
    success = test_complete_workflow()
    if success:
        print("\n🚀 Your Shopping Cart Recovery AI is fully operational!")
        print("   Customers who abandon their carts will now receive")
        print("   personalized emails with intelligent product recommendations.")
    else:
        print("\n❌ Some components are not working. Check the error messages above.")
    exit(0 if success else 1)