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
import pandas as pd
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
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


# #URLs

sku = {
    "petdotu344": "https://www.petco.cl/petco-chile/es_CL/PRODUCTOS/Perro/Premios-/Jerky-Treats/Hill%27s-Science-Diet-Jerky-Premio-Suave-en-Tiras-para-Perro-Receta-Pollo%2C-200-g/p/105275",
    "petdotu360": "https://www.petco.cl/petco-chile/es_CL/PRODUCTOS/Gato/Alimento/Alimento-Gato-Senior/Hill%27s-Science-Diet-Alimento-Seco-Feline-Adult-Mature-7%2B-Hairball-Control-para-Gato%2C-1-59-kg/p/600495",
    "petdotu361": "https://www.petco.cl/petco-chile/es_CL/PRODUCTOS/Gato/Alimento/Alimento-Seco/Hill%27s-Science-Diet-Perfect-Weight-Alimento-Seco-para-Gato-Adulto-Reducci%C3%B3n-de-Peso-Receta-Pollo%2C-1-4-kg/p/114695",
    "petdotu354": "https://www.petco.cl/petco-chile/es_CL/PRODUCTOS/Gato/Alimento/Alimento-Gato-Senior/Hill%27s-Science-Diet-Alimento-Seco-Feline-Adult-11%2B-Indoor-para-Gato%2C-1-59-kg/p/600496",
    "petdotu337": "https://www.petco.cl/petco-chile/es_CL/PRODUCTOS/Perro/Hill%27s-Science-Diet-Small-Paws-Adult-7%2B-Alimento-Seco-para-Perro-Senior-Raza-Peque%C3%B1a-y-Miniatura-Receta-Pollo%2C-2-kg/p/134520",
    "petdotu341": "https://www.petco.cl/petco-chile/es_CL/PRODUCTOS/Perro/Hill%27s-Science-Diet-Alimento-Seco-Adult-Sensitive-Stomach-y-Skin-para-Perro%2C-7-03-kg/p/600477",
    "petdotu409": "https://www.petco.cl/petco-chile/es_CL/PRODUCTOS/Gato/Hill%27s-Science-Diet-Perfect-Digesti%C3%B3n-Alimento-Seco-Salud-Digestiva-para-Gato-Adulto%2C-1-5-kg/p/134535",
    "petdotu411": "https://www.petco.cl/petco-chile/es_CL/PRODUCTOS/Perro/Alimento/Alimento-Perros-Senior/Hill%27s-Science-Diet-Adult-7%2B-Alimento-Seco-para-Perro-Senior-Receta-Pollo%2C-Cebada-y-Arroz-Integral%2C-12-kg/p/600480",
    "petdotu335": "https://www.petco.cl/petco-chile/es_CL/PRODUCTOS/Perro/Alimento/Alimento-Perros-Senior/Hill%27s-Science-Diet-Adult-7%2B-Alimento-Seco-para-Perro-Senior-Receta-Pollo%2C-Cebada-y-Arroz-Integral%2C-12-kg/p/600480",
    "petdotu365": "https://www.petco.cl/petco-chile/es_CL/App/Alimento/Hill%27s-Science-Diet/Hill%27s-Science-Diet-Alimento-Seco-para-Perro-Adulto-Raza-Mediana-Grande-Receta-Pollo-y-Cebada%2C-7-5-kg/p/105242",
    "petdotu324": "https://www.petco.cl/petco-chile/es_CL/App/Alimento/Hill%27s-Science-Diet/Hill%27s-Science-Diet-Small-Bites-Alimento-Seco-para-Perro-Adulto-Raza-Mediana-Receta-Pollo-y-Cebada%2C-2-kg/p/105258",
    "petdotu332": "https://www.petco.cl/petco-chile/es_CL/App/Alimento/Hill%27s-Science-Diet/Hill%27s-Science-Diet-Alimento-Seco-Adult-Light-Small-Bites-para-Perro%2C-2-26-kg/p/600481",
    "petdotu333": "https://www.petco.cl/petco-chile/es_CL/PRODUCTOS/Perro/Hill%27s-Science-Diet-Alimento-Seco-Adult-Light-Small-Bites-para-Perro%2C-6-8-kg/p/600489",
    "petdotu330": "https://www.petco.cl/petco-chile/es_CL/PRODUCTOS/Perro/Alimento/Hill%27s-Science-Diet-Alimento-Seco-Light-para-Perro-Adulto-Raza-Grande-Receta-Pollo-y-Cebada%2C-6-8-kg/p/105249",
    "petdotu340": "https://www.petco.cl/petco-chile/es_CL/App/Alimento/Hill%27s-Science-Diet/Hill%27s-Science-Diet-Alimento-Seco-Adult-Sensitive-Stomach-y-Skin-Mini-para-Perro%2C-1-8-1-kg/p/600478",
    "petdotu331": "https://www.petco.cl/petco-chile/es_CL/App/Alimento/Hill%27s-Science-Diet/Hill%27s-Science-Diet-Small-Paws-Alimento-Seco-para-Perro-Adulto-Raza-Peque%C3%B1a-Receta-Pollo-y-Arroz%2C-2-04-kg/p/105231",
    "petdotu322": "https://www.petco.cl/petco-chile/es_CL/PRODUCTOS/Perro/Alimento/Alimento-Perros-Talla-Peque%C3%B1a/Hill%27s-Science-Diet-Small-%26-Mini-Light-Alimento-Seco-para-Perro-Adulto-Raza-Peque%C3%B1a-y-Toy%2C-2-kg/p/105233",
    "petdotu366": "https://www.petco.cl/petco-chile/es_CL/App/Alimento/Hill%27s-Science-Diet/Hill%27s-Science-Diet-Alimento-Seco-para-Perro-Adulto-Raza-Grande-Gigante-Receta-Pollo-y-Cebada%2C-15-kg/p/105243",
    # "petdotu348": "https://www.petco.cl/petco-chile/es_CL/PRODUCTOS/Gato/Alimento/Alimento-Gato-Senior/Hill%27s-Science-Diet-Alimento-Seco-Feline-Adult-Mature-7%2B-Hairball-Control-para-Gato%2C-1-59-kg/p/600495",
    # "petdotu349": "https://www.petco.cl/petco-chile/es_CL/PRODUCTOS/Gato/Hill%27s-Science-Diet-Alimento-Seco-Control-Bolas-de-Pelo-para-Gato-Adulto-Receta-Pollo%2C-7-kg/p/105175",
    "petdotu353": "https://www.petco.cl/petco-chile/es_CL/PRODUCTOS/Gato/Alimento/Alimento-Gato-Senior/Hill%27s-Science-Diet-Adult-7%2B-Alimento-Seco-para-Gato-Senior%2C-1-8-kg/p/105159",
    "petdotu356": "https://www.petco.cl/petco-chile/es_CL/PRODUCTOS/Gato/Alimento/Alimento-Gato-Senior/Hill%27s-Science-Diet-Alimento-Seco-Feline-Adult-Mature-7%2B-Hairball-Control-para-Gato%2C-1-59-kg/p/600495",
    "petdotu358": "https://www.petco.cl/petco-chile/es_CL/PRODUCTOS/Gato/Hill%27s-Science-Diet-Alimento-Seco-Control-Bolas-de-Pelo-para-Gato-Adulto-Receta-Pollo%2C-7-kg/p/105175",
    "petdotu359": "https://www.petco.cl/petco-chile/es_CL/App/Alimento/Hill%27s-Science-Diet/Hills-Science-Diet-Alimento-Para-Gato-Adulto-Hairball-Control-Light-3-18-kg/p/110091",
    "petdotu352": "https://www.petco.cl/petco-chile/es_CL/PRODUCTOS/Gato/Alimento/Hill%27s-Science-Diet-Indoor-Comida-Seca-para-Gato-Adulto-de-Interior-Receta-Pollo%2C-1-6-kg/p/110088",
    "petdotu362": "https://www.petco.cl/petco-chile/es_CL/PRODUCTOS/Gato/Alimento/Hill%27s-Science-Diet-Alimento-Seco-Feline-Adult-Sensitive-Stomach-y-Skin-para-Gato%2C-1-59-kg/p/600494",
    "petdotu350": "https://www.petco.cl/petco-chile/es_CL/PRODUCTOS/Gato/Hill%27s-Science-Diet-Alimento-Seco-Feline-Adult-Light-para-Gato%2C-1-81-kg/p/600497",
    "petdotu351": "https://www.petco.cl/petco-chile/es_CL/App/Alimento/Hill%27s-Science-Diet/Hill%27s-Science-Diet-Alimento-para-Gato-Adulto-Light%2C-1-81-kg/p/105168",
    "petdotu355": "https://www.petco.cl/petco-chile/es_CL/PRODUCTOS/Gato/Alimento/Alimento-Seco/Hill%27s-Science-Diet%C2%A0Youthful-Vitality-Alimento-Seco-para-Gato-Senior-Receta-Pollo-y-Arroz%2C-1-4-kg/p/125469",
    "petdotu399": "https://www.petco.cl/petco-chile/es_CL/PRODUCTOS/Gato/Hill%27s-Prescription-Diet-Alimento-Seco-Feline-y-D-Thyroid-Care-para-Gato%2C-1-81-kg/p/600511",
    "petdotu345": "https://www.petco.cl/petco-chile/es_CL/PRODUCTOS/Gato/Alimento/Alimento-Gatito/Hill%27s-Science-Diet-Alimento-Seco-Feline-Kitten-para-Gatito%2C-3-18-kg/p/105299",
    "petdotu347": "https://www.petco.cl/petco-chile/es_CL/PRODUCTOS/Gato/Alimento/Alimento-Gatito/Hill%27s-Science-Diet-Alimento-Seco-para-Gatito-de-Interior-Receta-Pollo%2C-1-6-kg/p/110095",
    "petdotu369": "https://www.petco.cl/petco-chile/es_CL/PRODUCTOS/Perro/Alimento/Alimento-Medicado-/Hill%27s%C2%A0Prescription-Diet-c-d-Alimento-Seco-Cuidado-Urinario-para-Perro-Adulto%2C-8-kg/p/105340",
    "petdotu390": "https://www.petco.cl/petco-chile/es_CL/App/Bienestar-para-tu-Mascota-Perro-Gato/Bienestar-para-Gato/Hill%27s-Prescription-Diet-c-d-Alimento-Seco-Cuidado-Urinario-para-Gato-Adulto%2C-3-9-kg/p/105178",
    "petdotu391": "https://www.petco.cl/petco-chile/es_CL/MARCAS/Hill%27s/Hill%27s-Prescription-Diet/Hill%27s-Prescription-Diet-i-d-Alimento-Seco-Gastrointestinal-para-Gato%2C-1-8-kg/p/105179",
    # "petdotu373": "https://www.petco.cl/petco-chile/es_CL/PRODUCTOS/Perro/Alimento/Alimento-Medicado-/Hill%27s-Prescription-Diet-i-d-Alimento-Seco-Gastrointestinal-Bajo-en-Grasa-para-Perro-Adulto%2C-3-9-kg/p/105284",
    "petdotu374": "https://www.petco.cl/petco-chile/es_CL/App/Bienestar-para-tu-Mascota-Perro-Gato/Bienestar-para-Perro/Hill%27s-Prescription-Diet-l-d-Alimento-Seco-Salud-Hep%C3%A1tica-para-Perro-Adulto-Receta-Cerdo%2C-8-kg/p/105327",
    "petdotu376": "https://www.petco.cl/petco-chile/es_CL/App/Bienestar-para-tu-Mascota-Perro-Gato/Bienestar-para-Perro/Hill%27s-Prescription-Diet-j-d-Alimento-Seco-para-Movilidad-para-Perro-Adulto%2C-12-5-kg/p/105306",
    "petdotu379": "https://www.petco.cl/petco-chile/es_CL/PRODUCTOS/Perro/Alimento/Alimento-Medicado-/Hill%27s%C2%A0Prescription-Diet-k-d-Alimento-Seco-Cuidado-Renal-para-Perro-Adulto%2C-12-5-kg/p/105330",
    "petdotu393": "https://www.petco.cl/petco-chile/es_CL/MARCAS/Hill%27s/Hill%27s-Prescription-Diet/Hill%27s-Prescription-Diet-k-d-Alimento-Seco-Cuidado-Renal-para-Gato-Adulto%2C-1-8-kg/p/105181",
    "petdotu380": "https://www.petco.cl/petco-chile/es_CL/App/Bienestar-para-tu-Mascota-Perro-Gato/Bienestar-para-Perro/Hill%27s-Prescription-Diet-l-d-Alimento-Seco-Salud-Hep%C3%A1tica-para-Perro-Adulto-Receta-Cerdo%2C-8-kg/p/105327",
    "petdotu385": "https://www.petco.cl/petco-chile/es_CL/PRODUCTOS/Perro/Alimento/Alimento-Medicado-/Hill%27s-Prescription-Diet-Metabolic-Alimento-Seco-Control-del-Peso-para-Perro-Adulto%2C-12-5-kg/p/105311",
    "petdotu394": "https://www.petco.cl/petco-chile/es_CL/PRODUCTOS/Gato/Alimento/Alimento-Medicado/Hill%27s%C2%A0Prescription-Diet-Metabolic-Alimento-Seco-para-Gato-Adulto%2C-3-7-kg/p/105190",
    "petdotu395": "https://www.petco.cl/petco-chile/es_CL/MARCAS/Hill%27s/Hill%27s-Prescription-Diet/Hill%27s%C2%A0Prescription-Diet-Metabolic-Alimento-Seco-Control-de-Peso-para-Gato-Adulto%2C-8-kg/p/105191",
    "petdotu396": "https://www.petco.cl/petco-chile/es_CL/MARCAS/Hill%27s/Hill%27s-Prescription-Diet/Hill%27s-Prescription-Diet-Metabolic-%2B-Urinary-Alimento-Seco-Peso-Uinario-para-Gato-Adulto%2C-2-9-kg/p/122363",
    "petdotu381": "https://www.petco.cl/petco-chile/es_CL/PRODUCTOS/Perro/Alimento/Alimento-Medicado-/Hill%27s%C2%A0Prescription-Diet-r-d%2C-Alimento-Seco-Reducci%C3%B3n-de-Peso-para-Perro-Adulto%2C-8-kg/p/600507",
    "petdotu382": "https://www.petco.cl/petco-chile/es_CL/PRODUCTOS/Perro/Alimento/Alimento-Medicado-/Hill%27s%C2%A0Prescription-Diet-r-d%2C-Alimento-Seco-Reducci%C3%B3n-de-Peso-para-Perro-Adulto%2C-8-kg/p/105289",
    "petdotu383": "https://www.petco.cl/petco-chile/es_CL/PRODUCTOS/Perro/Alimento/Alimento-Medicado-/Hill%27s%C2%A0Prescription-Diet-r-d%2C-Alimento-Seco-Reducci%C3%B3n-de-Peso-para-Perro-Adulto%2C-8-kg/p/105325",
    "petdotu397": "https://www.petco.cl/petco-chile/es_CL/MARCAS/Hill%27s/Hill%27s-Prescription-Diet/Hill%27s-Prescription-Diet-Alimento-para-Gato-R-D%2C-1-81-kg/p/105182",
    "petdotu398": "https://www.petco.cl/petco-chile/es_CL/PRODUCTOS/Gato/Alimento/Alimento-Medicado/Hill%27s%C2%A0Prescription-Diet-r-d-Weight-Loss-Alimento-Seco-Reducci%C3%B3n-de-Peso-para-Gato-Adulto%2C-3-7-kg/p/105183",
    "petdotu386": "https://www.petco.cl/petco-chile/es_CL/PRODUCTOS/Perro/Alimento/Alimento-Medicado-/Hill%27s-Prescription-Diet-Alimento-Seco-Canine-U-D-Urinary-Care-para-Perro%2C-3-8-kg/p/105293",
    "petdotu388": "https://www.petco.cl/petco-chile/es_CL/PRODUCTOS/Perro/Alimento/Alimento-Perros-Talla-Grande/Hill%27s%C2%A0Prescription-Diet-w-d-Alimento-Seco-Digestivo-Control-de-Peso-Glucosa-para-Perro-Adulto%2C-12-5-kg/p/105322",
    "petdotu400": "https://www.petco.cl/petco-chile/es_CL/PRODUCTOS/Gato/Hill%27s-Prescription-Diet-Alimento-Seco-Feline-W-D-Digestive%2C-Weight%2C-Glucose-Management-para-Gato%2C-1-81-kg/p/600512",
    "petdotu389": "https://www.petco.cl/petco-chile/es_CL/App/Bienestar-para-tu-Mascota-Perro-Gato/Bienestar-para-Perro/Hill%27s-Prescription-Diet-z-d-Alimento-Seco-Alergias-Alimentarias-para-Perro-Adulto%2C-3-6-kg/p/105296",
    "petdotu401": "https://www.petco.cl/petco-chile/es_CL/PRODUCTOS/Gato/Alimento/Alimento-Medicado/Hill%27s-Prescription-Diet-z-d-Alimento-Seco-para-Alergias-Alimentarias-para-Gato-Adulto%2C-1-8-kg/p/105189",
    "petdotu326": "https://www.petco.cl/petco-chile/es_CL/PRODUCTOS/Perro/Alimento/Alimento-Seco/Hill%27s-Science-Diet-Alimento-Seco-para-Cachorro-Raza-Grande-Receta-Pollo-y-Cebada%2C-2-kg/p/105255",
    "petdotu320": "https://www.petco.cl/petco-chile/es_CL/PRODUCTOS/Perro/Alimento/Alimento-para-Cachorro/Hill%27s-Science-Diet-Small-Bites-Alimento-Seco-para-Cachorro-Raza-Mediana-Receta-Pollo-y-Cebada%2C-2-kg/p/105201",
    "petdotu328": "https://www.petco.cl/petco-chile/es_CL/PRODUCTOS/Perro/Alimento/Alimento-Perros-Talla-Peque%C3%B1a/Hill%27s-Science-Diet-Small-Paws-Alimento-Seco-para-Cachorro-Raza-Chica-Receta-Pollo-Cebada-y-Arroz-Integral%2C-2-kg/p/105230",
    "petdotu338": "https://www.petco.cl/petco-chile/es_CL/PRODUCTOS/Perro/Alimento/Alimento-Seco/Hill%27s-Science-Diet-Youthful-Vitality-Alimento-Seco-para-Perro-Senior-Raza-Peque%C3%B1a-Receta-Pollo-y-Arroz%2C-1-6-kg/p/125466",
    "petdotu432": "https://www.petco.cl/petco-chile/es_CL/MARCAS/Pro-Plan/Pro-Plan-Alimento-Avanzado-Seco-Optidual-Sensitive-Skin-And-Stomach-para-Perro-Adulto-Raza-Peque%C3%B1a%2C-7-5-kg/p/600015",
    "petdotu430": "https://www.petco.cl/petco-chile/es_CL/MARCAS/Pro-Plan/Pro-Plan-Alimento-Avanzado-Seco-Optidual-Sensitive-Skin-And-Stomach-para-Perro-Adulto-Raza-Mediana-y-Grande%2C-15-kg/p/600012",
    "petdotu425": "https://www.petco.cl/petco-chile/es_CL/MARCAS/Pro-Plan/Pro-Plan-Alimento-Avanzado-Seco-Optiderma-Sensitive-Skin-para-Perro-Adulto-receta-Cordero-y-Arroz%2C-15-kg/p/600011",
    "petdotu434": "https://www.petco.cl/petco-chile/es_CL/PRODUCTOS/Perro/Alimento/Alimento-Perros-Talla-Grande/Pro-Plan-Reduced-Calorie-Alimento-Seco-para-Perro-Adulto-de-Razas-Medianas-y-Grandes%2C-3-kg/p/600008",
    "petdotu429": "https://www.petco.cl/petco-chile/es_CL/PRODUCTOS/Perro/Pro-Plan-Sensitive-Skin-Alimento-Seco-para-Perro-Adulto-de-Raza-Peque%C3%B1a%2C-3-kg/p/600028",
    "petdotu415": "https://www.petco.cl/petco-chile/es_CL/PRODUCTOS/Perro/Alimento/Alimento-Perros-Talla-Grande/Pro-Plan-Alimento-Seco-para-Perro-Adulto-de-Razas-Medianas%2C-15-kg/p/600005",
    "petdotu417": "https://www.petco.cl/petco-chile/es_CL/PRODUCTOS/Perro/Pro-Plan-Alimento-Seco-para-Perro-Adulto-de-Razas-Peque%C3%B1as%2C-7-5-kg/p/600004",
    "petdotu440": "https://www.petco.cl/petco-chile/es_CL/PRODUCTOS/Perro/Pro-Plan-Exigent-Alimento-Seco-para-Perro-Adulto-de-Razas-Peque%C3%B1as%2C-7-5-kg/p/600014",
    "petdotu431": "https://www.petco.cl/petco-chile/es_CL/MARCAS/Pro-Plan/Pro-Plan-Alimento-Avanzado-Seco-Optidual-Sensitive-Skin-And-Stomach-para-Perro-Adulto-Raza-Mediana-y-Grande%2C-15-kg/p/600012",
    "petdotu416": "https://www.petco.cl/petco-chile/es_CL/PRODUCTOS/Perro/Pro-Plan-Alimento-Seco-para-Perro-Adulto-de-Razas-Grandes%2C-15-kg/p/600006",
    "petdotu462": "https://www.petco.cl/petco-chile/es_CL/PRODUCTOS/Gato/Pro-Plan-Optiage-Alimento-Seco-para-Gato-Adulto-de-Todas-las-Razas%2C-3-kg/p/600068",
    "petdotu456": "https://www.petco.cl/petco-chile/es_CL/MARCAS/Pro-Plan/Pro-Plan-Alimento-Seco-para-Gato-Adulto-de-Todas-las-Razas%2C-1-kg/p/600046",
    "petdotu452": "https://www.petco.cl/petco-chile/es_CL/MARCAS/Pro-Plan/Pro-Plan-Live-Clear-Alimento-Seco-para-Gato-Adulto-de-Todas-las-Razas%2C-1-kg/p/600052",
    "petdotu454": "https://www.petco.cl/petco-chile/es_CL/PRODUCTOS/Gato/Pro-Plan-Urinary-Alimento-Seco-para-Gato-Adulto-de-Todas-las-Razas%2C-1-kg/p/600049",
    "petdotu451": "https://www.petco.cl/petco-chile/es_CL/PRODUCTOS/Gato/Pro-Plan-Alimento-Seco-para-Gatitos-de-Todas-las-Razas%2C-1-kg/p/600050",
    "petdotu450": "https://www.petco.cl/petco-chile/es_CL/PRODUCTOS/Gato/Pro-Plan-Alimento-Seco-para-Gatitos-de-Todas-las-Razas%2C-1-kg/p/600048",
    "petdotu449": "https://www.petco.cl/petco-chile/es_CL/PRODUCTOS/Gato/Pro-Plan-Alimento-Seco-para-Gatitos-de-Todas-las-Razas%2C-1-kg/p/600044",
    "petdotu460": "https://www.petco.cl/petco-chile/es_CL/PRODUCTOS/Gato/Pro-Plan-Alimento-Seco-para-Gato-Esterilizado-de-Todas-las-Razas%2C-1-kg/p/600061",
    "petdotu459": "https://www.petco.cl/petco-chile/es_CL/PRODUCTOS/Gato/Pro-Plan-Alimento-Seco-para-Gato-Esterilizado-de-Todas-las-Razas%2C-1-kg/p/600047",
    "petdotu444": "https://www.petco.cl/petco-chile/es_CL/PRODUCTOS/Perro/Alimento/Alimento-Perros-Talla-Grande/Pro-Plan-Alimento-Seco-para-Cachorro-de-Razas-Medianas%2C-1-kg/p/600001",
    "petdotu424": "https://www.petco.cl/petco-chile/es_CL/MARCAS/Pro-Plan/Pro-Plan-Alimento-Avanzado-Seco-Optiderma-Cachorro-Sensitive-Skin-para-Cachorro-Receta-Cordero-y-Arroz%2C-3-kg/p/600030",
    "petdotu421": "https://www.petco.cl/petco-chile/es_CL/PRODUCTOS/Perro/Alimento/Alimento-Perros-Talla-Grande/Pro-Plan-Active-Mind-Alimento-Seco-para-Perro-Adulto-de-Razas-Medianas-y-Grandes%2C-15-kg/p/600013",
    "petdotu442": "https://www.petco.cl/petco-chile/es_CL/PRODUCTOS/Perro/Pro-Plan-Active-Mind-Alimento-Seco-para-Perro-Adulto-de-Razas-Peque%C3%B1as%2C-7-5-kg/p/600016",
    "petdotu317": "https://www.petco.cl/petco-chile/es_CL/PRODUCTOS/Perro/Alimento/Alimento-Perros-Talla-Peque%C3%B1a/Royal-Canin-Alimento-Seco-para-Perro-Bulldog-Frances-Adult%2C-7-5-kg/p/600638",
    "petdotu303": "https://www.petco.cl/petco-chile/es_CL/PRODUCTOS/Perro/Royal-Canin-Alimento-Seco-para-Cachorro-Raza-Mediana%2C-15-kg/p/600643",
    "petdotu309": "https://www.petco.cl/petco-chile/es_CL/PRODUCTOS/Gato/Royal-Canin-Savour-Selective-Alimento-Seco-para-Gato-Adulto-Paladar-Exigente-Receta-Pollo%2C-1-5-kg/p/600708",
    "petdotu311": "https://www.petco.cl/petco-chile/es_CL/PRODUCTOS/Gato/Royal-Canin-Alimento-Seco-para-Gato-Intense-Hairball%2C-1-5-kg/p/600718",
    "petdotu307": "https://www.petco.cl/petco-chile/es_CL/PRODUCTOS/Gato/Royal-Canin-Hairball-Alimento-Seco-para-Gato-Adulto-De-Interior-Control-Bolas-De-Pelo-Receta-Pollo%2C-7-5-kg/p/600721",
    "petdotu300": "https://www.petco.cl/petco-chile/es_CL/PRODUCTOS/Perro/Alimento/Alimento-Perros-Talla-Grande/Royal-Canin-Alimento-Seco-para-Perro-Adulto-Raza-Maxi%2C-15-kg/p/600655",
    "petdotu301": "https://www.petco.cl/petco-chile/es_CL/PRODUCTOS/Perro/Royal-Canin-Alimento-Seco-para-Perro-Junior-Maxi%2C-15-kg/p/600653",
    "petdotu304": "https://www.petco.cl/petco-chile/es_CL/PRODUCTOS/Perro/Royal-Canin-Alimento-Seco-para-Perro-Adulto-Raza-Peque%C3%B1a%2C-1-kg/p/600631",
    "petdotu313": "https://www.petco.cl/petco-chile/es_CL/PRODUCTOS/Gato/Royal-Canin-Alimento-Seco-para-Gato-Urinary%2C-7-5-kg/p/600719",
    "petdotu600":"https://www.petco.cl/petco-chile/es_CL/PRODUCTOS/Gato/Leonardo-Alimento-Natural-Seco-para-Adulto-Libre-de-Granos-Maxi-Gato%2C-7-5-kg/p/600457"
}
sku2 = {"petdotu97": "https://www.petco.cl/petco-chile/es_CL/PRODUCTOS/Perro/Salud-y-Bienestar/Estr%C3%A9s-y-Ansiedad/Ceva-Adaptil-Calm-Collar-con-Efecto-Calmante-para-Perro%2C-Mediano-Grande/p/122231"}
results = []

