# Django App Base

A starter template for quickly setting up new Django applications with best practices, reusable configurations, and essential tools.

## Features

- **Pre-configured Settings**: Organized and modular settings for development, testing, and production.
- **Reusable Structure**: A scalable app layout for adding new features easily.
- **Built-in Tools**:
  - Debugging with `django-debug-toolbar`.
  - Static and media file management.
  - Logging configuration for better monitoring.
- **Test-Ready**: Includes testing tools and sample test cases.
- **Docker Support**: Containerized environment for easy setup.

## Prerequisites

- Python 3.8+
- Django 4.x
- Docker (optional, for containerized development)
- PostgreSQL or other database as required

## Getting Started

### 1. Clone the Repository

```bash
git clone <repository-url> django-app-base
cd django-app-base
```

### 2. Set Up a Virtual Environment

```bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the Project

1. Copy the `.env.example` file to `.env` and update the variables as needed:
   ```bash
   cp .env.example .env
   ```
2. Update database settings and secrets in the `.env` file.

### 5. Run Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Start the Development Server

```bash
python manage.py runserver
```

Access the application at `http://127.0.0.1:8000/`.

## Project Structure

```plaintext
backend
├── manage.py
├── app_base/        # Main app folder
│   ├── settings/    # Organized settings (base, dev, prod)
│   ├── static/      # Static files
│   ├── templates/   # HTML templates
│   ├── urls.py      # Project URL configurations
│   ├── wsgi.py      # WSGI application
├── .env.example     # Sample environment variables
├── requirements.txt # Project dependencies
├── README.md        # Project documentation
```

## Deployment

### Using Docker

1. Build the Docker image:
   ```bash
   docker build -t django-app-base .
   ```
2. Run the container:
   ```bash
   docker run -d -p 8000:8000 --env-file .env django-app-base
   ```

### Manual Deployment

1. Set up a production server (e.g., Gunicorn, Nginx).
2. Apply production settings from `settings/production.py`.
3. Use a WSGI server to serve the application.

## Testing

Run tests with:

```bash
python manage.py test
```

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new feature branch (`git checkout -b feature-name`).
3. Commit changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature-name`).
5. Open a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgements

Inspired by Django's best practices and community guidelines.
