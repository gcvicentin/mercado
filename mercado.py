from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException

# Configure options and initialize the WebDriver only once
options = Options()
options.page_load_strategy = 'normal'
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
driver.get("https://www.confianca.com.br")
driver.maximize_window()

# Criar objeto de espera explícita
wait = WebDriverWait(driver, 10)

# FECHA A TELA BEM VINDO #TODO: TENTAR USAR element_attibute_to_include - alt="close"
try:
    # Espera o elemento de fechamento estar clicável
    welcome_close = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//*[@id='root']/header/section/div[3]/div/div/div[1]/img"))
    )
    welcome_close.click()
except TimeoutException:
    print("Modal de boas-vindas não encontrado")
except StaleElementReferenceException:
    # Se o elemento estiver obsoleto, aguarda novamente e tenta clicar
    try:
        welcome_close = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='root']/header/section/div[3]/div/div/div[1]/img"))
        )
        welcome_close.click()
    except Exception as e:
        print("Erro ao fechar modal de boas-vindas:", e)

# CLICA EM BEBIDAS
try:
    bebidas_link = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//span[text()='Bebidas']"))
    )
    bebidas_link.click()
except TimeoutException:
    print("Link de Bebidas não encontrado")

# Espera os produtos carregarem
try:
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "h3")))
except TimeoutException:
    print("Produtos não carregados")

# Encontra os elementos dos produtos e processa os textos
produtos = driver.find_elements(By.TAG_NAME, "h3")   # TODO: FAZER UM SCROLL DOWN PARA CARREGAR TODOS OS PRODUTOS
# TODO: PAGINAÇÃO
# TODO: INCLUIR JÁ NA FORMA DE DICIONARIO

meus_produtos = []
meus_preços = []

for produto in produtos:
    meus_produtos.append(produto.text)
    
precos = driver.find_elements(By.CLASS_NAME, "product-shelf__price-current")
for preco in precos:
    meus_preços.append(preco.text)
    
print(meus_produtos, meus_preços)

driver.quit()