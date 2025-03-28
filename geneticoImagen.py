import numpy as np
import matplotlib.pyplot as plt
import requests
from PIL import Image, ImageTk
import random as rd
import tkinter as tk
from tkinter import Label, Button

# Parámetros globales
tamano = 64
generaciones = 1000
url_imagen = "https://www.tallerdeescritores.com/img/contraste-opt.jpg"

# Funciones para el sistema de evolución de imágenes
def descargar_imagen(url, tamano):
    respuesta = requests.get(url, stream=True)
    imagen = Image.open(respuesta.raw).convert("RGB")
    imagen = imagen.resize((tamano, tamano))
    return np.array(imagen)

def generar_imagen_aleatoria(tamano):
    return np.random.randint(0, 256, (tamano, tamano, 3), dtype=np.uint8)

def calcular_adaptacion(individuo, modelo):
    diferencia = np.abs(individuo.astype(np.int32) - modelo.astype(np.int32))
    return -np.sum(diferencia) / (modelo.shape[0] * modelo.shape[1] * 3)

def cruce(padre1, padre2):
    mask = np.random.rand(*padre1.shape) > 0.5  # Mascara de cruce aleatoria
    hijo = np.where(mask, padre1, padre2)
    return hijo

def mutacion(individuo, prob_mutacion=0.2):
    if rd.random() < prob_mutacion:
        for _ in range(10):  # Muta 10 píxeles aleatorios
            x, y = rd.randint(0, individuo.shape[0]-1), rd.randint(0, individuo.shape[1]-1)
            individuo[x, y] = [rd.randint(0, 255) for _ in range(3)]
    return individuo

def evolucionar_poblacion(poblacion, modelo, generaciones):
    for generacion in range(generaciones):
        poblacion = sorted(poblacion, key=lambda ind: calcular_adaptacion(ind, modelo), reverse=True)
        padres = poblacion[:5]  # Selección de los mejores 5
        nueva_poblacion = [cruce(rd.choice(padres), rd.choice(padres)) for _ in range(len(poblacion))]
        nueva_poblacion = [mutacion(ind, prob_mutacion=max(0.05, 0.2 - generacion / generaciones)) for ind in nueva_poblacion]
        poblacion = nueva_poblacion
    return poblacion[0]

def iniciar_evolucion_imagen():
    modelo = descargar_imagen(url_imagen, tamano)
    poblacion = [generar_imagen_aleatoria(tamano) for _ in range(20)]
    mejor_individuo = evolucionar_poblacion(poblacion, modelo, generaciones)
    
    plt.subplot(1, 2, 1)
    plt.title("Imagen Original")
    plt.imshow(modelo)

    plt.subplot(1, 2, 2)
    plt.title("Imagen Evolucionada")
    plt.imshow(mejor_individuo)
    plt.show()

# Interfaz gráfica
root = tk.Tk()
root.title("Evolución de Imágenes")
root.geometry("400x300")

label = Label(root, text="Evolución de imagenes:")
label.pack(pady=20)

btn_imagen = Button(root, text="Iniciar evolución", command=iniciar_evolucion_imagen)
btn_imagen.pack(pady=10)

# Ejecutar interfaz gráfica
root.mainloop()
