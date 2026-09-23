# SaintGraal

A personal finance tracker REST API built with Django REST Framework. Users manage income and expense transactions under custom categories, with per-user data isolation, analytics endpoints, and export to CSV or PDF.

## Features

- User-scoped categories and transactions (income / expense)
- JWT and OAuth2 social authentication via `djoser` + `simplejwt`
- Filtering on type, category, and date range via `django-filter`
- Analytics: spending/income breakdown by category and monthly summaries
- Export: transactions to CSV or PDF (via `reportlab`)
- Swagger / OpenAPI documentation via `drf-yasg`

## Tech Stack

| Layer | Technology |
|---|---|
| Web framework | Django 5.1 + DRF 3.15 |
| Auth | djoser + simplejwt + social-auth |
| Database | PostgreSQL (psycopg2) |
| PDF generation | ReportLab |
| API docs | drf-yasg (Swagger) |

## Data Model

```
User
 ├──< Category (name)
 └──< Transaction (type, category FK, amount, description, created)
```

| Model | Key Fields |
|---|---|
| `Category` | `name`, `user` (FK) |
| `Transaction` | `user` (FK), `type` (income/expense), `category` (FK), `amount`, `description`, `created`, `updated` |

## Project Structure

```
SaintGraal/
├── graal_app/
│   ├── models.py         # Category, Transaction
│   ├── serializers.py    # ModelSerializers
│   ├── views.py          # CRUD + CategorySummaryView + MonthlySummaryView
│   ├── analytics.py      # get_summary_by_category(), get_monthly_summary()
│   ├── export.py         # CSV and PDF export views
│   ├── filters.py        # CategoryFilter, TransactionFilter
│   └── permissions.py    # Object-level permissions
├── main/                 # Django settings, root URLs
├── .env.example
└── requirements.txt
```

## Getting Started

```bash
git clone https://github.com/beif3ng/SaintGraal.git
cd SaintGraal
cp .env.example .env  # fill in your values
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## API Endpoints

### Auth

| Method | Endpoint | Description |
|---|---|---|
| POST | `/auth/users/` | Register |
| POST | `/auth/jwt/create/` | Obtain JWT |
| POST | `/auth/jwt/refresh/` | Refresh JWT |

### Finance

| Method | Endpoint | Description |
|---|---|---|
| GET / POST | `/categories/` | List or create categories |
| GET / PUT / DELETE | `/categories/<id>/` | Manage a category |
| GET / POST | `/transactions/` | List or create transactions |
| GET / PUT / DELETE | `/transactions/<id>/` | Manage a transaction |

### Analytics & Export

| Method | Endpoint | Description |
|---|---|---|
| GET | `/analytics/categories/` | Spending/income by category (supports `start_date`, `end_date`) |
| GET | `/analytics/monthly/` | Monthly summary (supports `year`) |
| GET | `/export/csv/` | Download transactions as CSV |
| GET | `/export/pdf/` | Download transactions as PDF |

Swagger UI is available at `/swagger/`.

## Environment Variables

| Variable | Description |
|---|---|
| `SECRET_KEY` | Django secret key |
| `DEBUG` | `1` for development |
| `DB_NAME` | PostgreSQL database name |
| `DB_USER` | PostgreSQL username |
| `DB_PASSWORD` | PostgreSQL password |
| `DB_HOST` | Database host |
| `DB_PORT` | Database port |
