def apply_business_rules(offers, persona):
    # Apply rules: e.g., loyal -> discount, first_time -> free shipping
    if persona == "loyal":
        offers.append({"type": "discount", "value": "10%", "description": "10% coupon for loyal customers"})
    elif persona == "first_time":
        offers.append({"type": "free_shipping", "value": "Free", "description": "Free shipping on your first order"})
    # High value cart
    # Add more logic
    return offers