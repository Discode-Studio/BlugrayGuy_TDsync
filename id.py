import os
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Hello!')

async def main() -> None:
    token = os.getenv('TELEGRAM_TOKEN')
    application = Application.builder().token(token).build()
    application.add_handler(CommandHandler('start', start))
    await application.run_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
