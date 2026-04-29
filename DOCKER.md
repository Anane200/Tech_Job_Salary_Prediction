# Running in Docker

The app ships with a `Dockerfile` and a `docker-compose.yml` so it can
be hosted anywhere Docker runs (local laptop, VM, Kubernetes, Fly.io,
Render, Cloud Run, etc.).

## Quick start

```bash
docker compose up -d --build
```

Open <http://localhost:8501>. Stop with:

```bash
docker compose down
```

## Without compose

```bash
docker build -t tech-job-salary-prediction .
docker run --rm -p 8501:8501 tech-job-salary-prediction
```

## What is in the image

- `python:3.11-slim` base
- `libgomp1` (required at runtime by XGBoost / LightGBM)
- `app.py`
- `best_salary_model_improved.joblib` (the trained XGBoost model)
- `Data/job_salary_prediction_dataset.csv` (reference rows for the
  dropdowns and the Data Insights tab)
- `images/` (model-performance plots shown in the Visualizations tab)

The training notebook, docs, `.git/`, virtualenvs and legacy
artefacts are excluded via `.dockerignore` to keep the build context
and final image minimal.

## Regenerating the model inside the build

The image ships a pre-trained model so the container starts in
seconds. If you change the notebook and want the image to retrain on
each build, add a training step to the Dockerfile before `COPY
best_salary_model_improved.joblib`. A quick way is:

```dockerfile
RUN pip install jupyter nbconvert \
    && jupyter nbconvert --to notebook --execute notebook.ipynb
```

Expect a build-time cost of several minutes on a laptop CPU.

## Health

Both the container and the compose service expose a healthcheck
against Streamlit's `/_stcore/health` endpoint:

```bash
docker inspect -f '{{.State.Health.Status}}' salary-app
```

Should report `healthy` about 20 seconds after start.

## Troubleshooting

- **`OSError: libgomp.so.1: cannot open shared object file`** — you
  are running an image built from a different base. The provided
  Dockerfile already installs `libgomp1`; make sure you rebuild from
  the repo's Dockerfile rather than a stale image.
- **Port 8501 already in use** — change the host side of the port
  mapping in `docker-compose.yml` (for example `"8080:8501"`).
- **Model file missing at startup** — you likely excluded
  `best_salary_model_improved.joblib` via `.dockerignore` or forgot
  to generate it. Run `notebook.ipynb` end-to-end before building.
