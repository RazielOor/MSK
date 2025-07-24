import os
import random
from datetime import datetime
from pathlib import Path
from telegram import (
    Update,
    ReplyKeyboardMarkup,
    KeyboardButton
)
from telegram.ext import (
    ApplicationBuilder, ContextTypes,
    CommandHandler, MessageHandler, filters
)
from openai import OpenAI

# 🔐 Zmienne środowiskowe (Render NIE obsługuje .env)
try:
    openai_api_key = os.environ["OPENAI_API_KEY"]
    telegram_token = os.environ["TELEGRAM_BOT_TOKEN"]
except KeyError as e:
    raise RuntimeError(f"Brakuje zmiennej środowiskowej: {e}")

# 🔗 OpenAI
client = OpenAI(api_key=openai_api_key)
user_histories = {}
user_last_seen = {}

# 🚀 /start z klawiaturą
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
        "ℹ️ W nagłych przypadkach dzwoń: 112 lub 999.",
        reply_markup=reply_markup
    )

# 📋 Komendy tematyczne
async def uslugi(update, context): await update.message.reply_text(
    "Nasze usługi obejmują:\n"
    "✅ Transport medyczny\n"
    "✅ Domowe pobrania krwi\n"
    "✅ Cewnikowanie i zmiany opatrunków\n"
    "✅ Zabezpieczenia medyczne imprez\n"
    "✅ Szkolenia z pierwszej pomocy i obsługi sprzętu\n"
    "📞 733 847 903"
)

async def kontakt(update, context): await update.message.reply_text(
    "📞 733 847 903\n📧 msk.ratownictwo@gmail.com\n🌐 www.ratownictwo.online"
)

async def idea(update, context): await update.message.reply_text(
    "Działamy tam, gdzie inni nie mogą.\n"
    "Poza systemem, ale z poszanowaniem pacjenta i standardami medycznymi.\n"
    "Nie dorabiamy się na cierpieniu – działamy z misją i jakością."
)

async def faq(update, context): await update.message.reply_text(
    "❓ Najczęstsze pytania:\n\n"
    "🔹 Czy działacie w nocy/weekendy?\nTak, zadzwoń: 733 847 903\n"
    "🔹 Czy to refundowane przez NFZ?\nNie, usługi są odpłatne.\n"
    "🔹 Czy transportujecie osoby leżące?\nTak, z noszami i opieką.\n"
    "🔹 Czy można zamówić pobranie krwi w domu?\nTak, z dostawą wyników.\n"
    "🔹 Czy wystawiacie faktury?\nTak, VAT i dokumentację medyczną."
)

async def zobacz(update, context):
    folder = Path("pictures_msk")
    if not folder.exists():
        await update.message.reply_text("Brak katalogu 'pictures_msk'.")
        return
    images = list(folder.glob("*.*"))
    if not images:
        await update.message.reply_text("Brak zdjęć do wyświetlenia.")
        return
    captions = [
        "Ambulans MSK – gotowy do działania.",
        "Jakość i wyposażenie to podstawa.",
        "Nasza codzienność – Twoje bezpieczeństwo.",
        "Rzetelność i nowoczesność w jednym.",
        "Działamy skutecznie i z godnością."
    ]
    selected = random.choice(images)
    caption = random.choice(captions)
    with open(selected, "rb") as photo:
        await update.message.reply_photo(photo=photo, caption=caption)

async def lokalizacja(update, context):
    await update.message.reply_location(latitude=51.131503, longitude=20.793458)

async def formularz(update, context):
    await update.message.reply_text(
        "📄 Formularz zgłoszeniowy:\n👉 https://ratownictwo.online/formularz\n"
        "Lub zadzwoń: 733 847 903"
    )

# 🔎 Usługi szczegółowe
async def transport(update, context): await update.message.reply_text(
    "🚑 Transport medyczny:\n▪️ Nosze, schodołaz, opieka medyczna\n"
    "▪️ Cała Polska, również trasy planowane\n📞 733 847 903"
)

async def pobranie(update, context): await update.message.reply_text(
    "💉 Pobranie krwi w domu pacjenta:\n▪️ Bez kolejek i stresu\n"
    "▪️ Z dostawą wyników\n📞 733 847 903"
)

async def szkolenia(update, context): await update.message.reply_text(
    "🧯 Szkolenia:\n▪️ Pierwsza pomoc BLS, AED\n▪️ Kursy KPP\n▪️ Firmy i szkoły\n📞 733 847 903"
)

async def regulamin(update, context): await update.message.reply_text(
    "📘 Regulamin usług MSK:\n👉 https://ratownictwo.online/regulamin"
)

async def cennik(update, context): await update.message.reply_text(
    "💰 Cennik (orientacyjny):\n"
    "▪️ Pobranie krwi – od 50 zł\n▪️ Transport – od 180 zł\n"
    "▪️ Opieka pielęgniarska – od 120 zł\n▪️ Szkolenia – od 100 zł/os.\n"
    "📞 733 847 903"
)

async def dyzur(update, context): await update.message.reply_text(
    "🕐 Dyżurujemy 7 dni w tygodniu, także w święta.\nW nagłych sprawach – dzwoń: 733 847 903"
)

async def zapomnij(update, context):
    user_histories.pop(str(update.effective_user.id), None)
    await update.message.reply_text("Twoja historia została wyczyszczona.")

# 🧠 Obsługa klawiatury ekranowej
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
        await update.message.reply_text("📞 Kliknij, aby zadzwonić: tel:+48733847903")
    elif "pokaż lokalizację" in text:
        await lokalizacja(update, context)
    else:
        await gpt_reply(update, context)

# 💬 GPT z pamięcią
async def gpt_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    text = update.message.text
    user_last_seen[user_id] = datetime.now()
    history = user_histories.get(user_id, [])
    history.append({"role": "user", "content": text})
    prompt = (
        "Jesteś przedstawicielem MSK Ratownictwo Medyczne – podmiotu leczniczego. "
        "Świadczysz profesjonalne usługi medyczne poza systemem NFZ. "
        "Odpowiadasz z empatią, konkretnie i rzeczowo, bez technicznego języka. "
        "Nie jesteś AI, nie mów o sobie jako sztucznej inteligencji. "
        "W przypadku zagrożenia życia przypominasz o numerach alarmowych 112/999."
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
        reply = f"Wystąpił błąd: {e}"
    await update.message.reply_text(reply)

# ▶️ Uruchomienie
if __name__ == "__main__":
    app = ApplicationBuilder().token(telegram_token).build()

    # Komendy
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("uslugi", uslugi))
    app.add_handler(CommandHandler("kontakt", kontakt))
    app.add_handler(CommandHandler("idea", idea))
    app.add_handler(CommandHandler("faq", faq))
    app.add_handler(CommandHandler("zobacz", zobacz))
    app.add_handler(CommandHandler("lokalizacja", lokalizacja))
    app.add_handler(CommandHandler("formularz", formularz))
    app.add_handler(CommandHandler("transport", transport))
    app.add_handler(CommandHandler("pobranie", pobranie))
    app.add_handler(CommandHandler("szkolenia", szkolenia))
    app.add_handler(CommandHandler("regulamin", regulamin))
    app.add_handler(CommandHandler("cennik", cennik))
    app.add_handler(CommandHandler("dyzur", dyzur))
    app.add_handler(CommandHandler("zapomnij", zapomnij))

    # Przyciski i GPT
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, klawiatura_rozpoznanie))

    app.run_polling()
