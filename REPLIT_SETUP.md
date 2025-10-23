# 🚀 CONFIGURACIÓN EN REPLIT - Guía Completa

## 📋 Paso a Paso para Replit

### PASO 1: Preparar tu Repl (2 minutos)

1. **Ve a tu Repl** donde tienes el proyecto
2. **Borra el archivo `viral_scraper_api.py` anterior** (el que tenía datos mock)
3. Mantén solo estos archivos si los tienes:
   - Puedes borrar casi todo, vamos a empezar fresco

---

### PASO 2: Subir los nuevos archivos (3 minutos)

**Descarga el ZIP que te pasé:**
- [viral_scraper_api_v2.zip](computer:///mnt/user-data/outputs/viral_scraper_api_v2.zip)

**En Replit, sube estos 3 archivos principales:**

1. **viral_scraper_api.py** (el nuevo, con scraping real)
2. **requirements.txt** (las dependencias)
3. **test_api.py** (para probar)

**Cómo subir archivos en Replit:**
```
1. Click en los "..." o "+" en la barra lateral izquierda
2. Click "Upload file"
3. Arrastra los archivos o selecciónalos
4. Espera que se suban
```

---

### PASO 3: Configurar Secrets en Replit (5 minutos) 🔐

**⚠️ IMPORTANTE: En Replit NO uses archivo .env, usa "Secrets"**

#### 3.1 Abrir el panel de Secrets

```
1. Mira en la barra lateral izquierda de Replit
2. Busca el icono de 🔒 "Secrets" o "Tools" → "Secrets"
3. Click en "Secrets"
```

#### 3.2 Agregar tu YouTube API Key (NUEVA, regenerada)

```
1. En "Key" escribe: YOUTUBE_API_KEY
2. En "Value" pega: tu_nueva_api_key_regenerada
3. Click "Add new secret"
```

#### 3.3 (Opcional) Agregar credenciales de Instagram

Si quieres scrapear Instagram (opcional):

```
Secret 1:
Key: INSTAGRAM_USER
Value: tu_usuario_instagram

Secret 2:
Key: INSTAGRAM_PASS
Value: tu_password_instagram
```

**💡 Tip:** Usa una cuenta secundaria de Instagram, no tu cuenta principal.

#### 3.4 (Opcional) TikTok MS Token

Si quieres scrapear TikTok (opcional pero recomendado):

```
Key: TIKTOK_MS_TOKEN
Value: tu_ms_token_de_tiktok
```

**Cómo obtener MS Token:**
1. Abre TikTok en tu navegador
2. Presiona F12 (DevTools)
3. Ve a "Application" → "Cookies" → tiktok.com
4. Busca cookie llamada `msToken`
5. Copia el valor completo

#### 3.5 Verificar tus Secrets

Deberías tener al menos esto:
```
✅ YOUTUBE_API_KEY = AIzaSy... (tu NUEVA key regenerada)
```

Opcionalmente:
```
⚪ INSTAGRAM_USER = tu_usuario
⚪ INSTAGRAM_PASS = tu_password
⚪ TIKTOK_MS_TOKEN = tu_token
```

---

### PASO 4: Instalar Dependencias (2 minutos)

En la **Shell/Console** de Replit (parte inferior o pestaña "Shell"):

```bash
# Instalar dependencias
pip install -r requirements.txt

# Instalar Playwright browsers (para TikTok)
playwright install
```

**⚠️ Si playwright install da error, es normal en Replit.** TikTok puede no funcionar, pero YouTube e Instagram sí funcionarán.

---

### PASO 5: Configurar el archivo principal (1 minuto)

Replit necesita saber qué archivo ejecutar.

**Opción A: Crear/editar `.replit` file**

En la raíz de tu proyecto, crea un archivo llamado `.replit` con este contenido:

```toml
run = "python viral_scraper_api.py"

[nix]
channel = "stable-23_05"

[deployment]
run = ["sh", "-c", "python viral_scraper_api.py"]
```

**Opción B: Usar botón de configuración**
1. Click en los "..." en la parte superior
2. "Show hidden files"
3. Edita `.replit` si existe

---

### PASO 6: Ejecutar la API (1 minuto) ▶️

```
1. Click en el botón verde "Run" en la parte superior
2. Espera a que se instalen las dependencias (puede tomar 1-2 minutos la primera vez)
3. Verás logs como:
   🚀 Viral Scraper API iniciando...
   📋 Endpoints disponibles:
   * Running on http://0.0.0.0:5000
```

**Tu API está corriendo!** 🎉

---

### PASO 7: Obtener la URL de tu API (importante para n8n)

Cuando tu Repl esté corriendo, verás una URL en la parte superior:

```
https://[tu-proyecto].repl.co
```

O algo como:
```
https://a34da17e-f2ee-416f-afc3-2ed544f253d4-00-2lqakquiv0m8d.kirk.replit.dev
```

**Guarda esta URL**, la necesitas para n8n.

---

### PASO 8: Probar tu API en Replit (3 minutos)

#### Test 1: Health Check

En la Shell/Console de Replit:

```bash
curl https://[TU-URL-REPLIT].repl.co/health
```

**Resultado esperado:**
```json
{
  "status": "ok",
  "timestamp": "2024-01-20T15:45:00",
  "available_platforms": ["tiktok", "instagram", "youtube"]
}
```

#### Test 2: Test con datos mock

```bash
curl -X POST https://[TU-URL-REPLIT].repl.co/test \
  -H "Content-Type: application/json" \
  -d '{"hashtag": "fitness", "cantidad": 3}'
```

**Resultado esperado:**
Array de 3 videos de prueba.

#### Test 3: Scraping REAL de YouTube

```bash
curl -X POST https://[TU-URL-REPLIT].repl.co/scrape \
  -H "Content-Type: application/json" \
  -d '{"platforms": ["youtube"], "hashtag": "fitness", "cantidad": 5}'
```

**⚠️ Esto tomará 5-10 segundos.** Deberías ver un JSON con 5 videos reales de YouTube.

---

### PASO 9: Probar desde tu computadora (opcional)

Si quieres probar más exhaustivamente, descarga el archivo `test_api.py` y ejecútalo en tu computadora:

```bash
# Edita test_api.py y cambia la línea:
API_URL = "https://[TU-URL-REPLIT].repl.co"  # <- Pega tu URL de Replit aquí

# Ejecuta:
python test_api.py
```

---

### PASO 10: Conectar con n8n (5 minutos)

Ahora actualiza tu workflow de n8n:

#### 10.1 En Google Sheets "Configuración"

Agrega la columna `plataformas`:

| nicho   | hashtag | cantidad_videos | **plataformas** |
|---------|---------|-----------------|-----------------|
| fitness | fitness | 10              | youtube         |

**Empieza solo con YouTube** (más estable). Luego puedes probar con `youtube,instagram`.

#### 10.2 En n8n - Nodo "HTTP Request"

Cambia la configuración:

**URL anterior:**
```
https://a34da17e-f2ee-416f-afc3-2ed544f253d4-00-2lqakquiv0m8d.kirk.replit.dev/scrape
```

**URL nueva:**
```
https://[TU-NUEVA-URL-REPLIT].repl.co/scrape
```

**Body anterior:**
```json
{
  "hashtag": "{{ $json.hashtag }}",
  "cantidad": "{{ $json.cantidad_videos }}"
}
```

**Body nuevo:**
```json
{
  "platforms": {{ $json.plataformas.split(',').map(p => p.trim()) }},
  "hashtag": "{{ $json.hashtag }}",
  "cantidad": {{ $json.cantidad_videos }}
}
```

#### 10.3 Aumentar Timeout

En el nodo HTTP Request:
```
Settings → Timeout: 60000 (60 segundos)
```

Porque scrapear puede tomar más tiempo ahora.

---

## 🎯 Ejemplo Completo de Request desde n8n

**Google Sheets dice:**
```
plataformas: youtube,instagram
hashtag: fitness
cantidad_videos: 10
```

**n8n envía a tu Replit:**
```json
POST https://[tu-url].repl.co/scrape
{
  "platforms": ["youtube", "instagram"],
  "hashtag": "fitness",
  "cantidad": 10
}
```

**Replit responde:**
```json
{
  "success": true,
  "total_videos": 20,
  "videos": [
    {
      "platform": "YouTube",
      "viral_score": 125000,
      "views": 2500000,
      "likes": 95000,
      ...
    },
    // ... 19 videos más
  ]
}
```

**n8n procesa:**
- Parse → 20 items
- Filter → 12 items virales (score >= 1000)
- OpenAI → 3 guiones
- Save → Google Sheets

---

## 🐛 Troubleshooting en Replit

### "Module not found" error

```bash
# En la Shell:
pip install -r requirements.txt
```

### "Can't connect to port 5000"

Verifica que `viral_scraper_api.py` tenga al final:
```python
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

### "YouTube API Key invalid"

1. Verifica que el Secret esté configurado correctamente
2. Regenera la API Key en Google Cloud Console
3. Asegúrate de agregar el Secret con el nombre exacto: `YOUTUBE_API_KEY`

### "Instagram login failed"

Instagram puede ser complicado:
- Usa una cuenta sin 2FA
- Verifica usuario y password
- Prueba primero SOLO con YouTube

### "TikTok scraping returns empty"

TikTok es la plataforma más difícil:
- Puede no funcionar en Replit (limitaciones de Playwright)
- Empieza solo con YouTube + Instagram
- TikTok funciona mejor en un VPS con proxies

### "Request timeout"

- Reduce la cantidad de videos: 5 en vez de 10
- Usa solo 1-2 plataformas a la vez
- Aumenta timeout en n8n a 90 segundos

### "Repl keeps sleeping"

Replit gratuito pone tu Repl a dormir después de inactividad.

**Soluciones:**
1. **Replit Hacker Plan** ($7/mes) - Siempre activo
2. **UptimeRobot** - Ping gratuito cada 5 minutos: https://uptimerobot.com/
3. **Cron-job.org** - Similar a UptimeRobot
4. **n8n Cron** - Agrega un nodo Schedule que haga ping a `/health` cada 5 min

---

## 📊 Checklist de Configuración en Replit

- [ ] Subí `viral_scraper_api.py` nuevo
- [ ] Subí `requirements.txt`
- [ ] Configuré Secret: `YOUTUBE_API_KEY` con mi key REGENERADA
- [ ] (Opcional) Configuré `INSTAGRAM_USER` y `INSTAGRAM_PASS`
- [ ] Ejecuté `pip install -r requirements.txt`
- [ ] Click en "Run" y la API arrancó
- [ ] Probé endpoint `/health` y funciona
- [ ] Probé endpoint `/test` y devuelve datos
- [ ] Probé endpoint `/scrape` con YouTube y funciona
- [ ] Copié mi URL de Replit
- [ ] Actualicé nodo HTTP Request en n8n con nueva URL
- [ ] Agregué columna "plataformas" en Google Sheets
- [ ] Ejecuté workflow completo en n8n y funcionó
- [ ] Guardé mi URL de Replit para referencia

---

## 💡 Tips Pro para Replit

### 1. Mantener tu Repl despierto (si tienes plan gratis)

Crea un workflow en n8n que haga ping cada 5 minutos:

```
Schedule Trigger (every 5 minutes)
    ↓
HTTP Request GET https://[tu-repl].repl.co/health
```

### 2. Ver logs en tiempo real

En Replit, abre la pestaña "Console" o "Logs" para ver qué está pasando.

### 3. Debug rápido

Agrega `print()` statements en tu código:
```python
print(f"🔍 Scraping {platform} para #{hashtag}...")
```

### 4. Backup de Secrets

Anota tus Secrets en un lugar seguro (gestor de passwords):
- YouTube API Key
- Instagram credentials
- TikTok MS Token

### 5. Deploy automático

Cada vez que edites código y guardes, Replit reinicia automáticamente.

---

## 🚀 Próximos Pasos

Una vez que todo funcione:

1. **Prueba con YouTube solo** (más confiable)
2. **Agrega Instagram** cuando domines YouTube
3. **Experimenta con TikTok** (puede ser inestable en Replit)
4. **Optimiza prompts de OpenAI** para mejores guiones
5. **Programa ejecuciones automáticas** con n8n Schedule

---

## 🎉 ¡Listo!

Tu API de scraping multi-plataforma está funcionando en Replit.

**Tu stack completo:**
- 🔧 Replit → API de scraping (Python + Flask)
- 🔄 n8n → Orquestación del workflow
- 📊 Google Sheets → Configuración y resultados
- 🤖 OpenAI → Generación de guiones
- 🎬 TikTok + Instagram + YouTube → Datos reales

---

**¿Necesitas ayuda con algo específico de Replit?** Avísame y te guío paso a paso.
