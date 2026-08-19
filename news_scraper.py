import random

def generate_video_script():
    # 35 ta juda kuchli, professional va keng qamrovli doping mavzulari!
    topics = [
        "Qon dopingi (Blood doping) qanday ishlaydi? Qizil qon tanachalari (eritrotsitlar) sonini sun'iy ravishda ko'paytirish orqali sportchi mushaklariga kislorod yetkazib berishni tezlashtiradi. Ammo bu qonning quyuqlashishiga, yurak xurujiga va to'satdan o'limga olib kelishi mumkin. WADA buni bio-pasport orqali qattiq nazorat qiladi.",
        
        "Rossiya Olimpiya qo'mitasining tizimli doping mojarosi qanday yuz berdi? 2014-yilgi Sochi Olimpiadasida davlat tomonidan qo'llab-quvvatlangan doping dasturi fosh bo'ldi. Doping-nazorat xonasi devoridagi maxfiy teshik orqali musbat qon namunalari toza namunalarga almashtirilgan. Natijada yuzlab sportchilar diskvalifikatsiya qilindi.",
        
        "Lance Armstrong qanday qilib yillar davomida WADA ni aldab kelgan? Tour de France musobaqasining 7 karra g'olibi EPO, testosteron va qon quyish kabi eng murakkab doping usullaridan foydalangan. Uning jamoasi maxsus shifokorlar bilan tillabiriktirib, testlardan muvaffaqiyatli o'tishni o'rgangan. Yakunda uning barcha unvonlari tortib olindi.",
        
        "Meldoniy (Mildronat) mojarosi. Asosan Sharqiy Yevropada yurak kasalliklarini davolash uchun dori sifatida ishlatiladigan bu modda sportchilarda chidamlilikni oshirgani uchun 2016-yilda WADA tomonidan taqiqlandi. Mariya Sharapova kabi yuzlab mashhur sportchilar ehtiyotsizlik sababli sportdan chetlatildi.",
        
        "Yengil atletikada anabolik steroidlar qanday halokatli ta'sir qiladi? Anabolik steroidlar mushak massasini va kuchni tez sur'atlarda oshiradi, ammo jigar yemirilishi, yurak-qon tomir kasalliklari va gormonal buzilishlarga olib keladi. Bunga Ben Jonsonning 1988-yildagi mojarosi yaqqol misol bo'la oladi.",
        
        "Caster Semenya ishi: Testosteron va ayol sportchilardagi gender mojarolari. Tabiatan yuqori testosteron darajasiga ega bo'lgan ayol sportchilar (giperandrogenizm) boshqalarga nisbatan adolatsiz ustunlikka ega hisoblanadi. World Athletics ulardan sun'iy ravishda gormonni pasaytiruvchi dorilar ichishni talab qilib, katta inson huquqlari mojarosiga sabab bo'ldi.",
        
        "Og'ir atletikada doping oqibatlari. Nima uchun Butunjahon Og'ir Atletika Federatsiyasi (IWF) katta inqirozga yuz tutdi? Rahbariyatdagi korrupsiya va yashirilgan musbat doping-testlar tufayli bu sport turi Xalqaro Olimpiya Qo'mitasi tomonidan Olimpiada dasturidan chiqarib yuborilish xavfi ostida qoldi.",
        
        "O'zbekistonda UzNADA (Milliy Antidoping Agentligi) faoliyati. O'zbekiston sportchilarini dopingdan himoya qilish uchun muntazam ravishda musobaqadan tashqari va musobaqa davrida qat'iy doping nazoratlari o'tkazilmoqda. Sportchilarga ruxsatsiz dorilarni qabul qilishning jinoiy va sport karerasini yo'q qiluvchi oqibatlari doimiy tushuntiriladi.",
        
        "Bio-pasport (Athlete Biological Passport) nima va u qanday ishlaydi? WADA sportchining qon va siydik namunalarini yillar davomida to'plab, uning biologik profilini yaratadi. Garchi doping moddasi aniqlanmasa ham, agar qondagi ko'rsatkichlar sun'iy ravishda o'zgarganligi (sakrashlar) sezilsa, sportchi to'g'ridan-to'g'ri dopingda ayblanib, jazolanadi.",
        
        "Mashhur futbolchilardagi doping janjallari. Diego Maradona 1994-yilgi Jahon chempionatida efedrin qabul qilib ushlangan bo'lsa, yaqinda Pol Pogba testosteron qabul qilgani uchun 4 yilga diskvalifikatsiya qilindi. Futbol dunyosi ham doping xavfidan to'liq himoyalanmagan.",
        
        "UFC va aralash jang san'atlarida USADA ning qattiqqo'l doping tekshiruvlari. Jon Jons, Teylor Dillashou va boshqa mashhur chempionlar steroid yoki taqiqlangan moddalar sababli o'z kamarlaridan mahrum bo'lishdi. UFC endilikda o'z mustaqil antidoping dasturini ishlab chiqib, qoidalarni yanada kuchaytirdi.",
        
        "EPO (Eritropoetin) moddasining qora tarixi. Buyraklar tomonidan ishlab chiqariladigan bu gormon sun'iy ravishda yuborilganda chidamlilikni mo'jizaviy tarzda oshiradi. Biroq 90-yillarda EPO qabul qilgan yigirmaga yaqin yosh velosportchilar uxlab yotgan joyida yurak to'xtashi sababli vafot etishgan.",
        
        "Paralimpiya o'yinlarida doping mojarolari. Imkoniyati cheklangan sportchilar nega doping qabul qiladi? Ba'zilar mushak spazmlarini yo'qotish, og'riqni qoldirish yoki qon bosimini sun'iy ko'tarish (boosting) orqali adolatsiz ustunlikka erishishga urinishadi, bu esa qat'iy nazorat qilinadi.",
        
        "Gen dopingi (Genetik modifikatsiya) – kelajak xavfi! Olimlar sportchining DNK sini o'zgartirish orqali chidamlilik genlarini (masalan, miostatin blokatorlari) faollashtirishi mumkin. WADA hozirdanoq genetik dopingni aniqlovchi innovatsion test usullari ustida qizg'in ish olib bormoqda.",
        
        "Sport oziq-ovqatlari (SportPit) va protestinlardagi yashirin xavf! Ko'plab protein va BCAA qutilari ichida yashirin holda steroidlar yoki taqiqlangan stimulyatorlar mavjud. Sportchilar ongsiz ravishda ifloslangan qo'shimchalarni iste'mol qilib, 4 yillik diskvalifikatsiyaga tushib qolish holatlari keskin ko'paydi.",
        
        "Doping faqat g'alaba emas, balki to'satdan o'limga ham olib keladi. Steroid va gormonlarning me'yordan ortiq dozasi jigar saratoni, insult, yurak mushagining kengayishi va buyrak yetishmovchiligi kabi og'ir kasalliklarni chaqiradi. Sog'liq va hayot – medallardan qimmatroqdir!",
        
        "Doping tekshiruvidan bo'yin tovlash qoidalari. Agar sportchi doping ofitseri kelganida undan qochsa, test topshirishni rad etsa yoki qon namunasini buzishga urinsa, u to'g'ridan-to'g'ri doping qabul qilgan deb topiladi va 4 yilga sportdan butunlay chetlatiladi.",
        
        "Terapevtik istisnolar (TUE - Therapeutic Use Exemptions). Agar sportchi haqiqatan ham kasal bo'lsa va davolanish uchun taqiqlangan dori kerak bo'lsa, WADA qat'iy tekshiruvdan so'ng ruxsat berishi mumkin. Ammo ba'zi sportchilar qalbaki astma kasalligi (Norvegiya chang'ichilari) yordamida buni suiiste'mol qilgani fosh etilgan.",
        
        "Muvaffaqiyatsiz 'Klenbuterol' oqlanishlari. Xitoy va Meksikadagi go'sht mahsulotlarida hayvonlarni semirtirish uchun ishlatiladigan klenbuterol moddasi uchraydi. Ba'zi sportchilar doping testdan yiqilganda 'ifloslangan go'sht yegan edim' deb bahona qilishadi, ammo WADA buni har doim ham qabul qilavermaydi.",
        
        "O'zbekistonda yosh sportchilarni antidoping ta'limiga jalb etish. Doping asosan bilimsizlik va ustoz-murabbiylarning bosimi tufayli sodir bo'ladi. Hozirda UzNADA yoshlarni erta yoshdanoq 'Toza sport' g'oyasi ostida o'qitib, kelajakda musobaqalarga toza vijdon bilan chiqishiga zamin yaratmoqda.",
        
        "Trenbolon va hayvonlar uchun dori-darmonlar. Qora bozorda tarqalgan eng kuchli va xavfli steroidlardan biri – asosan mol-qo'ylarni semirtirish uchun mo'ljallangan. Buni qabul qilgan sportchilarda agressiya, ruhiy tushkunlik va ichki a'zolarning parchalanishi kuzatiladi.",
        
        "Qon quyish (Blood transfusion) qanday amalga oshiriladi? Sportchi baland tog'li hududda mashq qilgach, kislorodga boy qonini olib muzlatib qo'yadi. Musobaqa oldidan esa o'z qonini qayta vujudiga quyadi. Bu WADA ni aldashning qadimiy, lekin eng ehtiyotkor texnikalaridan biri bo'lib kelgan.",
        
        "Xitoy suzuvchilari va Trimetazidin mojarosi. 2021-yilda 23 nafar xitoylik suzuvchida musbat test chiqishiga qaramay, mehmonxonadagi 'oshxona ifloslanishi' vajidan ular oqlandi. Bu voqea WADA va USADA (AQSh antidoping) o'rtasida global siyosiy va huquqiy jangga sabab bo'ldi.",
        
        "Taqiqlangan diuretiklar (siydik haydovchi dorilar). Ko'plab sportchilar diuretiklardan nafaqat vazn haydash (boks, dzyudo), balki tanadagi doping moddasini siydik orqali tezroq yuvib chiqarib tashlash (masking agent) maqsadida foydalanadi. Ularning aniqlanishi darhol diskvalifikatsiyaga sabab bo'ladi.",
        
        "WADA Qoidalari qanday yangilanadi? Har yili 1-yanvarda Butunjahon Antidoping Agentligi taqiqlangan dorilar ro'yxatini e'lon qiladi. Sportchilar va jamoa shifokorlari har qanday aptekadan dori sotib olishdan oldin GlobalDRO bazasidan tekshirib ko'rishlari shart.",
        
        "Kamila Valiyeva mojarosi. 15 yoshli figurali uchish yulduzida topilgan Trimetazidin moddasi Butunjahon Olimpiadasini larzaga keltirdi. 'Buvimning stakanidan suv ichgandim' degan oqlanish ish bermadi, unga 4 yillik qamoq (sportdan) jazosi tayinlandi.",
        
        "Sportda Stimulyatorlarning qo'llanilishi (Kokain, Efedrin, Amfetamin). Stimulyatorlar asab tizimini qo'zg'atib, reaksiyani tezlashtiradi va charchoqni his qildirmaydi. Biroq musobaqa paytidagi haddan tashqari zo'riqish insult, infarkt yoki aqldan ozishga olib kelishi ilmiy tasdiqlangan.",
        
        "Iqlimga moslashish xonalari (Hypoxic chambers) va qon dopingiga muqobil qonuniy usullar. Sportchilar qonini qonuniy yo'l bilan boyitish uchun past kislorodli maxsus xonalarda uxlaydilar. Bu qonuniy texnologiya doping vositalarisiz tabiiy chidamlilikni oshirishning zamonaviy yechimi hisoblanadi.",
        
        "Siyosat va Doping: Davlat rahbarlari nega dopingni qoplab kelgan? Ayrim davlatlar uchun sportchilarning medallari geosiyosiy qudrat belgisi hisoblanadi. Shuning uchun ham Maxsus Xizmatlar aralashuvi orqali qon namunalarini almashtirish tarixda chinakam siyosiy mojarolarni yuzaga keltirgan.",
        
        "Antidoping ofitserlarining qat'iy vakolatlari. Doping xodimlari sportchini xohlagan vaqtda: tungi soat 3 da, uyquda, dam olish kunlari yoki hatto to'y marosimida bo'lsa ham kelib tekshirish huquqiga ega. Sportchi ADAMS tizimiga har kunlik turar joyini kiritib borishi majburiydir."
    ]
    
    selected_topic = random.choice(topics)
    
    # Madina huddi diktatordek o'qishi uchun qat'iy, sovuqqon va hukmron ohangdagi buyruq matni.
    full_text = f"🚨 DIQQAT! SPORTDAGI JIDDIY XAVF VA QOIDABUZARLIK! 🚨\n\n{selected_topic}\n\nDoping — bu shunchaki qoidabuzarlik emas, bu sizning sportdagi kelajagingizni, sog'lig'ingizni va insoniylik qadr-qimmatingizni butunlay yakson qiluvchi xiyonatdir! Hech qanday soxta g'alaba umrbod sharmandalikka arzimasligini unutmang! Halol sport — chinakam chempionlarning yagona yo'lidir!\n\n#TozaSport #UzNADA #WADA #DopingControl"

    return full_text
