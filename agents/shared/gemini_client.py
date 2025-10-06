import google.generativeai as genai
import os
import json
import random
from typing import Dict, List, Any
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini API
def configure_gemini():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in environment variables")
    
    genai.configure(api_key=api_key)
    print("Gemini API configured successfully")

class PersonalizedEmailGenerator:
    """Advanced email generator with personalized content based on cart items and user behavior."""
    
    def __init__(self):
        configure_gemini()
        self.model = genai.GenerativeModel('gemini-1.5-pro')
    
    def determine_customer_persona(self, cart_items: List[Dict], behavior: Dict) -> str:
        """Determine customer persona based on cart contents and behavior."""
        categories = [item.get('category', '').lower() for item in cart_items]
        
        if 'smartphone' in categories:
            if any('iphone' in item.get('name', '').lower() for item in cart_items):
                return "tech_enthusiast_apple"
            elif any('samsung' in item.get('name', '').lower() for item in cart_items):
                return "tech_enthusiast_android"
            else:
                return "tech_enthusiast_general"
        
        elif 'shoes' in categories:
            if any('running' in item.get('name', '').lower() for item in cart_items):
                return "running_enthusiast"
            elif any('gym' in item.get('name', '').lower() or 'training' in item.get('name', '').lower() for item in cart_items):
                return "fitness_enthusiast"
            else:
                return "athletic_lifestyle"
        
        # Check for mixed categories
        if 'smartphone' in categories and 'shoes' in categories:
            return "active_tech_user"
        
        return "valued_customer"
    
    def get_personalized_greeting(self, persona: str, customer_name: str = "there") -> str:
        """Generate personalized greeting based on customer persona."""
        greetings = {
            "tech_enthusiast_apple": [
                f"Hello {customer_name}, fellow Apple enthusiast! 🍎",
                f"Hi {customer_name}, we know you appreciate premium tech! 📱",
                f"Hey {customer_name}, your taste in Apple products is impeccable! ✨"
            ],
            "tech_enthusiast_android": [
                f"Hello {customer_name}, Android power user! 🤖",
                f"Hi {customer_name}, we see you love cutting-edge Android tech! 📱",
                f"Hey {customer_name}, great choice in Samsung innovation! 🌟"
            ],
            "tech_enthusiast_general": [
                f"Hello {customer_name}, tech enthusiast! 💻",
                f"Hi {customer_name}, we love your tech-savvy choices! 🔧",
                f"Hey {customer_name}, staying ahead with the latest tech! 🚀"
            ],
            "running_enthusiast": [
                f"Hello {customer_name}, running enthusiast! 🏃‍♀️",
                f"Hi {customer_name}, ready to hit the pavement? 👟",
                f"Hey {customer_name}, your running gear is waiting! 🏃‍♂️"
            ],
            "fitness_enthusiast": [
                f"Hello {customer_name}, fitness warrior! 💪",
                f"Hi {customer_name}, time to crush those workouts! 🏋️‍♀️",
                f"Hey {customer_name}, your fitness journey continues! 🔥"
            ],
            "athletic_lifestyle": [
                f"Hello {customer_name}, active lifestyle champion! ⚡",
                f"Hi {customer_name}, living that athletic life! 🏃‍♀️",
                f"Hey {customer_name}, sport meets style! 👟"
            ],
            "active_tech_user": [
                f"Hello {customer_name}, the perfect blend of tech and fitness! 📱💪",
                f"Hi {customer_name}, staying connected while staying active! 🏃‍♀️📱",
                f"Hey {customer_name}, tech-enabled fitness enthusiast! ⚡"
            ],
            "valued_customer": [
                f"Hello {customer_name}, valued customer! 😊",
                f"Hi {customer_name}, we appreciate your business! 🌟",
                f"Hey {customer_name}, thanks for choosing us! 💝"
            ]
        }
        
        return random.choice(greetings.get(persona, greetings["valued_customer"]))

    def generate_email_content(self, 
                             customer_name: str,
                             cart_items: List[Dict],
                             recommendations: List[Dict],
                             offer_details: Dict,
                             behavior: Dict) -> Dict[str, str]:
        """Generate complete personalized email content."""
        
        persona = self.determine_customer_persona(cart_items, behavior)
        greeting = self.get_personalized_greeting(persona, customer_name)
        
        # Create email with Gemini AI
        try:
            prompt = f"""
            Create a compelling cart recovery email for a {persona} customer.
            
            Customer: {customer_name}
            Greeting: {greeting}
            
            Cart Items: {[f"{item.get('name', '')} - ${item.get('price', 0)}" for item in cart_items]}
            Offer: {offer_details.get('offer_summary', 'Special offer')}
            Savings: ${offer_details.get('total_savings', 0)}
            
            Recommendations: {[rec.get('item_name', '') for rec in recommendations[:3]]}
            
            Create a subject line and HTML email body that:
            1. Uses the exact greeting provided
            2. Mentions specific cart items
            3. Highlights the savings opportunity
            4. Includes product recommendations
            5. Creates urgency without being pushy
            
            Return as JSON with "subject" and "body" keys.
            """
            
            response = self.model.generate_content(prompt)
            
            # Try to parse JSON response
            try:
                content = json.loads(response.text)
                if 'subject' in content and 'body' in content:
                    return content
            except json.JSONDecodeError:
                pass
            
            # Fallback parsing
            lines = response.text.strip().split('\n')
            subject = f"Don't Miss Out - {offer_details.get('discount', {}).get('label', 'Special Offer')}!"
            body = self._create_fallback_html(greeting, cart_items, recommendations, offer_details)
            
            return {"subject": subject, "body": body}
            
        except Exception as e:
            print(f"Error generating email content: {e}")
            return self._create_fallback_email(greeting, cart_items, recommendations, offer_details)
    
    def _create_fallback_html(self, greeting: str, cart_items: List[Dict], 
                             recommendations: List[Dict], offer_details: Dict) -> str:
        """Create HTML email when AI generation fails."""
        cart_html = ""
        for item in cart_items:
            cart_html += f"<li>{item.get('name', 'Product')} - ${item.get('price', 0):.2f}</li>"
        
        rec_html = ""
        for rec in recommendations[:3]:
            rec_html += f"<li>{rec.get('item_name', 'Product')} - ${rec.get('price', 0):.2f}</li>"
        
        return f"""
        <html>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <h2 style="color: #2c5aa0;">{greeting}</h2>
            <p>We noticed you left some great items in your cart:</p>
            <ul>{cart_html}</ul>
            
            <div style="background-color: #e8f5e8; padding: 15px; border-radius: 8px; margin: 20px 0;">
                <h3 style="color: #2e7d32;">🎉 {offer_details.get('offer_summary', 'Special Offer!')}</h3>
                <p><strong>Total Savings: ${offer_details.get('total_savings', 0):.2f}</strong></p>
            </div>
            
            <h3>You might also like:</h3>
            <ul>{rec_html}</ul>
            
            <div style="text-align: center; margin: 30px 0;">
                <a href="#" style="background-color: #ff6b35; color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px;">
                    Complete Your Purchase
                </a>
            </div>
        </body>
        </html>
        """
    
    def _create_fallback_email(self, greeting: str, cart_items: List[Dict], 
                              recommendations: List[Dict], offer_details: Dict) -> Dict[str, str]:
        """Fallback email when everything fails."""
        return {
            "subject": "Complete Your Purchase - Special Offer!",
            "body": self._create_fallback_html(greeting, cart_items, recommendations, offer_details)
        }

