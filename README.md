Event Management API — README & Migration Plan

Overview

The Event Management API is a backend application built with Django REST Framework that allows users to manage
events, categories, ticket pricing, and registrations. This implementation merges ALX's required features with
additional real-world functionality like waitlists, notifications, comments, and recurring events. The API follows RESTful
principles with JWT-based authentication and strict permission control.


Migration Plan
1. Initialize Django project & app structure.
2. Install dependencies: Django, DRF, SimpleJWT, django-filter.
3. Configure settings.py for database, REST framework, JWT auth.
4. Define models: User, Category, Event, TicketType, Registration, WaitlistEntry, Comment, Notification.
5. Create migrations (`python manage.py makemigrations`).
6. Apply migrations (`python manage.py migrate`).
7. Register models in admin.py for admin interface management.
8. Create serializers for each model with validation logic.
9. Implement viewsets/endpoints with appropriate permissions.
10. Add filtering, pagination, and search in views.
11. Test endpoints with pytest or Django test client.
12. Seed initial data (categories, admin user).
13. Deploy to production environment (Heroku/PythonAnywhere).


## Features
- **User Authentication & Profile**
  - JWT login, logout, register, refresh
  - View and update own profile
  - Admin can view all users

- **Event Management**
  - CRUD for events
  - Only event creators or admins can update/delete
  - Prevent creating events in the past
  - Capacity management (prevent overbooking)

- **Event Categories**
  - CRUD for categories (admin only for create/update/delete)
  
- **Ticket Pricing**
  - CRUD for ticket options per event
  
- **Registrations**
  - Register for events
  - View own registrations
  - Admins and creators can view/manage event registrations

## API Endpoints

### 1. Authentication & Profile
- `POST /auth/register/` — Register a new user
- `POST /auth/login/` — Obtain JWT token
- `POST /auth/logout/` — Logout (blacklist token)
- `POST /auth/refresh/` — Refresh access token
- `GET /users/me/` — Get current user profile
- `PUT /users/me/` — Update current user profile
- `GET /users/{id}/` — Admin get user by ID
- `GET /users/` — Admin list all users

### 2. Event Categories
- `GET /categories/` — List categories
- `POST /categories/` — Create category (admin only)
- `GET /categories/{id}/` — Retrieve category
- `PUT /categories/{id}/` — Update category (admin only)
- `DELETE /categories/{id}/` — Delete category (admin only)

### 3. Events
- `GET /events/` — List all events (filters: category, date)
- `POST /events/` — Create event (auth required)
- `GET /events/{id}/` — Retrieve event details
- `PUT /events/{id}/` — Update (creator/admin only)
- `DELETE /events/{id}/` — Delete (creator/admin only)

### 4. Ticket Pricing
- `GET /events/{event_id}/tickets/` — List tickets for event
- `POST /events/{event_id}/tickets/` — Create ticket (creator/admin)
- `GET /tickets/{id}/` — Get ticket details
- `PUT /tickets/{id}/` — Update (creator/admin)
- `DELETE /tickets/{id}/` — Delete (creator/admin)

### 5. Registrations
- `GET /registrations/` — List own registrations
- `POST /events/{event_id}/register/` — Register for event
- `GET /events/{event_id}/registrations/` — View registrations for event (creator/admin)
- `PUT /registrations/{id}/` — Update status (creator/admin)
- `DELETE /registrations/{id}/` — Cancel registration

## Tech Stack
- Python 3.x
- Django
- Django REST Framework
- djangorestframework-simplejwt
- SQLite/MySQL/PostgreSQL (configurable)

## Setup

```bash
# Clone repository
git clone https://github.com/<your-username>/event-management-api.git
cd event-management-api

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start server
python manage.py runserver

Deployment Notes
• Use environment variables for all secrets (SECRET_KEY, DB credentials, JWT settings).
• Enable HTTPS and set ALLOWED_HOSTS correctly.
• Configure static files (WhiteNoise for Heroku).
• Add worker process for Celery tasks.
• Run migrations on deploy and create a superuser.


Documentation
The API includes a generated Swagger/OpenAPI specification accessible at `/swagger/` or `/docs/` after deployment.
This includes all endpoints, parameters, request/response schemas, and authentication details.