from cProfile import label
from faulthandler import is_enabled
import dotenv
import os
from selenium import webdriver
import selenium
import selenium.webdriver
from selenium.webdriver.common.by import By
import selenium.webdriver.remote
import selenium.webdriver.remote.webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json

dotenv.load_dotenv()


def setup():
    chrome_profile_path = os.getenv("CHROME_PROFILE")

    options = webdriver.ChromeOptions()
    options.add_argument(f"--user-data-dir={chrome_profile_path}")
    options.add_argument("--profile-directory=Profile 1")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(3)
    return driver


def get_site():
    domain = os.getenv("DOMAIN")
    driver = setup()
    wait = WebDriverWait(driver, timeout=5)
    
    driver.get(f"{domain}/relatorioTarefas/DetalheTarefa/40336017")
    if driver.current_url == f"{domain}/login":
        driver.find_element(By.CLASS_NAME, "form-login-button").click()
        wait.until(EC.url_changes(f"{domain}/login"))
    if driver.current_url == f"{domain}/planejamento":
        driver.get(f"{domain}/relatorioTarefas/DetalheTarefa/40336017")
        wait.until(EC.url_changes(f"{domain}/planejamento"))
    wait.until(EC.element_to_be_clickable((By.ID, "editar")))
    return driver



def load_questionnaires():
    with open("questionnaires.json", "r", encoding="utf-8") as json_file:
        return json.load(json_file)
    
### TO DO 

    
    
    


def editar(driver: webdriver.Chrome):
    questions = load_questionnaires()
    driver.find_element(By.ID, "editar").click()
    questionarios_tab = driver.find_element(
        By.XPATH, "//*[@href='#checklist']" # Encontra o item Questionarios
    )
    wait = WebDriverWait(driver, timeout=5)
    wait.until(EC.element_to_be_clickable(questionarios_tab))
    questionarios_tab.click()
    questionarios = driver.find_elements(By.XPATH, f"//*[@data-codigo='153680']")
    for questionario in questionarios:
        labels = questionario.find_elements(By.XPATH, ".//label")
        for label in labels:
            driver.execute_script("arguments[0].style.color = 'yellow';", label)
        


def quit_by_console_input(driver: webdriver.Chrome):
    input("Press enter to quit")
    driver.quit()

driver = get_site()
editar(driver)
quit_by_console_input(driver)
