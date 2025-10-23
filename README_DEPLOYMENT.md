# 🚀 Viral Scraper API - TikTok + Instagram + YouTube

API de scraping multi-plataforma para obtener videos virales y generar guiones con IA.

## 🎯 Características

- ✅ **TikTok** - Scraping real usando TikTokApi + Playwright
- ✅ **Instagram** - Scraping con Instaloader
- ✅ **YouTube** - API oficial de YouTube Data v3
- ✅ **Multi-plataforma** - Obtén videos de las 3 redes en una sola request
- ✅ **Viral Score** - Algoritmo avanzado de engagement
- ✅ **n8n Integration** - Workflow automation ready

## 📋 Requisitos

### Variables de Entorno Requeridas

```bash
# YouTube (OBLIGATORIO)
YOUTUBE_API_KEY=tu_youtube_api_key

# Instagram (OPCIONAL pero recomendado)
INSTAGRAM_USER=tu_usuario
INSTAGRAM_PASS=tu_password

# TikTok (OPCIONAL pero recomendado para TikTok)
TIKTOK_MS_TOKEN=tu_ms_token
```

### Cómo Obtener las Credenciales

**YouTube API Key:**
1. Ve a [Google Cloud Console](https://console.cloud.google.com/)
2. Crea proyecto → Activa YouTube Data API v3
3. Crea credencial tipo "API Key"

**Instagram:**
- Usa una cuenta secundaria (no tu cuenta principal)
- Desactiva 2FA en esa cuenta

**TikTok MS Token:**
1. Abre [tiktok.com](https://www.tiktok.com) en Chrome
2. Presiona F12 → Application → Cookies
3. Busca "msToken" y copia el valor

## 🚂 Deployment en Railway (Recomendado)

### 1. Preparar

```bash
git clone tu-repo
cd viral-scraper-api
```

### 2. Subir a GitHub

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/tu-usuario/viral-scraper-api.git
git push -u origin main
```

### 3. Deploy en Railway

1. Ve a [railway.app](https://railway.app)
2. "New Project" → "Deploy from GitHub repo"
3. Selecciona tu repositorio
4. Railway detecta el Dockerfile automáticamente
5. Configura variables de entorno
6. Deploy automático en ~5 minutos

### 4. Obtener URL

- Settings → Domains → Generate Domain
- Tu URL será algo como: `https://viral-scraper-api-production.up.railway.app`

## 🐳 Deployment con Docker (Manual)

```bash
# Build
docker build -t viral-scraper-api .

# Run
docker run -d \
  -p 5000:5000 \
  -e YOUTUBE_API_KEY=tu_key \
  -e INSTAGRAM_USER=tu_usuario \
  -e INSTAGRAM_PASS=tu_password \
  -e TIKTOK_MS_TOKEN=tu_token \
  --name viral-api \
  viral-scraper-api
```

## 📡 Endpoints

### GET /health

Health check del servicio.

**Response:**
```json
{
  "status": "ok",
  "timestamp": "2024-01-20T15:45:00",
  "available_platforms": ["tiktok", "instagram", "youtube"]
}
```

### POST /scrape

Scraping multi-plataforma de videos virales.

**Request:**
```json
{
  "platforms": ["tiktok", "instagram", "youtube"],
  "hashtag": "fitness",
  "cantidad": 10
}
```

**Response:**
```json
{
  "success": true,
  "total_videos": 30,
  "platforms_scraped": ["tiktok", "instagram", "youtube"],
  "hashtag": "fitness",
  "videos": [
    {
      "platform": "TikTok",
      "video_id": "7345678901234567890",
      "video_url": "https://www.tiktok.com/@user/video/xxx",
      "author": "fitness_pro",
      "views": 1500000,
      "likes": 85000,
      "comments": 1200,
      "shares": 450,
      "engagement_rate": 5.77,
      "viral_score": 89650,
      "created_at": "2024-01-15T10:30:00",
      "scraped_at": "2024-01-20T15:45:00"
    }
  ]
}
```

### POST /test

Endpoint de prueba con datos mock.

**Request:**
```json
{
  "hashtag": "fitness",
  "cantidad": 5
}
```

## 🧮 Viral Score Formula

```python
viral_score = (
    likes * 1 +
    comments * 3 +
    shares * 5 +
    (engagement_rate * 100)
)

engagement_rate = (likes + comments + shares) / views * 100
```

**Interpretación:**
- `< 1,000` = Bajo engagement
- `1,000 - 10,000` = Engagement medio
- `10,000 - 50,000` = Buen engagement
- `> 50,000` = VIRAL 🔥

## 🔄 Integración con n8n

### Google Sheets Configuración

| nicho | hashtag | cantidad_videos | plataformas |
|-------|---------|-----------------|-------------|
| fitness | fitness | 10 | tiktok,instagram,youtube |

### n8n HTTP Request Node

**URL:** `https://tu-api-url.com/scrape`

**Method:** POST

**Body:**
```json
{
  "platforms": {{ $json.plataformas.split(',').map(p => p.trim()) }},
  "hashtag": "{{ $json.hashtag }}",
  "cantidad": {{ $json.cantidad_videos }}
}
```

**Timeout:** 90000 (90 segundos)

## 🛠️ Desarrollo Local

```bash
# 1. Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. Instalar dependencias
pip install -r requirements.txt
playwright install chromium

# 3. Configurar variables
cp .env.example .env
# Editar .env con tus credenciales

# 4. Ejecutar
python viral_scraper_api.py

# 5. Probar
curl http://localhost:5000/health
```

## 📊 Rate Limits

| Plataforma | Sin Login | Con Login | Recomendación |
|------------|-----------|-----------|---------------|
| TikTok | 5-10 videos | 20-30 videos | Máx 10 requests/hora |
| Instagram | 10-20 videos | 50-100 videos | Máx 50 requests/hora |
| YouTube | Ilimitado* | Ilimitado* | 10k unidades API/día |

*YouTube: 10,000 unidades de cuota diaria (suficiente para ~100 búsquedas)

## ⚠️ Troubleshooting

### "YouTube API Key invalid"
- Verifica que está correctamente configurada en variables de entorno
- Asegúrate que YouTube Data API v3 está activada
- Revisa cuota en Google Cloud Console

### "Instagram login failed"
- Usa cuenta sin 2FA
- Verifica usuario y contraseña
- Intenta desde el mismo IP donde scrapeaste antes

### "TikTok returns 0 videos"
- MS Token expirado (regenera cada 7-14 días)
- Rate limit alcanzado (espera 1 hora)
- TikTok puede estar bloqueando tu IP (usa proxies)

### "Playwright browser not found"
- En Docker: Verifica que el Dockerfile instala Playwright
- Local: Ejecuta `playwright install chromium`

## 💰 Costos Estimados

### Railway
- Primeros meses: **$0** (crédito de $5 gratis)
- Después: **$5-10/mes** (uso moderado)

### APIs Externas
- YouTube: **Gratis** (10k unidades/día)
- Instagram: **Gratis**
- TikTok: **Gratis**

### Total
- **$0-10/mes** dependiendo de uso y plataforma de hosting

## 📈 Escalamiento

Para uso intensivo (1000+ requests/día):
- Implementa cache con Redis (1-2 horas por hashtag)
- Usa proxies rotativos (BrightData, Oxylabs)
- Queue system (Celery + Redis)
- Multiple instances (load balancer)

## 📄 Licencia

Uso personal y educativo. No redistribuir datos masivamente sin permiso de las plataformas.

## 🆘 Soporte

- [Documentación completa](./README.md)
- [Guía de Railway](./RAILWAY_DEPLOYMENT.md)
- [Opciones de deployment](./DEPLOYMENT_OPTIONS.md)

## 🎉 Créditos

Creado para automatizar la generación de guiones virales basados en datos reales de redes sociales.

---

**¿Dudas?** Revisa la documentación completa o abre un issue.
