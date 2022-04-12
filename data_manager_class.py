import asyncio
import aiohttp
import aiosqlite
import time
import datetime

import get_data
import exceptions

DATABASE = get_data.get_variable("DATABASE")

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
    @exceptions.check_function
    async def connect_api_address(link):

        session = aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False))
        response = await session.get(link)
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

        if len(list1) == 0:
            return "Test"
        str1 = "Confirmed - " + str(list1[0]["Confirmed"])
        str2 = "Total deaths - " + str(list1[0]["Deaths"])
        str3 = "Active - " + str(list1[0]["Active"])
        final_str = str1 + ", " + str2 + ", " + str3

        return final_str
