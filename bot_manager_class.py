import asyncio


import aiosqlite



TELEGRAM_TOKEN = "5069072255:AAHWjosTYGmR56MQ6Sm16uOFuYEu9L3XrXw"
TELEGRAM_URL = "https://api.telegram.org/bot{0}/".format(TELEGRAM_TOKEN)
DATABASE = "main_bot_database.db"

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
