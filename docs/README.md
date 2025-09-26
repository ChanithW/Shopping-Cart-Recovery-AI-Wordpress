# Shopping Cart Recovery AI

This project implements an intelligent Shopping Cart Recovery AI system designed to detect abandoned shopping carts, generate personalized recovery emails with tailored offers, and integrate seamlessly with WordPress/WooCommerce. The system uses AI-powered agents to analyze user behavior and provide targeted recovery strategies to reduce cart abandonment and increase conversions.

## Features

- **Real-time Cart Tracking**: Monitors user interactions on WooCommerce sites.
- **AI-Powered Abandonment Detection**: Uses machine learning to determine if a cart is likely abandoned based on behavior patterns.
- **Personalized Email Generation**: Crafts customized recovery emails with product recommendations and special offers.
- **Analytics Dashboard**: Provides insights into abandonment rates, recovery success, and user behavior.
- **RESTful API**: Secure communication between WordPress plugin and Python agents.
- **Docker Support**: Easy deployment with containerization.

## Architecture

The system is built with a microservices architecture:

### Components

- **WordPress Plugin** (`wordpress_plugin/`):
  - Integrates with WooCommerce hooks for cart tracking.
  - Handles user behavior data collection (page views, idle time, session duration).
  - Makes API calls to Python agents for abandonment detection and email generation.
  - Logs recovery data to WordPress database for analytics.

- **Python Agents** (`agents/`):
  - **Abandonment Detector** (`agents/abandonment_detector/`): FastAPI service that analyzes cart data and user behavior to detect abandonment.
  - **Email Generator & Offer Suggestor** (`agents/email_generator_offer_suggestor/`): FastAPI service that creates personalized emails with AI-generated offers and recommendations.

- **Shared Utilities** (`agents/shared/`):
  - `gemini_client.py`: Interface for Google Gemini AI API for content generation.
  - `db.py`: Database connection utilities.
  - `utils.py`: Common helper functions.

- **Docker Setup** (`docker/`):
  - `docker-compose.yml`: Orchestrates all services.
  - `Dockerfile.detector` and `Dockerfile.email`: Build files for agent containers.

### AI and NLP Integration

- **Large Language Models (LLMs)**:
  - Uses Google Gemini AI for personalized email content generation (subject lines, body text, offers).
  - Processes user data (cart items, behavior) to tailor messages based on personas.
  - Integrated via `gemini_client.py` wrapper for API handling.

- **Natural Language Processing (NLP)**:
  - Analyzes user behavior and product descriptions for personalization (e.g., keyword extraction, recommendations).
  - Crafts context-aware emails with semantic similarity and tone adjustment.
  - Supports potential multilingual generation.

- **AI Workflow**: Data collection → LLM processing → NLP refinement → Email generation.

### Data Flow

1. User browses WooCommerce site → JavaScript tracks behavior.
2. User adds items to cart → WordPress plugin initiates tracking.
3. On cart updates or periodic checks → Plugin calls Abandonment Detector API.
4. If abandoned → Plugin calls Email Generator API.
5. Personalized email sent to user.
6. Recovery events (opens, clicks, conversions) tracked and logged.

### Database Schema

The system uses WordPress's database with additional tables:

- `wp_cart_logs`: Stores abandonment events, email sends, and recovery metrics.
  - `id` (int, primary key)
  - `user_id` (varchar)
  - `email` (varchar)
  - `items` (text, JSON)
  - `timestamp` (datetime)
  - `abandoned` (tinyint)
  - `email_sent` (tinyint)
  - `opened` (tinyint)
  - `clicked` (tinyint)
  - `converted` (tinyint)

## Prerequisites

- **WordPress** 5.0+ with **WooCommerce** 4.0+
- **Python** 3.8+
- **Docker** and **Docker Compose** (for containerized deployment)
- **Google Gemini API** key for AI features
- **MySQL/MariaDB** (via WordPress)

## Installation

