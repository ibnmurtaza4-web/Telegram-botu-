#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════╗
║          TELEGRAM ANALİTİKA BOTU - TAM KOD                  ║
║          Versiya: 1.0.0  |  Dil: Azərbaycan                 ║
║                                                              ║
║  Quraşdırma:                                                 ║
║    pip install python-telegram-bot==20.7 aiohttp            ║
║                                                              ║
║  İşə salma:                                                  ║
║    python TAM_BOT_KODU.py                                    ║
╚══════════════════════════════════════════════════════════════╝

BOT ƏMRLƏRİ:
  /start          - Bota başla
  /help           - Yardım menyusu
  /analiz @kanal  - Tam analiz
  /er @kanal      - Engagement Rate
  /saxt @kanal    - Saxta abunəçi analizi
  /muqayise @k1 @k2 - İki kanal müqayisəsi
  /admin @kanal   - Adminlər siyahısı
  /link @kanal    - Kanal linki
  /tip @kanal     - Hesab növü
  /hesabla @kanal - Reklam qiyməti
  /haqqimda       - Bot haqqında
  (hər link/username avtomatik analiz olunur)
"""

# ════════════════════════════════════════════
# KONFİQURASİYA
# ════════════════════════════════════════════
BOT_TOKEN = "8683799392:AAHF9vMfdpEP-pHSNEEAWe_4o6uQ9fdRjIA"
VERSION = "1.0.0"


# ════════════════════════════════════════════
# KÖMƏKÇİ FUNKSİYALAR (utils.py)
# ════════════════════════════════════════════
import re

def extract_username(text: str):
    text = text.strip()
    match = re.search(r'(?:https?://)?t\.me/([a-zA-Z][a-zA-Z0-9_]{3,})', text)
    if match:
        return match.group(1)
    match = re.search(r'@([a-zA-Z][a-zA-Z0-9_]{3,})', text)
    if match:
        return match.group(1)
    if re.match(r'^[a-zA-Z][a-zA-Z0-9_]{3,}$', text):
        return text
    return None

def format_number(n: int) -> str:
    if n >= 1_000_000:
        return f"{n/1_000_000:.1f}M"
    elif n >= 1_000:
        return f"{n/1_000:.1f}K"
    return str(n)

def engagement_rate(views: int, subscribers: int) -> float:
    if subscribers == 0:
        return 0.0
    return round((views / subscribers) * 100, 2)

def er_grade(rate: float) -> str:
    if rate >= 80: return "🟢 Əla"
    elif rate >= 50: return "🟡 Yaxşı"
    elif rate >= 20: return "🟠 Orta"
    elif rate >= 5: return "🔴 Zəif"
    else: return "⚫ Çox Zəif"

def build_bar(value: float, max_value: float = 100, length: int = 10) -> str:
    filled = int((value / max_value) * length) if max_value > 0 else 0
    filled = min(filled, length)
    return "█" * filled + "░" * (length - filled)


# ════════════════════════════════════════════
# TELEGRAM API SORĞULARI (telegram_api.py)
# ════════════════════════════════════════════
import aiohttp

BASE = "https://api.telegram.org"

async def get_chat_info(username: str):
    url = f"{BASE}/bot{BOT_TOKEN}/getChat"
    async with aiohttp.ClientSession() as s:
        async with s.post(url, json={"chat_id": f"@{username}"}) as r:
            data = await r.json()
            return data["result"] if data.get("ok") else None

async def get_member_count(username: str):
    url = f"{BASE}/bot{BOT_TOKEN}/getChatMemberCount"
    async with aiohttp.ClientSession() as s:
        async with s.post(url, json={"chat_id": f"@{username}"}) as r:
            data = await r.json()
            return data["result"] if data.get("ok") else None

async def get_chat_admins(username: str):
    url = f"{BASE}/bot{BOT_TOKEN}/getChatAdministrators"
    async with aiohttp.ClientSession() as s:
        async with s.post(url, json={"chat_id": f"@{username}"}) as r:
            data = await r.json()
            return data["result"] if data.get("ok") else None


# ════════════════════════════════════════════
# HANDLER FUNKSİYALARI (handlers.py)
# ════════════════════════════════════════════
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

async def cmd_start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    text = (
        "👋 <b>Telegram Analitika Botuna xoş gəldiniz!</b>\n\n"
        "Bu bot Telegram kanalları, qrupları və istifadəçiləri haqqında ətraflı statistika və analiz aparır.\n\n"
        "📌 <b>Əsas əmrlər:</b>\n"
        "• /analiz @kanal — Kanal/qrup tam analizi\n"
        "• /muqayise @kanal1 @kanal2 — İki kanalı müqayisə et\n"
        "• /er @kanal — Engagement Rate hesabla\n"
        "• /admin @kanal — Kanal adminlərini göstər\n"
        "• /link @kanal — Kanal linki və məlumatı\n"
        "• /tip @kanal — Kanalın növünü müəyyən et\n"
        "• /saxt @kanal — Saxta abunəçi ehtimalı\n"
        "• /hesabla @kanal — Reklam qiyməti təxmini\n"
        "• /help — Tam yardım menyusu\n\n"
        "💡 Sadəcə @username, t.me/link və ya tam link göndərin!"
    )
    await update.message.reply_text(text, parse_mode=ParseMode.HTML)

async def cmd_help(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    text = (
        "📖 <b>BOT YARDIMı - TAM ƏMRLƏR SİYAHISI</b>\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "🔍 <b>ANALİZ ƏMRLƏRİ</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "/analiz @username — Tam analiz\n"
        "/er @username — Engagement Rate\n"
        "/saxt @username — Saxta abunəçi ehtimalı\n"
        "/tip @username — Hesab növü\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "📊 <b>STATİSTİKA ƏMRLƏRİ</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "/muqayise @k1 @k2 — İki kanal müqayisəsi\n"
        "/hesabla @username — Reklam qiyməti\n"
        "/admin @username — Admin siyahısı\n"
        "/link @username — Kanal linki\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "🛠 <b>DİGƏR ƏMRLƏR</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "/start — Bota başla\n"
        "/help — Bu mesaj\n"
        "/haqqimda — Bot haqqında\n\n"
        "💡 <i>İstənilən @username, t.me/link qəbul edilir.</i>"
    )
    await update.message.reply_text(text, parse_mode=ParseMode.HTML)

async def cmd_about(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    text = (
        "🤖 <b>Telegram Analitika Botu</b>\n\n"
        f"📋 <b>Versiya:</b> {VERSION}\n"
        "🌐 <b>Dil:</b> Azərbaycan\n"
        "⚙️ <b>Texnologiya:</b> Python + python-telegram-bot\n\n"
        "📌 <b>Funksiyalar:</b>\n"
        "• Kanal/qrup tam analizi\n"
        "• Baxış/abunəçi müqayisəsi\n"
        "• Engagement rate hesablaması\n"
        "• Saxta abunəçi aşkarlanması\n"
        "• Reklam qiyməti təxmini\n"
        "• İki kanal müqayisəsi\n"
        "• Admin siyahısı\n"
        "• Kanal növü müəyyənləşdirmə\n\n"
        "🔒 Bot yalnız ictimai kanal/qrupları analiz edə bilər."
    )
    await update.message.reply_text(text, parse_mode=ParseMode.HTML)


async def cmd_analiz(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    args = ctx.args
    raw = " ".join(args) if args else ""
    if not raw:
        if update.message.forward_from_chat:
            fc = update.message.forward_from_chat
            username = fc.username
            if not username:
                await update.message.reply_text("❌ Bu kanalın ictimai usernamei yoxdur.")
                return
        else:
            await update.message.reply_text("❗ İstifadə: /analiz @username")
            return
    else:
        username = extract_username(raw)
        if not username:
            await update.message.reply_text("❌ Düzgün username daxil edin.")
            return

    msg = await update.message.reply_text("🔍 Analiz aparılır... Lütfən gözləyin.")
    chat = await get_chat_info(username)
    if not chat:
        await msg.edit_text("❌ Kanal tapılmadı. Username düzgündürmü?")
        return

    members = await get_member_count(username)
    ctype = chat.get("type", "unknown")
    title = chat.get("title") or chat.get("first_name", "Naməlum")
    desc = chat.get("description", "")
    invite = chat.get("invite_link", "")
    pinned = chat.get("pinned_message")
    photo = chat.get("photo")

    type_emoji = {"channel":"📢","supergroup":"👥","group":"👥","private":"🔒","bot":"🤖"}.get(ctype,"❓")
    type_name = {"channel":"Kanal","supergroup":"Superqrup","group":"Qrup","private":"Şəxsi","bot":"Bot"}.get(ctype,ctype)
    members_fmt = format_number(members) if members else "Bilinmir"

    lines = [
        f"{type_emoji} <b>KANAL ANALİZİ</b>","",
        f"📛 <b>Ad:</b> {title}",
        f"🔗 <b>Username:</b> @{username}",
        f"🌐 <b>Link:</b> t.me/{username}",
        f"📂 <b>Növ:</b> {type_name}",
        f"👥 <b>Abunəçi sayı:</b> {members_fmt}",
    ]
    if desc:
        lines.append(f"📝 <b>Açıqlama:</b> {desc[:200]}{'...' if len(desc)>200 else ''}")
    if invite: lines.append(f"🔗 <b>Dəvət linki:</b> {invite}")
    if chat.get("linked_chat_id"): lines.append("🔀 <b>Əlaqəli qrup/kanal var</b>")
    if pinned: lines.append("📌 <b>Sabitlənmiş post var</b>")
    if photo: lines.append("🖼 <b>Profil şəkli var</b>")
    if chat.get("is_verified"): lines.append("✅ <b>TƏSDİQLƏNMİŞ hesab</b>")
    if chat.get("is_scam"): lines.append("⛔ <b>SCAM hesab!</b>")
    if chat.get("is_fake"): lines.append("🚫 <b>FAKE hesab!</b>")

    if members and ctype == "channel":
        lines += ["", "📊 <b>STATİSTİKA TƏXMİNİ</b>",
            f"📉 Zəif baxış (5% ER): ~{format_number(int(members*0.05))}",
            f"📊 Orta baxış (20% ER): ~{format_number(int(members*0.20))}",
            f"📈 Yaxşı baxış (45% ER): ~{format_number(int(members*0.45))}",
            "", f"💡 <i>Dəqiq ER üçün /er @{username}</i>"]

    lines += ["", "🕐 <i>Analiz tamamlandı</i>"]
    await msg.edit_text("\n".join(lines), parse_mode=ParseMode.HTML)

async def cmd_er(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    args = ctx.args
    raw = " ".join(args) if args else ""
    if not raw:
        await update.message.reply_text("❗ İstifadə: /er @username")
        return
    username = extract_username(raw)
    if not username:
        await update.message.reply_text("❌ Düzgün username daxil edin.")
        return

    msg = await update.message.reply_text("📊 Engagement analiz edilir...")
    chat = await get_chat_info(username)
    if not chat:
        await msg.edit_text("❌ Kanal tapılmadı.")
        return
    members = await get_member_count(username)
    if not members:
        await msg.edit_text("❌ Abunəçi sayı alına bilmədi.")
        return

    title = chat.get("title", username)
    scenarios = [
        (int(members*0.02),"Çox aşağı"),(int(members*0.08),"Aşağı"),
        (int(members*0.20),"Orta"),(int(members*0.40),"Yaxşı"),
        (int(members*0.65),"Əla"),(int(members*0.85),"Viral"),
    ]
    lines = [
        "📊 <b>ENGAGEMENT RATE ANALİZİ</b>","",
        f"📛 <b>Kanal:</b> {title}",
        f"👥 <b>Abunəçi:</b> {format_number(members)}","",
        "📈 <b>Baxış/Abunəçi Cədvəli:</b>","",
    ]
    for views, label in scenarios:
        rate = engagement_rate(views, members)
        bar = build_bar(rate, 100, 10)
        grade = er_grade(rate)
        lines.append(f"• {label}: {format_number(views)} baxış → {rate}% [{bar}] {grade}")

    lines += ["","━━━━━━━━━━━━━━━━━━━━━━",
        "📌 <b>ER Şkalası:</b>",
        "🟢 80%+ → Əla  |  🟡 50-79% → Yaxşı",
        "🟠 20-49% → Orta  |  🔴 5-19% → Zəif  |  ⚫ 0-4% → Çox Zəif",
        "","<i>ER = (Baxış / Abunəçi) × 100</i>"]
    await msg.edit_text("\n".join(lines), parse_mode=ParseMode.HTML)


async def cmd_saxt(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    args = ctx.args
    raw = " ".join(args) if args else ""
    if not raw:
        await update.message.reply_text("❗ İstifadə: /saxt @username")
        return
    username = extract_username(raw)
    if not username:
        await update.message.reply_text("❌ Düzgün username daxil edin.")
        return
    msg = await update.message.reply_text("🕵️ Saxta abunəçi analizi aparılır...")
    chat = await get_chat_info(username)
    if not chat:
        await msg.edit_text("❌ Kanal tapılmadı.")
        return
    members = await get_member_count(username)
    title = chat.get("title", username)
    if not members:
        await msg.edit_text("❌ Məlumat alına bilmədi.")
        return

    trust_score = 50
    factors = []
    if chat.get("description"): trust_score += 10; factors.append(("✅","Açıqlama mövcuddur"))
    else: trust_score -= 10; factors.append(("❌","Açıqlama yoxdur"))
    if chat.get("photo"): trust_score += 10; factors.append(("✅","Profil şəkli var"))
    else: trust_score -= 5; factors.append(("⚠️","Profil şəkli yoxdur"))
    if chat.get("pinned_message"): trust_score += 10; factors.append(("✅","Sabitlənmiş post var"))
    else: factors.append(("ℹ️","Sabitlənmiş post yoxdur"))
    if chat.get("linked_chat_id"): trust_score += 10; factors.append(("✅","Əlaqəli qrup/kanal var"))
    if members > 100000: trust_score += 5; factors.append(("📊","Böyük kanal (100K+)"))
    elif members < 1000: trust_score -= 10; factors.append(("⚠️","Kiçik kanal (<1K)"))
    if chat.get("is_verified"): trust_score += 20; factors.append(("✅","Telegram tərəfindən təsdiqlənib"))
    if chat.get("is_scam"): trust_score -= 50; factors.append(("⛔","SCAM olaraq işarələnib!"))
    if chat.get("is_fake"): trust_score -= 40; factors.append(("🚫","FAKE olaraq işarələnib!"))

    trust_score = max(0, min(100, trust_score))
    fake_est = 100 - trust_score

    if trust_score >= 75: verdict, color = "✅ Güvənilir görünür", "🟢"
    elif trust_score >= 55: verdict, color = "🟡 Orta güvən", "🟡"
    elif trust_score >= 35: verdict, color = "🟠 Şübhəli", "🟠"
    else: verdict, color = "🔴 Çox şübhəli", "🔴"

    bar = build_bar(trust_score, 100, 12)
    lines = [
        "🕵️ <b>SAXTA ABUNƏÇİ ANALİZİ</b>","",
        f"📛 <b>Kanal:</b> {title}",
        f"👥 <b>Abunəçi:</b> {format_number(members)}","",
        f"🔐 <b>Güvən Skoru:</b> {trust_score}/100",
        bar,"",
        f"{color} <b>Nəticə:</b> {verdict}",
        f"⚠️ <b>Saxta ehtimalı:</b> ~{fake_est}%","",
        "📋 <b>Analiz Amilləri:</b>",
    ]
    for icon, fact in factors:
        lines.append(f"  {icon} {fact}")
    lines.append("\n<i>⚠️ Bu analiz metadata əsasındadır. 100% dəqiq deyil.</i>")
    await msg.edit_text("\n".join(lines), parse_mode=ParseMode.HTML)

async def cmd_muqayise(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not ctx.args or len(ctx.args) < 2:
        await update.message.reply_text("❗ İstifadə: /muqayise @kanal1 @kanal2")
        return
    u1 = extract_username(ctx.args[0])
    u2 = extract_username(ctx.args[1])
    if not u1 or not u2:
        await update.message.reply_text("❌ Hər iki kanalın usernameni daxil edin.")
        return
    msg = await update.message.reply_text("⚖️ Müqayisə aparılır...")
    import asyncio
    c1, c2, m1, m2 = await asyncio.gather(
        get_chat_info(u1), get_chat_info(u2),
        get_member_count(u1), get_member_count(u2)
    )
    if not c1: await msg.edit_text(f"❌ @{u1} tapılmadı."); return
    if not c2: await msg.edit_text(f"❌ @{u2} tapılmadı."); return

    t1, t2 = c1.get("title",u1), c2.get("title",u2)
    m1, m2 = m1 or 0, m2 or 0
    winner = t1 if m1>=m2 else t2
    max_m = max(m1,m2) or 1

    def feats(c):
        f=[]
        if c.get("description"): f.append("📝")
        if c.get("photo"): f.append("🖼")
        if c.get("pinned_message"): f.append("📌")
        if c.get("linked_chat_id"): f.append("🔀")
        if c.get("is_verified"): f.append("✅")
        return " ".join(f) or "—"

    lines = [
        "⚖️ <b>KANAL MÜQAYİSƏSİ</b>","",
        f"1️⃣ <b>{t1}</b> (@{u1})",
        f"   👥 {format_number(m1)} abunəçi",
        f"   {build_bar(m1,max_m,10)}",
        f"   {feats(c1)}","",
        f"2️⃣ <b>{t2}</b> (@{u2})",
        f"   👥 {format_number(m2)} abunəçi",
        f"   {build_bar(m2,max_m,10)}",
        f"   {feats(c2)}","",
        "━━━━━━━━━━━━━━━━━━━━━━",
        f"🏆 <b>Qalibi (abunəçi):</b> {winner}",
    ]
    if m1>0 and m2>0:
        diff = abs(m1-m2)
        pct = round((diff/min(m1,m2))*100,1)
        lines.append(f"📊 <b>Fərq:</b> {format_number(diff)} ({pct}% daha çox)")
    await msg.edit_text("\n".join(lines), parse_mode=ParseMode.HTML)


async def cmd_admin(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    raw = " ".join(ctx.args) if ctx.args else ""
    if not raw:
        await update.message.reply_text("❗ İstifadə: /admin @username")
        return
    username = extract_username(raw)
    if not username:
        await update.message.reply_text("❌ Düzgün username daxil edin.")
        return
    msg = await update.message.reply_text("👑 Adminlər yüklənir...")
    admins = await get_chat_admins(username)
    chat = await get_chat_info(username)
    if admins is None:
        await msg.edit_text("❌ Adminlər alına bilmədi.")
        return
    title = chat.get("title", username) if chat else username
    lines = [f"👑 <b>{title} — ADMİNLƏR</b>\n"]
    for i, a in enumerate(admins, 1):
        user = a.get("user", {})
        status = a.get("status","")
        name = f"{user.get('first_name','')} {user.get('last_name','')}".strip()
        uname = user.get("username","")
        is_bot = user.get("is_bot",False)
        role_icon = "👑" if status=="creator" else "🛡"
        role = "Sahib" if status=="creator" else "Admin"
        line = f"{i}. {role_icon} <b>{name}</b>{'🤖' if is_bot else ''} [{role}]"
        if uname: line += f" — @{uname}"
        lines.append(line)
    lines.append(f"\n<b>Cəmi:</b> {len(admins)} admin")
    await msg.edit_text("\n".join(lines), parse_mode=ParseMode.HTML)

async def cmd_link(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    raw = " ".join(ctx.args) if ctx.args else ""
    if not raw:
        await update.message.reply_text("❗ İstifadə: /link @username")
        return
    username = extract_username(raw)
    if not username:
        await update.message.reply_text("❌ Düzgün username daxil edin.")
        return
    msg = await update.message.reply_text("🔗 Link məlumatı alınır...")
    chat = await get_chat_info(username)
    if not chat:
        await msg.edit_text("❌ Kanal tapılmadı.")
        return
    members = await get_member_count(username)
    title = chat.get("title") or chat.get("first_name","Naməlum")
    ctype = chat.get("type","")
    invite = chat.get("invite_link","")
    type_name = {"channel":"Kanal","supergroup":"Superqrup","group":"Qrup","bot":"Bot"}.get(ctype,ctype)
    lines = [
        "🔗 <b>LİNK VƏ MƏLUMAT</b>","",
        f"📛 <b>Ad:</b> {title}",
        f"📂 <b>Növ:</b> {type_name}","",
        "🌐 <b>İctimai link:</b>",
        f"<code>https://t.me/{username}</code>","",
    ]
    if invite and invite != f"https://t.me/{username}":
        lines += ["🔑 <b>Dəvət linki:</b>", f"<code>{invite}</code>",""]
    if members:
        lines.append(f"👥 <b>Üzv sayı:</b> {format_number(members)}")
    lines += ["","📋 <b>Paylaşmaq üçün:</b>", f"<code>@{username}</code>"]
    await msg.edit_text("\n".join(lines), parse_mode=ParseMode.HTML)

async def cmd_tip(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    raw = " ".join(ctx.args) if ctx.args else ""
    if not raw:
        await update.message.reply_text("❗ İstifadə: /tip @username")
        return
    username = extract_username(raw)
    if not username:
        await update.message.reply_text("❌ Düzgün username daxil edin.")
        return
    msg = await update.message.reply_text("🔍 Növ müəyyən edilir...")
    chat = await get_chat_info(username)
    if not chat:
        await msg.edit_text("❌ Hesab tapılmadı.")
        return
    members = await get_member_count(username)
    ctype = chat.get("type","unknown")
    title = chat.get("title") or chat.get("first_name",username)
    type_map = {
        "channel":("📢","Kanal","Yayım kanalı. Yalnız adminlər yazır."),
        "supergroup":("👥","Superqrup","Böyük qrup. Üzvlər yazışa bilər."),
        "group":("👫","Qrup","Adi qrup."),
        "private":("👤","Şəxsi hesab","Fərdi istifadəçi."),
        "bot":("🤖","Bot","Telegram botu."),
    }
    emoji, type_label, type_desc = type_map.get(ctype,("❓","Naməlum","Müəyyən edilmədi"))
    badges=[]
    if chat.get("is_verified"): badges.append("✅ Təsdiqlənmiş")
    if chat.get("is_scam"): badges.append("⛔ SCAM")
    if chat.get("is_fake"): badges.append("🚫 FAKE")
    if chat.get("is_restricted"): badges.append("🔒 Məhdudlaşdırılmış")
    if chat.get("linked_chat_id"): badges.append("🔀 Əlaqəli kanal/qrup")
    if not badges: badges.append("🔵 Standart hesab")
    lines = [
        f"{emoji} <b>HESAB NÖVÜ ANALİZİ</b>","",
        f"📛 <b>Ad:</b> {title}",
        f"🔗 <b>Username:</b> @{username}","",
        f"📂 <b>Növ:</b> {type_label}",
        f"📖 <b>İzah:</b> {type_desc}","",
        "🏷 <b>Xüsusiyyətlər:</b>",
    ]
    for b in badges: lines.append(f"  • {b}")
    if members: lines += ["", f"👥 <b>Üzv sayı:</b> {format_number(members)}"]
    await msg.edit_text("\n".join(lines), parse_mode=ParseMode.HTML)

async def cmd_hesabla(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    raw = " ".join(ctx.args) if ctx.args else ""
    if not raw:
        await update.message.reply_text("❗ İstifadə: /hesabla @username")
        return
    username = extract_username(raw)
    if not username:
        await update.message.reply_text("❌ Düzgün username daxil edin.")
        return
    msg = await update.message.reply_text("💰 Reklam qiyməti hesablanır...")
    chat = await get_chat_info(username)
    if not chat:
        await msg.edit_text("❌ Kanal tapılmadı.")
        return
    members = await get_member_count(username)
    title = chat.get("title", username)
    if not members:
        await msg.edit_text("❌ Abunəçi sayı alına bilmədi.")
        return
    def price(v,cpm): return round((v/1000)*cpm,2)
    vl,vm,vh = int(members*0.05), int(members*0.20), int(members*0.45)
    lines = [
        "💰 <b>REKLAM QİYMƏTİ TƏXMİNİ</b>","",
        f"📛 <b>Kanal:</b> {title}",
        f"👥 <b>Abunəçi:</b> {format_number(members)}","",
        "━━━━━━━━━━━━━━━━━━━━━━",
        "📉 <b>Zəif ER (5%):</b>",
        f"   👁 ~{format_number(vl)} baxış  💵 ${price(vl,3)} — ${price(vl,8)}","",
        "📊 <b>Orta ER (20%):</b>",
        f"   👁 ~{format_number(vm)} baxış  💵 ${price(vm,3)} — ${price(vm,8)}","",
        "📈 <b>Yüksək ER (45%):</b>",
        f"   👁 ~{format_number(vh)} baxış  💵 ${price(vh,5)} — ${price(vh,8)}","",
        "━━━━━━━━━━━━━━━━━━━━━━",
        f"📌 <b>Tövsiyə:</b> ${price(vm,3)} — ${price(vm,8)} (orta ER)","",
        "<i>⚠️ CPM $3-8 əsasında təxmini hesablamadır.</i>",
    ]
    await msg.edit_text("\n".join(lines), parse_mode=ParseMode.HTML)

async def msg_auto_detect(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    text = update.message.text or ""
    if update.message.forward_from_chat:
        fc = update.message.forward_from_chat
        uname = fc.username
        if uname:
            ctx.args = [f"@{uname}"]
            await cmd_analiz(update, ctx)
            return
    username = extract_username(text)
    if username:
        ctx.args = [f"@{username}"]
        await cmd_analiz(update, ctx)
    else:
        await update.message.reply_text(
            "❓ Analiz etmək istədiyiniz kanalın linkini göndərin.\n/help — yardım üçün"
        )
