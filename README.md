# ToC-API

ToC-API is a Django REST Framework API project with PostgreSQL as its database.

## Tech Stack

- Python
- Django 6.1
- Django REST Framework
- PostgreSQL
- `psycopg` / `psycopg-binary`
- `python-dotenv`
- Ruff

## Project Structure

```text
ToC-API/
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── src/
│   ├── users/
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── migrations/
│   ├── credit_cards/
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   └── migrations/
│   └── masking_data/
│       ├── models.py
│       ├── serializers.py
│       ├── views.py
│       ├── urls.py
│       ├── migrations/
│       ├── queries/
│       │   └── masking_data_queries.py
│       └── services/
│           └── masking_data_service.py
├── shared/
│   └── masked_and_pattern/
│       ├── pattern.py
│       └── masked.py
├── manage.py
├── requirements.txt
├── pyproject.toml
└── .env.example
```

## Requirements

Install the following before starting:

- Python 3.12+ recommended
- PostgreSQL
- Git (optional, if you are cloning the repository)

Check Python:

```bash
python --version
```

Check PostgreSQL:

```bash
psql --version
```

## 1. Get the Project

If you have the ZIP file, extract it first:

```text
ToC-API/
```

Open a terminal inside the directory containing `manage.py`.

For example:

```bash
cd ToC-API
```

## 2. Create a Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

If PowerShell blocks activation, you can run:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then activate again:

```powershell
venv\Scripts\Activate.ps1
```

### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

After activation, your terminal should show something similar to:

```text
(venv)
```

## 3. Install Dependencies

Run:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 4. Configure Environment Variables

Copy `.env.example` to `.env`.

### Windows

```cmd
copy .env.example .env
```

### macOS / Linux

```bash
cp .env.example .env
```

Open `.env` and configure it.

Example:

```env
DEBUG=True
SECRET_KEY=change-this-to-a-long-random-secret-key

ALLOWED_HOSTS=127.0.0.1,localhost

DB_NAME=toc_db
DB_USER=postgres
DB_PASSWORD=your-postgres-password
DB_HOST=localhost
DB_PORT=5432
```

## 5. Create the PostgreSQL Database

Make sure PostgreSQL is running.

Open PostgreSQL using `psql` or another PostgreSQL client and create the database:

```sql
CREATE DATABASE toc_db;
```

The database name, username, password, host, and port must match the values in `.env`.

For example, if your PostgreSQL username is `postgres`:

```env
DB_NAME=toc_db
DB_USER=postgres
DB_PASSWORD=your-postgres-password
DB_HOST=localhost
DB_PORT=5432
```

## 6. Run Database Migrations

From the project directory, run:

```bash
python manage.py makemigrations
python manage.py migrate
```

You can verify the migration state with:

```bash
python manage.py showmigrations
```

## 7. Create an Admin User

To access Django Admin, create a superuser:

```bash
python manage.py createsuperuser
```

Follow the prompts for username, email, and password.

## 8. Start the Development Server

Run:

```bash
python manage.py runserver
```

The API should be available at:

```text
http://127.0.0.1:8000/
```

Keep the terminal running while using the API.

To stop the server, press:

```text
Ctrl + C
```

## 9. Run Tests

Run the masking data tests with:

```bash
python manage.py test src/masking_data
```

Note: plain `python manage.py test` currently discovers no tests because `src/` is a namespace package — always pass the app path as above.

## 10. Code Quality

Ruff is included in the project dependencies.

To check the code:

```bash
ruff check .
```

To format the code:

```bash
ruff format .
```

## 11. Common Problems

### `ModuleNotFoundError: No module named 'django'`

Make sure the virtual environment is activated and dependencies are installed:

```bash
venv\Scripts\activate
pip install -r requirements.txt
```

On macOS/Linux:

```bash
source venv/bin/activate
pip install -r requirements.txt
```

### PostgreSQL connection error

Check that:

1. PostgreSQL is running.
2. `DB_NAME` exists.
3. `DB_USER` is correct.
4. `DB_PASSWORD` is correct.
5. `DB_HOST` and `DB_PORT` are correct.

For a local PostgreSQL installation, these are commonly:

```env
DB_HOST=localhost
DB_PORT=5432
```

### `relation does not exist`

Run the migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

### Port 8000 is already in use

Start Django on another port:

```bash
python manage.py runserver 8001
```

Then use:

```text
http://127.0.0.1:8001/
```

## 12. Development Workflow

A typical development session looks like this:

```bash
# Enter project
cd ToC-API

# Activate virtual environment
# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate

# Install/update dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# Start API
python manage.py runserver
```

Then test:

```text
GET http://127.0.0.1:8000/api/user/
GET http://127.0.0.1:8000/api/masking-data/
```

## 13. Notes About the Current Project

The repository currently has the basic Django/DRF structure in place.

- `src/users` contains a custom Django `User` model based on `AbstractUser`.
- `src/masking_data` contains a `MaskingData` model.
- `src/credit_cards` contains a `CreditCard` model with encrypted `number` and a `masked_number`.
- Sensitive fields (`email`, `phone_number`, `dob`, `address`, card `number`) are encrypted via `django-encrypted-model-fields`.
- `PUT` and `PATCH` on `/api/masking-data/<id>/` update the editable fields and regenerate their masked counterparts.
- `POST` and `DELETE` are placeholders and still need implementation.
- `masking_data` follows a layered structure: views handle HTTP, serializers validate input, `services/` contains the update business logic (masking, credit-card co-update, transaction), and `queries/` handles all database access.
- PostgreSQL is configured as the default database.
- Authentication/authorization and API permissions should be added if the API will be exposed beyond local development.

## API Endpoints

### Update masking data

`PUT /api/masking-data/<id>/` — full replacement. All five editable fields are required.

Request:

```json
{
  "email": "new@example.com",
  "phone_number": "081-234-5678",
  "dob": "DOB:01/01/2000",
  "address": "Address: 123 ถนนสุขุมวิท แขวงคลองเตย เขตคลองเตย กรุงเทพมหานคร",
  "credit_card": "1234-1234-1234-1234"
}
```

`PATCH /api/masking-data/<id>/` — partial update. Only the supplied fields change.

Request:

```json
{
  "email": "new@example.com"
}
```

Responses:

- `200 OK` — updated. The server stores the encrypted value and regenerates the corresponding masked value for each supplied field. The response returns the stored masked fields only — raw sensitive values are never echoed back:

  ```json
  {
    "id": 1,
    "masked_email": "n**@example.com",
    "masked_phone_number": "XXX-XXX-9999",
    "masked_dob": "DOB:**/**/01",
    "masked_address": "...",
    "status": "ACTIVE"
  }
  ```
- `400 Bad Request` — a supplied field fails validation (e.g. invalid email format).
- `404 Not Found` — no record exists for the given `id`.

Writable fields: `email`, `phone_number`, `dob`, `address`, `credit_card`. The masked fields, `user`, `status`, and timestamps are server-controlled and cannot be set by the client. Updating `credit_card` reuses the existing `CreditCard` object rather than creating a new one.

## Quick Start

If Python and PostgreSQL are already installed:

```bash
cd ToC-API

python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
# source venv/bin/activate

pip install -r requirements.txt
```

Create and configure `.env`, create the PostgreSQL database, then run:

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/api/user/
```

You should receive:

```json
{
  "message": "Response from UserView GET method"
}
```
