import logging
from dotenv import load_dotenv
import os
from google.api_core.exceptions import InvalidArgument
from telegram import Bot
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
import dialogflow_v2 as dialogflow


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
    text_answer = detect_intent_texts(session_id, text_message, 'ru')
    context.bot.send_message(chat_id=update.effective_chat.id, text=text_answer)


def detect_intent_texts(session_id, text_message, language_code):
    global project_id
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    
    text_input = dialogflow.types.TextInput(text=text_message, language_code=language_code)
    query_input = dialogflow.types.QueryInput(text=text_input)
    response = session_client.detect_intent(session=session, query_input=query_input)
    
    return response.query_result.fulfillment_text


if __name__ == '__main__':
    load_dotenv()
    tg_token = os.getenv('TG_TOKEN')
    tg_user_id = os.getenv('TG_USED_ID')
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.getenv('GOOGLE_CLOUD_KEY_JSON')
    project_id = os.getenv('GOOGLE_CLOUD_PROJECT_ID')

    tg_bot = Bot(tg_token)
    
    updater = Updater(tg_token, use_context=True)
    dispatcher = updater.dispatcher

    logger.setLevel(logging.INFO)
    logger.addHandler(TelegramLogsHandler(tg_bot, tg_user_id))
    logger.info('Бот начал работу')
    
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)
    
    try:
        dialogflow_handler = MessageHandler(Filters.text, dialogflow_answer)
        dispatcher.add_handler(dialogflow_handler)
    except InvalidArgument:
        logger.exception('Ошибка в запросе к Dialogflow')
    
    updater.start_polling()
