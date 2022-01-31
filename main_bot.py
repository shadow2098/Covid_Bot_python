import random
import asyncio
import aiohttp
import json
import aiosqlite
import time
import datetime
from quart import Quart
from quart import request

TELEGRAM_TOKEN = "5069072255:AAHWjosTYGmR56MQ6Sm16uOFuYEu9L3XrXw"
TELEGRAM_URL = "https://api.telegram.org/bot{0}/".format(TELEGRAM_TOKEN)
DATABASE = "main_bot_database.db"
app = Quart(__name__)

class BotAdmins:
    @staticmethod
    async def user_is_admin(chat_id):
        conn = await aiosqlite.connect(DATABASE)
        data = (chat_id, 1)
        cur = await conn.execute("SELECT * FROM users WHERE chat_id=? AND admin=?", data)
        user_data = await cur.fetchall()
        await cur.close()
        await conn.close()

        return len(user_data) != 0

class BotManager:
    def __init__(self, admins_manager, telegram_manager, data_manager):
        self.__admins_manager = admins_manager
        self.__telegram_manager = telegram_manager
        self.__data_manager = data_manager

    async def check_user(self, chat_id):

        conn = await aiosqlite.connect(DATABASE)
        data = (chat_id, )
        cur = await conn.execute("SELECT * FROM users WHERE chat_id=?", data)
        user_data = await cur.fetchall()

        if len(user_data) != 0:
            await cur.close()
            await conn.close()
            return

        data = (chat_id, 1, 0, 0)
        cur = await conn.execute("INSERT INTO users (chat_id, customer, admin, blocked) VALUES(?, ?, ?, ?)", data)
        await conn.commit()
        await cur.close()
        await conn.close()

    async def get_bot_customers(self):
        list1 = []
        conn = await aiosqlite.connect(DATABASE)
        data = (1, )
        cur = await conn.execute("SELECT * FROM users WHERE customer=?", data)
        user_data = await cur.fetchall()
        await cur.close()
        await conn.close()

        for i in range(len(user_data)):
            list1.append(user_data[i][0])
        return list1

    async def get_bot_stuff(self):
        list1 = []
        conn = await aiosqlite.connect(DATABASE)
        data = (1, )
        cur = await conn.execute("SELECT * FROM users WHERE admin=?", data)
        user_data = await cur.fetchall()
        await cur.close()
        await conn.close()

        for i in range(len(user_data)):
            list1.append(user_data[i][0])
        return list1

    async def count_bot_customers(self):
        return len(await self.get_bot_customers())

    async def get_amount_of_users(self, chat_id):
        if await BotAdmins.user_is_admin(chat_id):
            return await self.count_bot_customers()
        return None

    async def get_users_chat_id(self, chat_id):
        if await BotAdmins.user_is_admin(chat_id):
            return await self.get_bot_customers()
        return None

    async def block_user(self, chat_id, user_to_be_blocked_id):

        conn = await aiosqlite.connect(DATABASE)
        data = (user_to_be_blocked_id, )
        cur = await conn.execute("SELECT * FROM users WHERE chat_id=?", data)
        user_to_be_blocked_data = await cur.fetchall()

        if len(user_to_be_blocked_data) == 0:
            await cur.close()
            await conn.close()
            return "Incorrect chat id"

        if not await BotAdmins.user_is_admin(chat_id):
            await cur.close()
            await conn.close()
            return "Not enought rights"

        elif await BotAdmins.user_is_admin(user_to_be_blocked_id):
            await cur.close()
            await conn.close()
            return "Admin can't block admin"

        data = (msg, 1)
        cur = await conn.execute("SELECT * FROM actions WHERE chat_id=? AND customer=?", data)
        user_data1 = await cur.fetchall()
        cur = await conn.execute("SELECT * FROM actions WHERE chat_id=? AND blocked=?", data)
        user_data2 = await cur.fetchall()

        if len(user_data1) != 0:

            conn = await aiosqlite.connect(DATABASE)
            data = (1, 0, user_to_be_blocked_id)
            cur = await conn.execute("UPDATE users SET bloked=?, customer=? WHERE chat_id=?", data)
            cur = await conn.execute("DELETE FROM actions WHERE chat_id=?", data)
            await conn.commit()
            await cur.close()
            await conn.close()

            return "User has been blocked sucsessfully"

        elif len(user_data2) != 0:
            return "User is already blocked"

        return "Incorrect chat_id"

    async def create_action(self, chat_id, action_name):

        conn = await aiosqlite.connect(DATABASE)
        data = (chat_id, action_name)
        cur = await conn.execute("INSERT INTO actions(chat_id, action_name) VALUES(?, ?)", data)
        await conn.commit()
        await cur.close()
        await conn.close()

    async def create_block_action(self, chat_id):
        if not await BotAdmins.user_is_admin(chat_id):
            return "Not enought rights"

        await self.create_action(chat_id, "block_user")
        return "Please send chat id"

    async def create_country_action(self, chat_id):

        conn = await aiosqlite.connect(DATABASE)
        data = (chat_id , "country_information")
        cur = await conn.execute("SELECT * FROM actions WHERE chat_id=? AND action_name=?", data)
        user_data = await cur.fetchall()
        if len(user_data) != 0:
            return "Please, send country name"

        await self.create_action(chat_id, "country_information")
        return "Please, send country name"

    async def create_global_message_action(self, chat_id):

        conn = await aiosqlite.connect(DATABASE)
        data = (chat_id, 1)
        cur = await conn.execute("SELECT * FROM users WHERE chat_id=? AND admin=?", data)
        user_data = await cur.fetchall()
        await cur.close()
        await conn.close()

        if len(user_data) != 0:
                return "Not enought rights"

        await self.create_action(chat_id, "global_message")
        return "Please send message that you want to send"

    async def check_action(self, chat_id, msg):

        conn = await aiosqlite.connect(DATABASE)
        data = (chat_id, )
        cur = await conn.execute("SELECT * FROM actions WHERE chat_id=?", data)
        user_data = await cur.fetchall()

        if len(user_data) == 0:
            await cur.close()
            await conn.close()
            return "False message"

        action_name = user_data[0][1]

        if action_name == "block_user":

            if await BotAdmins.user_is_admin(msg):
                data = (chat_id, )
                cur = await conn.execute("DELETE FROM actions WHERE chat_id=?", data)
                await conn.commit()
                await cur.close()
                await conn.close()
                return "Admin can't block admin"

            data = (msg, 1)
            cur = await conn.execute("SELECT * FROM users WHERE chat_id=? AND customer=?", data)
            user_data1 = await cur.fetchall()
            cur = await conn.execute("SELECT * FROM users WHERE chat_id=? AND blocked=?", data)
            user_data2 = await cur.fetchall()

            if len(user_data1) != 0:

                data = (1, 0, msg)
                cur = await conn.execute("UPDATE users SET bloked=?, customer=? WHERE chat_id=?", data)
                data = (chat_id, )
                cur = await conn.execute("DELETE FROM actions WHERE chat_id=?", data)
                await conn.commit()
                await cur.close()
                await conn.close()

                return "User has been blocked sucsessfully"

            elif len(user_data2) != 0:

                data = (chat_id, )
                cur = await conn.execute("DELETE FROM actions WHERE chat_id=?", data)
                await conn.commit()
                await cur.close()
                await conn.close()

                return "User is already blocked"

            return "Incorrect chat id"

        elif action_name == "global_message":

            main_list = []
            main_list.append(await self.get_bot_customers())
            main_list.append(await self.get_bot_stuff())

            for k in range(len(main_list)):
                for j in range(len(main_list[k])):
                    for i in range(len(main_list[k])):

                        chat_id1 = main_list[k][i]
                        await self.__telegram_manager.send_message(chat_id1, str(msg))

            conn = await aiosqlite.connect(DATABASE)
            data = (chat_id, )
            cur = await conn.execute("DELETE FROM actions WHERE chat_id=?", data)
            await conn.commit()
            await cur.close()
            await conn.close()
            main_list = []

            return "Message has been send sucsesfully"

        elif action_name == "country_information":

            res = await self.__data_manager.check_country(msg)        
            if res == "There is no such country in our country list, please try later":
                conn = await aiosqlite.connect(DATABASE)
                data = (chat_id, "country_information")
                cur = await conn.execute("DELETE FROM actions WHERE chat_id=? AND action_name=?", data)
                await conn.commit()
                await cur.close()
                await conn.close()
                return "There is no such country in our country list, please try later"

            conn = await aiosqlite.connect(DATABASE)
            data = (chat_id, "country_information")
            cur = await conn.execute("DELETE FROM actions WHERE chat_id=? AND action_name=?", data)
            await conn.commit()
            await cur.close()
            await conn.close()
            return await self.__data_manager.get_country_information(res)   

        return "Incorrect action"

