import allure
from selenium.webdriver.support.wait import WebDriverWait as Wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from pages.page import Page
from API.api import API
from data.data import email, password
from generator.generator import generator, age
import random


@allure.suite('Тесты сайта PetFriends')
class TestPetFriends:

    """Тест регистрации на сайте"""

    """После регистрации мы сразу попадаем на сайт, без авторизации"""

    @allure.title('Тест регистрации на сайте')
    def test_registration(self, driver):  #  Проверка регистрации на сайте
        page = Page(driver)
        page.open_site()  #  Открываем сайт
        page.registration()  #  Регитсрируемся на сайте
        try:
            driver.find_element(By.XPATH, "//div[contains(text(),'The user with this name already registered!')]")  #  Если имя существует, вводим другое
            page.registration()
        except:
            pass
        all_pets_text = Wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[contains(text(),'Все питомцы наших пользователей')]")))  #  Текст на странице с питомцами
        with allure.step('Регистрация прошла успешно'):
            assert 'Все питомцы наших пользователей' in all_pets_text.text  #  Проверяем, что мы попали на страницу со всеми питомцами
        Wait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Выйти')]"))).click()  #  Нажимаем кнопку "Выход"
        button_registration = Wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//button[contains(text(),'Зарегистрироваться')]")))  #  Кнопка "Зарегестрироваться"
        with allure.step('Выход из учетной записи прошел успешно'):
            assert 'Зарегистрироваться' in button_registration.text  #  Проверяем, что мы вышли из аккаунта



    """Тест открытия формы авторизации"""

    @allure.title('Тест открытия формы авторизации')
    def test_authorization_form_is_opening(self, driver):  #  Проверка открытия формы авторизации
        page = Page(driver)
        page.open_site()  #  Открываем сайт
        Wait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Зарегистрироваться')]"))).click()  #  Нажимаем на кнопку Зарегестрироваться
        Wait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'У меня уже есть аккаунт')]"))).click()  #  Нажимаем на кнопку У меня уже есть аккаунт
        block_of_fields_and_buttons = Wait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//body/div[1]/div[1]/form[1]')))  #  Блок с полями для авторизации
        list_of_names_of_fields_and_buttons = [i for i in block_of_fields_and_buttons.text.split('\n') if i != '']  #  Список с наименованиями полей и кнопок формы авторизации
        with allure.step('Произошел переход на форму авторизации'):
            assert 'Войти' and 'Электронная почта' and 'Пароль' in list_of_names_of_fields_and_buttons  #  Проверяем, что присутствуют поля для авторизации


    """Тест авторизации на сайте"""

    @allure.title('Тест авторизации')
    def test_authorization(self, driver):  #  Проверка успешной авторизации
        page = Page(driver)
        page.open_site()  #  Открываем сайт
        page.authorization()  #  Авторизовываемся
        list_of_all_pets = Wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//div[@class="card-deck"]')))  #  Блок со всеми питомцами
        all_pets_text = Wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[contains(text(),'Все питомцы наших пользователей')]")))  #  Надпись над блоком с питомцами
        with allure.step('Авторизация прошла успешно'):
            assert 'Все питомцы наших пользователей' in all_pets_text.text  # Проверяем, что мы авторизовались и зашли на страницу с питомцами всех пользователей
        with allure.step('На странице присутствуют карточки с питомцами'):
            assert list_of_all_pets.text != ''  #  Проверяем, что блок с питомцами не путой


    """Тест получения ключа авторизации"""

    @allure.title('Тест получения АПИ ключа')
    def test_get_api_key(self, email=email, password=password):  #  Проверка получения АПИ ключа
        pf = API()
        status, result = pf.get_api_key(email, password)  #  Получаем статус код и АПИ ключ
        with allure.step('Статус код = 200'):
            assert status == 200  #  Проверяем статус код
        with allure.step('АПИ ключ получен'):
            assert 'key' in result  #  Проверяем, что получили АПИ ключ


    """Тест получения списка моих питомцев"""

    @allure.title('Тест получения списка моих питомцев')
    def test_get_list_of_pets(self, filter = 'my_pets'):  #  Проверяем возможность получить список моих питомцев
        pf = API()
        _, auth_key = pf.get_api_key(email, password)  #  Получаем АПИ ключ
        status, result = pf.get_list_of_my_pets(auth_key, filter)  #  Получаем список моих питомцев
        with allure.step('Статус код = 200'):
            assert status == 200  #  Проверяем статус код
        with allure.step('Присутствуют карточки с моими питомцами'):
            assert len(result['pets']) > 0  #  Проверяем, что список питомцев не пустой


    """Тест добавления нового питомца"""

    @allure.title('Тест добавления питомца')
    def test_add_new_pet(self, driver, name = f'{generator().names}', animal_type = 'Флафер', age = f'{age}', pet_photo = 'C:\MyProjects\DontNeed\images\wallhaven-j8grwy.jpg'):  #  Проверка добавления питомца
        page = Page(driver)
        page.open_site()  #  Открываем сайт
        page.authorization_and_open_my_pets()  # Авторизуемся и открываем раздел Мои питомцы
        block_with_count_of_my_pets = [i for i in (Wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH,
        '//div[@class=".col-sm-4 left"]')))).text.split()]  # Достаем из блока в левой части (с именем пользователя) количество моих питомцев до добавления нового
        count_of_my_pets_before_adding_new_pet = int(block_with_count_of_my_pets[2])  # Числовое значение количества питомцев до добавления нового питомца
        pf = API()
        _, auth_key = pf.get_api_key(email, password)  #  Получаем АПИ ключ
        status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)  #  добавляем питомца
        driver.refresh()  #  Обновляем страницу
        block_with_count_of_my_pets = [i for i in (Wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH,
        '//div[@class=".col-sm-4 left"]')))).text.split()]  # Достаем из блока в левой части (с именем пользователя) количество моих питомцев после добавления нового
        count_of_my_pets_after_adding_new_pet = int(block_with_count_of_my_pets[2])  #  Числовое значение количества питомцев после добавления нового питомца
        all_my_pets = Wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@id='all_my_pets']")))  #  Список всех моих питомцев, включая нового
        with allure.step('Статус код = 200'):
            assert status == 200  #  Проверяем ствтус код
        with allure.step('Питомец создался'):
            assert result['name'] == name  #  Проверяем, что питомец создался
        with allure.step('Имя нового питомца содержится в списке моих питомцев'):
            assert result['name'] in all_my_pets.text  # Проверяем, что имя добавленного питомца содержится в списке всех моих питомцев
        with allure.step('Количество питомцев увеличилось на 1'):
            assert count_of_my_pets_after_adding_new_pet == (count_of_my_pets_before_adding_new_pet + 1)  #  Проверяем, что количество питомцев после добавления нового равно количеству питомцев до добавления плюс один, то есть питомец добавился


    """Тест изменения питомца"""

    @allure.title('Тест изменения питомца')
    def test_change_my_pet(self, driver, name = f'{generator().names}', animal_type = 'Флаферино', age = f'{age}'):  #  Проверка изменения питомца
        page = Page(driver)
        page.open_site()  #  Открываем сайт
        page.authorization_and_open_my_pets()  # Авторизуемся и открываем раздел Мои питомцы
        pf = API()
        _, auth_key = pf.get_api_key(email, password)  #  Получаем АПИ ключ
        _, list_of_my_pets_before_change = pf.get_list_of_my_pets(auth_key, 'my_pets')  #  Список моих питомцев до изменения питомца
        pet_before_change = list_of_my_pets_before_change['pets'][0]  #  Питомец до изменения
        pet_id = list_of_my_pets_before_change['pets'][0]['id']  #  ID изменяемого питомца
        status, result = pf.change_pet(auth_key, pet_id, name, animal_type, age)  #  Изменяем питомца
        _, list_of_my_pets_after_change = pf.get_list_of_my_pets(auth_key, 'my_pets')  #  Список моих питомцев после изенения питомца
        pet_after_change = list_of_my_pets_after_change['pets'][0]  #  Питомец после изменения
        with allure.step('Статус код = 200'):
            assert status == 200  #  Проверяем статус код
        with allure.step('Количество моих питомцев не изменилось'):
            assert len(list_of_my_pets_before_change) == len(list_of_my_pets_after_change)  #  Проверяем, что количество моих питомцев не изменилось после изменения питомца
        with allure.step('Существующий питомец был изменен'):
            assert pet_before_change['id'] == pet_after_change['id'] and pet_before_change['name'] != pet_after_change['name']  #  Проверяем, что ID у питомца до и после изменения - одинаковый (т.е. питомец один и тот же); и что имя питомца изменилось


    """Тест удаления питомца"""

    @allure.title('Тест удаления питомца')
    def test_delete_my_pet(self, driver):  #  Проверка удаления питомца
        page = Page(driver)
        page.open_site()  #  Открываем сайт
        page.authorization_and_open_my_pets()  # Авторизуемся и открываем раздел Мои питомцы
        pf = API()
        _, auth_key = pf.get_api_key(email, password)  #  Получаем АПИ ключ
        _, list_of_my_pets = pf.get_list_of_my_pets(auth_key, 'my_pets')  #  Список моих питомцев
        pet_ids = [i.get('id') for i in list_of_my_pets['pets']]  #  Создаем список с ID всех моих питомцев
        pet_id = random.choice(pet_ids)  #  ID рандомного питомца
        block_with_count_of_my_pets = Wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//div[@class=".col-sm-4 left"]')))  #  Блок в левой части с именем пользователя
        count_of_my_pets_before_delete = int([i for i in block_with_count_of_my_pets.text.split()][2])  #  Количество моих питомцев до удаления питомца
        status, result = pf.delete_my_pet(auth_key, pet_id)  #  Удаляем питомца
        driver.refresh()  #  Обновляем страницу
        block_with_count_of_my_pets = Wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//div[@class=".col-sm-4 left"]')))  #  Блок в левой части с именем пользователя
        count_of_my_pets_after_delete = int([i for i in block_with_count_of_my_pets.text.split()][2])  #  Количество моих питомцев после удаления питомца
        with allure.step('Статус код = 200'):
            assert status == 200  # Проверяем статус код
        with allure.step('Количество питомцев уменьшилось на 1'):
            assert count_of_my_pets_after_delete == (count_of_my_pets_before_delete - 1)  #  Проверяем, что количество моих питомцев после удаления равно количеству моих питомцев до удаления минус 1, то есть питомец удален