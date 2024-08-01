import logging
import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Lire le token Telegram à partir des variables d'environnement
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

if not TELEGRAM_TOKEN:
    raise ValueError("Aucun token Telegram trouvé. Assurez-vous que TELEGRAM_TOKEN est défini.")

# Configurer le logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Fonction qui sera appelée lorsque le bot reçoit un message
def echo(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    update.message.reply_text(f'This chat ID is {chat_id}')

def main():
    # Créer l'Updater et le Dispatcher
    updater = Updater(TELEGRAM_TOKEN)

    dispatcher = updater.dispatcher

    # Ajouter un gestionnaire de messages pour répondre avec l'ID du chat
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Démarrer le bot
    updater.start_polling()

    # Exécuter le bot jusqu'à ce que vous appuyiez sur Ctrl-C ou que le processus soit terminé
    updater.idle()

if __name__ == '__main__':
    main()
