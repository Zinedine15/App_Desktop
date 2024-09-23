import tkinter as tk
from tkinter import ttk
import requests
import pandas as pd

# URL de la API MockAPI
API_URL = "https://66eb02f255ad32cda47b5715.mockapi.io/IoTCarStatus"

# Función para obtener y mostrar los últimos 10 registros desde MockAPI
def update_last_records():
    response = requests.get(API_URL)
    if response.status_code == 200:
        data = response.json()
        # Limitar a los últimos 10 registros
        last_records = data[-10:] if len(data) > 10 else data
        # Crear un DataFrame con los datos
        df = pd.DataFrame(last_records)
        # Limpiar el árbol de la tabla
        for row in tree.get_children():
            tree.delete(row)
        # Insertar los registros en el árbol de la tabla
        for _, record in df.iterrows():
            tree.insert("", tk.END, values=(record['id'], record['status'], record['date'], record['ipClient']))
    else:
        print(f"Error al obtener datos: {response.status_code}")

# Crear la ventana principal
window = tk.Tk()
window.title("Últimos Registros de IoT Car Status")

# Crear una etiqueta con la descripción del programa
description_label = tk.Label(window, text="Este programa muestra los últimos 10 registros del estado de un carro IoT.\nPulse 'Actualizar Registros' para obtener los datos de MockAPI.", font=("Arial", 12), pady=10)
description_label.pack()

# Crear un botón para actualizar los registros
update_button = tk.Button(window, text="Actualizar Registros", width=20, command=update_last_records)
update_button.pack(pady=10)

# Crear un árbol para mostrar los datos en forma de tabla
columns = ('ID', 'Status', 'Date', 'IP')
tree = ttk.Treeview(window, columns=columns, show='headings')
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor=tk.CENTER)
tree.pack(pady=10)

# Iniciar la ventana principal
window.mainloop()
