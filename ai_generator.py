import json
import os
import requests

def load_history():
    if os.path.exists("history.json"):
        try:
            with open("history.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def save_history(history):
    with open("history.json", "w", encoding="utf-8") as f:
        json.dump(history[-10:], f, ensure_ascii=False, indent=2)

def call_gemini(prompt_text):
    """Gemini API — REST orqali (kutubxonasiz, barqaror)"""
    api_key = os.environ.get("GEMINI_API_KEY", "")
    if not api_key:
        print("Gemini API kaliti yo'q.")
        return None
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
        payload = {
            "contents": [{"parts": [{"text": prompt_text}]}],
            "generationConfig": {
                "maxOutputTokens": 4096,
                "temperature": 0.9
            }
        }
        resp = requests.post(url, json=payload, timeout=90)
        if resp.status_code == 200:
            data = resp.json()
            text = data["candidates"][0]["content"]["parts"][0]["text"]
            return text.strip()
        else:
            print(f"Gemini HTTP xatosi: {resp.status_code} — {resp.text[:300]}")
            return None
    except Exception as e:
        print(f"Gemini xatosi: {e}")
        return None

def call_duckduckgo_ai(prompt_text):
    """DuckDuckGo AI Chat — bevosita HTTP orqali"""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
            "accept": "text/event-stream",
            "accept-language": "en-US,en;q=0.9",
            "cache-control": "no-cache",
            "content-type": "application/json",
            "pragma": "no-cache",
            "origin": "https://duckduckgo.com",
            "referer": "https://duckduckgo.com/",
            "x-vqd-accept": "1",
        }
        
        status_resp = requests.get("https://duckduckgo.com/duckchat/v1/status", headers=headers, timeout=10)
        vqd4 = status_resp.headers.get("x-vqd-4", "")
        vqdhash = status_resp.headers.get("x-vqd-hash-1", "")
        
        if not vqd4 and not vqdhash:
            print("DuckDuckGo: token olinmadi.")
            return None
        
        chat_headers = dict(headers)
        if vqd4:
            chat_headers["x-vqd-4"] = vqd4
        if vqdhash:
            chat_headers["x-vqd-hash-1"] = vqdhash
        
        chat_payload = {
            "model": "gpt-4o-mini",
            "messages": [{"role": "user", "content": prompt_text}]
        }
        
        chat_resp = requests.post(
            "https://duckduckgo.com/duckchat/v1/chat",
            headers=chat_headers,
            json=chat_payload,
            timeout=60
        )
        
        if chat_resp.status_code != 200:
            print(f"DuckDuckGo chat xatosi: {chat_resp.status_code}")
            return None
        
        full_text = ""
        for line in chat_resp.text.split("\n"):
            if line.startswith("data: "):
                chunk = line[6:]
                if chunk == "[DONE]":
                    break
                try:
                    data = json.loads(chunk)
                    msg = data.get("message", "")
                    if msg:
                        full_text += msg
                except json.JSONDecodeError:
                    continue
        
        return full_text.strip() if len(full_text.strip()) > 50 else None
    except Exception as e:
        print(f"DuckDuckGo AI xatosi: {e}")
        return None

def call_groq_free(prompt_text):
    """Groq bepul API — juda tez (Llama modeli)"""
    groq_key = os.environ.get("GROQ_API_KEY", "")
    if not groq_key:
        return None
    try:
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {groq_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "llama-3.1-70b-versatile",
            "messages": [{"role": "user", "content": prompt_text}],
            "max_tokens": 4000
        }
        resp = requests.post(url, headers=headers, json=payload, timeout=60)
        if resp.status_code == 200:
            return resp.json()["choices"][0]["message"]["content"].strip()
        return None
    except Exception as e:
        print(f"Groq xatosi: {e}")
        return None

def ask_ai(prompt_text):
    """3 qatlamli AI so'rov: Gemini -> DuckDuckGo -> Groq"""
    return call_gemini(prompt_text) or call_duckduckgo_ai(prompt_text) or call_groq_free(prompt_text)

def generate_super_post():
    from super_agent import get_reddit_discussions, get_arxiv_papers, get_news
    
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

Post O'ZBEK TILIDA quyidagi tuzilishda bo'lsin:
- Sarlavha (qiziqarli, clickbait emas)
- Kirish (muammo yoki savol)
- Asosiy tahlil (3 ta band, har biri dalillar bilan)
- Yangi taklif (oldinga siljish)
- Xulosa va ochiq savollar

Juda muhim: Matn kamida 800 so'zdan iborat bo'lsin. Chuqur, boy va ilmiy jihatdan kuchli tahlil yoz.
Savol-Javob formatida emas, to'g'ridan to'g'ri jiddiy tahlil matni bo'lsin.
"""

    print("2. Qoralama yozilmoqda...")
    first_draft = ask_ai(prompt)
    if not first_draft:
        print("Hech bir AI ishlamadi, oflayn zaxiraga o'tilmoqda.")
        return None
    
    refine_prompt = f"""
Quyidagi antidoping haqidagi postni tahlil qilib, uni yanada faktlarga, ilmiy dalillarga va chuqur ma'lumotlarga boy qilib qayta yoz. 
Xatolarni tuzat, takrorlarni olib tash. Matnni podkast qilib o'qishga moslashtir. 
Juda qisqa bo'lmasin, yetarlicha boy va ilmiy jihatdan kuchli tahlil bo'lsin (3-4 daqiqalik nutq).
"DIQQAT PROFESSIONAL ANTIDOPING TAHLILI" kabi eski qoliplarni ishlatma.
Savol-Javob formatida emas, to'g'ridan-to'g'ri jiddiy tahlil matni bo'lsin.
Matn sof o'zbek tilida bo'lsin.

Qoralama matn:
{first_draft}
"""
    print("3. O'z-o'zini tahrirlamoqda (Self-refinement)...")
    final_post = ask_ai(refine_prompt)
    
    if not final_post:
        final_post = first_draft
    
    # Yangi sarlavhani xotiraga saqlab qolish
    first_line = final_post.split('\n')[0].replace('#', '').strip()
    if first_line:
        past_topics.append(first_line)
        save_history(past_topics)
    
    return final_post

if __name__ == "__main__":
    post = generate_super_post()
    print("=== FINAL POST ===")
    print(post)
