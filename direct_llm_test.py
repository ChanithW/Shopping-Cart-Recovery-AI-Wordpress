#!/usr/bin/env python3
"""
Direct LLM Test - Test Gemini API directly
"""

import sys
import os

# Add the project root to Python path
sys.path.append(r"c:\IRWA_2\Shopping-Cart-Recovery-AI-Wordpress")

from agents.shared.gemini_client import get_product_recommendations, generate_email_content, suggest_offers
from agents.abandonment_detector.models import CartItem
from agents.email_generator_offer_suggestor.models import EmailData
from dotenv import load_dotenv

load_dotenv()

def test_llm_directly():
    print("🤖 DIRECT LLM (GEMINI) TESTING")
    print("="*50)
    
    # Test 1: Product Recommendations
    print("\n1. 🛍️ TESTING: get_product_recommendations()")
    print("-"*40)
    
    # Create sample cart items
    cart_items = [
        CartItem(product_id=1001, name="iPhone 15 Pro", price=999.99, quantity=1),
        CartItem(product_id=1002, name="AirPods Pro", price=249.99, quantity=1)
    ]
    
    print(f"Input Cart Items:")
    for item in cart_items:
        print(f"  • {item.name} - ${item.price}")
    
    print(f"\n🤖 LLM Processing...")
    recommendations = get_product_recommendations(cart_items)
    
    print(f"✅ LLM Generated Recommendations:")
    for i, rec in enumerate(recommendations, 1):
        print(f"  {i}. {rec['name']} - ${rec['price']:.2f}")
    
    # Test 2: Email Content Generation
    print(f"\n2. 📧 TESTING: generate_email_content()")
    print("-"*40)
    
    # Mock EmailData
    class MockEmailData:
        def __init__(self):
            self.name = "Sarah Johnson"
            self.items = [
                {"name": "MacBook Pro", "price": 1999.99},
                {"name": "Magic Mouse", "price": 79.99}
            ]
            self.persona = "creative_professional"
    
    email_data = MockEmailData()
    
    print(f"Input Data:")
    print(f"  • Customer: {email_data.name}")
    print(f"  • Items: {[item['name'] for item in email_data.items]}")
    print(f"  • Persona: {email_data.persona}")
    
    print(f"\n🤖 LLM Processing...")
    email_content = generate_email_content(email_data)
    
    print(f"✅ LLM Generated Email:")
    print(f"  📧 Subject: {email_content['subject']}")
    print(f"  📝 Body: {email_content['body'][:100]}..." if len(email_content['body']) > 100 else f"  📝 Body: {email_content['body']}")
    
    # Test 3: Offer Suggestions
    print(f"\n3. 🎁 TESTING: suggest_offers()")
    print("-"*40)
    
    print(f"Input: Same customer data as above")
    print(f"\n🤖 LLM Processing...")
    offers = suggest_offers(email_data)
    
    print(f"✅ LLM Generated Offers:")
    for i, offer in enumerate(offers, 1):
        print(f"  {i}. {offer.get('description', 'No description')} ({offer.get('value', 'No value')})")
    
    # Test 4: Different Scenario
    print(f"\n4. 🎮 TESTING: Gaming Scenario")
    print("-"*40)
    
    gaming_items = [
        CartItem(product_id=2001, name="Gaming Mouse", price=89.99, quantity=1),
        CartItem(product_id=2002, name="Mechanical Keyboard", price=149.99, quantity=1),
        CartItem(product_id=2003, name="Gaming Headset", price=199.99, quantity=1)
    ]
    
    print(f"Gaming Cart Items:")
    for item in gaming_items:
        print(f"  • {item.name} - ${item.price}")
    
    print(f"\n🤖 LLM Processing...")
    gaming_recs = get_product_recommendations(gaming_items)
    
    print(f"✅ LLM Gaming Recommendations:")
    for i, rec in enumerate(gaming_recs, 1):
        print(f"  {i}. {rec['name']} - ${rec['price']:.2f}")
    
    print(f"\n" + "="*50)
    print("🎉 DIRECT LLM TEST COMPLETE!")
    print("="*50)
    
    print(f"\n💡 LLM Functions Tested:")
    print("✅ Product Recommendations - Analyzes cart and suggests related items")
    print("✅ Email Content Generation - Creates personalized subject and body")
    print("✅ Offer Suggestions - Generates contextual discount offers")
    
    print(f"\n🤖 LLM Model: Google Gemini 1.5 Flash")
    print("🔑 API Key: Configured and working")
    print("⚡ Response Time: Real-time processing")
    print("🧠 Intelligence: Contextual understanding of products and customers")

if __name__ == "__main__":
    test_llm_directly()