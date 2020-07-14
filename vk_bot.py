import logging
from telegram import Bot
from tg_bot import TelegramLogsHandler
import os
import random
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from dotenv import load_dotenv
import dialogflow_v2 as dialogflow
from google.api_core.exceptions import InvalidArgument

logger = logging.getLogger('Speach_bot')


def dialogflow_answer(event, vk_api):
    user_id = event.user_id
    user_message = event.text
    text_answer = detect_intent_texts(user_id, user_message, 'ru')
    if text_answer is not None:
        vk_api.messages.send(
            user_id=event.user_id,
            message=text_answer,
            random_id=random.randint(1, 1000)
        )


def detect_intent_texts(session_id, text_message, language_code):
    global project_id
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    
    text_input = dialogflow.types.TextInput(text=text_message, language_code=language_code)
    query_input = dialogflow.types.QueryInput(text=text_input)
    
    response = session_client.detect_intent(session=session, query_input=query_input)
    if response.query_result.intent.is_fallback:
        return None
    
    return response.query_result.fulfillment_text


if __name__ == "__main__":
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.getenv('GOOGLE_CLOUD_KEY_JSON')
    load_dotenv()
    tg_user_id = os.getenv('TG_USED_ID')
    tg_bot = Bot(os.getenv('TG_TOKEN'))
    project_id = os.getenv('GOOGLE_CLOUD_PROJECT_ID')
    
    vk_token = os.getenv('VK_TOKEN')
    vk_session = vk_api.VkApi(token=vk_token)

    logger.setLevel(logging.INFO)
    logger.addHandler(TelegramLogsHandler(tg_bot, tg_user_id))
    
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            try:
                dialogflow_answer(event, vk_api)
            except InvalidArgument:
                logger.exception('Ошибка в запросе к Dialogflow')
