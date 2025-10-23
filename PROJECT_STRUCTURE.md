# 📁 ESTRUCTURA DEL PROYECTO

```
viral-scraper-api-v2/
│
├── 📄 viral_scraper_api.py          # API principal (Flask)
├── 📄 test_api.py                   # Suite de tests
├── 📄 requirements.txt              # Dependencias Python
├── 📄 env.example                   # Variables de entorno (renombrar a .env)
│
├── 📖 README.md                     # Guía completa de instalación y uso
├── 📖 N8N_UPDATE_GUIDE.md          # Guía para actualizar n8n
├── 📖 QUICK_START.md               # Resumen ejecutivo y próximos pasos
└── 📖 PROJECT_STRUCTURE.md         # Este archivo
```

---

# 🔄 DIAGRAMA DE FLUJO COMPLETO

```
┌─────────────────────────────────────────────────────────────┐
│                    USUARIO (n8n)                             │
└───────────────────┬─────────────────────────────────────────┘
                    │
                    │ POST /scrape
                    │ { platforms: ["tiktok","instagram","youtube"],
                    │   hashtag: "fitness", cantidad: 10 }
                    ▼
┌─────────────────────────────────────────────────────────────┐
│                  FLASK API SERVER                            │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Endpoint: /scrape                                    │  │
│  │  - Valida parámetros                                 │  │
│  │  - Inicia scraping por plataforma                    │  │
│  └──────────────────────────────────────────────────────┘  │
└───┬────────────────┬─────────────────┬──────────────────────┘
    │                │                 │
    │ TikTok         │ Instagram       │ YouTube
    ▼                ▼                 ▼
┌─────────┐    ┌──────────┐     ┌───────────┐
│ TikTok  │    │Instagram │     │  YouTube  │
│   API   │    │  Loader  │     │  API v3   │
└────┬────┘    └─────┬────┘     └─────┬─────┘
     │               │                 │
     │ 10 videos     │ 10 videos       │ 10 videos
     │               │                 │
     └───────────────┴─────────────────┘
                     │
                     │ 30 videos totales
                     ▼
        ┌─────────────────────────┐
        │   PROCESAMIENTO:        │
        │ - Calcular viral_score  │
        │ - Calcular engagement   │
        │ - Normalizar datos      │
        │ - Ordenar por score     │
        └─────────┬───────────────┘
                  │
                  │ JSON Response
                  ▼
        ┌─────────────────────────┐
        │   n8n WORKFLOW:         │
        │ 1. Parse Videos         │
        │ 2. Filter (score≥1000)  │
        │ 3. Aggregate            │
        │ 4. OpenAI (3 guiones)   │
        │ 5. Save to Sheets       │
        └─────────────────────────┘
```

---

# 🎯 FLUJO DE DATOS DETALLADO

## 1️⃣ REQUEST (n8n → API)

```json
{
  "platforms": ["tiktok", "instagram", "youtube"],
  "hashtag": "fitness",
  "cantidad": 10
}
```

## 2️⃣ SCRAPING (API → Plataformas)

### TikTok
```python
async with TikTokApi() as api:
    tag = api.hashtag(name="fitness")
    async for video in tag.videos(count=10):
        # Extraer: views, likes, comments, shares
        # Calcular: engagement_rate, viral_score
```

### Instagram
```python
L = instaloader.Instaloader()
hashtag_posts = Hashtag.from_name(L.context, "fitness")
for post in hashtag_posts.get_posts():
    if post.is_video:
        # Extraer: views, likes, comments
        # Calcular: engagement_rate, viral_score
```

### YouTube
```python
youtube = build('youtube', 'v3', developerKey=API_KEY)
search_response = youtube.search().list(
    q="fitness",
    maxResults=10,
    type='video'
)
# Extraer: views, likes, comments
# Calcular: engagement_rate, viral_score
```

## 3️⃣ NORMALIZACIÓN DE DATOS

Todos los videos se convierten a este formato:

```python
{
    'platform': 'TikTok' | 'Instagram' | 'YouTube',
    'video_id': str,
    'video_url': str,
    'author': str,
    'author_followers': int,
    'description': str,
    'hashtag': str,
    'views': int,
    'likes': int,
    'comments': int,
    'shares': int,
    'engagement_rate': float,
    'viral_score': int,
    'duration': int,
    'created_at': str,
    'music': str,
    'scraped_at': str
}
```

