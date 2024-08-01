import os
import discord
from discord.ext import commands
from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Variables d'environnement pour les tokens
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

# Configuration du bot Discord
intents = discord.Intents.default()
intents.messages = True
bot_discord = commands.Bot(command_prefix='!', intents=intents)

# Configuration du bot Telegram
bot_telegram = Bot(token=TELEGRAM_TOKEN)
updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
dispatcher = updater.dispatcher

# Channels IDs
DISCORD_CHANNEL_ID = 123456789012345678  # Remplacez par votre ID de canal Discord
TELEGRAM_CHANNEL_ID = -1001234567890     # Remplacez par votre ID de canal Telegram

# Synchronisation Discord vers Telegram
@bot_discord.event
async def on_message(message):
    if message.channel.id == DISCORD_CHANNEL_ID and not message.author.bot:
        chat_id = TELEGRAM_CHANNEL_ID
        text = f"**{message.author.name}:** {message.content}"
        bot_telegram.send_message(chat_id=chat_id, text=text)
    await bot_discord.process_commands(message)

# Synchronisation Telegram vers Discord
def telegram_message_handler(update: Update, context):
    if update.message.chat_id == TELEGRAM_CHANNEL_ID:
        channel = bot_discord.get_channel(DISCORD_CHANNEL_ID)
        text = f"**{update.message.from_user.username}:** {update.message.text}"
        asyncio.run_coroutine_threadsafe(channel.send(text), bot_discord.loop)

telegram_handler = MessageHandler(Filters.text & ~Filters.command, telegram_message_handler)
dispatcher.add_handler(telegram_handler)

# Démarrage des bots
def main():
    updater.start_polling()
    bot_discord.run(DISCORD_TOKEN)

if __name__ == '__main__':
    main()
