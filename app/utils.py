import os
import random

import requests

from dotenv import load_dotenv


def send_sms(recipients):
    load_dotenv()
    code = str(random.randint(100000, 999999))
    url = 'https://sms.notisend.ru/api/message/send'
    headers = {
        'Accept': 'application/json',
    }
    data = {
        'project': os.getenv('PROJECT_NAME'),
        'recipients': recipients,
        'message': f'Ваш код подтверждения: {code}',
        'apikey': os.getenv('SMS_API_KEY'),
    }
    response = requests.get(url, headers=headers, params=data)
    return code


