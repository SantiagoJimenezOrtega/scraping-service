# 🎯 MS TOKEN DE TIKTOK - GUÍA ULTRA-RÁPIDA (2 MINUTOS)

## 📱 MÉTODO MÁS FÁCIL (Chrome)

### 🔴 PASO 1: Abrir TikTok
```
1. Abre Google Chrome
2. Ve a: https://www.tiktok.com
3. (Opcional pero recomendado) Inicia sesión con tu cuenta
```

---

### 🔴 PASO 2: Abrir Herramientas de Desarrollador
```
Opción 1: Presiona la tecla F12
Opción 2: Click derecho → "Inspeccionar"
Opción 3: Ctrl + Shift + I (Windows) o Cmd + Option + I (Mac)
```

**Se abrirá un panel en la parte inferior o lateral de la ventana.**

---

### 🔴 PASO 3: Ir a Application
```
En la barra superior del panel que se abrió:
1. Busca y click en la pestaña "Application"
2. Si no la ves, busca el símbolo » (dos flechas)
3. Click ahí y selecciona "Application"
```

**Visual:**
```
Console | Elements | Sources | Network | Performance | Memory | >>> Application <<<
```

---

### 🔴 PASO 4: Expandir Cookies
```
En el panel lateral IZQUIERDO, verás:

Storage
  ▶ Local Storage
  ▶ Session Storage
  ▶ Cookies               ← Click en la flecha para expandir
     ▶ https://www.tiktok.com  ← Click aquí
```

---

### 🔴 PASO 5: Buscar msToken
```
En el panel CENTRAL verás una tabla con todas las cookies:

Name                | Value
--------------------|---------------------------
__tea_cache_tokens  | ...
csrf_session_id     | ...
msToken             | v3ELrR-5xKJ8YNqF_8h3... ← ESTA ES LA QUE NECESITAS
tt_chain_token      | ...
```

**Busca la fila que dice "msToken" en la columna Name**

---

### 🔴 PASO 6: Copiar el Token
```
1. Haz DOBLE CLICK en el valor de msToken (columna "Value")
2. Se seleccionará todo el texto
3. Presiona Ctrl+C (Windows) o Cmd+C (Mac) para copiar
4. El token se ve así: v3ELrR-5xKJ8YNqF_8h3jK9mNpQsA7eX...
```

**¡IMPORTANTE! Copia TODO el valor, puede ser muy largo.**

---

### 🔴 PASO 7: Guardar en Replit
```
1. Ve a tu Repl en Replit
2. Click en el icono 🔒 "Secrets" (barra lateral izquierda)
3. Click en "Add new secret"
4. Key: TIKTOK_MS_TOKEN
5. Value: [Pega aquí el token que copiaste] (Ctrl+V)
6. Click "Add new secret"
```

---

### ✅ PASO 8: Verificar
```bash
# En la Shell de Replit:
python -c "import os; token = os.getenv('TIKTOK_MS_TOKEN'); print('Token configurado:', 'SI' if token else 'NO')"
```

**Debería mostrar: Token configurado: SI**

---

## 🎯 VISUAL COMPLETO

```
1. TikTok.com
   ↓
2. Presionar F12
   ↓
3. Pestaña "Application"
   ↓
4. Cookies → tiktok.com
   ↓
5. Buscar "msToken"
   ↓
6. Doble click en el valor → Copiar (Ctrl+C)
   ↓
7. Replit → Secrets → TIKTOK_MS_TOKEN
   ↓
8. ✅ ¡Listo!
```

---

## 🔍 ¿DÓNDE ESTÁ CADA COSA?

### En Chrome DevTools:

```
┌─────────────────────────────────────────────────────────┐
│ [X] Inspector Web                                        │
├────────────┬────────────────────────────────────────────┤
│ Application│ ← CLICK AQUÍ                                │
├────────────┴────────────────────────────────────────────┤
│  PANEL IZQUIERDO          PANEL CENTRAL                 │
│  ════════════════          ═══════════════               │
│  Storage                                                 │
│    ▶ Local Storage        Name      | Value             │
│    ▼ Cookies              ──────────|──────────         │
│      ▶ https://tiktok.com csrf_id   | abc123           │
│                           msToken   | v3ELrR...  ← AQUÍ │
│                           tt_chain  | xyz789           │
└──────────────────────────────────────────────────────────┘
```

