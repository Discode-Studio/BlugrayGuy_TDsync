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

# Channels IDs
DISCORD_CHANNEL_ID = 123456789012345678  # Remplacez par votre ID de canal Discord
TELEGRAM_CHANNEL_ID = -1001234567890     # Remplacez par votre ID de canal Telegram

# Synchronisation Discord vers Telegram
@bot_discord.event
async def on_message(message):
    if message.channel.id == DISCORD_CHANNEL_ID and not message.author.bot:
        text = f"**{message.author.name}:** {message.content}"
        await bot_telegram.send_message(chat_id=TELEGRAM_CHANNEL_ID, text=text)
    await bot_discord.process_commands(message)

# Synchronisation Telegram vers Discord
async def handle_telegram_message(update: Update) -> None:
    if update.message.chat_id == TELEGRAM_CHANNEL_ID:
        channel = bot_discord.get_channel(DISCORD_CHANNEL_ID)
        text = f"**{update.message.from_user.username}:** {update.message.text}"
        await channel.send(text)

async def start_telegram_command(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Hello!')

async def send_id_list(update: Update, context: CallbackContext) -> None:
    chat_ids = [update.message.chat_id]
    response = "The bot is present in the following chat(s):\n" + "\n".join(str(chat_id) for chat_id in chat_ids)
    await update.message.reply_text(response)

async def start_telegram_application() -> None:
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    
    # Ajouter les handlers de commande
    application.add_handler(CommandHandler('start', start_telegram_command))
    application.add_handler(CommandHandler('id', send_id_list))
    
    # Ajouter le handler de message
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_telegram_message))
    
    # Démarrage de l'application Telegram
    await application.run_polling()

async def main() -> None:
    # Démarrage du bot Discord
    discord_task = asyncio.create_task(bot_discord.start(DISCORD_TOKEN))
    
    # Démarrage de l'application Telegram
    telegram_task = asyncio.create_task(start_telegram_application())
    
    try:
        # Attente de la fin des tâches
        await asyncio.gather(discord_task, telegram_task)
    except KeyboardInterrupt:
        print("Program interrupted")
    finally:
        # Annulation des tâches pour un arrêt propre
        discord_task.cancel()
        telegram_task.cancel()
        # Attente de la fin des tâches de fermeture
        await asyncio.gather(discord_task, telegram_task, return_exceptions=True)

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
