#!/usr/bin/env python3
"""
Test loading products from wp_products table
"""

from agents.shared.recommendation_engine import ProductRecommendationEngine

def main():
    rec = ProductRecommendationEngine()
    rec.load_products()
    print(f'Loaded {len(rec.products)} products from wp_products table')
    print('\nSample products:')
    for i, product in enumerate(rec.products[:5]):
        print(f'{i+1}. {product["item_name"]} - ${product["price"]} ({product["category"]})')

    # Test TF-IDF recommendations
    print('\nTesting TF-IDF recommendations for iPhone 15 Pro Max...')
    test_items = [{
        'name': 'iPhone 15 Pro Max 256GB',
        'description': 'Experience the ultimate iPhone with titanium design',
        'category': 'smartphone',
        'product_id': 1
    }]

    recommendations = rec.find_similar_products(test_items, top_n=5)
    print(f'Found {len(recommendations)} recommendations:')
    for i, rec in enumerate(recommendations):
        print(f'{i+1}. {rec["item_name"]} - ${rec["price"]}')

if __name__ == "__main__":
    main()