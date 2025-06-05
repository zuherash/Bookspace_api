# 📚 Bookspace API

Welcome to **Bookspace API** — a backend system for managing books, users, and orders for a virtual library or bookstore.

---

## ✨ What is Bookspace?

Bookspace is a RESTful API backend where users can:
- Browse available books
- Register and manage their accounts
- Place orders for books
- Manage book listings (for admins)

It’s built with a clean, scalable Django architecture, ideal for learning or expanding into a full bookstore system.

---

## 🛠 Built With

- **Python 3.11+**
- **Django 5**
- **Django REST Framework**
- **PostgreSQL** 
- **JWT Authentication** 

---

## 🚀 Getting Started

Clone the project and get it running locally in a few steps:

# Clone repository
git clone https://github.com/zuherash/Bookspace_api.git

# Move into project directory
cd Bookspace_api

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# Run the development server
python manage.py runserver

# Run tests (uses SQLite by default)
python manage.py test

Running tests automatically sets the `USE_SQLITE` environment variable to `1`,
so SQLite is used for test databases. Unset this variable if you prefer running
tests against PostgreSQL.

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

## 📚 Core API Endpoints

Here are the main API endpoints:

- **POST** `/api/auth/register/` → Register a new user
- **POST** `/api/auth/login/` → User login and obtain authentication tokens
- **GET** `/api/books/` → List all available books
- **POST** `/api/books/` → Add a new book (admin only)
- **GET** `/api/books/{id}/` → Get details of a specific book
- **PUT** `/api/books/{id}/` → Update an existing book
- **DELETE** `/api/books/{id}/` → Delete a book
- **GET** `/api/reviews/` → List all reviews
- **POST** `/api/reviews/` → Create a new review
- **GET** `/api/reviews/{id}/` → Retrieve a specific review
- **PUT** `/api/reviews/{id}/` → Update an existing review
- **DELETE** `/api/reviews/{id}/` → Delete a review


📩 Contact
Need help or want to collaborate?
Feel free to reach me via:

Email: zuherash@gmail.com


Instagram : zuheir.dev

Happy building! 🚀
