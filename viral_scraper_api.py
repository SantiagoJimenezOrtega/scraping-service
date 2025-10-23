from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from datetime import datetime
import time

# ============================================
# IMPORTS PARA SCRAPING
# ============================================
# TikTok
from TikTokApi import TikTokApi
import asyncio

# Instagram  
import instaloader

# YouTube
from googleapiclient.discovery import build

app = Flask(__name__)
CORS(app)

# ============================================
# CONFIGURACIÓN DE APIs
# ============================================
# YouTube API Key (obtener en: https://console.cloud.google.com/)
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY', 'TU_API_KEY_AQUI')

# ============================================
# FUNCIÓN: SCRAPING TIKTOK REAL
# ============================================
async def scrape_tiktok_real(hashtag, cantidad=10):
    """
    Scraping real de TikTok usando TikTokApi
    """
    videos = []
    
    try:
        async with TikTokApi() as api:
            await api.create_sessions(
                ms_tokens=[os.getenv('TIKTOK_MS_TOKEN')],
                num_sessions=1,
                sleep_after=3
            )
            
            # Buscar por hashtag
            tag = api.hashtag(name=hashtag)
            
            async for video in tag.videos(count=cantidad):
                try:
                    stats = video.stats
                    
                    # Calcular engagement rate
                    total_interactions = (
                        stats.get('diggCount', 0) + 
                        stats.get('commentCount', 0) + 
                        stats.get('shareCount', 0)
                    )
                    views = stats.get('playCount', 1)
                    engagement_rate = (total_interactions / views * 100) if views > 0 else 0
                    
                    # Calcular viral score (fórmula mejorada)
                    viral_score = (
                        stats.get('diggCount', 0) * 1 +
                        stats.get('commentCount', 0) * 3 +
                        stats.get('shareCount', 0) * 5 +
                        (engagement_rate * 100)
                    )
                    
                    video_data = {
                        'platform': 'TikTok',
                        'video_id': video.id,
                        'video_url': f"https://www.tiktok.com/@{video.author.username}/video/{video.id}",
                        'author': video.author.username,
                        'author_followers': video.author.stats.get('followerCount', 0),
                        'description': video.desc,
                        'hashtag': hashtag,
                        'views': views,
                        'likes': stats.get('diggCount', 0),
                        'comments': stats.get('commentCount', 0),
                        'shares': stats.get('shareCount', 0),
                        'engagement_rate': round(engagement_rate, 2),
                        'viral_score': int(viral_score),
                        'duration': video.video.duration,
                        'created_at': datetime.fromtimestamp(video.createTime).isoformat(),
                        'music': video.music.title if video.music else None,
                        'scraped_at': datetime.now().isoformat()
                    }
                    
                    videos.append(video_data)
                    
                except Exception as e:
                    print(f"Error procesando video TikTok: {e}")
                    continue
                    
    except Exception as e:
        print(f"Error general TikTok: {e}")
        return []
    
    # Ordenar por viral_score descendente
    videos.sort(key=lambda x: x['viral_score'], reverse=True)
    return videos


