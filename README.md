# Digital No-Dues Clearance System

Full-stack Digital No-Dues Clearance System built with FastAPI, React, Tailwind CSS, PostgreSQL, SQLAlchemy, JWT authentication, ReportLab PDFs, and QR-code certificate verification.

## Structure            

- `backend/` - FastAPI API, SQLAlchemy models, schemas, routers, workflow engine, certificate service
- `frontend/` - React + Vite dashboard UI with Tailwind CSS
- `schema.sql` - PostgreSQL schema

## Backend Setup

1. Ensure PostgreSQL is installed and running locally, and create a database (e.g., `nodues`). Apply `schema.sql` to this database.

2. Create the backend environment file:

```bash
copy backend\.env.example backend\.env
```

3. Install Python dependencies:

```bash
cd backend
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
cd ..
```

4. Run the API from the project root:

```bash
python -m uvicorn backend.main:app --reload
```

The API runs at `http://localhost:8000`, and API docs are available at `http://localhost:8000/docs`.

If `DEFAULT_ADMIN_EMAIL` and `DEFAULT_ADMIN_PASSWORD` are set in `backend/.env`, the app creates that admin account automatically on first startup.

## Frontend Setup

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

## Default Flow

1. Log in as the default admin from `backend/.env`.
2. Create departments in the Admin Dashboard.
3. Create department users and assign each to a department.
4. Create student users.
5. Students log in, apply for clearance, and track department-wise status.
6. Department users approve, reject, or raise a query for assigned requests.
7. Once every department approves, the student can download the generated PDF certificate.
8. The QR code points to `GET /verify/{certificate_id}`, which returns `VALID` or `INVALID`.

## Key API Endpoints

- `POST /auth/login`
- `POST /clearance/apply`
- `GET /clearance/status/{id}`
- `POST /clearance/{id}/action`
- `GET /verify/{certificate_id}`

## Workflow Rules

- `PENDING -> APPROVED`
- `PENDING -> REJECTED`
- `PENDING -> QUERY`
- `QUERY -> PENDING`
- Final request approval happens only when every department approval is `APPROVED`.
- Certificates are generated only for fully approved clearance requests.
 