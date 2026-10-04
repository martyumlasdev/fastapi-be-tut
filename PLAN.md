# FastAPI + Next.js Learning Roadmap

A step-by-step learning project for building a production-style FastAPI + Next.js application.

The roadmap is ordered by **implementation dependencies**, so each topic builds on concepts learned earlier.

---

## Phase 1 — Core API Architecture

* [x] Project setup
* [x] Routers
* [x] Users CRUD
* [x] Relationships
* [x] Dependencies / `Depends()`
* [x] Authentication & authorization
* [x] `Annotated` dependency patterns
* [x] Application configuration
* [x] Services / business logic layer

---

## Phase 2 — Frontend Integration

* [x] Next.js + TypeScript setup
* [x] API client
* [x] Generic `apiFetch<T>`
* [x] Authentication flow
* [x] JWT storage
* [x] Protected routes / dashboard
* [x] CRUD integration
* [x] Global 401 handling

---

## Phase 3 — Application Lifecycle & Database

* [x] Lifespan / startup & shutdown
* [x] Alembic migrations
* [ ] Seeders & factories

### Goal

Learn how to reliably create test/development data instead of manually inserting records.

---

## Phase 4 — Files & User Accounts

* [ ] File uploads
* [ ] Static/media file serving
* [ ] Email infrastructure
* [ ] Email verification
* [ ] Password reset

### Dependency

```text
Email infrastructure
        ↓
Email verification
        ↓
Password reset
```

File uploads are mostly independent of email, so they are introduced first.

---

## Phase 5 — Background Processing

* [ ] FastAPI `BackgroundTasks`
* [ ] Task queues
* [ ] Queue workers
* [ ] Notifications

### Dependency

```text
BackgroundTasks
        ↓
Task queues
        ↓
Workers
        ↓
Notifications
```

Email will provide a practical example of why background processing is useful.

Example:

```text
User registers
      ↓
Create account
      ↓
Queue verification email
      ↓
Worker sends email
      ↓
User verifies account
```

---

## Phase 6 — Performance & Abuse Protection

* [ ] Rate limiting
* [ ] Caching
* [ ] Cache invalidation / cache strategies

### Dependency

Rate limiting comes before caching because rate limiting is primarily an API protection/security concern, while caching is primarily a performance concern.

Rate limiting will eventually be applied to areas such as:

```text
/login
/password-reset
/email-verification
/API endpoints
```

---

## Phase 7 — Real-Time Features

* [ ] WebSockets
* [ ] Real-time notifications
* [ ] Connection management

### Dependency

The notification system is learned first, then WebSockets can be used to deliver notifications in real time.

```text
Notification
      ↓
WebSocket
      ↓
Real-time notification
```

---

## Phase 8 — Quality & Maintainability

* [ ] Testing
* [ ] Unit tests
* [ ] API / integration tests
* [ ] Authentication tests
* [ ] File upload tests
* [ ] Background-job tests
* [ ] Logging
* [ ] Error handling
* [ ] Structured application logging

---

## Phase 9 — API & Security

* [ ] OpenAPI / API documentation
* [ ] Security hardening
* [ ] Input validation
* [ ] Authentication hardening
* [ ] CORS / security configuration
* [ ] Rate-limit hardening
* [ ] Production secrets / configuration

---

## Phase 10 — Deployment

* [ ] Docker
* [ ] Docker Compose / multi-service development
* [ ] Production configuration
* [ ] Production database
* [ ] Reverse proxy / HTTPS
* [ ] AWS deployment
* [ ] Monitoring / health checks
* [ ] Production deployment workflow

---

## Phase 11 — Advanced Database

* [ ] Async SQLAlchemy
* [ ] Async database dependencies
* [ ] Async services
* [ ] Async performance / concurrency considerations

Async SQLAlchemy is intentionally placed near the end because it changes the database access pattern throughout the application.

The project will remain **synchronous SQLAlchemy** until this phase.

---

# Overall Dependency Chain

```text
Core FastAPI
    ↓
Authentication
    ↓
Services
    ↓
Frontend
    ↓
Alembic
    ↓
Seeders / Factories
    ↓
File Uploads
    ↓
Email
    ↓
Email Verification
    ↓
Password Reset
    ↓
Background Tasks
    ↓
Task Queues
    ↓
Notifications
    ↓
Rate Limiting
    ↓
Caching
    ↓
WebSockets
    ↓
Testing / Logging / Error Handling
    ↓
Security
    ↓
Docker
    ↓
AWS
    ↓
Async SQLAlchemy
```

---

# Current Progress

The immediate next topic is:

**Seeders & Factories**

After that:

1. File uploads
2. Email infrastructure
3. Email verification
4. Password reset
5. Background tasks
6. Task queues
7. Notifications
8. Rate limiting
9. Caching
10. WebSockets
11. Testing
12. Logging / error handling
13. Security
14. Docker
15. AWS
16. Async SQLAlchemy

---

# Learning Rule

For this project:

> **Learn the concept → implement it → use it in the application → move to the next dependency.**

Avoid introducing advanced infrastructure before the project actually needs it.
