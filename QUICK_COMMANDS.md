# ⚡ COMANDOS RÁPIDOS PARA REPLIT

Guarda este archivo para copiar/pegar comandos rápidamente.

---

## 🔧 INSTALACIÓN (primera vez)

```bash
# Instalar todas las dependencias
pip install -r requirements.txt

# Intentar instalar Playwright (puede fallar en Replit, es normal)
playwright install
```

---

## 🧪 TESTING RÁPIDO

### Test 1: Health Check (más rápido, <1 segundo)

```bash
curl https://[TU-URL].repl.co/health
```

**Debe responder:**
```json
{"status": "ok", ...}
```

---

### Test 2: Datos Mock (rápido, 1 segundo)

```bash
curl -X POST https://[TU-URL].repl.co/test \
  -H "Content-Type: application/json" \
  -d '{"hashtag": "fitness", "cantidad": 3}'
```

**Debe devolver:** Array con 3 videos de prueba

---

### Test 3: YouTube Real (5-10 segundos)

```bash
curl -X POST https://[TU-URL].repl.co/scrape \
  -H "Content-Type: application/json" \
  -d '{"platforms": ["youtube"], "hashtag": "fitness", "cantidad": 3}'
```

**Debe devolver:** Array con 3 videos reales de YouTube

---

### Test 4: Instagram Real (20-30 segundos)

**⚠️ Solo si configuraste Instagram en Secrets**

```bash
curl -X POST https://[TU-URL].repl.co/scrape \
  -H "Content-Type: application/json" \
  -d '{"platforms": ["instagram"], "hashtag": "fitness", "cantidad": 3}'
```

---

### Test 5: Multi-Plataforma (30-40 segundos)

```bash
curl -X POST https://[TU-URL].repl.co/scrape \
  -H "Content-Type: application/json" \
  -d '{"platforms": ["youtube", "instagram"], "hashtag": "fitness", "cantidad": 5}'
```

**Debe devolver:** 10 videos (5 de cada plataforma)

---

## 🔍 DEBUGGING

### Ver variables de entorno configuradas

```bash
# En la Shell de Replit:
python -c "import os; print('YOUTUBE_API_KEY:', os.getenv('YOUTUBE_API_KEY')[:20] + '...')"
```

**Debe mostrar:** `YOUTUBE_API_KEY: AIzaSy...`

Si muestra `None`, el Secret no está configurado.

---

### Verificar que Flask esté escuchando

```bash
ps aux | grep python
```

**Debe mostrar:** Proceso de `python viral_scraper_api.py`

---

### Ver logs en tiempo real

```bash
# En la Shell:
tail -f /tmp/logs/app.log

# O simplemente mira la consola de Replit
```

---

## 🚨 SOLUCIÓN DE PROBLEMAS

### Problema: "Module not found"

```bash
# Reinstalar dependencias
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

---

### Problema: "YouTube API invalid"

```bash
# Verificar que el Secret esté configurado
python -c "import os; print('Key:', os.getenv('YOUTUBE_API_KEY'))"
```

Si dice `None`:
1. Ve a 🔒 Secrets en Replit
2. Verifica que `YOUTUBE_API_KEY` esté ahí
3. Reinicia el Repl (Stop → Run)

---

### Problema: "Port 5000 already in use"

```bash
# Matar proceso anterior
pkill -f viral_scraper_api.py

# Reiniciar
python viral_scraper_api.py
```

---

### Problema: "Timeout error"

**Solución 1:** Reduce la cantidad de videos
```bash
curl -X POST https://[TU-URL].repl.co/scrape \
  -H "Content-Type: application/json" \
  -d '{"platforms": ["youtube"], "hashtag": "fitness", "cantidad": 2}'
```

**Solución 2:** Usa solo YouTube (más rápido)
```bash
# En n8n, cambia en Google Sheets:
plataformas: youtube
```

---

### Problema: "Repl keeps sleeping"

**Solución temporal:** Mantén la pestaña de Replit abierta

**Solución permanente:** Configura UptimeRobot (gratis)
1. Ve a https://uptimerobot.com/
2. Crea cuenta gratis
3. Agrega monitor HTTP(s)
4. URL: `https://[TU-URL].repl.co/health`
5. Intervalo: 5 minutos
6. Listo, hará ping automáticamente

---

## 📊 MONITOREO DE CUOTA DE YOUTUBE

### Ver cuota usada hoy

