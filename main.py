import os
import asyncio
import discord
from discord.ext import commands
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackContext, filters

# Variables d'environnement pour les tokens
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

if not DISCORD_TOKEN or not TELEGRAM_TOKEN:
    raise ValueError("DISCORD_TOKEN and TELEGRAM_TOKEN must be set.")

# Configuration du bot Discord
intents = discord.Intents.default()
intents.messages = True
bot_discord = commands.Bot(command_prefix='!', intents=intents)

# Configuration du bot Telegram
async def start_telegram_application(application: Application) -> None:
    async def handle_telegram_message(update: Update) -> None:
        if update.message.chat_id == TELEGRAM_CHANNEL_ID:
            channel = bot_discord.get_channel(DISCORD_CHANNEL_ID)
            text = f"**{update.message.from_user.username}:** {update.message.text}"
            await channel.send(text)

    async def start_telegram_command(update: Update, context: CallbackContext) -> None:
        await update.message.reply_text('Hello!')

    async def send_id_list(update: Update, context: CallbackContext) -> None:
        response = f'The bot is present in chat ID: {update.message.chat_id}'
        await update.message.reply_text(response)

    application.add_handler(CommandHandler('start', start_telegram_command))
    application.add_handler(CommandHandler('id', send_id_list))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_telegram_message))
    await application.run_polling()

# Synchronisation Discord vers Telegram
@bot_discord.event
async def on_message(message):
    if message.channel.id == DISCORD_CHANNEL_ID and not message.author.bot:
        text = f"**{message.author.name}:** {message.content}"
        await bot_telegram.bot.send_message(chat_id=TELEGRAM_CHANNEL_ID, text=text)
    await bot_discord.process_commands(message)

async def main() -> None:
    # Démarrage du bot Telegram
    telegram_application = Application.builder().token(TELEGRAM_TOKEN).build()
    telegram_task = asyncio.create_task(start_telegram_application(telegram_application))

    # Démarrage du bot Discord
    discord_task = asyncio.create_task(bot_discord.start(DISCORD_TOKEN))

    # Attente de la fin des tâches
    await asyncio.gather(discord_task, telegram_task)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Program interrupted")
    except Exception as e:
        print(f"An error occurred: {e}")
