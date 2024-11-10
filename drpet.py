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
    "petdotu430": "https://www.drpet.cl/alimento-seco/245-1008-proplan-dog-stomach-mb-gr-alimento-para-perro.html#/22-tamano_producto-15_kg",
    
    "petdotu457": "https://www.drpet.cl/alimento-seco/207-909-proplan-cat-adulto-alimento-para-gato.html#/15-tamano_producto-3_kg",
    "petdotu434": "https://www.drpet.cl/alimento-seco/234-661-proplan-dog-adulto-red-c-m-l15-kg-alimento-para-perro.html#/22-tamano_producto-15_kg",
    "petdotu428": "https://www.drpet.cl/alimento-seco/1260-1006-proplan-dog-sens-adult-salm-sb-3kg-alimento-para-perro.html#/15-tamano_producto-3_kg",
    "petdotu427": "https://www.drpet.cl/alimento-seco/1260-1007-proplan-dog-sens-adult-salm-sb-3kg-alimento-para-perro.html#/22-tamano_producto-15_kg",
    "petdotu429": "https://www.drpet.cl/alimento-seco/244-664-proplan-dog-sens-adult-salm-sb-3kg-alimento-para-perro.html#/15-tamano_producto-3_kg",
    "petdotu437": "https://www.drpet.cl/alimento-seco/231-829-proplan-dog-adulto-m-b-15-kg-alimento-para-perro.html#/15-tamano_producto-3_kg",
    "petdotu415": "https://www.drpet.cl/alimento-seco/231-658-proplan-dog-adulto-m-b-15-kg-alimento-para-perro.html#/22-tamano_producto-15_kg",
    "petdotu438": "https://www.drpet.cl/alimento-seco/236-137-proplan-dog-adulto-sb-alimento-para-perro.html#/15-tamano_producto-3_kg",
    "petdotu417": "https://www.drpet.cl/alimento-seco/236-136-proplan-dog-adulto-sb-alimento-para-perro.html#/12-tamano_producto-75_kg",
    "petdotu441": "https://www.drpet.cl/alimento-seco/229-135-proplan-dog-adulto-exigent-sb-alimento-para-perro.html#/15-tamano_producto-3_kg",
    "petdotu440": "https://www.drpet.cl/alimento-seco/229-134-proplan-dog-adulto-exigent-sb-alimento-para-perro.html#/12-tamano_producto-75_kg",
    "petdotu448": "https://www.drpet.cl/alimento-seco/240-143-proplan-dog-cachorro-sb-alimento-para-perro.html#/15-tamano_producto-3_kg",
    "petdotu447": "https://www.drpet.cl/alimento-seco/240-142-proplan-dog-cachorro-sb-alimento-para-perro.html#/12-tamano_producto-75_kg",
    "petdotu431": "https://www.drpet.cl/alimento-seco/245-665-proplan-dog-stomach-mb-gr-alimento-para-perro.html#/15-tamano_producto-3_kg",
    "petdotu416": "https://www.drpet.cl/alimento-seco/230-653-proplan-dog-adulto-l-b-15-kg-alimento-para-perro.html#/22-tamano_producto-15_kg",
    "petdotu462": "https://www.drpet.cl/alimento-seco/208-649-proplan-cat-adulto-senior-x-3kg-alimento-para-gato.html#/15-tamano_producto-3_kg",
    "petdotu456": "https://www.drpet.cl/alimento-seco/207-910-proplan-cat-adulto-alimento-para-gato.html#/12-tamano_producto-75_kg",
    "petdotu452": "https://www.drpet.cl/alimento-seco/210-proplan-cat-live-clear-alimento-para-gato-7613287119629.html",
    "petdotu455": "https://www.drpet.cl/alimento-seco/221-130-proplan-cat-urinary-alimento-para-gato.html#/15-tamano_producto-3_kg",
    "petdotu454": "https://www.drpet.cl/alimento-seco/221-129-proplan-cat-urinary-alimento-para-gato.html#/12-tamano_producto-75_kg",
    "petdotu451": "https://www.drpet.cl/alimento-seco/209-911-proplan-cat-kitte-alimento-para-gato.html#/2-tamano_producto-1_kg",
    "petdotu450": "https://www.drpet.cl/alimento-seco/209-122-proplan-cat-kitte-alimento-para-gato.html#/15-tamano_producto-3_kg",
    "petdotu449": "https://www.drpet.cl/alimento-seco/209-121-proplan-cat-kitte-alimento-para-gato.html#/12-tamano_producto-75_kg",
    "petdotu460": "https://www.drpet.cl/alimento-seco/220-128-proplan-cat-sterilized-alimento-para-gato.html#/15-tamano_producto-3_kg",
    "petdotu459": "https://www.drpet.cl/alimento-seco/220-127-proplan-cat-sterilized-alimento-para-gato.html#/12-tamano_producto-75_kg",
    "petdotu418": "https://www.drpet.cl/alimento-seco/237-663-proplan-dog-cachorro-lb-15-kg-alimento-para-perro.html#/22-tamano_producto-15_kg",
    "petdotu446": "https://www.drpet.cl/alimento-seco/239-140-proplan-dog-cachorro-mb-alimento-para-perro.html#/15-tamano_producto-3_kg",
    "petdotu444": "https://www.drpet.cl/alimento-seco/239-139-proplan-dog-cachorro-mb-alimento-para-perro.html#/22-tamano_producto-15_kg",
    "petdotu421": "https://www.drpet.cl/alimento-seco/226-654-proplan-dog-active-mind-15-kg-alimento-para-perro.html#/22-tamano_producto-15_kg",
    "petdotu443": "https://www.drpet.cl/alimento-seco/228-133-proplan-dog-active-mind-sb-alimento-para-perro.html#/15-tamano_producto-3_kg",
    "petdotu442": "https://www.drpet.cl/alimento-seco/228-132-proplan-dog-active-mind-sb-alimento-para-perro.html#/12-tamano_producto-75_kg",
    "petdotu302": "https://www.drpet.cl/alimento-seco/351-512-royal-dog-medium-adult-alimento-para-perro.html#/22-tamano_producto-15_kg",
    "petdotu309": "https://www.drpet.cl/alimento-seco/292-678-royal-cat-exigent-15-kg-alimento-para-gato.html#/24-tamano_producto-15_kg",
    "petdotu308": "https://www.drpet.cl/alimento-seco/293-175-royal-cat-fit-32-alimento-para-gato.html#/12-tamano_producto-75_kg",
    "petdotu311": "https://www.drpet.cl/alimento-seco/298-681-royal-cat-hairball-care-15-kg-alimento-para-gato.html#/24-tamano_producto-15_kg",
    "petdotu307": "https://www.drpet.cl/alimento-seco/1259-1005-royal-cat-indoor-alimento-para-gato.html#/12-tamano_producto-75_kg",
    "petdotu300": "https://www.drpet.cl/alimento-seco/347-696-royal-dog-maxi-adult-15-kg-alimento-para-perro.html#/22-tamano_producto-15_kg",
    "petdotu301": "https://www.drpet.cl/alimento-seco/350-698-royal-dog-maxi-puppy-15-kg-alimento-para-perro.html#/22-tamano_producto-15_kg",
    "petdotu304": "https://www.drpet.cl/alimento-seco/353-197-royal-dog-mini-adulto-alimento-para-perro.html#/12-tamano_producto-75_kg",
    "petdotu305": "https://www.drpet.cl/alimento-seco/359-201-royal-dog-mini-puppy-alimento-para-perro.html#/12-tamano_producto-75_kg",
    "petdotu318": "https://www.drpet.cl/alimento-seco/314-686-royal-cat-raza-persian-30-x-15-kg-alimento-para-gato.html#/24-tamano_producto-15_kg",
    "petdotu303": "https://www.drpet.cl/alimento-seco/351-512-royal-dog-medium-adult-alimento-para-perro.html#/22-tamano_producto-15_kg",
    "petdotu313": "https://www.drpet.cl/alimento-seco/327-184-royal-cat-urinary-care-alimento-para-gato.html#/24-tamano_producto-15_kg",
    "petdotu316": "https://www.drpet.cl/alimento-seco/327-183-royal-cat-urinary-care-alimento-para-gato.html#/12-tamano_producto-75_kg",
    "petdotu600":"https://www.drpet.cl/alimento-seco/81-42-leonardo-adulto-maxi-alimento-para-gato-libre-de-granos.html#/12-tamano_producto-75_kg"
}
sku2 = {"petdotu1": "https://puntomascotas.cl/cicatrizantes/37170-apoquel-16-mg-x-20-comprimidos-5414736044217.html"}


