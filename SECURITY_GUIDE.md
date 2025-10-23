# 🔐 GUÍA DE SEGURIDAD - API KEYS

## ⚠️ REGLAS DE ORO

1. **NUNCA compartas tu API Key públicamente**
   - ❌ No en chats
   - ❌ No en código que subes a GitHub
   - ❌ No en capturas de pantalla
   - ❌ No en foros o Discord

2. **SIEMPRE usa archivo .env**
   - ✅ Guarda keys en `.env` local
   - ✅ Agrega `.env` a `.gitignore`
   - ✅ Usa variables de entorno en producción

3. **RESTRINGE tus API Keys**
   - ✅ Limita a APIs específicas
   - ✅ Limita por dominio/IP si es posible
   - ✅ Monitorea uso regularmente

---

## 🚨 ¿Qué hacer si expusiste tu API Key?

### Paso 1: Regenerar INMEDIATAMENTE

1. Ve a [Google Cloud Console](https://console.cloud.google.com/apis/credentials)
2. Encuentra la API Key expuesta
3. Click en los 3 puntos → "Delete" o "Regenerate"
4. Copia la NUEVA API Key

### Paso 2: Restringir la nueva API Key

En Google Cloud Console:

```
1. Click en tu API Key
2. Scroll a "API restrictions"
3. Selecciona "Restrict key"
4. Marca SOLO: "YouTube Data API v3"
5. Click "Save"
```

Esto asegura que aunque alguien tenga tu key, solo pueda usarla para YouTube.

### Paso 3: Opcional - Restringir por aplicación

Si tu API está en un servidor con IP fija:

```
1. En "Application restrictions"
2. Selecciona "IP addresses"
3. Agrega la IP de tu servidor
4. Click "Save"
```

---

## 📝 Configuración Correcta del archivo .env

### Crear archivo .env

```bash
# En tu servidor/computadora (NO en GitHub)
touch .env
nano .env
```

### Contenido del .env

```bash
# ============================================
# YOUTUBE API (OBLIGATORIO)
# ============================================
YOUTUBE_API_KEY=AIza...tu_key_aqui...XYZ

# ============================================
# INSTAGRAM (OPCIONAL)
# ============================================
INSTAGRAM_USER=tu_usuario
INSTAGRAM_PASS=tu_password

# ============================================
# TIKTOK (OPCIONAL)
# ============================================
TIKTOK_MS_TOKEN=tu_ms_token

# ============================================
# FLASK CONFIG
# ============================================
FLASK_ENV=production
FLASK_DEBUG=False
```

### Proteger el archivo .env

```bash
# Cambiar permisos (solo tú puedes leer)
chmod 600 .env

# Si usas Git, agregar a .gitignore
echo ".env" >> .gitignore
```

---

## 🛡️ Mejores Prácticas por Plataforma

### YouTube API Key

**Configuración Recomendada:**
- ✅ Restringir a "YouTube Data API v3"
- ✅ Opcional: Restringir por IP del servidor
- ✅ Monitorear cuota diaria (10k unidades)

**Señales de que fue comprometida:**
- Cuota consumida rápidamente sin razón
- Requests desde IPs desconocidas
- Notificaciones de Google Cloud sobre uso inusual

### Instagram Login

**Configuración Recomendada:**
- ✅ Usa cuenta secundaria (NO tu cuenta personal)
- ✅ Activa 2FA en la cuenta
- ✅ Cambia password regularmente
- ✅ Monitorea inicios de sesión

**Señales de compromiso:**
- Intentos de login desde ubicaciones extrañas
- Cuenta bloqueada temporalmente
- Notificaciones de Instagram sobre actividad sospechosa

### TikTok MS Token

**Configuración Recomendada:**
- ✅ Regenerar cada 7-14 días
- ✅ Obtener desde navegador en modo incógnito
- ✅ No compartir nunca

**Señales de compromiso:**
- Scraping deja de funcionar repentinamente
- Requests muy lentas
- Respuestas vacías o errores 403

---

## 📊 Monitoreo de Uso de API

### YouTube - Revisar Cuota

1. Ve a [Google Cloud Console](https://console.cloud.google.com/apis/api/youtube.googleapis.com/quotas)
2. Revisa "Queries per day"
3. Límite: 10,000 unidades/día
4. Cada search = 100 unidades
5. Cada videos.list = 1 unidad

**Cálculo:**
- 10 búsquedas = 1,000 unidades
- Puedes hacer ~100 búsquedas por día
- O ~10,000 videos.list por día

### Instagram - Monitorear Rate Limits

**Sin Login:**
- ~10-20 posts por hora
- IP puede ser bloqueada temporalmente

**Con Login:**
- ~50-100 posts por hora
- Cuenta puede ser suspendida si abusas

**Recomendación:**
- Máximo 50 requests por hora
- Agregar delay de 2-3 segundos entre requests
- Usar proxies si necesitas escalar

### TikTok - Límites Estrictos

**Límites conocidos:**
- ~10-20 videos por request
- ~5-10 requests por hora
- IP puede ser bloqueada fácilmente

**Recomendación:**
- Máximo 5 requests por hora
- Usar proxies rotativos si necesitas más
- MS Token actualizado siempre

---

## 🔒 Despliegue Seguro en Producción

### Replit

```bash
# No uses archivo .env
# Usa "Secrets" en el panel izquierdo:

1. Click en 🔒 "Secrets"
2. Agrega cada variable:
   - Key: YOUTUBE_API_KEY
   - Value: tu_api_key
3. Click "Add new secret"
```

Tu código automáticamente leerá de `os.getenv('YOUTUBE_API_KEY')`.

### Railway.app

```bash
# En el dashboard de Railway:

1. Click en tu proyecto
2. Ve a "Variables"
3. Click "New Variable"
4. Agrega:
   - YOUTUBE_API_KEY=tu_key
   - INSTAGRAM_USER=tu_usuario
   - etc.
```

### Heroku

```bash
# Via CLI:
heroku config:set YOUTUBE_API_KEY=tu_key
heroku config:set INSTAGRAM_USER=tu_usuario

# Via Dashboard:
Settings → Config Vars → Reveal Config Vars
```

### VPS (AWS, DigitalOcean, etc.)

```bash
# Opción 1: Archivo .env en el servidor
scp .env usuario@tu-servidor:/home/app/.env

# Opción 2: Variables de entorno del sistema
export YOUTUBE_API_KEY=tu_key
echo 'export YOUTUBE_API_KEY=tu_key' >> ~/.bashrc

# Opción 3: systemd service
# En /etc/systemd/system/viral-api.service
[Service]
Environment="YOUTUBE_API_KEY=tu_key"
```

---

## ✅ Checklist de Seguridad

Antes de desplegar a producción:

- [ ] API Keys en variables de entorno (.env o secrets)
- [ ] `.env` en `.gitignore`
- [ ] YouTube API Key restringida a "YouTube Data API v3"
- [ ] Instagram usando cuenta secundaria
- [ ] Passwords seguros (mínimo 12 caracteres)
- [ ] MS Token actualizado (< 14 días)
- [ ] Permisos de archivo .env: 600
- [ ] Sin API keys en código fuente
- [ ] Sin credenciales en logs
- [ ] Monitoreo de uso de cuota configurado
- [ ] Rate limiting implementado
- [ ] HTTPS activado (no HTTP)

---

## 🚨 Señales de Compromiso

Si notas esto, regenera tus keys INMEDIATAMENTE:

1. **Cuota de YouTube agotada** sin razón
2. **Cuenta de Instagram bloqueada** temporalmente
3. **Requests fallando** con errores 401/403
4. **Email de Google Cloud** sobre actividad inusual
5. **Notificaciones de Instagram** sobre login desde ubicación extraña
6. **Logs mostrando** requests desde IPs que no reconoces

---

## 📚 Recursos Adicionales

- [Google Cloud Security Best Practices](https://cloud.google.com/security/best-practices)
- [Instagram Security Center](https://help.instagram.com/369001149843369)
- [OWASP API Security](https://owasp.org/www-project-api-security/)

---

## 💡 Recuerda

> "La única API Key segura es la que nadie más conoce."

**Nunca compartas:**
- ❌ API Keys
- ❌ Passwords
- ❌ Tokens
- ❌ Secrets
- ❌ Credenciales de cualquier tipo

**Siempre usa:**
- ✅ Variables de entorno
- ✅ Secrets management
- ✅ Restricciones de API
- ✅ Monitoring
- ✅ Regeneración regular

---

🔐 **Mantén tus credenciales seguras y tu API funcionará sin problemas.**
