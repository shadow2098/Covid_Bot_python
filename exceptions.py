import asyncio

def check_function(function):
    async def wrapper(*args):

        try:

            x = await function(*args)
            return x

        except Exception as e:

            f = open("errors.txt", "a")
            f.write("\n")
            f.write(str(e))
            f.close()

    return wrapper
