import os
import time

# Lista de nombres de los scripts que deseas ejecutar
scripts = [
    "pawal.py",
    "drpet.py",
    "jardinzoo.py",
    "tusmascotas.py",
    "punto.py",
    "razas.py",
    "petco.py",
    "superzoo.py",
    "laika.py"
    
]

# Iteramos sobre la lista de scripts y los ejecutamos uno por uno
for script in scripts:
    # Construimos la ruta completa al script
    script_path = os.path.join(os.path.dirname(__file__), script)
    print(f"Ejecutando {script}...")
    # Ejecutamos el script
    exec(open(script_path).read())
    print(f"{script} ejecutado.")

# # Espera de 10 segundos antes de ejecutar el último script
print("Esperando 10 segundos antes de ejecutar estadopetvet.py...")
time.sleep(10)

# Ejecutamos estadopetvet.py
estadopetvet_script = os.path.join(os.path.dirname(__file__), "estadopetvet.py")
print(f"Ejecutando estadopetvet.py...")
exec(open(estadopetvet_script).read())
print(f"estadopetvet.py ejecutado.")
