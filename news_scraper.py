import random
import os
from ai_generator import generate_super_post

def get_agent_generated_qa():
    # Eski kodni butunlay almashtirdik, endi ai_generator ishlaydi
    return generate_super_post()

def generate_post_script():
    ai_text = get_agent_generated_qa()
    
    if ai_text:
        selected_topic = ai_text
    else:
        topics = [
            "S: Musobaqadan oldin qattiq shamollab qoldim. Aptekadan oddiy 'Teraflyu' yoki 'Taylolxot' ichsam bo'ladimi?\n\nJ: Qat'iyan ehtiyot bo'ling! Bunday kompleks dori vositalari tarkibida ko'pincha 'Efedrin' yoki 'Psevdoefedrin' kabi stimulyatorlar bo'ladi va ular musobaqa davrida taqiqlangan. Har doim dorini qabul qilishdan oldin GlobalDRO.com sayti orqali uning tarkibini tekshiring yoki faqat jamoa shifokori tavsiyasi bilan ruxsat etilgan oddiy Paratsetamol/Ibuprofen qabul qiling.",
            "S: Men xorijdan qimmat va sifatli sport oziq-ovqati (Protin, BCAA) sotib oldim. Lekin uning tozaligiga qanday ishonch hosil qilishim mumkin?\n\nJ: Eng yaxshi himoya — bu 'Informed-Sport' yoki 'NSF Certified for Sport' logotiplarini qidirishdir. Bu sertifikatlar har bir partiya mustaqil laboratoriyada doping moddalariga tekshirilganini kafolatlaydi. Shunga qaramay, 'Qat'iy javobgarlik' qoidasiga ko'ra, tavakkalchilik baribir o'zingizning bo'yningizda qoladi.",
            "S: Doping-ofitser (DCO) mendan test olishga keldi, lekin men ingliz yoki rus tilini tushunmayman. Qanday huquqlarim bor?\n\nJ: Vahimaga tushmang! Siz DCO'dan jarayonni tushunish uchun tarjimon yoki o'z vakilingizni (murabbiy, shifokor) chaqirishni talab qilish huquqiga egasiz. Garchi DCO sizni kutishga majbur bo'lmasa-da, siz bu huquqingizni Doping nazorati bayonnomasining 'Izohlar' (Comments) qismiga yozib qo'yishingiz shart.",
            "S: Boks yoki dzyudoda vazn tashlash (ves quvish) uchun 'Furosemid' kabi siydik haydovchi dorilar ichilsa nima bo'ladi?\n\nJ: Bu sportdagi eng og'ir jinoyatlardan biri hisoblanadi. Diuretiklar (Furosemid) kuch bermaydi, lekin ular organizmdagi boshqa og'ir doping moddalarining izini siydik bilan tez yuvib yuboruvchi 'Niqoblovchi agent' (Masking agent) hisoblanadi. Aniqlansa, 4 yilgacha qat'iy diskvalifikatsiya olasiz.",
            "S: Menga doim dorilarni va vitaminlarni shaxsiy murabbiyim beradi. Agar analizimdan doping chiqsa, murabbiyimni ayblab jazodan qutula olamanmi?\n\nJ: Yo'q. WADA'ning 'Strict Liability' (Qat'iy javobgarlik) qoidasiga ko'ra, sportchining tanasiga kirgan har bir tomchi modda uchun 100% sportchining o'zi javobgar. Murabbiy jazolanishi mumkin, lekin bu sizni oqlamaydi. O'zingiz ichayotgan har bir dorining nomini bilishingiz shart!",
            "S: Astma (ziqna) kasalligim bor. Nafas qisganda ishlatiladigan Ingalatorlar (Salbutamol) doping hisoblanadimi?\n\nJ: Salbutamol ruxsat etilgan doza doirasida (12 soat ichida 800 mikrogrammgacha) ishlatilishi mumkin. Biroq, agar sizga undan kuchliroq preparat kerak bo'lsa, musobaqadan kamida 30 kun oldin 'Terapevtik Istisno' (TUE) hujjati to'ldirilib, tibbiy komissiyaga ruxsat uchun yuborilishi shart.",
            "S: Qon testini topshirishdan qochish uchun 'Ignadan qo'rqish' (Belonefobiya) kasalligimni ro'kach qilsam o'tadimi?\n\nJ: Afsuski, yo'q. Qon testini rad etish qoidabuzarlik sanaladi va 4 yillik chetlatishga sabab bo'ladi. Hatto rasmiy ruhiy kasallik tashxisingiz bo'lsa ham, bu sizni qon topshirish majburiyatidan ozod qilmaydi. Jamoangiz bilan psixologik tayyorgarlik ko'rishingiz zarur.",
            "S: Kutilmagan jarohat sababli tezyordam xizmati menga kuchli og'riq qoldiruvchi (Narkotik) ukol qildi. Karyeram nima bo'ladi?\n\nJ: Shoshilinch hollarda hayot va sog'liq birinchi o'rinda turadi! Muolajani oling, so'ngra jamoa shifokori darhol 'Ortga qaytuvchi TUE' (Retroactive TUE) ga ariza topshirishi kerak. Kasalxona qog'ozlari va shoshilinch holat isbotlansa, WADA buni qonuniy deb qabul qiladi.",
            "S: Musobaqadan so'ng doping ofitseri menga yaqinlashdi, lekin men darhol yuvinishim va kiyim almashtirishim kerak. Ruxsat bormi?\n\nJ: Faqat DCO (Doping-ofitser) ning bevosita kuzatuvi ostida! Sizga xabar berilgan soniyadan boshlab toki test to'liq tugaguniga qadar DCO sizni ko'zdan qochirmasligi shart. Agar uning ruxsatisiz kiyim almashtirish xonasiga kirib ketsangiz, bu testdan qochish deb baholanadi.",
            "S: Internetdan topilgan tabiiy o'simlik choylari va giyohlar doping testida ko'rinadimi?\n\nJ: Juda katta xavf bor! Ko'plab 'Tabiiy energiya beruvchi' giyohlar tarkibida tabiiy Efedrin (Mahuang) kabi taqiqlangan alkaloidlar mavjud. 'Tabiiy' degani 'Ruxsat etilgan' degani emas. O'simlik choylarini iste'mol qilishda yorliqni va GlobalDRO bazasini diqqat bilan o'rganing.",
            "S: O'yin davomida kuchli charchoqni olish uchun har kuni 5-6 banka Energetik ichimlik (RedBull, Gorilla) ichaman. Bu dopingmi?\n\nJ: Kofein 2004-yildan beri WADA ning taqiqlangan ro'yxatidan chiqarilgan. Biroq, u 'Kuzatuv dasturi'da turibdi. Haddan tashqari ko'p energetik ichish yurak urishini buzadi va sog'liqqa o'ta zararli. Qolaversa, ba'zi xalqaro energetiklar tarkibida Geran (DMAA) kabi taqiqlangan moddalar ham uchrashi kuzatilgan.",
            "S: Tizza bo'g'imlarimni davolash uchun shifokor to'g'ridan-to'g'ri bo'g'im ichiga (Diprospan) ukol yozib berdi. Nima qilishim kerak?\n\nJ: 2022-yilgi WADA qoidalariga ko'ra, barcha turdagi Glukokortikoid inyeksiyalari musobaqa davrida qat'iyan taqiqlangan! Agar musobaqagacha davolanish (Washout period) muddati yetarli bo'lmasa, siz albatta TUE (Terapevtik istisno) olishingiz shart, aks holda doping-test musbat chiqadi.",
            "S: A probam musbat chiqdi va meni darhol chetlatishdi. Lekin men 100% tozaman! Endi nima qila olaman?\n\nJ: Umidsizlikka tushmang. Sizda o'z hisobingizdan 7 kun ichida 'B proba'ni ochishni talab qilish huquqi bor. Agar imkoningiz bo'lsa, o'z yurist yoki mustaqil mutaxassisingiz bilan o'sha laboratoriyaga borib, kolba qanday ochilayotganini va tahlil qilinayotganini shaxsan kuzatib turishingiz mumkin.",
            "S: Xorijga yig'inga (sbor) ketyapmiz. ADAMS tizimiga ma'lumotlarni kiritish esdan chiqibdi. Eng yomoni nima bo'lishi mumkin?\n\nJ: Agar doping-inspektor sizni ADAMS da ko'rsatilgan manzildan topa olmasa, bu 'Filing failure' (Ma'lumot kiritmaslik) hisoblanadi. Agar 12 oy ichida bunday xato 3 marta takrorlansa, sportchi xuddi doping qabul qilgandek 1 yildan 2 yilgacha sportdan diskvalifikatsiya qilinadi. Har doim joyingizni yangilab turing!",
            "S: 8 yil oldingi Olimpiadada yutgan edim, endi xotirjam bo'lsam bo'ladimi?\n\nJ: Aslo! WADA sizning qon va siydik namunalaringizni laboratoriya muzlatgichlarida 10 yilgacha saqlaydi. Texnologiyalar rivojlangani sari, eski namunalar yangi usullarda qayta tahlil qilinadi (Re-analysis). 10 yil ichida firibgarlik aniqlansa, barcha medallar tortib olinadi va sharmandali chetlatish yuz beradi."
        ]
        selected_topic = random.choice(topics)
    
    return selected_topic

if __name__ == "__main__":
    post = generate_post_script()
    print("YANGILIK POSTI:\n\n", post)
