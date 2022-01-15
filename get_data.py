import json

def get_data(file_name):

        
        f = open(file_name, "r")
        data = json.load(f)
        #data = f.read()
        f.close()

        return data

def get_variable(variable_name):

        data = get_data("bot_information.json")
        return data[variable_name]
'''
        data = data.split()
        
        for i in range(len(data)):
                if data[i] == variable_name:
                        return data[i + 2]
'''

x = get_variable("TELEGRAM_TOKEN")
print(x)
