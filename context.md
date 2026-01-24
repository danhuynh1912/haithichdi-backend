This project builds a management and booking system for a Trekking Tours Provider.

### Project Goals
- Allow customers to view information about trekking tours, itineraries, images, and make tour bookings.
- Provide an Admin interface (Django Admin) for the provider to manage tours, customers, and the leader team.
- Manage guest capacity (slots) for each tour and allocate appropriate leaders.

### Current Tech Stack
- **Backend:** Django 5.x
- **Database:** PostgreSQL 16
- **Storage:** MinIO (S3 compatible) for storing tour images.
- **Frontend:** Next.js 15 (App Router), TypeScript, Tailwind CSS.
- **Infra:** Docker & Docker Compose.

### Implementation Details (Codebase)

#### 1. Backend (Django)
The system is divided into 2 main apps:
- **`accounts`**: Custom User model (`User`) supporting multiple roles: `admin`, `leader`, `customer`.
- **`tours`**: Manages the core logic of the system.
    - `Tour`: Stores title, summary, itinerary (Markdown), start/end dates, location, and maximum guests (`max_guests`). It has a Many-to-Many relationship with `User` to manage `leaders`.
    - `Booking`: Manages customer registration information. It has a Unique constraint (`tour`, `phone`) to prevent duplicate registrations for the same tour. Supports statuses: `pending`, `confirmed`, `cancelled`.
    - `Location`: Stores location information (name, elevation).
    - `TourImage`: Stores images for tours, supporting both `image` field (upload to MinIO) and `image_url`.

#### 2. Frontend (Next.js)
- Uses Next.js App Router.
- Modern interface with Tailwind CSS.
- Integrated Framer Motion for page transition effects (`page-transition.tsx`).
- Connects to the backend via API (`NEXT_PUBLIC_API_BASE_URL`).

#### 3. Infrastructure (Docker)
The system runs with 5 services:
- `db`: PostgreSQL database.
- `backend`: Django API server.
- `frontend`: Next.js development server.
- `minio`: Media asset storage.
- `minio-init`: Automatically initializes the bucket and permissions for MinIO when the system starts.

### Key Business Rules
- **Slot Management:** Each tour has `max_guests`. The number of remaining slots is calculated based on the existing `Booking` records for that tour.
- **Leader Assignment:** Each tour can be allocated 2-5 leaders depending on its size.
- **Booking Uniqueness:** Ensures no duplicate phone numbers are registered for the same tour (Handled via `UniqueConstraint` in the DB).
- **Transaction:** Booking operations must ensure data integrity, especially when checking available slots.