## 4️⃣ CÁLCULO DE VIRAL SCORE

```python
# Engagement Rate
total_interactions = likes + comments + shares
engagement_rate = (total_interactions / views * 100)

# Viral Score (pesos diferentes por acción)
viral_score = (
    likes * 1 +           # Like = 1 punto
    comments * 3 +        # Comment = 3 puntos
    shares * 5 +          # Share = 5 puntos
    (engagement_rate * 100)
)
```

**Ejemplo:**
- Video con 1M views, 50k likes, 2k comments, 500 shares
- Engagement = (50k + 2k + 500) / 1M * 100 = 5.25%
- Viral Score = 50,000 + 6,000 + 2,500 + 525 = **59,025** 🔥

## 5️⃣ RESPONSE (API → n8n)

```json
{
  "success": true,
  "total_videos": 30,
  "platforms_scraped": ["tiktok", "instagram", "youtube"],
  "hashtag": "fitness",
  "videos": [
    {
      "platform": "YouTube",
      "viral_score": 125000,
      "views": 2500000,
      "likes": 95000,
      "comments": 1200,
      "engagement_rate": 3.85,
      "video_url": "https://youtube.com/watch?v=..."
    },
    // ... 29 videos más
  ],
  "errors": {}  // Solo si alguna plataforma falló
}
```

---

# 🧩 INTEGRACIÓN CON N8N

## Flujo Actualizado en n8n:

```
1. Manual Trigger
   ↓
2. Config (Google Sheets)
   Lee: { nicho, hashtag, cantidad_videos, plataformas }
   ↓
3. HTTP Request (POST)
   URL: https://tu-api.com/scrape
   Body: {
     "platforms": {{ $json.plataformas.split(',') }},
     "hashtag": "{{ $json.hashtag }}",
     "cantidad": {{ $json.cantidad_videos }}
   }
   ↓
4. Parse Videos (Code)
   1 item → 30 items (1 por video)
   ↓
5. Filter Viral Videos (Code)
   30 items → 12 items (viral_score >= 1000)
   ↓
6. Aggregate
   12 items → 1 item con array
   ↓
7. OpenAI (Generate Scripts)
   Prompt: "Basándote en estos 12 videos virales..."
   Output: 3 guiones completos
   ↓
8. Code in JavaScript
   1 item → 3 items (1 por guión)
   ↓
9. Save Scripts (Google Sheets)
   3 items → Guardados en "Guiones Generados"
```

---

# 📊 EJEMPLO REAL DE EJECUCIÓN

## Input en Google Sheets:
| nicho   | hashtag | cantidad_videos | plataformas              |
|---------|---------|-----------------|--------------------------|
| fitness | fitness | 10              | tiktok,instagram,youtube |

## Request a la API:
```bash
POST https://api.tu-dominio.com/scrape
{
  "platforms": ["tiktok", "instagram", "youtube"],
  "hashtag": "fitness",
  "cantidad": 10
}
```

## Response (30 videos):
```
┌─────────────┬───────┬────────┬──────────┐
│ Plataforma  │ Count │ Avg VS │ Top VS   │
├─────────────┼───────┼────────┼──────────┤
│ YouTube     │   10  │ 45,230 │ 125,000  │
│ TikTok      │   10  │ 38,150 │  89,650  │
│ Instagram   │   10  │ 22,840 │  45,800  │
└─────────────┴───────┴────────┴──────────┘
Total: 30 videos, Promedio VS: 35,407
```

## Filtrado (viral_score >= 1,000):
- YouTube: 10 videos ✅
- TikTok: 9 videos ✅
- Instagram: 7 videos ✅
- **Total: 26 videos virales**

## OpenAI recibe:
Análisis de 26 videos virales de 3 plataformas

## OpenAI genera:
3 guiones profesionales adaptables a todas las plataformas

## Resultado en Google Sheets:

| script_number | nicho   | plataformas_usadas       | title                          | viral_score_avg |
|---------------|---------|--------------------------|--------------------------------|-----------------|
| 1             | fitness | tiktok,instagram,youtube | 5 Errores que Arruinan...      | 35,407          |
| 2             | fitness | tiktok,instagram,youtube | La Verdad sobre el...          | 35,407          |
| 3             | fitness | tiktok,instagram,youtube | Transforma tu Cuerpo en...     | 35,407          |

