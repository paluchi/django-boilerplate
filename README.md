# Django CRUD API for Email Verification Service

## Overview
This Django application integrates with an email verification service (like Hunter.io) and provides CRUD (Create, Read, Update, Delete) operations on the data received from the service. It features a RESTful API and includes auto-generated documentation for ease of use. The application uses Django ORM to interact with a SQL database and stores the data there.

## Getting Started

### Prerequisites
- Python 3.x

### Installation
1. Clone the repository
2. Install required packages:`pip install -r requirements.txt`
4. create .env file and add required environment variables
3. Make migrations `python manage.py migrate`


### Running the Application
Run the Django server with: `python manage.py runserver`

The application will be available at `http://localhost:8000/`.

### Test Linting
`mypy .`
`flake8 .`


## Available Paths

### API Documentation
- **Path:** `/docs/`
- **Description:** Auto-generated documentation for the API, detailing available endpoints, request formats, and expected responses.

### Admin Interface
- **Path:** `admin/`
- **Description:** Django’s built-in admin interface for application management.

### Email Service API
- **Path:** `/api/v1/email_service`
- **Description:** API endpoints for interacting with the email verification service. Includes CRUD operations for email data.

## Usage

### API Endpoints
The main API endpoints under `/api/v1/email_service` include:
- Email verification and creation
- Data retrieval
- Data updating
- Data deletion

Each endpoint supports standard HTTP methods (GET, POST, PUT, DELETE) corresponding to CRUD operations.
Check the docs to test the paths.