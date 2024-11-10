import requests
from google.oauth2 import service_account
from googleapiclient.discovery import build
import json
import time

# Configuración de Google Sheets
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
KEY = 'key.json'
SPREADSHEET_ID = '1S8jzZl4UehXDJxWuHfTSLftBnq3CKUXhgRGrJIShyhE'
RANGE_NAME = 'apipets!F:I'  # Rango que incluye las columnas F, G, H, I

# Autenticación con Google Sheets
creds = service_account.Credentials.from_service_account_file(KEY, scopes=SCOPES)
service = build('sheets', 'v4', credentials=creds)
time.sleep(30)
# Leer los datos de Google Sheets
result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
values = result.get('values', [])

# Convertir los datos en JSON
data_json = []
for row in values:  # Iterar sobre cada fila
    if len(row) == 4:  # Asegurarse de que la fila tiene todas las columnas necesarias
        sku, tienda, price, stock = row
        
        # Manejar el caso donde el precio o el stock no sea convertible a float o int
        try:
            price = float(price) if price else 0.0  # Si el precio está vacío, asignar 0.0
        except ValueError:
            price = 0.0  # Si el precio no es numérico, asignar 0.0

        try:
            stock = int(stock) if stock else 0  # Si el stock está vacío, asignar 0
        except ValueError:
            stock = 0  # Si el stock no es numérico, asignar 0

        data_json.append({
            "sku": sku,
            "tienda": tienda,
            "price": price,
            "stock": stock
        })

# Imprimir el JSON para verificar
print(json.dumps(data_json, indent=2))

# URL de la API
api_url = "https://dotupetpublic-production.up.railway.app/bulk_update_prices"


# Enviar el JSON a la API
response = requests.put(api_url, json=data_json)

# Verificar la respuesta
if response.status_code == 200:
    print("Datos enviados exitosamente.")
    print(response.json())  # Muestra la respuesta de la API si es JSON
else:
    print(f"Error al enviar datos: {response.status_code} - {response.text}")