class DataManager:

    @staticmethod
    async def get_date():

        today = time.strftime("%Y-%m-%d")

        date1 = datetime.datetime(year=int(today[0:4]), month=int(today[5:7]), day=int(today[8:10]))
        diff = datetime.timedelta(days=1)
        date2 = date1 - diff

        date1 = str(date1)
        date2 = str(date2)

        date1 = date1.replace(" ", "T")
        date2 = date2.replace(" ", "T")
        date1 += "Z"
        date2 += "Z"

        return date1, date2

    @staticmethod
    async def create_link(slug_key):

        base = "https://api.covid19api.com/country/"
        date1, date2 = await DataManager.get_date()

        link = base + slug_key + "?from=" + date2 + "&to=" + date1
        return link

    @staticmethod
    async def connect_api_address(link):

        session = aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False))
        response = await session.get(link)
        print(response.status)
        list1 = await response.json()
        await session.close()

        return list1

    @staticmethod
    async def check_country(msg):

        conn = await aiosqlite.connect(DATABASE)
        data = (msg, )
        cur = await conn.execute("SELECT * FROM countries WHERE country_name=?", data)
        country_data = await cur.fetchall()
        await cur.close()
        await conn.close()

        if len(country_data) == 0:
            return "There is no such country in our country list, please try later"

        slug_key = country_data[0][1]
        return slug_key

    @staticmethod
    async def get_country_information(slug_key):

        link = await DataManager.create_link(slug_key)
        list1 = await DataManager.connect_api_address(link)

        str1 = "Confirmed - " + str(list1[0]["Confirmed"]) + "\n"
        str2 = "Total deaths - " + str(list1[0]["Deaths"]) + "\n"
        str3 = "Active - " + str(list1[0]["Active"])
        final_str = str1 + str2 + str3

        return final_str

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

@app.route("/", methods=["POST"])
async def request_quart():

    print(request.method)
    data_json = await request.get_json()
    print(data_json)

    if "message" not in list(data_json.keys()):
        return "Request response!"

    chat_id = str(data_json["message"]["chat"]["id"])
    text = data_json["message"]["text"]
    first_name = data_json["message"]["from"]["first_name"]

    res = await telegram_manager.responses(text, chat_id) + ", " + first_name
    await bot_manager.check_user(chat_id)
    await telegram_manager.send_message(chat_id, res)

    print("Incoming request")
    return "Request response!"

if __name__ == "__main__":

    admins_manager = BotAdmins()
    telegram_manager = TelegramManager()
    data_manager = DataManager()
    bot_manager = BotManager(admins_manager, telegram_manager, data_manager)

    app.run(port=6000)
