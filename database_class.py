import requests
import sqlite3

import get_data

DATABASE = get_data.get_variable("DATABASE")

class BotDatabase:

    @staticmethod
    def get_countries_list():

        r = requests.get("https://api.covid19api.com/countries")
        list1 = r.json()
        return list1

    @staticmethod
    def create_tables():
        list1 = BotDatabase.get_countries_list()

        conn = sqlite3.connect(DATABASE)
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS users (chat_id text PRIMARY KEY, customer int, admin int, blocked int, last_action_date text)")
        cur.execute("CREATE TABLE IF NOT EXISTS actions (chat_id text, action_name text, FOREIGN KEY(chat_id) REFERENCES users(chat_id) ON DELETE CASCADE)")
        cur.execute("CREATE TABLE IF NOT EXISTS countries (country_name text PRIMARY KEY, slug text)")

        for i in range(len(list1)):

            data = (list1[i]["Country"], list1[i]["Slug"])
            cur.execute("INSERT INTO countries (country_name, slug) VALUES(?, ?)", data)
            conn.commit()   
        conn.close()

    @staticmethod
    def check_file():
        try:
            conn = sqlite3.connect(DATABASE)
            cur = conn.cursor()
            cur.execute("SELECT * FROM countries")
            conn.close()
        except:
            BotDatabase.create_tables()
