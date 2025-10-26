import aiohttp
from config import BOT_SERVICE, GOOGLE_POST_URL

class APIService:
    @staticmethod
    async def send_data(data, bot_name):
        data['service'] = BOT_SERVICE
        data['sent_from'] = bot_name

        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=20)) as session:
            try:
                async with session.post(GOOGLE_POST_URL, data=data) as response:
                    response_data = await response.json()
                    if response_data.get('status') == 'success':
                        return 'ok'
                    else:
                        return 'uncorrect data'
                        
            except Exception as e:
                return 'connection error'