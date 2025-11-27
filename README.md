# StayAssist Backend

A Django REST API for managing property rentals and bookings with JWT authentication.

## Tech Stack

### Core Framework
- **Django 5.2.8** - High-level Python web framework
- **Django REST Framework 3.16.1** - Powerful toolkit for building Web APIs
- **Python 3.12+** - Programming language

### Authentication & Authorization
- **djangorestframework-simplejwt 5.5.0** - JWT authentication for DRF
- **djoser 2.3.1** - REST implementation of Django auth system

### Database
- **PostgreSQL** (Production) - Recommended production database
- **SQLite** (Development) - Default development database
- **psycopg2-binary 2.9.10** - PostgreSQL adapter

### API & Documentation
- **drf-spectacular 0.28.0** - OpenAPI 3 schema generation
- **drf-standardized-errors 0.14.1** - Standardized error responses

### File Storage
- **Cloudinary 1.43.0** - Cloud-based image and video management
- **Pillow 11.3.0** - Python Imaging Library

### Security & CORS
- **django-cors-headers 4.7.0** - Handle Cross-Origin Resource Sharing
- **cryptography 46.0.3** - Cryptographic recipes and primitives

### Development & Deployment
- **django-debug-toolbar 5.1.0** - Debugging toolbar for development
- **gunicorn 23.0.0** - Python WSGI HTTP Server for production
- **whitenoise 6.11.0** - Static file serving for Python web apps
- **python-dotenv 1.1.0** - Environment variable management

### Utilities
- **requests 2.32.5** - HTTP library for Python
- **PyYAML 6.0.3** - YAML parser and emitter

## Setup Instructions

### Prerequisites
- Python 3.12+
- pip
- PostgreSQL (for production) or SQLite (for development)
- Cloudinary account (for image uploads)

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

Create a `.env.local` file in the root directory:

```env
# Django Settings
DJANGO_SECRET_KEY=your-secret-key-here
DEBUG=True
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost

# Database Configuration (SQLite for development)
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3

# Database Configuration (PostgreSQL for production)
# DB_ENGINE=django.db.backends.postgresql
# DB_NAME=your_database_name
# DB_USER=your_database_user
# DB_PASSWORD=your_database_password
# DB_HOST=your_database_host
# DB_PORT=5432

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

# Frontend URL (for CORS)
DOMAIN=localhost:3000

# Authentication
AUTH_COOKIE_SECURE=False  # Set to True in production with HTTPS
```

5. Run database migrations:
```bash
python3 manage.py migrate
```

6. Create a superuser (optional):
```bash
python3 manage.py createsuperuser
```

7. Collect static files (for production):
```bash
python3 manage.py collectstatic
```

8. Start the development server:
```bash
python3 manage.py runserver
```

The API will be available at `http://localhost:8000/api/`

### Available Commands

- `python3 manage.py runserver` - Start development server
- `python3 manage.py migrate` - Run database migrations
- `python3 manage.py makemigrations` - Create new migrations
- `python3 manage.py createsuperuser` - Create admin user
- `python3 manage.py collectstatic` - Collect static files for production
- `python3 manage.py shell` - Open Django shell

## Project Structure

```
stayassist-backend/
├── apps/
│   ├── accounts/              # User authentication & management
│   │   ├── models.py          # CustomUser model
│   │   ├── serializers.py     # User serializers
│   │   ├── views.py           # Auth views
│   │   ├── authentication.py  # Custom JWT authentication
│   │   └── urls.py            # Auth endpoints
│   └── stay/                  # Property listings & bookings
│       ├── models.py          # Listing, Booking models
│       ├── serializers.py     # Listing serializers
│       ├── views.py           # Listing views
│       └── urls.py            # Listing endpoints
├── commons/                   # Shared utilities
│   ├── exceptions.py          # Custom exception handlers
│   └── models.py              # Abstract base models
├── stayassist/
│   ├── settings/              # Split settings
│   │   ├── base.py            # Base settings
│   │   ├── dev.py             # Development settings
│   │   └── prod.py            # Production settings
│   ├── urls.py                # Main URL configuration
│   ├── wsgi.py                # WSGI configuration
│   └── asgi.py                # ASGI configuration
├── staticfiles/               # Collected static files
├── manage.py                  # Django management script
├── requirements.txt           # Python dependencies
└── .env.local                 # Environment variables
```

