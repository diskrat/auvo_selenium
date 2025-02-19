import random
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
import locale
#import time
dotenv.load_dotenv()
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
#start_time = time.time() 

def setup():
    chrome_profile_path = os.getenv("CHROME_PROFILE")

    options = webdriver.ChromeOptions()
    options.add_argument(f"--user-data-dir={chrome_profile_path}")
    options.add_argument("--profile-directory=default")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    return driver


def get_site():
    domain = os.getenv("DOMAIN")
    driver = setup()
    wait = WebDriverWait(driver, timeout=5)
    tarefa =  40118777
    driver.get(f"{domain}/relatorioTarefas/DetalheTarefa/{tarefa}")
    if driver.current_url == f"{domain}/login":
        driver.find_element(By.CLASS_NAME, "form-login-button").click()
        wait.until(EC.url_changes(f"{domain}/login"))
    if driver.current_url == f"{domain}/planejamento":
        driver.get(f"{domain}/relatorioTarefas/DetalheTarefa/{tarefa}")
        wait.until(EC.url_changes(f"{domain}/planejamento"))
    wait.until(EC.element_to_be_clickable((By.ID, "editar")))
    return driver



def load_questionnaires():
    with open("questionnaires.json", "r", encoding="utf-8") as json_file:
        return json.load(json_file)
    
### TO DO 

    
def load_equipment_data():
    with open("processed_data.json", "r", encoding="utf-8") as json_file:
        return json.load(json_file)




