import allure
import requests
from requests_toolbelt.multipart import MultipartEncoder


class API:

    def __init__(self):
        self.url = 'https://petfriends.skillfactory.ru/'  #  Базовый url


    """Функция получения ключа авторизации"""
    @allure.step('Получаем Апи ключ')
    def get_api_key(self, email, password):
        headers = {'accept': 'application/json', 'email': email, 'password': password}
        response = requests.get(self.url + 'api/key', headers=headers)
        status = response.status_code
        try:
            result = response.json()
        except:
            result = response.text
        return status, result


    """Функция получения списка моих питомцев"""
    @allure.step('Получаем список моих питомцев')
    def get_list_of_my_pets(self, auth_key, filter):
        headers = {'accept': 'application/json', 'auth_key': auth_key['key']}
        params = {'filter': filter}
        response = requests.get(self.url + 'api/pets', headers=headers, params=params)
        status = response.status_code
        try:
            result = response.json()
        except:
            result = response.text
        return status, result


    """Функция добавления нового питомца"""
    @allure.step('Добавляем нового питомца')
    def add_new_pet(self, auth_key, name, animal_type, age, pet_photo):
        data = MultipartEncoder(
            {
                'name': name,
                'animal_type': animal_type,
                'age': age,
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'C:\MyProjects\DontNeed\images\wallhaven-j8grwy.jpg')
            }
        )
        headers = {'accept': 'application/json', 'auth_key': auth_key['key'], 'Content-Type': data.content_type}
        response = requests.post(self.url + 'api/pets', data=data, headers=headers)
        status = response.status_code
        try:
            result = response.json()
        except:
            result = response.text
        return status, result


    """Функция изменения питомца"""
    @allure.step('Изменяем питомца')
    def change_pet(self, auth_key, pet_id, name, animal_type, age):
        data = MultipartEncoder(
            {
                'name': name,
                'animal_type': animal_type,
                'age': age
            }
        )
        headers = {'accept': 'application/json', 'auth_key': auth_key['key'], 'Content-Type': data.content_type}
        response = requests.put(self.url + 'api/pets/' + pet_id, headers=headers, data=data)
        status = response.status_code
        try:
            result = response.json()
        except:
            result = response.text
        return status, result


    """Функция удаления питомца"""
    @allure.step('Удаляем питомца')
    def delete_my_pet(self, auth_key, pet_id):
        headers = {'accept': 'application/json', 'auth_key': auth_key['key']}
        response = requests.delete(self.url + 'api/pets/' + pet_id, headers=headers)
        status = response.status_code
        try:
            result = response.json()
        except:
            result = response.text
        return status, result