## API Endpoints

### Authentication
- `POST /api/accounts/register/` - User registration
- `POST /api/accounts/token/` - Login (returns JWT in httpOnly cookies)
- `POST /api/accounts/token/refresh/` - Refresh access token
- `POST /api/accounts/logout/` - Logout (clears cookies)
- `GET /api/accounts/me/` - Get current authenticated user

### Listings
- `GET /api/stay/listings/` - Get all available listings
  - Query params: `check_in`, `check_out` (for availability filtering)
- `GET /api/stay/listings/{id}/` - Get listing details
- `POST /api/stay/listings/` - Create listing (admin only)
- `PUT /api/stay/listings/{id}/` - Update listing (admin only)
- `DELETE /api/stay/listings/{id}/` - Delete listing (admin only)

### Bookings
- `GET /api/stay/bookings/` - Get user's bookings
- `POST /api/stay/bookings/` - Create a booking
- `GET /api/stay/bookings/{id}/` - Get booking details
- `DELETE /api/stay/bookings/{id}/` - Cancel booking

### API Documentation
- `GET /api/schema/` - OpenAPI schema (JSON)
- `GET /api/schema/swagger-ui/` - Swagger UI documentation
- `GET /api/schema/redoc/` - ReDoc documentation

## Architecture Decisions

### 1. JWT Authentication with Cookies
- **httpOnly cookies** prevent XSS attacks by making tokens inaccessible to JavaScript
- **Access tokens** (5 minutes) minimize damage if compromised
- **Refresh tokens** (1 day) reduce need for frequent re-authentication
- **Custom authentication class** handles cookie-based JWT extraction

### 2. Split Settings Configuration
- **base.py**: Common settings for all environments
- **dev.py**: Development-specific settings (DEBUG=True, debug toolbar)
- **prod.py**: Production settings (DEBUG=False, security headers)
- Environment-specific settings loaded via `DJANGO_SETTINGS_MODULE`

### 3. App Organization
- **accounts**: Authentication, user management, custom user model
- **stay**: Business logic for listings and bookings
- **commons**: Shared utilities, base models, exception handlers
- Apps are registered in `apps/` directory for cleaner imports

### 4. Custom Exception Handling
- Centralized exception handler in `commons/exceptions.py`
- Standardized error response format across all endpoints
- Consistent error codes and messages

### 5. Image Storage Strategy
- **Cloudinary** for scalable cloud storage
- Automatic image optimization and transformation
- CDN delivery for fast loading

### 6. CORS Configuration
- Configured for specific frontend origins
- Credentials allowed for cookie-based auth
- Secure in production with HTTPS-only cookies

### 7. Static Files Handling
- **WhiteNoise** for efficient static file serving
- Compressed manifest storage for caching
- Collected to `staticfiles/` directory

## Known Limitations

### Authentication & Security
1. **Short access token lifetime (5 minutes)** - May cause frequent re-authentication if user is inactive
2. **No token blacklisting** - Logout only clears cookies, tokens remain valid until expiration
3. **No multi-device session tracking** - Cannot view or revoke sessions from other devices
4. **No rate limiting** - API endpoints not protected from brute force attacks
5. **No email verification** - Users can register without verifying email
6. **No password strength validation** - Only Django's default validators
7. **No two-factor authentication** - Single factor (password) only
8. **CORS allows all origins** - `CORS_ALLOW_ALL_ORIGINS = True` is insecure for production
9. **Hardcoded email credentials** - Email credentials in settings.py (line 259-260)

### Database & Performance
10. **No database connection pooling** - Each request creates new connection
11. **No caching layer** - Redis or Memcached not implemented
12. **No database read replicas** - All queries hit primary database
13. **N+1 query problems** - Listings with images may have inefficient queries
14. **No pagination on listings** - Returns all listings in single response
15. **No database indexes** - Missing indexes on frequently queried fields (city, price_per_night)

