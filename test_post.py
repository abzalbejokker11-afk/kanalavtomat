"""Lokal test — AI generatorni va offline fallbackni tekshirish"""
import news_scraper

print("=" * 60)
print("POST GENERATSIYA BOSHLANMOQDA...")
print("=" * 60)

text = news_scraper.generate_post_script()

print(f"\n{'=' * 60}")
print(f"POST UZUNLIGI: {len(text)} belgi")
print(f"SO'ZLAR SONI: {len(text.split())}")
print(f"{'=' * 60}")
print(text)
print(f"{'=' * 60}")

if len(text) < 50:
    print("❌ XATO: Matn juda qisqa!")
elif "S:" in text or "J:" in text:
    print("❌ XATO: Eski format (S:/J:) topildi!")
else:
    print("✅ Matn formati to'g'ri!")
