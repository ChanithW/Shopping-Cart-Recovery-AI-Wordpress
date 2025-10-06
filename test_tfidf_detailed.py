#!/usr/bin/env python3
"""
Detailed TF-IDF testing
"""
from agents.shared.recommendation_engine import ProductRecommendationEngine
from sklearn.metrics.pairwise import cosine_similarity

engine = ProductRecommendationEngine()
engine.load_products()

print('Product texts:')
for i, text in enumerate(engine.product_texts):
    print(f'  {i+1}. {text}')

print('\nTesting similarity calculation...')

# Test with different cart items
test_cases = [
    {'name': 'iPhone 15 Pro Max', 'description': 'Latest iPhone with advanced camera'},
    {'name': 'Samsung Galaxy', 'description': 'Android phone'},
    {'name': 'Unknown Phone', 'description': 'some phone with camera'}
]

for i, cart_item in enumerate(test_cases):
    print(f'\nTest case {i+1}: {cart_item["name"]}')

    cart_texts = [f'{cart_item["name"]} {cart_item["description"]}']
    cart_vectors = engine.vectorizer.transform(cart_texts)

    similarities = cosine_similarity(cart_vectors, engine.tfidf_matrix).flatten()
    print(f'Similarities: {[round(s, 3) for s in similarities]}')

    # Get top 2
    top_indices = similarities.argsort()[-2:][::-1]
    for j, idx in enumerate(top_indices):
        print(f'  Top {j+1}: {engine.products[idx]["item_name"]} (score: {similarities[idx]:.3f})')