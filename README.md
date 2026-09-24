# Job Application Tracker
 
![CI](https://github.com/SameerProDev/Job-Tracker/actions/workflows/ci.yml/badge.svg)
 
A REST API with a small web UI for tracking job applications through the hiring pipeline: **applied → interview → offer / rejected**. I built it to manage my own job search.
 
## Features
 
- Full CRUD for applications (company, role, status, link, notes, date)
- Filter by status and view pipeline statistics
- Input validation with clear error messages
- Automated tests (pytest) and CI with GitHub Actions
- Docker support for easy deployment
## Tech Stack
 
Python 3.12, Flask, Flask-SQLAlchemy, SQLite, Gunicorn, pytest, Docker, GitHub Actions
 
## Getting Started
 
```bash
git clone https://github.com/SameerProDev/Job-Tracker.git
cd Job-Tracker
```
 
Create a virtual environment and activate it:
 
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate
 
# Mac / Linux
python -m venv .venv
source .venv/bin/activate
```
 
Install dependencies and run:
 
```bash
pip install -r requirements.txt
python run.py
```
 
Open http://127.0.0.1:5000.
 
### With Docker
 
```bash
docker build -t job-tracker .
docker run -p 8000:8000 job-tracker
```
 
Open http://localhost:8000.
 
### Run the tests
 
```bash
pytest -q
```
 
## API Reference
 
| Method | Endpoint                 | Description                             |
|--------|--------------------------|-----------------------------------------|
| GET    | `/api/applications`      | List all (optional `?status=interview`) |
| POST   | `/api/applications`      | Create (`company` and `role` required)  |
| GET    | `/api/applications/<id>` | Get one                                 |
| PUT    | `/api/applications/<id>` | Update any fields                       |
| DELETE | `/api/applications/<id>` | Delete                                  |
| GET    | `/api/stats`             | Totals grouped by status                |
 
Example:
 
```bash
curl -X POST http://127.0.0.1:5000/api/applications \
  -H "Content-Type: application/json" \
  -d '{"company": "Acme", "role": "Junior Developer"}'
```
 
## Project Structure
 
```
app/            Flask app (factory, models, routes, static UI)
tests/          pytest test suite
.github/        CI workflow
Dockerfile      Container image
```
 
## Design Decisions
 
- **Application factory** pattern so tests can create an isolated in-memory database.
- **Validation in one place** (`validate()`), returning field-level errors.
- **SQLite** keeps setup zero-config; switching to PostgreSQL only needs a new `SQLALCHEMY_DATABASE_URI`.
## Roadmap
 
- [ ] User accounts with JWT authentication
- [ ] Reminders for follow-ups
- [ ] PostgreSQL and database migrations (Flask-Migrate)
- [ ] Pagination and search
- [ ] Live deployment (Render/Railway)
## License
 
MIT