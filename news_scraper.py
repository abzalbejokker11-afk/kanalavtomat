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
        return f"❌ Gemini (AI) kalitingizda xato bor! Google qaytargan javob: {e}"

if __name__ == "__main__":
    post = generate_news_post()
    print("YANGILIK POSTI:\n", post)
