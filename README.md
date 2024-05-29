# Finance Project

A Django application that integrates with the Yahoo Finance API using the `yfinance` Python library. The application allows CRUD operations on company data and provides endpoints for data export with advanced filtering options. The application also implements background tasks using Celery for periodic updates.

## Features

- **Integration**: Fetch data from Yahoo Finance and store it in the local database.
- **CRUD Operations**: Add, update, delete, and retrieve company data.
- **Data Export**: Export data to CSV with date range filtering.
- **Background Tasks**: Use Celery to periodically update company data.
- **Pagination**: Retrieve all companies with pagination.

## Requirements

- Python3
- Django
- Django REST framework
- `yfinance` library
- Celery
- Redis (for Celery broker)

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/yfinance.git
    cd finance_project
    ```

2. **Create and activate a virtual environment**:
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3. **Install the dependencies**:
    ```bash
    pip3 install -r requirements.txt
    ```

4. **Set up Redis**:
    - Install Redis using Homebrew (macOS):
        ```bash
        brew install redis
        ```
    - Start Redis:
        ```bash
        brew services start redis
        ```
5. **Make migrations**:
    ```bash
    python3 manage.py makemigrations
    ```
6. **Apply database migrations**:
    ```bash
    python3 manage.py migrate
    ```

7. **Create a superuser**:
    ```bash
    python3 manage.py createsuperuser
    ```
## Running the Application

1. **Start the Django development server**:
    ```bash
    python3 manage.py runserver
    ```
2. **Start the Celery worker**:
    ```bash
    celery -A finance_project worker -l info
    ```
3. **Start the Celery Beat scheduler**:
    ```bash
    celery -A finance_project beat -l info
    ```
## Running the tests
  ```bash
  python3 manage.py test
  ```
## API Endpoints

- Add a new company:
    ```bash
    POST /api/companies/add_company/
    Body: {"symbol": "AAPL"}
    ```
- Update a company:
    ```bash
    PUT /api/companies/update_company/<symbol>/
    Body: {"symbol": "NEW_SYMBOL"}
    ```
- Delete a company:
    ```bash
    DELETE /api/companies/delete_company/<symbol>/
    ```
- Retrieve all companies:
    ```bash
    GET /api/companies/
    ```
- Retrieve a company:
    ```bash
    GET /api/companies/get_company/<symbol>/
    ```
- Export data to CSV with date range filtering:
    ```bash
    GET /api/companies/export/?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD
    ```

## Configuration

### Celery Configuration

Ensure your `settings.py` has the necessary Celery configuration:

```python
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'
