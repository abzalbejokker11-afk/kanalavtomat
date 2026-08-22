import json
import os
import google.generativeai as genai
from super_agent import get_reddit_discussions, get_arxiv_papers, get_news

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")

def load_history():
    if os.path.exists("history.json"):
        with open("history.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_history(history):
    with open("history.json", "w", encoding="utf-8") as f:
        json.dump(history[-10:], f, ensure_ascii=False, indent=2) # Oxirgi 10 tasini saqlaymiz (xotira to'lib ketmasligi uchun)

def generate_super_post():
    print("1. Ma'lumotlar yig'ilmoqda...")
    news = get_news()
    social = get_reddit_discussions()
    history_arxiv = get_arxiv_papers()
    
    past_topics = load_history()
    past_context = "\n".join([f"- {t}" for t in past_topics]) if past_topics else "Hali hech qanday post yozilmagan."
    
    prompt = f"""
Siz dunyodagi eng yaxshi ilmiy jurnalist va WADA qoidalari bo'yicha eksportsiz.
Vazifangiz – quyidagi 3 xil manbadan olingan ma'lumotlar asosida HALI HECH KIM YOZMAGAN, ammo mantiqan to'g'ri bo'lgan yangi g'oyani taklif qilish va uni asoslovchi post yozish.

DIQQAT! Quyidagi mavzular oldin yozilgan, ularni mutlaqo TAKRORLAMANG:
{past_context}

Manbalar:
1. Ilmiy yangiliklar: {news}
2. Ijtimoiy tarmoqlardagi muhokamalar: {social}
3. Tarixiy/Ilmiy kontekst (ArXiv): {history_arxiv}

Post O'ZBEK TILIDA quyidagi tuzilishda bo‘lsin:
- Sarlavha (qiziqarli, clickbait emas)
- Kirish (muammo yoki savol)
- Asosiy tahlil (3 ta band, har biri dalillar bilan)
- Yangi taklif (oldinga siljish)
- Xulosa va ochiq savollar
"""

    def call_gemini(prompt_text):
        if not GEMINI_API_KEY:
            return None
        try:
            genai.configure(api_key=GEMINI_API_KEY)
            model = genai.GenerativeModel("gemini-1.5-flash")
            return model.generate_content(prompt_text).text.strip()
        except Exception as e:
            print(f"Gemini xatosi: {e}")
            return None

    def call_ddgs(prompt_text):
        try:
            from duckduckgo_search import DDGS
            ddgs = DDGS()
            return ddgs.chat(prompt_text, model="gpt-4o-mini")
        except Exception as e:
            print(f"DDGS xatosi: {e}")
            return None

    print("2. Qoralama yozilmoqda...")
    first_draft = call_gemini(prompt) or call_ddgs(prompt)
    if not first_draft:
        return None
    
    refine_prompt = f"""
Quyidagi antidoping haqidagi postni tahlil qilib, uni yanada faktlarga, ilmiy dalillarga va chuqur ma'lumotlarga boy qilib qayta yoz. 
Xatolarni tuzat, takrorlarni olib tash. Matnni podkast qilib o'qishga moslashtir. 
Juda qisqa bo'lmasin, yetarlicha boy va ilmiy jihatdan kuchli tahlil bo'lsin (ammo o'ta uzun ham bo'lib ketmasin, 3-4 daqiqalik nutq).
"DIQQAT PROFESSIONAL ANTIDOPING TAHLILI" kabi eski qoliplarni va "Xulosa: Qoidani bilmaslik..." degan yozuvlarni umuman ishlatma. To'g'ridan to'g'ri jiddiy matnga o't.
Matn sof o'zbek tilida bo'lsin.

Qoralama matn:
{first_draft}
"""
    print("3. O'z-o'zini tahrirlamoqda (Self-refinement)...")
    final_post = call_gemini(refine_prompt) or call_ddgs(refine_prompt)
    
    if not final_post:
        return None
    
    # Yangi sarlavhani xotiraga saqlab qolish
    first_line = final_post.split('\n')[0].replace('#', '').strip()
    past_topics.append(first_line)
    save_history(past_topics)
    
    return final_post

if __name__ == "__main__":
    post = generate_super_post()
    print("=== FINAL POST ===")
    print(post)
