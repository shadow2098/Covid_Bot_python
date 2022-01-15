import asyncio
import json
import aiosqlite
from quart import Quart
from quart import request

import bot_admins_class
import bot_manager_class
import bot_data_manager_class
import bot_telegram_manager_class

app = Quart(__name__)

admins_manager = None
telegram_manager = None
data_manager = None
bot_manager = None

@app.route("/", methods=["POST"])
async def request_quart():

    await telegram_manager.bind_bot_manager(bot_manager)
    
    #print(request.method)
    data_json = await request.get_json()
    #print(data_json)
    
    if "message" not in list(data_json.keys()):
        return "Request response!"

    chat_id = str(data_json["message"]["chat"]["id"])
    text = data_json["message"]["text"]
    first_name = data_json["message"]["from"]["first_name"]
            
    res = await telegram_manager.responses(text, chat_id) + ", " + first_name
    await bot_manager.check_user(chat_id)
    await telegram_manager.send_message(chat_id, res)
    
    #print("Incoming request")
    return "Request response!"

if __name__ == "__main__":
    
    admins_manager = bot_admins_class.BotAdmins()
    telegram_manager = bot_telegram_manager_class.TelegramManager()
    data_manager = bot_data_manager_class.DataManager()
    bot_manager = bot_manager_class.BotManager(admins_manager, telegram_manager, data_manager)
    
    app.run(port=6000)
    
