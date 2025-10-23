#!/usr/bin/env python3
"""
Script de prueba para la API Viral Scraper
Úsalo para probar la API localmente antes de conectarla con n8n
"""

import requests
import json
from datetime import datetime

# ============================================
# CONFIGURACIÓN
# ============================================
API_URL = "http://localhost:5000"  # Cambiar si está en otro servidor
HASHTAG = "fitness"
CANTIDAD = 5

# ============================================
# COLORES PARA TERMINAL
# ============================================
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.END}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text.center(60)}{Colors.END}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.END}\n")

def print_success(text):
    print(f"{Colors.GREEN}✅ {text}{Colors.END}")

def print_error(text):
    print(f"{Colors.RED}❌ {text}{Colors.END}")

def print_info(text):
    print(f"{Colors.CYAN}ℹ️  {text}{Colors.END}")

def print_warning(text):
    print(f"{Colors.YELLOW}⚠️  {text}{Colors.END}")

# ============================================
# TEST 1: Health Check
# ============================================
def test_health():
    print_header("TEST 1: Health Check")
    
    try:
        response = requests.get(f"{API_URL}/health", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            print_success(f"API está funcionando correctamente")
            print_info(f"Status: {data['status']}")
            print_info(f"Timestamp: {data['timestamp']}")
            print_info(f"Plataformas disponibles: {', '.join(data['available_platforms'])}")
            return True
        else:
            print_error(f"API respondió con status {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print_error("No se puede conectar a la API")
        print_info(f"Asegúrate de que la API esté corriendo en {API_URL}")
        return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False

# ============================================
# TEST 2: Endpoint de Prueba (Mock Data)
# ============================================
def test_mock_data():
    print_header("TEST 2: Mock Data (Datos de Prueba)")
    
    payload = {
        "hashtag": HASHTAG,
        "cantidad": CANTIDAD
    }
    
    try:
        response = requests.post(
            f"{API_URL}/test",
            json=payload,
            timeout=10
        )
        
        if response.status_code == 200:
            videos = response.json()
            print_success(f"Recibidos {len(videos)} videos de prueba")
            
            if videos:
                print_info("Ejemplo de video:")
                print(json.dumps(videos[0], indent=2))
            
            return True
        else:
            print_error(f"Error: Status {response.status_code}")
            print(response.text)
            return False
            
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False

# ============================================
# TEST 3: Scraping Real - Una Plataforma
# ============================================
def test_single_platform(platform):
    print_header(f"TEST 3: Scraping Real - {platform.upper()}")
    
    payload = {
        "platforms": [platform],
        "hashtag": HASHTAG,
        "cantidad": CANTIDAD
    }
    
    print_info(f"Scraping {CANTIDAD} videos de #{HASHTAG} en {platform}...")
    print_warning("Esto puede tomar 10-30 segundos...")
    
    try:
        response = requests.post(
            f"{API_URL}/scrape",
            json=payload,
            timeout=60
        )
        
        if response.status_code == 200:
            data = response.json()
            
            if data['success']:
                videos = data['videos']
                print_success(f"Scraped {len(videos)} videos de {platform}")
                
                if videos:
                    # Mostrar estadísticas
                    total_views = sum(v['views'] for v in videos)
                    total_likes = sum(v['likes'] for v in videos)
                    avg_engagement = sum(v['engagement_rate'] for v in videos) / len(videos)
                    
                    print_info(f"Total de vistas: {total_views:,}")
                    print_info(f"Total de likes: {total_likes:,}")
                    print_info(f"Engagement promedio: {avg_engagement:.2f}%")
                    
                    # Mostrar top video
                    top_video = max(videos, key=lambda x: x['viral_score'])
                    print_info("\nTop Video:")
                    print(f"  👤 Autor: {top_video['author']}")
                    print(f"  👁️  Vistas: {top_video['views']:,}")
                    print(f"  ❤️  Likes: {top_video['likes']:,}")
                    print(f"  💬 Comentarios: {top_video['comments']:,}")
                    print(f"  🔥 Viral Score: {top_video['viral_score']:,}")
                    print(f"  🔗 URL: {top_video['video_url']}")
                
                return True
            else:
                print_error(f"Error en scraping")
                if 'errors' in data:
                    print(json.dumps(data['errors'], indent=2))
                return False
        else:
            print_error(f"Error: Status {response.status_code}")
            print(response.text)
            return False
            
    except requests.exceptions.Timeout:
        print_error("Timeout - El scraping tomó demasiado tiempo")
        print_info("Intenta con menos videos o una sola plataforma")
        return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False

# ============================================
# TEST 4: Multi-Plataforma
# ============================================
def test_multi_platform():
    print_header("TEST 4: Scraping Multi-Plataforma")
    
    payload = {
        "platforms": ["youtube"],  # Empezar solo con YouTube (más estable)
        "hashtag": HASHTAG,
        "cantidad": 3
    }
    
    print_info("Scraping de múltiples plataformas...")
    print_warning("Esto puede tomar 30-60 segundos...")
    
    try:
        response = requests.post(
            f"{API_URL}/scrape",
            json=payload,
            timeout=90
        )
        
        if response.status_code == 200:
            data = response.json()
            
            if data['success']:
                videos = data['videos']
                print_success(f"Total de videos: {len(videos)}")
                
                # Agrupar por plataforma
                by_platform = {}
                for video in videos:
                    platform = video['platform']
                    if platform not in by_platform:
                        by_platform[platform] = []
                    by_platform[platform].append(video)
                
                # Mostrar stats por plataforma
                for platform, platform_videos in by_platform.items():
                    avg_score = sum(v['viral_score'] for v in platform_videos) / len(platform_videos)
                    print_info(f"{platform}: {len(platform_videos)} videos, avg viral score: {avg_score:,.0f}")
                
                # Mostrar top 3
                print_info("\nTop 3 Videos Virales:")
                top_3 = sorted(videos, key=lambda x: x['viral_score'], reverse=True)[:3]
                for i, video in enumerate(top_3, 1):
                    print(f"\n  {i}. [{video['platform']}] {video['author']}")
                    print(f"     Viral Score: {video['viral_score']:,}")
                    print(f"     Views: {video['views']:,} | Likes: {video['likes']:,}")
                    print(f"     URL: {video['video_url']}")
                
                return True
            else:
                print_error("Error en scraping multi-plataforma")
                if 'errors' in data:
                    print(json.dumps(data['errors'], indent=2))
                return False
        else:
            print_error(f"Error: Status {response.status_code}")
            return False
            
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False

# ============================================
# TEST 5: Validar Estructura de Datos
# ============================================
def test_data_structure():
    print_header("TEST 5: Validar Estructura de Datos")
    
    payload = {
        "platforms": ["youtube"],
        "hashtag": HASHTAG,
        "cantidad": 2
    }
    
    try:
        response = requests.post(
            f"{API_URL}/scrape",
            json=payload,
            timeout=60
        )
        
        if response.status_code == 200:
            data = response.json()
            
            if data['success'] and data['videos']:
                video = data['videos'][0]
                
                # Campos requeridos
                required_fields = [
                    'platform', 'video_id', 'video_url', 'author',
                    'hashtag', 'views', 'likes', 'comments', 'shares',
                    'engagement_rate', 'viral_score', 'duration',
                    'created_at', 'scraped_at'
                ]
                
                missing_fields = [f for f in required_fields if f not in video]
                
                if not missing_fields:
                    print_success("Estructura de datos válida ✓")
                    print_info("Todos los campos requeridos están presentes")
                    
                    # Validar tipos
                    print_info("\nValidando tipos de datos:")
                    validations = [
                        (isinstance(video['views'], int), "views es int"),
                        (isinstance(video['likes'], int), "likes es int"),
                        (isinstance(video['comments'], int), "comments es int"),
                        (isinstance(video['engagement_rate'], (int, float)), "engagement_rate es numérico"),
                        (isinstance(video['viral_score'], int), "viral_score es int"),
                    ]
                    
                    all_valid = True
                    for is_valid, check_name in validations:
                        if is_valid:
                            print_success(check_name)
                        else:
                            print_error(check_name)
                            all_valid = False
                    
                    return all_valid
                else:
                    print_error("Estructura de datos incompleta")
                    print_info(f"Campos faltantes: {', '.join(missing_fields)}")
                    return False
        
        return False
            
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False

# ============================================
# MAIN
# ============================================
def main():
    print(f"\n{Colors.BOLD}🚀 VIRAL SCRAPER API - TEST SUITE{Colors.END}")
    print(f"{Colors.CYAN}{'='*60}{Colors.END}")
    print(f"URL de la API: {Colors.YELLOW}{API_URL}{Colors.END}")
    print(f"Hashtag de prueba: {Colors.YELLOW}#{HASHTAG}{Colors.END}")
    print(f"Cantidad de videos: {Colors.YELLOW}{CANTIDAD}{Colors.END}")
    
    results = []
    
    # Ejecutar tests
    results.append(("Health Check", test_health()))
    
    if results[-1][1]:  # Si health check pasa, continuar
        results.append(("Mock Data", test_mock_data()))
        results.append(("YouTube Scraping", test_single_platform("youtube")))
        # results.append(("Instagram Scraping", test_single_platform("instagram")))  # Descomentar cuando esté configurado
        # results.append(("TikTok Scraping", test_single_platform("tiktok")))  # Descomentar cuando esté configurado
        results.append(("Multi-Platform", test_multi_platform()))
        results.append(("Data Structure", test_data_structure()))
    
    # Resumen
    print_header("RESUMEN DE TESTS")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        color = Colors.GREEN if result else Colors.RED
        print(f"{color}{status}{Colors.END} - {test_name}")
    
    print(f"\n{Colors.BOLD}Total: {passed}/{total} tests pasaron{Colors.END}")
    
    if passed == total:
        print_success("\n🎉 ¡Todos los tests pasaron! La API está lista para usar con n8n")
    else:
        print_warning("\n⚠️  Algunos tests fallaron. Revisa la configuración de la API")
        print_info("Asegúrate de:")
        print("  1. Tener las API keys configuradas en .env")
        print("  2. Haber instalado todas las dependencias")
        print("  3. Tener la API corriendo en el puerto correcto")

if __name__ == "__main__":
    main()
