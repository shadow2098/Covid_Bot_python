
import asyncio
import aiohttp
import aiosqlite



TELEGRAM_TOKEN = "5069072255:AAHWjosTYGmR56MQ6Sm16uOFuYEu9L3XrXw"
TELEGRAM_URL = "https://api.telegram.org/bot{0}/".format(TELEGRAM_TOKEN)
DATABASE = "main_bot_database.db"

class DataManager:

    async def connect_api_address(self):
        
        session = aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False))
        response = await session.get("https://api.covid19api.com/summary")
        print(response.status)
        dict1 = await response.json()
        await session.close()

        return dict1
        
    async def check_country(self, msg):
        
        conn = await aiosqlite.connect("main_bot_database.db")
        data = (msg, )
        cur = await conn.execute("SELECT * FROM countries WHERE country_name=?", data)
        country_data = await cur.fetchall()
        await cur.close()
        await conn.close()

        if len(country_data) == 0:
            return "There is no such country in our country list, please try later"

        slug_key = country_data[0][1]
        return slug_key
    
    async def get_country_information(self, slug_key):

        dict1 = await self.connect_api_address()

        for i in range(len(dict1["Countries"])):
            
            if dict1["Countries"][i]["Slug"] == slug_key:
                break

        str1 = "New Confirmed - " + str(dict1["Countries"][i]['NewConfirmed'])
        str2 = "New Deaths - " + str(dict1["Countries"][i]["NewDeaths"])
        str3 = "Total Confirmed - " + str(dict1["Countries"][i]["TotalConfirmed"])
        str4 = "Total Deaths - " + str(dict1["Countries"][i]["TotalDeaths"])
        final_str = str1 + ", " + str2 + ", " + str3 + ", " + str4
        
        return final_str
