from selenium.webdriver.common.by import By
from settings import site


class TestPetParams:

    def test_pet_params(self):
        """Поверка того, что на странице "Мои питомцы" у всех питомцев есть имя, возраст и порода"""

        assert self.driver.current_url == f'{site}/my_pets', "Failed path"

        # Установка неявного ожидания загрузки страницы
        self.driver.implicitly_wait(10)

        pets_in_table = self.driver.find_elements(By.CSS_SELECTOR, '.table.table-hover tbody tr')

        for i in range(len(pets_in_table)):
            name, breed, age = pets_in_table[i].text.split("\n")[0].split(" ")
            #print("\n", name, breed, age)

            # Проверка имени
            assert name != '', f"{i} pet's name is empty"
            # Проверка породы
            assert breed != '', f"{i} pet's breed is empty"
            # Проверка возраста
            assert age != '', f"{i} pet's age is empty"

    def test_different_names(self):
        """Поверка того, что на странице "Мои питомцы" у всех питомцев разные клички"""

        assert self.driver.current_url == f'{site}/my_pets', "Failed path"

        # Установка неявного ожидания загрузки страницы
        self.driver.implicitly_wait(10)

        pets_in_table = self.driver.find_elements(By.CSS_SELECTOR, '.table.table-hover tbody tr')

        name_list = set()
        for i in range(len(pets_in_table)):
            name, breed, age = pets_in_table[i].text.split("\n")[0].split(" ")
            #print("\n", name, breed, age)
            assert name not in name_list, f"{i} pet's name {name} is not unique"
            name_list.add(name)
