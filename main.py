import os
import random
from datetime import datetime
from pathlib import Path
from telegram import (
    Update, ReplyKeyboardMarkup, KeyboardButton
)
from telegram.ext import (
    ApplicationBuilder, ContextTypes,
    CommandHandler, MessageHandler, filters
)
from openai import OpenAI

# Zmienne środowiskowe
try:
    openai_api_key = os.environ["OPENAI_API_KEY"]
    telegram_token = os.environ["TELEGRAM_BOT_TOKEN"]
except KeyError as e:
    raise RuntimeError(f"Brakuje zmiennej środowiskowej: {e}")

# Stałe kontaktowe
MSK_PHONE = "733 847 903"
MSK_PHONE_TEL = "+48733847903"
MSK_ADDRESS = "ul. Kościuszki 133B, 26-120 Bliżyn"
MSK_LAT = 51.131503
MSK_LON = 20.793458
MSK_SITE = "https://ratownictwo.online"
MSK_REGULAMIN = f"{MSK_SITE}/regulamin"
MSK_FORMULARZ = f"{MSK_SITE}/formularz"

# OpenAI
client = OpenAI(api_key=openai_api_key)
user_histories = {}
user_last_seen = {}

# Start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["Transport", "Pobranie"],
        ["Szkolenia", "Cennik"],
        ["Lokalizacja", "Kontakt"],
        [KeyboardButton("📞 Zadzwoń teraz")],
        [KeyboardButton("📍 Pokaż lokalizację")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "Witaj. Tu MSK Ratownictwo Medyczne. 🩺\n"
        "Świadczymy usługi premium poza systemem NFZ.\n"
        "Jak mogę Ci pomóc?\n\n"
        "ℹ️ W nagłych przypadkach – dzwoń 112 lub 999.",
        reply_markup=reply_markup
    )

# Komendy tematyczne
async def uslugi(update, context): await update.message.reply_text(
    "Nasze usługi:\n"
    "✅ Transport medyczny\n"
    "✅ Pobrania krwi w domu\n"
    "✅ Cewnikowanie, opatrunki\n"
    "✅ Szkolenia i zabezpieczenia\n"
    f"📞 {MSK_PHONE}"
)

async def kontakt(update, context): await update.message.reply_text(
    f"📞 Telefon: {MSK_PHONE}\n📍 Adres: {MSK_ADDRESS}\n🌐 {MSK_SITE}"
)

async def lokalizacja(update, context):
    await update.message.reply_location(latitude=MSK_LAT, longitude=MSK_LON)

async def formularz(update, context):
    await update.message.reply_text(
        f"📄 Formularz zgłoszeniowy:\n👉 {MSK_FORMULARZ}\n📞 {MSK_PHONE}"
    )

async def regulamin(update, context):
    await update.message.reply_text(f"📘 Regulamin świadczenia usług:\n👉 {MSK_REGULAMIN}")

async def faq(update, context): await update.message.reply_text(
    "❓ Najczęściej zadawane pytania:\n\n"
    "🔹 Czy działacie w nocy/weekendy?\nTak. 📞 733 847 903\n"
    "🔹 Czy to usługi NFZ?\nNie – usługi są odpłatne i profesjonalne.\n"
    "🔹 Czy transportujecie osoby leżące?\nTak, z opieką medyczną.\n"
    "🔹 Czy pobieracie krew w domu?\nTak, z wynikami online.\n"
    "🔹 Czy wystawiacie faktury?\nTak, VAT i dokumentację medyczną."
)

async def zobacz(update, context):
    folder = Path("pictures_msk")
    if not folder.exists():
        await update.message.reply_text("Brak folderu 'pictures_msk'.")
        return
    images = list(folder.glob("*.*"))
    if not images:
        await update.message.reply_text("Brak dostępnych zdjęć.")
        return
    captions = [
        "Ambulans MSK – gotowy do działania.",
        "Sprzęt, który robi różnicę.",
        "Nasza codzienność – Twoje bezpieczeństwo.",
        "Działamy cicho, ale skutecznie.",
        "Pomagamy tam, gdzie inni nie mogą."
    ]
    selected = random.choice(images)
    caption = random.choice(captions)
    with open(selected, "rb") as photo:
        await update.message.reply_photo(photo=photo, caption=caption)

