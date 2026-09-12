FROM python:3.12-slim
RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*
# The forge always launches Chromium headless. Installing the full Chrome binary as
# well duplicated hundreds of MB and made the Cloudflare registry token expire during
# the initial push. Keep dependencies and the headless browser in separate cacheable
# layers so application-only deploys remain small.
RUN pip install --no-cache-dir playwright pillow
RUN playwright install-deps chromium
RUN playwright install --only-shell chromium
WORKDIR /app
# research_ig.py busca ../.venv-pw/bin/python relativo a scripts/: se le da un venv "fantasma"
# que apunta al python del container (que ya tiene playwright instalado)
RUN mkdir -p /app/.venv-pw/bin && ln -s $(which python3) /app/.venv-pw/bin/python
COPY . /app
CMD ["python3", "main.py"]
