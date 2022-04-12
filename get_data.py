import json

def get_data(file_name):
        f = open(file_name, "r")
        data = json.load(f)
        f.close()
        return data

def get_variable(variable_name):
        data = get_data("bot_information.json")
        return data[variable_name]