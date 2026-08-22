import random
import os

# Optional imports for AI agents
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

try:
    from duckduckgo_search import DDGS
except ImportError:
    DDGS = None

def get_latest_news_context():
    """DuckDuckGo orqali eng yangi ilmiy yangiliklarni qidirish"""
    if not DDGS:
        return "Terapevtik Istisno (TUE), qon dopingi va sportpitlardagi xavflar haqida umumiy ilmiy tahlil."
    try:
        print("[Agent] So'nggi doping yangiliklari qidirilmoqda...")
        ddgs = DDGS()
        news_results = ddgs.text("WADA doping anti-doping scientific updates", max_results=3)
        news_context = ""
        if news_results:
            for item in news_results:
                news_context += f"- {item.get('title')}: {item.get('body')}\n"
        
        if not news_context:
            return "Terapevtik Istisno (TUE), qon dopingi va sportpitlardagi xavflar haqida umumiy ilmiy tahlil."
        return news_context
    except Exception as e:
        print(f"[Agent] Yangilik qidirishda xato (Tarmoq yoki DDGS cheklovi): {e}")
        return "Terapevtik Istisno (TUE), qon dopingi va sportpitlardagi xavflar haqida umumiy ilmiy tahlil."

def ask_gemini(prompt):
    """Birlamchi Agent: Google Gemini (Eng kuchli va barqaror)"""
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not GEMINI_AVAILABLE or not api_key:
        return None
    try:
        print("[Agent] Gemini API orqali javob olinmoqda...")
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash") # Kichik va tezkor model
        response = model.generate_content(prompt)
        text = response.text.strip()
        if "S:" in text and "J:" in text:
            return text
        return None
    except Exception as e:
        print(f"[Agent] Gemini xato qildi: {e}")
        return None

def ask_ddg(prompt):
    """Ikkilamchi Agent: DuckDuckGo Llama/GPT-4o-mini (Tekin, lekin cheklovlar bo'lishi mumkin)"""
    if not DDGS:
        return None
    try:
        print("[Agent] DuckDuckGo Chat (GPT-4o-mini) orqali javob olinmoqda...")
        ddgs = DDGS()
        response = ddgs.chat(prompt, model="gpt-4o-mini")
        if response and "S:" in response and "J:" in response:
            return response.strip()
        return None
    except Exception as e:
        print(f"[Agent] DDGS Chat xato qildi: {e}")
        return None

def get_agent_generated_qa():
    news_context = get_latest_news_context()
    
    prompt = f"""
Sen WADA qoidalari bo'yicha eng kuchli, ilmiy va ishonchli professor-agentsan. 
Sening vazifang quyidagi **bugungi kungi real yangiliklar va ilmiy ma'lumotlar** (Context) asosida bitta juda ilmiy, professional va mukammal Savol-Javob (Q&A) yaratish. Shu orqali o'zingni takomillashtirib borasan.

Context (So'nggi jahon yangiliklari):
{news_context}

Talablar:
1. Matn sof va mukammal O'zbek tilida bo'lishi shart.
2. Formati faqat shunday bo'lsin:
S: [yangilikka yoki qoidaga asoslangan jiddiy, professional savol]
J: [chuqur ilmiy, WADA qoidalariga asoslangan batafsil va aniq javob]
3. Hech qanday salomlashish, qisqacha kirish so'zlari qo'shilmasin! Matn to'g'ridan-to'g'ri "S:" bilan boshlanishi shart.
4. Agar raqamlar, moddalar nomi, muddatlar kerak bo'lsa, 100% to'g'ri ishlating. 
5. Matn shunday yozilsinki, har bir sportchi bu faktlardan dars olsin!
"""

    # 1. Eng kuchli tahlilchi - Gemini'dan so'raymiz
    ai_text = ask_gemini(prompt)
    if ai_text:
        print("[Agent] Gemini muvaffaqiyatli ishladi!")
        return ai_text
        
    # 2. Agar Gemini bo'lmasa yoki xato qilsa - DDGS'dan so'raymiz
    ai_text = ask_ddg(prompt)
    if ai_text:
        print("[Agent] DDGS muvaffaqiyatli ishladi!")
        return ai_text
        
    # 3. Ikkalasi ham ishlamasa (masalan internet yoki API cheklovlari), zaxiraga qaytamiz
    print("[Agent] Barcha sun'iy intellekt tarmoqlari band, oflayn zaxiraga o'tilmoqda.")
    return None

