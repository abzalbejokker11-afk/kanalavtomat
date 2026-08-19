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
    print("Foydalanuvchi talabiga binoan AI o'chirildi, to'g'ridan-to'g'ri RSS ga o'tilmoqda...")
    
    rss_news = get_rss_news_fallback()
    if rss_news:
        return rss_news
    
    return f"❌ Barcha urinishlar barbod bo'ldi. Internet tarmog'ida yoki Google RSS'da muammo bor."

import random

def generate_video_script():
    # 20 ta eng dolzarb va muhokamali doping mavzulari!
    topics = [
        "Jahon sportida qon dopingi (Blood doping) qanday ishlaydi va nima uchun xavfli?",
        "Rossiya Olimpiya qo'mitasining doping mojarosi va uning tarixiy oqibatlari",
        "Lance Armstrong qanday qilib yillar davomida WADA ni aldab kelgan?",
        "Meldoniy mojarosi: Sharqiy Yevropa sportchilarining ommaviy diskvalifikatsiyasi",
        "Yengil atletikada anabolik steroidlar va ularning inson organizmiga halokatli ta'siri",
        "Xitoy suzuvchilarining Tokio Olimpiadasi oldidan ommaviy musbat doping-testlari",
        "Testosteron va ayol sportchilardagi gender mojarolari (Caster Semenya ishi)",
        "Doping-nazoratchilardan qochish sirlari: Sochi-2014 qishki Olimpiadasidagi teshik devorlar",
        "Og'ir atletikada doping qanday qilib butun bir sport turini Olimpiadadan chetlatishiga olib keldi?",
        "O'zbekistonda UzNADA faoliyati va yosh sportchilarni dopingdan himoya qilish",
        "WADA ning eng yangi taqiqlangan dorilar ro'yxati va ehtiyotsizlik qurbonlari",
        "Bio-pasport (Athlete Biological Passport) qanday qilib qon dopingini fosh qilmoqda?",
        "Mashhur futbolchilardagi doping janjallari (Diego Maradona, Pol Pogba ishi)",
        "UFC va aralash jang san'atlarida USADA ning qattiqqo'l doping tekshiruvlari",
        "EPO (Eritropoetin) moddasining velosportdagi qora tarixi",
        "Paralimpiya o'yinlarida doping: Imkoniyati cheklangan sportchilar nima uchun doping qabul qiladi?",
        "Doping tufayli umrbod diskvalifikatsiya qilingan 5 ta eng mashhur sportchi",
        "Doping vs Genetika: Kelajakda genetik modifikatsiya (Gen dopingi) xavfi",
        "Sport oziq-ovqatlari va protestinlardagi yashirin doping moddalari",
        "Doping faqat g'alaba emas, balki to'satdan o'limga ham olib kelishi haqida tibbiy faktlar"
    ]
    
    selected_topic = random.choice(topics)
    
    return f"🛑 {selected_topic}\n\nDoping — bu nafaqat faoliyatingizni, balki hayotingizni ham barbod qiluvchi zahar! Sportdagi g'alaba hech qachon sog'lig'ingizdan ustun bo'lishi mumkin emas. Halol sport — chinakam chempionlar tanlovi!\n\n#TozaSport #UzNADA #WADA"

if __name__ == "__main__":
    post = generate_news_post()
    print("YANGILIK POSTI:\n", post)
