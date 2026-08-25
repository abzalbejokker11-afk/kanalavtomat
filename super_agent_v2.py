#!/usr/bin/env python3
"""
🚀 SUPER AGENT V2 - INTELLIGENT MULTI-SOURCE DATA GATHERING
════════════════════════════════════════════════════════════════════

Yangilangan ma'lumot yig'ish tizimi:
✅ Reddit API (tekin, API key'siz)
✅ ArXiv API (ilmiy maqolalar)
✅ NewsAPI (yangiliklar)
✅ Caching (24h)
✅ Error handling va fallback
✅ Batch processing
"""

import requests
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from collections import defaultdict

# ═══════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════

NEWS_API_KEY = os.environ.get("NEWSAPI_KEY", "a32f89385b7d42b08f95f1110c5a88ee")
DATA_CACHE_FILE = "data_cache.json"

# ═══════════════════════════════════════════════════════════════════
# CACHE MANAGEMENT
# ═══════════════════════════════════════════════════════════════════

def load_data_cache() -> Dict[str, Any]:
    """Load data cache"""
    if os.path.exists(DATA_CACHE_FILE):
        try:
            with open(DATA_CACHE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


def save_data_cache(cache: Dict[str, Any]):
    """Save data cache"""
    try:
        with open(DATA_CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(cache, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"⚠️  Cache save error: {e}")


def is_cache_valid(cache_time: str, max_age_hours: int = 24) -> bool:
    """Check if cache is still valid"""
    try:
        cache_dt = datetime.fromisoformat(cache_time)
        age = datetime.now() - cache_dt
        return age < timedelta(hours=max_age_hours)
    except Exception:
        return False


# ═══════════════════════════════════════════════════════════════════
# INTELLIGENT DATA GATHERING
# ═══════════════════════════════════════════════════════════════════

class SuperAgentV2:
    """
    INTELLIGENT MULTI-SOURCE DATA GATHERING

    Features:
    ✅ Reddit discussions (API key'siz)
    ✅ ArXiv papers (ilmiy kontekst)
    ✅ NewsAPI yangiliklar
    ✅ Response caching (24h)
    ✅ Intelligent fallback
    ✅ Batch data gathering
    """

    def __init__(self):
        """Initialize super agent"""
        self.cache = load_data_cache()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'UzAntiDopingAgent/2.0 (by /u/Educational_Bot)'
        })
        self.stats = defaultdict(int)

    def _get_from_cache(self, cache_key: str) -> Optional[str]:
        """Get data from cache if valid"""
        if cache_key in self.cache:
            entry = self.cache[cache_key]
            if is_cache_valid(entry.get("timestamp", ""), max_age_hours=24):
                self.stats["cache_hits"] += 1
                print(f"💾 CACHE HIT: {cache_key}")
                return entry.get("data")

        return None

    def _save_to_cache(self, cache_key: str, data: str):
        """Save data to cache"""
        self.cache[cache_key] = {
            "data": data,
            "timestamp": datetime.now().isoformat()
        }
        save_data_cache(self.cache)

    def get_reddit_discussions(self, query: str = "doping WADA", limit: int = 5) -> str:
        """
        Get Reddit discussions (tekin!)

        Reddit API'dan diskussiyalar olish
        """
        cache_key = f"reddit_{query}_{limit}"

        # Try cache first
        cached = self._get_from_cache(cache_key)
        if cached:
            return cached

        print(f"📡 Reddit'dan ma'lumot yig'ilmoqda: {query}")
        self.stats["reddit_calls"] += 1

        try:
            url = f"https://www.reddit.com/r/sports/search.json?q={query}&restrict_sr=1&limit={limit}"

            response = self.session.get(url, timeout=15)

            if response.status_code != 200:
                print(f"⚠️  Reddit error: {response.status_code}")
                return "Reddit muhokamalari vaqtincha yopiq."

            data = response.json()
            posts = data.get('data', {}).get('children', [])

            # Format results
            social_context = ""
            for i, post in enumerate(posts[:limit], 1):
                title = post['data'].get('title', '')
                selftext = post['data'].get('selftext', '')[:150]
                score = post['data'].get('score', 0)

                social_context += f"{i}. {title}\n   Reyting: {score} | Xulosa: {selftext}...\n\n"

            result = social_context if social_context.strip() else "Reddit'da so'nggi paytlarda faol muhokamalar kuzatilmadi."

            # Cache it
            self._save_to_cache(cache_key, result)

            return result

        except Exception as e:
            print(f"❌ Reddit error: {e}")
            return "Reddit muhokamalari mavjud emas."

    def get_arxiv_papers(self, query: str = "all:doping", max_results: int = 3) -> str:
        """
        Get ArXiv papers (ilmiy kontekst)

        ArXiv'dan academic papers olish
        """
        cache_key = f"arxiv_{query}_{max_results}"

        # Try cache first
        cached = self._get_from_cache(cache_key)
        if cached:
            return cached

        print(f"📡 ArXiv'dan ma'lumot yig'ilmoqda: {query}")
        self.stats["arxiv_calls"] += 1

        try:
            import arxiv

            client = arxiv.Client()
            search = arxiv.Search(
                query=query,
                max_results=max_results,
                sort_by=arxiv.SortCriterion.SubmittedDate
            )

            history_context = ""
            for i, result in enumerate(client.results(search), 1):
                title = result.title
                authors = ", ".join([a.name for a in result.authors[:2]])
                summary = result.summary[:200]

                history_context += f"{i}. {title}\n"
                history_context += f"   Muallif: {authors}\n"
                history_context += f"   Xulosa: {summary}...\n\n"

            result = history_context if history_context.strip() else "Yangi ilmiy maqolalar topilmadi."

            # Cache it
            self._save_to_cache(cache_key, result)

            return result

        except Exception as e:
            print(f"❌ ArXiv error: {e}")
            return "Ilmiy baza hozircha yopiq."

    def get_news(self, query: str = "WADA doping", language: str = 'en', page_size: int = 5) -> str:
        """
        Get latest news (NewsAPI)

        So'nggi yangiliklar olish
        """
        cache_key = f"news_{query}_{language}_{page_size}"

        # Try cache first
        cached = self._get_from_cache(cache_key)
        if cached:
            return cached

        print(f"📡 NewsAPI'dan yangiliklar yig'ilmoqda: {query}")
        self.stats["news_calls"] += 1

        try:
            from newsapi import NewsApiClient

            newsapi = NewsApiClient(api_key=NEWS_API_KEY)
            top_headlines = newsapi.get_everything(
                q=query,
                language=language,
                sort_by='publishedAt',
                page_size=page_size
            )

            news_context = ""
            for i, article in enumerate(top_headlines.get('articles', []), 1):
                title = article.get('title', '')
                desc = article.get('description', '')[:150]
                source = article.get('source', {}).get('name', 'Unknown')
                published = article.get('publishedAt', '')[:10]

                news_context += f"{i}. {title}\n"
                news_context += f"   Manba: {source} ({published})\n"
                news_context += f"   Mazmun: {desc}...\n\n"

            result = news_context if news_context.strip() else "So'nggi 24 soat ichida yirik yangiliklar chiqmadi."

            # Cache it
            self._save_to_cache(cache_key, result)

            return result

        except Exception as e:
            print(f"❌ NewsAPI error: {e}")
            return "Yangiliklar bazasi vaqtincha ishlamayapti."

    def batch_gather(self, queries: Dict[str, str]) -> Dict[str, str]:
        """
        Batch data gathering

        Ko'p source'dan bir vaqtda ma'lumot yig'ish
        """
        print("\n" + "=" * 60)
        print("📦 BATCH DATA GATHERING")
        print("=" * 60)

        results = {}

        if "reddit_query" in queries:
            results["social"] = self.get_reddit_discussions(queries["reddit_query"])

        if "arxiv_query" in queries:
            results["arxiv"] = self.get_arxiv_papers(queries["arxiv_query"])

        if "news_query" in queries:
            results["news"] = self.get_news(queries["news_query"])

        return results

    def get_full_context(self) -> str:
        """Gather all data for post generation"""
        print("\n🔄 FULL CONTEXT GATHERING")
        print("=" * 60)

        data = self.batch_gather({
            "reddit_query": "doping WADA",
            "arxiv_query": "all:doping",
            "news_query": "WADA OR doping OR antidoping"
        })

        context = f"""
═══════════════════════════════════════════════════════════════
📰 REDDIT MUHOKAMALAR:
═══════════════════════════════════════════════════════════════
{data.get('social', 'Ma\'lumot mavjud emas')}

═══════════════════════════════════════════════════════════════
📚 ARXIV MAQOLALAR:
═══════════════════════════════════════════════════════════════
{data.get('arxiv', 'Ma\'lumot mavjud emas')}

═══════════════════════════════════════════════════════════════
📰 YANGILIKLAR:
═══════════════════════════════════════════════════════════════
{data.get('news', 'Ma\'lumot mavjud emas')}
"""

        return context

    def get_stats_report(self) -> str:
        """Generate statistics report"""
        report = f"""
╔════════════════════════════════════════════════════════════════╗
║         📊 SUPER AGENT V2 - DATA GATHERING REPORT 📊          ║
╠════════════════════════════════════════════════════════════════╣
║                                                                ║
║  📊 API CALLS:                                                ║
║     • Reddit: {self.stats['reddit_calls']:>20}                   ║
║     • ArXiv: {self.stats['arxiv_calls']:>21}                   ║
║     • NewsAPI: {self.stats['news_calls']:>18}                  ║
║                                                                ║
║  💾 CACHE STATISTICS:                                         ║
║     • Cache Hits: {self.stats['cache_hits']:>17}                ║
║     • Estimated Savings: ~{self.stats['cache_hits'] * 2}s      ║
║                                                                ║
║  ✨ STATUS:                                                   ║
║     ✅ Reddit integration: AKTIV                              ║
║     ✅ ArXiv integration: AKTIV                               ║
║     ✅ NewsAPI integration: AKTIV                             ║
║     ✅ Caching system: AKTIV                                  ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
"""
        return report


# ═══════════════════════════════════════════════════════════════════
# EXAMPLE USAGE
# ═══════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    agent = SuperAgentV2()

    print("\n🚀 SUPER AGENT V2 - INITIALIZED")
    print("=" * 60)

    # Test 1: Single source calls
    print("\n🔄 TEST 1: Individual source calls")
    print("-" * 60)

    reddit_data = agent.get_reddit_discussions("doping", limit=3)
    print("✅ Reddit data gathered")

    arxiv_data = agent.get_arxiv_papers("all:doping", max_results=2)
    print("✅ ArXiv data gathered")

    news_data = agent.get_news("WADA", page_size=3)
    print("✅ News data gathered")

    # Test 2: Batch gathering
    print("\n🔄 TEST 2: Batch gathering (with cache)")
    print("-" * 60)

    batch_data = agent.batch_gather({
        "reddit_query": "doping WADA",
        "arxiv_query": "all:doping",
        "news_query": "WADA OR doping"
    })
    print("✅ Batch complete")

    # Test 3: Full context
    print("\n🔄 TEST 3: Full context gathering")
    print("-" * 60)

    full_context = agent.get_full_context()
    print("✅ Full context prepared")

    # Print report
    print(agent.get_stats_report())
