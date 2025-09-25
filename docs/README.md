# Shopping Cart Recovery AI

This project implements a Shopping Cart Recovery AI system with agents for detecting abandonment, generating personalized emails, and suggesting offers, integrated with WordPress/WooCommerce.

## Architecture

- **Agents**: Python microservices using FastAPI.
  - Abandonment Detector: Detects abandoned carts.
  - Email Generator & Offer Suggestor: Crafts emails with offers.
- **Shared**: Common utilities (Gemini client, DB, utils).
- **WordPress Plugin**: Integrates with WooCommerce for tracking and API calls.
- **Communication**: REST APIs with JWT auth.

## Setup

1. Clone repo.
2. Install dependencies: `pip install -r agents/abandonment_detector/requirements.txt` etc.
3. Set up .env from .env.example.
4. Run agents: `uvicorn agents.abandonment_detector.app:app --port 8001`
5. Install WP plugin in wp-content/plugins/.
6. Configure WP options for API token.

## Deployment

Use Docker: `docker-compose up` in docker/ dir.

## End-to-End Flow

1. User adds to cart → WP tracks.
2. On inactivity → Detector API called → If abandoned → Email API called → Send email.
3. Analytics logged for feedback.

## Security

- Encrypt sensitive data.
- Use HTTPS.
- Sanitize inputs.

## Testing

Run agents locally, test APIs with Postman.