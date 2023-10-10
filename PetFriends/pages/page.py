import allure

from pages.base_page import BasePage
from locators.locators import Locators as L
from data.data import email, password
from generator.generator import generator
class Page(BasePage):

    @allure.step('Выполняем регистрацию на сайте')
    def registration(self):
        self.clickability(L.BUTTON_REGISTRATION).click()
        self.visibility(L.FIELD_NAME).clear()
        self.visibility(L.FIELD_NAME).send_keys(generator().names)
        self.visibility(L.FIELD_EMAIL).clear()
        self.visibility(L.FIELD_EMAIL).send_keys(generator().email)
        self.visibility(L.FIELD_PASSWORD).clear()
        self.visibility(L.FIELD_PASSWORD).send_keys(generator().password)
        self.clickability(L.BUTTON_REGISTRATION_2).click()

    @allure.step('Выполненяем авторизацию на сайте')
    def authorization(self):  #  Функция авторизации на сайте
        self.clickability(L.BUTTON_REGISTRATION).click()
        self.clickability(L.BUTTON_EXIST_ACCOUNT).click()
        self.visibility(L.EMAIL).send_keys(email)
        self.visibility(L.PASSWORD).send_keys(password)
        self.clickability(L.ENTER).click()

    @allure.step('Выполненяем авторизацию и переходим на страницу с моими питомцами')
    def authorization_and_open_my_pets(self):  #  Функция авторизации и открытия раздела Мои питомцы
        self.clickability(L.BUTTON_REGISTRATION).click()
        self.clickability(L.BUTTON_EXIST_ACCOUNT).click()
        self.visibility(L.EMAIL).send_keys(email)
        self.visibility(L.PASSWORD).send_keys(password)
        self.clickability(L.ENTER).click()
        self.clickability(L.MY_PETS).click()



