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

### Latest Changes
- Rewrote `frontend/README.md` and `backend/README.md` in English for recruiter-facing technical review.
- Added comprehensive recruiter-facing README documentation for both `frontend/` and `backend/`, covering context, architecture, tech stack, setup, API contracts, and engineering trade-offs.
- Location detail modal is now full-screen, shows the location's quotation PDF (if available) instead of the image, and removes the framer-motion morph animation.
- Location API now exposes `quotation_file_url`; frontend Location type updated accordingly.
- Opening a location detail sets `?name={slug}` in the URL; reloading with that query auto-focuses the matching location card and reopens the modal.
- PDF panel width set to 50% of the screen within the location detail modal.
- PDF viewer now hides the default sidebar/toolbar via URL params.
- Modal overlay/content now animates in/out with a subtle scale + fade.
- Backend adds `GET /api/tours/<id>/` and `POST /api/bookings/` (with validation on tour active/slots and duplicate phone).
- New booking page at `/tour-booking/[tourId]`: left PDF preview (50% width, toolbar hidden), right booking form using React 19 hooks (`useActionState`, `useFormStatus`) posting to create a Booking.
- Clicking a tour inside the location detail modal navigates to `/tour-booking/{tourId}`.
- Tour booking page now fetches tour detail via React Query (`useQuery`).
- Added a back arrow button in the booking page header to return to the previous page.
- Created reusable `BookingFlowHeader` component for breadcrumb/back UI in booking flow; booking page uses it.
- Added SEO helpers (`lib/seo.ts`) and root metadata template (title template, OG/Twitter, canonical). Home and Locations pages now export metadata via server files. Tour booking page uses server `generateMetadata` to set dynamic title/OG per tour (fallback when API unreachable).
- Header is now fixed (sticky top) with blurred gradient background (from black to transparent); page content padded to avoid overlap.
- Booking form now requires medal name, date of birth, and citizen ID; backend Booking model/serializer/API accept and validate these fields.
- Added Tours listing page with filters (locations, upcoming sort), debounced search, shared tour fetching hook, and reusable TourCard; header nav links to /tours.
- All tours API calls now go through `tourService` (list, detail, hot, bookings), `useTours` reuses the service for SDK-like layering.

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
