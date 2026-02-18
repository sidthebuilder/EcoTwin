# EcoTwin

EcoTwin is an AI-powered platform for tracking and forecasting personal carbon footprints. It uses graph databases to model complex relationships between user activities and environmental impact, and machine learning to predict future trends.

## Features

- **Carbon Tracking**: Logs daily activities (transport, consumption, energy) and estimates carbon impact.
- **Analytics Engine**: Uses Scikit-learn to forecast future emissions based on historical data.
- **Graph Database**: Maps user activities and their environmental consequences using Neo4j.
- **AI Inference**: Integrates with LLMs to interpret unstructured activity descriptions.
- **Security**: Implements OAuth2 with JWT tokens, rate limiting, and secure headers.
- **Infrastructure**: Fully containerized with Docker and Docker Compose.

## Tech Stack

- **Backend**: Python 3.11, FastAPI, SQLAlchemy, Pydantic
- **Frontend**: React, TypeScript, Tailwind CSS, Recharts
- **Database**: PostgreSQL (Relational), Neo4j (Graph), Redis (Cache/Queue)
- **DevOps**: Docker, Nginx

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Node.js 18+ (for local development)
- Python 3.11+ (for local development)

### Deployment

Run the deployment script to build and start all services:

```bash
./deploy.sh
```

This script will:
1. Start PostgreSQL, Neo4j, and Redis containers.
2. Build the backend and frontend images.
3. Apply database migrations.
4. Start the application services.

### Accessing the Application

- **Frontend Dashboard**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/api/v1/health

## Project Structure

- `backend/`: FastAPI application, database models, and analytics logic.
- `frontend/`: React application for the user dashboard.
- `deploy.sh`: Automated deployment script.
- `docker-compose.yml`: Service orchestration configuration.

## License

MIT
