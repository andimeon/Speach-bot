# Боты, демонстрирующий интеграцию с искусственным интеллектом

Данный бот ведет диалог с пользователем по определенным вопросам. В процессе диалога происходит обучение бота.
Представлены боты для площадок Telegram и VK (Вконтакте). В качестве нейросети использован сервис Dialogflow.

## Переменные и среда окружения

Доступны 6 переменных окружения:

`TG_TOKEN` - токен от бота в телеграмме.

`TG_USED_ID` - ID владельца бота для уведомления о состоянии ботов.

`VK_TOKEN` - токен от бота в VK.

`PROJECT_ID` - ID проекта на платформе Google Cloud.

`GOOGLE_CLOUD_KEY_JSON` - переменная среды платформе Google Cloud `[GOOGLE_APPLICATION_CREDENTIALS]`.

`QUESTION_JSON` - путь к файлу json с тренировочными вопросами и ответами на эти вопросы.

Для начала небходимо указать учетные данные для аутентификации в коде приложения, установив переменную среды `[GOOGLE_APPLICATION_CREDENTIALS]`. Для этого нужно скачать [json file](https://console.cloud.google.com/apis/credentials/serviceaccountkey?_ga=2.17190073.1666737017.1594636150-802301315.1594035578), содержащий `service account key`. Дальше в коде нужно заменить PATH на путь к файлу json и активировать переменную

```bash
export GOOGLE_APPLICATION_CREDENTIALS='PATH'
```

Активировать переменную так же можно установкой программы direnv и автоматической загрузкой переменных. Подробная информация об установке переменной среды находится в разделе [Creating a service account](https://cloud.google.com/docs/authentication/production#creating_a_service_account).

## Локальный запуск на машине

Остальные переменные окружения активируются различными способами.

Либо с помощью библиотеки [python-dotenv](https://pypi.org/project/python-dotenv/). Тогда переменные необходимо поместить в файл `.env`.

Либо использованием программы [direnv](https://github.com/direnv/direnv). Установку и активацию библиотеки необходимо провести согласно инструкции для своей оболочки.В файл `.envrc` который должен находится в папке проекта нужно поместить переменные окружения.
После этого, при входе в папку и запуске скриптов ботов переменные будут подгружаться автоматически (необходимо только
исправить определение переменных в скрипте, согласно инструкциям в библиотеке).

Либо из командной строки

```bash
export VARIABLE=VALUE
```

***

### Перед дальнейшими шагами рекомендуется активировать виртуальное окружение venv

Скрипт адоптирован под Python ver 3.8.0

Используйте `pip` для установки зависимостей:

```bash
pip install -r requirements.txt
```

Запуск проекта осуществляется из командной строки:

```bash
python tg_bot.py
python vk_bot.py
```

## Как задеплоить проект на сервис [heroku](https://dashboard.heroku.com/apps)

Необходимо создать новое приложение на сервисе и подключить Github с репозиторием, где находится бот. Нужно создать [Procfile](https://devcenter.heroku.com/articles/procfile). Переменные окружения поместить в [settings](https://dashboard.heroku.com/apps/devman-telegram-bot/settings) `Config var`. Активация окружения Google Cloud производится созданием [bildpack](https://github.com/gerywahyunugraha/heroku-google-application-credentials-buildpack).
После деплоя проекта необходимо активировать скрипты в разделе [Resources](https://dashboard.heroku.com/apps/speach-bot/resources).

## Пример работы скрипта

Telegram

![screenshot](screenshots/tg_bot.gif)

Vk (Вконтакте)

![screenshot](screenshots/vk_bot.gif)

## Тренер фраз для искусственного интеллекта

Для того, чтобы загрузить на платформу [Dialogflow](https://dialogflow.cloud.google.com) тренировочные вопросы и ответы можно воспользоваться скриптом `create_intent.py`

```python
python create_intent.py
```

Список вопросов и ответов должен быть оформлен в json файле (например questions.json) в следующем формате:

```json
{
    Intent: {
        "question": [
            "here is question",
            "here is question",
            "here is question",
        ],
        "answer": "here is answer"
    },
}
```

## Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).
