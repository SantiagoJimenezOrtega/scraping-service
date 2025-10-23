# 🚀 INICIO RÁPIDO - REPLIT

## ✅ CHECKLIST DE 10 MINUTOS

### ☑️ PASO 1: Regenerar YouTube API Key (URGENTE)
**POR SEGURIDAD, DEBES REGENERAR LA API KEY QUE COMPARTISTE**

1. Ve a: https://console.cloud.google.com/apis/credentials
2. Busca tu key antigua
3. Elimínala
4. Crea una nueva: "Create Credentials" → "API Key"
5. Restríngela a solo "YouTube Data API v3"
6. **Copia la nueva key**

---

### ☑️ PASO 2: Descargar archivos
**Descarga SOLO estos 3 archivos principales:**

1. [viral_scraper_api.py](computer:///mnt/user-data/outputs/viral_scraper_api.py) ⭐ PRINCIPAL
2. [requirements.txt](computer:///mnt/user-data/outputs/requirements.txt) ⭐ DEPENDENCIAS
3. [test_api.py](computer:///mnt/user-data/outputs/test_api.py) ⭐ TESTING

O descarga todo en ZIP:
- [viral_scraper_api_v2.zip](computer:///mnt/user-data/outputs/viral_scraper_api_v2.zip) (34 KB)

---

### ☑️ PASO 3: Subir a Replit

1. Abre tu Repl en Replit
2. **Borra** el archivo `viral_scraper_api.py` viejo (con datos mock)
3. Sube los 3 archivos nuevos:
   - Arrastra y suelta en la barra lateral
   - O usa "Upload file"

---

### ☑️ PASO 4: Configurar Secrets (MUY IMPORTANTE)

**NO uses archivo .env en Replit. Usa el panel de Secrets:**

1. Click en 🔒 **"Secrets"** (barra lateral izquierda)
2. Agrega tu Secret:
   ```
   Key: YOUTUBE_API_KEY
   Value: [pega aquí tu NUEVA API key regenerada]
   ```
3. Click **"Add new secret"**

**Opcional - Instagram (si quieres scrapear Instagram):**
```
Key: INSTAGRAM_USER
Value: tu_usuario_instagram

Key: INSTAGRAM_PASS
Value: tu_password
```

---

### ☑️ PASO 5: Instalar dependencias

En la **Shell** (parte inferior de Replit):

```bash
pip install -r requirements.txt
```

Espera 1-2 minutos. Ignorar warnings de playwright.

---

### ☑️ PASO 6: Ejecutar la API

1. Click en el botón verde **"Run"** (arriba)
2. Espera a ver:
   ```
   🚀 Viral Scraper API iniciando...
   * Running on http://0.0.0.0:5000
   ```
3. **Guarda tu URL** (aparece arriba):
   ```
   https://[tu-proyecto].repl.co
   ```

---

### ☑️ PASO 7: Probar que funciona

En la Shell, ejecuta:

```bash
curl https://[TU-URL].repl.co/health
```

**Resultado esperado:**
```json
{"status": "ok", "available_platforms": ["tiktok", "instagram", "youtube"]}
```

✅ **Si ves esto, tu API funciona!**

---

### ☑️ PASO 8: Test de scraping real

```bash
curl -X POST https://[TU-URL].repl.co/scrape \
  -H "Content-Type: application/json" \
  -d '{"platforms": ["youtube"], "hashtag": "fitness", "cantidad": 3}'
```

**Espera 5-10 segundos.** Deberías ver JSON con 3 videos reales de YouTube.

✅ **Si ves videos con datos reales, todo está perfecto!**

---

### ☑️ PASO 9: Actualizar n8n

#### 9.1 Google Sheets

Agrega columna **"plataformas"**:

| nicho   | hashtag | cantidad_videos | **plataformas** |
|---------|---------|-----------------|-----------------|
| fitness | fitness | 10              | youtube         |

#### 9.2 n8n - HTTP Request node

**URL:**
```
https://[TU-URL-REPLIT].repl.co/scrape
```

**Body:**
```json
{
  "platforms": {{ $json.plataformas.split(',').map(p => p.trim()) }},
  "hashtag": "{{ $json.hashtag }}",
  "cantidad": {{ $json.cantidad_videos }}
}
```

**Timeout:**
```
60000 (60 segundos)
```

---

### ☑️ PASO 10: Probar workflow completo

1. En n8n, click en **"Execute Workflow"**
2. Espera 60-90 segundos
3. Verifica que se generen 3 guiones en Google Sheets

✅ **Si funciona, ¡felicidades! Todo configurado.**

---

## 🎯 RESUMEN VISUAL

```
┌─────────────────────────────────────────┐
│  1. Regenerar YouTube API Key (Google)  │
│  ↓                                      │
│  2. Descargar archivos                  │
│  ↓                                      │
│  3. Subir a Replit                      │
│  ↓                                      │
│  4. Configurar Secrets                  │
│  ↓                                      │
│  5. pip install -r requirements.txt     │
│  ↓                                      │
│  6. Click en "Run"                      │
│  ↓                                      │
│  7. Probar /health                      │
│  ↓                                      │
│  8. Probar /scrape con YouTube          │
│  ↓                                      │
│  9. Actualizar n8n                      │
│  ↓                                      │
│  10. Ejecutar workflow completo         │
│  ↓                                      │
│  ✅ ¡FUNCIONANDO!                       │
└─────────────────────────────────────────┘
```

---

## 📚 DOCUMENTACIÓN COMPLETA

Si necesitas más detalles sobre algo:

1. **[REPLIT_SETUP.md](computer:///mnt/user-data/outputs/REPLIT_SETUP.md)** - Guía completa para Replit
2. **[QUICK_COMMANDS.md](computer:///mnt/user-data/outputs/QUICK_COMMANDS.md)** - Comandos de testing
3. **[SECURITY_GUIDE.md](computer:///mnt/user-data/outputs/SECURITY_GUIDE.md)** - Seguridad de API Keys
4. **[README.md](computer:///mnt/user-data/outputs/README.md)** - Documentación general
5. **[N8N_UPDATE_GUIDE.md](computer:///mnt/user-data/outputs/N8N_UPDATE_GUIDE.md)** - Actualizar n8n

---

## 🐛 PROBLEMAS COMUNES

### ❌ "Module not found"
**Solución:**
```bash
pip install -r requirements.txt
```

### ❌ "YouTube API Key invalid"
**Solución:**
1. Verifica que el Secret esté configurado: 🔒 Secrets
2. Verifica que se llame exactamente: `YOUTUBE_API_KEY`
3. Reinicia el Repl: Stop → Run

### ❌ "Timeout error"
**Solución:**
- Reduce cantidad: `"cantidad": 3`
- Usa solo YouTube: `"platforms": ["youtube"]`
- Aumenta timeout en n8n a 60-90 segundos

### ❌ "Instagram login failed"
**Solución:**
- Por ahora usa SOLO YouTube
- Instagram es opcional, no es necesario para empezar

### ❌ "Repl keeps sleeping"
**Solución temporal:** Mantén pestaña abierta
**Solución permanente:** Usa UptimeRobot (gratis): https://uptimerobot.com/

---

## 🎯 RECOMENDACIONES

### Primera semana: SOLO YouTube
```
plataformas: youtube
cantidad_videos: 5-10
```
**Por qué:** Más estable, sin complicaciones

### Segunda semana: YouTube + Instagram
```
plataformas: youtube,instagram
cantidad_videos: 5 por plataforma
```
**Por qué:** Instagram funciona bien con configuración correcta

### Tercera semana: Experimentar con TikTok
```
plataformas: tiktok,youtube,instagram
```
**Por qué:** TikTok puede ser inestable, mejor cuando ya domines las otras

---

## ⚡ TEST MEGA-RÁPIDO

Copia y pega este comando único para verificar todo:

```bash
curl -s https://[TU-URL].repl.co/health && \
echo "" && \
curl -X POST https://[TU-URL].repl.co/scrape \
  -H "Content-Type: application/json" \
  -d '{"platforms": ["youtube"], "hashtag": "fitness", "cantidad": 2}'
```

Si ves JSON con datos reales → ✅ Todo funciona

---

## 📞 ¿NECESITAS AYUDA?

Si algo no funciona:

1. **Revisa los logs** en la consola de Replit
2. **Ejecuta comandos de testing** de QUICK_COMMANDS.md
3. **Verifica Secrets** en 🔒 Secrets
4. **Pregúntame** lo que necesites

---

## 🎉 ¡ÉXITO!

Una vez que veas esto en n8n:

```
✅ Videos scrapeados: 10 videos de YouTube
✅ Videos filtrados: 7 videos virales
✅ Guiones generados: 3 guiones profesionales
✅ Guardados en Google Sheets
```

**¡Tu sistema está completamente funcional!** 🚀

---

## 🔄 MANTENIMIENTO

**Semanal:**
- Verifica que el Repl esté activo
- Revisa cuota de YouTube (debe estar <10k/día)

**Mensual:**
- Regenera MS Token de TikTok (si usas)
- Revisa logs para errores

**Trimestral:**
- Considera actualizar dependencias
- Optimiza prompts de OpenAI

---

**Siguiente paso:** Ejecuta el PASO 1 (regenerar API Key) y luego avísame cuando hayas llegado al PASO 7 para verificar que todo funciona correctamente.