### Local Development Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/kusal2002/Shopping-Cart-Recovery-AI-Wordpress.git
   cd Shopping-Cart-Recovery-AI-Wordpress
   ```

2. **Set Up Python Environment**:
   ```bash
   # Install dependencies for each agent
   pip install -r agents/abandonment_detector/requirements.txt
   pip install -r agents/email_generator_offer_suggestor/requirements.txt
   ```

3. **Configure Environment Variables**:
   - Copy `.env.example` to `.env`
   - Set your Google Gemini API key: `GEMINI_API_KEY=your_key_here`
   - Set API token: `API_TOKEN=your_secure_token`

4. **Install WordPress Plugin**:
   - Copy `wordpress_plugin/` to your WordPress `wp-content/plugins/` directory
   - Activate the "Shopping Cart Recovery AI" plugin in WordPress admin
   - Go to WooCommerce > Settings > Cart Recovery to configure API endpoints and token

5. **Run the Agents**:
   ```bash
   # Abandonment Detector
   python -m agents.abandonment_detector.app

   # Email Generator
   python -m agents.email_generator_offer_suggestor.app
   ```

6. **Test the System**:
   - Add items to cart on your WooCommerce site
   - Wait for abandonment detection (or use test scripts)
   - Check email delivery and analytics

### Docker Deployment

1. **Build and Run**:
   ```bash
   cd docker
   docker-compose up --build
   ```

2. **Access Services**:
   - WordPress: `http://localhost:8080`
   - Abandonment Detector API: `http://localhost:8001`
   - Email Generator API: `http://localhost:8002`

## Configuration

### WordPress Plugin Settings

- **API Token**: Secure token for authenticating API calls (set in wp-admin)
- **Detector API URL**: `http://localhost:8005/detect-abandonment`
- **Email API URL**: `http://localhost:8002/generate-email`
- **Abandonment Thresholds**: Customize detection parameters

### Agent Configuration

- **Gemini API Key**: Required for AI-powered content generation
- **Database Connection**: Configure MySQL credentials in agents/shared/db.py
- **Email Templates**: Customize in agents/email_generator_offer_suggestor/templates/

## API Documentation

### Abandonment Detector API

**Endpoint**: `POST /detect-abandonment`

**Request Body**:
```json
{
  "user_id": "string",
  "email": "user@example.com",
  "items": [
    {
      "product_id": 123,
      "name": "Product Name",
      "price": 29.99,
      "quantity": 1
    }
  ],
  "timestamp": 1638360000.0,
  "behavior": {
    "pages_viewed": 5,
    "idle_time": 120,
    "session_duration": 600
  }
}
```

**Response**:
```json
{
  "abandoned": true,
  "data": {
    "items": [...],
    "recommendations": ["Recommended Product 1", "Recommended Product 2"],
    "behavior": {...}
  }
}
```

### Email Generator API

**Endpoint**: `POST /generate-email`

**Request Body**:
```json
{
  "user_id": "string",
  "email": "user@example.com",
  "name": "John Doe",
  "items": [...],
  "recommendations": [...],
  "behavior": {...},
  "persona": "loyal"
}
```

**Response**:
```json
{
  "subject": "We Miss You! Your Cart is Waiting",
  "body": "<html>Personalized email content...</html>",
  "offers": ["10% off", "Free shipping"]
}
```

## Testing

### Unit Tests

Run Python tests:
```bash
pytest agents/
```

### Integration Testing

1. Use `test_scr_manual.php` to simulate cart abandonment
2. Check WordPress logs for API calls
3. Verify email delivery
4. Review database entries in `wp_cart_logs`

### API Testing

Use tools like Postman or curl to test endpoints:
```bash
curl -X POST http://localhost:8005/detect-abandonment \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d @test_payload.json
```

## Security Considerations

- **API Authentication**: JWT tokens for secure communication
- **Data Encryption**: Sensitive data encrypted in transit and at rest
- **Input Validation**: All inputs sanitized to prevent injection attacks
- **Rate Limiting**: Implemented on API endpoints to prevent abuse
- **HTTPS**: Always use secure connections in production

## Troubleshooting

### Common Issues

1. **Agents Not Starting**: Check Python version and dependencies
2. **API Connection Failed**: Verify ports and firewall settings
3. **Emails Not Sending**: Check email configuration in WordPress
4. **Database Errors**: Ensure WordPress DB permissions

### Logs

- WordPress: `wp-content/debug.log`
- Agents: Console output or configure logging to files

### Performance Tuning

- Adjust abandonment check intervals in `api_handler.php`
- Optimize database queries
- Use caching for frequent API calls

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

### Development Guidelines

- Follow PEP 8 for Python code
- Use WordPress coding standards for PHP
- Write comprehensive tests
- Update documentation

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please open an issue on GitHub or contact the maintainers.

---

**Note**: This system requires active Google Gemini API access for AI features. Ensure your API key has sufficient quota for production use.