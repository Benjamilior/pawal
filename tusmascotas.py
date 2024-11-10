
#No olvidarse del key.json
#Buscar todos los "Cambiar" antes de usar
#En chatgpt cruzar sku_dotu con links. Pedir que te haga el json desde el info del sheets
#No olvidarse del key.json
import json
import time
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.oauth2 import service_account

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException

#Google Sheets
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
KEY = 'key.json'
SPREADSHEET_ID = '1VU3_P_EqdSJzabp1eCpNdoyVP7LQfs8FkHkwFabac5A' #Cambiar
creds = None
creds = service_account.Credentials.from_service_account_file(KEY, scopes=SCOPES)
service = build('sheets', 'v4', credentials=creds)
sheet = service.spreadsheets()


# PATH = "C:\\Program Files (x86)\\chromedriver.exe"
PATH = "/usr/local/bin/chromedriver"
# Configurar las opciones de Chrome
chrome_options = Options()
chrome_options.add_argument("--headless")  # Ver el Navegador
chrome_options.add_argument("--window-size=1920x1080")
start_time = time.time()  # Tiempo de inicio de la ejecución
driver = webdriver.Chrome(options=chrome_options)

results = []

sku = {
    "petdotu344": "https://www.tusmascotas.cl/product/hills-jerky-mini-strips-premios-con-pollo-perro/",
    "petdotu360": "https://www.tusmascotas.cl/product/hills-hairball-control-7/",
    "petdotu357": "https://www.tusmascotas.cl/product/hills-hairball-control-317kg/",
    "petdotu361": "https://www.tusmascotas.cl/product/perfect-weight-adult-cat/",
    "petdotu354": "https://www.tusmascotas.cl/product/hills-indoor-age-defying/",
    "petdotu337": "https://www.tusmascotas.cl/product/hills-small-paws-7-2/",
    "petdotu372": "https://www.tusmascotas.cl/product/hills-i-d-digestive-care/",
    "petdotu334": "https://www.tusmascotas.cl/product/hills-active-longevity-perro-7-pellet-pequeno/",
    "petdotu412": "https://www.tusmascotas.cl/product/hills-adult-7-small-bites-2kg/",
    "petdotu411": "https://www.tusmascotas.cl/product/hills-longevity-ob-perro-7-3kg/",
    "petdotu335": "https://www.tusmascotas.cl/product/hills-active-longevity/",
    "petdotu407": "https://www.tusmascotas.cl/product/hills-perfect-weight-raza-pequena/",
    "petdotu410": "https://www.tusmascotas.cl/product/hills-youthful-vitality/",
    "petdotu365": "https://www.tusmascotas.cl/product/hills-adult-ob-15-9kg/",
    "petdotu324": "https://www.tusmascotas.cl/product/hills-adult-small-bites/",
    "petdotu332": "https://www.tusmascotas.cl/product/hills-light-perro-pellet-pequeno/",
    "petdotu340": "https://www.tusmascotas.cl/product/hills-adult-sensitive-stomach-y-skin-mini-1-81kg/",
    "petdotu331": "https://www.tusmascotas.cl/product/hills-small-paws-adulto/",
    "petdotu322": "https://www.tusmascotas.cl/product/hills-light-adulto-razas/",
    "petdotu364": "https://www.tusmascotas.cl/product/hills-adult-original-bites/",
    "petdotu348": "https://www.tusmascotas.cl/product/hills-optimal-care-adult/",
    "petdotu349": "https://www.tusmascotas.cl/product/hills-adult-optimalcare-7-25kg/",
    "petdotu356": "https://www.tusmascotas.cl/product/hills-hairball-control/",
    "petdotu358": "https://www.tusmascotas.cl/product/hills-hairball-control-gato-adulto/",
    "petdotu359": "https://www.tusmascotas.cl/product/hills-hairball-control-light/",
    "petdotu352": "https://www.tusmascotas.cl/product/hills-indoor-gato/",
    "petdotu362": "https://www.tusmascotas.cl/product/hills-sensitive-stomach/",
    "petdotu350": "https://www.tusmascotas.cl/product/hills-light-gato/",
    "petdotu351": "https://www.tusmascotas.cl/product/hills-light-gato-adulto-31kg/",
    "petdotu402": "https://www.tusmascotas.cl/product/hills-urinary-care-s-d-gato-18-kg/",
    "petdotu404": "https://www.tusmascotas.cl/product/hills-gato-indoor-7/",
    "petdotu355": "https://www.tusmascotas.cl/product/hills-youthful-vitality-cat/",
    "petdotu399": "https://www.tusmascotas.cl/product/hills-y-d-thyroid-care-1-81-kg/",
    "petdotu345": "https://www.tusmascotas.cl/product/hills-healthy-development-kitten-1-58kg/",
    "petdotu346": "https://www.tusmascotas.cl/product/healthy-development-kitten/",
    "petdotu347": "https://www.tusmascotas.cl/product/hills-kitten-indoor/",
    "petdotu405": "https://www.tusmascotas.cl/product/hills-c-d-urinary-care-perro-15-kg/",
    "petdotu368": "https://www.tusmascotas.cl/product/hills-c-d-urinary-care-perro-385-kg/",
    "petdotu369": "https://www.tusmascotas.cl/product/hills-urinary-care-c-d-chicken-canino-7-98kg/",
    "petdotu390": "https://www.tusmascotas.cl/product/hills-cd-urinary-care-felino-385kg/",
    "petdotu370": "https://www.tusmascotas.cl/product/hills-h-d-heart-care-perro-1-5kg/",
    "petdotu391": "https://www.tusmascotas.cl/product/hills-digestive-care-i-d/",
    "petdotu373": "https://www.tusmascotas.cl/product/hills-i-d-digestive-care-3/",
    "petdotu374": "https://www.tusmascotas.cl/product/hills-i-d-digestive-care-2/",
    "petdotu371": "https://www.tusmascotas.cl/product/hills-i-d-low-fat-digestive-care-3-85kg/",
    "petdotu375": "https://www.tusmascotas.cl/product/hills-jd-joint-care/",
    "petdotu377": "https://www.tusmascotas.cl/product/hills-kidney-care-kd/",
    "petdotu378": "https://www.tusmascotas.cl/product/hills-kidney-care-kd-385kg/",
    "petdotu379": "https://www.tusmascotas.cl/product/hills-kidney-care-k-d-perro-7-9-kg/",
    "petdotu392": "https://www.tusmascotas.cl/product/hills-kidney-care-kd-gato-18-kg/",
    "petdotu393": "https://www.tusmascotas.cl/product/hills-kidney-care-kd-gato/",
    "petdotu380": "https://www.tusmascotas.cl/product/hills-i-d-liver-care-7-98-kg/",
    "petdotu384": "https://www.tusmascotas.cl/product/hills-metabolic-weight-management-2/",
    "petdotu385": "https://www.tusmascotas.cl/product/hills-metabolic-weight-management/",
    "petdotu394": "https://www.tusmascotas.cl/product/hills-metabolic-felino/",
    "petdotu395": "https://www.tusmascotas.cl/product/hills-metabolic-felino-38kg/",
    "petdotu396": "https://www.tusmascotas.cl/product/hills-metabolic-urinary-2-88-kg/",
    "petdotu381": "https://www.tusmascotas.cl/product/hills-r-d-canino-1-5kg/",
    "petdotu382": "https://www.tusmascotas.cl/product/hills-r-d-canino/",
    "petdotu397": "https://www.tusmascotas.cl/product/hills-r-d-weight-reduction/",
    "petdotu386": "https://www.tusmascotas.cl/product/hills-u-d-urinary-care-perro-3-85kg/",
    "petdotu387": "https://www.tusmascotas.cl/product/hills-w-d-multibenefit/",
    "petdotu389": "https://www.tusmascotas.cl/product/hills-zd-canino/",
    "petdotu401": "https://www.tusmascotas.cl/product/hills-z-d-gato-skin-food-sensitive/",
    "petdotu326": "https://www.tusmascotas.cl/product/hills-puppy-original-bites/",
    "petdotu320": "https://www.tusmascotas.cl/product/hills-healthy-development-puppy-small-bites-204-kg/",
    "petdotu329": "https://www.tusmascotas.cl/product/hills-puppy-small-bites-healthy-development-703-kg/",
    "petdotu328": "https://www.tusmascotas.cl/product/hills-small-paws-puppy-204kg/",
    "petdotu339": "https://www.tusmascotas.cl/product/hills-youthful-vitality-small-y-mini-adult-7-5-6kg/",
    "petdotu338": "https://www.tusmascotas.cl/product/hills-youthful-vitality-razas-pequenas-y-mini-1-58-kg/",
    "petdotu432": "https://www.tusmascotas.cl/product/proplan-sensitive-and-stomach-razas-pequenas-7-5kg/",
    "petdotu430": "https://www.tusmascotas.cl/product/proplan-sensitive-and-stomach-razas-medianas-15kg/",
    "petdotu426": "https://www.tusmascotas.cl/product/pro-plan-sensitive/#",
    "petdotu425": "https://www.tusmascotas.cl/product/proplan-perro-sensitive-cordero-arroz/",
    "petdotu457": "https://www.tusmascotas.cl/product/pro-plan-adult-cat-3kg/",
    "petdotu435": "https://www.tusmascotas.cl/product/pro-plan-reducido-en-calorias-perro-3-kg/",
    "petdotu434": "https://www.tusmascotas.cl/product/pro-plan-reducido-en-calorias-perro-15-kg/",
    "petdotu428": "https://www.tusmascotas.cl/product/proplan-sensitive-skin-salmon-arroz/",
    "petdotu427": "https://www.tusmascotas.cl/product/pro-plan-perro-sensitive-skin-salmon-y-arroz-15-kg/",
    "petdotu429": "https://www.tusmascotas.cl/product/sensitive-skin-dog-2/",
    "petdotu437": "https://www.tusmascotas.cl/product/pro-plan-adult-dog-razas-medianas-3kg/",
    "petdotu415": "https://www.tusmascotas.cl/product/pro-plan-adult-dog-razas-medianas-15kg/",
    "petdotu438": "https://www.tusmascotas.cl/product/pro-plan-perro-adulto-razas-pequenas-3-kg/",
    "petdotu417": "https://www.tusmascotas.cl/product/pro-plan-perro-adulto-razas-pequenas-75-kg/",
    "petdotu441": "https://www.tusmascotas.cl/product/pro-plan-exigent-dog-small-breed-3kg/",
    "petdotu440": "https://www.tusmascotas.cl/product/exigent-dog-small-breed-7-5kg-pro-plan/",
    "petdotu448": "https://www.tusmascotas.cl/product/pro-plan-puppy-razas-pequenas-3-kg/",
    "petdotu447": "https://www.tusmascotas.cl/product/pro-plan-puppy-razas-pequenas-75-kg/",
    "petdotu431": "https://www.tusmascotas.cl/product/proplan-sensitive-and-stomach-razas-medianas-3kg/",
    "petdotu436": "https://www.tusmascotas.cl/product/pro-plan-reducido-en-calorias-razas-pequenas-3kg/",
    "petdotu433": "https://www.tusmascotas.cl/product/proplan-sensitive-and-stomach-razas-pequenas-3kg/",
    "petdotu416": "https://www.tusmascotas.cl/product/adult-vitality-razas-grandes/",
    "petdotu462": "https://www.tusmascotas.cl/product/adult-cat-7/",
    "petdotu456": "https://www.tusmascotas.cl/product/pro-plan-adult-cat-75-kg/",
    "petdotu453": "https://www.tusmascotas.cl/product/proplan-gato-adulto-live-clear-1kg/",
    "petdotu452": "https://www.tusmascotas.cl/product/proplan-gato-adulto-live-clear-3kg/",
    "petdotu455": "https://www.tusmascotas.cl/product/proplan-urinary-cat/",
    "petdotu454": "https://www.tusmascotas.cl/product/proplan-urinary-cat-7-5kg/",
    "petdotu451": "https://www.tusmascotas.cl/product/pro-plan-kitten-1-kg/",
    "petdotu450": "https://www.tusmascotas.cl/product/pro-plan-kitten-3-kg/",
    "petdotu449": "https://www.tusmascotas.cl/product/pro-plan-kitten-75-kg/",
    "petdotu461": "https://www.tusmascotas.cl/product/pro-plan-reduced-calorie-cat-3-kg/",
    "petdotu460": "https://www.tusmascotas.cl/product/pro-plan-sterilized-cat-3-kg/",
    "petdotu459": "https://www.tusmascotas.cl/product/pro-plan-sterilized-cat-75-kg/",
    "petdotu418": "https://www.tusmascotas.cl/product/pro-plan-puppy-razas-grandes-15-kg/",
    "petdotu446": "https://www.tusmascotas.cl/product/pro-plan-puppy-complete-3-kg/",
    "petdotu444": "https://www.tusmascotas.cl/product/puppy-complete-pro-plan/",
    "petdotu424": "https://www.tusmascotas.cl/product/sensitive-skin-dog/",
    "petdotu423": "https://www.tusmascotas.cl/product/sensitive-skin-dog-cordero-y-arroz-puppy-pro-plan-15kg/",
    "petdotu422": "https://www.tusmascotas.cl/product/proplan-active-mind-7-raza-media-y-grande/",
    "petdotu421": "https://www.tusmascotas.cl/product/pro-plan-active-mind-7-razas-medianas-y-grandes-15-kg/",
    "petdotu443": "https://www.tusmascotas.cl/product/pro-plan-active-mind-7-razas-pequenas-3-kg/",
    "petdotu442": "https://www.tusmascotas.cl/product/pro-plan-active-mind-7-razas-pequenas-75-kg/",
    "petdotu303": "https://www.tusmascotas.cl/product/royal-canin-medium-junior-perro/",
    "petdotu310": "https://www.tusmascotas.cl/product/royal-canin-sensible/",
    "petdotu302": "https://www.tusmascotas.cl/product/royal-canin-medium-adulto/",
    "petdotu309": "https://www.tusmascotas.cl/product/royal-canin-exigent-felino/",
    "petdotu311": "https://www.tusmascotas.cl/product/royal-canin-hairball-care/",
    "petdotu307": "https://www.tusmascotas.cl/product/royal-canin-indoor/",
    "petdotu300": "https://www.tusmascotas.cl/product/royal-canin-maxi-adulto-perro/",
    "petdotu301": "https://www.tusmascotas.cl/product/royal-canin-maxi-puppy-perro/",
    "petdotu318": "https://www.tusmascotas.cl/product/royal-canin-persian/",
    "petdotu319": "https://www.tusmascotas.cl/product/poodle-adulto-royal-canin/",
    "petdotu313": "https://www.tusmascotas.cl/product/royal-canin-urinary-care-gato-15-kg/",
    "petdotu316": "https://www.tusmascotas.cl/product/royal-canin-urinary-care-gato-75-kg/",
    "petdotu314": "https://www.tusmascotas.cl/product/royal-canin-urinary-s-o-cat-7-5kg/",
    "petdotu600":"https://www.tusmascotas.cl/product/leonardo-adulto-grain-free-4"
}
sku2 = {"petdotu1": "https://www.tusmascotas.cl/product/apoquel-16mg-oclacitinib/"}
results = []

