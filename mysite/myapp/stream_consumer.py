try:
    from tasks import evaluate_api_key, predict_diabetes, process_task_result
    from utils.redis_connection import redis_client
except ImportError:
    from myapp.tasks import evaluate_api_key, predict_diabetes, process_task_result
    from myapp.utils.redis_connection import redis_client

from celery import chain
import json

def main():
    print('Starting stream consumer')
    while True:
        # Read from the stream
        messages = redis_client.xread({'diabetes_predictions': '$'}, block=1000, count=1)

        for complete_message in messages:  # type: ignore
            # complete_message is a list where the first element is the stream name (not needed),
            # the second is a list of messages. each message is a tuple where the first element
            # is the message id, the second is the json data
            _, message_list = complete_message
            for concise_message in message_list:
                _, data_bytes = concise_message
                data = process_dict_bytes(data_bytes)
                action = data.get('action')
                api_key = data.get('api_key')
                channel_name = data.get('channel_name')
                isPrediction = action == 'predict_diabetes'

                # Enqueue tasks based on the action
                if isPrediction:
                    numbers = data.get('data')
                    # here, numbers are the literal numbers to predict on
                    # Chain evaluate_api_key -> predict_diabetes -> process_task_result
                    task_chain = chain(
                        evaluate_api_key.s(api_key, True),
                        predict_diabetes.s(numbers),
                        process_task_result.s(channel_name)
                    )
                    task_chain()
                else:
                    # Chain evaluate_api_key -> process_task_result
                    task_chain = chain(
                        evaluate_api_key.s(api_key, False),
                        process_task_result.s(channel_name)
                    )
                    task_chain()       

def process_dict_bytes(dict_bytes):
    dict_str = {}
    for key, value in dict_bytes.items():
        key_str = key.decode('utf-8')
        dict_str[key_str] = value.decode('utf-8')

    return dict_str

if __name__ == '__main__':
    main()