for sku_key, url in sku.items():
    driver.get(url)
    precio_oferta = "No disponible"
    precio_normal = "No disponible"
    time.sleep(1)
    try:
        # Intenta obtener el precio de oferta
        precio_oferta_element = driver.find_element("xpath", '/html/body/main/div[3]/div[2]/div[1]/div[5]/div/div/div[1]/div[2]/div[2]/div[1]/div/div/span[3]') #Cambiar
        precio_oferta = precio_oferta_element.text  # Guarda el precio de oferta
    except NoSuchElementException:
        pass  # Si no se encuentra el precio de oferta, se continuará con el siguiente bloque de código

    if precio_oferta == "No disponible" and precio_normal == "No disponible":
        try:
            # Si no se puede encontrar ni el precio de oferta ni el precio normal, intenta con el tercer XPath
            precio_normal_element = driver.find_element("xpath", '/html/body/main/div[3]/div[2]/div[1]/div[5]/div/div/div[1]/div[2]/div[2]/div[1]/div/div') #Cambiar
            precio_normal = precio_normal_element.text  # Guarda el precio normal
        except NoSuchElementException as e:
            pass
        
    if precio_oferta == "No disponible" and precio_normal == "No disponible":
        try:
            # Si no se puede encontrar ni el precio de oferta ni el precio normal, intenta con el tercer XPath
            precio_normal_element = driver.find_element("xpath", '/html/body/main/div[3]/div[2]/div[1]/div[5]/div/div/div[1]/div[2]/div[2]/div[1]/div/div') #Cambiar
            precio_normal = precio_normal_element.text  # Guarda el precio normal
        except NoSuchElementException as e:
            pass
    if precio_oferta == "No disponible" and precio_normal == "No disponible":
        try:
            # Intenta obtener el precio normal
            precio_normal_element = driver.find_element("xpath", '/html/body/main/div[3]/div[2]/div[1]/div[5]/div/div/div[1]/div[2]/div[2]/div[2]/div/div[2]/span[2]') #Cambiar
            precio_normal = precio_normal_element.text  # Guarda el precio normal
        except NoSuchElementException:
            pass  # Si no se encuentra el precio normal, se continuará con el siguiente bloque de código
        
    if precio_oferta == "No disponible" and precio_normal == "No disponible":
        try:
            # Si no se puede encontrar ni el precio de oferta ni el precio normal, intenta con el tercer XPath
            precio_normal_element = driver.find_element_by_class_name('discountedPrice') #Cambiar
            precio_normal = precio_normal_element.text  # Guarda el precio normal
        except NoSuchElementException as e:
            print(f"No se pudo encontrar el precio en la URL {url} - {e}")

    data = {
        "SKU": sku_key,
        "Precio": precio_normal,
        "Precio_oferta": precio_oferta
    }
    results.append(data)
    print(data)
    time.sleep(1.5)
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
							range='petco!K2',#CAMBIAR
							valueInputOption='USER_ENTERED',
							body={'values':values}).execute()


