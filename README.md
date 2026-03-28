# Hai Thich Di Backend

Backend API for the `Hai Thich Di` trekking management and booking platform, built with Django and Django REST Framework.

## 1. Product Context

The backend serves two core needs:
- Public API layer for the frontend (locations, tours, leaders, booking).
- Back-office operations through Django Admin (tour, booking, user, and media management).

Business goals:
- Manage tour capacity (slot management).
- Prevent duplicate registrations by phone number per tour.
- Store media and quotation PDFs via S3-compatible storage locally and AWS S3 in production.

## 2. Recruiter Highlights

Engineering signals in this backend:
- Domain-based app split: `accounts` and `tours`.
- Clean DRF generic views + serializers for maintainability.
- Booking validation at serializer level plus DB constraint (defense in depth).
- Accent-insensitive search using PostgreSQL `UNACCENT` extension.
- Storage abstraction through `django-storages` for local/S3-compatible flexibility.
- Practical Django Admin customization for real operations.

## 3. Tech Stack

- Language: `Python 3.12`
- Framework: `Django 5.x`
- API: `Django REST Framework`
- Database: `PostgreSQL 16`
- File/Object Storage:
  - local: `MinIO` (S3 protocol)
  - production: `AWS S3` + `CloudFront`
- Infrastructure:
  - local: `Docker`, `Docker Compose`
  - production: `AWS Lambda`, `API Gateway`, `RDS`, `VPC`, `S3`, `CloudFront`, `Terraform`

Main dependencies in `requirements.txt`:
- `Django`, `djangorestframework`, `django-cors-headers`
- `psycopg2-binary`
- `django-storages`, `boto3`
- `pillow`

## 4. Domain Model

### `accounts.User` (custom user)

Extends `AbstractUser` with:
- `role`: `admin | leader | customer`
- profile fields: `avatar`, `bio`, `strengths`, `display_role`, `relationship_status`, `years_experience`, etc.

### `tours.Location`

- `name`, `elevation_m`, `description`
- `image` / `image_url`
- `quotation_file` (PDF used in booking flow)

### `tours.Tour`

- `title`, `summary`, `itinerary_md`
- `start_date`, `end_date`
- `location` (FK)
- `max_guests`, `leaders`, `is_active`
- computed properties: `booked_count`, `slots_left`

### `tours.TourImage`

- Tour gallery image (`image` or `image_url`)
- Sorted with `sort_order`

### `tours.Booking`

Registration fields:
- `full_name`, `phone`, `email`, `note`
- required business fields: `medal_name`, `dob`, `citizen_id`
- `status`: `pending | confirmed | cancelled`

Critical constraint:
- Unique pair `(tour, phone)`.

## 5. Business Rules

- Booking allowed only for active tours (`is_active=True`).
- Booking rejected when `slots_left <= 0`.
- `medal_name`, `dob`, and `citizen_id` are mandatory.
- Duplicate phone number is blocked for the same tour.

Validation is enforced in serializers and protected at database level via `UniqueConstraint`.

## 6. API Endpoints

Base path: `/api/`

- `GET /locations/` -> locations (`full_image_url`, `quotation_file_url`)
- `GET /tours/hot/` -> upcoming hot tours
- `GET /tours/` -> tour list
  - Query params:
    - `location_id=1,2`
    - `search=ta chi nhu`
    - `ordering=start_date|-start_date`
- `GET /tours/<id>/` -> tour detail
- `POST /bookings/` -> create booking
- `GET /leaders/` -> leader profiles

### Booking request example

```json
{
  "tour": 1,
  "full_name": "Nguyen Van A",
  "phone": "0900000000",
  "email": "a@example.com",
  "note": "Need more consultation",
  "medal_name": "NGUYEN VAN A",
  "dob": "1998-05-13",
  "citizen_id": "012345678901"
}
```

### Booking success response example

```json
{
  "id": 10,
  "tour": 1,
  "full_name": "Nguyen Van A",
  "phone": "0900000000",
  "email": "a@example.com",
  "note": "Need more consultation",
  "medal_name": "NGUYEN VAN A",
  "dob": "1998-05-13",
  "citizen_id": "012345678901",
  "status": "pending"
}
```

## 7. Request Flow Architecture

```text
HTTP Request
  -> Django URLConf (backend/urls.py)
  -> DRF View (ListAPIView/CreateAPIView/...)
  -> Serializer (validation + response shaping)
  -> ORM Query (models)
  -> PostgreSQL / object storage
  -> JSON Response
```

## 8. Django Admin (Back-office)

Entry: `/admin/`

Operational customizations:
- `TourAdmin`: slot visibility, filtering, search, inline images, leader assignment.
- `BookingAdmin`: filter by status, search by phone/citizen ID/name.
- `CustomUserAdmin`: additional profile fields for leaders/customers.

## 9. Environment Variables

Main settings (defaults exist in code/compose):

- `DJANGO_SECRET_KEY`
- `DJANGO_DEBUG` (`1` to enable debug)
- `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`
- `POSTGRES_HOST`, `POSTGRES_PORT`
- `USE_S3` (`1` to enable object storage)
- `AWS_STORAGE_BUCKET_NAME`
- `AWS_S3_REGION_NAME`
- `AWS_S3_CUSTOM_DOMAIN` or `AWS_S3_PUBLIC_BASE_URL`
- `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` only when not using IAM roles
- `AWS_S3_ENDPOINT_URL`, `AWS_S3_PUBLIC_ENDPOINT_URL`, `AWS_S3_ADDRESSING_STYLE` only for local MinIO / S3-compatible storage

See also:

- `docs/AWS_PLATFORM_ARCHITECTURE.md`

## 10. Run Locally (Without Docker)

Prerequisites:
- Python 3.12+
- PostgreSQL 16

Setup commands:

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```

Create admin account:

```bash
python manage.py createsuperuser
```

Note: migration `0010_enable_unaccent` requires PostgreSQL `unaccent` extension support.

## 11. Run with Docker Compose (Recommended)

From repository root:

```bash
docker compose --env-file ./frontend/.env up -d --build
```

This starts:
- `db` (PostgreSQL)
- `backend` (Django API)
- `frontend` (Next.js)
- `minio` + `minio-init`

## 12. Project Structure

```text
backend/
  accounts/
    models.py
    serializers.py
    views.py
    urls.py
    admin.py
  tours/
    models.py
    serializers.py
    views.py
    urls.py
    admin.py
    migrations/
  backend/
    settings.py
    urls.py
    asgi.py
    wsgi.py
  manage.py
  Dockerfile
```

## 13. Security & Quality Notes

- CORS configured for local frontend origins (`localhost:3000`, `localhost:3001`).
- Public endpoints currently unauthenticated (fits current MVP stage).
- DB-level uniqueness protects booking data integrity.
- Production hardening opportunities: auth, rate limiting, audit logging.

## 14. Current Gaps / Next Improvements

- No automated tests yet (unit/integration/API).
- No pagination yet on tour list endpoints.
- No API auth/permission model yet beyond Django Admin auth.
- Could introduce domain services if business complexity grows.
