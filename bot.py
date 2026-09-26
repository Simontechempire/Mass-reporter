import os
from flask import Flask, render_template, jsonify
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OWNER_ID = int(os.getenv("OWNER_TELEGRAM_ID", "0"))
BOT_NAME = os.getenv("BOT_NAME", "Report real ban")

app = Flask(__name__)


@app.route("/")
def dashboard():
    return render_template("index.html", bot_name=BOT_NAME)


@app.route("/api/status")
def status():
    return jsonify({
        "bot": BOT_NAME,
        "mode": "real ban method",
        "status": "online"
    })


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        await update.message.reply_text("⛔ Access denied.")
        return

    await update.message.reply_text(
        f"🤖 {BOT_NAME}\n\n"
        "🧪 real exploits mode: ON\n"
        "📊 Use the dashboard to control the real exploits."
    )


def main():
    telegram = Application.builder().token(TOKEN).build()
    telegram.add_handler(CommandHandler("start", start))

    print(f"🚀 {BOT_NAME} started")

    # Telegram polling runs separately from the web dashboard.
    telegram.run_polling()


if __name__ == "__main__":
    main()
