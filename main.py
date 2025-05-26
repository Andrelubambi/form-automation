from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
 

def iniciar_driver():
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    return driver

def main():
    driver = iniciar_driver()
    driver.get("https://www.google.com")
    print(driver.title)
    driver.quit()

if __name__ == "__main__":
    main()
