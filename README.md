# Trello Clone Backend 🚀

A production-style project management backend inspired by Trello.

I built this project to learn and practice how to design a real-world backend system using Django. The goal was not just to create simple CRUD APIs, but to build a scalable backend with authentication, permissions, background tasks, caching, and containerized development.

---

## Project Overview

This project is a task management system where users can:

* Create and manage boards
* Add members to boards
* Create lists inside boards
* Create, update, move and delete cards
* Add comments to cards
* Attach labels to cards
* Upload attachments
* Track user activities
* Receive background notifications/tasks

The architecture is designed similar to real production applications.

---

# Tech Stack

## Backend

* Python 3.13
* Django 6
* Django REST Framework
* PostgreSQL
* Redis
* Celery
* Docker
* Docker Compose
* JWT Authentication
* Django Filter
* drf-spectacular (Swagger Documentation)

---

# Architecture

The project follows a modular Django app structure:

```
trello/

├── boards/
│   ├── models.py
│   ├── serializers.py
│   └── views.py
│
├── lists/
│   ├── models.py
│   └── views.py
│
├── cards/
│   ├── models.py
│   ├── serializers.py
│   └── views.py
│
├── comments/
│
├── labels/
│
├── attachments/
│
├── activities/
│   ├── models.py
│   └── tasks.py
│
└── trello/
    ├── settings.py
    ├── urls.py
    └── celery.py
```

---

# Features

## Authentication

Implemented JWT authentication.

Users can:

* Register
* Login
* Get access token
* Authenticate API requests

---

# Board Management

Users can create and manage boards.

Features:

* Create board
* Update board
* Delete board
* View user boards
* Add members

Board ownership and access permissions are handled at the API level.

---

# Card System

Cards are the main task objects.

Features:

* Create card
* Update card
* Delete card
* Search cards
* Filter cards
* Ordering
* Pagination

Example:

```
Board

 └── List

      └── Card
```

---

# Moving Cards

The card moving logic follows Trello's approach.

Instead of deleting and recreating cards, the card only changes its list relation.

Example:

Before:

```
Todo

- Build API
```

Database:

```
card.list = Todo
```

After moving:

```
Doing

- Build API
```

Only this field changes:

```
card.list = Doing
```

---

# Permissions

The API uses queryset-level permissions.

Users can access:

* Their own boards
* Boards where they are members

Example:

```python
Card.objects.filter(
    Q(list__board__owner=user)
    |
    Q(list__board__members=user)
)
```

---

# Comments

Users can add comments to cards.

Relationship:

```
Card

 |

Comments
```

---

# Labels

Cards support multiple labels.

Example:

```json
{
    "title": "Fix authentication bug",
    "labels": [
        {
            "title": "Bug",
            "color": "#EF4444"
        }
    ]
}
```

---

# Attachments

Users can upload files related to cards.

Example:

```
Card

 |

Attachment
```

---

# Activity Log

Important user actions are stored.

Examples:

```
Created card 'Login API'

Moved card 'Docker Setup'

Deleted card 'Test Task'
```

Activity creation is handled asynchronously with Celery.

---

# Celery + Redis

Celery is used for background processing.

Example:

When a user registers:

```
User Register

      |

      |

Celery Task

      |

      |

Send Welcome Email
```

Benefits:

* Faster API responses
* Non-blocking operations
* Background processing

---

# Redis Cache

Redis is used for API caching.

Example:

First request:

```
GET /cards/api/

Database
   |
   |
Redis Cache
```

Next requests:

```
GET /cards/api/

Redis
```

Cache is cleared after:

* Create
* Update
* Delete

operations.

---

# Docker Setup

The project runs with Docker Compose.

Services:

```
Django
 |
PostgreSQL
 |
Redis
 |
Celery Worker
```

Run project:

```bash
docker compose up -d
```

---

# API Documentation

Swagger documentation is available through:

```
/api/docs/
```

Schema:

```
/api/schema/
```

---

# Testing

API tests are written using Django REST Framework testing tools.

Current tests include:

* Create Card
* List Cards
* Update Card
* Delete Card
* Permission testing

Run tests:

```bash
docker exec -it django_app python manage.py test
```

---

# Environment

Example services:

```
Django      : 8000
PostgreSQL  : 5432
Redis       : 6379
```

---

# Future Improvements

Possible next steps:

* Role based permissions

  * Owner
  * Admin
  * Member
  * Viewer

* Celery Beat

  * Scheduled reports
  * Reminders
  * Cleanup tasks

* Real-time updates

  * Django Channels
  * WebSockets

* React frontend

* Production deployment

  * Nginx
  * Gunicorn
  * CI/CD

---

# Why I Built This Project

I created this project as a practical backend learning experience.

The goal was to understand how real applications are structured:

* API design
* Database relationships
* Authentication
* Permissions
* Background jobs
* Caching
* Docker environments
* Testing

This project helped me move from building simple Django applications toward designing more production-oriented backend systems.
