# ThreadIQ Macro Insights

A Django-based application for macro insights analysis with Celery background task processing.

## 🚀 Quick Start (Local Development)

### Prerequisites
- Docker and Docker Compose
- Python 3.12+ (for local development without Docker)

### Running with Docker Compose (Recommended)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd threadiq-macro-insights
   ```

2. **Start all services**
   ```bash
   docker-compose up -d
   ```

3. **Access the application**
   - **Django Admin**: http://localhost:8000/admin/
   - **API**: http://localhost:8000/api/
   - **Database Admin**: http://localhost:8080 (Adminer)

### Services Running Locally

- **Web**: Django application on port 8000
- **Worker**: Celery worker for background tasks
- **Beat**: Celery beat scheduler
- **PostgreSQL**: Database on port 5432
- **Redis**: Message broker on port 6379
- **Weaviate**: Vector database on port 8080
- **Adminer**: Database management on port 8080

### Local Development Commands

```bash
# View logs
docker-compose logs -f

# Run Django commands
docker-compose exec web python backend/manage.py shell

# Run migrations
docker-compose exec web python backend/manage.py migrate

# Create superuser
docker-compose exec web python backend/manage.py createsuperuser

# Stop all services
docker-compose down

# Rebuild and restart
docker-compose up -d --build
```

## 🏗️ Architecture

### Backend Structure
```
backend/
├── core/           # Django project settings
├── apps/           # Django applications
│   ├── users/      # User management
│   ├── transcripts/ # Transcript processing
│   ├── insights/   # Insights analysis
│   └── distribution/ # Content distribution
├── requirements.txt # Python dependencies
└── manage.py       # Django management
```

### Key Technologies
- **Django**: Web framework
- **Celery**: Background task processing
- **PostgreSQL**: Primary database
- **Redis**: Message broker and cache
- **Weaviate**: Vector database for embeddings
- **Gunicorn**: WSGI server (production)
- **Uvicorn**: ASGI server (development)

## 🚀 Deployment Pipeline

### Overview
The application uses GitHub Actions for CI/CD and deploys to DigitalOcean App Platform.

### Deployment Flow

1. **Code Push** → GitHub repository
2. **GitHub Actions** → Build Docker image
3. **Push to GHCR** → GitHub Container Registry
4. **Deploy to DigitalOcean** → App Platform

### GitHub Actions Workflow

The `.github/workflows/build-and-push.yaml` workflow:

1. **Triggers on**: Push to `main` branch or pull requests
2. **Builds**: Multi-platform Docker image
3. **Pushes to**: `ghcr.io/threadiq/threadiq-macro-insights`
4. **Deploys to**: DigitalOcean App Platform

### DigitalOcean App Platform

The application is deployed as three components:

- **Web**: Django application serving HTTP requests
- **Worker**: Celery worker processing background tasks
- **Beat**: Celery beat scheduler for periodic tasks

### Environment Variables & Secrets

Sensitive configuration is managed through GitHub Secrets:

- `SECRET_KEY`: Django secret key
- `PGPASSWORD`: PostgreSQL password
- `REDIS_URL`: Redis connection string
- `DIGITALOCEAN_ACCESS_TOKEN`: DO API access token

### Deployment Commands

```bash
# Manual deployment (if needed)
git push origin main  # Triggers automatic deployment

# Check deployment status
doctl apps list
doctl apps get <app-id>
```

## 🔧 Configuration

### Local Environment
Create a `.env` file from the .env.example file. Update the file with your own values as necessary.

### Production Environment
Environment variables are automatically set through DigitalOcean App Platform configuration and GitHub Secrets.

## 🐛 Troubleshooting

### Common Issues

**Static files not loading locally:**
```bash
# Ensure static directory exists
mkdir -p backend/static
docker-compose restart web
```

**Celery worker not starting:**
```bash
# Check Redis connection
docker-compose logs redis
docker-compose restart worker
```

**Database connection issues:**
```bash
# Check PostgreSQL logs
docker-compose logs db
docker-compose restart db
```

### Logs and Debugging

```bash
# View all service logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f web
docker-compose logs -f worker
docker-compose logs -f db
```
