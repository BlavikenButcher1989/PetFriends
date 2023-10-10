from selenium.webdriver.common.by import By


class Locators:

    BUTTON_REGISTRATION = (By.XPATH, "//button[contains(text(),'Зарегистрироваться')]")
    BUTTON_EXIST_ACCOUNT = (By.XPATH, "//a[contains(text(),'У меня уже есть аккаунт')]")
    EMAIL = (By.CSS_SELECTOR, '#email')
    PASSWORD = (By.CSS_SELECTOR, '#pass')
    ENTER = (By.XPATH, "//button[contains(text(),'Войти')]")

    MY_PETS = (By.XPATH, "//a[contains(text(),'Мои питомцы')]")

    FIELD_NAME = (By.CSS_SELECTOR, '#name')
    FIELD_EMAIL = (By.CSS_SELECTOR, '#email')
    FIELD_PASSWORD = (By.CSS_SELECTOR, '#pass')
    BUTTON_REGISTRATION_2 = (By.XPATH, "//button[contains(text(),'Зарегистрироваться')]")