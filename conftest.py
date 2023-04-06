import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from settings import valid_email, valid_password, site, drv_path


@pytest.fixture(autouse=True, scope='class')
def start_driver_and_login(request):
    """ Запуск веб-драйвера перед каждым тестовым классом, авторизация на сайте и закрытие браузера после тестов"""
    driver = webdriver.Chrome(drv_path)
    driver.set_window_size(1400, 1000)
    # Переходим на страницу авторизации
    driver.get(f'{site}/login')

    # Установка неявного ожидания загрузки страницы
    driver.implicitly_wait(10)

    # Вводим email
    driver.find_element(By.ID, 'email').send_keys(valid_email)
    # Вводим пароль
    driver.find_element(By.ID, 'pass').send_keys(valid_password)
    # Нажимаем на кнопку входа в аккаунт
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    # Проверяем, что мы оказались на главной странице пользователя
    assert driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends", "Main page"

    # Установка неявного ожидания загрузки страницы
    driver.implicitly_wait(10)

    # Переход по ссылке "Мои питомцы"
    my_pets = driver.find_element(By.LINK_TEXT, u"Мои питомцы")
    my_pets.click()

    request.cls.driver = driver

    yield

    driver.quit()