#Valores que se pasan a Sheets
values = [[item['SKU'], item['Precio'], item['Precio_oferta']] for item in results]
result = sheet.values().update(spreadsheetId=SPREADSHEET_ID,
							range='petco!A2:E',#CAMBIAR
							valueInputOption='USER_ENTERED',
							body={'values':values}).execute()
print(f"Datos insertados correctamente")


df = pd.DataFrame(results)
print(df)
print(df.head)
        

competitor = "Petco"  # Cambiar 
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

# # Obtener la última fila con datos en la nueva hoja
# result = sheet.values().get(spreadsheetId=NEW_SPREADSHEET_ID, range='stock!A:A').execute()  # Cambiar donde llega la info
# values = result.get('values', [])
# last_row = len(values) + 1  # Obtener el índice de la última fila vacía
# # Convertir resultados a la lista de valores
# values = [[now_str, competitor,row['SKU'], row['Stock']] for _, row in df.iterrows()]

# # Insertar los resultados en la nueva hoja después de la última fila
# print(values)
# update_range = f'Stock!A{last_row}:E{last_row + len(values) - 1}'  # Cambiar
# result = sheet.values().update(
#     spreadsheetId=NEW_SPREADSHEET_ID,
#     range=update_range,
#     valueInputOption='USER_ENTERED',
#     body={'values': values}
# ).execute()

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
