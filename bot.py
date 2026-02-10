# bot.py
import os
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler, ContextTypes
)
from paper_engine import PaperEngine
from trade_manager import TradeManager
from ml_engine import MLModel
from crypto_data import CryptoData
from portfolio_manager import PortfolioManager
from analytics import Analytics
from wallet_tracker import WalletTracker

# ---------- ENV VARIABLES ----------
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TRADING_MODE = os.environ.get("TRADING_MODE", "PAPER")  # PAPER or REAL
ADMIN_CHAT_ID = os.environ.get("ADMIN_CHAT_ID")  # optional for alerts

# ---------- INITIALIZE MODULES ----------
crypto_data = CryptoData()
ml_model = MLModel()
portfolio = PortfolioManager()
analytics_module = Analytics()
wallet_tracker = WalletTracker()

# Paper engine handles background learning
paper_engine = PaperEngine(
    crypto_data=crypto_data,
    ml_model=ml_model,
    portfolio=portfolio,
    analytics=analytics_module
)

# Trade manager handles real trades
trade_manager = TradeManager(
    crypto_data=crypto_data,
    ml_model=ml_model,
    portfolio=portfolio,
    analytics=analytics_module,
    wallet_tracker=wallet_tracker
)


# ---------- COMMANDS ----------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Welcome message with buttons"""
    keyboard = [
        [
            InlineKeyboardButton("📊 Dashboard", callback_data="dashboard"),
            InlineKeyboardButton("🧪 Paper Mode", callback_data="paper_mode"),
        ],
        [
            InlineKeyboardButton("💰 Real Mode", callback_data="real_mode"),
            InlineKeyboardButton("⚙️ Settings", callback_data="settings"),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "🚀 Welcome to PolyPulse Bot!\n\n"
        "Choose an option below to get started.",
        reply_markup=reply_markup
    )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button presses"""
    query = update.callback_query
    await query.answer()

    if query.data == "dashboard":
        dash = analytics_module.get_dashboard()
        corr = analytics_module.get_correlation_map()
        await query.edit_message_text(f"{dash}\n\n{corr}")

    elif query.data == "paper_mode":
        await query.edit_message_text("🧪 Paper Mode is active. Learning in background...")
        asyncio.create_task(paper_engine.run_simulations())

    elif query.data == "real_mode":
        if TRADING_MODE.upper() != "REAL":
            await query.edit_message_text(
                "⚠️ Real Mode disabled. Set TRADING_MODE=REAL to enable."
            )
        else:
            await query.edit_message_text("💰 Real Mode activated. Bot will trade with real wallet.")
            asyncio.create_task(trade_manager.run_real_trading())

    elif query.data == "settings":
        mode = TRADING_MODE.upper()
        await query.edit_message_text(f"⚙️ Settings\n\nTrading Mode: {mode}\nWallet Connected: {wallet_tracker.enabled}")


# ---------- BOT MAIN LOOP ----------
async def main():
    app = Application.builder().token(TOKEN).build()

    # Add command and button handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    # Initialize & start bot safely
    await app.initialize()
    await app.start()
    print("✅ PolyPulse Bot is running...")
    
    # Keep bot alive indefinitely
    await asyncio.Future()  # infinite wait


# ---------- ENTRY POINT ----------
if __name__ == "__main__":
    asyncio.run(main())
