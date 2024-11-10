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
    "petdotu344": "https://puntomascotas.cl/golosinas-y-huesos-para-perros/35333-golosina-hills-science-diet-jercky-snack-052742187501.html",
    "petdotu360": "https://puntomascotas.cl/gato-senior/34478-hills-felino-mature-7-hairball-control-158-kg-052742753300.html",
    "petdotu357": "https://puntomascotas.cl/cats/31980-hills-feline-hair-ball-control-317kg-052742888101.html",
    "petdotu361": "https://puntomascotas.cl/hills/36349-hills-perfect-weight-adulto-136-kg-052742296807.html",
    "petdotu354": "https://puntomascotas.cl/hills/36257-hills-indoor-age-defying-11-15kg-052742252902.html",
    "petdotu337": "https://puntomascotas.cl/dogs/33448-hills-mature-small-toy-breed-2-kg-052742909806.html",
    "petdotu409": "https://puntomascotas.cl/cats/39722-hills-felino-adulto-perfect-digestion-158-kg-052742038315.html",
    "petdotu324": "https://puntomascotas.cl/dogs/37734-hills-prescription-diet-canine-c-d-385-kg-052742020488.html",
    "petdotu321": "https://puntomascotas.cl/perros-adulto/41103-hills-adulto-canine-light-68kg-052742022147.html",
    "petdotu330": "https://puntomascotas.cl/perros-adulto/30624-hills-adulto-canine-light-136kg-052742022192.html",
    "petdotu333": "https://puntomascotas.cl/hills/31974-hills-canine-adulto-light-small-bites-79kg-052742022130.html",
    "petdotu331": "https://puntomascotas.cl/dogs/33177-hills-adulto-small-toy-204kg-052742909608.html",
    "petdotu366": "https://puntomascotas.cl/hills/40903-hills-adulto-large-15-kg-052742016054.html",
    "petdotu348": "https://puntomascotas.cl/cats/30618-hills-cat-adulto-ocean-18kg-052742204505.html",
    "petdotu349": "https://puntomascotas.cl/cats/34781-hills-feline-adulto-optimal-care-798kg-052742006437.html",
    "petdotu353": "https://puntomascotas.cl/cats/31715-hills-feline-active-longevity-18kg-052742710402.html",
    "petdotu356": "https://puntomascotas.cl/hills-gatos/30343-hills-hairbal-control-158-052742715605.html",
    "petdotu358": "https://puntomascotas.cl/cats/31981-hills-feline-hair-ball-control-7kg-052742887500.html",
    "petdotu359": "https://puntomascotas.cl/cats/31983-hills-feline-hair-ball-light-317kg-052742888200.html",
    "petdotu352": "https://puntomascotas.cl/cats/34206-indoor-hills-16-052742553207.html",
    "petdotu362": "https://puntomascotas.cl/hills/34476-hills-felino-adulto-estomago-y-piel-sensibles-158-kg-052742852300.html",
    "petdotu350": "https://puntomascotas.cl/cats/30344-hills-hairbal-control-158-052742671109.html",
    "petdotu351": "https://puntomascotas.cl/cats/31982-hills-feline-adulto-light-36kg-052742204703.html",
    "petdotu404": "https://puntomascotas.cl/hills/34480-hills-adulto-7-indoor-158-kg-052742644608.html",
    "petdotu355": "https://puntomascotas.cl/hills/36504-hills-feline-senior-vitality-136-kg-052742012117.html",
    "petdotu399": "https://puntomascotas.cl/cats/32037-hills-feline-prescription-diet-y-d-18kg-052742149707.html",
    "petdotu345": "https://puntomascotas.cl/cats/30681-hills-kitten-healty-development-15-kg-052742712307.html",
    "petdotu346": "https://puntomascotas.cl/cats/31977-hills-feline-kitten-develop-317kg-052742939100.html",
    "petdotu403": "https://puntomascotas.cl/cats/35830-hills-adulto-indoor-kitten-158-kg-052742713106.html",
    "petdotu347": "https://puntomascotas.cl/cats/35829-hills-adulto-indoor-kitten-158-kg-052742937809.html",
    "petdotu368": "https://puntomascotas.cl/dogs/30324-hills-prescription-diet-canine-c-d-385-kg-052742001746.html",
    "petdotu369": "https://puntomascotas.cl/dogs/32001-hills-canine-prescription-diet-c-d-798kg-052742001661.html",
    "petdotu390": "https://puntomascotas.cl/cats/30553-hills-felino-c-d-18kg-052742867908.html",
    "petdotu391": "https://puntomascotas.cl/cats/30620-hills-felino-c-d-18kg-052742462905.html",
    "petdotu371": "https://puntomascotas.cl/h/34623-hills-canine-prescription-diet-i-d-low-fat-385kg-052742186108.html",
    "petdotu376": "https://puntomascotas.cl/perros-necesidades-especificas/32012-hills-canine-prescription-diet-j-d-125kg-052742859804.html",
    "petdotu377": "https://puntomascotas.cl/dogs/34426-hills-canine-prescription-diet-k-d-2kg-052742001197.html",
    "petdotu378": "https://puntomascotas.cl/dogs/30325-hills-prescription-diet-canine-c-d-385-kg-052742862101.html",
    "petdotu379": "https://puntomascotas.cl/dogs/31716-hills-canine-prescription-diet-k-d-798kg-052742862200.html",
    "petdotu392": "https://puntomascotas.cl/cats/30346-hills-felino-k-d-18kg-052742725208.html",
    "petdotu393": "https://puntomascotas.cl/cats/30552-hills-felino-k-d-18kg-052742869605.html",
    "petdotu380": "https://puntomascotas.cl/dogs/32015-hills-canine-prescription-diet-l-d-798kg-052742862309.html",
    "petdotu394": "https://puntomascotas.cl/cats/32383-hills-feline-metabolic-18-kg-052742195407.html",
    "petdotu395": "https://puntomascotas.cl/cats/33010-prescription-diet-metabolic-cat-052742195506.html",
    "petdotu396": "https://puntomascotas.cl/cats/34124-metabolic-urinary-gato-288-kg-052742000732.html",
    "petdotu397": "https://puntomascotas.cl/cats/30347-hills-felino-r-d-18kg-052742615806.html",
    "petdotu398": "https://puntomascotas.cl/hills/32034-hills-feline-prescription-diet-r-d-385kg-052742589800.html",
    "petdotu386": "https://puntomascotas.cl/dogs/32022-hills-canine-prescription-diet-u-d-385kg-052742867007.html",
    "petdotu388": "https://puntomascotas.cl/dogs/32026-hills-canine-prescription-diet-w-d-798kg-052742867205.html",
    "petdotu400": "https://puntomascotas.cl/cats/32035-hills-feline-prescription-diet-w-d-18kg-052742615905.html",
    "petdotu389": "https://puntomascotas.cl/dogs/32031-hills-canine-prescription-z-d-ultra-allergie-36kg-052742790107.html",
    "petdotu401": "https://puntomascotas.cl/cats/32039-hills-feline-prescription-diet-z-d-18kg-allergen-052742790503.html",
    "petdotu327": "https://puntomascotas.cl/dogs/31948-hills-puppy-136-kg-052742936703.html",
    "petdotu320": "https://puntomascotas.cl/dogs/30683-hills-puppy-small-bites-2-kg-052742713908.html",
    "petdotu328": "https://puntomascotas.cl/dogs/33178-hills-puppy-small-toy-204kg-052742909400.html",
    "petdotu338": "https://puntomascotas.cl/dogs/36505-youthful-vitality-perros-158kg-052742012032.html",
    "petdotu432": "https://puntomascotas.cl/dogs/39924-pro-plan-adult-small-sensitive-skin-and-stomach-75-kg-7613287415011.html",
    "petdotu425": "https://puntomascotas.cl/pro-plan/35807-pro-plan-adult-sensible-support-cordero-arroz-123kg-7613287036162.html",
    "petdotu457": "https://puntomascotas.cl/cats/57-purina-pro-plan-cat-chicken-rice-7613039900277.html",
    "petdotu434": "https://puntomascotas.cl/dogs/142-pro-plan-reduced-calorie-123-kg--7613287033130.html",
    "petdotu428": "https://puntomascotas.cl/dogs/30020-pro-plan-adult-sensitive-salmon-rice-15-kg--7613287033208.html",
    "petdotu427": "https://puntomascotas.cl/dogs/143-pro-plan-adult-sensitive-salmon-rice-15-kg--7613287035011.html",
    "petdotu429": "https://puntomascotas.cl/pro-plan/35299-pro-plan-reduce-calorie-small-breed-3-kg-7613287033161.html",
    "petdotu437": "https://puntomascotas.cl/dogs/135-pro-plan-adult-complete-protection-con-optilife-3-kg--7613287031051.html",
    "petdotu415": "https://puntomascotas.cl/pro-plan/137-pro-plan-adult-complete-protection-con-optilife-123-kg--7613287031082.html",
    "petdotu438": "https://puntomascotas.cl/dogs/30024-pro-plan-aduto-small-breed-3-kg--7613287029195.html",
    "petdotu417": "https://puntomascotas.cl/dogs/136-pro-plan-adult-complete-protection-con-optilife-75-kg--7613287029515.html",
    "petdotu441": "https://puntomascotas.cl/dogs/33041-pro-plan-delicate-small-breed-3kg--7613287035196.html",
    "petdotu440": "https://puntomascotas.cl/dogs/35448-pro-plan-delicate-small-breed-3kg--7613287035264.html",
    "petdotu431": "https://puntomascotas.cl/dogs/39923-pro-plan-adult-medium-y-grande-sensitive-skin-and-stomach-3-kg-7613287415035.html",
    "petdotu416": "https://puntomascotas.cl/dogs/30023-pro-plan-aduto-large-breed-123-kg--7613287031570.html",
    "petdotu462": "https://puntomascotas.cl/cats/35521-pro-plan-cat-vital-age-proteciton-15-kg-7613039946886.html",
    "petdotu456": "https://puntomascotas.cl/cats/33510-purina-pro-plan-cat-chicken-rice-7613039899922.html",
    "petdotu452": "https://puntomascotas.cl/cats/39052-pro-plan-cat-live-clear-3-kg-7613287119629.html",
    "petdotu455": "https://puntomascotas.cl/cats/30022-pro-plan-cat-urinary-care-protection-3-kg-7613039947111.html",
    "petdotu454": "https://puntomascotas.cl/cats/33511-pro-plan-cat-urinary-care-protection-15-kg--7613039947739.html",
    "petdotu451": "https://puntomascotas.cl/cats/34179-pro-plan-kitten-15-kg--7613039886557.html",
    "petdotu450": "https://puntomascotas.cl/cats/34920-pro-plan-kitten-3-kg-7613039886922.html",
    "petdotu449": "https://puntomascotas.cl/cats/33509-pro-plan-kitten-15-kg--7613039784914.html",
    "petdotu460": "https://puntomascotas.cl/cats/34214-pro-plan-cat-sterilized-3kg-7613039947784.html",
    "petdotu459": "https://puntomascotas.cl/cats/35589-pro-plan-cat-sterilized-75kg-7613039947661.html",
    "petdotu418": "https://puntomascotas.cl/dogs/30033-pro-plan-puppy-large-breed-123-kg-7613287029034.html",
    "petdotu446": "https://puntomascotas.cl/dogs/138-pro-plan-puppy-complete-protection-con-optistartplus-3-kg--7613287028204.html",
    "petdotu444": "https://puntomascotas.cl/dogs/140-pro-plan-puppy-complete-protection-con-optistartplus-123-kg--7613287028549.html",
    "petdotu424": "https://puntomascotas.cl/dogs/35806-pro-plan-puppy-sensitive-support-3-kg-7613287035929.html",
    "petdotu421": "https://puntomascotas.cl/pro-plan/35450-pro-plan-active-mind-adult-7-123kg-7613287032911.html",
    "petdotu443": "https://puntomascotas.cl/pro-plan/35478-pro-plan-active-mind-raza-pequena-3-kg-7613287031969.html",
    "petdotu442": "https://puntomascotas.cl/pro-plan/36206-pro-plan-active-mind-raza-pequena-75-kg-7613287031983.html",
    "petdotu302": "https://puntomascotas.cl/dogs/30076-royal-canin-medium-adulto-15kg-7896181211884.html",
    "petdotu309": "https://puntomascotas.cl/cats/34946-royal-canin-special-exigent-3530-2kg-7896181213154.html",
    "petdotu307": "https://puntomascotas.cl/cats/32920-royal-canin-indoor-27-10kg-7790187338722.html",
    "petdotu300": "https://puntomascotas.cl/dogs/30082-royal-canin-maxi-adulto-15kg-7896181211822.html",
    "petdotu301": "https://puntomascotas.cl/dogs/30081-royal-canin-maxi-junior-15kg-7896181212324.html",
    "petdotu304": "https://puntomascotas.cl/dogs/30300-royal-canin-mini-adulto-75kg-7896181212102.html",
    "petdotu305": "https://puntomascotas.cl/dogs/30631-royal-canin-mini-junior-3kg-7790187339637.html",
    "petdotu318": "https://puntomascotas.cl/cats/30110-royal-canin-breed-nutrition-persian-30-2kg-7790187339422.html",
    "petdotu319": "https://puntomascotas.cl/dogs/34791-royal-canin-poodle-3kg-7790187341746.html",
    "petdotu313": "https://puntomascotas.cl/royal-canin/34468-royal-canin-urinary-care-15kg-7790187340350.html",
    "petdotu316": "https://puntomascotas.cl/cats/34469-royal-canin-urinary-care-15kg-7790187340367.html",
    "petdotu341": "https://puntomascotas.cl/hills/41354-hills-adulto-estomago-piel-sensible-181-kg-52742057545.html",
    "petdotu436": "https://puntomascotas.cl/dogs/35300-pro-plan-reduced-calorie-razas-pequenas-con-optifit--7613287032942.html",
    "petdotu433": "https://puntomascotas.cl/dogs/39920-pro-plan-adult-small-sensitive-skin-and-stomach-3-kg-7613287414922.html",
    "petdotu306": "https://puntomascotas.cl/dogs/30086-royal-canin-giant-puppy-15kg-7790187339811.html",
    "petdotu303": "https://puntomascotas.cl/dogs/30074-royal-canin-medium-junior-15kg-7896181211921.html",
    "petdotu310": "https://puntomascotas.cl/cats/35474-royal-canin-special-sensible-33-2kg-7790187339484.html",
    "petdotu314": "https://puntomascotas.cl/cats/36596-royal-canin-vet-felino-urinary-so-feline-75kg-7790187340251.html",
    "petdotu382": "https://puntomascotas.cl/h/30678-hills-prescription-diet-r-d-38-kg-052742862408.html",
    "petdotu383": "https://puntomascotas.cl/perros-necesidades-especificas/32018-hills-canine-prescription-diet-r-d-798kg-052742862507.html",
    "petdotu365": "https://puntomascotas.cl/dogs/34561-hills-adult-canine-original-174kg-052742648804.html",
    "petdotu373": "https://puntomascotas.cl/dogs/32009-hills-canine-prescription-diet-id-385kg-id-052742861807.html",
    "petdotu430": "https://puntomascotas.cl/dogs/39919-pro-plan-adult-small-and-medium-sensitive-skin-and-stomach-123-kg-7613287415059.html",
    "petdotu426": "https://puntomascotas.cl/pro-plan/35808-pro-plan-adult-sensible-support-cordero-arroz-15kg-7613287036100.html",
    "petdotu374": "https://puntomascotas.cl/dogs/32010-hills-canine-prescription-diet-i-d-798kg-052742861906.html",
    "petdotu384": "https://puntomascotas.cl/dogs/37445-hills-canine-prescription-diet-metabolic-349-kg-052742022369.html",
    "petdotu385": "https://puntomascotas.cl/dogs/32877-hills-canine-prescription-diet-metabolic-125-kg-052742195308.html",
    "petdotu372": "https://puntomascotas.cl/dogs/36400-hills-canine-prescription-diet-id-15kg-id-052742014296.html",
    "petdotu367": "https://puntomascotas.cl/hills/37446-hills-adult-7-small-bites-68-kg-052742057569.html",
    "petdotu412": "https://puntomascotas.cl/dogs/31970-hills-canine-senior-small-bites-2kg-052742005355.html",
    "petdotu413": "https://puntomascotas.cl/hills/37446-hills-adult-7-small-bites-68-kg-052742057569.html",
    "petdotu411": "https://puntomascotas.cl/hills/41353-hills-senior-active-longevity-3-kg-052742693804.html",
    "petdotu312": "https://puntomascotas.cl/royal-canin/30108-royal-canin-weight-care-15kg-7790187340527.html",
    "petdotu335": "https://puntomascotas.cl/hills/41353-hills-senior-active-longevity-3-kg-052742693804.html",
    "petdotu600":"https://puntomascotas.cl/cats/38927-leonardo-adult-gf-maxi-75kg-4002633758521.html"
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
        precio_oferta_element = driver.find_element("xpath", '/html/body/main/section/div/div/div/div/div/section/div[1]/div[1]/div[2]/section/div[1]/div/div[5]/div/form/div[2]/div[1]/span[1]/span[1]') #Cambiar
        precio_oferta = precio_oferta_element.text  # Guarda el precio de oferta
        stock_element= driver.find_element(By.XPATH,"/html/body/main/section/div/div/div/div/div/section/div[1]/div[1]/div[2]/section/div[1]/div/div[2]")
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

      
#Fecha de Extraccion
now = datetime.datetime.now()
now_str = now.strftime('%Y-%m-%d %H:%M:%S')
data = {"":now_str}
json_data = json.dumps(data)
values = [[json_data]]
result = sheet.values().update(spreadsheetId=SPREADSHEET_ID,
							range='puntomascotas!K2',#CAMBIAR
							valueInputOption='USER_ENTERED',
							body={'values':values}).execute()


#Valores que se pasan a Sheets
values = [[item['SKU'], item['Precio'],item['Precio_oferta']] for item in results]
result = sheet.values().update(spreadsheetId=SPREADSHEET_ID,
							range='puntomascotas!A2:C',#CAMBIAR
							valueInputOption='USER_ENTERED',
							body={'values':values}).execute()
print(f"Datos insertados correctamente")        

#Valores que se pasan a Sheets
values = [[item['Stock']] for item in results]
result = sheet.values().update(spreadsheetId=SPREADSHEET_ID,
							range='puntomascotas!M2:N',#CAMBIAR
							valueInputOption='USER_ENTERED',
							body={'values':values}).execute()
print(f"Datos insertados correctamente")        


competitor = "Punto Mascotas"  # Cambiar 
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
