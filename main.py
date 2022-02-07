import asyncio
import json
import aiosqlite
from quart import Quart
from quart import request

import admins_class
import manager_class
import data_manager_class
import telegram_manager_class
import database_class

app = Quart(__name__)

admins_manager = None
telegram_manager = None
data_manager = None
bot_manager = None

@app.route("/", methods=["POST"])
async def request_quart():
    try:
        data_json = await request.get_json()

        if "message" not in list(data_json.keys()):
            return "Request response!"

        chat_id = str(data_json["message"]["chat"]["id"])
        text = data_json["message"]["text"]
        first_name = data_json["message"]["from"]["first_name"]

        res = await telegram_manager.responses(text, chat_id) + ", " + first_name
        await bot_manager.check_user(chat_id)
        await telegram_manager.send_message(chat_id, res)
        return "Request response!"
    
    except Exception as e:

        f = open("errors.txt", "a")
        f.write("\n")
        f.write(str(e))
        f.close()
        return "Error happened"

if __name__ == "__main__":

    database_class.BotDatabase.check_file()

    admins_manager = admins_class.BotAdmins()
    telegram_manager = telegram_manager_class.TelegramManager()
    data_manager = data_manager_class.DataManager()
    bot_manager = manager_class.BotManager(admins_manager, telegram_manager, data_manager)

    telegram_manager.bind_bot_manager(bot_manager)

    app.run(port=6001, debug=True)
