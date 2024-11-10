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
    "petdotu360": "https://jardinzoo.cl/senior/3939-hills-cat-hairball-senior-15kg.html",
    "petdotu357": "https://jardinzoo.cl/adulto/2013-hills-cat-adulto-hairball-31kg.html",
    "petdotu361": "https://jardinzoo.cl/alimentos-light/2633-hills-cat-perfect-weight-13-kg.html",
    "petdotu354": "https://jardinzoo.cl/alimentos/3736-hills-cat-kitten-indoor-158kg-52742252902.html",
    "petdotu337": "https://jardinzoo.cl/senior-7-anos/1964-hills-adult-7-toy-small-2kg.html",
    "petdotu372": "https://jardinzoo.cl/medicados/1952-hills-dog-id-15kg.html",
    "petdotu367": "https://jardinzoo.cl/senior-7-anos/5295-hills-adult-7-small-bites-68-kg-052742057569.html",
    "petdotu412": "https://jardinzoo.cl/senior-7-anos/5387-hills-adult-7-small-bites-2-kg-052742005355.html",
    "petdotu413": "https://jardinzoo.cl/senior-7-anos/5295-hills-adult-7-small-bites-68-kg-052742057569.html",
    "petdotu324": "https://jardinzoo.cl/adulto/994-hills-adulto-small-bites-68-kg-52742020488.html",
    "petdotu332": "https://jardinzoo.cl/alimentos-light/706-hills-adulto-light-small-22kg-52742930107.html",
    "petdotu331": "https://jardinzoo.cl/adulto/2354-hills-dog-adulto-toy-204kg.html",
    "petdotu322": "https://jardinzoo.cl/alimentos-light/1960-hills-light-small-toy-2kg.html",
    "petdotu348": "https://jardinzoo.cl/adulto/1944-hills-adulto-cat-original-31kg.html",
    "petdotu353": "https://jardinzoo.cl/senior/1933-hills-cat-mature-active-18kg.html",
    "petdotu356": "https://jardinzoo.cl/adulto/1948-hills-cat-hairball-control-158-52742715605.html",
    "petdotu359": "https://jardinzoo.cl/alimentos-light/1882-hills-cat-hairball-light-31kg-52742888200.html",
    "petdotu352": "https://jardinzoo.cl/adulto/2634-hills-cat-indoor-158-kg.html",
    "petdotu350": "https://jardinzoo.cl/alimentos-light/1881-hills-cat-light-18-kg-52742671109.html",
    "petdotu404": "https://jardinzoo.cl/senior/1947-hills-cat-mature-indoor-158kg.html",
    "petdotu345": "https://jardinzoo.cl/ofertazoo/6069-hills-cat-kitten-317kg-052742712307.html",
    "petdotu346": "https://jardinzoo.cl/gatitos/1156-hills-cat-kitten-317kg-52742939100.html",
    "petdotu405": "https://jardinzoo.cl/medicados/1935-hills-dog-cd-15kg-52742001135.html",
    "petdotu368": "https://jardinzoo.cl/medicados/26-hills-dog-cd-385k-52742001746.html",
    "petdotu391": "https://jardinzoo.cl/medicados/215-hills-cat-id-18kg-52742462905.html",
    "petdotu377": "https://jardinzoo.cl/medicados/508-hills-dog-kd-15-kg-52742001197.html",
    "petdotu378": "https://jardinzoo.cl/medicados/509-hills-dog-kd-38kg-52742862101.html",
    "petdotu392": "https://jardinzoo.cl/medicados/1953-hills-cat-kd-18kg.html",
    "petdotu393": "https://jardinzoo.cl/medicados/212-hills-cat-kd-385-kg-52742869605.html",
    "petdotu384": "https://jardinzoo.cl/medicados/4003-hills-dog-metabolic-79-kg-52742022369.html",
    "petdotu394": "https://jardinzoo.cl/medicados/1943-hills-cat-metabolic-18kg.html",
    "petdotu395": "https://jardinzoo.cl/medicados/2353-hills-cat-metabolic-38kg-52742195506.html",
    "petdotu457": "https://jardinzoo.cl/adulto/1321-proplan-cat-adulto-3-kg-7613039900277.html",
    "petdotu434": "https://jardinzoo.cl/ofertazoo/17-proplan-reduced-calories-12-3g-kg-7613287033130.html",
    "petdotu415": "https://jardinzoo.cl/adulto/4617-proplan-adulto-raza-mediana-123-kg-7613287031082.html",
    "petdotu417": "https://jardinzoo.cl/adulto/1188-proplan-adulto-small-75-kilos-7613287029515.html",
    "petdotu447": "https://jardinzoo.cl/cachorro/2369-proplan-puppy-small-75-kg-7613287028129.html",
    "petdotu462": "https://jardinzoo.cl/senior/2375-proplan-cat-7-3-kg.html",
    "petdotu456": "https://jardinzoo.cl/ofertazoo/1322-proplan-cat-adulto-75-kg-7613039899922.html",
    "petdotu452": "https://jardinzoo.cl/adulto/4565-proplan-cat-sterilized-75-kg-7613287119629.html",
    "petdotu455": "https://jardinzoo.cl/adulto/1323-proplan-cat-urinary-3-kg-7613039947111.html",
    "petdotu454": "https://jardinzoo.cl/ofertazoo/1324-proplan-cat-urinary-75-kg-7613039947739.html",
    "petdotu451": "https://jardinzoo.cl/gatitos/1864-proplan-cat-kitten-1-kg.html",
    "petdotu450": "https://jardinzoo.cl/gatitos/2373-proplan-cat-kitten-3-k-7613039886922.html",
    "petdotu449": "https://jardinzoo.cl/ofertazoo/1325-proplan-cat-kitten-75-k-7613039784914.html",
    "petdotu460": "https://jardinzoo.cl/adulto/1925-proplan-cat-sterilized-3-kg-7613039947784.html",
    "petdotu459": "https://jardinzoo.cl/ofertazoo/2376-proplan-cat-sterilized-75-kg.html",
    "petdotu418": "https://jardinzoo.cl/cachorro/1872-proplan-puppy-large-breed-12-3-kg.html",
    "petdotu444": "https://jardinzoo.cl/cachorro/4319-proplan-puppy-complete-12-3-kg-7613034479204.html",
    "petdotu421": "https://jardinzoo.cl/senior-7-anos/2378-proplan-active-mind-raza-medgrande-12-3kg-7613287032911.html",
    "petdotu442": "https://jardinzoo.cl/senior-7-anos/2380-proplan-active-mind-razas-pequenas-75k.html",
    "petdotu302": "https://jardinzoo.cl/adulto/515-royal-canin-medium-adulto-15-kg-7896181211884.html",
    "petdotu309": "https://jardinzoo.cl/gatos/288-royal-canin-exigent-15-kg-7896181213154.html",
    "petdotu308": "https://jardinzoo.cl/alimentos/2263-royal-canin-cat-fit-75-kg.html",
    "petdotu311": "https://jardinzoo.cl/adulto/5147-royal-canin-hairball-care-15kg-7790187340336.html",
    "petdotu315": "https://jardinzoo.cl/alimentos/5204-royal-canin-cat-weight-care-75k-7790187340534.html",
    "petdotu300": "https://jardinzoo.cl/adulto/193-royal-canin-maxi-adulto-15-kg-7896181211822.html",
    "petdotu305": "https://jardinzoo.cl/cachorro/4904-royal-canin-mini-puppy-75-kg-7790187339637.html",
    "petdotu318": "https://jardinzoo.cl/alimentos/4887-royal-canin-persian-30-15-kg-7790187339422.html",
    "petdotu303": "https://jardinzoo.cl/adulto/515-royal-canin-medium-adulto-15-kg-7896181211884.html",
    "petdotu310": "https://jardinzoo.cl/adulto/4234-royal-canin-sensible-33-15-kg-7790187339484.html",
    "petdotu313": "https://jardinzoo.cl/adulto/6111-royal-canin-cat-urinary-care-15kg-7790187342767.html",
    
}

