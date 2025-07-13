# Email Service API

This is a FastAPI-based email sending service designed to handle contact form submissions from multiple client websites. It supports dynamic recipient routing, reCAPTCHA verification, and multiple email providers (SendGrid and AWS SES).

---

## Features

- Dynamic routing of emails to different client recipients based on `client_id`  
- Support for SendGrid and AWS SES email providers (configurable via environment variables)  
- Google reCAPTCHA v2 Invisible verification to prevent spam  
- CORS support configurable for local development and production  
- HTML and plain-text email templates using Jinja2  
- Reply-To header set to the user’s email for easy client replies  

---

## Setup

### Prerequisites

- Python 3.9+  
- SendGrid or AWS SES account with verified sender email/domain  
- Google reCAPTCHA v2 Invisible site key and secret key  
- Environment variables configured (see `.env.example`)  

### Installation

1. Clone this repository:

   ```
   git clone https://github.com/yourusername/email-service.git
   cd email-service
   ```
2. Create and activate a virtual environment:

        python3 -m venv venv
        source venv/bin/activate  # On Windows: .\venv\Scripts\activate


3. Install dependencies:
    ```
    pip install -r requirements.txt
    ```
4. Copy `.env.example` to `.env` and fill in your credentials:

    ```
    cp .env.example .env
    ```
    
5. Customize the `CLIENT_EMAIL_MAP` in `send_email.py` to map your client IDs to their recipient emails.


### Running Locally
Start the FastAPI server with:

```
uvicorn api.send_email:app --reload
```
The API docs are available at:
http://127.0.0.1:8000/docs


### Environment Variables
| Variable                 | Description                                      | Example                                    |
| ------------------------ | ------------------------------------------------ | ------------------------------------------ |
| SENDGRID\_API\_KEY       | API key for SendGrid                             | `SG.xxxxxxx`                               |
| AWS\_ACCESS\_KEY\_ID     | AWS access key ID for SES                        | `AKIAxxxxxx`                               |
| AWS\_SECRET\_ACCESS\_KEY | AWS secret access key for SES                    | `xxxxxxxxx`                                |
| AWS\_REGION              | AWS region for SES                               | `us-east-1`                                |
| FROM\_EMAIL              | Verified sender email (agency email)             | `no-reply@example.co`                      |
| RECAPTCHA\_SECRET        | Google reCAPTCHA secret key                      | `6Lcxxxxxx`                                |
| EMAIL\_PROVIDER          | Email provider to use (`sendgrid` or `ses`)      | `sendgrid`                                 |
| ALLOWED\_ORIGINS         | Comma-separated list of allowed CORS origins     | `http://localhost:5500,https://client.com` |

### Usage
Send a POST request to /send-email with JSON body:

```
{
  "client_id": "ClientA",
  "name": "John Doe",
  "email": "john@example.com",
  "message": "Hello from client!",
  "recaptcha_token": "token_from_recaptcha"
}
```
### Notes
- Make sure to serve your frontend from an allowed origin to avoid CORS issues.

- Verify your sending domains/emails in SendGrid or AWS SES before sending emails.

- For Google reCAPTCHA, use Invisible v2 keys and ensure tokens are generated and validated correctly.