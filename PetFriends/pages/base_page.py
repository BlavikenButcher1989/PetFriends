import allure
from selenium.webdriver.support.wait import WebDriverWait as Wait
from selenium.webdriver.support import expected_conditions as EC



class BasePage:

    def __init__(self, driver):
        self.driver = driver
        self.url = 'https://petfriends.skillfactory.ru/'

    @allure.step('Открываем сайт PetFriends')
    def open_site(self):  #  Функция открытия сайта
        self.driver.get(self.url)

    def visibility(self, locator):  #  Функция ожидания видимости элемента
        return Wait(self.driver, 10).until(EC.visibility_of_element_located(locator))

    def clickability(self, locator):  #  Функция ожидания кликабельности элемента
        return Wait(self.driver, 10).until(EC.element_to_be_clickable(locator))