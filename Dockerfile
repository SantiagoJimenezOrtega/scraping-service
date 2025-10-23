FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# Instalar Python y dependencias
RUN apt-get update && apt-get install -y \
    python3.11 \
    python3-pip \
    python3.11-venv \
    curl \
    wget \
    libnss3 \
    libnspr4 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libasound2 \
    libdbus-1-3 \
    fonts-liberation \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Crear symlink para python
RUN ln -sf /usr/bin/python3.11 /usr/bin/python

WORKDIR /app

# Copiar requirements
COPY requirements.txt .

# Actualizar pip y setuptools
RUN python -m pip install --upgrade pip setuptools wheel

# Instalar dependencias Python (SIN --break-system-packages)
RUN pip install --no-cache-dir -r requirements.txt

# Instalar Playwright browsers
RUN playwright install chromium

# Copiar código
COPY viral_scraper_api.py .

# Exponer puerto
EXPOSE 5000

# Variables de entorno
ENV PYTHONUNBUFFERED=1

# Comando de inicio
CMD ["python", "-u", "viral_scraper_api.py"]