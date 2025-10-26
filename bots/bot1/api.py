import requests
from config import BOT_SERVICE, GOOGLE_POST_URL

class APIService:
    @staticmethod
    async def send_data(data, bot_name):
        data['service'] = BOT_SERVICE
        data['sent_from'] = bot_name

        response = await requests.post(GOOGLE_POST_URL, data)
        return response

