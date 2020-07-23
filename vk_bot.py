import os
import logging
import random

from dotenv import load_dotenv
from telegram import Bot
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import dialogflow_v2 as dialogflow
from google.api_core.exceptions import InvalidArgument

from detect_intent import detect_intent_texts
from tg_bot import TelegramLogsHandler

logger = logging.getLogger('Speach_bot')


def dialogflow_answer(event, vk_api):
    global project_id
    session_id = f'vk-{event.user_id}'
    user_message = event.text
    intent = detect_intent_texts(GOOGLE_CLOUD_PROJECT_ID, session_id, user_message, 'ru')
    if not intent.intent.is_fallback:
        vk_api.messages.send(
            user_id=event.user_id,
            message=intent.fulfillment_text,
            random_id=random.randint(1, 1000)
        )


if __name__ == "__main__":
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.getenv('GOOGLE_CLOUD_KEY_JSON')

    load_dotenv()
    tg_user_id = os.getenv('TG_USED_ID')
    tg_bot = Bot(os.getenv('TG_TOKEN'))
    GOOGLE_CLOUD_PROJECT_ID = os.getenv('GOOGLE_CLOUD_PROJECT_ID')
    
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
