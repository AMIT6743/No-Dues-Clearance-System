# Digital No-Dues Clearance System

> **Live Demo:** [https://no-dues-clearance-system-5wef.onrender.com](https://no-dues-clearance-system-5wef.onrender.com/)

Full-stack Digital No-Dues Clearance System built with **FastAPI**, **React**, **Tailwind CSS**, **SQLAlchemy**, **JWT authentication**, **ReportLab PDFs**, and **QR-code certificate verification**.

## Features

- **Role-Based Access Control** — Admin, Department Manager, and Student roles
- **Clearance Workflow** — Students apply, departments approve/reject/query
- **PDF Certificate Generation** — Auto-generated certificates with QR code verification
- **Single Deployable Container** — Backend serves the built frontend via Docker

## Tech Stack

| Layer     | Technology                        |
|-----------|-----------------------------------|
| Backend   | FastAPI, SQLAlchemy, Passlib, JWT |
| Frontend  | React, Vite, Tailwind CSS         |
| Database  | SQLite (dev) / PostgreSQL (prod)  |
| Deploy    | Docker, Render                    |

## Project Structure

```
├── backend/          # FastAPI API, models, schemas, routes, services
├── frontend/         # React + Vite dashboard UI with Tailwind CSS
├── scripts/          # Utility scripts for seeding data
├── Dockerfile        # Multi-stage build (frontend + backend)
├── .dockerignore     # Optimized Docker build context
└── schema.sql        # Database schema reference
```

## Local Development Setup

### Backend

1. Create the backend environment file:

```bash
copy backend\.env.example backend\.env
```

2. Install Python dependencies:

```bash
cd backend
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
cd ..
```

3. Run the API from the project root:

```bash
python -m uvicorn backend.main:app --reload
```

The API runs at `http://localhost:8000`, and API docs are available at `http://localhost:8000/docs`.

If `DEFAULT_ADMIN_EMAIL` and `DEFAULT_ADMIN_PASSWORD` are set in `backend/.env`, the app creates that admin account automatically on first startup.

### Frontend

1. Create the frontend environment file:

```bash
copy frontend\.env.example frontend\.env
```

2. Install and run:

```bash
cd frontend
npm install
npm run dev
```

The frontend runs at `http://localhost:5173`.

### Docker (Full Stack)

```bash
docker build -t nodues-app .
docker run -p 8000:8000 \
  -e DATABASE_URL=sqlite:///./dev_nodues.db \
  -e SECRET_KEY=your-secret-key \
  -e DEFAULT_ADMIN_EMAIL=admin@college.edu \
  -e DEFAULT_ADMIN_PASSWORD=admin12345 \
  -e DEFAULT_ADMIN_NAME="System Admin" \
  nodues-app
```

## Default Workflow

1. Log in as the default admin (`admin@college.edu` / `admin12345`).
2. Create departments in the Admin Dashboard.
3. Create department manager users and assign each to a department.
4. Create student users.
5. Students log in, apply for clearance, and track department-wise status.
6. Department managers approve, reject, or raise a query for assigned requests.
7. Once every department approves, the student can download the generated PDF certificate.
8. The QR code on the certificate points to `/verify/{certificate_id}` for verification.

## Key API Endpoints

| Method | Endpoint                     | Description              |
|--------|------------------------------|--------------------------|
| POST   | `/auth/login`                | User login               |
| POST   | `/clearance/apply`           | Apply for clearance      |
| GET    | `/clearance/status`          | Check clearance status   |
| POST   | `/clearance/{id}/action`     | Approve/Reject/Query     |
| POST   | `/certificate/generate/{id}` | Generate PDF certificate |
| GET    | `/verify/{certificate_id}`   | Verify certificate       |

## Workflow Rules

| Transition            | Allowed           |
|-----------------------|-------------------|
| `PENDING → APPROVED`  | ✅                |
| `PENDING → REJECTED`  | ✅                |
| `PENDING → QUERY`     | ✅                |
| `QUERY → PENDING`     | ✅ (student reply) |

- Final clearance approval happens only when **every** department approval is `APPROVED`.
- Certificates are generated only for fully approved clearance requests.