def generate_post_script():
    ai_text = get_agent_generated_qa()
    
    if ai_text:
        selected_topic = ai_text
    else:
        # 4. ZAXIRA: Oflayn bo'lganda ham uzluksiz ishlashini ta'minlovchi 20 ta mavzu
        topics = [
            "S: Sportchingiz kutilmaganda kasal bo'lib qoldi va davolanish uchun taqiqlangan dori kerak. Nima qilasiz?\n\nJ: Zudlik bilan shifokorga murojaat qilinadi va WADA tizimi orqali 'Terapevtik Istisno' (TUE) hujjati to'ldiriladi. Ariza ADAMS tizimiga yuklanib, ruxsat kelmaguncha dori qabul qilinmaydi. Muddat va hujjatlarning aniqligi hal qiluvchi rol o'ynaydi.",
            "S: Doping-ofitser (DCO) musobaqadan tashqari vaqtda, tungi soat 23:00 da test olish uchun keldi. Sportchi charchaganini aytib, rad eta oladimi?\n\nJ: Mutlaqo yo'q! Qoidalarga ko'ra, testni rad etish yoki qochish – to'g'ridan-to'g'ri doping qabul qilgan deb baholanadi va sportchi 4 yilga diskvalifikatsiya qilinadi. Jarayon darhol bajarilishi shart.",
            "S: Oziq-ovqat qo'shimchasi (SportPit) tarkibida yashirin taqiqlangan modda bo'lsa va sportchi uni bilmay ichgan bo'lsa, kim aybdor?\n\nJ: Qat'iy javobgarlik (Strict Liability) prinsipi! Sportchi o'z vujudiga tushgan har qanday modda uchun shaxsan javobgardir. Ishlab chiqaruvchi aybdorligini isbotlash jazoni yengillashtirishi mumkin, lekin jazodan to'liq qutqarmaydi.",
            "S: Qon dopingi (Blood Doping) nima va WADA uni qanday fosh qiladi?\n\nJ: Bu sportchining o'z qonini oldindan olib qo'yib, musobaqa oldidan qayta quyish orqali kislorodni ko'paytirish usuli. Buni fosh qilish uchun WADA 'Biologik Pasport' (ABP) tizimidan foydalanadi. Qondagi retikulotsitlar keskin o'zgarishi darhol firibgarlikni oshkor qiladi.",
            "S: Sportchi jarohat oldi va shifoxonaga tushdi. Mahalliy shifokorlar unga narkotik og'riq qoldiruvchi dori yuborishdi. Qanday yo'l tutiladi?\n\nJ: Shoshilinch tibbiy yordam holatida dori darhol qabul qilinadi, lekin hayot xavfdan o'tgan zahoti 'Ortga qaytuvchi Terapevtik Istisno' (Retroactive TUE) uchun ariza topshirilishi shart. Barcha kasallik tarixi hujjatlashtirilishi zarur.",
            "S: ADAMS tizimi nima va nima uchun sportchi har kuni o'z turar joyini ko'rsatishi majburiy?\n\nJ: ADAMS – WADA ning xalqaro axborot bazasi. Doping nazorati kutilmagan bo'lishi shart. Agar sportchi 12 oy ichida 3 marta ADAMS orqali ko'rsatilgan joyidan topilmasa, u to'g'ridan-to'g'ri 1 yildan 2 yilgacha diskvalifikatsiya qilinadi.",
            "S: Steroidlar mushaklarni tez o'stiradi, ammo uning yashirin tibbiy halokati nimalarda namoyon bo'ladi?\n\nJ: Tashqi ko'rinish aldamchi! Anabolik steroidlar qonni quyuqlashtirib, tromb hosil qiladi. Natijada yosh sportchilarda ham miyaga qon quyilishi (insult), jigar saratoni va to'satdan yurak to'xtashi kuzatiladi. Bu tibbiy fakt.",
            "S: Trimetazidin yoki Meldoniy kabi yurak dorilari nega sportda qat'iy taqiqlangan?\n\nJ: Bu moddalar yurak mushaklariga kislorod yetishmovchiligi (gipoksiya) sharoitida ishlash imkonini beradi. Sportda bu chidamlilikni sun'iy oshirish hisoblanadi. Uning mavjudligi hatto nanogramm miqdorida bo'lsa ham qoidabuzarlik sanaladi.",
            "S: Mashg'ulotlar bazasida sportchi qoniga 100 ml dan ortiq IV (venadan tomchi) ukol oldi. Bu dopingmi?\n\nJ: Ha! Agar bu shifoxona sharoitida qonuniy tibbiy operatsiya bo'lmasa, har qanday 100 ml dan ortiq tomchi ukol (kapelnitsa) WADA tomonidan taqiqlangan manipulyatsiya hisoblanadi. Bu qonni yuvishga urinish deb baholanadi.",
            "S: Giyohvand moddalar (Kokain, Nasha) qabul qilish doping qoidabuzarligiga kiradimi?\n\nJ: Albatta. Agar ular musobaqa davrida aniqlansa, stimulyator yoki qonunbuzarlik sifatida sanksiya qo'llaniladi. 2021 yildan boshlab 'Substances of Abuse' (Suiiste'mol qilinuvchi moddalar) qoidasi bo'yicha reabilitatsiya va jazo muddatlari belgilanadi.",
            "S: Sportchining ovqatiga raqiblari qasddan doping moddasi qo'shib qo'ysa nima bo'ladi?\n\nJ: Bu 'Sabotaj' (Sabotage) deyiladi. Sportchi bu holatni politsiya va kuzatuv kameralari orqali yuridik jihatdan isbotlab bera olsa, u to'liq oqlanishi mumkin. Ammo isbot yuki (Burden of Proof) 100% sportchining o'zida bo'ladi.",
            "S: Genetik Doping (Gene Doping) degan yangi tahdid qanday ishlaydi?\n\nJ: Bu kelajakning eng qora texnologiyasi. Sportchi DNK siga maxsus vektorlar yuboriladi, natijada inson tanasining o'zi sintetik tarzda gormon (masalan, EPO) ishlab chiqara boshlaydi. WADA hozirda bu mutatsiyalarni aniqlovchi innovatsion mRNK testlarini joriy etmoqda.",
            "S: Musbat doping natijasi chiqdi (A proba). Sportchining keyingi huquqiy qadami qanday bo'lishi kerak?\n\nJ: Vahimaga tushmaslik kerak. Sportchi o'z hisobidan 7 kun ichida 'B proba' ni ochishni talab qilish huquqiga ega. 'B proba' ochilish jarayonida sportchi yoki uning yuridik vakili shaxsan ishtirok etishi va laboratoriya xatolarini nazorat qilishi mumkin.",
            "S: Yosh bolalar va o'smirlar sportida doping aralashuvi kuzatilsa kim javobgar?\n\nJ: Agar voyaga yetmagan sportchidan doping topilsa, WADA asosiy e'tiborni murabbiy va shifokorga qaratadi. Ularga nisbatan 'Personnel Involvement' moddasi orqali umrbod sportdan chetlatish va hatto jinoiy javobgarlik choralari qo'llaniladi.",
            "S: Diuretiklar (siydik haydovchi dorilar) nima uchun doping hisoblanadi, axir ular kuch bermaydi-ku?\n\nJ: Diuretiklar ikki xil firibgarlik uchun ishlatiladi: 1) Kurash va boksda vaznni sun'iy tashlash; 2) 'Masking agent' – ya'ni organizmdagi anabolik steroidlarni siydik orqali tez yuvib, izini yo'qotish uchun. Shuning uchun ham ular qat'iyan man qilingan.",
            "S: Maxsus balandlik kameralari (Hypoxic tents) va kislorod niqoblari dopingmi?\n\nJ: Yo'q. Atmosfera bosimini pasaytiruvchi uskunalar (kislorod tanqisligi yaratuvchi chodirlar) hozirgi kunda qonuniy hisoblanadi. Chunki ular organizmga hech qanday kimyoviy modda kiritmaydi, balki tananing o'z moslashuvchanligini tabiiy ishga tushiradi.",
            "S: Astma bilan kasallangan professional chang'ichi qanday qilib musobaqalarda qatnasha oladi?\n\nJ: Salbutamol kabi astma dorilari muayyan dozagacha (masalan, 12 soat ichida 800 mikrogram) ruxsat etilgan. Agar dozadan oshsa yoki og'irroq dori kerak bo'lsa, zudlik bilan rasmiy tibbiy xulosa (TUE) taqdim etilishi shart. Aks holda bu doping.",
            "S: Musobaqadan so'ng doping ofitseri kelganda, sportchi dush qabul qilib kelishini aytsa bo'ladimi?\n\nJ: Qat'iyan taqiqlanadi! DCO sportchini ogohlantirgan soniyadan boshlab, sportchi ofitserning ko'z o'ngidan bir soniyaga ham yo'qolmasligi shart. Dush qabul qilish, ko'p miqdorda suv ichish yoki peshob qilish ofitser kuzatuvida amalga oshiriladi.",
            "S: Klenbuterol mojarosi nima va u ba'zi mamlakatlarda qanday xavf tug'diradi?\n\nJ: Xitoy, Meksika kabi ba'zi davlatlarda klenbuterol mol go'shtini semirtirish uchun ishlatiladi. Sportchilar ifloslangan steyk yeb qo'yib, doping testdan yiqilishgan. WADA endilikda modda miqdori juda past bo'lsa, go'sht faktini inobatga olish qoidasini kiritgan.",
            "S: Glukokortikoidlar (yallig'lanishga qarshi ukollar) bo'yicha so'nggi 2022-yilgi o'zgarishlar qanday?\n\nJ: Ilgari barcha ukollar ruxsat etilgan edi. Hozirgi kunga kelib, bo'g'im ichiga (intra-articular) yuboriladigan barcha glukokortikoidlar musobaqa davrida qat'iyan taqiqlandi! Davolanish muddati (Washout period) ga qat'iy rioya qilinishi shart."
        ]
        selected_topic = random.choice(topics)
    
    full_text = f"🚨 DIQQAT: PROFESSIONAL ANTIDOPING TAHLILI 🚨\n\n{selected_topic}\n\nXulosa: Qoidani bilmaslik — javobgarlikdan ozod qilmaydi! O'z karyerangiz va sog'lig'ingizni xavf ostiga qo'ymang.\n\n#TozaSport #UzNADA #WADA #AntiDoping"
    return full_text

if __name__ == "__main__":
    post = generate_post_script()
    print("YANGILIK POSTI:\n\n", post)
