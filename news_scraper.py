import os
import random
import urllib.parse
import xml.etree.ElementTree as ET
import html
import requests

def generate_post_script():
    # 20 ta eng zamonaviy, professor-darajasidagi savol-javob mavzulari
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
    print("YANGILIK POSTI:\n", post)
