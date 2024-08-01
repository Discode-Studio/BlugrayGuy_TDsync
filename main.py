import os
import threading
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
bot_telegram = Application.builder().token(TELEGRAM_TOKEN).build()

# Channels IDs
DISCORD_CHANNEL_ID = 123456789012345678  # Remplacez par votre ID de canal Discord
TELEGRAM_CHANNEL_ID = -1001234567890     # Remplacez par votre ID de canal Telegram

# Synchronisation Discord vers Telegram
@bot_discord.event
async def on_message(message):
    if message.channel.id == DISCORD_CHANNEL_ID and not message.author.bot:
        text = f"**{message.author.name}:** {message.content}"
        await bot_telegram.bot.send_message(chat_id=TELEGRAM_CHANNEL_ID, text=text)
    await bot_discord.process_commands(message)

# Synchronisation Telegram vers Discord
async def handle_telegram_message(update: Update) -> None:
    if update.message.chat_id == TELEGRAM_CHANNEL_ID:
        channel = bot_discord.get_channel(DISCORD_CHANNEL_ID)
        text = f"**{update.message.from_user.username}:** {update.message.text}"
        await channel.send(text)

# Commande /start sur Telegram
async def start_telegram_command(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Hello!')

# Commande /id sur Telegram
async def send_id_list(update: Update, context: CallbackContext) -> None:
    response = f'The bot is present in chat ID: {update.message.chat_id}'
    await update.message.reply_text(response)

async def start_telegram_application() -> None:
    bot_telegram.add_handler(CommandHandler('start', start_telegram_command))
    bot_telegram.add_handler(CommandHandler('id', send_id_list))
    bot_telegram.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_telegram_message))
    await bot_telegram.run_polling()

def run_discord_bot():
    bot_discord.run(DISCORD_TOKEN)

def run_telegram_bot():
    asyncio.run(start_telegram_application())

if __name__ == '__main__':
    # Lancer les bots dans des threads séparés pour éviter les conflits de boucle d'événements
    discord_thread = threading.Thread(target=run_discord_bot)
    telegram_thread = threading.Thread(target=run_telegram_bot)
    
    discord_thread.start()
    telegram_thread.start()
    
    discord_thread.join()
    telegram_thread.join()