---

## 💡 TIPS

### Si no ves "msToken":
1. **Recarga la página** (F5)
2. **Navega** un poco por TikTok (scroll, mira algunos videos)
3. **Cierra y abre** DevTools (F12 dos veces)
4. **Inicia sesión** en TikTok si no lo has hecho

### Si el token es muy largo:
- ✅ **Es normal**, puede tener 100-200 caracteres
- ✅ Asegúrate de copiar TODO
- ✅ No agregues espacios ni saltos de línea

### Para copiar más fácil:
1. **Triple click** en el valor (selecciona todo)
2. O **Click derecho** → "Edit" → Ctrl+A → Ctrl+C

---

## 🚨 ERRORES COMUNES

### Error: "No veo la pestaña Application"

**Solución:**
```
La pestaña puede tener otro nombre según el idioma:
- Inglés: "Application"
- Español: "Aplicación"

O puede estar oculta:
- Busca el símbolo » (dos flechas)
- Click ahí
- Selecciona "Application" o "Aplicación"
```

### Error: "La cookie msToken está vacía"

**Solución:**
```
1. Cierra TikTok completamente
2. Abre en ventana de incógnito (Ctrl+Shift+N)
3. Ve a tiktok.com
4. Inicia sesión
5. Navega un poco
6. Ahora busca la cookie
```

### Error: "Copié el token pero no funciona"

**Solución:**
```
1. Verifica que NO tenga espacios al inicio o final
2. Debe ser una línea continua (sin saltos de línea)
3. Intenta copiarlo de nuevo
4. Pégalo primero en un editor de texto para verificar
```

---

## ⚡ MÉTODO ALTERNATIVO (Extensión)

Si el método anterior es complicado, usa una extensión:

### 1. Instala EditThisCookie
```
1. Ve a: chrome.google.com/webstore
2. Busca: "EditThisCookie"
3. Click "Añadir a Chrome"
```

### 2. Usa la extensión
```
1. Ve a tiktok.com
2. Click en el ICONO DE COOKIE (arriba a la derecha, junto a la URL)
3. Busca "msToken"
4. Click en el icono de COPIAR
5. ¡Listo! Token copiado
```

---

## 📊 CHECKLIST

Antes de continuar, verifica:

- [ ] Abriste tiktok.com en Chrome
- [ ] Presionaste F12
- [ ] Encontraste la pestaña "Application"
- [ ] Expandiste "Cookies" → "https://www.tiktok.com"
- [ ] Localizaste la cookie "msToken"
- [ ] Copiaste TODO el valor (puede ser muy largo)
- [ ] Agregaste el Secret en Replit con nombre: TIKTOK_MS_TOKEN
- [ ] Reiniciaste tu Repl (Stop → Run)

---

## 🎉 ¿FUNCIONÓ?

Prueba que funciona:

```bash
curl -X POST https://[TU-URL].repl.co/scrape \
  -H "Content-Type: application/json" \
  -d '{"platforms": ["tiktok"], "hashtag": "fitness", "cantidad": 2}'
```

Si ves 2 videos de TikTok con datos reales → ✅ ¡Éxito!

---

## 💬 EJEMPLO REAL

**Token válido se ve así:**
```
v3ELrR-5xKJ8YNqF_8h3jK9mNpQsA7eXf2LmK_ejemplo_muy_largo_0PqR3s-TuV4wXy_Z
```

**NO es válido si se ve así:**
```
null
undefined
(vacío)
123456 (solo números)
abc (muy corto)
```

---

## ⏰ DURACIÓN DEL TOKEN

- ✅ Funciona: ~7-14 días
- ⚠️ Después expira: Necesitas obtener uno nuevo
- 🔄 Regenera cuando: Scraping de TikTok deja de funcionar

**Es normal tener que regenerarlo cada 1-2 semanas.**

---

## ⚠️ IMPORTANTE

**TikTok es OPCIONAL.** Si tienes problemas:

✅ **Usa solo YouTube** → Más fácil, más confiable
✅ **Agrega Instagram** → También funciona bien
⚪ **TikTok es extra** → Es la plataforma más complicada

Tu sistema funciona perfectamente sin TikTok.

---

¿Necesitas ayuda con algún paso? Avísame en qué parte te trabas y te guío. 🚀