results = []
button_clicked = False  # Bandera para controlar si el botón ya fue presionado

for sku_key, url in sku.items():
    driver.get(url)
    time.sleep(1)

    if not button_clicked:
        try:
            button = driver.find_element(By.XPATH, "//button[contains(text(), 'Elegir') and contains(@class, 'sbs_selectStore')][1]")
            button.click()
            button_clicked = True  # Marcar que el botón ya fue presionado
            # time.sleep(5)
        except NoSuchElementException:
            print("Botón 'Elegir' no encontrado")
            pass

    precio_oferta = "No disponible"    
    precio_normal = "No disponible"
    stock= "Con Stock"
    
    try:
        # Intenta obtener el precio de oferta
        precio_oferta_element = driver.find_element("xpath", '/html/body/main/section/div/div/section/div[1]/div[2]/div[1]/div[2]/div/span[1]') #Cambiar
        precio_oferta = precio_oferta_element.text  # Guarda el precio de oferta
        stock_element= driver.find_element(By.XPATH,"-")
        stock = stock_element.text
    except NoSuchElementException:
        pass  # Si no se encuentra el precio de oferta, se continuará con el siguiente bloque de código

    try:
        # Intenta obtener el precio normal
        precio_normal_element = driver.find_element("xpath", '/html/body/main/section/div/div/section/div[1]/div[2]/div[1]/div[1]/div') #Cambiar
        precio_normal = precio_normal_element.text  # Guarda el precio normal
        stock_element= driver.find_element(By.XPATH,"/html/body/main/section/div/div/div/div/div/section/div[1]/div[1]/div[2]/section/div[1]/div/div[2]")
        stock = stock_element.text
    except NoSuchElementException:
        pass  # Si no se encuentra el precio normal, se continuará con el siguiente bloque de código

    if precio_oferta == "No disponible" and precio_normal == "No disponible":
        try:
            precio_oferta_element = driver.find_element("xpath", '/html/body/main/section/div/div/div/div/div/section/div[1]/div[1]/div[2]/section/div[1]/div/div[5]/div/form/div[2]/div[1]/span[1]/span[1]') #Cambiar
            precio_oferta = precio_oferta_element.text  # Guarda el precio de oferta
            stock_element= driver.find_element(By.XPATH,"/html/body/main/section/div/div/div/div/div/section/div[1]/div[1]/div[2]/section/div[1]/div/div[2]")
            stock = stock_element.text
        except NoSuchElementException as e:
            print(f"No se pudo encontrar el precio en la URL {url} - {e}")

    data = {
        "SKU": sku_key,
        "Precio": precio_normal,
        "Precio_oferta": precio_oferta,
        "Stock": stock
    }
    results.append(data)
    print(data)
    time.sleep(0.5)

