FROM python:3.11-slim

# Instalar dependencias del sistema para Playwright y navegadores
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    ca-certificates \
    fonts-liberation \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libatspi2.0-0 \
    libcups2 \
    libdbus-1-3 \
    libdrm2 \
    libgbm1 \
    libgtk-3-0 \
    libnspr4 \
    libnss3 \
    libwayland-client0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxkbcommon0 \
    libxrandr2 \
    xdg-utils \
    libu2f-udev \
    libvulkan1 \
    && rm -rf /var/lib/apt/lists/*

# Configurar directorio de trabajo
WORKDIR /app

# Copiar archivos de dependencias primero (para aprovechar cache de Docker)
COPY requirements.txt .

# Instalar dependencias Python
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Instalar navegadores de Playwright
# Solo Chromium (más ligero que instalar todos los navegadores)
RUN playwright install chromium
RUN playwright install-deps chromium

# Copiar el código de la aplicación
COPY viral_scraper_api.py .

# Crear directorio para logs (opcional)
RUN mkdir -p /app/logs

# Exponer puerto
EXPOSE 5000

# Variables de entorno para producción
ENV PYTHONUNBUFFERED=1
ENV PLAYWRIGHT_BROWSERS_PATH=/ms-playwright

# Health check (opcional pero recomendado)
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
  CMD python -c "import requests; requests.get('http://localhost:5000/health')" || exit 1

# Comando de inicio
CMD ["python", "-u", "viral_scraper_api.py"]
