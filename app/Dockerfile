ARG PYTHON_BASE=3.12-slim

FROM python:$PYTHON_BASE

# install postgres dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    python3-dev \
    build-essential \
    clang

# install PDM
RUN pip install -U pdm
ENV PDM_CHECK_UPDATE=false
COPY pyproject.toml pdm.lock README.md /
COPY /app .

# install dependencies and project into the local packages directory
RUN pdm install --check --prod --no-editable

ENV PATH="/.venv/bin:$PATH"
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
