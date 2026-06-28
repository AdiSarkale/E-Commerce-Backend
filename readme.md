# 🛒 E-Commerce Backend API

A production-inspired E-Commerce Backend built using **FastAPI**, **PostgreSQL**, **Redis**, **Docker**, and **SQLAlchemy Async**. The project follows a layered architecture with Repository and Service patterns to create a scalable, maintainable, and high-performance backend.

---

## 🚀 Features

### 🔐 Authentication

* JWT Authentication
* Secure Password Hashing
* User Registration & Login
* Protected Routes

### 👤 User Management

* User Profile
* Account Management
* Authentication Middleware

### 📦 Product Management

* Product CRUD
* Categories
* Product Images
* SKU Management

### 🛒 Shopping Cart

* Add to Cart
* Update Quantity
* Remove Items
* View Cart
* Cart Total Calculation

### 📋 Orders

* Checkout
* Order Creation
* Order History
* Order Details
* Order Status

### 📦 Inventory

* Stock Management
* Inventory Validation
* Automatic Stock Updates

### ⚡ Performance

* Redis Caching
* Optimized Database Queries
* Async SQLAlchemy
* Background Tasks

### 📨 Background Processing

* Celery Workers
* Email Tasks
* Redis Broker

### 🗄 Database

* PostgreSQL
* Alembic Migrations
* Relationships
* Transactions

---

# 🏗 Project Architecture

```
Client
   │
   ▼
FastAPI API Layer
   │
   ▼
Service Layer
   │
   ▼
Repository Layer
   │
   ▼
PostgreSQL Database

        │
        ├────────► Redis Cache
        │
        └────────► Celery Workers
                        │
                        ▼
                    Email Tasks
```

---

# 📁 Project Structure

```
backend/
│
├── alembic/
├── api/
├── cache/
├── core/
├── models/
├── repositories/
├── schemas/
├── services/
├── tasks/
├── utils/
│
├── main.py
├── db.py
├── compose.yaml
├── Dockerfile
└── requirements.txt
```

---

# 🛠 Tech Stack

### Backend

* FastAPI
* Python 3

### Database

* PostgreSQL
* SQLAlchemy Async
* Alembic

### Caching

* Redis

### Background Jobs

* Celery

### Authentication

* JWT
* Passlib / Bcrypt

### DevOps

* Docker
* Docker Compose

---

# ⚙️ Installation

## Clone Repository

```bash
git clone https://github.com/AdiSarkale/E-Commerce-Backend.git
cd E-Commerce-Backend/backend
```

## Create Virtual Environment

```bash
python -m venv .venv
```

Activate:

Windows

```bash
.venv\Scripts\activate
```

Linux

```bash
source .venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure Environment Variables

Create a `.env` file.

Example:

```env
DATABASE_URL=
SECRET_KEY=
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

REDIS_HOST=
REDIS_PORT=

SMTP_HOST=
SMTP_PORT=
SMTP_USER=
SMTP_PASSWORD=
```

---

## Run Database Migrations

```bash
alembic upgrade head
```

---

## Start Application

```bash
uvicorn main:app --reload
```

---

## Using Docker

```bash
docker compose up --build
```

---

# 📚 API Documentation

After starting the server:

Swagger UI

```
http://localhost:8000/docs
```

ReDoc

```
http://localhost:8000/redoc
```

---

# ✅ Current Modules

* Authentication
* Users
* Products
* Inventory
* Shopping Cart
* Orders
* Redis Cache
* Celery Tasks
* Email Service
* Docker Deployment

---

# 🎯 Learning Objectives

This project was developed to explore production-grade backend development concepts including:

* Clean Architecture
* Repository Pattern
* Service Layer Pattern
* Dependency Injection
* Asynchronous Programming
* JWT Authentication
* Redis Caching
* Background Processing
* Dockerized Development
* Database Migrations
* API Design Best Practices

---

# 📌 Future Improvements

* Payment Gateway Integration
* Product Reviews & Ratings
* Wishlist
* Search & Filtering
* Image Upload Service
* Role-Based Access Control (RBAC)
* API Rate Limiting
* Unit & Integration Testing
* CI/CD Pipeline
* Kubernetes Deployment

---

# 👨‍💻 Author

**Aditya Sarkale**

Python Backend Developer | FastAPI | PostgreSQL | Redis | Docker | SQLAlchemy | SAP Automation