for sku_key, url in sku.items():
    driver.get(url)
    precio_oferta = "No disponible"
    precio_normal = "No disponible"
    stock= "Con Stock"
    try:
        # Intenta obtener el precio de oferta
        precio_oferta_element = driver.find_element("xpath", '/html/body/div[1]/div[1]/div/div/div/div[2]/div[1]/div[2]/div/div/div[2]/div/p[1]/ins/span') #Cambiar
        precio_oferta = precio_oferta_element.text  # Guarda el precio de oferta
        stock_element= driver.find_element(By.XPATH,"/html/body/div[1]/div[1]/div/div/div/div[2]/div[1]/div[2]/div/div/div[2]/div/p[2]")
        stock = stock_element.text
    except NoSuchElementException:
        pass  # Si no se encuentra el precio de oferta, se continuará con el siguiente bloque de código

    try:
        # Intenta obtener el precio normal
        precio_normal_element = driver.find_element("xpath", '/html/body/div[1]/div[1]/div/div/div/div[2]/div[1]/div[2]/div/div/div[2]/div/p[1]/del/span[2]') #Cambiar
        precio_normal = precio_normal_element.text  # Guarda el precio normal
        stock_element= driver.find_element(By.XPATH,"/html/body/div[1]/div[1]/div/div/div/div[2]/div[1]/div[2]/div/div/div[2]/div/p[2]")
        stock = stock_element.text
    except NoSuchElementException:
        pass  # Si no se encuentra el precio normal, se continuará con el siguiente bloque de código

    if precio_oferta == "No disponible" and precio_normal == "No disponible":
        try:
            # Si no se puede encontrar ni el precio de oferta ni el precio normal, intenta con el tercer XPath
            precio_normal_element = driver.find_element("xpath", '/html/body/div[1]/div[1]/div/div/div/div[2]/div[1]/div[2]/div/div/div[2]/div/p[1]/span[2]') #Cambiar
            precio_normal = precio_normal_element.text  # Guarda el precio normal
            stock_element= driver.find_element(By.XPATH,"/html/body/div[1]/div[1]/div/div/div/div[2]/div[1]/div[2]/div/div/div[2]/div/p[2]")
            stock = stock_element.text
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

