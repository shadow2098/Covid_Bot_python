import aiohttp
import asyncio
import aiosqlite
import pprint
import sqlite3

async def main1():
    
    session = aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False))
    response = await session.get("https://api.covid19api.com/country/brazil?from=2022-01-26T00:00:00Z&to=2022-01-27T00:00:00Z")
    print(response.status)
    list1 = await response.json()
    print(type(list1))
    await session.close()
    return list1
    
list1 = asyncio.run(main1())
pprint.pprint(list1)
print("\n")
str1 = "Confirmed - " + str(list1[0]["Confirmed"]) + "\n"
str2 = "Total deaths - " + str(list1[0]["Deaths"]) + "\n"
str3 = "Active - " + str(list1[0]["Active"])
final_str = str1 + str2 + str3

print(final_str)


'''
conn = sqlite3.connect("main_bot_database.db")
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS users (chat_id text PRIMARY KEY, customer int, admin int, blocked int)")
cur.execute("CREATE TABLE IF NOT EXISTS actions (chat_id text, action_name text, FOREIGN KEY(chat_id) REFERENCES users(chat_id) ON DELETE CASCADE)")
cur.execute("CREATE TABLE IF NOT EXISTS countries (country_name text PRIMARY KEY, slug text)")

data = (1707367602 , )
cur.execute("SELECT * FROM users WHERE chat_id =?", data)
x = cur.fetchall()
print(x)
print(200)
data = ("1707367602" , )
#data1 = ("1707367602" , 0, 1, 0)
#cur.execute("INSERT INTO users (chat_id, customer, admin, blocked) VALUES(?, ?, ?, ?)", data1)
x = cur.fetchall()
print(x)


for i in range(len(list1)):

    data = (list1[i]["Country"], list1[i]["Slug"])
    cur.execute("INSERT INTO countries (country_name, slug) VALUES(?, ?)", data)
    conn.commit()

#https://api.covid19api.com/summary
#https://api.covid19api.com/countries
'''
'''
async def main():

    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        async with session.get('https://api.covid19api.com/countries') as resp:
            print(resp.status)
            print(await resp.text())

asyncio.run(main())
'''
'''
print("\n", "\n")

async def main1():
    
    session = aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False))
    response = await session.get("https://api.covid19api.com/countries")
    print(response.status)
    dict1 = await response.json()
    #print(list1[0]["Country"], list1[0]["Slug"])
    await session.close()
    #pprint.pprint(dict1)
    #slug = "afghanistan"
    print(dict1["Countries"][2]["Slug"])
    
    
    conn = await aiosqlite.connect("main_bot_database.db")
    data = ("Spain", )
    cur = await conn.execute("SELECT * FROM countries WHERE country_name=?", data)
    country_data = await cur.fetchall()
    await cur.close()
    await conn.close()
    
    slug_key = country_data[0][1]
    print(type(slug_key))
    
list1 = asyncio.run(main1())

conn = sqlite3.connect("main_bot_database.db")
cur = conn.cursor()
data = ("Albania", )
cur.execute("SELECT * FROM countries WHERE country_name=?", data)
country_data = cur.fetchal()
conn.close()

slug_key = list1[0][1]

list1 = asyncio.run(main1())
conn = sqlite3.connect("main_bot_database.db")
cur = conn.cursor()

for i in range(len(list1)):

    data = (list1[i]["Country"], list1[i]["Slug"])
    cur.execute("INSERT INTO countries (country_name, slug) VALUES(?, ?)", data)
    conn.commit()
    print(990)

#cur.execute("CREATE TABLE IF NOT EXISTS countries (country_name text PRIMARY KEY, slug text)")
print(200)
conn.close()
'
'''
