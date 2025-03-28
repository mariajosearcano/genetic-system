import tkinter as tk
import subprocess

def ejecutar_genetico_carro():
    subprocess.Popen(["python", "geneticoCarro.py"])

def ejecutar_genetico_imagen():
    subprocess.Popen(["python", "geneticoImagen.py"])

# Crear ventana principal
root = tk.Tk()
root.title("Menú de Sistemas Genéticos")
root.geometry("400x300")

label = tk.Label(root, text="Seleccione un sistema genético:", font=("Arial", 14))
label.pack(pady=20)

btn_carro = tk.Button(root, text="Optimización de Vehículos", command=ejecutar_genetico_carro, width=25, height=2)
btn_carro.pack(pady=10)

btn_imagen = tk.Button(root, text="Evolución de Imágenes", command=ejecutar_genetico_imagen, width=25, height=2)
btn_imagen.pack(pady=10)

# Ejecutar interfaz gráfica
root.mainloop()
