import os, json
import dialogflow_v2 as dialogflow
from dotenv import load_dotenv


def create_intent(project_id, display_name, training_phrases_parts, message_texts):
    intents_client = dialogflow.IntentsClient()
    parent = intents_client.project_agent_path(project_id)
    
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.types.Intent.TrainingPhrase.Part(
            text=training_phrases_part)
        
        training_phrase = dialogflow.types.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)
    
    text = dialogflow.types.Intent.Message.Text(text=message_texts)
    message = dialogflow.types.Intent.Message(text=text)
    
    intent = dialogflow.types.Intent(
        display_name=display_name,
        training_phrases=training_phrases,
        messages=[message])
    
    response = intents_client.create_intent(parent, intent)
    print('Intent created: {}'.format(response))


def train_intents(project_id):
    train_client = dialogflow.AgentsClient()
    parent = train_client.project_path(project_id)
    response = train_client.train_agent(parent)

    print('Train made: {}'.format(response))


def main():
    load_dotenv()
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.getenv('GOOGLE_CLOUD_KEY_JSON')
    project_id = os.getenv('PROJECT_ID')
    
    with open(os.getenv('QUESTION_JSON'), 'r', encoding='utf-8') as file:
        intents = json.load(file)
    
    for intent in intents:
        display_name = intent
        training_phrases_parts = intents[intent]['questions']
        message_texts = [intents[intent]['answer']]
        create_intent(project_id, display_name, training_phrases_parts, message_texts)
    
    train_intents(project_id)


if __name__ == '__main__':
    main()
