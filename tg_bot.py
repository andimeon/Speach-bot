import logging
import os
from functools import partial
from dotenv import load_dotenv

from google.api_core.exceptions import InvalidArgument
from telegram import Bot
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler

from detect_intent import detect_intent_texts


logger = logging.getLogger('Speach_bot')


class TelegramLogsHandler(logging.Handler):
    
    def __init__(self, bot, user_id):
        super().__init__()
        self.chat_id = user_id
        self.tg_bot = bot
    
    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)
        

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Вы активировали бота")


def dialogflow_answer(update, context):
    text_message = update.message.text
    session_id = update.effective_chat.id
    intent = detect_intent_texts(GOOGLE_CLOUD_PROJECT_ID, session_id, text_message, 'ru')
    text_answer = intent.fulfillment_text
    context.bot.send_message(chat_id=update.effective_chat.id, text=text_answer)


if __name__ == '__main__':
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.getenv('GOOGLE_CLOUD_KEY_JSON')

    load_dotenv()
    tg_token = os.getenv('TG_TOKEN')
    tg_user_id = os.getenv('TG_USED_ID')
    GOOGLE_CLOUD_PROJECT_ID = os.getenv('GOOGLE_CLOUD_PROJECT_ID')

    tg_bot = Bot(tg_token)
    
    dispatcher = Updater(tg_token, use_context=True).dispatcher

    logger.setLevel(logging.INFO)
    logger.addHandler(TelegramLogsHandler(tg_bot, tg_user_id))
    logger.info('Бот начал работу')   

    dispatcher.add_handler(CommandHandler('start', start))
    
    try:
        dispatcher.add_handler(MessageHandler(Filters.text, dialogflow_answer))
    except InvalidArgument:
        logger.exception('Ошибка в запросе к Dialogflow')
    
    updater.start_polling()