# Legacy functions for backward compatibility
def get_product_recommendations(items):
    """Legacy function - use PersonalizedEmailGenerator instead."""
    try:
        generator = PersonalizedEmailGenerator()
        # Convert old format to new format
        cart_items = []
        for item in items:
            if hasattr(item, 'name'):
                cart_items.append({"name": item.name})
            else:
                cart_items.append({"name": str(item)})
        
        # This is a simplified version - full recommendations need database access
        return [{"name": "Recommended Product", "price": 0.0}]
    except Exception as e:
        print(f"Error in legacy function: {e}")
        return [{"name": "Unable to fetch recommendations", "price": 0.0}]

def generate_email_content(data):
    """Legacy function - use PersonalizedEmailGenerator instead."""
    try:
        generator = PersonalizedEmailGenerator()
        cart_items = getattr(data, 'items', [])
        name = getattr(data, 'name', 'Customer')
        behavior = {}
        
        # Convert to new format
        formatted_items = []
        for item in cart_items:
            formatted_items.append({
                "name": item.get('name', ''),
                "price": item.get('price', 0)
            })
        
        offer_details = {"offer_summary": "Special offer available", "total_savings": 0}
        recommendations = []
        
        return generator.generate_email_content(name, formatted_items, recommendations, offer_details, behavior)
    except Exception as e:
        print(f"Error in legacy email generation: {e}")
        return {"subject": "We Miss You!", "body": "Complete your purchase today!"}

def suggest_offers(data):
    """Legacy function for offer suggestions."""
    return [{"type": "discount", "value": "10%", "description": "10% off your next purchase"}]