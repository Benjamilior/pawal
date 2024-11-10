import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from google.oauth2 import service_account
from googleapiclient.discovery import build
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
import pandas as pd
import json
import datetime

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
KEY = 'key.json'
NEW_SPREADSHEET_ID = '1lLfl_jSGUEtitfsezo_zz53Bn2zAzID73VtxIi4dKRo'  # ID de la hoja de cálculo

# Autenticación
creds = service_account.Credentials.from_service_account_file(KEY, scopes=SCOPES)
service = build('sheets', 'v4', credentials=creds)

# Especifica la hoja y el rango que quieres modificar
SHEET_ID = 82059109  # El ID de la hoja, asegúrate de que sea correcto
RANGE_NAME = 'apipets!A:E'  # Rango que quieres vaciar, ajusta según tus necesidades
time.sleep(30)
# Limpiar el contenido de las primeras 5 columnas (A:E)
clear_values_request_body = {}

response = service.spreadsheets().values().clear(
    spreadsheetId=NEW_SPREADSHEET_ID,
    range=RANGE_NAME,
    body=clear_values_request_body
).execute()

print("Las columnas especificadas han sido vaciadas.")
