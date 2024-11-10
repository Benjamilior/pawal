#Codigo para sacar el precio de producto donde la pagina no tiene boton 
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.oauth2 import service_account
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
import pandas as pd
import json
import datetime
#Google Sheets
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
KEY = 'key.json'
SPREADSHEET_ID = '1VU3_P_EqdSJzabp1eCpNdoyVP7LQfs8FkHkwFabac5A'
creds = None
creds = service_account.Credentials.from_service_account_file(KEY, scopes=SCOPES)
service = build('sheets', 'v4', credentials=creds)
sheet = service.spreadsheets()


#Ejecutador del Codigo

# PATH = "C:\\Program Files (x86)\\chromedriver.exe"
PATH = "/usr/local/bin/chromedriver"
# Configurar las opciones de Chrome
chrome_options = Options()
chrome_options.add_argument("--headless")  # Ver el Navegador
chrome_options.add_argument("--window-size=1920x1080")

start_time = time.time()  # Tiempo de inicio de la ejecución

driver = webdriver.Chrome(options=chrome_options)



sku = {
    "petdotu344": "https://laikamascotas.cl/producto/besties-alimento-puppy-todas-las-razas?sku=7707865304467",
}



results = []

for sku_key, url in sku.items():
    driver.get(url)
    precio_oferta = "No disponible"    
    precio_normal = "No disponible"
    stock= "Con Stock"
    try:
        # Intenta obtener el precio de oferta
        precio_oferta_element = driver.find_element("xpath", '/html/body/div[1]/main/div/div[5]/div/div[2]/div[1]/div[2]/div[1]/div[1]/h1') #Cambiar
        precio_oferta = precio_oferta_element.text  # Guarda el precio de oferta
        stock_element= driver.find_element(By.XPATH,"/html/body/div[1]/main/div/div[5]/div/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]")
        stock=stock_element.text
    except NoSuchElementException:
        pass  # Si no se encuentra el precio de oferta, se continuará con el siguiente bloque de código

    try:
        # Intenta obtener el precio normal
        precio_oferta_element = driver.find_element("xpath", '/html/body/main/section/div/div/div/div/div/section/div[1]/div[1]/div[2]/section/div[1]/div/div[5]/div/form/div[2]/div[1]/span[1]/span[1]') #Cambiar
        precio_oferta = precio_oferta_element.text  # Guarda el precio de oferta
        stock_element= driver.find_element(By.XPATH,"/html/body/main/section/div/div/div/div/div/section/div[1]/div[1]/div[2]/section/div[1]/div/div[2]")
        stock=stock_element.text
    except NoSuchElementException:
        pass  # Si no se encuentra el precio normal, se continuará con el siguiente bloque de código

    if precio_oferta == "No disponible" and precio_normal == "No disponible":
        try:
            precio_oferta_element = driver.find_element("xpath", '/html/body/main/section/div/div/div/div/div/section/div[1]/div[1]/div[2]/section/div[1]/div/div[5]/div/form/div[2]/div[1]/span[1]/span[1]') #Cambiar
            precio_oferta = precio_oferta_element.text  # Guarda el precio de oferta
            stock_element= driver.find_element(By.XPATH,"/html/body/main/section/div/div/div/div/div/section/div[1]/div[1]/div[2]/section/div[1]/div/div[2]")
            stock=stock_element.text
        except NoSuchElementException as e:
            print(f"No se pudo encontrar el precio en la URL {url} - {e}")

    data = {
        "SKU": sku_key,
        "Precio": precio_normal,
        "Precio_oferta": precio_oferta,
        "Stock" :stock
    }
    results.append(data)
    print(data)
    time.sleep(0.5)
driver.quit()

df = pd.DataFrame(results)
print(df)
print(df.head)

driver.quit()

print(results)
end_time = time.time()  # Tiempo de finalización de la ejecución

execution_time = end_time - start_time

print("Tiempo de ejecución: %.2f segundos" % execution_time)