# ============================================
# FUNCIÓN: SCRAPING INSTAGRAM REAL
# ============================================
def scrape_instagram_real(hashtag, cantidad=10):
    """
    Scraping real de Instagram usando Instaloader
    """
    videos = []
    
    try:
        L = instaloader.Instaloader()
        
        # Login opcional (recomendado para evitar rate limits)
        username = os.getenv('INSTAGRAM_USER')
        password = os.getenv('INSTAGRAM_PASS')
        
        if username and password:
            try:
                L.login(username, password)
            except Exception as e:
                print(f"Login Instagram falló: {e}")
        
        # Buscar por hashtag
        hashtag_posts = instaloader.Hashtag.from_name(L.context, hashtag)
        
        count = 0
        for post in hashtag_posts.get_posts():
            if count >= cantidad:
                break
            
            # Solo videos o reels
            if post.is_video or post.typename == 'GraphVideo':
                try:
                    # Calcular engagement
                    total_interactions = post.likes + post.comments
                    engagement_rate = (total_interactions / post.owner_profile.followers * 100) if post.owner_profile.followers > 0 else 0
                    
                    # Calcular viral score
                    viral_score = (
                        post.likes * 1 +
                        post.comments * 3 +
                        post.video_view_count * 0.1 +
                        (engagement_rate * 100)
                    )
                    
                    video_data = {
                        'platform': 'Instagram',
                        'video_id': post.shortcode,
                        'video_url': f"https://www.instagram.com/p/{post.shortcode}/",
                        'author': post.owner_username,
                        'author_followers': post.owner_profile.followers,
                        'description': post.caption if post.caption else '',
                        'hashtag': hashtag,
                        'views': post.video_view_count if post.video_view_count else 0,
                        'likes': post.likes,
                        'comments': post.comments,
                        'shares': 0,  # Instagram no expone shares públicamente
                        'engagement_rate': round(engagement_rate, 2),
                        'viral_score': int(viral_score),
                        'duration': post.video_duration if post.video_duration else 0,
                        'created_at': post.date_utc.isoformat(),
                        'music': None,  # No disponible vía API pública
                        'scraped_at': datetime.now().isoformat()
                    }
                    
                    videos.append(video_data)
                    count += 1
                    
                    # Rate limiting
                    time.sleep(2)
                    
                except Exception as e:
                    print(f"Error procesando post Instagram: {e}")
                    continue
                    
    except Exception as e:
        print(f"Error general Instagram: {e}")
        return []
    
    # Ordenar por viral_score
    videos.sort(key=lambda x: x['viral_score'], reverse=True)
    return videos


# ============================================
# FUNCIÓN: SCRAPING YOUTUBE REAL
# ============================================
def scrape_youtube_real(hashtag, cantidad=10):
    """
    Scraping real de YouTube usando YouTube Data API v3
    """
    videos = []
    
    try:
        youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
        
        # Buscar videos por keyword/hashtag
        search_response = youtube.search().list(
            q=hashtag,
            part='id,snippet',
            maxResults=cantidad,
            type='video',
            order='viewCount',  # Ordenar por más vistos
            videoDuration='short'  # Solo videos cortos (< 4 min)
        ).execute()
        
        video_ids = [item['id']['videoId'] for item in search_response['items']]
        
        # Obtener estadísticas detalladas
        videos_response = youtube.videos().list(
            id=','.join(video_ids),
            part='statistics,contentDetails,snippet'
        ).execute()
        
        for video in videos_response['items']:
            try:
                stats = video['statistics']
                snippet = video['snippet']
                
                views = int(stats.get('viewCount', 0))
                likes = int(stats.get('likeCount', 0))
                comments = int(stats.get('commentCount', 0))
                
                # Calcular engagement
                total_interactions = likes + comments
                engagement_rate = (total_interactions / views * 100) if views > 0 else 0
                
                # Calcular viral score
                viral_score = (
                    likes * 1 +
                    comments * 3 +
                    views * 0.01 +
                    (engagement_rate * 100)
                )
                
                # Parsear duración ISO 8601
                duration_str = video['contentDetails']['duration']
                duration_seconds = parse_youtube_duration(duration_str)
                
                video_data = {
                    'platform': 'YouTube',
                    'video_id': video['id'],
                    'video_url': f"https://www.youtube.com/watch?v={video['id']}",
                    'author': snippet['channelTitle'],
                    'author_followers': 0,  # Requiere llamada adicional
                    'description': snippet['description'][:500],
                    'hashtag': hashtag,
                    'views': views,
                    'likes': likes,
                    'comments': comments,
                    'shares': 0,  # No disponible públicamente
                    'engagement_rate': round(engagement_rate, 2),
                    'viral_score': int(viral_score),
                    'duration': duration_seconds,
                    'created_at': snippet['publishedAt'],
                    'music': None,
                    'thumbnail': snippet['thumbnails']['high']['url'],
                    'scraped_at': datetime.now().isoformat()
                }
                
                videos.append(video_data)
                
            except Exception as e:
                print(f"Error procesando video YouTube: {e}")
                continue
                
    except Exception as e:
        print(f"Error general YouTube: {e}")
        return []
    
    # Ordenar por viral_score
    videos.sort(key=lambda x: x['viral_score'], reverse=True)
    return videos


