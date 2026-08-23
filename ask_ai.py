import sys
try:
    from duckduckgo_search import DDGS
    ddgs = DDGS()
    prompt = """
Biz Telegram antidoping kanali uchun bot yozmoqdamiz (Aiogram, Python). 
Bot matnni o'qib (edge-tts), internetdan rasmlar olib video (slaydshou) yasashi kerak. 
Hozir ffmpeg concat demuxer va imageio-ffmpeg ishlatyapmiz, lekin bu serverda (Render free tier) qiyin bo'lyapti yoki qotib qolyapti. 
DeepSeek/AI mutaxassisi sifatida menga videoni eng tez, eng oson va serverni qotirmasdan yasashning 100% tekin, zo'r yechimini aytib ber. 
Yoki umuman video yasashdan ko'ra osonroq qanday formatda jo'natsak foydalanuvchiga qulay?
"""
    resp = ddgs.chat(prompt, model="llama-3.1-70b")
    print(resp)
except Exception as e:
    print("Xato:", e)
