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
    "petdotu360": "https://razaspet.cl/producto/hills-gato-7-hair-ball-control-1-59kg/",
    "petdotu357": "https://razaspet.cl/producto/hills-gato-adulto-hairball-control/?attribute_pa_peso=3.17kg",
    "petdotu354": "https://razaspet.cl/producto/hills-gato-adulto-11-indoor-age-1-5kg/",
    "petdotu337": "https://razaspet.cl/producto/hills-perro-adulto-7-mature-toy-breed2-04kg/",
    "petdotu341": "https://razaspet.cl/producto/hills-perro-adulto-sensitive-stomach-skin/",
    "petdotu409": "https://razaspet.cl/producto/hills-gato-adulto-perfect-digestion-1-6-1-58kg/",
    "petdotu372": "https://razaspet.cl/producto/hills-perro-adulto-i-d/",
    "petdotu411": "https://razaspet.cl/producto/hills-perro-adulto-ob/?attribute_pa_peso=3kg",
    "petdotu335": "https://razaspet.cl/producto/hills-perro-adulto-ob/?attribute_pa_peso=2.26kg",
    "petdotu410": "https://razaspet.cl/producto/hills-perro-youthfull-v-adulto-71-8kg/",
    "petdotu323": "https://razaspet.cl/producto/hills-perro-adulto-1-6-small-bites/?attribute_pa_peso=2kg",
    "petdotu324": "https://razaspet.cl/producto/hills-perro-adulto-1-6-small-bites/?attribute_pa_peso=6.8kg",
    "petdotu332": "https://razaspet.cl/producto/hills-perro-adulto-1-6-light-small-bites/?attribute_pa_peso=2.26kg",
    "petdotu333": "https://razaspet.cl/producto/hills-perro-adulto-1-6-light-small-bites/?attribute_pa_peso=6.8kg",
    "petdotu331": "https://razaspet.cl/producto/hills-perro-adulto-1-6-toy-breed-2-04kg/",
    "petdotu322": "https://razaspet.cl/producto/hills-perro-adulto-small-paws-light-2-04kg/",
    "petdotu364": "https://razaspet.cl/producto/hills-perro-adulto-ob/?attribute_pa_peso=6.8kg",
    "petdotu348": "https://razaspet.cl/producto/hills-gato-adulto-1-6-optimal-care/?attribute_pa_peso=3.17kg",
    "petdotu349": "https://razaspet.cl/producto/hills-gato-adulto-1-6-optimal-care/?attribute_pa_peso=7.25kg",
    "petdotu353": "https://razaspet.cl/producto/hills-gato-mature-7-1-81kg/",
    "petdotu356": "https://razaspet.cl/producto/hills-gato-adulto-hairball-control/?attribute_pa_peso=1.58kg",
    "petdotu358": "https://razaspet.cl/producto/hills-gato-adulto-hairball-control/?attribute_pa_peso=7kg",
    "petdotu359": "https://razaspet.cl/producto/hills-gato-adulto-hairball-control-light-3-1kg/",
    "petdotu352": "https://razaspet.cl/producto/hills-gato-adulto-indoor-1-6-1-58kg/",
    "petdotu362": "https://razaspet.cl/producto/hills-gato-adulto-sensitive-stomach-skin-1-58kg/",
    "petdotu351": "https://razaspet.cl/producto/hills-gato-adulto-1-6-light/?attribute_pa_peso=3.17kg",
    "petdotu402": "https://razaspet.cl/producto/hills-gato-adulto-s-d-1-8kg/",
    "petdotu404": "https://razaspet.cl/producto/hills-gato-mature-indoor-7-1-58kg/",
    "petdotu355": "https://razaspet.cl/producto/hills-gato-youthfull-v-adulto-7-1-36kg/",
    "petdotu399": "https://razaspet.cl/producto/hills-gato-adulto-y-d-1-8kg/",
    "petdotu345": "https://razaspet.cl/producto/hills-gato-kitten/?attribute_pa_peso=1.58kg",
    "petdotu346": "https://razaspet.cl/producto/hills-gato-kitten/?attribute_pa_peso=3.17kg",
    "petdotu403": "https://razaspet.cl/producto/hills-gato-kitten-indoor/?attribute_pa_peso=1.58kg",
    "petdotu347": "https://razaspet.cl/producto/hills-gato-kitten-indoor/?attribute_pa_peso=3.17kg",
    "petdotu405": "https://razaspet.cl/producto/hills-gato-c-d-multicare-chicken/?attribute_pa_peso=1.8kg",
    "petdotu368": "https://razaspet.cl/producto/hills-perro-adulto-c-d-multicare-chicken-3-85kg/",
    "petdotu369": "https://razaspet.cl/producto/hills-perro-adulto-c-d-multicare-chicken-7-98kg/",
    "petdotu390": "https://razaspet.cl/producto/hills-gato-c-d-multicare-chicken/?attribute_pa_peso=3.8kg",
    "petdotu370": "https://razaspet.cl/producto/hills-perro-adulto-h-d-1-5kg/",
    "petdotu391": "https://razaspet.cl/producto/hills-gato-i-d-1-81kg/",
    "petdotu373": "https://razaspet.cl/producto/hills-perro-adulto-i-d-low-fast-3-85kg/",
    "petdotu371": "https://razaspet.cl/producto/hills-perro-adulto-i-d-low-fast-3-85kg/",
    "petdotu375": "https://razaspet.cl/producto/hills-perro-adulto-j-d/?attribute_pa_peso=3.8kg",
    "petdotu376": "https://razaspet.cl/producto/hills-perro-adulto-j-d/?attribute_pa_peso=12kg",
    "petdotu377": "https://razaspet.cl/producto/hills-perro-adulto-k-d/?attribute_pa_peso=1.5kg",
    "petdotu378": "https://razaspet.cl/producto/hills-perro-adulto-k-d/?attribute_pa_peso=3.85kg",
    "petdotu379": "https://razaspet.cl/producto/hills-perro-adulto-k-d/?attribute_pa_peso=7.98kg",
    "petdotu392": "https://razaspet.cl/producto/hills-gato-k-d-chicken/?attribute_pa_peso=1.8kg",
    "petdotu393": "https://razaspet.cl/producto/hills-gato-k-d-chicken/?attribute_pa_peso=3.8kg",
    "petdotu380": "https://razaspet.cl/producto/hills-perro-adulto-l-d-7-98kg/",
    "petdotu384": "https://razaspet.cl/producto/hills-perro-adulto-metabolic/",
    "petdotu406": "https://razaspet.cl/producto/hills-perro-metabolic-mobility/",
    "petdotu394": "https://razaspet.cl/producto/hills-gato-adulto-metabolic/",
    "petdotu395": "https://razaspet.cl/producto/hills-gato-adulto-metabolic/?attribute_pa_peso=3.8kg",
    "petdotu396": "https://razaspet.cl/producto/hills-gato-adulto-metabolic-urinary-2-88kg/",
    "petdotu381": "https://razaspet.cl/producto/hills-perro-adulto-r-d/?attribute_pa_peso=1.5kg",
    "petdotu383": "https://razaspet.cl/producto/hills-perro-adulto-r-d/?attribute_pa_peso=7.98kg",
    "petdotu397": "https://razaspet.cl/producto/hills-gato-adulto-r-d/?attribute_pa_peso=1.8kg",
    "petdotu398": "https://razaspet.cl/producto/hills-gato-adulto-r-d/?attribute_pa_peso=3.8kg",
    "petdotu387": "https://razaspet.cl/producto/hills-perro-adulto-w-d/?attribute_pa_peso=1.5kg",
    "petdotu388": "https://razaspet.cl/producto/hills-perro-adulto-w-d/?attribute_pa_peso=7.98kg",
    "petdotu389": "https://razaspet.cl/producto/hills-perro-z-d-ultra-allergen-3-63kg/",
    "petdotu401": "https://razaspet.cl/producto/hills-gato-adulto-z-d-1-81kg/",
    "petdotu325": "https://razaspet.cl/producto/hills-perro-puppy-ob/?attribute_pa_peso=2kg",
    "petdotu326": "https://razaspet.cl/producto/hills-perro-puppy-ob/?attribute_pa_peso=7kg",
    "petdotu320": "https://razaspet.cl/producto/hills-perro-cachorro-small-bites/?attribute_pa_peso=2kg",
    "petdotu329": "https://razaspet.cl/producto/hills-perro-cachorro-small-bites/?attribute_pa_peso=7kg",
    "petdotu328": "https://razaspet.cl/producto/hills-perro-cachorro-toy-breed-2-04kg/",
    "petdotu426": "https://razaspet.cl/producto/pro-plan-perro-cachorro-sensitive-skin-cordero-3kg/",
    "petdotu425": "https://razaspet.cl/producto/pro-plan-perro-sensitive-skin-lamb-rice/?attribute_pa_peso=15kg",
    "petdotu457": "https://razaspet.cl/producto/pro-plan-gato-adulto-1-6/?attribute_pa_peso=3kg",
    "petdotu435": "https://razaspet.cl/producto/pro-plan-perro-reduced-calorie-raza-mediana-grande/?attribute_pa_peso=3kg",
    "petdotu434": "https://razaspet.cl/producto/pro-plan-perro-reduced-calorie-raza-mediana-grande/?attribute_pa_peso=15kg",
    "petdotu428": "https://razaspet.cl/producto/pro-plan-perro-sensitive-skin-salmon-raza-mediana/?attribute_pa_peso=3kg",
    "petdotu427": "https://razaspet.cl/producto/pro-plan-perro-sensitive-skin-salmon-raza-mediana/?attribute_pa_peso=15kg",
    "petdotu429": "https://razaspet.cl/producto/pro-plan-perro-adulto-sensitive-skin-salmon-razas-pequenas-3kg/",
    "petdotu437": "https://razaspet.cl/producto/pro-plan-perro-adulto-optihealth-raza-mediana/?attribute_pa_peso=3kg",
    "petdotu415": "https://razaspet.cl/producto/pro-plan-perro-adulto-optihealth-raza-mediana/?attribute_pa_peso=15kg",
    "petdotu438": "https://razaspet.cl/producto/pro-plan-perro-adulto-1-6-raza-pequena/?attribute_pa_peso=3kg",
    "petdotu417": "https://razaspet.cl/producto/pro-plan-perro-adulto-1-6-raza-pequena/?attribute_pa_peso=7.5kg",
    "petdotu441": "https://razaspet.cl/producto/pro-plan-perro-adulto-exigent-raza-pequena/?attribute_pa_peso=3kg",
    "petdotu440": "https://razaspet.cl/producto/pro-plan-perro-adulto-exigent-raza-pequena/?attribute_pa_peso=7.5kg",
    "petdotu439": "https://razaspet.cl/producto/pro-plan-perro-adulto-1-6-raza-pequena/?attribute_pa_peso=1kg",
    "petdotu448": "https://razaspet.cl/producto/pro-plan-perro-cachorro-raza-pequena/?attribute_pa_peso=3kg",
    "petdotu447": "https://razaspet.cl/producto/pro-plan-perro-cachorro-raza-pequena/?attribute_pa_peso=7.5kg",
    "petdotu436": "https://razaspet.cl/producto/pro-plan-perro-reduced-calorie-raza-mediana-grande/?attribute_pa_peso=3kg",
    "petdotu416": "https://razaspet.cl/producto/pro-plan-perro-adulto-1-6-raza-grande-123kg/",
    "petdotu462": "https://razaspet.cl/producto/pro-plan-gato-7-3kg/",
    "petdotu456": "https://razaspet.cl/producto/pro-plan-gato-adulto-1-6/?attribute_pa_peso=7.5kg",
    "petdotu455": "https://razaspet.cl/producto/pro-plan-gato-urinary-4/?attribute_pa_peso=3kg",
    "petdotu454": "https://razaspet.cl/producto/pro-plan-gato-urinary-4/?attribute_pa_peso=7.5kg",
    "petdotu451": "https://razaspet.cl/producto/pro-plan-gato-sterilized/?attribute_pa_peso=1kg",
    "petdotu450": "https://razaspet.cl/producto/pro-plan-gato-sterilized/?attribute_pa_peso=3kg",
    "petdotu449": "https://razaspet.cl/producto/pro-plan-gato-sterilized/?attribute_pa_peso=7.5kg",
    "petdotu460": "https://razaspet.cl/producto/pro-plan-gato-sterilized/?attribute_pa_peso=3kg",
    "petdotu459": "https://razaspet.cl/producto/pro-plan-gato-sterilized/?attribute_pa_peso=7.5kg",
    "petdotu446": "https://razaspet.cl/producto/pro-plan-perro-cachorro-raza-mediana/?attribute_pa_peso=3kg",
    "petdotu444": "https://razaspet.cl/producto/pro-plan-perro-cachorro-raza-mediana/?attribute_pa_peso=15kg",
    "petdotu424": "https://razaspet.cl/producto/pro-plan-perro-cachorro-sensitive-skin-cordero-3kg/",
    "petdotu423": "https://razaspet.cl/producto/pro-plan-perro-sensitive-skin-lamb-rice-123kg/",
    "petdotu422": "https://razaspet.cl/producto/pro-plan-perro-active-mind-7-raza-mediana-grande-123kg/",
    "petdotu421": "https://razaspet.cl/producto/pro-plan-perro-active-mind-7-raza-mediana-grande-123kg/",
    "petdotu443": "https://razaspet.cl/producto/pro-plan-perro-active-mind-7-raza-pequena/?attribute_pa_peso=3kg",
    "petdotu442": "https://razaspet.cl/producto/pro-plan-perro-active-mind-7-raza-pequena/?attribute_pa_peso=7.5kg",
    "petdotu308": "https://razaspet.cl/producto/royal-canin-gato-fit/?attribute_pa_peso=7-5kg",
    "petdotu317": "https://razaspet.cl/producto/royal-canin-perro-adulto-bulldog-frances/?attribute_pa_peso=7.5kg",
    "petdotu315": "https://razaspet.cl/producto/royal-canin-gato-weight-care-7-5kg/",
    "petdotu303": "https://razaspet.cl/producto/royal-canin-perro-puppy-medium/?attribute_pa_peso=15kg",
    "petdotu310": "https://razaspet.cl/producto/royal-canin-gato-regular-sensible-15kg/",
    "petdotu309": "https://razaspet.cl/producto/royal-canin-gato-adulto-exigent-1-5kg/",
    "petdotu311": "https://razaspet.cl/producto/royal-canin-gato-hairball-care-15kg/",
    "petdotu307": "https://razaspet.cl/producto/royal-canin-gato-indoor/?attribute_pa_peso=7.5kg",
    "petdotu300": "https://razaspet.cl/producto/royal-canin-perro-adulto-maxi-15kg/",
    "petdotu301": "https://razaspet.cl/producto/royal-canin-perro-adulto-maxi-15kg/",
    "petdotu319": "https://razaspet.cl/producto/royal-canin-perro-adulto-caniche-poodle/?attribute_pa_peso=7.5kg",
    "petdotu313": "https://razaspet.cl/producto/royal-canin-gato-urinary-care/?attribute_pa_peso=1.5kg",
    "petdotu316": "https://razaspet.cl/producto/royal-canin-gato-urinary-care/?attribute_pa_peso=7.5kg",
    "petdotu314": "https://razaspet.cl/producto/royal-canin-gato-urinary-s-o/?attribute_pa_peso=7.5kg",
    "petdotu600":"https://razaspet.cl/producto/leonardo-gato-adulto-gf-maxi/?attribute_pa_peso=7.5kg"
}

