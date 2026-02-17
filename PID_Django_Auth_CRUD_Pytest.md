# 📘 Project Initiation Document (PID)

# Django Authentication & CRUD REST API with Pytest

------------------------------------------------------------------------

## 1. Project Title

**Django Authentication & CRUD REST API with Pytest Testing Framework**

------------------------------------------------------------------------

## 2. Project Background

Modern backend applications require:

-   Secure authentication
-   Clean CRUD APIs
-   Automated testing
-   CI-ready structure

This project demonstrates:

-   REST API development using Django
-   API toolkit using Django REST Framework
-   Automated testing using Pytest

The purpose of this project is educational and demonstrative.

------------------------------------------------------------------------

## 3. Project Objectives

### Primary Objectives

-   Implement JWT-based authentication
-   Build CRUD APIs
-   Write comprehensive test cases using Pytest
-   Demonstrate fixtures, parametrize, mocking, and coverage
-   Ensure clean architecture and best practices

### Secondary Objectives

-   Docker-ready setup
-   CI-ready configuration
-   90%+ test coverage
-   Proper documentation

------------------------------------------------------------------------

## 4. Project Scope

### ✅ In Scope

-   User Registration
-   Login (JWT Authentication)
-   Protected CRUD APIs
-   Test suite with Pytest
-   API documentation
-   Code coverage reporting

### ❌ Out of Scope

-   Frontend application
-   Production deployment
-   Complex business workflows

------------------------------------------------------------------------

## 5. Functional Requirements

### 5.1 Authentication Module

Features:

-   User registration
-   Login
-   JWT token generation
-   Refresh token
-   Protected endpoints

Implementation:

-   Django built-in User model
-   DRF SimpleJWT for authentication

------------------------------------------------------------------------

### 5.2 CRUD Module

Example Model: **Task**

Fields:

-   id
-   title
-   description
-   is_completed
-   created_at
-   updated_at
-   owner (ForeignKey to User)

API Endpoints:

  Method   Endpoint             Description
  -------- -------------------- -----------------
  POST     /api/tasks/          Create task
  GET      /api/tasks/          List user tasks
  GET      /api/tasks/{{id}}/   Retrieve task
  PUT      /api/tasks/{{id}}/   Update task
  DELETE   /api/tasks/{{id}}/   Delete task

Business Rules:

-   Only authenticated users can access
-   Users can only access their own tasks

------------------------------------------------------------------------

## 6. Non-Functional Requirements

-   Clean project structure
-   Modular apps
-   PEP8 compliance
-   90%+ test coverage
-   CI compatible
-   Easy setup with README
-   Basic structured logging via Django logging configuration
-   Consistent API error responses with a standard error schema

------------------------------------------------------------------------

## 7. Technical Stack

  Component        Technology
  ---------------- -----------------------
  Backend          Django
  API              Django REST Framework
  Authentication   JWT (SimpleJWT)
  Testing          Pytest
  Database         SQLite (Development)
  Coverage         pytest-cov
  Linting          flake8

------------------------------------------------------------------------

## 8. Project Architecture

    project_root/
    │
    ├── config/
    ├── apps/
    │   ├── users/
    │   └── tasks/
    │
    ├── tests/
    │   ├── test_auth.py
    │   ├── test_tasks.py
    │   ├── conftest.py
    │
    ├── pytest.ini
    ├── requirements.txt
    └── README.md

Architecture Style:

-   App-based modular structure
-   Separation of concerns
-   DRF ViewSets + Routers
-   Optional service-layer pattern

------------------------------------------------------------------------

## 9. Testing Strategy (Pytest Focus)

### Testing Types

-   Unit Tests
-   API Tests
-   Authentication Tests
-   Permission Tests
-   Edge Case Tests

### Coverage Targets

  Module        Target
  ------------- --------
  Auth          95%
  Tasks         90%
  Permissions   100%

------------------------------------------------------------------------

## 10. Milestones

  Milestone         Deliverable                  Duration
  ----------------- ---------------------------- ----------
  Setup             Django project initialized   Day 1
  Auth Module       JWT implemented              Day 2
  CRUD Module       Task API complete            Day 3
  Testing           Full Pytest suite            Day 4
  Coverage & Docs   90% coverage + README        Day 5

------------------------------------------------------------------------

## 11. Acceptance Criteria

-   User can register and login
-   CRUD APIs are functional
-   Protected endpoints are secured
-   All tests pass
-   90%+ test coverage achieved
-   README contains setup instructions

------------------------------------------------------------------------

# Project Summary

This project demonstrates:

-   Professional Django REST API development
-   Secure authentication using JWT
-   Clean CRUD implementation
-   Strong automated testing using Pytest
-   Production-ready backend structure
