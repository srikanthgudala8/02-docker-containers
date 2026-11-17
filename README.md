# 02 - Docker and Containers

Phase 2 of the 60-day journey from support engineer to DevOps engineer.
Day-by-day plan: **[LEARNING.md](LEARNING.md)** (Days 13-18).

## Project: three-tier visit counter

```
Browser ─► nginx :8080 ─► Flask app (gunicorn) ─► Redis (volume)
           [frontend net]  [frontend + backend]     [backend net only]
```

| Concept | Where to look |
|---------|---------------|
| Multi-stage build, non-root, healthcheck | `app/Dockerfile` |
| Build-cache friendly layer order | `app/Dockerfile` |
| Network isolation | `docker-compose.yml` (Redis only on `backend`) |
| Data persistence | `redis-data` named volume |
| Health-based start order | `depends_on: condition: service_healthy` |
| Reverse proxy | `nginx/nginx.conf` |
| A bad Dockerfile to critique | `labs/bad.Dockerfile` |

## Run it

```bash
docker compose up --build
curl http://localhost:8080/          # {"message": "Hello from Docker", "visits": 1, ...}
curl http://localhost:8080/          # visits: 2
docker compose down                  # keeps the data volume
docker compose down -v               # deletes it too
```

Run the unit tests without Docker:

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt && pytest -q
```

Next phase: **03-github-actions-cicd**.
