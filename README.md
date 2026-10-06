# Django App Base

A starter template for new Django APIs: JWT auth with email login, public/private route
separation, database selectable by env, optional SPA serving, database logging, Celery,
Redis cache, Docker and a Helm chart.

## Features

- **Database by env**: `DB_ENGINE` = `sqlite` (default), `postgresql` or `mysql`.
- **Custom user** (`apps.users.User`): login by email, `uuid` field, signup and `me` endpoints.
- **Public and private routes**: everything under `api/public/` is open, everything under
  `api/private/` requires authentication. An expired/invalid token on a public route is
  ignored instead of returning 401.
- **SPA served by the backend**: with `SERVE_SPA=true`, the built frontend is served from
  the root and unknown routes fall back to `index.html`.
- **Database logging**: `Logger` writes JSON to stdout and, with `LOG_TO_DB=true`, to the
  `AppLog` table (read only in the admin). `LOG_REQUESTS=true` logs every `/api/` request.
- **Celery** with Redis broker, results in the database and beat with database scheduler.
- **Redis cache** (optional), **CORS**, **Swagger** at `api/swagger/`, **Jazzmin** admin,
  **WhiteNoise** static files.
- **Deploy**: Docker image, docker compose, Helm chart (api, admin, workers, beat, flower)
  and GitHub Actions CI/CD.

## Prerequisites

- Python 3.12+
- Optional: PostgreSQL or MySQL, Redis, Docker

## Getting Started

```bash
git clone <repository-url> my-project
cd my-project/backend
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp example.env .env            # edit as needed
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

With no `DB_ENGINE`, the app uses SQLite at `backend/db.sqlite3`.

## Configuration

| Variable | Default | Description |
|---|---|---|
| `ENV_NAME` | `DEV` | `DEV` enables DEBUG and open CORS |
| `SECRET_KEY` | insecure default | Required outside `DEV` |
| `ALLOWED_HOSTS` | | Comma-separated, ignored in `DEV` |
| `CORS_ALLOWED_ORIGINS` | | Comma-separated origins allowed outside `DEV` |
| `DB_ENGINE` | `sqlite` | `sqlite`, `postgresql` or `mysql` |
| `DB_NAME` | `backend/db.sqlite3` for sqlite | Database name, or file path for sqlite |
| `DB_USER`, `DB_PASS`, `DB_HOST` | | Server databases only |
| `DB_PORT` | `5432` / `3306` | Server databases only |
| `USE_REDIS_CACHE` | `false` | Enables Redis cache and Celery broker |
| `REDIS_*` | | Host, port, password, db index, SSL |
| `CELERY_BROKER_URL` | Redis DB 0 | Overrides the broker |
| `LOG_LEVEL` | `info` | `debug`, `info`, `warning`, `error`, `critical` |
| `LOG_TO_DB` | `false` | Persist `Logger` entries in `AppLog` |
| `LOG_REQUESTS` | `false` | Log every `/api/` request |
| `SERVE_SPA` | `false` | Serve the SPA from the backend |
| `SPA_DIR` | `backend/spa` | Folder with the built SPA (`index.html` + assets) |

MySQL needs the driver: `pip install mysqlclient` (and `mariadb-dev` in the Docker image).

## Routes

| Path | Access |
|---|---|
| `admin/` | Django admin |
| `api/public/token/`, `token/refresh/`, `token/verify/` | Public (JWT, login with `email` + `password`) |
| `api/public/users/signup/` | Public |
| `api/private/users/me/` | Authenticated |
| `api/swagger/` | Public |
| anything else | SPA `index.html` when `SERVE_SPA=true` |

### Adding routes to an app

Create `public_urls.py` and/or `private_urls.py` in the app and include them:

```python
# api/public_urls.py
path("blog/", include("apps.blog.public_urls")),

# api/private_urls.py
path("blog/", include("apps.blog.private_urls")),
```

Views do not need `permission_classes`: the default permission
(`api.permissions.IsPublicRouteOrAuthenticated`) decides by the namespace. Declaring
`permission_classes` on a view still overrides it (e.g. admin-only views).

## Logging

```python
from logger import Logger

logger = Logger("billing")
logger.info("Invoice created", extra={"invoice_id": invoice.id})
logger.error("Payment failed", extra={"order": order.id}, trace=traceback.format_exc())
```

A failure to save the log never breaks the caller. Note that a log written inside a
transaction that is rolled back is rolled back too.

## Serving a SPA

1. Build the frontend (e.g. `npm run build`).
2. Copy the output (`dist/`) to `backend/spa/` or point `SPA_DIR` to it.
3. Set `SERVE_SPA=true`.

Assets are served by WhiteNoise from the root (`/assets/...`, `/favicon.ico`). `index.html`
is sent with `Cache-Control: no-cache` so new deploys are picked up. In Kubernetes, enable
the `/` path in `deploy/helm/values.yaml`.

## Initial objects

`python manage.py initialize_objects` runs the idempotent functions listed in
`apps/management/commands/initialize_objects.py` (`INITIALIZERS`). Docker compose and the
Helm chart run it after `migrate`.

## Project Structure

```plaintext
backend/
    ├── manage.py
    ├── logger.py              # JSON logger, optional database persistence
    ├── config/                # settings, urls, celery, SPA view
    ├── api/                   # public/private routing, permission, authentication
    │   ├── public_urls.py
    │   └── private_urls.py
    ├── apps/                  # all apps go here
    │   ├── users/             # custom user (email login)
    │   ├── logs/              # AppLog model and request log middleware
    │   └── management/        # initialize_objects command
    ├── example.env
    └── requirements.txt
deploy/                        # Dockerfile, compose, scripts, Helm chart
.github/workflows/             # CI/CD (tests, image build, Helm tag update)
```

## Deployment

See [DEPLOY](deploy/README.md) for Docker and [the workflows README](.github/workflows/README.md)
for CI/CD. Before using the Helm chart, set `image.repository` in `deploy/helm/values.yaml`.

## Testing

```bash
cd backend
python manage.py test
```

## License

This project is licensed under the [MIT License](LICENSE).