### API & Data Validation
16. **No API versioning** - Breaking changes would affect all clients
17. **No request throttling** - No protection against API abuse
18. **Limited input validation** - Some fields lack proper validation (e.g., price ranges)
19. **No soft deletes** - Deleted data is permanently removed
20. **No audit trail** - No tracking of who created/modified records

### Features
21. **No payment integration** - Bookings created without payment processing
22. **No booking confirmation emails** - No automated email notifications
23. **No booking status management** - Cannot mark bookings as confirmed/cancelled/completed
24. **No availability calendar** - Availability checking is basic date range comparison
25. **No double-booking prevention** - Race condition possible on concurrent bookings
26. **No review system** - Cannot leave or view property reviews
27. **No host/guest messaging** - No communication between users
28. **No cancellation policy** - No refund or cancellation rules
29. **No search functionality** - Only basic filtering by dates
30. **No property amenities** - Cannot filter by WiFi, parking, etc.

### File Management
31. **No file upload size limits** - Large images could overwhelm storage
32. **No file type validation** - Could upload non-image files
33. **No image compression** - Original images stored without optimization
34. **Cloudinary credentials hardcoded** - Stored in settings instead of secure vault

### Admin & Management
35. **No admin dashboard analytics** - Cannot view booking statistics
36. **No bulk operations** - Cannot bulk delete or update listings
37. **Limited admin permissions** - Basic admin interface only

### Testing & Documentation
38. **No unit tests** - No automated testing
39. **No integration tests** - Endpoints not tested
40. **No API client examples** - Documentation lacks code samples
41. **No Postman collection** - No pre-configured API requests

### Deployment & Operations
42. **SQLite in production** - Not recommended for concurrent writes
43. **No health check endpoint** - Cannot monitor service status
44. **No logging configuration** - Limited error tracking in production
45. **No monitoring or alerting** - No Sentry or similar integration
46. **No backup strategy** - Database backups not automated
47. **No CI/CD pipeline** - Manual deployment process
48. **No database migrations rollback plan** - No easy way to revert migrations
49. **Static files in repository** - `staticfiles/` should be gitignored

### Code Quality
50. **Debug toolbar in production** - Should be disabled based on DEBUG flag
51. **Settings in base.py** - Some production settings mixed with base settings
52. **No type hints** - Python code lacks type annotations

## Production Deployment

The backend is deployed on Render:

### Environment Variables (Production)
```env
DJANGO_SECRET_KEY=<strong-secret-key>
DEBUG=False
DJANGO_ALLOWED_HOSTS=your-domain.onrender.com
DB_ENGINE=django.db.backends.postgresql
DB_NAME=<postgres-db-name>
DB_USER=<postgres-user>
DB_PASSWORD=<postgres-password>
DB_HOST=<postgres-host>
DB_PORT=5432
AUTH_COOKIE_SECURE=True
CLOUD_NAME=<cloudinary-cloud-name>
CLOUD_API_KEY=<cloudinary-api-key>
CLOUD_SECRET_KEY=<cloudinary-secret-key>
```

### Deployment Steps
1. Set `DEBUG=False` in production environment
2. Update `DJANGO_ALLOWED_HOSTS` with your domain
3. Set `AUTH_COOKIE_SECURE=True` (requires HTTPS)
4. Configure PostgreSQL database
5. Set up Cloudinary for image storage
6. Run migrations: `python3 manage.py migrate`
7. Collect static files: `python3 manage.py collectstatic --noinput`
8. Start with Gunicorn: `gunicorn stayassist.wsgi:application`

### Security Checklist
- [ ] Set strong `DJANGO_SECRET_KEY`
- [ ] Set `DEBUG=False`
- [ ] Configure `ALLOWED_HOSTS` with actual domain
- [ ] Enable `AUTH_COOKIE_SECURE=True`
- [ ] Use PostgreSQL instead of SQLite
- [ ] Configure proper CORS origins (remove `CORS_ALLOW_ALL_ORIGINS`)
- [ ] Set up HTTPS/SSL
- [ ] Configure security headers
- [ ] Remove hardcoded credentials

## Contributing

1. Create feature branches from `main`
2. Follow Django best practices and PEP 8
3. Add docstrings to functions and classes
4. Update API documentation for endpoint changes
5. Test authentication flows thoroughly

## License

Proprietary
