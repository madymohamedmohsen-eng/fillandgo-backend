# ⛽ Fill & Go — Backend API

Django + PostgreSQL backend for the Fill & Go fuel booking app.

## Tech Stack
- **Python 3.11+** / **Django 5** / **Django REST Framework**
- **PostgreSQL** — main database
- **Redis + Celery** — background tasks (reminders, notifications)
- **JWT** — authentication
- **QR Code generation** — per booking
- **Swagger UI** — auto API docs at `/api/docs/`

---

## Quick Start

### 1. Clone & install
```bash
git clone <repo>
cd fillandgo
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure environment
```bash
cp .env.example .env
# Edit .env with your DB credentials
```

### 3. Set up database
```bash
createdb fillandgo_db   # or create via pgAdmin
python manage.py migrate
python manage.py createsuperuser
```

### 4. Run the server
```bash
python manage.py runserver
```

### 5. (Optional) Start Celery for background tasks
```bash
redis-server                         # in one terminal
celery -A fillandgo worker -l info   # in another
celery -A fillandgo beat -l info     # for scheduled tasks
```

---

## API Endpoints

| Method | URL | Description |
|--------|-----|-------------|
| POST | `/api/auth/register/` | Register new user |
| POST | `/api/auth/login/` | Login → get JWT tokens |
| POST | `/api/auth/token/refresh/` | Refresh access token |
| GET/PUT | `/api/auth/profile/` | View/update profile |
| POST | `/api/auth/change-password/` | Change password |
| GET/POST | `/api/auth/vehicles/` | List/add vehicles |
| POST | `/api/auth/vehicles/<id>/set-primary/` | Set primary vehicle |
| GET | `/api/stations/` | List stations (supports ?lat=&lng=&fuel_type=) |
| GET | `/api/stations/<id>/` | Station detail |
| GET | `/api/stations/<id>/slots/?date=YYYY-MM-DD` | Available time slots |
| POST | `/api/stations/<id>/reviews/` | Submit review |
| GET | `/api/bookings/` | My bookings |
| POST | `/api/bookings/create/` | Create booking |
| GET | `/api/bookings/<id>/` | Booking detail + QR code |
| POST | `/api/bookings/<id>/cancel/` | Cancel booking |
| GET/POST | `/api/mobile-services/` | Mobile service requests |
| GET/POST | `/api/roadside/` | Roadside assistance requests |
| GET | `/api/loyalty/` | Loyalty account + tier |
| GET | `/api/loyalty/history/` | Points history |
| POST | `/api/loyalty/redeem/` | Redeem points |
| GET | `/api/reminders/` | Vehicle reminders |
| POST | `/api/reminders/` | Create reminder |
| GET/PUT/DELETE | `/api/reminders/<id>/` | Manage reminder |
| GET | `/api/payments/history/` | Payment history |
| GET | `/api/payments/wallet/` | Wallet balance |
| POST | `/api/payments/wallet/topup/` | Top up wallet |

**Interactive Docs:** `http://localhost:8000/api/docs/`

---

## How the App Makes Money

| Stream | Implementation |
|--------|---------------|
| Station percentage | `platform_fee` field on every `Payment` |
| Banque Misr integration | `method='banque_misr'` on payments |
| Ads | Frontend layer (not in backend) |

---

## Project Structure

```
fillandgo/
├── fillandgo/          # Django project config
│   ├── settings.py
│   ├── urls.py
│   └── celery.py
├── apps/
│   ├── users/          # Auth, User model, Vehicles
│   ├── stations/       # Stations, Fuel types, Slots, Reviews
│   ├── bookings/       # Bookings + QR code generation
│   ├── mobile_services/# At-home car services
│   ├── roadside/       # Emergency roadside assistance
│   ├── loyalty/        # Points, tiers, redemption
│   ├── reminders/      # Vehicle maintenance reminders
│   └── payments/       # Payments + Wallet
├── requirements.txt
└── .env.example
```
