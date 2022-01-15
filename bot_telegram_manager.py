import random
import asyncio
import aiohttp
import json

import bot_manager_class
bot_manager = bot_manager_class.BotManager(None, None, None)

TELEGRAM_TOKEN = "5069072255:AAHWjosTYGmR56MQ6Sm16uOFuYEu9L3XrXw"
TELEGRAM_URL = "https://api.telegram.org/bot{0}/".format(TELEGRAM_TOKEN)
DATABASE = "main_bot_database.db"

class TelegramManager:
    
    @staticmethod
    async def send_message(chat_id, msg):
        target = TELEGRAM_URL + "sendMessage"

        data = {
            "chat_id": chat_id,
            "text": msg,
        }

        session = aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False))
        response = await session.post(target, data=data)
        print(await response.text(), response.status)
        await session.close()
        
    @staticmethod
    async def responses(text_message, chat_id):
    
        words = text_message.split()
        user_to_be_blocked_id = words[-1]
    
        if text_message == "Hi" or text_message == "Hello" or text_message == "hi" or text_message == "hello":
            list1 = ["Hello",
                        "Hi",
                        "hello",
                        "hi",
                    ]
            return list1[random.randint(0, 3)]
        
        elif text_message == "How are you?" or text_message == "How are you doing?":
            list1 = ["I'm fine",
                        "Not bad",
                        "Great",
                        "It is not my day",
                    ]
            return list1[random.randint(0, 3)]
        
        elif text_message == "Goodbye" or text_message == "Bye":
            list1 = ["We had a nice talk.Good luck",
                        "Goodbye",
                        "Bye",
                        "See you later",
                    ]
            return list1[random.randint(0, 3)]

        elif text_message == "Get amount of users":
            x = await bot_manager.get_amount_of_users(chat_id)

            if x is not None:
                return "Amount of users: " + str(x)
            return "Not enought rights"
        
        elif text_message == "Get users chat id":
            x = await bot_manager.get_users_chat_id(chat_id)

            if x is not None:
                return "Users chat id: " + str(x)
            return "Not enought rights"
        
        elif text_message == "Block user {:s}".format(user_to_be_blocked_id):
            x = await bot_manager.block_user(chat_id, user_to_be_blocked_id)
            return x
            
        elif text_message == "Block user":
            x = await bot_manager.create_block_action(chat_id)
            return x

        elif text_message == "Send global message":
            x = await bot_manager.create_global_message_action(chat_id)
            return x

        elif text_message == "/get_information_about_country":

            x = await bot_manager.create_country_action(chat_id)
            return x
        
        else:
            x = await bot_manager.check_action(chat_id, text_message)
            return x

