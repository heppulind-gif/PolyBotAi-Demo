# bot.py
import os
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from paper_engine import PaperEngine
from trade_manager import TradeManager
from analytics import Analytics
from wallet_tracker import WalletTracker

TOKEN = os.environ.get("8146985739:AAFU0kQ3U0llvEPepQLk4Cy1tM5H1ZzeL9c") # Set this in Railway ENV

# Initialize components
paper_engine = PaperEngine()
analytics = Analytics()
wallet_tracker = WalletTracker()
trade_manager = TradeManager(paper_engine, wallet_tracker, analytics)

# Track mode states
modes = {"paper": True, "real": False}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📊 Dashboard", callback_data="dashboard")],
        [InlineKeyboardButton("🧪 Paper Mode ON/OFF", callback_data="toggle_paper")],
        [InlineKeyboardButton("💵 Real Mode ON/OFF", callback_data="toggle_real")],
        [InlineKeyboardButton("👀 Wallet Tracker", callback_data="wallet")],
        [InlineKeyboardButton("📈 Analytics & Heatmaps", callback_data="analytics")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Welcome to PolyPulse Bot!", reply_markup=reply_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "toggle_paper":
        modes["paper"] = not modes["paper"]
        status = "ON" if modes["paper"] else "OFF"
        await query.edit_message_text(f"Paper Mode is now {status}")
        if modes["paper"]:
            asyncio.create_task(paper_engine.run_paper_loop())
    elif data == "toggle_real":
        modes["real"] = not modes["real"]
        status = "ON" if modes["real"] else "OFF"
        await query.edit_message_text(f"Real Mode is now {status}")
        if modes["real"]:
            asyncio.create_task(trade_manager.run_real_loop())
    elif data == "dashboard":
        msg = analytics.get_dashboard()
        await query.edit_message_text(msg)
    elif data == "wallet":
        msg = wallet_tracker.get_status()
        await query.edit_message_text(msg)
    elif data == "analytics":
        heatmap = analytics.get_correlation_map()
        await query.edit_message_text(heatmap)

async def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    await app.start()
    await app.updater.start_polling()
    await asyncio.Event().wait()  # Keep running

if __name__ == "__main__":
    asyncio.run(main())
