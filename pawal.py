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
    "petdotu344": "https://pawal.cl/perros/477-674-hill-s-natural-jerky-mini-strips-with-real-chicken-dog-treat.html#/445-formato-200gr",
    "petdotu360": "https://pawal.cl/gatos/496-699-hills-science-diet-gato-senior-control-bolas-de-pelo.html#/453-formato-159_kg",
    "petdotu357": "https://pawal.cl/gatos/494-696-hill-s-science-diet-gato-adulto-control-bolas-de-pelo.html#/452-formato-317kg",
    "petdotu361": "https://pawal.cl/gatos/497-700-hill-s-science-diet-gato-adulto-peso-perfecto.html#/451-formato-136kg",
    "petdotu354": "https://pawal.cl/gatos/492-693-hill-s-science-diet-gato-senior-indoor-11.html#/443-formato-158kg",
    "petdotu337": "https://pawal.cl/perros/470-664-hill-s-science-diet-senior-7-razas-pequenas-pollo.html#/433-formato-204kg",
    "petdotu409": "https://pawal.cl/gatos/498-701-hill-s-science-diet-gato-adulto-digestion-perfecta.html#/443-formato-158kg",
    "petdotu408": "https://pawal.cl/perros/476-672-hill-s-science-diet-adulto-razas-medianas-digestion-perfecta.html#/443-formato-158kg",
    "petdotu407": "https://pawal.cl/perros/474-hill-s-science-diet-peso-perfecto-adulto-raza-pequena-y-mini.html",
    "petdotu410": "https://pawal.cl/perros/504-707-hill-s-science-diet-youthful-vitality-adult-7.html#/440-formato-159kg",
    "petdotu323": "https://pawal.cl/perros/466-657-hill-s-science-diet-adulto-raza-pequena-pollo.html#/439-formato-226kg",
    "petdotu324": "https://pawal.cl/perros/466-658-hill-s-science-diet-adulto-raza-pequena-pollo.html#/437-formato-68kg",
    "petdotu321": "https://pawal.cl/perros/463-653-hill-s-science-diet-adulto-light.html#/437-formato-68kg",
    "petdotu332": "https://pawal.cl/perros/467-659-hill-s-science-diet-adulto-light-razas-pequenas.html#/439-formato-226kg",
    "petdotu333": "https://pawal.cl/perros/467-660-hill-s-science-diet-adulto-light-razas-pequenas.html#/437-formato-68kg",
    "petdotu330": "https://pawal.cl/perros/463-654-hill-s-science-diet-adulto-light.html#/438-formato-136kg",
    "petdotu343": "https://pawal.cl/perros/475-671-hill-s-science-diet-peso-perfecto-adulto-razas-medianas.html#/437-formato-68kg",
    "petdotu340": "https://pawal.cl/perros/472-667-hill-s-science-diet-adulto-razas-minis-y-toy-estomago-piel-sensible.html#/442-formato-181kg",
    "petdotu331": "https://pawal.cl/perros/464-655-hill-s-science-diet-adulto-razas-mini-y-toy-pollo-y-arroz.html#/433-formato-204kg",
    "petdotu322": "https://pawal.cl/perros/465-656-hill-s-science-diet-adulto-razas-mini-y-toy.html#/433-formato-204kg",
    "petdotu366": "https://pawal.cl/perros/501-704-hill-s-science-diet-adulto-raza-grande.html#/454-formato-158kg",
    "petdotu348": "https://pawal.cl/gatos/486-685-hill-s-science-diet-adulto-pollo.html#/448-formato-318kg",
    "petdotu349": "https://pawal.cl/gatos/486-686-hill-s-science-diet-adulto-pollo.html#/450-formato-726kg",
    "petdotu353": "https://pawal.cl/gatos/490-691-hill-s-science-diet-gato-senior-7.html#/442-formato-181kg",
    "petdotu356": "https://pawal.cl/gatos/494-695-hill-s-science-diet-gato-adulto-control-bolas-de-pelo.html#/440-formato-159kg",
    "petdotu358": "https://pawal.cl/gatos/494-697-hill-s-science-diet-gato-adulto-control-bolas-de-pelo.html#/434-formato-703kg",
    "petdotu359": "https://pawal.cl/gatos/495-698-hill-s-science-diet-gato-adulto-light-control-bolas-de-pelo.html#/440-formato-159kg",
    "petdotu352": "https://pawal.cl/gatos/488-689-hill-s-science-diet-adulto-gato-indoor.html#/440-formato-159kg",
    "petdotu362": "https://pawal.cl/gatos/499-702-hill-s-science-diet-gato-adulto-estomago-y-piel-sensible.html#/443-formato-158kg",
    "petdotu350": "https://pawal.cl/gatos/487-687-hill-s-science-diet-adulto-light-gato.html#/442-formato-181kg",
    "petdotu351": "https://pawal.cl/gatos/487-688-hill-s-science-diet-adulto-light-gato.html#/448-formato-318kg",
    "petdotu402": "https://pawal.cl/gatos/541-764-hill-s-prescription-diet-s-d-cuidado-uranario-felino.html#/442-formato-181kg",
    "petdotu404": "https://pawal.cl/gatos/491-692-hill-s-science-diet-gato-senior-indoor-7.html#/443-formato-158kg",
    "petdotu355": "https://pawal.cl/gatos/493-694-hill-s-science-diet-youthful-vitality-gato-adulto-senior-7-pollo.html#/451-formato-136kg",
    "petdotu399": "https://pawal.cl/gatos/538-761-hill-s-prescription-diet-y-d-cuidado-de-tiroides-felino.html#/442-formato-181kg",
    "petdotu345": "https://pawal.cl/gatos/483-680-hill-s-science-diet-kitten-pollo.html#/440-formato-159kg",
    "petdotu346": "https://pawal.cl/gatos/483-681-hill-s-science-diet-kitten-pollo.html#/448-formato-318kg",
    "petdotu403": "https://pawal.cl/gatos/484-682-hill-s-science-diet-kitten-indoor.html#/440-formato-159kg",
    "petdotu347": "https://pawal.cl/gatos/484-683-hill-s-science-diet-kitten-indoor.html#/448-formato-318kg",
    "petdotu405": "https://pawal.cl/perros/506-709-hill-s-prescription-diet-c-d-urinary-care-multicare-canino.html#/443-formato-158kg",
    "petdotu368": "https://pawal.cl/perros/506-710-hill-s-prescription-diet-c-d-urinary-care-multicare-canino.html#/455-formato-386kg",
    "petdotu369": "https://pawal.cl/perros/506-711-hill-s-prescription-diet-c-d-urinary-care-multicare-canino.html#/456-formato-798kg",
    "petdotu390": "https://pawal.cl/gatos/529-749-hill-s-prescription-diet-c-d-multicare-felino-pollo.html#/464-formato-385kg",
    "petdotu370": "https://pawal.cl/perros/507-712-hill-s-prescription-diet-h-d-heart-care-canino.html#/443-formato-158kg",
    "petdotu391": "https://pawal.cl/gatos/532-752-hill-s-prescription-diet-i-d-cuidado-digestivo-felino.html#/442-formato-181kg",
    "petdotu371": "https://pawal.cl/perros/509-715-hill-s-prescription-diet-i-d-low-fat-canino-raza-grande.html#/455-formato-386kg",
    "petdotu375": "https://pawal.cl/perros/511-719-hill-s-prescription-diet-j-d-cuidado-articular-canino.html#/455-formato-386kg",
    "petdotu376": "https://pawal.cl/perros/511-720-hill-s-prescription-diet-j-d-cuidado-articular-canino.html#/458-formato-1247kg",
    "petdotu377": "https://pawal.cl/perros/2107-3279-hill-s-prescription-diet-k-d-cuidado-renal-canino.html#/443-formato-158kg",
    "petdotu378": "https://pawal.cl/perros/2107-3277-hill-s-prescription-diet-k-d-cuidado-renal-canino.html#/455-formato-386kg",
    "petdotu379": "https://pawal.cl/perros/2107-3278-hill-s-prescription-diet-k-d-cuidado-renal-canino.html#/456-formato-798kg",
    "petdotu392": "https://pawal.cl/gatos/534-754-hill-s-prescription-diet-k-d-cuidado-renal-felino.html#/442-formato-181kg",
    "petdotu393": "https://pawal.cl/gatos/534-755-hill-s-prescription-diet-k-d-cuidado-renal-felino.html#/464-formato-385kg",
    "petdotu380": "https://pawal.cl/perros/515-726-hill-s-prescription-diet-l-d-cuidado-hepatico-canino.html#/456-formato-798kg",
    "petdotu406": "https://pawal.cl/perros/520-735-hill-s-prescription-diet-metabolic-mobility-canine.html#/455-formato-386kg",
    "petdotu394": "https://pawal.cl/gatos/535-756-hill-s-prescription-diet-metabolic-control-peso-felino.html#/442-formato-181kg",
    "petdotu395": "https://pawal.cl/gatos/535-757-hill-s-prescription-diet-metabolic-control-peso-felino.html#/464-formato-385kg",
    "petdotu396": "https://pawal.cl/gatos/536-758-hill-s-prescription-diet-metabolic-urinary-felino.html#/465-formato-288kg",
    "petdotu397": "https://pawal.cl/gatos/537-759-hill-s-prescription-diet-r-d-control-de-peso-felino.html#/442-formato-181kg",
    "petdotu398": "https://pawal.cl/gatos/537-760-hill-s-prescription-diet-r-d-control-de-peso-felino.html#/464-formato-385kg",
    "petdotu387": "https://pawal.cl/perros/524-740-hill-s-prescription-diet-w-d-multi-beneficios-canino.html#/443-formato-158kg",
    "petdotu388": "https://pawal.cl/perros/524-742-hill-s-prescription-diet-w-d-multi-beneficios-canino.html#/456-formato-798kg",
    "petdotu400": "https://pawal.cl/gatos/539-762-hill-s-prescription-diet-w-d-multi-benefit-felino.html#/442-formato-181kg",
    "petdotu389": "https://pawal.cl/perros/525-743-hill-s-prescription-diet-z-d-sensibilidad-cutanea-alergias-alimentarias-sabor-original.html#/461-formato-363kg",
    "petdotu401": "https://pawal.cl/gatos/540-763-hill-s-prescription-diet-z-d-sensibilidad-cutanea-alergias-alimentarias-felino.html#/442-formato-181kg",
    "petdotu325": "https://pawal.cl/perros/458-645-hill-s-science-diet-puppy-chicken-meal-barley-recipe.html#/433-formato-204kg",
    "petdotu326": "https://pawal.cl/perros/458-646-hill-s-science-diet-puppy-chicken-meal-barley-recipe.html#/434-formato-703kg",
    "petdotu327": "https://pawal.cl/perros/458-647-hill-s-science-diet-puppy-chicken-meal-barley-recipe.html#/435-formato-1361kg",
    "petdotu320": "https://pawal.cl/perros/460-649-hill-s-science-diet-puppy-small-bites-chicken-barley-recipe-dog-food.html#/433-formato-204kg",
    "petdotu329": "https://pawal.cl/perros/460-650-hill-s-science-diet-puppy-small-bites-chicken-barley-recipe-dog-food.html#/434-formato-703kg",
    "petdotu328": "https://pawal.cl/perros/459-648-hill-s-science-diet-puppy-small-paws-chicken-meal-barley-brown-rice-recipe.html#/433-formato-204kg",
    "petdotu339": "https://pawal.cl/perros/471-666-hill-s-science-diet-senior-7-razas-minis-y-toy.html#/441-formato-565kg",
    "petdotu338": "https://pawal.cl/perros/471-665-hill-s-science-diet-senior-7-razas-minis-y-toy.html#/440-formato-159kg",
    "petdotu432": "https://pawal.cl/perros/141-240-pro-plan-sensitive-skin-and-stomach-adulto-razas-pequenas.html#/345-size-75kg",
    "petdotu425": "https://pawal.cl/perros/137-233-pro-plan-adulto-todo-tamano-sensitive-skin-cordero.html#/340-size-15kg",
    "petdotu458": "https://pawal.cl/gatos/155-270-pro-plan-adulto-sensitive.html#/341-size-3kg",
    "petdotu457": "https://pawal.cl/gatos/154-269-pro-plan-adultos.html#/341-size-3kg",
    "petdotu435": "https://pawal.cl/perros/142-3411-pro-plan-adulto-rz-mediana-grande-reduced-calorie.html#/683-formato-3kg",
    "petdotu434": "https://pawal.cl/perros/142-3414-pro-plan-adulto-rz-mediana-grande-reduced-calorie.html#/685-formato-15kg",
    "petdotu428": "https://pawal.cl/perros/138-236-pro-plan-adulto-rz-mediana-grande-sensitive-skin.html#/341-size-3kg",
    "petdotu427": "https://pawal.cl/perros/138-235-pro-plan-adulto-rz-mediana-grande-sensitive-skin.html#/340-size-15kg",
    "petdotu429": "https://pawal.cl/perros/139-237-pro-plan-adulto-raza-pequena-sensitive-skin.html#/341-size-3kg",
    "petdotu437": "https://pawal.cl/perros/144-246-pro-plan-adulto-raza-mediana.html#/341-size-3kg",
    "petdotu415": "https://pawal.cl/perros/144-245-pro-plan-adulto-raza-mediana.html#/340-size-15kg",
    "petdotu438": "https://pawal.cl/perros/146-249-pro-plan-adulto-raza-pequena.html#/341-size-3kg",
    "petdotu417": "https://pawal.cl/perros/146-248-pro-plan-adulto-raza-pequena.html#/345-size-75kg",
    "petdotu441": "https://pawal.cl/perros/147-252-pro-plan-adulto-raza-pequena-exigent.html#/341-size-3kg",
    "petdotu440": "https://pawal.cl/perros/147-251-pro-plan-adulto-raza-pequena-exigent.html#/345-size-75kg",
    "petdotu431": "https://pawal.cl/perros/140-239-pro-plan-sensitive-skin-and-stomach-adulto-razas-medianas-y-grandes.html#/341-size-3kg",
    "petdotu416": "https://pawal.cl/perros/145-247-pro-plan-adulto-raza-grande.html#/340-size-15kg",
    "petdotu462": "https://pawal.cl/gatos/158-274-pro-plan-adulto-7.html#/341-size-3kg",
    "petdotu456": "https://pawal.cl/gatos/154-268-pro-plan-adultos.html#/345-size-75kg",
    "petdotu453": "https://pawal.cl/gatos/152-265-pro-plan-adulto-live-clear.html#/370-size-1kg",
    "petdotu452": "https://pawal.cl/gatos/152-264-pro-plan-adulto-live-clear.html#/341-size-3kg",
    "petdotu455": "https://pawal.cl/gatos/153-267-pro-plan-adulto-urinary.html#/341-size-3kg",
    "petdotu454": "https://pawal.cl/gatos/153-266-pro-plan-adulto-urinary.html#/345-size-75kg",
    "petdotu451": "https://pawal.cl/gatos/151-263-pro-plan-gatitos-kitten.html#/370-size-1kg",
    "petdotu450": "https://pawal.cl/gatos/151-262-pro-plan-gatitos-kitten.html#/341-size-3kg",
    "petdotu449": "https://pawal.cl/gatos/151-261-pro-plan-gatitos-kitten.html#/345-size-75kg",
    "petdotu461": "https://pawal.cl/gatos/157-273-pro-plan-adulto-reduced-calorie.html#/341-size-3kg",
    "petdotu460": "https://pawal.cl/gatos/156-272-pro-plan-adulto-esterilizado.html#/341-size-3kg",
    "petdotu459": "https://pawal.cl/gatos/156-271-pro-plan-adulto-esterilizado.html#/345-size-75kg",
    "petdotu418": "https://pawal.cl/perros/150-258-pro-plan-cachorro-raza-grande.html#/340-size-15kg",
    "petdotu446": "https://pawal.cl/perros/149-257-pro-plan-cachorro-raza-mediana.html#/341-size-3kg",
    "petdotu444": "https://pawal.cl/perros/149-255-pro-plan-cachorro-raza-mediana.html#/340-size-15kg",
    "petdotu424": "https://pawal.cl/perros/136-232-pro-plan-cachorro-todo-tamano-sensitive-skin-cordero.html#/341-size-3kg",
    "petdotu423": "https://pawal.cl/perros/136-231-pro-plan-cachorro-todo-tamano-sensitive-skin-cordero.html#/340-size-15kg",
    "petdotu422": "https://pawal.cl/perros/135-230-pro-plan-adulto-7-raza-mediana-y-grande-senior.html#/341-size-3kg",
    "petdotu421": "https://pawal.cl/perros/135-229-pro-plan-adulto-7-raza-mediana-y-grande-senior.html#/340-size-15kg",
    "petdotu443": "https://pawal.cl/perros/148-254-pro-plan-adulto-7-raza-pequena.html#/341-size-3kg",
    "petdotu442": "https://pawal.cl/perros/148-253-pro-plan-adulto-7-raza-pequena.html#/345-size-75kg",
    "petdotu302": "https://pawal.cl/perros/951-1199-royal-canin-medium-adulto-seco-size-health-nutrition.html#/427-formato-15kg",
    "petdotu309": "https://pawal.cl/gatos/871-1091-royal-canin-exigent-seco-feline-health-nutrition.html#/470-formato-15kg",
    "petdotu311": "https://pawal.cl/gatos/862-1079-royal-canin-intense-hairball-seco-feline-care-nutrition.html#/470-formato-15kg",
    "petdotu307": "https://pawal.cl/gatos/867-2953-royal-canin-indoor-feline-seco-feline-health-nutrition.html#/682-formato-75kg",
    "petdotu300": "https://pawal.cl/perros/955-3051-royal-canin-maxi-adulto-seco-size-health-nutrition.html#/685-formato-15kg",
    "petdotu301": "https://pawal.cl/perros/954-1202-royal-canin-maxi-puppy-seco-size-health-nutrition.html#/427-formato-15kg",
    "petdotu304": "https://pawal.cl/perros/949-3042-royal-canin-mini-adulto-seco-size-health-nutrition.html#/682-formato-75kg",
    "petdotu305": "https://pawal.cl/perros/947-3686-royal-canin-mini-puppy-seco-size-health-nutrition.html#/469-formato-75kg",
    "petdotu318": "https://pawal.cl/inicio/2689-4575-royal-canin-persian-.html#/470-formato-15kg",
    "petdotu319": "https://pawal.cl/perros/912-2988-royal-canin-poodle-adulto-seco-breed-health-nutrition.html#/682-formato-75kg",
    "petdotu313": "https://pawal.cl/gatos/860-2942-royal-canin-urinary-care-seco-feline-care-nutrition.html#/681-formato-15kg",
    "petdotu316": "https://pawal.cl/gatos/860-2943-royal-canin-urinary-care-seco-feline-care-nutrition.html#/682-formato-75kg",
    "petdotu600":"https://pawal.cl/gatos/88-2884-leonardo-adulto-maxi-gf.html#/682-formato-75kg"

}
sku2 = {"petdotu1": "https://pawal.cl/perros/466-657-hill-s-science-diet-adulto-raza-pequena-pollo.html#/439-formato-226kg"}


