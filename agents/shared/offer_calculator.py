"""
Dynamic offer calculation logic for the Shopping Cart Recovery AI system.
Calculates personalized discounts based on cart total and provides offer details.
"""

from typing import Dict, List, Any
from decimal import Decimal

class OfferCalculator:
    """Handles dynamic offer calculation based on cart value and business rules."""
    
    def __init__(self):
        # Define discount tiers based on cart total
        self.discount_tiers = [
            {"min_amount": 50000, "discount_percent": 20, "label": "Premium Discount"},
            {"min_amount": 10000, "discount_percent": 10, "label": "Great Savings"},
            {"min_amount": 5000, "discount_percent": 5, "label": "Special Offer"},
        ]
    
    def calculate_cart_total(self, cart_items: List[Dict[str, Any]]) -> Decimal:
        """Calculate total cart value from items."""
        total = Decimal('0')
        for item in cart_items:
            price = Decimal(str(item.get('price', 0)))
            quantity = int(item.get('quantity', 1))
            total += price * quantity
        return total
    
    def get_applicable_discount(self, cart_total: Decimal) -> Dict[str, Any]:
        """Determine the best applicable discount for the cart total."""
        cart_total_cents = int(cart_total * 100)  # Convert to cents for comparison
        
        for tier in self.discount_tiers:
            if cart_total_cents >= tier["min_amount"]:
                discount_amount = cart_total * (Decimal(tier["discount_percent"]) / 100)
                return {
                    "discount_percent": tier["discount_percent"],
                    "discount_amount": round(discount_amount, 2),
                    "label": tier["label"],
                    "final_total": round(cart_total - discount_amount, 2),
                    "savings": round(discount_amount, 2)
                }
        
        # No discount applicable
        return {
            "discount_percent": 0,
            "discount_amount": Decimal('0'),
            "label": "No Discount",
            "final_total": round(cart_total, 2),
            "savings": Decimal('0')
        }
    
    def generate_offer_details(self, cart_items: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate complete offer details including discounts and free shipping."""
        cart_total = self.calculate_cart_total(cart_items)
        discount_info = self.get_applicable_discount(cart_total)
        
        # Everyone gets free shipping
        free_shipping = {
            "available": True,
            "value": Decimal('9.99'),  # Standard shipping cost
            "message": "Free shipping on all orders!"
        }
        
        # Calculate total savings
        total_savings = discount_info["savings"] + free_shipping["value"]
        
        return {
            "cart_total": cart_total,
            "discount": discount_info,
            "free_shipping": free_shipping,
            "total_savings": total_savings,
            "final_amount": discount_info["final_total"],
            "offer_summary": self._generate_offer_summary(discount_info, free_shipping, total_savings)
        }
    
    def _generate_offer_summary(self, discount_info: Dict, free_shipping: Dict, total_savings: Decimal) -> str:
        """Generate a human-readable offer summary."""
        parts = []
        
        if discount_info["discount_percent"] > 0:
            parts.append(f"{discount_info['discount_percent']}% off your cart")
        
        if free_shipping["available"]:
            parts.append("free shipping")
        
        if parts:
            summary = " + ".join(parts)
            return f"Save ${total_savings} with {summary}!"
        
        return "Free shipping on your order!"
    
    def format_currency(self, amount: Decimal) -> str:
        """Format decimal amount as currency string."""
        return f"${amount:,.2f}"
    
    def get_next_tier_incentive(self, cart_total: Decimal) -> Dict[str, Any]:
        """Get information about the next discount tier to encourage upselling."""
        cart_total_cents = int(cart_total * 100)
        
        for tier in reversed(self.discount_tiers):
            if cart_total_cents < tier["min_amount"]:
                amount_needed = Decimal(tier["min_amount"]) / 100 - cart_total
                return {
                    "available": True,
                    "amount_needed": round(amount_needed, 2),
                    "discount_percent": tier["discount_percent"],
                    "message": f"Add ${amount_needed:.2f} more to get {tier['discount_percent']}% off!"
                }
        
        return {"available": False, "message": "You're getting our best discount!"}

# Example usage and testing
if __name__ == "__main__":
    calculator = OfferCalculator()
    
    # Test with different cart values
    test_carts = [
        [{"name": "iPhone 15 Pro", "price": 999.99, "quantity": 1}],  # $999.99 - no discount
        [{"name": "iPhone 15 Pro", "price": 999.99, "quantity": 1}, 
         {"name": "AirPods Pro", "price": 249.99, "quantity": 2}],  # $1499.97 - 5% off
        [{"name": "MacBook Pro", "price": 2499.99, "quantity": 2}],  # $4999.98 - no discount
        [{"name": "MacBook Pro", "price": 2499.99, "quantity": 3}],  # $7499.97 - 10% off
        [{"name": "iPhone 15 Pro Max", "price": 1299.99, "quantity": 5}]  # $6499.95 - 20% off
    ]
    
    for i, cart in enumerate(test_carts, 1):
        print(f"\n--- Test Cart {i} ---")
        offer = calculator.generate_offer_details(cart)
        print(f"Cart Total: {calculator.format_currency(offer['cart_total'])}")
        print(f"Offer: {offer['offer_summary']}")
        print(f"Final Amount: {calculator.format_currency(offer['final_amount'])}")
        
        incentive = calculator.get_next_tier_incentive(offer['cart_total'])
        if incentive["available"]:
            print(f"Upsell: {incentive['message']}")