# Guardar el DataFrame en un archivo Excel
# nombre_archivo = "datos_productos.xlsx"  # Nombre del archivo Excel
# df.to_excel(nombre_archivo, index=False)  # El parámetro index=False evita que se incluyan los índices en el archivo Excel
# print(f"Datos guardados en {nombre_archivo}")


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
							range='tusmascotas!k2',#CAMBIAR
							valueInputOption='USER_ENTERED',
							body={'values':values}).execute()


#Valores que se pasan a Sheets
values = [[item['SKU'], item['Precio'],item['Precio_oferta']] for item in results]
result = sheet.values().update(spreadsheetId=SPREADSHEET_ID,
							range='tusmascotas!A2:E',#CAMBIAR
							valueInputOption='USER_ENTERED',
							body={'values':values}).execute()
print(f"Datos insertados correctamente")

#Valores que se pasan a Sheets
values = [[item['Stock']] for item in results]
result = sheet.values().update(spreadsheetId=SPREADSHEET_ID,
							range='tusmascotas!M2:N',#CAMBIAR
							valueInputOption='USER_ENTERED',
							body={'values':values}).execute()
print(f"Datos insertados correctamente")


df = pd.DataFrame(results)
print(df)
print(df.head)


competitor = "Tus Mascotas"  # Cambiar 
# Enviar datos a otro Google Sheets
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
KEY = 'key.json'
NEW_SPREADSHEET_ID = '1Yn7Ze_WQJ19s-PmbaeLsTFaehygu3jSHaMvrxcfbneU'  #CAMBIAR

creds = service_account.Credentials.from_service_account_file(KEY, scopes=SCOPES)
service = build('sheets', 'v4', credentials=creds)
sheet = service.spreadsheets()

# Obtener la última fila con datos en la nueva hoja
result = sheet.values().get(spreadsheetId=NEW_SPREADSHEET_ID, range='historico!A:A').execute() #Cambiar donde llega la info
values = result.get('values', [])
last_row = len(values) + 1  # Obtener el índice de la última fila vacía

# Convertir resultados a la lista de valores
values = [[row['SKU'], competitor,row['Precio'],row['Precio_oferta'], now_str] for _, row in df.iterrows()]

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
result = sheet.values().get(spreadsheetId=NEW_SPREADSHEET_ID, range='stock!A:A').execute()  # Cambiar donde llega la info
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
