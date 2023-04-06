from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from settings import site


class TestPetsInTable:

    def test_count_my_pets(self):
        """Поверка того, что на странице "Мои питомцы" общее количество питомцев равно числу питомцев в таблице"""

        # Сюда потом можно добавить авторизацию, если не та ссылка
        assert self.driver.current_url == f'{site}/my_pets', "Failed path"

        # Явное ожидание загрузки элемента классов .col-sm-4 left, в котором указывается количество питомцев
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.\\.col-sm-4.left'))
        )
        # Кол-во питомцев
        account_summary = self.driver.find_element(By.CSS_SELECTOR, '.\\.col-sm-4.left').text
        count_pets = int(account_summary.split("\n")[1].split(" ")[1])
        # print(f"\ncount_pets = {count_pets}")

        # Явное ожидание загрузки строк таблицы с питомцами
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.table.table-hover tbody tr'))
        )

        # Питомцы в таблице
        count_pets_in_table = len(self.driver.find_elements(By.CSS_SELECTOR, '.table.table-hover tbody tr'))
        # print(f"\ncount_pets_in_table = {count_pets_in_table}")

        assert count_pets == count_pets_in_table, "Summary count of pets is not equal the count in the table "

    def test_count_photo(self):
        """Поверка того, что на странице "Мои питомцы" у половины и более питомцев есть фото"""

        # Сюда потом можно добавить авторизацию, если не та ссылка
        assert self.driver.current_url == f'{site}/my_pets', "Failed path"

        # Явное ожидание загрузки строк таблицы с питомцами
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.table.table-hover tbody tr'))
        )

        pets_in_table = self.driver.find_elements(By.CSS_SELECTOR, '.table.table-hover tbody tr')
        count_pets_in_table = len(pets_in_table)

        # Явное ожидание загрузки фото питомцев
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//img[contains(@src, "data:image")]'))
        )

        # Фото
        images = self.driver.find_elements(By.XPATH, '//img[contains(@src, "data:image")]')
        count_my_pets_image = len(images)
        # print(f"\nImages = {count_my_pets_image}")

        assert count_my_pets_image / count_pets_in_table > 0.5, "Too few photos"

    def test_different_pets(self):
        """Поверка того, что на странице "Мои питомцы" у все питомцы разные"""

        # Сюда потом можно добавить авторизацию, если не та ссылка
        assert self.driver.current_url == f'{site}/my_pets', "Failed path"

        # Явное ожидание загрузки строк таблицы с питомцами
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.table.table-hover tbody tr'))
        )

        pets_in_table = self.driver.find_elements(By.CSS_SELECTOR, '.table.table-hover tbody tr')

        pet_list = set()
        for i in range(len(pets_in_table)):
            name, breed, age = pets_in_table[i].text.split("\n")[0].split(" ")
            pet = name + "|" + breed + "|" + age
            # print("\n", pet)
            assert pet not in pet_list, f"{i} pet {pet} is not unique"
            pet_list.add(pet)
