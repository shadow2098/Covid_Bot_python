import random
import asyncio
import aiohttp
import json

import get_data
import bot_exceptions

TELEGRAM_TOKEN = get_data.get_variable("TELEGRAM_TOKEN")
TELEGRAM_URL = "https://api.telegram.org/bot{0}/".format(TELEGRAM_TOKEN)

class TelegramManager:

    def bind_bot_manager(self, bot_manager):
        self.__bot_manager = bot_manager

    @staticmethod
    @bot_exceptions.check_function
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

    async def responses(self, text_message, chat_id):

        words = text_message.split()
        user_to_be_blocked_id = words[-1]

        if text_message == "hi" or text_message == "hello":
            list1 = ["Hello",
                        "Hi",
                        "hello",
                        "hi",
                    ]
            return list1[random.randint(0, 3)]

        elif text_message == "how are you?":
            list1 = ["I'm fine",
                        "Not bad",
                        "Great",
                        "It is not my day",
                    ]
            return list1[random.randint(0, 3)]

        elif text_message == "goodbye" or text_message == "bye":
            list1 = ["We had a nice talk.Good luck",
                        "Goodbye",
                        "Bye",
                        "See you later",
                    ]
            return list1[random.randint(0, 3)]

        elif text_message == "get amount of users":
            x = await self.__bot_manager.get_amount_of_users(chat_id)
            if x is not None:
                return "Amount of users: " + str(x)
            return "Not enought rights"

        elif text_message == "get users chat id":
            x = await self.__bot_manager.get_users_chat_id(chat_id)
            if x is not None:
                return "Users chat id: " + str(x)
            return "Not enought rights"

        elif text_message == "block user {:s}".format(user_to_be_blocked_id):
            x = await self.__bot_manager.block_user(chat_id, user_to_be_blocked_id)
            return x

        elif text_message == "block user":
            x = await self.__bot_manager.create_block_action(chat_id)
            return x

        elif text_message == "send global message":
            x = await self.__bot_manager.create_global_message_action(chat_id)
            return x

        elif text_message == "/get_information_about_country":
            x = await self.__bot_manager.create_country_action(chat_id)
            return x

        else:
            x = await self.__bot_manager.check_action(chat_id, text_message)
            return x
