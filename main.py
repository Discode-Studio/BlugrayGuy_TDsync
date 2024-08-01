import os
import asyncio
import discord
from discord.ext import commands
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

# Variables d'environnement pour les tokens
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

# Configuration du bot Discord
intents = discord.Intents.default()
intents.messages = True
bot_discord = commands.Bot(command_prefix='!', intents=intents)

# Configuration du bot Telegram
async def start_telegram_application() -> None:
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    async def telegram_message_handler(update: Update) -> None:
        if update.message.chat_id == TELEGRAM_CHANNEL_ID:
            channel = bot_discord.get_channel(DISCORD_CHANNEL_ID)
            text = f"**{update.message.from_user.username}:** {update.message.text}"
            await channel.send(text)

    telegram_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, telegram_message_handler)
    application.add_handler(telegram_handler)
    
    await application.run_polling()

# Channels IDs
DISCORD_CHANNEL_ID = 123456789012345678  # Remplacez par votre ID de canal Discord
TELEGRAM_CHANNEL_ID = -1001234567890     # Remplacez par votre ID de canal Telegram

# Synchronisation Discord vers Telegram
@bot_discord.event
async def on_message(message):
    if message.channel.id == DISCORD_CHANNEL_ID and not message.author.bot:
        chat_id = TELEGRAM_CHANNEL_ID
        text = f"**{message.author.name}:** {message.content}"
        await bot_telegram.send_message(chat_id=chat_id, text=text)
    await bot_discord.process_commands(message)

# Démarrage des bots
async def main():
    # Démarrage du bot Telegram
    telegram_task = asyncio.create_task(start_telegram_application())
    
    # Démarrage du bot Discord
    await bot_discord.start(DISCORD_TOKEN)

if __name__ == '__main__':
    asyncio.run(main())
