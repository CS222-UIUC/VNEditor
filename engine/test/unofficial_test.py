def check_authorization(f):
    def wrapper(*args):
        print(args[0].url)
        return f(*args)

    return wrapper


class Client(object):
    def __init__(self, url):
        self.url = url

    @check_authorization
    def get(self):
        print("get")


Client("https://www.google.com").get()
