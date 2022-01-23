import asyncio
import aiohttp
import aiosqlite

import get_data
import bot_exceptions

DATABASE = get_data.get_variable("DATABASE")

class DataManager:
    
    @staticmethod
    @bot_exceptions.check_function
    async def connect_api_address():

        session = aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False))
        response = await session.get("https://api.covid19api.com/summary")
        print(response.status)
        dict1 = await response.json()
        await session.close()

        return dict1

    async def check_country(self, msg):

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
    
    async def get_country_information(self, slug_key):

        dict1 = await DataManager.connect_api_address()

        for i in range(len(dict1["Countries"])):

            if dict1["Countries"][i]["Slug"] == slug_key:
                break

        str1 = "New Confirmed - " + str(dict1["Countries"][i]['NewConfirmed'])
        str2 = "New Deaths - " + str(dict1["Countries"][i]["NewDeaths"])
        str3 = "Total Confirmed - " + str(dict1["Countries"][i]["TotalConfirmed"])
        str4 = "Total Deaths - " + str(dict1["Countries"][i]["TotalDeaths"])
        final_str = str1 + ", " + str2 + ", " + str3 + ", " + str4
        
        return final_str
