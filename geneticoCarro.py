import tkinter as tk
from tkinter import Label, Button, Canvas, PhotoImage
import random as rd
import time
import requests
from PIL import Image, ImageTk
import io

# Parámetros del problema
num_generaciones = 10
tamano_poblacion = 10
prob_mutacion = 0.3
vel_max = 30
ocup_max = 5
maletas_max = 4
masa_base = 1000
masa_ocupante = 70
masa_maleta = 15
umbral_destruccion = 5500

# URL de la imagen del auto
url_imagen = "https://images.vexels.com/media/users/3/154661/isolated/preview/7288653d1853bbc9f5e2a844ffadb763-coche-de-lujo-vista-lateral-silueta.png"

def descargar_imagen(url, tamano):
    respuesta = requests.get(url, stream=True)
    imagen = Image.open(respuesta.raw).convert("RGBA")
    imagen = imagen.resize(tamano)
    return ImageTk.PhotoImage(imagen)

class AutoGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulación de Auto")
        self.canvas = Canvas(root, width=500, height=300, bg="lightblue")
        self.canvas.pack()
        
        self.label_info = Label(root, text="Presiona 'Simular' para empezar")
        self.label_info.pack()
        
        self.btn_simular = Button(root, text="Simular", command=self.simular_generaciones)
        self.btn_simular.pack()
        
        self.auto_img = descargar_imagen(url_imagen, (70, 60))  # Descargar imagen del auto
        self.poblacion = self.crear_poblacion()
        self.generacion = 0
    
    def crear_individuo(self):
        velocidad = rd.randint(5, vel_max)
        ocupantes = rd.randint(1, ocup_max)
        maletas = rd.randint(0, maletas_max)
        return [velocidad, ocupantes, maletas]
    
    def crear_poblacion(self):
        return [self.crear_individuo() for _ in range(tamano_poblacion)]

    def calcular_fitness(self, individuo):
        velocidad, ocupantes, maletas = individuo
        masa_total = masa_base + (ocupantes * masa_ocupante) + (maletas * masa_maleta)
        fuerza = masa_total * velocidad
        return velocidad + ocupantes + maletas, fuerza
    
    def seleccionar_mejores(self):
        return sorted(self.poblacion, key=lambda ind: self.calcular_fitness(ind)[0])[:2]
    
    def cruzar(self, padres):
        padre1, padre2 = padres
        v1, o1, m1 = padre1
        v2, o2, m2 = padre2
        
        hijo1_velocidad = max(5, min(vel_max, min(v1, v2) + rd.randint(-2, 2)))
        hijo1_ocupantes = max(1, min(ocup_max, min(o1, o2) + rd.randint(-1, 1)))
        hijo1_maletas = max(0, min(maletas_max, min(m1, m2) + rd.randint(-1, 1)))

        hijo2_velocidad = max(5, min(vel_max, min(v1, v2) + rd.randint(-2, 2)))
        hijo2_ocupantes = max(1, min(ocup_max, min(o1, o2) + rd.randint(-1, 1)))
        hijo2_maletas = max(0, min(maletas_max, min(m1, m2) + rd.randint(-1, 1)))

        return [[hijo1_velocidad, hijo1_ocupantes, hijo1_maletas], [hijo2_velocidad, hijo2_ocupantes, hijo2_maletas]]
    
    def mutar(self, individuo):
        if rd.random() < prob_mutacion:
            individuo[0] = max(5, min(vel_max, individuo[0] + rd.randint(-3, 3)))
        if rd.random() < prob_mutacion:
            individuo[1] = max(1, min(ocup_max, individuo[1] + rd.randint(-1, 1)))
        if rd.random() < prob_mutacion:
            individuo[2] = max(0, min(maletas_max, individuo[2] + rd.randint(-1, 1)))
        return individuo
    
    def simular_generaciones(self):
        if self.generacion < num_generaciones:
            self.canvas.delete("all")
            print(f"\nGeneración {self.generacion}:")
            for individuo in self.poblacion:
                fitness, fuerza = self.calcular_fitness(individuo)
                print(f"  Vehículo -> Velocidad: {individuo[0]} m/s, Ocupantes: {individuo[1]}, Maletas: {individuo[2]}, Fuerza: {fuerza}")
            
            mejor_individuo = min(self.poblacion, key=lambda ind: self.calcular_fitness(ind)[0])
            self.mover_auto(mejor_individuo)
            
            padres = self.seleccionar_mejores()
            nueva_poblacion = padres.copy()
            while len(nueva_poblacion) < tamano_poblacion:
                hijos = self.cruzar(padres)
                nueva_poblacion.extend([self.mutar(hijos[0]), self.mutar(hijos[1])])
            
            self.poblacion = nueva_poblacion[:tamano_poblacion]
            self.generacion += 1
    
    def mover_auto(self, individuo):
        velocidad, ocupantes, maletas = individuo
        fitness, fuerza = self.calcular_fitness(individuo)
        resultado = f"Generación: {self.generacion}\nVel: {velocidad} m/s, Pasajeros: {ocupantes}, Maletas: {maletas}\nFuerza: {fuerza} N"
        self.label_info.config(text=resultado)
        
        auto = self.canvas.create_image(50, 225, image=self.auto_img, anchor=tk.NW)
        
        for x in range(50, 400, velocidad):
            self.canvas.move(auto, velocidad, 0)
            self.root.update()
            time.sleep(0.05)
        
        if fuerza > umbral_destruccion:
            self.canvas.create_oval(420, 230, 450, 260, fill="red")
        else:
            self.canvas.create_text(400, 150, text="¡Éxito!", font=("Arial", 16), fill="green")

if __name__ == "__main__":
    root = tk.Tk()
    app = AutoGUI(root)
    root.mainloop()
