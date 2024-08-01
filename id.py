import os
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Hello!')

async def main() -> None:
    token = os.getenv('TELEGRAM_TOKEN')
    if not token:
        raise ValueError("TELEGRAM_TOKEN must be set.")
    application = Application.builder().token(token).build()
    application.add_handler(CommandHandler('start', start))

    try:
        await application.run_polling()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        try:
            await application.shutdown()
        except Exception as e:
            print(f"An error occurred during shutdown: {e}")

if __name__ == '__main__':
    asyncio.run(main())
