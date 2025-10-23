# 🔄 ACTUALIZACIÓN DEL WORKFLOW N8N - Multi-Plataforma

## 📝 Cambios Necesarios en n8n

### 1. Google Sheets "Configuración" - Agregar Columna

Agrega esta nueva columna a tu hoja "Configuración":

| nicho | hashtag | cantidad_videos | **plataformas** | instagram_user | instagram_pass |
|-------|---------|-----------------|-----------------|----------------|----------------|
| fitness | fitness | 10 | tiktok,instagram,youtube | user@mail.com | pass123 |

**Valores válidos para columna "plataformas":**
- `tiktok` - Solo TikTok
- `instagram` - Solo Instagram  
- `youtube` - Solo YouTube
- `tiktok,instagram` - TikTok e Instagram
- `tiktok,youtube` - TikTok y YouTube
- `tiktok,instagram,youtube` - Las 3 plataformas

---

### 2. HTTP Request Node - Actualizar Body

#### ❌ ANTES (solo TikTok):

```json
{
  "hashtag": "{{ $json.hashtag }}",
  "cantidad": "{{ $json.cantidad_videos }}"
}
```

#### ✅ DESPUÉS (multi-plataforma):

```json
{
  "platforms": "{{ $json.plataformas.split(',') }}",
  "hashtag": "{{ $json.hashtag }}",
  "cantidad": "{{ $json.cantidad_videos }}"
}
```

**Configuración completa del nodo HTTP Request:**

```json
{
  "method": "POST",
  "url": "https://tu-api-url.com/scrape",
  "authentication": "none",
  "sendBody": true,
  "contentType": "json",
  "jsonBody": "{\n  \"platforms\": {{ $json.plataformas.split(',') }},\n  \"hashtag\": \"{{ $json.hashtag }}\",\n  \"cantidad\": {{ $json.cantidad_videos }}\n}",
  "options": {
    "response": {
      "response": {
        "responseFormat": "json"
      }
    },
    "timeout": 60000
  }
}
```

**Nota:** Aumenta el timeout a 60 segundos porque scrapear 3 plataformas toma más tiempo.

---

### 3. Parse Videos - Ya Compatible ✅

**No requiere cambios.** El nodo actual maneja correctamente arrays de videos de cualquier plataforma.

El código actual:
```javascript
const response = $input.item.json;

// Si la API devuelve { videos: [...] }
if (response.videos && Array.isArray(response.videos)) {
  return response.videos.map(video => ({json: video}));
}

// Si la API devuelve [...] directamente
if (Array.isArray(response)) {
  return response.map(video => ({json: video}));
}
```

**Funciona con:**
- Solo TikTok
- Solo Instagram
- Solo YouTube
- Mezcla de las 3 plataformas

---

### 4. Filter Viral Videos - Ya Compatible ✅

**No requiere cambios.** El filtro actual funciona para todas las plataformas:

```javascript
return $input.all().filter(i => i.json.viral_score >= 1000);
```

Todos los videos tienen el campo `viral_score`, sin importar la plataforma.

---

### 5. Generate Scripts (OpenAI) - Mejorar Prompt (Opcional)

#### Opción A: Prompt Básico (actual)

Mantener el prompt actual. OpenAI automáticamente considerará las diferentes plataformas.

#### Opción B: Prompt Mejorado (recomendado)

Actualizar el prompt para mencionar explícitamente que los videos vienen de múltiples plataformas:

**Encuentra esta línea en el prompt:**
```
"Basándote en estos videos virales, genera EXACTAMENTE 3 guiones..."
```

**Cámbiala por:**
```
"Basándote en estos videos virales de TikTok, Instagram y YouTube, genera EXACTAMENTE 3 guiones que funcionen bien en TODAS las plataformas..."
```

**Agregar al final del system prompt:**
```
"Los guiones deben ser adaptables a formato vertical (TikTok/Instagram Reels) y horizontal (YouTube Shorts)."
```

---

### 6. Aggregate - Ya Compatible ✅

**No requiere cambios.** Agrupa todos los videos sin importar la plataforma.

---

### 7. Code in JavaScript - Ya Compatible ✅

**No requiere cambios.** Procesa los guiones de OpenAI sin dependencia de plataforma.

---

### 8. Save Scripts - Opcional: Agregar Info de Plataformas

Si quieres saber qué plataformas se usaron, modifica el código para agregar esta info:

**Encuentra esta sección en el nodo "Code in JavaScript":**

```javascript
const cleanScript = {
  script_number: index + 1,
  nicho: nicho,
  fecha_generacion: new Date().toISOString().split('T')[0],
  title: script.title || '',
  // ... resto del código
```

**Agrega estas líneas:**

```javascript
const cleanScript = {
  script_number: index + 1,
  nicho: nicho,
  plataformas_usadas: plataformas,  // ← NUEVA LÍNEA
  fecha_generacion: new Date().toISOString().split('T')[0],
  title: script.title || '',
  // ... resto del código
```

**Y al inicio del código, captura las plataformas:**

```javascript
// Obtener plataformas usadas
let plataformas = 'tiktok,instagram,youtube';
try {
  const configNode = $('Config');
  if (configNode && configNode.first && configNode.first()) {
    plataformas = configNode.first().json.plataformas || 'tiktok,instagram,youtube';
  }
} catch (e) {
  console.log('Usando plataformas default');
}
```

