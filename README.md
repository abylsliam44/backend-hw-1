# Task Management Application

A full-stack task management application built with FastAPI and modern web technologies.

## Features

- User authentication with JWT
- CRUD operations for tasks
- PostgreSQL database integration
- Docker and Docker Compose support
- CI/CD with GitHub Actions
- Modern web frontend with Tailwind CSS

## Prerequisites

- Docker and Docker Compose
- Python 3.9+
- Node.js (for frontend development)

## Getting Started

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-name>
```

2. Create a `.env` file in the root directory:
```bash
DATABASE_URL=postgresql://postgres:postgres@db:5432/task_manager
SECRET_KEY=your-secret-key-change-in-production
```

3. Start the application using Docker Compose:
```bash
docker-compose up --build
```

The application will be available at:
- Backend API: http://localhost:8000
- Frontend: Open `frontend/index.html` in your browser

## API Documentation

Once the application is running, you can access the API documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Development

### Backend Development

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the development server:
```bash
uvicorn app.main:app --reload
```

### Frontend Development

The frontend is a simple HTML/JS application using Tailwind CSS. To modify:

1. Edit files in the `frontend` directory
2. Open `frontend/index.html` in your browser

## Testing

Run tests using pytest:
```bash
pytest
```

## Deployment

The application includes GitHub Actions workflows for CI/CD. To deploy:

1. Set up the following secrets in your GitHub repository:
   - `DOCKER_USERNAME`
   - `DOCKER_PASSWORD`

2. Push to the main branch to trigger the workflow

## License

MIT 