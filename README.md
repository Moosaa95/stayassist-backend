# StayAssist Backend

A Django REST API for managing property rentals and bookings.

## Tech Stack

- Django 5.2.8
- Django REST Framework 3.16
- SimpleJWT for authentication
- Cloudinary for image storage
- SQLite (development) / PostgreSQL (production ready)

## Getting Started

### Prerequisites

- Python 3.12+
- pip

### Installation

1. Clone the repository and navigate to the backend directory:
```bash
cd stayassist-backend
```

2. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:

Create a `.env.local` file in the root directory with the following:

```env
# Django Settings
DJANGO_SECRET_KEY=your-secret-key
DEBUG=True
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost

# Email Configuration (Mailgun example)
EMAIL_HOST=smtp.mailgun.org
EMAIL_HOST_USER=your-mailgun-username
EMAIL_HOST_PASSWORD=your-mailgun-password
EMAIL_PORT=587
EMAIL_USE_TLS=True

# Cloudinary (for image uploads)
CLOUD_NAME=your-cloudinary-cloud-name
CLOUD_API_KEY=your-cloudinary-api-key
CLOUD_SECRET_KEY=your-cloudinary-secret-key

# Frontend URL
DOMAIN=localhost:5173

# Authentication
AUTH_COOKIE_SECURE=False  # Set to True in production with HTTPS

# OAuth (optional)
GOOGLE_AUTH_KEY=your-google-client-id
GOOGLE_AUTH_SECRET_KEY=your-google-client-secret
```

5. Run migrations:
```bash
python3 manage.py migrate
```

6. Create a superuser (optional):
```bash
python3 manage.py createsuperuser
```

7. Start the development server:
```bash
python3 manage.py runserver
```

The API will be available at `http://localhost:8000/api/`

## Project Structure

```
stayassist-backend/
├── apps/
│   ├── accounts/       # User authentication and management
│   └── stay/          # Property listings and bookings
├── stayassist/
│   └── settings/      # Settings (base, dev, prod)
├── commons/           # Shared utilities and mixins
└── manage.py
```

## API Endpoints

### Authentication
- `POST /api/accounts/register/` - User registration
- `POST /api/accounts/token/` - Login (get tokens)
- `POST /api/accounts/token/refresh/` - Refresh access token
- `POST /api/accounts/logout/` - Logout
- `GET /api/accounts/me/` - Get current user

### Listings
- `GET /api/stay/listings/` - Get all listings
- `GET /api/stay/listings/{id}/` - Get listing details
- `POST /api/stay/listings/` - Create listing (admin only)

### Bookings
- `GET /api/stay/bookings/` - Get user bookings
- `POST /api/stay/bookings/` - Create a booking

## Authentication

This API uses JWT (JSON Web Tokens) with cookie-based authentication:
- Access tokens expire after 15 minutes
- Refresh tokens expire after 7 days
- Tokens are stored in HTTP-only cookies for security

## Development Notes

- Debug toolbar is enabled in development mode
- CORS is configured to allow requests from `http://localhost:5173`
- API documentation is available at `/api/schema/swagger-ui/`

## Deployment

For production deployment:
1. Set `DEBUG=False` in environment variables
2. Update `DJANGO_ALLOWED_HOSTS` with your domain
3. Set `AUTH_COOKIE_SECURE=True` (requires HTTPS)
4. Use a production database (PostgreSQL recommended)
5. Configure proper email backend
6. Collect static files: `python3 manage.py collectstatic`

## License

Proprietary
