# 🚂 RAILWAY.APP - Deployment con TikTok + Instagram + YouTube

## 🎯 POR QUÉ RAILWAY

**Railway.app es PERFECTO para tu API porque:**

✅ **Soporta Playwright** (navegadores para TikTok)
✅ **Fácil de usar** (más simple que AWS/DigitalOcean)
✅ **Deploy automático** desde GitHub
✅ **$5/mes** de crédito gratis (suficiente para empezar)
✅ **Escalable** (puedes crecer después)
✅ **Variables de entorno** integradas

**Resultado: Las 3 plataformas funcionan perfectamente.** 🔥

---

## 🚀 DEPLOYMENT EN RAILWAY (10 minutos)

### PASO 1: Crear cuenta en Railway (2 min)

1. Ve a: **https://railway.app/**
2. Click en **"Start a New Project"** o **"Login with GitHub"**
3. Conecta tu cuenta de GitHub (recomendado)
4. Verifica tu email

**Tip:** Railway te da $5/mes gratis. Después es ~$5-10/mes dependiendo uso.

---

### PASO 2: Preparar archivos localmente (3 min)

Necesitas estos archivos en una carpeta:

#### 📄 Archivo 1: `viral_scraper_api.py`

Usa el archivo **ORIGINAL** (con TikTok incluido):
- [viral_scraper_api.py](computer:///mnt/user-data/outputs/viral_scraper_api.py) ← El primero que te pasé

#### 📄 Archivo 2: `requirements.txt`

Usa el **ORIGINAL** (con todas las dependencias):
- [requirements.txt](computer:///mnt/user-data/outputs/requirements.txt) ← El completo

#### 📄 Archivo 3: `Dockerfile` (NUEVO - importante)

Crea un archivo llamado `Dockerfile` (sin extensión) con este contenido:

```dockerfile
FROM python:3.11-slim

# Instalar dependencias del sistema para Playwright
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
    && rm -rf /var/lib/apt/lists/*

# Configurar directorio de trabajo
WORKDIR /app

# Copiar archivos
COPY requirements.txt .
COPY viral_scraper_api.py .

# Instalar dependencias Python
RUN pip install --no-cache-dir -r requirements.txt

# Instalar navegadores de Playwright
RUN playwright install chromium
RUN playwright install-deps chromium

# Exponer puerto
EXPOSE 5000

# Variable de entorno para producción
ENV PYTHONUNBUFFERED=1

# Comando de inicio
CMD ["python", "viral_scraper_api.py"]
```

#### 📄 Archivo 4: `.dockerignore` (NUEVO)

Crea un archivo `.dockerignore`:

```
__pycache__
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.env
.git
.gitignore
*.md
```

#### 📄 Archivo 5: `railway.json` (NUEVO - configuración Railway)

```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "DOCKERFILE"
  },
  "deploy": {
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 3
  }
}
```

---

### PASO 3: Subir a GitHub (2 min)

#### Opción A: GitHub Desktop (más fácil)

1. Descarga **GitHub Desktop**: https://desktop.github.com/
2. Abre GitHub Desktop
3. File → New Repository
4. Nombre: `viral-scraper-api`
5. Arrastra la carpeta con tus archivos
6. Click "Publish repository"
7. Marca "Public" o "Private" (tu elección)
8. Click "Publish"

#### Opción B: Línea de comandos

```bash
# En la carpeta de tu proyecto:
git init
git add .
git commit -m "Initial commit - Viral Scraper API"

# Crea repo en GitHub.com y luego:
git remote add origin https://github.com/tu-usuario/viral-scraper-api.git
git push -u origin main
```

---

### PASO 4: Conectar Railway con GitHub (2 min)

1. En **Railway.app**, click **"New Project"**
2. Selecciona **"Deploy from GitHub repo"**
3. Autoriza Railway a acceder a GitHub
4. Selecciona tu repositorio: `viral-scraper-api`
5. Railway detectará automáticamente el `Dockerfile`
6. Click **"Deploy"**

**Railway comenzará a construir tu aplicación (toma 3-5 minutos).**

---

### PASO 5: Configurar Variables de Entorno (2 min)

Mientras Railway construye:

1. En el dashboard de Railway, click en tu proyecto
2. Ve a la pestaña **"Variables"**
3. Agrega estas variables:

```
YOUTUBE_API_KEY=tu_youtube_api_key_aqui
INSTAGRAM_USER=tu_usuario_instagram
INSTAGRAM_PASS=tu_password_instagram
TIKTOK_MS_TOKEN=tu_ms_token_tiktok
```

**Todas deben estar configuradas para que las 3 plataformas funcionen.**

4. Railway reiniciará automáticamente la app con las nuevas variables

---

### PASO 6: Obtener tu URL (1 min)

1. En Railway, ve a **"Settings"**
2. Scroll hasta **"Domains"**
3. Click **"Generate Domain"**
4. Railway te dará una URL como:
   ```
   https://viral-scraper-api-production-xxxx.up.railway.app
   ```

**¡Esta es tu URL para n8n!** 🎉

---

### PASO 7: Probar la API (1 min)

```bash
# Health check
curl https://[TU-URL-RAILWAY].up.railway.app/health

# Test de las 3 plataformas
curl -X POST https://[TU-URL-RAILWAY].up.railway.app/scrape \
  -H "Content-Type: application/json" \
  -d '{"platforms": ["tiktok", "instagram", "youtube"], "hashtag": "fitness", "cantidad": 3}'
```

**Debería devolver videos de las 3 plataformas.** ✅

---

## 📊 ESTRUCTURA DE ARCHIVOS FINAL

```
viral-scraper-api/
├── viral_scraper_api.py     # API con TikTok + Instagram + YouTube
├── requirements.txt          # Todas las dependencias
├── Dockerfile               # Configuración Docker
├── .dockerignore            # Archivos a ignorar
├── railway.json             # Configuración Railway
├── .gitignore               # Git ignore (opcional)
└── README.md                # Documentación (opcional)
```

---

## 🔄 ACTUALIZAR TU CÓDIGO

Cuando hagas cambios:

```bash
# 1. Edita tus archivos
# 2. Commit y push a GitHub:
git add .
git commit -m "Actualización de la API"
git push

# 3. Railway detecta el cambio y redeploy automáticamente
```

**Deploy automático en ~3 minutos.** 🚀

---

## 💰 COSTOS DE RAILWAY

| Uso | Costo Mensual |
|-----|---------------|
| Hobby (con $5 gratis) | **$0** (primeros meses) |
| Después del crédito | ~**$5-10/mes** |
| Uso intensivo | ~**$15-20/mes** |

**Comparado con:**
- Replit Hacker: $7/mes (pero TikTok no funciona)
- AWS/DigitalOcean: $5-20/mes (más complicado)

**Railway es la mejor opción calidad/precio.** ✅

---

## 🛠️ TROUBLESHOOTING EN RAILWAY

### "Build failed"

**Solución:** Revisa los logs en Railway:
1. Click en tu proyecto
2. Pestaña "Deployments"
3. Click en el deployment fallido
4. Revisa los logs

Errores comunes:
- Dockerfile mal formateado → Copia exactamente el de arriba
- requirements.txt incorrecto → Usa el original
- Falta algún archivo → Verifica que estén todos en GitHub

### "API responde 502"

**Solución:**
1. Verifica que la app está corriendo (ícono verde en Railway)
2. Revisa logs en tiempo real
3. Asegúrate que expones el puerto 5000

### "TikTok no funciona"

**Solución:**
1. Verifica que `TIKTOK_MS_TOKEN` está en Variables
2. El token debe ser válido (obtén uno nuevo)
3. Revisa logs para ver el error específico

### "Instagram login failed"

**Solución:**
1. Verifica `INSTAGRAM_USER` y `INSTAGRAM_PASS`
2. Usa cuenta sin 2FA
3. Intenta desde el mismo IP donde scrapeaste antes

---

## 🎯 ACTUALIZAR N8N

Una vez que Railway esté funcionando:

### En Google Sheets:

| nicho | hashtag | cantidad_videos | plataformas |
|-------|---------|-----------------|-------------|
| fitness | fitness | 10 | **tiktok,instagram,youtube** |

**Ahora SÍ puedes usar las 3 plataformas.** 🔥

### En n8n - HTTP Request:

**URL:**
```
https://[TU-URL-RAILWAY].up.railway.app/scrape
```

**Body:**
```json
{
  "platforms": {{ $json.plataformas.split(',').map(p => p.trim()) }},
  "hashtag": "{{ $json.hashtag }}",
  "cantidad": {{ $json.cantidad_videos }}
}
```

**Timeout:** 90000 (90 segundos, porque 3 plataformas toman más tiempo)

---

## 📊 RESULTADO ESPERADO

### Request de n8n:
```json
{
  "platforms": ["tiktok", "instagram", "youtube"],
  "hashtag": "fitness",
  "cantidad": 10
}
```

### Response de Railway:
```json
{
  "success": true,
  "total_videos": 30,
  "platforms_scraped": ["tiktok", "instagram", "youtube"],
  "videos": [
    {"platform": "TikTok", "viral_score": 89650, ...},
    {"platform": "Instagram", "viral_score": 45800, ...},
    {"platform": "YouTube", "viral_score": 125000, ...}
    // ... 27 videos más
  ]
}
```

### Filtrado en n8n:
- 30 videos → 20 videos virales (score >= 1000)

### OpenAI genera:
- 3 guiones basados en 20 videos de 3 plataformas diferentes

### Resultado final:
- 3 guiones profesionales en Google Sheets ✅

---

## 🎉 VENTAJAS DE RAILWAY

✅ **Soporte completo de Playwright** → TikTok funciona
✅ **Deploy automático** → Push a GitHub y listo
✅ **Logs en tiempo real** → Debugging fácil
✅ **Escalable** → Crece con tu proyecto
✅ **Variables de entorno** → Seguro y fácil
✅ **SSL/HTTPS gratis** → Sin configuración
✅ **Sin mantenimiento** → Railway lo gestiona todo

---

## 🔄 COMPARACIÓN CON REPLIT

| Característica | Replit | Railway |
|----------------|--------|---------|
| **TikTok** | ❌ No funciona | ✅ Funciona |
| **Instagram** | ✅ Funciona | ✅ Funciona |
| **YouTube** | ✅ Funciona | ✅ Funciona |
| **Playwright** | ❌ No soportado | ✅ Soportado |
| **Costo** | $7/mes | $5-10/mes |
| **Estabilidad** | ⚪ Media | ✅ Alta |
| **Sleeping** | ⚠️ Sí (plan gratis) | ✅ No |
| **Deploy** | Manual | Automático |

**Railway gana en todos los aspectos para tu caso de uso.** 🏆

---

## 💡 ESTRATEGIA HÍBRIDA (Opcional)

Si quieres lo mejor de ambos mundos:

1. **Replit:** Para desarrollo/testing rápido (solo YouTube)
2. **Railway:** Para producción (las 3 plataformas)

**Ventajas:**
- Testing rápido en Replit
- Producción estable en Railway
- Backup si uno falla

---

## 🆘 SOPORTE

**Railway Documentation:** https://docs.railway.app/
**Railway Discord:** https://discord.gg/railway
**Railway Status:** https://status.railway.app/

---

## ✅ CHECKLIST DE DEPLOYMENT

- [ ] Cuenta en Railway creada
- [ ] GitHub conectado a Railway
- [ ] Archivos subidos a GitHub (Dockerfile incluido)
- [ ] Proyecto desplegado en Railway
- [ ] Variables de entorno configuradas
- [ ] Dominio generado
- [ ] Health check responde OK
- [ ] Test de scraping con 3 plataformas funciona
- [ ] n8n actualizado con nueva URL
- [ ] Google Sheets con "tiktok,instagram,youtube"
- [ ] Workflow completo probado y funciona

---

## 🚀 SIGUIENTE PASO

1. **Crea cuenta** en Railway.app
2. **Prepara archivos** (Dockerfile especialmente)
3. **Sube a GitHub**
4. **Conecta Railway**
5. **Configura variables**
6. **¡Las 3 plataformas funcionando!** 🎉

---

¿Necesitas ayuda con algún paso? Avísame y te guío.
