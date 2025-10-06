from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .models import EmailData, GeneratedEmail, Offer
from ..shared.gemini_client import PersonalizedEmailGenerator
from ..shared.offer_calculator import OfferCalculator
from ..shared.recommendation_engine import ProductRecommendationEngine
from ..shared.utils import apply_business_rules
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import logging

app = FastAPI(title="Email Generator & Offer Suggestor Agent")
security = HTTPBearer()
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "templates"))

# Initialize enhanced components (moved to startup event to avoid global init issues)
email_generator = None
offer_calculator = None
recommendation_engine = None

@app.on_event("startup")
async def startup_event():
    """Initialize components on startup."""
    global email_generator, offer_calculator, recommendation_engine
    
    try:
        print("Initializing email generator...")
        
        # Initialize components
        email_generator = PersonalizedEmailGenerator()
        offer_calculator = OfferCalculator()
        recommendation_engine = ProductRecommendationEngine()
        
        products = recommendation_engine.load_products()
        print(f"Email generator service started successfully - loaded {len(products)} products")
    except Exception as e:
        print(f"Warning: Failed to initialize recommendation engine: {e}. Service will continue with limited functionality.")
        # Don't fail startup - the service can still work with fallback recommendations

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials.credentials != os.getenv("API_TOKEN"):
        raise HTTPException(status_code=401, detail="Invalid token")

@app.post("/generate-email", response_model=GeneratedEmail)
def generate_email(data: EmailData, token: str = Depends(verify_token)):
    """Generate personalized recovery email with dynamic offers and recommendations."""
    try:
        # Check if components are initialized
        if not all([email_generator, offer_calculator, recommendation_engine]):
            raise Exception("Service components not properly initialized")
        
        # Calculate dynamic offers based on cart value
        offer_details = offer_calculator.generate_offer_details(data.items)
        
        # Get personalized product recommendations using TF-IDF
        recommendations = recommendation_engine.find_similar_products(data.items, top_n=5)
        
        # Generate personalized email content using Gemini LLM
        email_content = email_generator.generate_email_content(
            customer_name=data.name,
            cart_items=data.items,
            recommendations=recommendations,
            offer_details=offer_details,
            behavior=data.behavior if hasattr(data, 'behavior') else {}
        )
        
        # Format offers for response
        formatted_offers = []
        if offer_details["discount"]["discount_percent"] > 0:
            formatted_offers.append(Offer(
                type="discount",
                value=f"{offer_details['discount']['discount_percent']}%",
                description=offer_details["discount"]["label"]
            ))
        
        if offer_details["free_shipping"]["available"]:
            formatted_offers.append(Offer(
                type="shipping",
                value="free",
                description=offer_details["free_shipping"]["message"]
            ))
        
        # Apply any additional business rules
        final_offers = apply_business_rules(formatted_offers, data.persona)
        
        # Use the enhanced email content directly (it's already HTML formatted)
        subject = email_content["subject"]
        body = email_content["body"]
        
        # Optionally send email if configured
        if os.getenv("SEND_EMAIL_DIRECTLY", "false").lower() == "true":
            try:
                email_sent = send_email(data.email, subject, body)
                if email_sent:
                    logging.info(f"Recovery email sent successfully to {data.email}")
                else:
                    logging.warning(f"Failed to send recovery email to {data.email}")
            except Exception as e:
                logging.error(f"Error sending email to {data.email}: {e}")
                # Don't fail the request if email sending fails
        
        return GeneratedEmail(
            subject=subject, 
            body=body, 
            offers=final_offers,
            recommendations=[
                f"{rec['item_name']} - ${rec['price']:.2f}" 
                for rec in recommendations[:3]
            ],
            total_savings=float(offer_details["total_savings"]),
            final_amount=float(offer_details["final_amount"])
        )
        
    except Exception as e:
        error_msg = str(e)
        logging.error(f"Error generating email: {error_msg}")
        
        # Check if it's a quota issue
        if "429" in error_msg or "quota" in error_msg.lower() or "rate limit" in error_msg.lower():
            logging.warning("Gemini API quota exceeded - using enhanced fallback template")
        
        # Enhanced fallback with basic recommendations
        try:
            basic_recommendations = recommendation_engine.find_similar_products(data.items, top_n=3) if recommendation_engine else []
        except:
            basic_recommendations = []
        
        # Create a more comprehensive fallback email
        cart_items_text = ", ".join([item.get('name', 'item') for item in data.items])
        fallback_subject = f"Complete Your Purchase - {cart_items_text}"
        
        recommendations_html = ""
        if basic_recommendations:
            recommendations_html = "<h3>You might also like:</h3><ul>" + "".join([f"<li>{rec.get('item_name', 'Product')}</li>" for rec in basic_recommendations[:3]]) + "</ul>"
        
        fallback_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
            <h2>Hello {data.name or 'Valued Customer'}!</h2>
            <p>We noticed you were interested in: <strong>{cart_items_text}</strong></p>
            <p>Don't miss out on completing your purchase! We have some great offers waiting for you.</p>
            
            <div style="background-color: #f0f8ff; padding: 15px; border-radius: 8px; margin: 20px 0;">
                <h3>🎁 Special Offer: Free Shipping!</h3>
                <p>Get free shipping on your order when you complete your purchase today.</p>
            </div>
            
            {recommendations_html}
            
            <div style="text-align: center; margin: 30px 0;">
                <a href="#" style="background-color: #007bff; color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px; display: inline-block;">
                    Complete Your Purchase Now
                </a>
            </div>
            
            <p style="color: #666; font-size: 12px;">This email was sent because you have items in your shopping cart.</p>
        </body>
        </html>
        """
        
        return GeneratedEmail(
            subject=fallback_subject,
            body=fallback_body,
            offers=[Offer(type="shipping", value="free", description="Free shipping on all orders")],
            recommendations=[f"{rec.get('item_name', 'Product')} - ${rec.get('price', 0):.2f}" for rec in basic_recommendations[:3]],
            total_savings=0.0,
            final_amount=sum(item.get('price', 0) * item.get('quantity', 1) for item in data.items)
        )

def send_email(to_email: str, subject: str, body: str):
    try:
        msg = MIMEMultipart()
        msg['From'] = os.getenv("SMTP_FROM")
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'html'))

        server = smtplib.SMTP(os.getenv("SMTP_SERVER"), int(os.getenv("SMTP_PORT")))
        server.starttls()
        server.login(os.getenv("SMTP_USER"), os.getenv("SMTP_PASS"))
        server.sendmail(msg['From'], to_email, msg.as_string())
        server.quit()
        logging.info(f"Email sent successfully to {to_email}")
        return True
    except Exception as e:
        logging.error(f"Failed to send email to {to_email}: {e}")
        return False

@app.get("/track-open")
def track_open(user_id: str, email: str):
    # Note: Tracking is now handled by WordPress plugin
    return {"status": "tracked"}

@app.get("/track-click")
def track_click(user_id: str, email: str):
    # Note: Tracking is now handled by WordPress plugin
    return {"status": "tracked"}

@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "email-generator", "port": 8002}

@app.get("/")
def root():
    """Root endpoint."""
    return {"message": "Shopping Cart Recovery - Email Generator Agent", "status": "running", "docs": "/docs"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)