# ============================================
# FUNCIÓN AUXILIAR: Parse duración YouTube
# ============================================
def parse_youtube_duration(duration_str):
    """
    Convierte ISO 8601 duration (PT1M30S) a segundos
    """
    import re
    match = re.match(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', duration_str)
    if not match:
        return 0
    
    hours = int(match.group(1) or 0)
    minutes = int(match.group(2) or 0)
    seconds = int(match.group(3) or 0)
    
    return hours * 3600 + minutes * 60 + seconds


# ============================================
# ENDPOINT PRINCIPAL
# ============================================
@app.route('/scrape', methods=['POST'])
def scrape():
    """
    Endpoint principal para scraping multi-plataforma
    
    Body JSON:
    {
        "platforms": ["tiktok", "instagram", "youtube"],
        "hashtag": "fitness",
        "cantidad": 10
    }
    """
    try:
        data = request.json
        
        # Parámetros
        platforms = data.get('platforms', ['tiktok'])
        hashtag = data.get('hashtag', 'fitness')
        cantidad = int(data.get('cantidad', 10))
        
        # Validar plataformas
        valid_platforms = ['tiktok', 'instagram', 'youtube']
        platforms = [p.lower() for p in platforms if p.lower() in valid_platforms]
        
        if not platforms:
            return jsonify({
                'error': 'No hay plataformas válidas',
                'valid_platforms': valid_platforms
            }), 400
        
        all_videos = []
        errors = {}
        
        # Scraping por plataforma
        for platform in platforms:
            try:
                print(f"Scraping {platform} para #{hashtag}...")
                
                if platform == 'tiktok':
                    videos = asyncio.run(scrape_tiktok_real(hashtag, cantidad))
                    all_videos.extend(videos)
                    
                elif platform == 'instagram':
                    videos = scrape_instagram_real(hashtag, cantidad)
                    all_videos.extend(videos)
                    
                elif platform == 'youtube':
                    videos = scrape_youtube_real(hashtag, cantidad)
                    all_videos.extend(videos)
                    
                print(f"✅ {platform}: {len(videos)} videos")
                
            except Exception as e:
                error_msg = str(e)
                errors[platform] = error_msg
                print(f"❌ Error en {platform}: {error_msg}")
        
        # Ordenar todos los videos por viral_score
        all_videos.sort(key=lambda x: x['viral_score'], reverse=True)
        
        response = {
            'success': True,
            'total_videos': len(all_videos),
            'platforms_scraped': platforms,
            'hashtag': hashtag,
            'videos': all_videos
        }
        
        if errors:
            response['errors'] = errors
        
        return jsonify(response), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# ============================================
# ENDPOINT: Health Check
# ============================================
@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'ok',
        'timestamp': datetime.now().isoformat(),
        'available_platforms': ['tiktok', 'instagram', 'youtube']
    })


# ============================================
# ENDPOINT: Test (datos mock para testing)
# ============================================
@app.route('/test', methods=['POST'])
def test():
    """
    Endpoint de prueba con datos mock
    """
    data = request.json
    hashtag = data.get('hashtag', 'fitness')
    cantidad = int(data.get('cantidad', 5))
    
    videos = []
    for i in range(cantidad):
        videos.append({
            'platform': 'TikTok',
            'video_id': f'test_{i}',
            'hashtag': hashtag,
            'views': 10000 * (i+1),
            'likes': 1000 * (i+1),
            'comments': 100 * (i+1),
            'shares': 50 * (i+1),
            'viral_score': 5000 * (i+1)
        })
    
    return jsonify(videos)


if __name__ == '__main__':
    print("🚀 Viral Scraper API iniciando...")
    print("📋 Endpoints disponibles:")
    print("   POST /scrape - Scraping real multi-plataforma")
    print("   POST /test - Datos de prueba")
    print("   GET /health - Health check")
    app.run(host='0.0.0.0', port=5000, debug=True)
