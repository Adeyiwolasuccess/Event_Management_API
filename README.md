# 🎟️ Event Management API — README & Migration Plan

## Overview
The Event Management API is a backend application built with Django REST Framework that allows users to manage
events, categories, ticket pricing, and registrations. This implementation merges ALX's required features with
real-world functionality like strict permission controls, filtering, and pagination. The API follows RESTful
principles with JWT-based authentication.

---

## Migration Plan
1. Initialize Django project & app structure.
2. Install dependencies: Django, DRF, SimpleJWT, django-filter.
3. Configure `settings.py` for database, REST framework, JWT auth.
4. Define models: User, EventCategory, Event, TicketPricing, Registration.
5. Create migrations (`python manage.py makemigrations`).
6. Apply migrations (`python manage.py migrate`).
7. Register models in `admin.py` for admin interface management.
8. Create serializers for each model with validation logic.
9. Implement viewsets/endpoints with appropriate permissions.
10. Add filtering, pagination, and search in views.
11. Test endpoints with Django test client or Postman.
12. Seed initial data (categories, admin user).
13. Deploy to production environment (Heroku/PythonAnywhere).

---

## Features
- **User Authentication & Profile**
  - JWT login, logout, register, refresh
  - View and update own profile
  - Admin can view/manage all users

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
  - Prevent duplicate registrations
  - Prevent registration if event is full
  - View own registrations
  - Admins and creators can view/manage event registrations

---

## API Endpoints

### 1. Authentication & Profile
- `POST /api/auth/register/` — Register a new user
- `POST /api/auth/login/` — Obtain JWT token
- `POST /api/auth/logout/` — Logout (blacklist token)
- `POST /api/auth/refresh/` — Refresh access token
- `GET /api/auth/users/me/` — Get current user profile
- `PUT /api/auth/users/me/` — Update current user profile
- `GET /api/auth/users/{id}/` — Admin get user by ID
- `GET /api/auth/users/` — Admin list all users

### 2. Event Categories
- `GET /api/categories/` — List categories
- `POST /api/categories/` — Create category (admin only)
- `GET /api/categories/{id}/` — Retrieve category
- `PUT /api/categories/{id}/` — Update category (admin only)
- `DELETE /api/categories/{id}/` — Delete category (admin only)

### 3. Events
- `GET /api/events/` — List all upcoming events (filters: category, location, date)
- `POST /api/events/` — Create event (auth required)
- `GET /api/events/{id}/` — Retrieve event details
- `PUT /api/events/{id}/` — Update (creator/admin only)
- `DELETE /api/events/{id}/` — Delete (creator/admin only)

### 4. Ticket Pricing
- `GET /api/events/{event_id}/tickets/` — List tickets for event
- `POST /api/events/{event_id}/tickets/` — Create ticket (creator/admin)
- `GET /api/events/{event_id}/tickets/{id}/` — Get ticket details
- `PUT /api/events/{event_id}/tickets/{id}/` — Update (creator/admin)
- `DELETE /api/events/{event_id}/tickets/{id}/` — Delete (creator/admin)

### 5. Registrations
- `GET /api/events/{event_id}/registrations/` — View registrations for event (creator/admin sees all, user sees own)
- `POST /api/events/{event_id}/registrations/` — Register for event (auth required)
- `GET /api/events/{event_id}/registrations/{id}/` — View single registration
- `PUT /api/events/{event_id}/registrations/{id}/` — Update status (creator/admin only)
- `DELETE /api/events/{event_id}/registrations/{id}/` — Cancel registration

---

## Tech Stack
- Python 3.x
- Django 5.x
- Django REST Framework
- djangorestframework-simplejwt
- django-filter
- SQLite (default, can be swapped for PostgreSQL/MySQL)

---

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

