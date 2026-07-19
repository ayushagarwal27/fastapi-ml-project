# FastAPI ML Project — Car Price Prediction API

A production-style FastAPI boilerplate for serving Machine Learning models, built around a car price prediction use case. Includes Redis caching, Prometheus metrics, and Grafana dashboards out of the box.

## Features

- ⚡ **FastAPI** application with a clean, modular project structure
- 🤖 **ML model serving** via `joblib` (car price prediction)
- 🗄️ **Redis caching** for prediction results, keyed on input features
- 🔐 **JWT-based authentication**
- 📊 **Prometheus** metrics + **Grafana** dashboards for observability
- 🐳 **Dockerized** with `docker-compose` for local orchestration
- 📓 Dedicated `notebooks/` and `training/` folders for model development

## Project Structure

```
.
├── app/
│   ├── api/            # Route definitions (auth, predict, etc.)
│   ├── cache/          # Redis cache utilities
│   ├── core/           # App-wide config, security, exceptions
│   ├── middleware/      # Custom middleware
│   ├── models/         # Serialized ML model artifacts (e.g. model.joblib)
│   ├── services/        # Business logic (model inference, etc.)
│   └── main.py          # FastAPI app entrypoint
├── data/                 # Datasets used for training
├── notebooks/            # Exploratory analysis & experimentation
├── training/             # Model training scripts/pipeline
├── Dockerfile
├── docker-compose.yml
├── prometheus.yml
├── pyproject.toml
├── requirements.txt
├── uv.lock
└── README.md
```

## Prerequisites

- Python 3.12
- Docker & Docker Compose (recommended for local development)
- [uv](https://github.com/astral-sh/uv) (optional, for dependency management via `pyproject.toml` / `uv.lock`)

## Getting Started

### Option 1 — Run with Docker Compose (recommended)

This spins up the API alongside Redis, Prometheus, and Grafana.

```bash
docker-compose up --build
```

The API will be available at `http://localhost:8000`.

### Option 2 — Run locally

1. Clone the repository:

   ```bash
   git clone https://github.com/ayushagarwal27/fastapi-ml-project.git
   cd fastapi-ml-project
   ```

2. Create a virtual environment and install dependencies:

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # on Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

   Or with `uv`:

   ```bash
   uv sync
   ```

3. Set up environment variables (see [Configuration](#configuration) below).

4. Run the app:

   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

5. Visit the interactive API docs at `http://localhost:8000/docs`.

## Configuration

The app reads configuration from environment variables (see `app/core/config.py`). Create a `.env` file in the project root:

```env
API_KEY=your-api-key
JWT_SECRET_KEY=your-jwt-secret
REDIS_URL=redis://localhost:6379
MODEL_PATH=app/models/model.joblib
```

| Variable         | Description                        | Default                   |
| ---------------- | ---------------------------------- | ------------------------- |
| `API_KEY`        | API key for request authentication | `demo-key`                |
| `JWT_SECRET_KEY` | Secret used to sign JWTs           | `jwt-secret-key`          |
| `REDIS_URL`      | Redis connection string            | `redis://localhost:6379`  |
| `MODEL_PATH`     | Path to the serialized model file  | `app/models/model.joblib` |

## API Endpoints

| Method | Endpoint      | Description                           |
| ------ | ------------- | ------------------------------------- |
| POST   | `/auth/login` | Authenticate and receive a JWT        |
| POST   | `/predict`    | Predict car price from input features |

> Full request/response schemas are available via the auto-generated Swagger docs at `/docs`.

### Example: Predict Car Price

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "make": "Toyota",
    "model": "Corolla",
    "year": 2019,
    "mileage": 42000,
    "fuel_type": "Petrol"
  }'
```

Predictions are cached in Redis based on the input payload, so repeated requests with identical inputs return instantly from cache.

## Model Training

Training scripts and notebooks live in `training/` and `notebooks/`. To retrain and export a new model:

```bash
python training/train.py
```

This should produce a new `model.joblib` file — update `MODEL_PATH` (or overwrite the existing file at `app/models/model.joblib`) to use it.

## Monitoring

- **Prometheus** scrapes metrics from the API using the configuration in `prometheus.yml`.
- **Grafana** can be pointed at the Prometheus data source to visualize request latency, throughput, and error rates.

When running via `docker-compose`, Prometheus and Grafana are started alongside the API automatically.

## Tech Stack

- **FastAPI** — web framework
- **joblib** — model serialization/loading
- **Redis** — caching layer
- **Prometheus / Grafana** — monitoring & observability
- **Docker / Docker Compose** — containerization

## Contributing

Issues and pull requests are welcome. Please open an issue first to discuss any significant changes.

## License

Specify your license here (e.g. MIT).