driver.quit()

df = pd.DataFrame(results)
print(df)
print(df.head())

print(results)
end_time = time.time()  # Tiempo de finalización de la ejecución

execution_time = end_time - start_time

print("Tiempo de ejecución: %.2f segundos" % execution_time)


      
#Fecha de Extraccion
now = datetime.datetime.now()
now_str = now.strftime('%Y-%m-%d %H:%M:%S')
data = {"":now_str}
json_data = json.dumps(data)
values = [[json_data]]
result = sheet.values().update(spreadsheetId=SPREADSHEET_ID,
							range='drpet!K2',#CAMBIAR
							valueInputOption='USER_ENTERED',
							body={'values':values}).execute()


#Valores que se pasan a Sheets
values = [[item['SKU'], item['Precio'],item['Precio_oferta']] for item in results]
result = sheet.values().update(spreadsheetId=SPREADSHEET_ID,
							range='drpet!A2:C',#CAMBIAR
							valueInputOption='USER_ENTERED',
							body={'values':values}).execute()
print(f"Datos insertados correctamente")        

#Valores que se pasan a Sheets
values = [[item['Stock']] for item in results]
result = sheet.values().update(spreadsheetId=SPREADSHEET_ID,
							range='drpet!M2:N',#CAMBIAR
							valueInputOption='USER_ENTERED',
							body={'values':values}).execute()
