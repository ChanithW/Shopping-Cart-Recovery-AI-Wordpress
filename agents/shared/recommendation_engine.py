"""
TF-IDF based product recommendation engine for cart recovery.
Uses product names and descriptions to find similar items.
"""

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict, Any, Tuple
import logging
from sqlalchemy.orm import Session
from .db import Product, get_db_session

class ProductRecommendationEngine:
    """TF-IDF based recommendation system for suggesting similar products."""
    
    def __init__(self):
        self.vectorizer = None
        self.tfidf_matrix = None
        self.products = []
        self.product_texts = []
        self.logger = logging.getLogger(__name__)
        
    def load_products(self, db_session: Session = None):
        """Load products from database and prepare TF-IDF vectors."""
        if db_session is None:
            db_session = get_db_session()
        
        try:
            # Fetch all products that are in stock
            products = db_session.query(Product).filter(
                Product.stock_status == 'in_stock',
                Product.stock_quantity > 0
            ).all()
            
            self.products = []
            self.product_texts = []
            
            for product in products:
                self.products.append({
                    'id': product.id,
                    'item_name': product.item_name,
                    'description': product.description,
                    'price': float(product.price),
                    'category': product.category,
                    'stock_quantity': product.stock_quantity
                })
                
                # Combine name and description for TF-IDF
                combined_text = f"{product.item_name} {product.description}"
                self.product_texts.append(combined_text)
            
            # Create TF-IDF vectors
            if self.product_texts:
                self.vectorizer = TfidfVectorizer(
                    max_features=5000,
                    stop_words='english',
                    ngram_range=(1, 2),
                    min_df=1,
                    max_df=0.95
                )
                self.tfidf_matrix = self.vectorizer.fit_transform(self.product_texts)
                self.logger.info(f"Loaded {len(self.products)} products for recommendations")
            
        except Exception as e:
            self.logger.error(f"Error loading products: {str(e)}")
            raise
        finally:
            db_session.close()
    
    def preprocess_cart_items(self, cart_items: List[Dict[str, Any]]) -> List[str]:
        """Extract and preprocess text from cart items."""
        cart_texts = []
        for item in cart_items:
            name = item.get('name', '')
            description = item.get('description', '')
            combined = f"{name} {description}".strip()
            if combined:
                cart_texts.append(combined)
        return cart_texts
    
    def find_similar_products(self, cart_items: List[Dict[str, Any]], top_n: int = 5) -> List[Dict[str, Any]]:
        """Find top N similar products based on cart items."""
        if not self.products or not self.tfidf_matrix is not None:
            try:
                self.load_products()
            except Exception as e:
                self.logger.warning(f"Failed to load products from database: {e}. Using fallback recommendations.")
                return self._get_fallback_recommendations(cart_items, top_n)
        
        if not self.products:
            self.logger.warning("No products available for recommendations")
            return self._get_fallback_recommendations(cart_items, top_n)
        
        try:
            # Get cart item texts
            cart_texts = self.preprocess_cart_items(cart_items)
            if not cart_texts:
                self.logger.warning("No valid text found in cart items")
                return self._get_popular_products(top_n)
            
            # Transform cart items to TF-IDF vectors
            cart_vectors = self.vectorizer.transform(cart_texts)
            
            # Calculate average cart vector if multiple items
            if cart_vectors.shape[0] > 1:
                avg_cart_vector = np.mean(cart_vectors.toarray(), axis=0).reshape(1, -1)
            else:
                avg_cart_vector = cart_vectors
            
            # Calculate cosine similarities
            similarities = cosine_similarity(avg_cart_vector, self.tfidf_matrix).flatten()
            
            # Get cart product IDs to exclude them from recommendations
            cart_product_ids = set()
            for item in cart_items:
                if 'product_id' in item:
                    cart_product_ids.add(item['product_id'])
            
            # Create similarity scores with product info
            product_similarities = []
            for i, (product, similarity) in enumerate(zip(self.products, similarities)):
                # Skip products already in cart
                if product['id'] in cart_product_ids:
                    continue
                
                product_similarities.append({
                    'product': product,
                    'similarity': similarity,
                    'rank': i
                })
            
            # Sort by similarity score
            product_similarities.sort(key=lambda x: x['similarity'], reverse=True)
            
            # Return top N recommendations
            recommendations = []
            for item in product_similarities[:top_n]:
                product = item['product']
                recommendations.append({
                    'id': product['id'],
                    'item_name': product['item_name'],
                    'description': product['description'],
                    'price': product['price'],
                    'category': product['category'],
                    'stock_quantity': product['stock_quantity'],
                    'similarity_score': round(float(item['similarity']), 4),
                    'reason': self._generate_recommendation_reason(product, cart_items)
                })
            
            self.logger.info(f"Generated {len(recommendations)} recommendations")
            return recommendations
            
        except Exception as e:
            self.logger.error(f"Error generating recommendations: {str(e)}")
            return self._get_popular_products(top_n)
    
    def _generate_recommendation_reason(self, product: Dict, cart_items: List[Dict]) -> str:
        """Generate a human-readable reason for the recommendation."""
        product_category = product.get('category', '').lower()
        
        # Check if cart has items in same category
        cart_categories = [item.get('category', '').lower() for item in cart_items]
        
        if product_category in cart_categories:
            if product_category == 'smartphone':
                return "Perfect companion for your tech setup"
            elif product_category == 'shoes':
                return "Great addition to your athletic gear"
            else:
                return "Complements your current selection"
        else:
            # Cross-category recommendation
            if product_category == 'smartphone' and 'shoes' in cart_categories:
                return "Stay connected during your workouts"
            elif product_category == 'shoes' and 'smartphone' in cart_categories:
                return "Perfect for your active lifestyle"
            else:
                return "Customers like you also bought this"
    
    def _get_popular_products(self, top_n: int) -> List[Dict[str, Any]]:
        """Fallback to popular products when recommendations fail."""
        try:
            # Sort by stock quantity as a proxy for popularity
            popular_products = sorted(
                self.products, 
                key=lambda x: x['stock_quantity'], 
                reverse=True
            )
            
            recommendations = []
            for product in popular_products[:top_n]:
                recommendations.append({
                    'id': product['id'],
                    'item_name': product['item_name'],
                    'description': product['description'],
                    'price': product['price'],
                    'category': product['category'],
                    'stock_quantity': product['stock_quantity'],
                    'similarity_score': 0.0,
                    'reason': "Popular choice among customers"
                })
            
            return recommendations
        except Exception as e:
            self.logger.error(f"Error getting popular products: {str(e)}")
            return []
    
    def _get_fallback_recommendations(self, cart_items: List[Dict[str, Any]], top_n: int = 5) -> List[Dict[str, Any]]:
        """Provide fallback recommendations when database is not available."""
        self.logger.info("Using fallback recommendations due to database unavailability")
        
        # Extract categories from cart items
        categories = set()
        for item in cart_items:
            if 'category' in item:
                categories.add(item['category'].lower())
        
        # Provide generic recommendations based on cart categories
        fallback_recommendations = []
        
        if 'smartphone' in categories:
            fallback_recommendations.extend([
                {
                    'id': 9991,
                    'item_name': 'Premium Phone Case',
                    'description': 'Protect your smartphone with our premium case',
                    'price': 29.99,
                    'category': 'smartphone',
                    'stock_quantity': 50,
                    'similarity_score': 0.8,
                    'reason': "Complements your smartphone purchase"
                },
                {
                    'id': 9992,
                    'item_name': 'Screen Protector',
                    'description': 'Crystal clear screen protection for your device',
                    'price': 19.99,
                    'category': 'smartphone',
                    'stock_quantity': 100,
                    'similarity_score': 0.7,
                    'reason': "Essential accessory for smartphone protection"
                }
            ])
        
        if 'shoes' in categories:
            fallback_recommendations.extend([
                {
                    'id': 9993,
                    'item_name': 'Shoe Care Kit',
                    'description': 'Complete care kit for maintaining your shoes',
                    'price': 24.99,
                    'category': 'shoes',
                    'stock_quantity': 75,
                    'similarity_score': 0.8,
                    'reason': "Keep your shoes looking new longer"
                },
                {
                    'id': 9994,
                    'item_name': 'Orthotic Insoles',
                    'description': 'Comfort-enhancing insoles for better support',
                    'price': 34.99,
                    'category': 'shoes',
                    'stock_quantity': 60,
                    'similarity_score': 0.7,
                    'reason': "Improve comfort and support for your shoes"
                }
            ])
        
        # If no category-specific recommendations, provide general ones
        if not fallback_recommendations:
            fallback_recommendations = [
                {
                    'id': 9995,
                    'item_name': 'Premium Accessory Bundle',
                    'description': 'Complete accessory bundle for your purchase',
                    'price': 49.99,
                    'category': 'accessories',
                    'stock_quantity': 25,
                    'similarity_score': 0.6,
                    'reason': "Popular accessory bundle"
                },
                {
                    'id': 9996,
                    'item_name': 'Extended Warranty',
                    'description': 'Peace of mind with extended warranty coverage',
                    'price': 39.99,
                    'category': 'services',
                    'stock_quantity': 200,
                    'similarity_score': 0.5,
                    'reason': "Protect your investment"
                }
            ]
        
        return fallback_recommendations[:top_n]
    
    def get_category_recommendations(self, category: str, exclude_ids: List[int] = None, top_n: int = 3) -> List[Dict[str, Any]]:
        """Get recommendations from a specific category."""
        if exclude_ids is None:
            exclude_ids = []
        
        try:
            category_products = [
                p for p in self.products 
                if p['category'].lower() == category.lower() and p['id'] not in exclude_ids
            ]
            
            # Sort by stock quantity (popularity proxy)
            category_products.sort(key=lambda x: x['stock_quantity'], reverse=True)
            
            recommendations = []
            for product in category_products[:top_n]:
                recommendations.append({
                    'id': product['id'],
                    'item_name': product['item_name'],
                    'description': product['description'],
                    'price': product['price'],
                    'category': product['category'],
                    'stock_quantity': product['stock_quantity'],
                    'similarity_score': 0.8,  # High relevance for same category
                    'reason': f"Popular in {category} category"
                })
            
            return recommendations
        except Exception as e:
            self.logger.error(f"Error getting category recommendations: {str(e)}")
            return []

