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

---

## 🚀 Features

- **User Authentication & Management**
  - Register, login, logout with JWT
  - View & update user profile
  - CRUD operations for users

- **Event Management**
  - Create, Read, Update, Delete events
  - Only event creators or admins can update/delete
  - Prevent creation of past events
  - Search, filter (date, location, category), and ordering

- **Event Categories**
  - Admin can manage event categories
  - Public can list & view categories

- **Ticket Management**
  - Event creators can add, update, delete ticket types
  - Supports multiple ticket types (VIP, Regular, etc.)
  - Includes price, currency, and availability

- **Event Registrations**
  - Users can register for events (once per event)
  - Prevents registration when events are full
  - Event creators/admins can view all registrations
  - Users can only view their own registrations

- **Permissions**
  - Read-only for anonymous users
  - Create/Update/Delete only for authenticated users
  - Creator/Admin restrictions for event and ticket management

---

## 🛠 Tech Stack

- [Django 5.x](https://www.djangoproject.com/)
- [Django Rest Framework](https://www.django-rest-framework.org/)
- [Django Filter](https://django-filter.readthedocs.io/)
- [SimpleJWT](https://django-rest-framework-simplejwt.readthedocs.io/) (for authentication)

---

## 📂 Project Structure

event_manager/
│── events/ # Event app (categories, events, tickets, registrations)
│ ├── models.py
│ ├── views.py
│ ├── serializers.py
│ ├── urls.py
│── users/ # User app (auth, profiles)
│ ├── models.py
│ ├── views.py
│ ├── serializers.py
│ ├── urls.py
│── event_manager/ # Project config
│ ├── settings.py
│ ├── urls.py
│── db.sqlite3 # Local database
│── requirements.txt

yaml
Copy
Edit

---

## ⚙️ Installation

1. **Clone repository**
   ```bash
   git clone https://github.com/yourusername/event-manager-api.git
   cd event-manager-api
Create virtual environment

bash
Copy
Edit
python -m venv venv
source venv/bin/activate   # Linux / Mac
venv\Scripts\activate      # Windows
Install dependencies

bash
Copy
Edit
pip install -r requirements.txt
Run migrations

bash
Copy
Edit
python manage.py migrate
Create superuser

bash
Copy
Edit
python manage.py createsuperuser
Start development server

bash
Copy
Edit
python manage.py runserver
🔐 Authentication
This project uses JWT Authentication.

Login to obtain a token:
POST /api/auth/login/

Include token in headers:

makefile
Copy
Edit
Authorization: Bearer <your_token>
📡 API Endpoints
Users
Method	Endpoint	Description
POST	/api/auth/register/	Register new user
POST	/api/auth/login/	Login (JWT token)
POST	/api/auth/logout/	Logout
POST	/api/auth/refresh/	Refresh JWT token
GET	/api/auth/users/me/	Get current user profile
GET	/api/auth/users/	List all users (admin only)
GET	/api/auth/users/{id}/	Retrieve a user

Categories
Method	Endpoint	Description
GET	/api/categories/	List categories
POST	/api/categories/	Create category (admin only)
GET	/api/categories/{id}/	Get category details
PUT	/api/categories/{id}/	Update category (admin only)
DELETE	/api/categories/{id}/	Delete category (admin only)

Events
Method	Endpoint	Description
GET	/api/events/	List all upcoming events
POST	/api/events/	Create event (auth required)
GET	/api/events/{id}/	Get event details
PUT	/api/events/{id}/	Update event (creator/admin only)
DELETE	/api/events/{id}/	Delete event (creator/admin only)

Tickets
Method	Endpoint	Description
GET	/api/events/{event_id}/tickets/	List tickets for an event
POST	/api/events/{event_id}/tickets/	Create ticket (creator/admin only)
GET	/api/events/{event_id}/tickets/{id}/	Get ticket details
PUT	/api/events/{event_id}/tickets/{id}/	Update ticket (creator/admin)
DELETE	/api/events/{event_id}/tickets/{id}/	Delete ticket (creator/admin)

Registrations
Method	Endpoint	Description
GET	/api/events/{event_id}/registrations/	List registrations (creator/admin sees all, users see own)
POST	/api/events/{event_id}/registrations/	Register for event (auth required)
GET	/api/events/{event_id}/registrations/{id}/	Get registration details
PUT	/api/events/{event_id}/registrations/{id}/	Update status (admin only)
DELETE	/api/events/{event_id}/registrations/{id}/	Cancel registration (user/admin)

🧪 Example Workflow (CRUD)
Register a User

http
Copy
Edit
POST /api/auth/register/
{
  "username": "john",
  "email": "john@example.com",
  "phone": "1234567890",
  "password": "StrongPass123!"
}
Login & Get Token

http
Copy
Edit
POST /api/auth/login/
{
  "username": "john",
  "password": "StrongPass123!"
}
Response:

json
Copy
Edit
{
  "access": "jwt_token_here",
  "refresh": "refresh_token_here"
}
Create Event

http
Copy
Edit
POST /api/events/
Authorization: Bearer <jwt_token>
{
  "title": "Django Workshop",
  "description": "Learn Django REST API",
  "date": "2025-08-25T10:00:00Z",
  "location": "Online",
  "category": 1,
  "capacity": 50
}
Add Ticket

http
Copy
Edit
POST /api/events/1/tickets/
Authorization: Bearer <jwt_token>
{
  "ticket_type": "VIP",
  "price": "100.00",
  "currency": "USD",
  "available_quantity": 20
}
Register for Event

http
Copy
Edit
POST /api/events/1/registrations/
Authorization: Bearer <jwt_token>
{}

---
📖 Future Improvements
Add waitlist system when events are full

Payment gateway integration (Stripe/PayPal)

Email notifications for registrations

Dockerize the project for production

👨‍💻 Author
Built with ❤️ using Django & DRF.
