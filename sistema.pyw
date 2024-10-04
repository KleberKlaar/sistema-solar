import tkinter as tk
import math
import random

# Aumentando a largura da janela
WIDTH = 1200  # Alterado de 800 para 1200 para deixar mais largo
HEIGHT = 800
CENTER_X = WIDTH // 2
CENTER_Y = HEIGHT // 2

# Escalas simplificadas para tamanhos, distâncias e velocidades
planet_data = [
    ("Mercúrio", 3, 50, 60, 0.03, "gray"),
    ("Vênus", 6, 80, 100, 0.015, "orange"),
    ("Terra", 7, 110, 130, 0.01, "blue"),
    ("Marte", 4, 150, 180, 0.008, "red"),
    ("Júpiter", 15, 220, 260, 0.005, "brown"),
    ("Saturno", 12, 300, 350, 0.004, "yellow"),
    ("Urano", 10, 380, 430, 0.003, "light blue"),
    ("Netuno", 10, 450, 500, 0.002, "dark blue")
]

class Planet:
    def __init__(self, canvas, name, radius, semi_minor, semi_major, speed, color, label):
        self.canvas = canvas
        self.name = name
        self.radius = radius
        self.semi_minor = semi_minor
        self.semi_major = semi_major
        self.speed = speed
        self.color = color
        self.angle = 0
        self.label = label

        # Cria o planeta no canvas
        self.planet = canvas.create_oval(
            CENTER_X + self.semi_major - self.radius,
            CENTER_Y - self.radius,
            CENTER_X + self.semi_major + self.radius,
            CENTER_Y + self.radius,
            fill=self.color
        )

        # Adiciona Lua se for a Terra
        if self.name == "Terra":
            self.moon = canvas.create_oval(0, 0, 0, 0, fill="gray")
            self.moon_radius = 2
            self.moon_distance = 15
            self.moon_angle = 0

        # Adiciona anéis se for Saturno
        if self.name == "Saturno":
            self.draw_rings()

        # Bind de eventos do mouse
        self.canvas.tag_bind(self.planet, "<Enter>", self.show_name)
        self.canvas.tag_bind(self.planet, "<Leave>", self.hide_name)

    def draw_rings(self):
        # Desenhar os anéis de Saturno
        self.back_ring = self.canvas.create_oval(
            CENTER_X - (self.radius + 20), CENTER_Y - (self.radius + 8),
            CENTER_X + (self.radius + 20), CENTER_Y + (self.radius + 8),
            outline="white", width=2
        )
        self.front_ring = self.canvas.create_oval(
            CENTER_X - (self.radius + 15), CENTER_Y - (self.radius + 5),
            CENTER_X + (self.radius + 15), CENTER_Y + (self.radius + 5),
            outline="white", width=2
        )

    def move(self):
        self.angle += self.speed
        x = CENTER_X + self.semi_major * math.cos(self.angle)
        y = CENTER_Y + self.semi_minor * math.sin(self.angle)

        # Atualiza a posição do planeta
        self.canvas.coords(
            self.planet,
            x - self.radius, y - self.radius,
            x + self.radius, y + self.radius
        )

        # Atualiza a Lua (se for a Terra)
        if self.name == "Terra":
            self.moon_angle += 0.05  # Velocidade da lua
            moon_x = x + self.moon_distance * math.cos(self.moon_angle)
            moon_y = y + self.moon_distance * math.sin(self.moon_angle)
            self.canvas.coords(
                self.moon,
                moon_x - self.moon_radius, moon_y - self.moon_radius,
                moon_x + self.moon_radius, moon_y + self.moon_radius
            )

        # Atualiza os anéis (se for Saturno)
        if self.name == "Saturno":
            self.canvas.coords(
                self.back_ring,
                x - (self.radius + 20), y - (self.radius + 8),
                x + (self.radius + 20), y + (self.radius + 8)
            )
            self.canvas.coords(
                self.front_ring,
                x - (self.radius + 15), y - (self.radius + 5),
                x + (self.radius + 15), y + (self.radius + 5)
            )

    def show_name(self, event):
        # Exibe o nome do planeta
        self.label.config(text=self.name)
        self.label.place(x=event.x, y=event.y)

    def hide_name(self, event):
        # Oculta o nome do planeta
        self.label.config(text="")
        self.label.place_forget()

class SolarSystem:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="black")
        self.canvas.pack()

        # Adiciona fundo estrelado
        self.create_stars(100)  # Adiciona 100 estrelas

        # Rótulo para mostrar o nome do planeta
        self.label = tk.Label(root, bg="black", fg="white", font=("Arial", 12))
        self.label.place(x=0, y=0)

        # Rótulo de autoria
        self.author_label = tk.Label(root, text="Criado por Kleber Klaar", bg="black", fg="white", font=("Arial", 12))
        self.author_label.place(x=WIDTH - 150, y=HEIGHT - 50)  # Coloca na parte inferior direita

        # Sol no centro (amarelo brilhante e maior)
        self.sun = self.canvas.create_oval(
            CENTER_X - 30, CENTER_Y - 30,
            CENTER_X + 30, CENTER_Y + 30,
            fill="yellow"
        )

        # Cria cada planeta com base nos dados da lista planet_data
        self.planets = [
            Planet(self.canvas, name, radius, semi_minor, semi_major, speed, color, self.label)
            for name, radius, semi_minor, semi_major, speed, color in planet_data
        ]

        self.animate()

    def create_stars(self, num_stars):
        """Cria estrelas no fundo do canvas."""
        for _ in range(num_stars):
            x = random.randint(0, WIDTH)
            y = random.randint(0, HEIGHT)
            size = random.randint(1, 3)  # Tamanhos das estrelas variam de 1 a 3
            self.canvas.create_oval(
                x, y, x + size, y + size, fill="white", outline=""
            )

    def animate(self):
        for planet in self.planets:
            planet.move()
        self.root.after(20, self.animate)

# Inicializa a janela
root = tk.Tk()
root.title("Simulador de Sistema Solar Simplificado - Kleber Klaar")

# Inicia a simulação
solar_system = SolarSystem(root)

root.mainloop()
