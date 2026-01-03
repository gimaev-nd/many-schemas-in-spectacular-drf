from itertools import islice
from random import randint
from time import sleep

from faker import Faker


class Item:
    def __init__(self, faker: Faker) -> None:
        self.faker: Faker = faker
        self.gender = randint(0, 1)

    @property
    def first_name(self) -> str:
        if self.gender:
            return self.faker.first_name_male()
        return self.faker.first_name_female()

    @property
    def last_name(self) -> str:
        if self.gender:
            return self.faker.last_name_male()
        return self.faker.last_name_female()

    @property
    def debt(self) -> int:
        sleep(0.1)
        return randint(0, 1) and randint(0, 10000)


class FakeData:
    def __init__(self, count=1000):
        faker = Faker("ru")
        self._count = count
        self.data = (Item(faker) for _ in range(self._count))

    def __iter__(self):
        return self

    def __next__(self):
        return next(self.data)

    def count(self):
        return self._count

    def __getitem__(self, index, /):
        if isinstance(index, slice):
            return list(islice(self.data, index.start, index.stop, index.step))
        return 0
