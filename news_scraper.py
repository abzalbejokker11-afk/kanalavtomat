import requests
import google.generativeai as genai
import os
import random

GEMINI_KEY = os.environ.get("GEMINI_KEY", "BU_YERGA_KALIT_YOZING")

def get_latest_doping_news():
    print("⏳ Yangiliklar skanerlanmoqda...")
    try:
        from duckduckgo_search import DDGS
        ddgs = DDGS()
        
        # Dunyo bo'yicha doping yangiliklarini topish uchun kengroq qidiruv so'zlari
        queries = ["doping scandal sports", "WADA doping news", "anti-doping agency suspension"]
        query = random.choice(queries)
        
        results = ddgs.news(query, max_results=5)
        if not results:
            return None
        
        # Eng birinchi yangilikni olamiz
        news_item = results[0]
        return {
            "title": news_item.get("title", ""),
            "body": news_item.get("body", ""),
            "url": news_item.get("url", ""),
            "source": news_item.get("source", "Internet")
        }
    except Exception as e:
        print(f"Yangilik qidirishda xatolik: {e}")
        return None

import urllib.parse
import xml.etree.ElementTree as ET
import html

def get_rss_news_fallback():
    url = "https://news.google.com/rss/search?q=doping+sports+scandal&hl=en-US&gl=US&ceid=US:en"
    try:
        r = requests.get(url, timeout=10)
        root = ET.fromstring(r.content)
        items = root.findall('.//item')
        if items:
            top_item = items[0]
            title = top_item.find('title').text
            
            # Tarjima qilish
            title_encoded = urllib.parse.quote(title)
            trans_url = f"https://api.mymemory.translated.net/get?q={title_encoded}&langpair=en|uz"
            tr_res = requests.get(trans_url, timeout=10).json()
            uz_title = tr_res['responseData']['translatedText']
            uz_title = html.unescape(uz_title)
            
            link = top_item.find('link').text
            pubDate = top_item.find('pubDate').text
            
            return f"🌐 JAHON DOPING YANGILIKLARI\n\n📌 {uz_title}\n\n🗓 {pubDate}\n\n🔗 Manba: {link}"
    except Exception as e:
        print(f"RSS xatosi: {e}")
        return None
    return None

def generate_news_post():
    news = get_latest_doping_news()
    
    genai.configure(api_key=GEMINI_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    if news:
        prompt = f"""Sen o'zbek tilida WADA va UzNADA qoidalariga asoslangan yirik sport va antidoping kanalini yurituvchi mutaxassissan. 
Quyidagi jahon yangiligini o'qib, kanal obunachilariga tahliliy, vahimali bo'lmagan, lekin ogohlantiruvchi qiziqarli post yozib ber. 
QATTİY TALAB: Yangilik aynan qaysi davlat, qit'a (masalan, Afrika, Yevropa, AQSh) yoki tashkilotda bo'layotganligini aniq ajratib ko'rsat!

Matnni "🌐 Jahon Doping Yangiliklari" degan mazmunda boshla.
Post oxirida manba sifatida ushbu havolani ({news['url']}) qoldir.

Yangilik sarlavhasi: {news['title']}
Skanerlangan qisqacha mazmuni: {news['body']}
Manba: {news['source']}
"""
    else:
        # MUQOBIL VERSIYA (Fallback): Agar internetdan topa olmasa, o'zi bitta tarixiy/qoida yangiligini yasaydi
        prompt = """Sen o'zbek tilida yirik sport va antidoping kanalini yurituvchi mutaxassissan. 
Ayni damda internetdan so'nggi daqiqadagi yangilik topilmadi, shuning uchun obunachilarni bexabar qoldirmaslik uchun 
WADA yoki UzNADA qoidalaridan bitta juda muhim va qiziqarli faktni yoki tarixda ro'y bergan eng shov-shuvli doping janjalini 
(masalan, Rossiya dopingi, Lance Armstrong yoki Afrikadagi yengil atletikachilar) eslatma sifatida yozib ber. 
Sarlavhani "📌 Antidoping Tarixi va Qoidalari" deb boshla va davlatlarni aniq tilga ol."""

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Gemini API xatosi (Yangilik): {e}")
        # FALLBACK 1: DuckDuckGo Chat
        print("DuckDuckGo Chat (bepul AI) ga o'tilmoqda...")
        try:
            from duckduckgo_search import DDGS
            ddgs = DDGS()
            ddg_prompt = prompt + "\n\nIltimos, o'zbek tilida yoz."
            resp = ddgs.chat(ddg_prompt, model="gpt-4o-mini")
            return resp
        except Exception as e2:
            print(f"DuckDuckGo Chat xatosi: {e2}")
            # FALLBACK 2: RSS + Auto Translate (100% ishonchli, AI kerak emas)
            print("RSS Fallback ga o'tilmoqda...")
            rss_news = get_rss_news_fallback()
            if rss_news:
                return rss_news
            return f"❌ Barcha urinishlar barbod bo'ldi. Internet tarmog'ida muammo bor. Xato: {e2}"

if __name__ == "__main__":
    post = generate_news_post()
    print("YANGILIK POSTI:\n", post)
