import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini API
api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        print("Gemini API configured successfully")
    except Exception as e:
        print(f"Failed to configure Gemini API: {e}")
        model = None
else:
    print("GEMINI_API_KEY not found in environment")
    model = None

def get_product_recommendations(items):
    if not model:
        return [{"name": "Gemini API not configured", "price": 0.0}]

    try:
        prompt = f"Based on these cart items: {[item.name for item in items]}, suggest 3 related products with prices. Format as: Product Name - $Price"
        response = model.generate_content(prompt)
        recommendations = []
        if response.text:
            lines = response.text.split('\n')[:3]
            for line in lines:
                if line.strip():
                    # Try to parse "Product Name - $Price" format
                    if ' - $' in line:
                        parts = line.split(' - $', 1)
                        name = parts[0].strip()
                        try:
                            price = float(parts[1].strip())
                        except ValueError:
                            price = 0.0
                    else:
                        name = line.strip()
                        price = 0.0
                    recommendations.append({"name": name, "price": price})
        return recommendations if recommendations else [{"name": "No recommendations available", "price": 0.0}]
    except Exception as e:
        print(f"Gemini API error: {e}")
        return [{"name": "Unable to fetch recommendations", "price": 0.0}]

def generate_email_content(data):
    if not model:
        return {"subject": "We Miss You!", "body": "We noticed you left some items in your cart. Come back and complete your purchase!"}

    try:
        prompt = f"Generate a personalized recovery email for user {data.name or 'customer'} with abandoned items: {[item['name'] for item in data.items]}. Persona: {data.persona}. Include subject and body."
        response = model.generate_content(prompt)
        # Assume response is "Subject: ...\nBody: ..."
        lines = response.text.split('\n')
        subject = "We Miss You!"
        body = response.text
        for line in lines:
            if line.startswith("Subject:"):
                subject = line.replace("Subject:", "").strip()
            elif line.startswith("Body:"):
                body = line.replace("Body:", "").strip()
        return {"subject": subject, "body": body}
    except Exception as e:
        print(f"Gemini API error: {e}")
        return {"subject": "We Miss You!", "body": "We noticed you left some items in your cart. Come back and complete your purchase!"}
        print(f"Gemini API error: {e}")
        return {"subject": "We Miss You!", "body": "Please complete your purchase."}

def suggest_offers(data):
    try:
        prompt = f"Suggest offers for abandoned cart with items: {[item['name'] for item in data.items]}. Persona: {data.persona}."
        response = model.generate_content(prompt)
        # Parse into list
        return [{"type": "discount", "value": "10%", "description": "10% off your next purchase"}]
    except Exception as e:
        print(f"Gemini API error: {e}")
        return [{"type": "discount", "value": "10%", "description": "10% off"}]