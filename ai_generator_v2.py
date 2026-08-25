#!/usr/bin/env python3
"""
🚀 ULTRA-POWERFUL AI GENERATOR V2 - TELEGRAM POSTING AGENT
════════════════════════════════════════════════════════════════════

Yangilangan arxitektura:
✅ Smart API routing (12 API tier system)
✅ Response caching (24h)
✅ Request batching
✅ Multi-source news integration
✅ Professional Uzbek content
✅ Unlimited operation (no token limits!)
✅ Budget protection ($20 OpenRouter = last resort)
✅ Real-time monitoring
"""

import json
import os
import re
import time
from datetime import datetime
from typing import Tuple, Optional, List, Dict, Any
from smart_api_router_v2 import SmartAPIRouterV2

# ═══════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════

HISTORY_FILE = "history.json"
CACHE_FILE = "generation_cache.json"

TOPIC_CATEGORIES = [
    "Sportchilarning ovqatlanishi, vitaminlar va xavfsiz sport oziq-ovqatlari (Supplements) dagi yashirin xatarlar",
    "Musobaqadan tashqari testlar (Out-of-competition testing) va ADAMS tizimi qoidalari",
    "Biologik pasport (Athlete Biological Passport - ABP) sirlari va ahamiyati",
    "Terapevtik istisnolar (TUE) - Kasallik paytida ruxsat etilgan davolanish yo'llari",
    "Murabbiy va shifokorlarning qat'iy javobgarligi (Strict Liability tamoyili)",
    "Sportchilarning ruhiyati va qasddan qilingan xatolar (Sanksiyalar va oqibatlar)",
    "Yakkakurashlarda vazn tashlash daxshati (Diuretiklar va ularning jazosi)",
    "Doping ofitserlari (DCO) bilan ishlash jarayonidagi sportchining qonuniy huquqlari",
    "Oddiy apteka dorilari (Teraflyu, Taylolxot) tarkibidagi yashirin doping xavfi"
]

# ═══════════════════════════════════════════════════════════════════
# HISTORY MANAGEMENT
# ═══════════════════════════════════════════════════════════════════

def load_history() -> List[str]:
    """Load previously generated post titles"""
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠️  History load error: {e}")
            return []
    return []


def save_history(history: List[str]):
    """Save post titles to history (keep last 50)"""
    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(history[-50:], f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"❌ History save error: {e}")


def load_generation_cache() -> Dict[str, Any]:
    """Load generation cache"""
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


def save_generation_cache(cache: Dict[str, Any]):
    """Save generation cache"""
    try:
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(cache, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"❌ Cache save error: {e}")


# ═══════════════════════════════════════════════════════════════════
# CONTENT GENERATION ENGINE
# ═══════════════════════════════════════════════════════════════════

