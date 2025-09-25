#!/usr/bin/env python3
"""
Live LLM Demo - Shows the LLM working in real-time
"""

import requests
import json
import os
from dotenv import load_dotenv
import time

load_dotenv()

def demo_llm_in_action():
    print("🤖 LIVE LLM DEMONSTRATION")
    print("="*60)
    print("Let's see the LLM (Gemini) working in real-time!")
    
    api_token = os.getenv("API_TOKEN")
    headers = {
        'Authorization': f'Bearer {api_token}',
        'Content-Type': 'application/json'
    }
    
    # Demo scenarios
    scenarios = [
        {
            "name": "Tech Enthusiast Cart",
            "items": [
                {"product_id": 1001, "name": "Gaming Laptop", "price": 1599.99, "quantity": 1},
                {"product_id": 1002, "name": "Mechanical Keyboard", "price": 149.99, "quantity": 1}
            ],
            "persona": "tech_enthusiast"
        },
        {
            "name": "Fitness Lover Cart", 
            "items": [
                {"product_id": 2001, "name": "Smartwatch", "price": 299.99, "quantity": 1},
                {"product_id": 2002, "name": "Wireless Earbuds", "price": 179.99, "quantity": 1}
            ],
            "persona": "fitness_enthusiast"
        },
        {
            "name": "Home Chef Cart",
            "items": [
                {"product_id": 3001, "name": "Stand Mixer", "price": 379.99, "quantity": 1}
            ],
            "persona": "cooking_enthusiast"
        }
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n🎭 SCENARIO {i}: {scenario['name']}")
        print("="*60)
        
        # Step 1: Test Abandonment Detection LLM
        print(f"\n📍 STEP 1: LLM Product Recommendations")
        print("-"*40)
        
        abandonment_data = {
            "user_id": f"demo_user_{i}",
            "email": f"demo{i}@example.com", 
            "items": scenario["items"],
            "behavior": {
                "idle_time": 90,  # Above threshold
                "pages_viewed": 5,
                "session_duration": 300
            },
            "timestamp": time.time()
        }
        
        print(f"🛒 Cart Items: {[item['name'] for item in scenario['items']]}")
        print(f"💰 Total Value: ${sum(item['price'] * item['quantity'] for item in scenario['items']):.2f}")
        
        try:
            print(f"\n🤖 Calling LLM for product recommendations...")
            response = requests.post(
                'http://localhost:8001/detect-abandonment',
                headers=headers,
                json=abandonment_data,
                timeout=15
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get('abandoned'):
                    recommendations = result.get('data', {}).get('recommendations', [])
                    print(f"✅ LLM Generated {len(recommendations)} Recommendations:")
                    
                    for j, rec in enumerate(recommendations, 1):
                        name = rec.get('name', 'Unknown')
                        price = rec.get('price', 0)
                        if len(name) > 50:
                            name = name[:50] + "..."
                        print(f"   {j}. {name} - ${price:.2f}")
                    
                    # Step 2: Test Email Generation LLM
                    print(f"\n📍 STEP 2: LLM Email Generation")
                    print("-"*40)
                    
                    email_data = {
                        "user_id": f"demo_user_{i}",
                        "email": f"demo{i}@example.com",
                        "name": f"Demo Customer {i}",
                        "items": scenario["items"],
                        "recommendations": recommendations[:3],
                        "behavior": {
                            "idle_time": 90,
                            "pages_viewed": 5,
                            "session_duration": 300
                        },
                        "persona": scenario["persona"]
                    }
                    
                    print(f"👤 Customer Persona: {scenario['persona']}")
                    print(f"🤖 Calling LLM for personalized email...")
                    
                    email_response = requests.post(
                        'http://localhost:8002/generate-email',
                        headers=headers,
                        json=email_data,
                        timeout=20
                    )
                    
                    if email_response.status_code == 200:
                        email_result = email_response.json()
                        
                        print(f"\n✅ LLM Generated Personalized Content:")
                        print(f"📧 Subject: {email_result.get('subject', 'N/A')}")
                        
                        offers = email_result.get('offers', [])
                        if offers:
                            print(f"🎁 LLM Generated Offers:")
                            for offer in offers:
                                print(f"   • {offer.get('description', 'N/A')}")
                        
                        # Show part of the email body
                        body = email_result.get('body', '')
                        if body:
                            # Extract first few lines for preview
                            lines = body.replace('<', '\n<').split('\n')
                            text_lines = [line for line in lines if not line.strip().startswith('<') and line.strip()]
                            if text_lines:
                                preview = text_lines[0] if text_lines else "Email content generated"
                                if len(preview) > 100:
                                    preview = preview[:100] + "..."
                                print(f"📝 Email Preview: {preview}")
                    else:
                        print(f"❌ Email generation failed: {email_response.status_code}")
                else:
                    print(f"⚠️  Cart not flagged as abandoned (unexpected)")
            else:
                print(f"❌ Abandonment detection failed: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Demo error: {e}")
        
        # Add delay between scenarios
        if i < len(scenarios):
            print(f"\n⏳ Waiting 3 seconds before next scenario...")
            time.sleep(3)
    
    # Summary
    print(f"\n" + "="*60)
    print("🎉 LLM DEMONSTRATION COMPLETE!")
    print("="*60)
    
    print(f"\n💡 What you just saw:")
    print("1. 🧠 LLM analyzing cart contents and generating relevant recommendations")
    print("2. 🎨 LLM creating personalized email subjects based on customer personas") 
    print("3. 🎁 LLM suggesting contextual offers and discounts")
    print("4. ⚡ Real-time AI processing in under 10 seconds per request")
    
    print(f"\n🤖 The LLM (Google Gemini) makes your system intelligent by:")
    print("✅ Understanding product relationships and cross-sell opportunities")
    print("✅ Personalizing communication based on customer behavior")
    print("✅ Generating contextual offers that increase conversion rates")
    print("✅ Adapting content style to different customer personas")
    
    print(f"\n🚀 This is why your cart recovery system has AI superpowers!")

if __name__ == "__main__":
    demo_llm_in_action()