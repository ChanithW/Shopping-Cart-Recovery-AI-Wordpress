#!/usr/bin/env python3
"""
Simple LLM Test - Shows where AI works in the system
"""

import requests
import json

def test_api_endpoints():
    print("🤖 SHOPPING CART RECOVERY AI - LLM INTEGRATION TEST")
    print("="*60)
    
    print("\n📍 WHERE THE LLM WORKS IN THE SYSTEM:")
    print("-" * 40)
    print("1. 🛍️  Cart Abandonment Detection (Port 8001)")
    print("   • Analyzes user behavior patterns")
    print("   • AI generates personalized product recommendations")
    print("   • Uses Google Gemini 1.5 Flash for contextual understanding")
    
    print("\n2. 📧 Email Generation & Offers (Port 8002)")
    print("   • AI creates personalized email content")
    print("   • Generates dynamic subject lines")
    print("   • Suggests contextual offers and discounts")
    
    print("\n3. 🔗 WordPress Integration")
    print("   • PHP plugin calls AI services via REST API")
    print("   • Real-time cart tracking triggers AI analysis")
    print("   • Analytics dashboard shows AI-generated insights")
    
    # Test Abandonment Detection API
    print(f"\n🧪 TESTING AI SERVICE #1: Cart Abandonment Detection")
    print("-" * 50)
    
    test_data = {
        "user_id": "test_user_123",
        "email": "test@example.com",
        "timestamp": 1705315800.0,
        "items": [
            {
                "product_id": 101,
                "name": "MacBook Pro 16-inch",
                "price": 2499.99,
                "quantity": 1
            },
            {
                "product_id": 102,
                "name": "Magic Mouse",
                "price": 79.99,
                "quantity": 1
            }
        ],
        "behavior": {
            "idle_time": 120,
            "pages_viewed": 5,
            "session_duration": 300
        }
    }
    
    print(f"Input Cart Items:")
    for item in test_data['items']:
        print(f"  • {item['name']} - ${item['price']}")
    
    try:
        print(f"\n🔄 Calling AI Service at http://localhost:8001/detect-abandonment")
        response = requests.post(
            "http://localhost:8001/detect-abandonment",
            json=test_data,
            headers={"Authorization": "Bearer d405b55571c2b2471760c4ccfc6a62a9d8e8ee5e15a3cccd6a576cf69939f379"},
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ AI Analysis Complete!")
            print(f"📊 Result: {result}")
            
            if 'recommendations' in result:
                print(f"\n🤖 AI-Generated Product Recommendations:")
                for i, rec in enumerate(result['recommendations'], 1):
                    print(f"  {i}. {rec.get('name', 'Unknown')} - ${rec.get('price', 0)}")
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print(f"❌ Connection Error: AI service not running on port 8001")
        print(f"💡 To start service: cd agents/abandonment_detector && uvicorn app:app --host 0.0.0.0 --port 8001")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test Email Generation API
    print(f"\n🧪 TESTING AI SERVICE #2: Email Generation")
    print("-" * 50)
    
    email_data = {
        "user_id": "test_user_456", 
        "name": "Sarah Johnson",
        "email": "sarah@example.com",
        "items": [
            {"name": "Gaming Laptop", "price": 1299.99},
            {"name": "Gaming Mouse", "price": 89.99}
        ],
        "persona": "tech_enthusiast",
        "recommendations": [],
        "behavior": {
            "idle_time": 180,
            "pages_viewed": 3,
            "session_duration": 400
        }
    }
    
    print(f"Input Data:")
    print(f"  • Customer: {email_data['name']}")
    print(f"  • Items: {[item['name'] for item in email_data['items']]}")
    print(f"  • Persona: {email_data['persona']}")
    
    try:
        print(f"\n🔄 Calling AI Service at http://localhost:8002/generate-email")
        response = requests.post(
            "http://localhost:8002/generate-email",
            json=email_data,
            headers={"Authorization": "Bearer d405b55571c2b2471760c4ccfc6a62a9d8e8ee5e15a3cccd6a576cf69939f379"},
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ AI Email Generation Complete!")
            print(f"📧 Subject: {result.get('subject', 'No subject')}")
            print(f"📝 Body Preview: {result.get('body', 'No body')[:100]}...")
            
            if 'offers' in result:
                print(f"\n🎁 AI-Generated Offers:")
                for i, offer in enumerate(result['offers'], 1):
                    print(f"  {i}. {offer.get('description', 'No description')}")
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print(f"❌ Connection Error: AI service not running on port 8002")
        print(f"💡 To start service: cd agents/email_generator_offer_suggestor && uvicorn app:app --host 0.0.0.0 --port 8002")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Summary
    print(f"\n" + "=" * 60)
    print("🎯 LLM INTEGRATION SUMMARY")
    print("=" * 60)
    
    print(f"\n🧠 AI MODEL: Google Gemini 1.5 Flash")
    print(f"📍 INTEGRATION POINTS:")
    print(f"  1. agents/shared/gemini_client.py - Core AI functions")
    print(f"  2. agents/abandonment_detector/app.py - Behavior analysis")
    print(f"  3. agents/email_generator_offer_suggestor/app.py - Content generation")
    print(f"  4. wordpress_plugin/includes/api_handler.php - WordPress bridge")
    
    print(f"\n⚡ AI CAPABILITIES:")
    print(f"  • Contextual product recommendations based on cart analysis")
    print(f"  • Personalized email content generation")
    print(f"  • Dynamic offer suggestions based on user persona")
    print(f"  • Real-time behavioral pattern recognition")
    
    print(f"\n🔄 DATA FLOW:")
    print(f"  Cart Activity → WordPress Plugin → AI Services → LLM Analysis → Personalized Response")
    
    print(f"\n💡 The LLM is the 'brain' that:")
    print(f"  • Understands product relationships")
    print(f"  • Generates human-like email content")
    print(f"  • Creates contextually relevant recommendations")
    print(f"  • Adapts to different customer personas")

if __name__ == "__main__":
    test_api_endpoints()