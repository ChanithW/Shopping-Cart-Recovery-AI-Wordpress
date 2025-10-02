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

# Initialize enhanced components
email_generator = PersonalizedEmailGenerator()
offer_calculator = OfferCalculator()
recommendation_engine = ProductRecommendationEngine()

@app.on_event("startup")
async def startup_event():
    """Initialize components on startup."""
    try:
        recommendation_engine.load_products()
        logging.info("Email generator service started successfully")
    except Exception as e:
        logging.error(f"Failed to initialize recommendation engine: {e}")

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials.credentials != os.getenv("API_TOKEN"):
        raise HTTPException(status_code=401, detail="Invalid token")

@app.post("/generate-email", response_model=GeneratedEmail)
def generate_email(data: EmailData, token: str = Depends(verify_token)):
    """Generate personalized recovery email with dynamic offers and recommendations."""
    try:
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
            send_email(data.email, subject, body)
        
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
        logging.error(f"Error generating email: {str(e)}")
        # Fallback to basic email
        return GeneratedEmail(
            subject="Complete Your Purchase - Special Offer!",
            body="<p>We noticed you left some items in your cart. Complete your purchase today!</p>",
            offers=[Offer(type="shipping", value="free", description="Free shipping on all orders")],
            recommendations=[],
            total_savings=0.0,
            final_amount=0.0
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
        print(f"Email sent successfully to {to_email}")
    except Exception as e:
        print(f"Failed to send email to {to_email}: {e}")
        # Don't raise exception - just log the error for now

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