---

## 🎯 Flujo Actualizado Completo

```
Manual Trigger
    ↓
Config (lee: nicho, hashtag, cantidad_videos, plataformas)
    ↓
HTTP Request (envía: platforms=["tiktok","instagram","youtube"], hashtag, cantidad)
    ↓
Parse Videos (1 item → N items multi-plataforma)
    ↓
Filter Viral Videos (N items → M items, viral_score >= 1000)
    ↓
Aggregate (M items → 1 item con array)
    ↓
Generate Scripts (considera videos de todas las plataformas)
    ↓
Code in JavaScript (1 item → 3 items de guiones)
    ↓
Save Scripts (guarda en Google Sheets con info de plataformas usadas)
```

---

## 📊 Ejemplo de Salida Multi-Plataforma

### Request a la API:

```json
{
  "platforms": ["tiktok", "instagram", "youtube"],
  "hashtag": "fitness",
  "cantidad": 10
}
```

### Response de la API:

```json
{
  "success": true,
  "total_videos": 30,
  "videos": [
    {
      "platform": "YouTube",
      "viral_score": 125000,
      "views": 2500000,
      "likes": 95000,
      "comments": 1200
    },
    {
      "platform": "TikTok", 
      "viral_score": 89650,
      "views": 1500000,
      "likes": 85000,
      "comments": 1200
    },
    {
      "platform": "Instagram",
      "viral_score": 45800,
      "views": 850000,
      "likes": 42000,
      "comments": 650
    }
    // ... 27 videos más
  ]
}
```

### Después del filtro (viral_score >= 1000):

Solo pasan los videos con buen engagement de todas las plataformas mezclados.

### OpenAI recibe contexto de:

- 5 videos de YouTube
- 4 videos de TikTok  
- 3 videos de Instagram

Y genera 3 guiones que funcionan en TODAS las plataformas.

---

## ✅ Checklist de Actualización

- [ ] Agregar columna "plataformas" en Google Sheets
- [ ] Actualizar body del nodo HTTP Request
- [ ] Aumentar timeout del HTTP Request a 60 segundos
- [ ] (Opcional) Mejorar prompt de OpenAI
- [ ] (Opcional) Guardar info de plataformas en resultados
- [ ] Desplegar API actualizada en Replit/Railway
- [ ] Probar con una sola plataforma primero
- [ ] Probar con 2 plataformas
- [ ] Probar con las 3 plataformas
- [ ] Verificar que los guiones se guardan correctamente

---

## 🔧 Troubleshooting

### "Error: platforms not in request"

Verifica que el nodo HTTP Request tenga:
```json
"platforms": {{ $json.plataformas.split(',') }}
```

### "No videos returned"

- Verifica que tu API esté desplegada y funcionando
- Prueba el endpoint `/health` primero
- Revisa los logs de la API
- Verifica las API Keys en `.env`

### "Timeout error"

- Aumenta timeout a 60-90 segundos
- Reduce la cantidad de videos por plataforma
- Usa menos plataformas simultáneas

### "OpenAI generates bad scripts"

- Verifica que los videos tengan buena metadata
- Asegúrate que `description` no esté vacío
- Mejora el prompt para mencionar las plataformas

---

## 💡 Tips Pro

1. **Comienza solo con YouTube**: Es la más estable
   ```
   plataformas: youtube
   ```

2. **Luego agrega Instagram**:
   ```
   plataformas: youtube,instagram
   ```

3. **Finalmente agrega TikTok**:
   ```
   plataformas: tiktok,instagram,youtube
   ```

4. **Personaliza por nicho**: Algunas plataformas son mejores para ciertos nichos
   - Fitness: TikTok + Instagram
   - Tech: YouTube + TikTok
   - Lifestyle: Instagram + TikTok

5. **Horarios diferentes**: Scrapea en diferentes horarios para más diversidad

---

## 🎨 Visualización del Flujo de Datos

```
Google Sheets: 
{ nicho: "fitness", hashtag: "fitness", cantidad_videos: 10, plataformas: "tiktok,instagram,youtube" }
    ↓
API Request:
{ platforms: ["tiktok","instagram","youtube"], hashtag: "fitness", cantidad: 10 }
    ↓
API Response:
{ videos: [30 videos mezclados de 3 plataformas], total_videos: 30 }
    ↓
Parse: 
30 items separados
    ↓
Filter (viral_score >= 1000):
12 items virales
    ↓
Aggregate:
1 item con array de 12 videos
    ↓
OpenAI:
Genera 3 guiones basados en los 12 videos multi-plataforma
    ↓
Save:
3 guiones guardados en Google Sheets
```

---

## 📈 Ventajas del Sistema Multi-Plataforma

1. **Más datos**: 3x más videos para analizar
2. **Mejor diversidad**: Diferentes estilos de contenido
3. **Mejor calidad**: Los guiones consideran lo mejor de cada plataforma
4. **Flexibilidad**: Puedes elegir qué plataformas usar por nicho
5. **Escalable**: Fácil agregar más plataformas en el futuro

---

¡Listo! Con estos cambios tendrás un sistema de scraping multi-plataforma completamente funcional. 🚀