1. Ve a https://console.cloud.google.com/apis/api/youtube.googleapis.com/quotas
2. Busca "Queries per day"
3. Límite: 10,000 unidades/día

### Calcular uso por request

```
1 request de scrape con 10 videos = ~110 unidades
- search.list (1 request) = 100 unidades
- videos.list (1 request) = 1 unidad

Puedes hacer ~90 requests por día con 10 videos cada uno
```

---

## 🔄 REINICIAR TODO

Si algo está muy roto:

```bash
# 1. Detener el Repl
Click en "Stop" en Replit

# 2. Limpiar procesos
pkill -f python

# 3. Reinstalar dependencias
pip uninstall -y -r requirements.txt
pip install -r requirements.txt

# 4. Verificar Secrets
# Ve a 🔒 Secrets y verifica que estén todas las keys

# 5. Reiniciar
Click en "Run"
```

---

## 📦 ACTUALIZAR CÓDIGO

Si hago cambios en `viral_scraper_api.py`:

```bash
# 1. Detener el Repl
Stop

# 2. Reemplazar el archivo
# Descarga el nuevo archivo y súbelo a Replit (arrastra y suelta)

# 3. Reiniciar
Run
```

---

## 🎯 TESTING DESDE TU COMPUTADORA

Si descargaste `test_api.py`:

```bash
# 1. Edita test_api.py
# Cambia línea 20:
API_URL = "https://[TU-URL-REPLIT].repl.co"

# 2. Ejecuta
python test_api.py
```

**Resultado esperado:**
```
=========================
TEST 1: Health Check
=========================
✅ API está funcionando correctamente
...
Total: 5/5 tests pasaron
🎉 ¡Todos los tests pasaron!
```

---

## 💾 BACKUP DE CONFIGURACIÓN

**Guarda esto en un lugar seguro:**

```
URL de tu Replit:
https://[TU-URL].repl.co

YouTube API Key:
AIzaSy...

Instagram User (si usas):
tu_usuario

Instagram Pass (si usas):
tu_password

TikTok MS Token (si usas):
tu_token...
```

---

## 📱 ACCESO DESDE POSTMAN (opcional)

Si prefieres usar Postman para testing:

### Health Check
```
GET https://[TU-URL].repl.co/health
```

### Scraping
```
POST https://[TU-URL].repl.co/scrape
Headers:
  Content-Type: application/json
Body (raw JSON):
{
  "platforms": ["youtube"],
  "hashtag": "fitness",
  "cantidad": 5
}
```

---

## 🔐 REGENERAR SECRETS

Si necesitas cambiar algún Secret:

```
1. Ve a 🔒 Secrets en Replit
2. Click en la "X" junto al Secret que quieres cambiar
3. Agrega el nuevo Secret con el mismo nombre
4. Reinicia el Repl (Stop → Run)
```

---

## 📈 OPTIMIZACIÓN

### Para scraping más rápido:

```bash
# Usa solo YouTube (la más rápida)
{"platforms": ["youtube"], "cantidad": 5}

# Reduce cantidad de videos
{"platforms": ["youtube", "instagram"], "cantidad": 3}
```

### Para más datos:

```bash
# Usa las 3 plataformas
{"platforms": ["youtube", "instagram", "tiktok"], "cantidad": 10}

# ⚠️ Esto tomará 60-90 segundos
```

---

## ⚡ COMANDO MEGA-RÁPIDO DE VERIFICACIÓN

Copia y pega esto para verificar que todo funciona:

```bash
echo "=== VERIFICANDO CONFIGURACIÓN ===" && \
python -c "import os; print('✅ YouTube API Key:', 'Configurado' if os.getenv('YOUTUBE_API_KEY') else '❌ NO configurado')" && \
curl -s https://[TU-URL].repl.co/health | python -m json.tool && \
echo "=== TODO OK ==="
```

**Resultado esperado:**
```
=== VERIFICANDO CONFIGURACIÓN ===
✅ YouTube API Key: Configurado
{
  "status": "ok",
  ...
}
=== TODO OK ===
```

---

## 🎓 RECURSOS ÚTILES

- **Replit Docs:** https://docs.replit.com/
- **YouTube API Quota:** https://console.cloud.google.com/apis/api/youtube.googleapis.com/quotas
- **UptimeRobot:** https://uptimerobot.com/
- **n8n Docs:** https://docs.n8n.io/

---

**¡Guarda este archivo! Te ahorrará mucho tiempo en testing y debugging.** 🚀