---

# 🔐 SEGURIDAD Y VARIABLES DE ENTORNO

## Archivo .env (NO compartir):

```bash
# YouTube (OBLIGATORIO)
YOUTUBE_API_KEY=AIzaSyXXXXXXXXXXXXXXXXX

# Instagram (OPCIONAL)
INSTAGRAM_USER=tu_usuario
INSTAGRAM_PASS=tu_password_seguro

# TikTok (OPCIONAL)
TIKTOK_MS_TOKEN=tu_ms_token_largo

# Flask
FLASK_ENV=production
FLASK_DEBUG=False
```

## Variables por Plataforma:

| Plataforma | Variable Requerida | Dónde Obtener |
|------------|-------------------|---------------|
| YouTube    | YOUTUBE_API_KEY   | Google Cloud Console |
| Instagram  | INSTAGRAM_USER    | Tu cuenta IG |
| Instagram  | INSTAGRAM_PASS    | Tu password IG |
| TikTok     | TIKTOK_MS_TOKEN   | Cookies del navegador |

---

# ⚡ PERFORMANCE Y TIEMPOS

## Tiempos de Ejecución Estimados:

| Operación | Tiempo | Notas |
|-----------|--------|-------|
| Health Check | <1s | Instantáneo |
| YouTube (10 videos) | 3-5s | API es rápida |
| Instagram (10 videos) | 20-30s | Rate limiting |
| TikTok (10 videos) | 15-25s | Más lento |
| Multi-platform (30 videos) | 40-60s | Paralelo cuando sea posible |
| OpenAI (3 guiones) | 15-30s | Depende del prompt |
| **Total n8n workflow** | 60-90s | De inicio a fin |

## Optimizaciones Posibles:

1. **Cache de resultados** (Redis)
   - Guardar por hashtag por 1-2 horas
   - Reduce API calls en 80%

2. **Scraping asíncrono**
   - Scrapear las 3 plataformas en paralelo
   - Reduce tiempo a 30s

3. **Batch processing**
   - Procesar múltiples hashtags a la vez
   - Mejor uso de cuotas de API

---

# 🎓 CONCEPTOS CLAVE

## Viral Score
**Fórmula ponderada** que combina métricas de engagement:
- Likes (peso: 1x)
- Comments (peso: 3x) → Más valiosos que likes
- Shares (peso: 5x) → Más valiosos que comments
- Engagement Rate (peso: 100x)

## Engagement Rate
Porcentaje de interacciones vs visualizaciones:
```
ER = (likes + comments + shares) / views * 100
```

Benchmark:
- < 1%: Bajo
- 1-3%: Promedio
- 3-6%: Bueno
- > 6%: Excelente 🔥

## Rate Limiting
Restricciones de requests por hora/día:
- **YouTube**: 10,000 unidades/día (generoso)
- **Instagram**: ~50-100 posts/hora (con login)
- **TikTok**: ~10-20 videos/hora (restrictivo)

---

# 🚀 ROADMAP FUTURO (v3.0)

Posibles mejoras:

1. **Análisis de Tendencias**
   - Dashboard con gráficos de viral scores
   - Trending hashtags por nicho
   - Mejores horarios de publicación

2. **Machine Learning**
   - Predicción de viralidad
   - Clasificación automática de nichos
   - Recomendaciones de contenido

3. **Más Plataformas**
   - Twitter/X
   - LinkedIn
   - Pinterest
   - Snapchat Spotlight

4. **Automatización Completa**
   - Scraping programado (cron)
   - Generación automática de guiones
   - Publicación automática (con aprobación)

5. **Análisis Avanzado**
   - Sentiment analysis de comments
   - Detección de música/audio trending
   - Análisis de colores y thumbnails

---

# 📞 SOPORTE Y CONTACTO

**¿Necesitas ayuda?**

1. Revisa primero: README.md y QUICK_START.md
2. Ejecuta: `python test_api.py`
3. Verifica: Logs de la API
4. Consulta: Documentación de cada plataforma

**Problemas comunes ya documentados en README.md:**
- YouTube API Key inválida
- Instagram login failed
- TikTok scraping returns 0
- Rate limit exceeded
- Timeout errors

---

¡Éxito con tu proyecto! 🎉

Este es un sistema profesional de scraping multi-plataforma con datos reales.
