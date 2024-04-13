class Car():
    def __init__(self, n, p ):
        self.name = n
        self.price = p
        print(f'{self.name} has {self.price}')


car1 = Car('BMW', 10000000)
car2 = Car('Benz', 20000000)


