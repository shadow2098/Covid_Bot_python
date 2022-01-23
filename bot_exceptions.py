import asyncio

def check_function(function):
    async def wrapper(*args):

        try:
            print("test")
            await function(*args)
            print(9999999)
        except Exception as e:

            f = open("errors.txt", "a")
            f.write("\n")
            f.write(str(e))
            f.close()

    return wrapper

'''
@check_function
async def summ():
print(10 / 0)

asyncio.run(summ())

try:
except:
finally:
'''
