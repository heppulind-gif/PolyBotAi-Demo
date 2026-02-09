# bot.py
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from sandbox import Sandbox

# -----------------------------
# GLOBALS
# -----------------------------
sandbox = Sandbox()

# -----------------------------
# TELEGRAM COMMANDS
# -----------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🚀 PolyPulseBot is online!\n"
        "Commands:\n"
        "/ping - test bot\n"
        "/status - view dashboard\n"
        "/correlations - view correlation map\n"
        "/start_sandbox - start paper trading\n"
        "/stop_sandbox - stop paper trading"
    )

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🏓 Pong!")

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    dashboard = sandbox.analytics.get_dashboard()
    await update.message.reply_text(dashboard)

async def correlations(update: Update, context: ContextTypes.DEFAULT_TYPE):
    corr_map = sandbox.analytics.get_correlation_map()
    await update.message.reply_text(corr_map)

async def start_sandbox(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not sandbox.running:
        # Run sandbox safely in Telegram bot async loop
        context.application.create_task(sandbox.start())
        await update.message.reply_text("🧪 Sandbox started in background!")
    else:
        await update.message.reply_text("⚠️ Sandbox already running.")

async def stop_sandbox(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if sandbox.running:
        await sandbox.stop()
        await update.message.reply_text("🛑 Sandbox stopped!")
    else:
        await update.message.reply_text("⚠️ Sandbox is not running.")

# -----------------------------
# MAIN BOT SETUP
# -----------------------------
def main():
    TOKEN = "8146985739:AAFU0kQ3U0llvEPepQLk4Cy1tM5H1ZzeL9c"

    app = ApplicationBuilder().token(TOKEN).build()

    # Add command handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ping", ping))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("correlations", correlations))
    app.add_handler(CommandHandler("start_sandbox", start_sandbox))
    app.add_handler(CommandHandler("stop_sandbox", stop_sandbox))

    print("[Bot] Starting Telegram bot...")
    # ✅ run_polling handles asyncio internally; no asyncio.run()
    app.run_polling()

# -----------------------------
# ENTRY POINT
# -----------------------------
if __name__ == "__main__":
    main()