sku2 = {"petdotu1": "https://razaspet.cl/producto/leonardo-gato-adulto-gf-maxi/?attribute_pa_peso=7.5kg"}


results = []

for sku_key, url in sku2.items():
    driver.get(url)
    precio_oferta = "No disponible"    
    precio_normal = "No disponible"
    stock= "Con Stock"
    time.sleep(3)
    try:
        # Intenta obtener el precio de oferta
        precio_oferta_element = driver.find_element("xpath", '/html/body/div[2]/div[1]/div/div[3]/div/div/div[3]/div[6]/div/p/ins/span') #Cambiar
        precio_oferta = precio_oferta_element.text  # Guarda el precio de oferta
        stock_element= driver.find_element(By.XPATH,"/html/body/div[2]/div[1]/div/div[3]/div/div/div[3]/div[3]/div/p")
    except NoSuchElementException:
        pass  # Si no se encuentra el precio de oferta, se continuará con el siguiente bloque de código

    try:
        # Intenta obtener el precio normal
        precio_oferta_element = driver.find_element("xpath", '/html/body/div[2]/div[1]/div/div[3]/div/div/div[3]/div[6]/div/p/ins/span') #Cambiar
        precio_oferta = precio_oferta_element.text  # Guarda el precio de oferta
        stock_element= driver.find_element(By.XPATH,"/html/body/div[2]/div[1]/div/div[3]/div/div/div[3]/div[3]/div/p")
        stock=stock_element.text
    except NoSuchElementException:
        pass  # Si no se encuentra el precio normal, se continuará con el siguiente bloque de código

    if precio_oferta == "No disponible" and precio_normal == "No disponible":
        try:
            precio_oferta_element = driver.find_element("xpath", '/html/body/div[2]/div[1]/div/div[3]/div/div/div[3]/div[6]/div/p') #Cambiar
            precio_oferta = precio_oferta_element.text  # Guarda el precio de oferta
            stock_element= driver.find_element(By.XPATH,"/html/body/div[2]/div[1]/div/div[3]/div/div/div[3]/div[3]/div")
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

      
#Fecha de Extraccion
now = datetime.datetime.now()
now_str = now.strftime('%Y-%m-%d %H:%M:%S')
data = {"":now_str}
json_data = json.dumps(data)
values = [[json_data]]
result = sheet.values().update(spreadsheetId=SPREADSHEET_ID,
							range='razaspet!K2',#CAMBIAR
							valueInputOption='USER_ENTERED',
							body={'values':values}).execute()


#Valores que se pasan a Sheets
values = [[item['SKU'], item['Precio'],item['Precio_oferta']] for item in results]
result = sheet.values().update(spreadsheetId=SPREADSHEET_ID,
							range='razaspet!A2:C',#CAMBIAR
							valueInputOption='USER_ENTERED',
							body={'values':values}).execute()
print(f"Datos insertados correctamente")        

#Valores que se pasan a Sheets
values = [[item['Stock']] for item in results]
result = sheet.values().update(spreadsheetId=SPREADSHEET_ID,
							range='razaspet!M2:N',#CAMBIAR
							valueInputOption='USER_ENTERED',
							body={'values':values}).execute()
print(f"Datos insertados correctamente")        


competitor = "Razapet"  # Cambiar 
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
values = [[row['SKU'], competitor,row['Precio'],row["Precio_oferta"], now_str] for _, row in df.iterrows()]

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






