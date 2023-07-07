from faker import Faker
from pprint import pprint


def imitateData():
    fake = Faker()
    for i in range(10):
        print(fake.name())


if __name__ == '__main__':
    imitateData()