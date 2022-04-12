import asyncio
import aiosqlite

import get_data

DATABASE = get_data.get_variable("DATABASE")

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