import asyncio

import aiosqlite

TELEGRAM_TOKEN = "5069072255:AAHWjosTYGmR56MQ6Sm16uOFuYEu9L3XrXw"
TELEGRAM_URL = "https://api.telegram.org/bot{0}/".format(TELEGRAM_TOKEN)
DATABASE = "main_bot_database.db"
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
        