print(f"Datos insertados correctamente")        


competitor = "dr pet"  # Cambiar 
# # Enviar datos a otro Google Sheets
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
KEY = 'key.json'
NEW_SPREADSHEET_ID = '1Yn7Ze_WQJ19s-PmbaeLsTFaehygu3jSHaMvrxcfbneU'  # ID de la nueva hoja de cálculo

creds = service_account.Credentials.from_service_account_file(KEY, scopes=SCOPES)
service = build('sheets', 'v4', credentials=creds)
sheet = service.spreadsheets()

# Obtener la última fila con datos en la nueva hoja
result = sheet.values().get(spreadsheetId=NEW_SPREADSHEET_ID, range='historico!A:A').execute() #Cambiar donde llega la info
values = result.get('values', [])
last_row = len(values) + 1  # Obtener el índice de la última fila vacía

# Convertir resultados a la lista de valores
values = [[row['SKU'], competitor,row['Precio'], row['Precio_oferta'], now_str] for _, row in df.iterrows()]

# Insertar los resultados en la nueva hoja después de la última fila
update_range = f'historico!A{last_row}:E{last_row + len(values) - 1}' #Cambiar
result = sheet.values().update(
    spreadsheetId=NEW_SPREADSHEET_ID,
    range=update_range,
    valueInputOption='USER_ENTERED',
    body={'values': values}
).execute()

print(f"Datos insertados correctamente en la nueva hoja de Google Sheets en el rango {update_range}")
# Obtener la última fila con datos en la nueva hoja
result = sheet.values().get(spreadsheetId=NEW_SPREADSHEET_ID, range='Stock!A:A').execute()  # Cambiar donde llega la info
values = result.get('values', [])
last_row = len(values) + 1  # Obtener el índice de la última fila vacía
# Convertir resultados a la lista de valores
values = [[now_str, competitor,row['SKU'], row['Stock']] for _, row in df.iterrows()]

# Insertar los resultados en la nueva hoja después de la última fila
print(values)
update_range = f'Stock!A{last_row}:E{last_row + len(values) - 1}'  # Cambiar
result = sheet.values().update(
    spreadsheetId=NEW_SPREADSHEET_ID,
    range=update_range,
    valueInputOption='USER_ENTERED',
    body={'values': values}
).execute()

# MANDAR DATOS A LA API ----------------------------------------------------------------------------------------------------
SPREADSHEET_ID_API = '1S8jzZl4UehXDJxWuHfTSLftBnq3CKUXhgRGrJIShyhE'  
# Obtener la última fila con datos en la nueva hoja
result = sheet.values().get(spreadsheetId=SPREADSHEET_ID_API, range='apipets!A:A').execute() #Cambiar donde llega la info
values = result.get('values', [])
last_row = len(values) + 1  # Obtener el índice de la última fila vacía

# Convertir resultados a la lista de valores
values = [[row['SKU'], competitor, row['Precio'], row['Precio_oferta'], "Algo hay"] for _, row in df.iterrows()]

# Insertar los resultados en la nueva hoja después de la última fila
update_range = f'apipets!A{last_row}:E{last_row + len(values) - 1}' #Cambiar
result = sheet.values().update(
    spreadsheetId=SPREADSHEET_ID_API,
    range=update_range,
    valueInputOption='USER_ENTERED',
    body={'values': values}
).execute()
