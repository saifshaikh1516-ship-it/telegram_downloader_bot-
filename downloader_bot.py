from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import yt_dlp
import os

# Replace with your Bot Token
BOT_TOKEN = "8293070790:AAFgzHB8zVIJW-GpPed1z59ZbWuBqW4nRA0"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Send me any video or image link (YouTube, Instagram, etc.) and I’ll download it for you!")

async def download_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    await update.message.reply_text("⏳ Downloading... Please wait...")

    try:
        ydl_opts = {
            'outtmpl': 'downloads/%(title)s.%(ext)s',
            'format': 'best',
            'quiet': True
        }

        os.makedirs("downloads", exist_ok=True)
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info)

        # Send file if small enough
        if os.path.getsize(file_path) < 50 * 1024 * 1024:
            with open(file_path, "rb") as f:
                await update.message.reply_video(f)
        else:
            await update.message.reply_text("⚠️ File too large for Telegram (50MB limit).")

        os.remove(file_path)

    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_link))
    print("🤖 Bot is running...")
    app.run_polling()

if __name__ == '__main__':
    main()