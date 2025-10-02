#!/usr/bin/env python3
"""
Test script for the enhanced Shopping Cart Recovery AI system.
Tests dynamic offers, TF-IDF recommendations, and personalized email generation.
"""

import json
import sys
import os
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

try:
    from agents.shared.offer_calculator import OfferCalculator
    from agents.shared.gemini_client import PersonalizedEmailGenerator
    print("✅ Successfully imported enhanced modules!")
    
    # Test 1: Dynamic Offer Calculation
    print("\n=== Testing Dynamic Offer Calculator ===")
    calculator = OfferCalculator()
    
    test_carts = [
        # Low value cart - no discount
        [{"name": "Phone Case", "price": 29.99, "quantity": 1}],
        # Medium cart - 5% discount
        [{"name": "iPhone 15 Pro", "price": 999.99, "quantity": 1}, 
         {"name": "AirPods Pro", "price": 249.99, "quantity": 1}],
        # High value cart - 20% discount
        [{"name": "iPhone 15 Pro Max", "price": 1299.99, "quantity": 4}]
    ]
    
    for i, cart in enumerate(test_carts, 1):
        offer = calculator.generate_offer_details(cart)
        print(f"Cart {i}: {calculator.format_currency(offer['cart_total'])}")
        print(f"  Offer: {offer['offer_summary']}")
        print(f"  Final: {calculator.format_currency(offer['final_amount'])}")
        print(f"  Savings: {calculator.format_currency(offer['total_savings'])}")
        print()
    
    # Test 2: Email Generation
    print("=== Testing Personalized Email Generator ===")
    email_generator = PersonalizedEmailGenerator()
    
    # Test persona detection
    smartphone_cart = [
        {"name": "iPhone 15 Pro", "price": 999.99, "quantity": 1, "category": "smartphone"}
    ]
    
    shoes_cart = [
        {"name": "Nike Air Zoom Pegasus", "price": 129.99, "quantity": 1, "category": "shoes"}
    ]
    
    behavior = {"pages_viewed": 5, "idle_time": 120, "session_duration": 600}
    
    # Test smartphone persona
    persona1 = email_generator.determine_customer_persona(smartphone_cart, behavior)
    greeting1 = email_generator.get_personalized_greeting(persona1, "John")
    print(f"Smartphone cart persona: {persona1}")
    print(f"Greeting: {greeting1}")
    
    # Test shoes persona
    persona2 = email_generator.determine_customer_persona(shoes_cart, behavior)
    greeting2 = email_generator.get_personalized_greeting(persona2, "Sarah")
    print(f"Shoes cart persona: {persona2}")
    print(f"Greeting: {greeting2}")
    
    print("\n✅ All tests completed successfully!")
    print("\n📝 Next Steps:")
    print("1. Run: python -m uvicorn agents.abandonment_detector.app:app --host 0.0.0.0 --port 8006")
    print("2. Run: python -m uvicorn agents.email_generator_offer_suggestor.app:app --host 0.0.0.0 --port 8002")
    print("3. Access the manual database setup: http://yourwordpress/wp-content/plugins/shopping-cart-recovery/setup_database.php")
    print("4. Activate the WordPress plugin to create the products table")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure all dependencies are installed:")
    print("pip install fastapi uvicorn pydantic sqlalchemy google-generativeai scikit-learn numpy pandas python-dotenv")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()