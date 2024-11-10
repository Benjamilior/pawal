import requests
import time
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


start_time = time.time()  # Tiempo de inicio de la ejecución

# URL del endpoint
url = "https://www.superzoo.cl/on/demandware.store/Sites-SuperZoo-Site/es_CL/Product-GetById"

# Diccionario de SKUs
skus = {
    "petdotu360": "2017",
    "petdotu357": "1725",
    "petdotu361": "2447",
    "petdotu354": "1363",
    "petdotu337": "4754",
    "petdotu341": "14026",
    "petdotu324": "611",
    "petdotu321": "5003",
    "petdotu330": "2052",
    "petdotu332": "991",
    "petdotu322": "992",
    "petdotu353": "1010",
    "petdotu356": "1003",
    "petdotu358": "2226",
    "petdotu359": "1004",
    "petdotu352": "970",
    "petdotu362": "2016",
    "petdotu351": "979",
    "petdotu399": "2245",
    "petdotu345": "1008",
    "petdotu346": "987",
    "petdotu403": "2206",
    "petdotu347": "2207",
    "petdotu405": "2227",
    "petdotu391": "2239",
    "petdotu373": "149_m",
    "petdotu377": "2231",
    "petdotu392": "1844",
    "petdotu384": "4940",
    "petdotu385": "221",
    "petdotu394": "1845",
    "petdotu395": "1359",
    "petdotu383": "219",
    "petdotu397": "2238",
    "petdotu387": "2132",
    "petdotu325": "602_m",
    "petdotu326": "1121",
    "petdotu320": "1006",
    "petdotu338": "3536",
    "petdotu425": "2096",
    "petdotu434": "191",
    "petdotu428": "188",
    "petdotu427": "189",
    "petdotu429": "1731",
    "petdotu437": "185",
    "petdotu415": "186",
    "petdotu417": "183",
    "petdotu440": "1835",
    "petdotu416": "187",
    "petdotu462": "908",
    "petdotu452": "10522",
    "petdotu455": "913",
    "petdotu451": "904",
    "petdotu446": "178",
    "petdotu444": "180",
    "petdotu423": "2098",
    "petdotu308": "53",
    "petdotu306": "28",
    "petdotu310": "1948",
    "petdotu302": "14",
    "petdotu311": "58",
    "petdotu307": "50",
    "petdotu300": "22",
    "petdotu301": "21",
    "petdotu304": "5",
    "petdotu305": "3",
    "petdotu318": "32_m",
    "petdotu313": "1723",
    "petdotu316": "1502",
    "petdotu314": "3136"
}


# Encabezados de la solicitud
headers = {
    "cookie": "dwanonymous_d0dc502116cb8dbe645f9cfd4de7a41c=bcMOVoozmTsaCnopmAfqnOFYdA; sid=I5m0lb08bfRr1IZd-AGpLIewqr6SH52xkBU; __cq_dnt=1; dw_dnt=1; dwsid=4nSsmpJ2_8RY_L_RBnLeHkZdsrG9VQ-Boz3nGFJtQqM6J6OU1Rx3ppeUOHQm3CEj_PLgGdVaWDVOtJBmIKtvrg%3D%3D",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:130.0) Gecko/20100101 Firefox/130.0",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Language": "en-US,es-CL;q=0.7,en;q=0.3",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "X-Requested-With": "XMLHttpRequest",
    "Connection": "keep-alive",
    "Referer": "https://www.superzoo.cl/gato/alimentos/alimento-seco/hills-feline-adult-mature-hairball-control-7-1.58-kg-alimento-para-gato/2017.html",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "TE": "trailers"
}
# Lista para almacenar los resultados
results = []

# Función para obtener datos por SKU
def get_product_by_sku(sku_key, sku_id):
    querystring = {"id": sku_id}
    try:
        response = requests.get(url, headers=headers, params=querystring, timeout=10)
        response.raise_for_status()  # Verifica si hubo un error en la respuesta
        data = response.json()  # Asumiendo que la respuesta es JSON
        
        # Extraer solo el 'price' y 'quantity'
        product = data.get('product', {})
        price = product.get('price', 'No disponible')
        quantity = product.get('quantity', 'No disponible')
        
        # Guardar los datos en un diccionario y añadirlo a 'results'
        data = {
            "SKU": sku_key,
            "Precio": price,
            "Stock": quantity
        }
        results.append(data)
        
        # Imprimir el resultado actual
        print(f"SKU: {sku_key} (ID: {sku_id}) - Precio: {price}, Cantidad: {quantity}")
    
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred para SKU {sku_key} (ID: {sku_id}): {http_err}")
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Error de conexión para SKU {sku_key} (ID: {sku_id}): {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        print(f"Timeout para SKU {sku_key} (ID: {sku_id}): {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"Error en la solicitud para SKU {sku_key} (ID: {sku_id}): {req_err}")
    except ValueError as json_err:
        print(f"Error al parsear JSON para SKU {sku_key} (ID: {sku_id}): {json_err}")

# Medir el tiempo de ejecución
start_time = time.time()

# Iterar sobre todos los SKUs y obtener sus datos
for sku_key, sku_id in skus.items():
    get_product_by_sku(sku_key, sku_id)
    time.sleep(1)  # Pausa de 1 segundo entre solicitudes para evitar sobrecargar el servidor

# Calcular el tiempo total de ejecución
end_time = time.time()
execution_time = end_time - start_time

# Convertir los resultados en un DataFrame y mostrarlo
df = pd.DataFrame(results)
print(df)

# Mostrar las primeras filas del DataFrame
print(df.head())

# Imprimir el tiempo de ejecución
print(f"Tiempo de ejecución: {execution_time} segundos")

# Mostrar el contenido de la lista 'results'
print(results)

print("Tiempo de ejecución: %.2f segundos" % execution_time)

      
#Fecha de Extraccion
now = datetime.datetime.now()
now_str = now.strftime('%Y-%m-%d %H:%M:%S')
data = {"":now_str}
json_data = json.dumps(data)
values = [[json_data]]
result = sheet.values().update(spreadsheetId=SPREADSHEET_ID,
							range='superzoo!K2',#CAMBIAR
							valueInputOption='USER_ENTERED',
							body={'values':values}).execute()


#Valores que se pasan a Sheets
values = [[item['SKU'], item['Precio'],] for item in results]
result = sheet.values().update(spreadsheetId=SPREADSHEET_ID,
							range='superzoo!A2:C',#CAMBIAR
							valueInputOption='USER_ENTERED',
							body={'values':values}).execute()
print(f"Datos insertados correctamente")        

#Valores que se pasan a Sheets
values = [[item['Stock']] for item in results]
result = sheet.values().update(spreadsheetId=SPREADSHEET_ID,
							range='superzoo!M2:N',#CAMBIAR
							valueInputOption='USER_ENTERED',
							body={'values':values}).execute()
print(f"Datos insertados correctamente")        
