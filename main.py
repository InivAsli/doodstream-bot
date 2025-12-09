import logging
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from config import config
from handlers import handlers

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def main():
    print("🚀 Starting DoodStream Bot...")
    
    # Validate credentials
    if not config.TELEGRAM_TOKEN:
        print("❌ ERROR: TELEGRAM_TOKEN not found in environment variables!")
        print("💡 Add it in Render dashboard → Environment Variables")
        return
    
    if not config.DOODSTREAM_API_KEY:
        print("❌ ERROR: DOODSTREAM_API_KEY not found!")
        return
    
    print("✅ Credentials loaded successfully")
    print(f"👤 Admin IDs: {config.ADMIN_IDS}")
    
    # Create application
    application = Application.builder().token(config.TELEGRAM_TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", handlers.start_command))
    application.add_handler(CommandHandler("help", handlers.start_command))
    application.add_handler(CallbackQueryHandler(handlers.handle_callback))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handlers.handle_url_upload))
    
    # Start bot
    print("✅ Bot is running and ready!")
    application.run_polling(allowed_updates=["message", "callback_query"])

if __name__ == "__main__":
    main()
