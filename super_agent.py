import requests
import json
import os

# Konfiguratsiya
NEWS_API_KEY = "a32f89385b7d42b08f95f1110c5a88ee"

def get_reddit_discussions(query="doping WADA", limit=3):
    """Reddit'dan tekin (API kalitsiz) ma'lumot olish"""
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
        
        return social_context if social_context else "Reddit'da so'nggi paytlarda faol muhokamalar kuzatilmadi."
    except Exception:
        return "Muhokamalar mavjud emas."

def get_arxiv_papers(query="all:\"doping in sports\" OR all:\"WADA\"", max_results=2):
    """ArXiv'dan ilmiy va tarixiy kontekst olish"""
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
            
        return history_context if history_context else "Yangi ilmiy maqolalar topilmadi."
    except Exception as e:
        print(f"ArXiv xatosi: {e}")
        return "Ilmiy baza hozircha yopiq."

def get_news(query="WADA OR doping", language='en'):
    """NewsAPI orqali yangiliklar olish"""
    try:
        from newsapi import NewsApiClient
        newsapi = NewsApiClient(api_key=NEWS_API_KEY)
        top_headlines = newsapi.get_everything(q=query, language=language, sort_by='publishedAt', page_size=3)
        
        news_context = ""
        for article in top_headlines.get('articles', []):
            title = article.get('title')
            desc = article.get('description')
            news_context += f"- {title}: {desc}\n"
            
        return news_context if news_context else "So'nggi 24 soat ichida yirik yangiliklar chiqmadi."
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
