class A:
    def __init__(self, arr):
        self.arr = arr.copy()
        print(self.arr)
        self.arr.pop(0)
        print(self.arr)


class B:
    def __init__(self):
        self.x = 10


a = [B(), B(), B()]

print(a)

b = A(a)


