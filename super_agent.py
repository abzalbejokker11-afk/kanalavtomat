import requests
import json
import os
import time

from kv_storage import kv_get, kv_set

# Konfiguratsiya
NEWS_API_KEY = "a32f89385b7d42b08f95f1110c5a88ee"
CACHE_DURATION_HOURS = 4

def get_cached_data(key):
    try:
        cache = kv_get("api_cache")
        if cache and key in cache:
            # Tekshiramiz, kesh eskirganmi?
            if time.time() - cache[key]['time'] < CACHE_DURATION_HOURS * 3600:
                return cache[key]['data']
    except:
        pass
    return None

def set_cached_data(key, data):
    try:
        cache = kv_get("api_cache") or {}
        cache[key] = {'time': time.time(), 'data': data}
        kv_set("api_cache", cache)
    except:
        pass

def get_reddit_discussions(query="doping WADA", limit=3):
    """Reddit'dan tekin (API kalitsiz) ma'lumot olish"""
    cache_key = f"reddit_{query}_{limit}"
    cached = get_cached_data(cache_key)
    if cached: return cached
    
    try:
        url = f"https://www.reddit.com/r/sports/search.json?q={query}&restrict_sr=1&limit={limit}"
        # Reddit blocks generic User-Agents, using a custom one
        headers = {'User-agent': 'UzAntiDopingBot/1.0 (by /u/Educational_Bot)'}
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code != 200:
            return "Reddit muhokamalari vaqtincha yopiq."
            
        data = response.json()
        posts = data.get('data', {}).get('children', [])
        
        social_context = ""
        for post in posts:
            title = post['data'].get('title', '')
            selftext = post['data'].get('selftext', '')
            social_context += f"- {title}\n  {selftext[:100]}...\n"
        
        result = social_context if social_context else "Reddit'da so'nggi paytlarda faol muhokamalar kuzatilmadi."
        set_cached_data(cache_key, result)
        return result
    except Exception:
        return "Muhokamalar mavjud emas."

def get_arxiv_papers(query="all:\"doping in sports\" OR all:\"WADA\"", max_results=2):
    """ArXiv'dan ilmiy va tarixiy kontekst olish"""
    cache_key = f"arxiv_{query}_{max_results}"
    cached = get_cached_data(cache_key)
    if cached: return cached
    
    try:
        import arxiv
        client = arxiv.Client()
        search = arxiv.Search(
            query=query,
            max_results=max_results,
            sort_by=arxiv.SortCriterion.SubmittedDate
        )
        
        history_context = ""
        for result in client.results(search):
            history_context += f"- {result.title}\n  Xulosa: {result.summary[:150]}...\n"
            
        result = history_context if history_context else "Yangi ilmiy maqolalar topilmadi."
        set_cached_data(cache_key, result)
        return result
    except Exception as e:
        print(f"ArXiv xatosi: {e}")
        return "Ilmiy baza hozircha yopiq."

def get_news(query="WADA OR doping", language='en'):
    """NewsAPI orqali yangiliklar olish"""
    cache_key = f"news_{query}_{language}"
    cached = get_cached_data(cache_key)
    if cached: return cached
    
    try:
        from newsapi import NewsApiClient
        newsapi = NewsApiClient(api_key=NEWS_API_KEY)
        top_headlines = newsapi.get_everything(q=query, language=language, sort_by='publishedAt', page_size=3)
        
        news_context = ""
        for article in top_headlines.get('articles', []):
            title = article.get('title')
            desc = article.get('description')
            news_context += f"- {title}: {desc}\n"
            
        result = news_context if news_context else "So'nggi 24 soat ichida yirik yangiliklar chiqmadi."
        set_cached_data(cache_key, result)
        return result
    except Exception as e:
        print(f"NewsAPI xatosi: {e}")
        return "Yangiliklar bazasi vaqtincha ishlamayapti."

if __name__ == "__main__":
    print("=== REDDIT ===")
    print(get_reddit_discussions())
    print("\n=== ARXIV ===")
    print(get_arxiv_papers())
    print("\n=== NEWSAPI ===")
    print(get_news())
