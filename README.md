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

## 🔐 Environment Variables

The `.env` file is excluded from version control so your secrets stay safe. Before running the project or tests, create this file or export the variables below in your shell:

- `SECRET_KEY`
- `DB_NAME`
- `DB_USER`
- `DB_PASSWORD`
- `DB_HOST`
- `DB_PORT`
- `USE_SQLITE` *(optional)*

Example `.env`:

```bash
SECRET_KEY=your-secret-key
DB_NAME=bookspace_db
DB_USER=postgres
DB_PASSWORD=your-db-password
DB_HOST=localhost
DB_PORT=5432
# USE_SQLITE=1
```

Load these variables with `source .env` (or export them manually) before running `manage.py` commands or executing tests.

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


📩 Contact
Need help or want to collaborate?
Feel free to reach me via:

Email: zuherash@gmail.com


Instagram : zuheir.dev

Happy building! 🚀
