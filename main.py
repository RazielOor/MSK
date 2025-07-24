import os
from datetime import datetime
from openai import OpenAI
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, ContextTypes,
    CommandHandler, MessageHandler, filters
)

# Zmienne środowiskowe (Render NIE obsługuje .env)
try:
    openai_api_key = os.environ["OPENAI_API_KEY"]
    telegram_token = os.environ["TELEGRAM_BOT_TOKEN"]
except KeyError as e:
    raise RuntimeError(f"Brakuje zmiennej środowiskowej: {e}")

# Klient OpenAI
client = OpenAI(api_key=openai_api_key)

# Historia rozmów i czas ostatniego kontaktu
user_histories = {}
user_last_seen = {}

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Witaj. Tu MSK Ratownictwo Medyczne. 🩺\n"
        "Jesteśmy podmiotem leczniczym świadczącym usługi premium, poza systemem NFZ.\n"
        "Jak mogę Ci pomóc?\n\n"
        "ℹ️ W nagłych przypadkach – dzwoń 112 lub 999."
    )

# /uslugi
async def uslugi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Nasze usługi obejmują:\n"
        "✅ Transport medyczny\n"
        "✅ Domowe pobrania krwi\n"
        "✅ Cewnikowanie i zmiany opatrunków\n"
        "✅ Zabezpieczenia medyczne imprez\n"
        "✅ Szkolenia z pierwszej pomocy i obsługi sprzętu\n\n"
        "Zadzwoń: 733 847 903\nNapisz: msk.ratownictwo@gmail.com"
    )

# /kontakt
async def kontakt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📞 Telefon: 733 847 903\n"
        "📧 Email: msk.ratownictwo@gmail.com\n"
        "🌐 www.ratownictwo.online"
    )

# /idea
async def idea(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "MSK powstało z potrzeby niesienia pomocy tam, gdzie inni nie mogą lub nie chcą.\n"
        "Działamy poza systemem publicznym, ale zgodnie z najwyższymi standardami medycznymi.\n"
        "Nie dorabiamy się na ludzkim cierpieniu – przywracamy opiece zdrowotnej godność."
    )

# /zapomnij
async def zapomnij(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_histories.pop(str(update.effective_user.id), None)
    await update.message.reply_text("Rozmowa wyczyszczona. Zaczynamy od nowa.")

# Odpowiedzi GPT z pamięcią
async def gpt_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    text = update.message.text
    user_last_seen[user_id] = datetime.now()

    history = user_histories.get(user_id, [])
    history.append({"role": "user", "content": text})

    prompt = (
        "Jesteś przedstawicielem MSK Ratownictwo Medyczne – profesjonalnego podmiotu leczniczego. "
        "Świadczysz usługi premium: transport medyczny, pobrania krwi, zmiany opatrunków, szkolenia. "
        "Działasz poza systemem NFZ, ale z najwyższą jakością i poszanowaniem pacjenta. "
        "Zawsze informuj, że w nagłym zagrożeniu należy dzwonić na 112 lub 999. "
        "Nie jesteś AI – jesteś człowiekiem odpowiadającym na pytania z empatią i profesjonalizmem."
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

# Uruchomienie bota
if __name__ == "__main__":
    app = ApplicationBuilder().token(telegram_token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("uslugi", uslugi))
    app.add_handler(CommandHandler("kontakt", kontakt))
    app.add_handler(CommandHandler("idea", idea))
    app.add_handler(CommandHandler("zapomnij", zapomnij))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, gpt_reply))

    app.run_polling()
