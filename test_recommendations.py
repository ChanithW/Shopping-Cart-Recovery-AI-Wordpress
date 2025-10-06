#!/usr/bin/env python3
"""
Test script for TF-IDF recommendation engine
"""
from agents.shared.recommendation_engine import ProductRecommendationEngine

try:
    print("🔍 Testing TF-IDF Recommendation Engine...")

    engine = ProductRecommendationEngine()
    print("✅ Recommendation engine created")

    # Try to load products
    engine.load_products()
    print(f"✅ Products loaded: {len(engine.products)}")

    if engine.products:
        print("📊 Sample products:")
        for i, p in enumerate(engine.products[:3]):
            print(f"  {i+1}. {p['item_name']} - {p['category']}")

    # Test recommendations
    test_cart = [{'name': 'iPhone', 'description': 'smartphone', 'product_id': 1}]
    recommendations = engine.find_similar_products(test_cart, top_n=3)
    print(f"✅ Got {len(recommendations)} recommendations")

    if recommendations:
        print("🎯 Recommendations:")
        for i, rec in enumerate(recommendations):
            print(f"  {i+1}. {rec['item_name']} (score: {rec['similarity_score']:.3f})")
            print(f"     Reason: {rec['reason']}")

    print("🎉 TF-IDF system is working!")

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()