FROM python:3.12-slim
# HTTPS avoids the long-lived port-80 connections that Docker Desktop's proxy
# periodically resets while Debian package indexes are downloading.
RUN sed -i 's|http://deb.debian.org|https://deb.debian.org|g' /etc/apt/sources.list.d/debian.sources \
    && apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*
# The forge always launches Chromium headless. Installing the full Chrome binary as
# well duplicated hundreds of MB and made the Cloudflare registry token expire during
# the initial push. Keep dependencies and the headless browser in separate cacheable
# layers so application-only deploys remain small.
RUN pip install --no-cache-dir playwright pillow
# ``playwright install-deps`` produced one 145 MB compressed blob. Docker Desktop's
# proxy repeatedly dropped that monolithic upload near completion, so keep the same
# official dependency set but split it into resumable/cacheable registry layers.
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt/lists,sharing=locked \
    apt-get update && apt-get install -y --no-install-recommends \
    fonts-freefont-ttf fonts-liberation fonts-tlwg-loma-otf xfonts-scalable
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt/lists,sharing=locked \
    apt-get update && apt-get install -y --no-install-recommends \
    fonts-ipafont-gothic fonts-noto-color-emoji
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt/lists,sharing=locked \
    apt-get update && apt-get install -y --no-install-recommends \
    fonts-unifont fonts-wqy-zenhei
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt/lists,sharing=locked \
    apt-get update && apt-get install -y --no-install-recommends \
    libasound2t64 libatk-bridge2.0-0t64 libatk1.0-0t64 libatspi2.0-0t64 \
    libcairo2 libcups2t64 libdbus-1-3 libdrm2
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt/lists,sharing=locked \
    apt-get update && apt-get install -y --no-install-recommends \
    libfontconfig1 libfreetype6 libgbm1 libglib2.0-0t64 libnspr4 libnss3 libpango-1.0-0
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt/lists,sharing=locked \
    apt-get update && apt-get install -y --no-install-recommends \
    libx11-6 libxcb1 libxcomposite1 libxdamage1 libxext6 libxfixes3 \
    libxkbcommon0 libxrandr2 xvfb
RUN PLAYWRIGHT_DOWNLOAD_CONNECTION_TIMEOUT=120000 playwright install --only-shell chromium
WORKDIR /app
# research_ig.py busca ../.venv-pw/bin/python relativo a scripts/: se le da un venv "fantasma"
# que apunta al python del container (que ya tiene playwright instalado)
RUN mkdir -p /app/.venv-pw/bin && ln -s $(which python3) /app/.venv-pw/bin/python
COPY . /app
CMD ["python3", "main.py"]