results = []

for sku_key, url in sku.items():
    driver.get(url)
    precio_oferta = "No disponible"    
    precio_normal = "No disponible"
    stock= "Con Stock"
    try:
        # Intenta obtener el precio de oferta
        precio_oferta_element = driver.find_element(By.XPATH, '/html/body/main/section/div[2]/div/section/div[2]/div[1]/div[2]/div/div[2]/div[2]/form/div[2]/div/div[1]/div') #Cambiar
        precio_oferta = precio_oferta_element.text  # Guarda el precio de oferta
        stock_element= driver.find_element(By.ID,"product-availability")
        stock=stock_element.text
    except NoSuchElementException:
        pass 

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
							range='pawal!K2',#CAMBIAR
							valueInputOption='USER_ENTERED',
							body={'values':values}).execute()


#Valores que se pasan a Sheets
values = [[item['SKU'], item['Precio'],item['Precio_oferta']] for item in results]
result = sheet.values().update(spreadsheetId=SPREADSHEET_ID,
							range='pawal!A2:C',#CAMBIAR
							valueInputOption='USER_ENTERED',
							body={'values':values}).execute()
print(f"Datos insertados correctamente")        

#Valores que se pasan a Sheets
values = [[item['Stock']] for item in results]
result = sheet.values().update(spreadsheetId=SPREADSHEET_ID,
							range='pawal!M2:N',#CAMBIAR
							valueInputOption='USER_ENTERED',
							body={'values':values}).execute()
print(f"Datos insertados correctamente")        



competitor = "Pawal"  # Cambiar 
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