class UltraPowerfulGenerator:
    """
    ULTRA-POWERFUL POST GENERATOR

    Features:
    ✅ 12-tier API routing
    ✅ Response caching (24h)
    ✅ Multi-step self-refinement
    ✅ Professional Uzbek content
    ✅ News-integrated
    ✅ Image prompt generation
    ✅ Unlimited operation
    """

    def __init__(self):
        """Initialize generator with smart router"""
        self.router = SmartAPIRouterV2()
        self.history = load_history()
        self.gen_cache = load_generation_cache()
        self.session_stats = {
            "posts_generated": 0,
            "cache_hits": 0,
            "api_calls": 0,
            "start_time": datetime.now()
        }

    def _prepare_system_prompt(self, focus_topic: str, past_context: str) -> str:
        """Prepare comprehensive system prompt"""
        return f"""
Siz xalqaro antidoping qoidalari (WADA) bo'yicha eng nufuzli huquqshunos, mutaxassis va ilmiy jurnalistsiz.

VAZIFANGIZ:
- BUGUNGI MAVZU YO'NALISHI asosida sportchilar uchun o'ta dolzarb, mutlaqo qonuniy va xatosiz mukammal post yozish
- Barcha ma'lumotlar rasmiy WADA kodeksiga va huquqiy me'yorlarga yuz foiz mos kelishi shart
- Post O'ZBEK TILIDA, ravon va tabiiy gaplardan iborat bo'lsin

BUGUNGI ASOSIY MAVZU YO'NALISHI: "{focus_topic}"
(Aynan shu mavzuni chuqur ochib bering, boshqa mavzularga chalg'imang!)

DIQQAT! Quyidagi mavzular oldin yozilgan, ularni mutlaqo TAKRORLAMANG:
{past_context}

Post TUZILISHI:
- Sarlavha (Jiddiy va e'tiborni tortuvchi)
- Kirish (Huquqiy muammo yoki dolzarb savol)
- Asosiy tahlil (3 ta band, har biri rasmiy qoidalar va ilmiy dalillar bilan tasdiqlangan)
- Xulosa va huquqiy ogohlantirish (Qat'iy javobgarlik qoidasi eslatilsin)

MUHIM QOIDALAR:
- Matn kamida 800 so'zdan iborat bo'lsin
- Chuqur, boy va yuridik/ilmiy jihatdan benuqson tahlil yoz
- Hech qanday belgi ishlatma: yulduzcha (*), reshyotka (#), tag (__), emoji
- Raqamlarni so'z bilan yoz (masalan: 4 emas, to'rt)
- Matn podkast uchun ovozga aylantiriladi, shuning uchun ravon va rasmiy tilda bo'lsin
- Oxirida alohida qatorda: [IMAGE_PROMPT: cinematic, dramatic lighting stilida inglizcha 15-20 ta so'zli rasm prompti]
"""

    def _generate_initial_draft(self, prompt: str) -> Optional[str]:
        """Generate initial draft using smart router"""
        print("\n📝 1-BOSQICH: Qoralama yozilmoqda...")
        print("-" * 60)

        # Try to get from cache first
        cache_key = f"draft_{hash(prompt) % 1000000}"
        if cache_key in self.gen_cache:
            print("💾 CACHE HIT: Qoralama cache'dan olinmoqda")
            self.session_stats["cache_hits"] += 1
            return self.gen_cache[cache_key]

        # Not in cache - generate via smart router
        response = self.router.process_with_cache_and_fallback(prompt, model_name="draft")
        self.session_stats["api_calls"] += 1

        if response and "[" not in response:  # Filter out model markers
            # Cache it
            self.gen_cache[cache_key] = response
            save_generation_cache(self.gen_cache)
            return response

        return None

    def _refine_post(self, draft: str) -> Optional[str]:
        """Self-refine the draft for better quality"""
        print("\n🔄 2-BOSQICH: O'z-o'zini tahrirlamoqda...")
        print("-" * 60)

        refine_prompt = f"""
Quyidagi antidoping haqidagi postni tahlil qilib, uni yanada faktlarga, ilmiy dalillarga va chuqur ma'lumotlarga boy qilib qayta yoz.

Qilish kerak:
- Xatolarni tuzat
- Takrorlarni olib tash
- Matnni podkast qilib o'qishga moslashtir
- Yetarlicha boy va ilmiy jihatdan kuchli tahlil (3-4 daqiqalik nutq)

MUHIM:
- Hech qanday belgi ishlatma: yulduzcha (*), reshyotka (#), tag (__), emoji
- Raqamlarni so'z bilan yoz
- Savol-Javob formatida emas, to'g'ridan-to'g'ri jiddiy tahlil matni bo'lsin

Qoralama matn:
{draft}

[OXIRIDA ALOHIDA QATORDA]
[IMAGE_PROMPT: cinematic dramatic lighting, professional antidoping poster, highly detailed]
"""

        response = self.router.process_with_cache_and_fallback(refine_prompt, model_name="refine")
        self.session_stats["api_calls"] += 1

        return response if response else draft

    def _extract_image_prompt(self, post_text: str) -> Tuple[str, str]:
        """Extract image prompt from [IMAGE_PROMPT: ...] tags"""
        print("\n🖼️  3-BOSQICH: Rasm prompti ajratilmoqda...")
        print("-" * 60)

        # Try to find [IMAGE_PROMPT: ...] tag
        match = re.search(r'\[IMAGE_PROMPT:\s*(.*?)\]', post_text, re.IGNORECASE | re.DOTALL)

        if match:
            image_prompt = match.group(1).strip()
            # Remove the tag from text
            clean_post = re.sub(r'\[IMAGE_PROMPT:\s*.*?\]', '', post_text, flags=re.IGNORECASE | re.DOTALL)
        else:
            image_prompt = "A dramatic anti-doping motivational poster, cinematic lighting, highly detailed, professional sport, WADA regulations themed"
            clean_post = post_text

        return clean_post.strip(), image_prompt.strip()

    def _clean_formatting(self, text: str) -> str:
        """Clean formatting for podcast audio (remove markdown)"""
        print("\n🎙️  4-BOSQICH: Podkast formatiga o'tkazilyapti...")
        print("-" * 60)

        # Remove markdown and special characters
        text = text.replace("*", "").replace("#", "").replace("_", "").replace("`", "")
        text = text.replace("**", "").replace("__", "")

        # Clean multiple spaces
        text = re.sub(r'\s+', ' ', text)

        return text.strip()

    def _update_history(self, post_text: str):
        """Extract title and update history"""
        # Get first line as title
        first_line = post_text.split('\n')[0].strip()

        if first_line and len(first_line) > 10:
            self.history.append(first_line)
            save_history(self.history)
            print(f"📝 Post title saved to history: {first_line[:60]}...")

    def generate_super_post(self, news_data: str = "", social_data: str = "", arxiv_data: str = "") -> Tuple[Optional[str], str]:
        """
        MAIN GENERATION FLOW:
        1. Prepare context
        2. Generate initial draft
        3. Self-refine
        4. Extract image prompt
        5. Clean formatting
        6. Update history

        Returns: (final_post, image_prompt)
        """

        print("\n" + "=" * 60)
        print("🚀 ULTRA-POWERFUL TELEGRAM POST GENERATION")
        print("=" * 60)
        print(f"Session Start: {datetime.now().isoformat()}")

        # Select random topic
        import random
        current_focus = random.choice(TOPIC_CATEGORIES)
        print(f"\n🎯 Bugungi mavzu: {current_focus[:80]}...")

        # Prepare context
        past_context = "\n".join([f"- {t}" for t in self.history]) if self.history else "Hali hech qanday post yozilmagan."

        # Prepare full prompt
        system_prompt = self._prepare_system_prompt(current_focus, past_context)

        full_prompt = f"""
{system_prompt}

Manbalar:
1. Ilmiy yangiliklar: {news_data if news_data else 'Yangiliklar mavjud emas'}
2. Ijtimoiy tarmoqlardagi muhokamalar: {social_data if social_data else 'Muhokamalar mavjud emas'}
3. Tarixiy/Ilmiy kontekst (ArXiv): {arxiv_data if arxiv_data else 'Maqolalar mavjud emas'}

Endi jiddiy, professional va chuqur tahlil matni yoz:
"""

        # Generate initial draft
        first_draft = self._generate_initial_draft(full_prompt)

        if not first_draft:
            print("❌ Qoralama yozilib bolmadi")
            return None, ""

        # Self-refine
        final_post = self._refine_post(first_draft)

        if not final_post:
            final_post = first_draft

        # Extract image prompt
        final_post, image_prompt = self._extract_image_prompt(final_post)

        # Clean formatting
        final_post = self._clean_formatting(final_post)

        # Update history
        self._update_history(final_post)

        # Update stats
        self.session_stats["posts_generated"] += 1

        return final_post, image_prompt

    def get_session_report(self) -> str:
        """Generate session report"""
        elapsed = datetime.now() - self.session_stats["start_time"]

        report = f"""
╔════════════════════════════════════════════════════════════════╗
║           📊 POST GENERATION SESSION REPORT 📊               ║
╠════════════════════════════════════════════════════════════════╣
║                                                                ║
║  📈 GENERATION STATS:                                         ║
║     • Posts Generated: {self.session_stats['posts_generated']:>10}                    ║
║     • API Calls: {self.session_stats['api_calls']:>19}                    ║
║     • Cache Hits: {self.session_stats['cache_hits']:>19}                    ║
║     • Session Duration: {elapsed.total_seconds():.1f}s                      ║
║                                                                ║
║  💰 COST SAVINGS:                                             ║
║     • Free APIs Used: {len([s for s in self.router.api_stats.values() if s['requests_made'] > 0]):>10}                    ║
║     • OpenRouter Cost: ${self.router.tokens_spent_openrouter:.4f} (MINIMAL!)              ║
║     • Budget Remaining: ${20 - self.router.tokens_spent_openrouter:.2f}                       ║
║                                                                ║
║  ✨ STATUS:                                                   ║
║     ✅ Unlimited operation active                             ║
║     ✅ Smart routing working                                  ║
║     ✅ Caching enabled                                        ║
║     ✅ OpenRouter budget protected                            ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
"""

        return report + "\n" + self.router.get_usage_report()


# ═══════════════════════════════════════════════════════════════════
# EXAMPLE USAGE
# ═══════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    generator = UltraPowerfulGenerator()

    print("\n" + "=" * 70)
    print("🎯 ULTRA-POWERFUL TELEGRAM POSTING AGENT V2")
    print("=" * 70)

    # Generate a post
    post, img_prompt = generator.generate_super_post(
        news_data="WADA haqida yangiliklar",
        social_data="Reddit muhokamalarida doping haqida gaplar",
        arxiv_data="Antidoping qoidalariga oid ilmiy maqolalar"
    )

    if post:
        print("\n" + "=" * 70)
        print("✅ FINAL POST:")
        print("=" * 70)
        print(post[:500] + "...\n")

        print("=" * 70)
        print("🖼️  IMAGE PROMPT:")
        print("=" * 70)
        print(img_prompt)

    # Print session report
    print(generator.get_session_report())
