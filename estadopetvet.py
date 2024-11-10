from google.oauth2 import service_account
from googleapiclient.discovery import build
import datetime
import pandas as pd

# Autenticación y construcción del servicio de la API
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
KEY = 'key.json'
SPREADSHEET_ID = '1VU3_P_EqdSJzabp1eCpNdoyVP7LQfs8FkHkwFabac5A'

# Cargar credenciales de servicio
creds = service_account.Credentials.from_service_account_file(KEY, scopes=SCOPES)
service = build('sheets', 'v4', credentials=creds)
sheet = service.spreadsheets()

# Definir los rangos que deseas obtener
ranges = ['Verificador!BL2:BM164']
ranges2 = ['Verificador!AA2:AA164']

def fetch_data(range_list):
    all_values = []
    for range_name in range_list:
        result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=range_name).execute()
        values = result.get('values', [])
        all_values.append(values)
    return all_values

# Obtener datos de los rangos
data1 = fetch_data(ranges)
data2 = fetch_data(ranges2)

# Fecha de Extracción
now = datetime.datetime.now()
now_str = now.strftime('%Y-%m-%d %H:%M:%S')

# Convertir los datos obtenidos a DataFrame de pandas
data1_flat = [item for sublist in data1 for item in sublist]
df1 = pd.DataFrame(data1_flat)
df1['Fecha'] = now_str
df1 = df1[['Fecha'] + list(df1.columns[:-1])]

data2_flat = [item for sublist in data2 for item in sublist]
df2 = pd.DataFrame(data2_flat)

# Escribir los datos en la nueva hoja de Google Sheets
NEW_SPREADSHEET_ID = '1Yn7Ze_WQJ19s-PmbaeLsTFaehygu3jSHaMvrxcfbneU'

def write_data(df, start_column, end_column):
    data_to_write = df.values.tolist()
    # Obtener la última fila con datos en la nueva hoja
    result = sheet.values().get(spreadsheetId=NEW_SPREADSHEET_ID, range=f'Estado!{start_column}:{end_column}').execute()
    values = result.get('values', [])
    last_row = len(values) + 1

    # Insertar los resultados en la nueva hoja después de la última fila
    update_range = f'Estado!{start_column}{last_row}:{end_column}{last_row + len(data_to_write) - 1}'
    try:
        result = sheet.values().update(
            spreadsheetId=NEW_SPREADSHEET_ID,
            range=update_range,
            valueInputOption='USER_ENTERED',
            body={'values': data_to_write}
        ).execute()
        print(f'Datos actualizados en la hoja de cálculo en el rango {update_range}.')
    except Exception as e:
        print(f'Error al actualizar datos: {e}')

# Escribir los datos de df1 en columnas A:C
write_data(df1, 'A', 'C')

# Escribir los datos de df2 en la columna D
# Ajustar df2 para que solo tenga una columna si es necesario
df2.columns = ['Datos']  # Ajusta según lo que esperas que contenga df2
df2 = df2[['Datos']]  # Solo mantener la columna que quieres escribir en la columna D

# Escribir los datos en la columna D
write_data(df2, 'D', 'D')
