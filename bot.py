from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from yt_dlp import YoutubeDL

TOKEN = "8219811869:AAEgcJeDwKOxlfTWq1bTaRhpS9VEkOL26AI"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Salom!\n\nVideo nomini yuboring, men YouTube'dan qidiraman."
    )

async def search_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text

    ydl_opts = {
        "quiet": True,
        "default_search": "ytsearch5",
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(query, download=False)

        if "entries" in info:
            text = "Topilgan videolar:\n\n"

            for video in info["entries"]:
                title = video["title"]
                url = video["webpage_url"]
                duration = video.get("duration", 0)

                minutes = duration // 60
                seconds = duration % 60

                text += f"🎬 {title}\n⏱ {minutes}:{seconds:02d}\n🔗 {url}\n\n"

            await update.message.reply_text(text)
        else:
            await update.message.reply_text("Video topilmadi.")

    except Exception as e:
        await update.message.reply_text(f"Xatolik: {e}")

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search_video))

print("Bot ishga tushdi...")
app.run_polling()