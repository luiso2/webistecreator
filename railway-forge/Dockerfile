FROM python:3.12-slim
RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir playwright pillow && playwright install --with-deps chromium
WORKDIR /app
# research_ig.py busca ../.venv-pw/bin/python relativo a scripts/: se le da un venv "fantasma"
# que apunta al python del container (que ya tiene playwright instalado)
RUN mkdir -p /app/.venv-pw/bin && ln -s $(which python3) /app/.venv-pw/bin/python
COPY . /app
CMD ["python3", "main.py"]