# Example usage and testing
if __name__ == "__main__":
    # Initialize recommendation engine
    engine = ProductRecommendationEngine()
    
    # Load products (this would normally connect to database)
    # For testing, we'll create some mock data
    engine.products = [
        {
            'id': 1,
            'item_name': 'iPhone 15 Pro Max',
            'description': 'Latest iPhone with advanced camera and A17 Pro chip',
            'price': 1299.99,
            'category': 'smartphone',
            'stock_quantity': 50
        },
        {
            'id': 2,
            'item_name': 'Samsung Galaxy S24',
            'description': 'Flagship Android phone with AI features and great camera',
            'price': 849.99,
            'category': 'smartphone',
            'stock_quantity': 75
        },
        {
            'id': 3,
            'item_name': 'Nike Air Zoom Pegasus',
            'description': 'Comfortable running shoes with responsive cushioning',
            'price': 129.99,
            'category': 'shoes',
            'stock_quantity': 120
        }
    ]
    
    engine.product_texts = [
        f"{p['item_name']} {p['description']}" for p in engine.products
    ]
    
    # Test cart items
    test_cart = [
        {
            'product_id': 1,
            'name': 'iPhone 15 Pro',
            'description': 'High-end smartphone',
            'price': 999.99,
            'quantity': 1
        }
    ]
    
    print("Testing recommendation engine...")
    recommendations = engine.find_similar_products(test_cart, top_n=3)
    
    for rec in recommendations:
        print(f"- {rec['item_name']}: ${rec['price']} (Score: {rec['similarity_score']})")
        print(f"  Reason: {rec['reason']}")