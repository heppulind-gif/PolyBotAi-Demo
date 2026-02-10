# bot.py
import os
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from paper_engine import PaperEngine
from trade_manager import TradeManager
from ml_engine import MLModel
from crypto_data import CryptoData
from portfolio_manager import PortfolioManager
from analytics import Analytics
from wallet_tracker import WalletTracker

# Environment variables
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TRADING_MODE = os.environ.get("TRADING_MODE", "PAPER")
ADMIN_CHAT_ID = os.environ.get("ADMIN_CHAT_ID")

if not TOKEN:
    raise ValueError("❌ TELEGRAM_BOT_TOKEN not set!")

# Modules
crypto_data = CryptoData()
ml_model = MLModel()
portfolio = PortfolioManager()
analytics_module = Analytics()
wallet_tracker = WalletTracker()
paper_engine = PaperEngine(crypto_data, ml_model, portfolio, analytics_module)
trade_manager = TradeManager(crypto_data, ml_model, portfolio, analytics_module, wallet_tracker)

# Commands
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📊 Dashboard", callback_data="dashboard"),
         InlineKeyboardButton("🧪 Paper Mode", callback_data="paper_mode")],
        [InlineKeyboardButton("💰 Real Mode", callback_data="real_mode"),
         InlineKeyboardButton("⚙️ Settings", callback_data="settings")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "🚀 Welcome to PolyPulse Bot!\nChoose an option below to get started.",
        reply_markup=reply_markup
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "dashboard":
        dash = analytics_module.get_dashboard()
        corr = analytics_module.get_correlation_map()
        await query.edit_message_text(f"{dash}\n\n{corr}")
    elif query.data == "paper_mode":
        await query.edit_message_text("🧪 Paper Mode active. Learning in background...")
        asyncio.create_task(paper_engine.run_simulations())
    elif query.data == "real_mode":
        if TRADING_MODE.upper() != "REAL":
            await query.edit_message_text("⚠️ Real Mode disabled. Set TRADING_MODE=REAL to enable.")
        else:
            await query.edit_message_text("💰 Real Mode activated. Trading with real wallet...")
            asyncio.create_task(trade_manager.run_real_trading())
    elif query.data == "settings":
        mode = TRADING_MODE.upper()
        await query.edit_message_text(f"⚙️ Settings\nTrading Mode: {mode}\nWallet Connected: {wallet_tracker.enabled}")

# Main entry
def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    print("✅ PolyPulse Bot starting...")
    app.run_polling()  # ✅ This handles initialize/start/idle internally

if __name__ == "__main__":
    main()
    