# Usługi szczegółowe
async def transport(update, context): await update.message.reply_text(
    "🚑 Transport medyczny:\n▪️ Dla osób leżących i chodzących\n"
    "▪️ Nosze, schodołaz, opieka medyczna\n"
    "▪️ Trasy lokalne i ogólnopolskie\n"
    f"📞 {MSK_PHONE}"
)

async def pobranie(update, context): await update.message.reply_text(
    "💉 Pobrania krwi w domu pacjenta:\n▪️ Komfortowo i bez kolejek\n"
    "▪️ Materiał przekazujemy do laboratorium\n"
    f"📞 {MSK_PHONE}"
)

async def szkolenia(update, context): await update.message.reply_text(
    "🧯 Szkolenia:\n▪️ Pierwsza pomoc BLS/AED\n▪️ Kursy KPP\n▪️ Szkolenia dla firm/szkół\n"
    f"📞 {MSK_PHONE}"
)

async def cennik(update, context): await update.message.reply_text(
    "💰 Cennik (orientacyjny):\n"
    "▪️ Pobranie krwi – od 50 zł\n"
    "▪️ Transport – od 180 zł\n"
    "▪️ Usługi pielęgniarskie – od 120 zł\n"
    "▪️ Szkolenia – od 100 zł/os.\n"
    f"📞 {MSK_PHONE}"
)

async def dyzur(update, context): await update.message.reply_text(
    "🕐 Dyżury 7 dni w tygodniu, również w święta.\n"
    "W pilnych sprawach: 📞 733 847 903"
)

async def zapomnij(update, context):
    user_histories.pop(str(update.effective_user.id), None)
    await update.message.reply_text("Twoja historia została wyczyszczona.")

# Rozpoznanie przycisków
async def klawiatura_rozpoznanie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    if "transport" in text:
        await transport(update, context)
    elif "pobranie" in text:
        await pobranie(update, context)
    elif "szkolenia" in text:
        await szkolenia(update, context)
    elif "cennik" in text:
        await cennik(update, context)
    elif "lokalizacja" in text:
        await lokalizacja(update, context)
    elif "kontakt" in text:
        await kontakt(update, context)
    elif "zadzwoń" in text:
        await update.message.reply_text(f"📞 Kliknij, aby zadzwonić: tel:{MSK_PHONE_TEL}")
    elif "pokaż lokalizację" in text:
        await lokalizacja(update, context)
    else:
        await gpt_reply(update, context)

# GPT z pamięcią
async def gpt_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    text = update.message.text
    user_last_seen[user_id] = datetime.now()
    history = user_histories.get(user_id, [])
    history.append({"role": "user", "content": text})
    prompt = (
        "Jesteś przedstawicielem MSK Ratownictwo Medyczne – podmiotu leczniczego. "
        "Świadczysz profesjonalne usługi medyczne poza systemem NFZ: transport, pobrania, opatrunki, szkolenia. "
        "Odpowiadasz z empatią i konkretnie. W razie zagrożenia przypominasz: zadzwoń 112 lub 999. "
        "Nigdy nie mów, że jesteś AI."
    )
    messages = [{"role": "system", "content": prompt}] + history[-10:]
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages
        )
        reply = response.choices[0].message.content
        history.append({"role": "assistant", "content": reply})
        user_histories[user_id] = history
    except Exception as e:
        reply = f"Błąd: {e}"
    await update.message.reply_text(reply)

# Uruchomienie bota
if __name__ == "__main__":
    app = ApplicationBuilder().token(telegram_token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("uslugi", uslugi))
    app.add_handler(CommandHandler("kontakt", kontakt))
    app.add_handler(CommandHandler("lokalizacja", lokalizacja))
    app.add_handler(CommandHandler("formularz", formularz))
    app.add_handler(CommandHandler("regulamin", regulamin))
    app.add_handler(CommandHandler("faq", faq))
    app.add_handler(CommandHandler("zobacz", zobacz))
    app.add_handler(CommandHandler("transport", transport))
    app.add_handler(CommandHandler("pobranie", pobranie))
    app.add_handler(CommandHandler("szkolenia", szkolenia))
    app.add_handler(CommandHandler("cennik", cennik))
    app.add_handler(CommandHandler("dyzur", dyzur))
    app.add_handler(CommandHandler("zapomnij", zapomnij))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, klawiatura_rozpoznanie))

    app.run_polling()