def editar(driver: webdriver.Chrome):
    questions = load_questionnaires()['questions']
    dados_equipamento = load_equipment_data()
    driver.find_element(By.ID, "editar").click()
    questionarios_tab = driver.find_element(
        By.XPATH, "//*[@href='#checklist']" # Encontra o item Questionarios
    )
    wait = WebDriverWait(driver, timeout=5)
    wait.until(EC.element_to_be_clickable(questionarios_tab))
    questionarios_tab.click()
    questionarios = driver.find_elements(By.XPATH, f"//*[@data-codigo='153680']")
    maquinas = []
    with open("maquinas.txt",'r') as file:
        maquinas = file.readlines()
    equipamento_selecionado = []
    for index, equipamento in enumerate(questionarios):
        if equipamento:
            equipamento_id = ''
            tensao = None
            carga_termica = maquinas[index].split()[0]
            if carga_termica == 'e':
                equipamento_selecionado.append('skip')
            else:
                if int(carga_termica) < 36:
                    equipamento_id = f'{carga_termica}'
                    tensao = random.randint(205,225)
                        
                elif int(carga_termica) >= 36:
                    equipamento_id = f'{carga_termica}'
                    fase = ''
                    while fase not in ['t', 'm']:
                        fase = maquinas[index].split()[1]
                        if fase in ['m', 't']:
                            if fase == 't':
                                equipamento_id += f' {380}'
                                tensao = (random.randint(350,390), random.randint(205,225))
                            else:
                                equipamento_id += f' {220}'
                                tensao = random.randint(205,225)
                    
                equipamento_selecionado.append((equipamento_id, tensao))
    
                
    for index, questionario in enumerate(questionarios):
        if questionario:
            if equipamento_selecionado[index] != 'skip':
                labels = questionario.find_elements(By.XPATH, ".//label")
                questao_identificador = "observação"
                label_id = next(
                    item.get_attribute('for')
                    for item in labels
                    if questao_identificador in  item.text
                )
                input_element = driver.find_element(By.ID, label_id)
                if input_element.get_attribute('value') != '':
                    input_element.click()
                    pular_questionario = input('Pular? (y,n) ')
                    if pular_questionario == 'y':
                        continue
                for label in labels:
                    label_id = label.get_attribute("for")
                    if label_id:
                        input_element = driver.find_element(By.ID, label_id)
                        id_pergunta = input_element.get_attribute("data-codigo-pergunta")
                        
                        question = next(
                            item
                            for item in questions
                            if (item['id'] == int(id_pergunta))
                        )
                        if question['answerType'] == 3:
                            driver.execute_script("arguments[0].style.color = 'green';", label)
                            if question["expectedValue"] != input_element.is_selected():
                                driver.execute_script("arguments[0].click();", label)
                        if question['answerType'] == 2:
                            driver.execute_script("arguments[0].style.color = 'blue';", label)
                            text_field = driver.find_element(By.ID, label_id)
                            if text_field.get_attribute("data-tipo-da-pergunta") == "2":
                                if text_field.get_attribute('value') == '' or not text_field.get_attribute('value'):
                                    if question['id'] == 1980614 or question['id'] == 1980615:
                                        if int(equipamento_selecionado[index][0].split()[0]) < 36:
                                            text_field.send_keys(f"{equipamento_selecionado[index][1]}")
                                        else:
                                            if equipamento_selecionado[index][0].split()[1] == '220':
                                                text_field.send_keys(f"{equipamento_selecionado[index][1]}")
                                            else:
                                                text_field.send_keys(f"{equipamento_selecionado[index][1][1]}")
                                            
                                    if question['id'] == 1980616:
                                        if int(equipamento_selecionado[index][0].split()[0]) < 36:
                                            text_field.send_keys(f"{equipamento_selecionado[index][1]}")
                                        else:
                                            if equipamento_selecionado[index][0].split()[1] == '220':
                                                text_field.send_keys(f"{equipamento_selecionado[index][1]}")
                                            else:
                                                text_field.send_keys(f"{equipamento_selecionado[index][1][0]}")
                                    
                                    if question['id'] == 1980619:
                                        min =float(dados_equipamento[equipamento_selecionado[index][0]]['evaporador_inf'])
                                        max = float(dados_equipamento[equipamento_selecionado[index][0]]['evaporador_sup'])
                                        result = random.uniform(min, max)
                                        result = locale.format_string("%.1f", result, grouping=True)
                                        text_field.send_keys(f"{result}")
                                    
                                    if question['id'] == 1980620:
                                        min =float(dados_equipamento[equipamento_selecionado[index][0]]['condensador inferior'])
                                        max = float(dados_equipamento[equipamento_selecionado[index][0]]['condensador superior'])
                                        result = random.uniform(min, max)
                                        result = locale.format_string("%.1f", result, grouping=True)
                                        text_field.send_keys(f"{result}")
                                    
                                    if question['id'] == 1980621:
                                        min =float(dados_equipamento[equipamento_selecionado[index][0]]['compressor inferior'])
                                        max = float(dados_equipamento[equipamento_selecionado[index][0]]['compressor superior'])
                                        result = random.uniform(min, max)
                                        result = locale.format_string("%.1f", result, grouping=True)
                                        text_field.send_keys(f"{result}")
                                        
                                    if question['id'] == 1980625:
                                        min =int(dados_equipamento[equipamento_selecionado[index][0]]['T descarga_inf'])
                                        max = int(dados_equipamento[equipamento_selecionado[index][0]]['T descarga_sup'])
                                        result = random.randint(min, max)
                                        text_field.send_keys(f"{result}")
                                    
                                    if question['id'] == 1980626:
                                        min =int(dados_equipamento[equipamento_selecionado[index][0]]['T sucção_inf'])
                                        max = int(dados_equipamento[equipamento_selecionado[index][0]]['T sucção_sup'])
                                        result = random.randint(min, max)
                                        text_field.send_keys(f"{result}")
                                        
                                    if question['id'] == 1980627:
                                        text_field.send_keys(f"{0}")
                                    
                                    if question['id'] == 1980628:
                                        min =int(dados_equipamento[equipamento_selecionado[index][0]]['410 P alta_inf'])
                                        max = int(dados_equipamento[equipamento_selecionado[index][0]]['410 P alta_sup'])
                                        result = random.randint(min, max)
                                        text_field.send_keys(f"{result}")
                                    
                                    if question['id'] == 2468823:
                                        min =int(dados_equipamento[equipamento_selecionado[index][0]]['410 P baixa_inf'])
                                        max = int(dados_equipamento[equipamento_selecionado[index][0]]['410 P baixa_sup'])
                                        result = random.randint(min, max)
                                        text_field.send_keys(f"{result}")
                                
                                            

            
        



    

driver = get_site()
editar(driver)
input()
driver.quit()
#end_time = time.time()  # End timer
#print(f"Time taken: {end_time - start_time:.6f} seconds")