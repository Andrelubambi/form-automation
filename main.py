from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time

def main():
    # Inicializa o navegador
    driver = webdriver.Chrome()

    try:
        # Acessa o site do formulário
        driver.get("https://www.selenium.dev/selenium/web/web-form.html")
        time.sleep(2)

        # Preenche os campos do formulário
        driver.find_element(By.NAME, "my-text").send_keys("Teste Selenium")
        driver.find_element(By.NAME, "my-password").send_keys("123456")
        driver.find_element(By.NAME, "my-textarea").send_keys("Esse é um teste automatizado.")

        select = Select(driver.find_element(By.NAME, "my-select"))
        select.select_by_visible_text("Two")

        driver.find_element(By.NAME, "my-check").click()
        driver.find_element(By.ID, "my-radio-2").click()

        time.sleep(1)
        driver.find_element(By.TAG_NAME, "button").click()

        time.sleep(5)  # Espera para ver o resultado
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
