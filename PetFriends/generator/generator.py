from faker import Faker
from dataclasses import dataclass
from random import randint

"""Генератор"""
@dataclass
class Generator:
    names: str = None
    email: str = None
    password: str = None

faker_ru = Faker('Ru')
def generator():
    return Generator(
        names=faker_ru.first_name(),
        email=faker_ru.email(),
        password=faker_ru.password()
    )


age = randint(1, 100)  #  Генерируем возраст