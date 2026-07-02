# Study Sync

**Learn Together. Schedule Smarter.**

Study Sync is a production-ready academic scheduling SaaS built with **Python Flask**, **MySQL**, and **Bootstrap 5**. It provides role-based portals for students, lecturers, and admins with calendar views, time-slot booking, attendance tracking, and in-app notifications.

## Features

- Modern responsive UI (Notion + Calendly inspired)
- Blue & white theme with **dark mode toggle**
- Bootstrap Icons and smooth animations
- Student registration & login
- Lecturer and admin login portals
- Student, lecturer, and admin dashboards
- Class catalog with **search & filter**
- **Calendar view** (FullCalendar)
- **Time-slot booking** with double-booking prevention
- Booking cancellation
- **User profiles** for all roles
- **Attendance tracking** (lecturer)
- **In-app notifications**
- Email confirmation **placeholders** (ready for SMTP)
- Secure authentication with **hashed passwords**
- Clean **MVC folder structure**

## Project Structure

```text
Class booking system/
├── run.py                      # Application entry point
├── app.py                      # Legacy entry (delegates to run.py)
├── requirements.txt
├── database.sql
├── .env.example
├── scripts/
│   └── seed_users.py           # Generate password hashes for seed users
├── study_sync/                 # Application package
│   ├── __init__.py             # App factory
│   ├── config.py
│   ├── extensions.py
│   ├── decorators.py
│   ├── controllers/            # Flask blueprints (routes)
│   ├── models/                 # Data access layer
│   ├── services/               # Business logic
│   └── utils/
├── templates/
│   ├── layouts/
│   ├── public/
│   ├── auth/
│   ├── student/
│   ├── lecturer/
│   ├── admin/
│   └── partials/
└── static/
    ├── css/main.css
    └── js/
```

## Setup

### 1. Install dependencies

```bash
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

### 2. Configure environment

Copy `.env.example` to `.env` and update values:

```bash
copy .env.example .env
```

### 3. Create database

```bash
mysql -u root -p < database.sql
```

### 4. Seed lecturer & admin passwords

```bash
python scripts/seed_users.py
```

Copy the generated hashes into MySQL:

```sql
UPDATE users SET password_hash='<lecturer_hash>' WHERE email='lecturer@studysync.app';
UPDATE users SET password_hash='<admin_hash>' WHERE email='admin@studysync.app';
```

Default credentials after seeding:
- Lecturer: `lecturer@studysync.app` / `lecturer123`
- Admin: `admin@studysync.app` / `admin123`

Students register via the app at `/auth/register`.

### 5. Run the application

```bash
python run.py
```

Visit: http://127.0.0.1:5000

## Pages

| Page | URL |
|------|-----|
| Landing | `/` |
| Contact | `/contact` |
| Student Register | `/auth/register` |
| Student Login | `/auth/login` |
| Lecturer Login | `/auth/lecturer/login` |
| Admin Login | `/auth/admin/login` |
| Student Dashboard | `/student/dashboard` |
| Book Class | `/student/classes` |
| Student Calendar | `/student/calendar` |
| Lecturer Dashboard | `/lecturer/dashboard` |
| Admin Dashboard | `/admin/dashboard` |

## Security

- Passwords hashed with Werkzeug `pbkdf2:sha256`
- Session-based authentication
- Role-based route protection
- Unique DB constraint prevents duplicate slot bookings
- Row locking on slot booking for concurrency safety

## Production Notes

- Set a strong `SECRET_KEY` in production
- Enable `MAIL_ENABLED=true` and wire SMTP in `study_sync/utils/email.py`
- Use a WSGI server (e.g. Gunicorn + Nginx)
- Disable Flask `debug` mode
