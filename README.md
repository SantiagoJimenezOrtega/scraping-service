# 🚀 VIRAL SCRAPER API - Guía Completa de Instalación

## 📋 Requisitos Previos

- Python 3.9 o superior
- pip instalado
- Cuenta de Google Cloud (para YouTube API - GRATIS)
- Cuenta de Instagram (opcional, pero recomendado)

---

## 🔧 Instalación Paso a Paso

### 1. Clonar/Descargar los archivos

Asegúrate de tener estos archivos:
- `viral_scraper_api.py`
- `requirements.txt`
- `.env.example`

### 2. Crear entorno virtual (recomendado)

```bash
# En Windows
python -m venv venv
venv\Scripts\activate

# En Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt

# Instalar Playwright browsers (para TikTok)
playwright install
```

### 4. Configurar variables de entorno

```bash
# Copiar archivo de ejemplo
cp .env.example .env

# Editar con tus credenciales
nano .env  # o usar tu editor favorito
```

---

## 🔑 Obtener API Keys

### YouTube API Key (OBLIGATORIO)

1. Ve a [Google Cloud Console](https://console.cloud.google.com/)
2. Crea un nuevo proyecto o selecciona uno existente
3. Ve a "APIs & Services" > "Library"
4. Busca "YouTube Data API v3" y actívala
5. Ve a "Credentials" > "Create Credentials" > "API Key"
6. Copia el API Key y pégalo en `.env`:
   ```
   YOUTUBE_API_KEY=AIzaSyXXXXXXXXXXXXXXXXXX
   ```

**Nota:** La API de YouTube es GRATUITA hasta 10,000 unidades/día (suficiente para ~100 requests)

### Instagram Login (OPCIONAL)

```env
INSTAGRAM_USER=tu_usuario
INSTAGRAM_PASS=tu_password
```

**Importante:** 
- Usa una cuenta secundaria, no tu cuenta principal
- Instagram puede bloquear si haces muchos requests
- Sin login: 10-20 posts por hora
- Con login: 100+ posts por hora

### TikTok MS Token (OPCIONAL)

1. Abre TikTok en tu navegador
2. Abre DevTools (F12)
3. Ve a Application > Cookies
4. Busca cookie llamada `msToken`
5. Copia el valor y pégalo en `.env`

---

## 🎯 Ejecutar la API

### Desarrollo Local

```bash
python viral_scraper_api.py
```

La API estará disponible en: `http://localhost:5000`

### Producción (Replit, Railway, etc.)

```bash
# El comando puede variar según la plataforma
gunicorn viral_scraper_api:app --bind 0.0.0.0:5000
```

---

## 📡 Endpoints de la API

### 1. POST /scrape - Scraping Real Multi-Plataforma

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
      "author_followers": 500000,
      "description": "5 ejercicios para...",
      "hashtag": "fitness",
      "views": 1500000,
      "likes": 85000,
      "comments": 1200,
      "shares": 450,
      "engagement_rate": 5.77,
      "viral_score": 89650,
      "duration": 45,
      "created_at": "2024-01-15T10:30:00",
      "music": "Original Sound",
      "scraped_at": "2024-01-20T15:45:00"
    }
  ],
  "errors": {}
}
```

### 2. POST /test - Datos Mock para Pruebas

**Request:**
```json
{
  "hashtag": "fitness",
  "cantidad": 5
}
```

### 3. GET /health - Health Check

**Response:**
```json
{
  "status": "ok",
  "timestamp": "2024-01-20T15:45:00",
  "available_platforms": ["tiktok", "instagram", "youtube"]
}
```

---

## 🧮 Fórmula de Viral Score

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

---

## 🔍 Troubleshooting

### Error: "YouTube API Key inválido"
- Verifica que el API Key esté correcto en `.env`
- Asegúrate de haber activado YouTube Data API v3
- Revisa que no hayas excedido el límite de 10k unidades/día

### Error: "Instagram login failed"
- Verifica usuario y contraseña
- Instagram puede pedir verificación 2FA
- Intenta desde el mismo IP donde scrapeaste antes

### Error: "TikTok scraping failed"
- TikTok es la plataforma más restrictiva
- Usa MS Token actualizado
- Reduce la cantidad de videos por request
- Agrega delays entre requests

### Error: "playwright not found"
- Ejecuta: `playwright install`
- Reinicia el terminal/IDE

---

## ⚡ Optimización y Mejores Prácticas

### Rate Limits Recomendados

| Plataforma | Sin Login | Con Login | Delay |
|------------|-----------|-----------|-------|
| TikTok     | 5-10 videos | 20-30 videos | 3-5 seg |
| Instagram  | 10-20 videos | 50-100 videos | 2-3 seg |
| YouTube    | 50-100 videos | Ilimitado* | 0 seg |

*Hasta 10,000 unidades API/día

### Consejos de Uso

1. **Empieza con YouTube**: Es la más estable y generosa
2. **Instagram con login**: Mejora significativamente los límites
3. **TikTok**: Usa con moderación, es la más restrictiva
4. **Cache**: Considera guardar resultados por 1-2 horas
5. **Errores**: Siempre maneja errores por plataforma individualmente

### Escalamiento

Para uso intensivo:
- Usa proxies rotativos (BrightData, Oxylabs)
- Implementa cola de tareas (Celery + Redis)
- Cache con Redis (24h por hashtag)
- Deploy en múltiples IPs (AWS Lambda, Google Cloud Run)

---

## 📊 Estructura de Datos Normalizada

Todas las plataformas devuelven la misma estructura:

```python
{
    'platform': str,           # 'TikTok', 'Instagram', 'YouTube'
    'video_id': str,           # ID único del video
    'video_url': str,          # URL completa
    'author': str,             # Username del creador
    'author_followers': int,   # Seguidores del autor
    'description': str,        # Descripción/caption
    'hashtag': str,            # Hashtag buscado
    'views': int,              # Visualizaciones
    'likes': int,              # Me gusta
    'comments': int,           # Comentarios
    'shares': int,             # Compartidos
    'engagement_rate': float,  # % de engagement
    'viral_score': int,        # Puntaje viral calculado
    'duration': int,           # Duración en segundos
    'created_at': str,         # Fecha de creación (ISO)
    'music': str,              # Audio/música usado
    'scraped_at': str          # Fecha de scraping (ISO)
}
```

---

## 🆘 Soporte

Si tienes problemas:
1. Revisa los logs de la API
2. Verifica tu archivo `.env`
3. Prueba cada plataforma individualmente
4. Usa el endpoint `/test` para validar que n8n se conecta correctamente

---

## 📝 Changelog

### v2.0.0 (Actual)
- ✅ Scraping real de TikTok, Instagram, YouTube
- ✅ Multi-plataforma en una sola request
- ✅ Cálculo de viral_score mejorado
- ✅ Engagement rate por video
- ✅ Manejo de errores por plataforma
- ✅ Datos normalizados

### v1.0.0 (Original)
- ❌ Solo datos mock
- ❌ Solo TikTok
