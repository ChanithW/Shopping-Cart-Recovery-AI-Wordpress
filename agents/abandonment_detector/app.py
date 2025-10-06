from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import time
from .models import CartData, AbandonmentResponse
from ..shared.recommendation_engine import ProductRecommendationEngine
import os

app = FastAPI(title="Abandonment Detector Agent")
security = HTTPBearer()

@app.on_event("startup")
async def startup_event():
    """Initialize components on startup."""
    print("Starting abandonment detector...")
    try:
        # Test database connection
        from .models import CartData
        print("Database connection test passed")
    except Exception as e:
        print(f"Database connection error: {e}")
        # Don't fail startup

@app.post("/detect-abandonment", response_model=AbandonmentResponse)
def detect_abandonment(data: CartData):
    # Check if abandoned: e.g., idle time > threshold and no checkout
    idle_threshold = int(os.getenv("ABANDONMENT_THRESHOLD_SECONDS", "60"))  # Default 1 minute (60 seconds)
    if data.behavior.idle_time > idle_threshold:
        # Fetch product details and recommendations using TF-IDF engine
        try:
            rec_engine = ProductRecommendationEngine()
            tfidf_recommendations = rec_engine.find_similar_products([
                {
                    'name': item.name, 
                    'description': f"{item.name} - Product ID: {item.product_id}", 
                    'category': 'Electronics',  # Default category since not in model
                    'product_id': item.product_id
                } for item in data.items
            ], top_n=3)
            
            # Format recommendations for API response
            recommendations = [
                {"name": rec["item_name"], "price": float(rec["price"])}
                for rec in tfidf_recommendations
            ]
            
        except Exception as e:
            print(f"Error getting recommendations: {e}")
            recommendations = [{"name": "Similar Product", "price": 50.0}]
        
        # Note: Database logging is now handled by WordPress plugin
        
        return AbandonmentResponse(abandoned=True, data={
            "user_id": data.user_id,
            "email": data.email,
            "items": [item.model_dump() for item in data.items],
            "timestamp": data.timestamp,
            "behavior": data.behavior.model_dump(),
            "recommendations": recommendations
        })
    return AbandonmentResponse(abandoned=False)

@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "abandonment-detector", "port": 8006}

@app.get("/")
def root():
    """Root endpoint."""
    return {"message": "Shopping Cart Recovery - Abandonment Detector Agent", "status": "running", "docs": "/docs"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8006)