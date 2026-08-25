import random

def generate_post_script():
    # AI bilan generatsiya qilishga urinib ko'ramiz
    try:
        from ai_generator import generate_super_post
        ai_result, img_prompt = generate_super_post()
        if ai_result:
            return ai_result, img_prompt
    except Exception as e:
        print(f"AI generatsiyasida xato, zaxiraga o'tilmoqda: {e}")
    
    # Agar AI ishlamasa, zaxiradagi oflayn format
    default_image_prompt = "A dramatic anti-doping motivational poster, cinematic lighting, highly detailed, professional sport"
    
    topics = [
        "Kasallik va Doping Xavfi\n\nMusobaqa oldidan shamollash sportchi uchun jiddiy sinovdir. 'Teraflyu' yoki 'Taylolxot' kabi kompleks dorilar tarkibida ko'pincha 'Efedrin' kabi kuchli stimulyatorlar mavjud. Ular qat'iyan taqiqlangan dorilar ro'yxatiga kiradi va darhol diskvalifikatsiyaga olib keladi. Dorini qabul qilishdan oldin GlobalDRO.com xalqaro bazasi orqali uning tarkibini tekshirish shart.",
        "Sport Oziq-ovqatlari va Xavfsizlik\n\nXorijdan keltirilgan qimmatbaho sport oziq-ovqatlari ham yuz foiz xavfsiz bo'lmasligi mumkin. Eng ishonchli himoya — qutida 'Informed-Sport' yoki 'NSF Certified for Sport' logotiplarini qidirishdir. Shunga qaramay, WADA ning 'Qat'iy javobgarlik' qoidasiga ko'ra, har qanday holatda ham mas'uliyat sportchining o'zida qoladi.",
        "Doping-ofitser bilan Muloqot Huquqlari\n\nDoping-ofitser kelganda til bilmaslik muammo tug'dirishi mumkin. Bunday vaziyatda sportchi jarayonni to'liq tushunish uchun tarjimon yoki o'z vakilini chaqirishni talab qilish huquqiga ega. Agar bu huquq poymol etilsa, bayonnomaning 'Izohlar' qismiga ona tilida yozib qo'yish kerak.",
        "Yakkakurashlarda Vazn Tashlash Xatarlari\n\nBoks yoki kurash kabi sport turlarida vazn tashlash maqsadiida 'Furosemid' kabi siydik haydovchi dorilar ichish og'ir jinoyat hisoblanadi. Ular organizmdagi boshqa doping moddalarining izini yuvib yuboruvchi 'Niqoblovchi agent' vazifasini bajaradi va 4 yilgacha qat'iy diskvalifikatsiyaga sabab bo'ladi.",
        "Murabbiy va Shifokor Javobgarligi\n\nWADA'ning 'Qat'iy javobgarlik' (Strict Liability) qoidasiga ko'ra, sportchining tanasiga kirgan har bir dori uchun sportchi shaxsan javobgar. Murabbiy yoki shifokorning xatosi sportchini jazodan ozod qilmaydi. Har bir sportchi qabul qilayotgan dori tarkibini bilishi shart.",
        "Astma va Ingalatorlar Qoidasi\n\nNafas qisishi kasalligi bor sportchilar ruxsat etilgan me'yor doirasida (12 soat ichida maksimal 800 mikrogramm) Salbutamol ishlatishlari mumkin. Agar kuchliroq preparat zarur bo'lsa, musobaqadan kamida bir oy oldin 'Terapevtik Istisno' (TUE) hujjati olinishi shart.",
        "Doping Testini Topshirish Majburiyati\n\nRuhiy holat yoki ignadan qo'rqish sababli qon testini topshirishdan bosh tortish — to'g'ridan-to'g'ri musbat natija bilan tenglashtiriladi va 4 yillik chetlatishga olib keladi. Hech qanday sabab qon topshirish majburiyatidan ozod qilmaydi."
    ]
    chosen = random.choice(topics)
    
    selected_topic = f"🎙 Doping va Sport qoidalari bo'yicha Maxsus Tahlil!\n\n{chosen}\n\n⚠️ Eslatma: Doping qoidalari tez-tez o'zgarib turadi. Har doim yangiliklarni kuzatib boring va mutaxassislar bilan maslahatlashing. Barchangizga sog'lom va halol sport tilaymiz!"
    
    return selected_topic, default_image_prompt

if __name__ == "__main__":
    post, img = generate_post_script()
    print("YANGILIK POSTI:\n\n", post)
