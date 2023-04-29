from pydantic import BaseModel


class a(BaseModel):
    x = 1
    y = 2


class b:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def p(self):
        print(f"x {self.x}, y {self.y}")


ai = a()
bi = b(**ai.dict())

bi.p()
