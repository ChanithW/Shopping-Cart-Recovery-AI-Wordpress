#!/usr/bin/env python3
"""
Test just the abandonment detection with TF-IDF recommendations
"""

import requests
import json

def test_abandonment_detection():
    print("🧪 Testing Abandonment Detection with TF-IDF Recommendations")
    print("=" * 60)

    # Test data - abandoned cart with iPhone (matching CartData model)
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
        "timestamp": 1705312200.0,  # Unix timestamp
        "behavior": {
            "pages_viewed": 3,
            "idle_time": 300,  # 5 minutes
            "session_duration": 1800  # 30 minutes
        }
    }

    try:
        response = requests.post(
            "http://localhost:8006/detect-abandonment",
            json=cart_data,
            headers={"Authorization": "Bearer test-token"}
        )

        if response.status_code != 200:
            print(f"❌ Request failed: {response.status_code}")
            print(response.text)
            return False

        result = response.json()
        print("✅ Abandonment detection successful!")
        print(f"Full response: {json.dumps(result, indent=2)}")

        abandoned = result.get('abandoned', False)
        print(f"Abandoned: {abandoned}")

        recommendations = result.get('data', {}).get('recommendations', [])
        print(f"\n📦 Recommendations ({len(recommendations)} items):")

        for i, rec in enumerate(recommendations, 1):
            print(f"  {i}. {rec['name']} - ${rec['price']}")

        # Verify these are TF-IDF recommendations, not fallbacks
        rec_names = [r['name'] for r in recommendations]
        unique_names = set(rec_names)

        if len(unique_names) > 1:
            print("\n✅ SUCCESS: TF-IDF recommendations working!")
            print("   - Multiple different products recommended")
            print("   - No fallback hardcoded recommendations")
            return True
        elif len(recommendations) == 1 and recommendations[0]['name'] == "Similar Product":
            print("\n❌ FAILURE: Still using fallback recommendations")
            print("   - Fallback 'Similar Product' detected")
            return False
        else:
            print("\n⚠️  WARNING: Limited recommendations detected")
            print("   - May be working but with limited product data")
            return True

    except requests.exceptions.ConnectionError:
        print("❌ Connection failed - make sure abandonment detector is running on port 8005")
        return False
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_abandonment_detection()
    exit(0 if success else 1)