sku2 = {"petdotu1": "https://puntomascotas.cl/cicatrizantes/37170-apoquel-16-mg-x-20-comprimidos-5414736044217.html"}


results = []

for sku_key, url in sku.items():
    driver.get(url)
    precio_oferta = "No disponible"    
    precio_normal = "No disponible"
    stock= "Con Stock"
    try:
        # Intenta obtener el precio de oferta
        precio_oferta_element = driver.find_element("xpath", '/html/body/main/section/div/div/section/div[1]/div[2]/div[1]/div[2]/div') #Cambiar
        precio_oferta = precio_oferta_element.text  # Guarda el precio de oferta
        stock_element= driver.find_element(By.ID,"product-availability")
        stock=stock_element.text
    except NoSuchElementException:
        pass  # Si no se encuentra el precio de oferta, se continuará con el siguiente bloque de código

    try:
        # Intenta obtener el precio normal
        precio_oferta_element = driver.find_element("xpath", '/html/body/main/section/div/div/section/div[1]/div[2]/div[1]/div[1]/div') #Cambiar
        precio_oferta = precio_oferta_element.text  # Guarda el precio de oferta
        stock_element= driver.find_element(By.ID,"product-availability")
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

      
#Fecha de Extraccion
now = datetime.datetime.now()
now_str = now.strftime('%Y-%m-%d %H:%M:%S')
data = {"":now_str}
json_data = json.dumps(data)
values = [[json_data]]
result = sheet.values().update(spreadsheetId=SPREADSHEET_ID,
							range='jardinzoo!K2',#CAMBIAR
							valueInputOption='USER_ENTERED',
							body={'values':values}).execute()


#Valores que se pasan a Sheets
values = [[item['SKU'], item['Precio'],item['Precio_oferta']] for item in results]
result = sheet.values().update(spreadsheetId=SPREADSHEET_ID,
							range='jardinzoo!A2:C',#CAMBIAR
							valueInputOption='USER_ENTERED',
							body={'values':values}).execute()
print(f"Datos insertados correctamente")        

#Valores que se pasan a Sheets
values = [[item['Stock']] for item in results]
result = sheet.values().update(spreadsheetId=SPREADSHEET_ID,
							range='jardinzoo!M2:N',#CAMBIAR
							valueInputOption='USER_ENTERED',
							body={'values':values}).execute()
print(f"Datos insertados correctamente")        


competitor = "Jardinzoo"  # Cambiar 
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
