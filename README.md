# Legacy Album Organizer

An intelligent photo and video management system built with FastAPI and React. This application uses AI-powered search, face recognition, and semantic understanding to help organize and discover your media library.

## Features

- User authentication and authorization with JWT tokens
- Media upload with automatic metadata extraction
- AI-powered semantic search using OpenAI embeddings
- Face detection and person management with Azure Face API
- Advanced filtering by media type, date range, and people
- Vector similarity search using PostgreSQL with pgvector
- Responsive React frontend with dark mode support
- Real-time search with URL state management

## Tech Stack

### Backend
- FastAPI 0.115.0 - High-performance web framework
- PostgreSQL with pgvector - Vector database for embeddings
- SQLAlchemy 2.0.35 - ORM for database operations
- OpenAI API - Embedding generation and image captioning
- Azure Face API - Face detection and recognition
- Celery & Redis - Asynchronous task processing
- JWT authentication with python-jose

### Frontend
- React 19.2.0 - UI library
- Vite 7.1.12 - Build tool and dev server
- React Router 7.9.5 - Client-side routing
- Axios 1.13.1 - HTTP client
- Tailwind CSS 3.4.14 - Utility-first CSS framework
- React Icons - Icon library

## Prerequisites

- Python 3.10 or higher
- Node.js 18 or higher
- PostgreSQL 14 or higher with pgvector extension
- OpenAI API key
- Azure Face API credentials (optional, for face detection)
- Redis server (for background tasks)

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/adenjc22/Hackathon_2025_Nov.git
cd Hackathon_2025_Nov
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# Install dependencies
pip install -r ../requirements.txt

# Create .env file from example
cp .env.example .env
```

Edit `.env` and configure:
```bash
FRONTEND_URL=http://localhost:5173
OPENAI_API_KEY=your_openai_api_key
AZURE_FACE_KEY=your_azure_face_key
AZURE_FACE_ENDPOINT=your_azure_endpoint
DATABASE_URL=postgresql://user:password@localhost/legacy_album
SECRET_KEY=your-secret-key-here
```

### 3. Database Setup

```bash
# Create PostgreSQL database
createdb legacy_album

# Enable pgvector extension
psql -d legacy_album -c "CREATE EXTENSION IF NOT EXISTS vector;"

# Initialize database tables
python -c "from app.database.init_database import init_db; init_db()"
```

### 4. Frontend Setup

```bash
cd ../frontend

# Install dependencies
npm install

# Create .env file from example
cp .env.example .env
```

Edit `.env` and configure:
```bash
VITE_API_URL=http://localhost:8000
```

## Running the Application

### Development Mode

Terminal 1 - Backend:
```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Terminal 2 - Frontend:
```bash
cd frontend
npm run dev
```

Terminal 3 - Celery Worker (optional, for background tasks):
```bash
cd backend
celery -A app.celery_app worker --loglevel=info
```

Access the application at `http://localhost:5173`

### Production Build

Backend:
```bash
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

Frontend:
```bash
cd frontend
npm run build
npm run preview
```

## Project Structure

```
.
├── backend/
│   ├── app/
│   │   ├── api/routes/        # API endpoints
│   │   ├── core/              # Configuration and security
│   │   ├── database/          # Models and database setup
│   │   ├── schemas/           # Pydantic schemas
│   │   ├── services/          # Business logic
│   │   └── utils/             # AI utilities (OpenAI, Azure)
│   ├── tests/                 # Backend tests
│   ├── uploads/               # Media storage
│   └── main.py               # FastAPI application entry
│
├── frontend/
│   ├── src/
│   │   ├── components/        # Reusable UI components
│   │   ├── pages/            # Page components
│   │   ├── hooks/            # Custom React hooks
│   │   ├── context/          # React context providers
│   │   ├── utils/            # Utilities and API client
│   │   └── styles/           # Global styles
│   └── public/               # Static assets
│
└── requirements.txt          # Python dependencies

```

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `GET /api/users/me` - Get current user

### Media
- `POST /api/upload/media` - Upload media files
- `GET /api/upload/media` - List user media
- `DELETE /api/upload/media/{id}` - Delete media

### Search
- `GET /api/search` - Semantic search across media
- `GET /api/search/similar/{media_id}` - Find similar media
- `POST /api/search/reindex` - Regenerate embeddings

### People
- `GET /api/people` - List detected people
- `PUT /api/people/{id}` - Update person name
- `DELETE /api/people/{id}` - Delete person

### Health
- `GET /api/health` - Health check endpoint

## Environment Variables

### Backend (.env)
| Variable | Description | Required |
|----------|-------------|----------|
| `FRONTEND_URL` | Frontend URL for CORS | Yes |
| `OPENAI_API_KEY` | OpenAI API key for embeddings | Yes |
| `DATABASE_URL` | PostgreSQL connection string | Yes |
| `SECRET_KEY` | JWT token secret key | Yes |
| `AZURE_FACE_KEY` | Azure Face API key | No |
| `AZURE_FACE_ENDPOINT` | Azure Face API endpoint | No |

### Frontend (.env)
| Variable | Description | Required |
|----------|-------------|----------|
| `VITE_API_URL` | Backend API base URL | Yes |

## Testing

### Backend Tests
```bash
cd backend
pytest tests/ -v
```

### Frontend Build Test
```bash
cd frontend
npm run build
```

## Deployment

### Railway (Recommended)

1. Connect your GitHub repository to Railway
2. Set environment variables in Railway dashboard
3. Deploy backend and frontend as separate services
4. Railway will automatically detect and build both services

### Manual Deployment

1. Set up PostgreSQL database with pgvector extension
2. Configure environment variables for production
3. Build frontend: `npm run build`
4. Serve frontend static files
5. Run backend with production ASGI server (uvicorn/gunicorn)

## Troubleshooting

### Database Connection Issues
- Ensure PostgreSQL is running
- Verify DATABASE_URL is correct
- Check pgvector extension is installed

### OpenAI API Errors
- Verify API key is valid
- Check rate limits and quota
- Ensure OpenAI account has credits

### CORS Errors
- Verify FRONTEND_URL in backend .env
- Check frontend VITE_API_URL matches backend URL

### Upload Failures
- Check uploads/ directory exists and is writable
- Verify file size limits in backend configuration
- Ensure media file formats are supported

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project was created for Durhack 2025.

## Contact

Repository: https://github.com/adenjc22/Hackathon_2025_Nov
