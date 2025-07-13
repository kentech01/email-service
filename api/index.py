from .send_email import app  # Import your FastAPI app instance

from mangum import Mangum  # Adapter for ASGI apps to AWS Lambda-like environments (works on Vercel)

handler = Mangum(app)