# Library-Service-API

## Description

Library-Service-API is a comprehensive RESTful API for library management systems. It provides functionality for
managing books, user authentication, and borrowing operations. The system allows users to register, browse the library
catalog, borrow books, and track their borrowings, while librarians can manage the book inventory and monitor borrowing
activities.

## Features

- **User Management**:
    - User registration and authentication
    - JWT token-based authentication
    - User profile management

- **Book Management**:
    - Complete CRUD operations for books
    - Inventory tracking
    - Book details and catalog management

- **Borrowing System**:
    - Borrow books with automatic inventory adjustment
    - Return books functionality
    - Due date tracking
    - Active/inactive borrowing filtering
    - Staff-specific functionalities for monitoring

## How to Start

### Prerequisites

- Python 3.x
- pip
- PostgreSQL (or other database)

### Installation

1. Clone the repository:

```bash
git clone https://github.com/zave52/Library-Service-API.git
cd Library-Service-API
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Configure environment variables (create a `.env` from `.env.sample`):

```
SECRET_KEY=your_secret_key
DEBUG=True
```

5. Run migrations:

```bash
python manage.py migrate
```

6. Create a superuser:

```bash
python manage.py createsuperuser
```

7. Start the development server:

```bash
python manage.py runserver
```

## API Documentation

Access interactive API documentation at:

- Raw Schema: `/api/v1/schema/`
- Swagger UI: `/api/v1/doc/swagger/`
- ReDoc: `/api/v1/doc/redoc/`

### Books Service

| Method    | Endpoint       | Description                                    |
|-----------|----------------|------------------------------------------------|
| POST      | `/books/`      | Add a new book to the library                  |
| GET       | `/books/`      | Get a list of all books                        |
| GET       | `/books/<id>/` | Get detailed information about a specific book |
| PUT/PATCH | `/books/<id>/` | Update book information (including inventory)  |
| DELETE    | `/books/<id>/` | Delete a book from the library                 |

### Users Service

| Method    | Endpoint                | Description                          |
|-----------|-------------------------|--------------------------------------|
| POST      | `/users/`               | Register a new user                  | |
| GET       | `/users/me/`            | Get current user profile information |
| PUT/PATCH | `/users/me/`            | Update current user profile          |
| POST      | `/users/token/`         | Get JWT tokens (login)               |
| POST      | `/users/token/refresh/` | Refresh JWT token                    |
| POST      | `/users/token/verify/`  | Verify JWT token                     |

### Borrowings Service

| Method | Endpoint                                 | Description                                                        |
|--------|------------------------------------------|--------------------------------------------------------------------|
| POST   | `/borrowings/`                           | Create a new borrowing (decreases book inventory by 1)             |
| GET    | `/borrowings/?user_id=...&is_active=...` | Get borrowings with optional filters for user ID and active status |
| GET    | `/borrowings/<id>/`                      | Get detailed information about a specific borrowing                |
| POST   | `/borrowings/<id>/return/`               | Return a borrowed book (increases book inventory by 1)             |

```