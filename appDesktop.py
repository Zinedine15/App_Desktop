import tkinter as tk
import requests
import socket
from datetime import datetime
from tkinter import scrolledtext

# URL de la API MockAPI
API_URL = "https://66eb02f255ad32cda47b5715.mockapi.io/IoTCarStatus"

# Función para obtener la IP local
def get_local_ip():
    return socket.gethostbyname(socket.gethostname())

# Función para enviar datos a la MockAPI
def send_data(action):
    ip = get_local_ip()
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Crear el payload que será enviado a MockAPI
    payload = {
        "status": action,
        "date": date,
        "ipClient": ip
    }

    # Enviar los datos usando POST
    response = requests.post(API_URL, json=payload)

    # Mostrar el status del último registro desde MockAPI
    update_last_status()

# Función para obtener y mostrar el status del último registro desde MockAPI
def update_last_status():
    response = requests.get(API_URL)
    if response.status_code == 200:
        data = response.json()
        if data:
            # Obtener el último registro
            last_record = data[-1]
            # Extraer el campo status del último registro
            last_status = last_record.get("status", "No encontrado")
            result_text.insert(tk.END, f"Último status registrado: {last_status}\n")
        else:
            result_text.insert(tk.END, "No hay registros en MockAPI\n")
    else:
        result_text.insert(tk.END, f"Error al obtener datos: {response.status_code}\n")

# Crear la ventana principal
window = tk.Tk()
window.title("Control de Carro IoT")

# Crear una etiqueta con la descripción del programa
description_label = tk.Label(window, text="Este programa permite controlar el estado de un carro IoT.\nSeleccione una acción para enviar el estado a la MockAPI.", font=("Arial", 12), pady=10)
description_label.pack()

# Crear botones para cada acción
actions = ["Adelante", "Atras", "Izquierda", "Derecha", "Alto"]
for action in actions:
    button = tk.Button(window, text=action, width=15, command=lambda a=action: send_data(a))
    button.pack(pady=5)

# Crear una caja de texto para mostrar los resultados
result_text = scrolledtext.ScrolledText(window, width=60, height=15)
result_text.pack(pady=10)

# Iniciar la ventana principal
window.mainloop()
