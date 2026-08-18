import requests
from bs4 import BeautifulSoup
import google.generativeai as genai
import os
import datetime

GEMINI_KEY = os.environ.get("GEMINI_KEY", "BU_YERGA_KALIT_YOZING")

def get_latest_doping_news():
    print("⏳ Yangiliklar skanerlanmoqda...")
    try:
        from duckduckgo_search import DDGS
        ddgs = DDGS()
        # Search for recent doping news
        results = ddgs.news("doping wada uznada", max_results=3)
        if not results:
            return None
        
        news_item = results[0]
        title = news_item.get("title", "")
        body = news_item.get("body", "")
        url = news_item.get("url", "")
        
        return {"title": title, "body": body, "url": url}
    except Exception as e:
        print(f"Yangilik qidirishda xatolik: {e}")
        return None

def generate_news_post():
    news = get_latest_doping_news()
    if not news:
        return None
        
    genai.configure(api_key=GEMINI_KEY)
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    prompt = f"""Sen o'zbek tilida yirik sport va antidoping kanalini yurituvchi mutaxassissan. 
Quyidagi eng so'nggi yangilikni o'qib, kanal obunachilariga tahliliy, tushunarli va qiziqarli qilib yozib ber. 
Yangilik matnini "Shu saytda doping bo'yicha quyidagi yangilik chiqdi..." degan mazmunda boshla va sarlavhalar bilan boyit.
Post oxirida manba sifatida havola ({news['url']}) qoldir.

Yangilik sarlavhasi: {news['title']}
Yangilik qisqacha mazmuni: {news['body']}
"""
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Gemini API xatosi (Yangilik): {e}")
        return None

if __name__ == "__main__":
    post = generate_news_post()
    if post:
        print("YANGILIK POSTI:\n", post)
    else:
        print("Hech qanday yangilik topilmadi.")
