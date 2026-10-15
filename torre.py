import tkinter as tk
from tkinter import messagebox, ttk

class JuegoHanoiGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Torre de Hanói (3 a 64 discos)")
        self.root.geometry("900x650")
        self.root.configure(bg="#f0f0f0")

        self.num_discos = 3
        self.torres = {'A': [], 'B': [], 'C': []}
        self.movimientos = 0
        self.disco_seleccionado = None
        self.torre_origen = None

        self._crear_interfaz()
        self.reiniciar_juego()

    def _crear_interfaz(self):
        frame_controles = tk.Frame(self.root, bg="#ffffff", pady=10)
        frame_controles.pack(fill=tk.X, side=tk.TOP)

        label_num = tk.Label(frame_controles, text="Número de discos:", bg="#ffffff", font=("Arial", 12))
        label_num.pack(side=tk.LEFT, padx=10)

        # Opciones desde 3 hasta 64 discos
        self.combo_discos = ttk.Combobox(frame_controles, values=list(range(3, 65)), state="readonly", width=5)
        self.combo_discos.set(3)
        self.combo_discos.pack(side=tk.LEFT, padx=5)
        self.combo_discos.bind("<<ComboboxSelected>>", lambda e: self.reiniciar_juego())

        btn_reiniciar = tk.Button(frame_controles, text="Reiniciar", command=self.reiniciar_juego, bg="#4CAF50", fg="white", font=("Arial", 10, "bold"))
        btn_reiniciar.pack(side=tk.LEFT, padx=10)

        btn_resolver = tk.Button(frame_controles, text="Resolver Automático", command=self.resolver_automatico, bg="#2196F3", fg="white", font=("Arial", 10, "bold"))
        btn_resolver.pack(side=tk.LEFT, padx=10)

        self.label_movs = tk.Label(frame_controles, text="Movimientos: 0", bg="#ffffff", font=("Arial", 12, "bold"))
        self.label_movs.pack(side=tk.RIGHT, padx=20)

        self.canvas = tk.Canvas(self.root, bg="#ffffff", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        self.canvas.bind("<Button-1>", self.al_hacer_clic)

    def reiniciar_juego(self):
        self.num_discos = int(self.combo_discos.get())
        self.torres = {
            'A': list(range(self.num_discos, 0, -1)),
            'B': [],
            'C': []
        }
        self.movimientos = 0
        self.disco_seleccionado = None
        self.torre_origen = None
        self.label_movs.config(text="Movimientos: 0")
        self.dibujar_escenario()

    def dibujar_escenario(self):
        self.canvas.delete("all")
        ancho = self.canvas.winfo_width()
        alto = self.canvas.winfo_height()

        if ancho <= 1 or alto <= 1:
            ancho, alto = 860, 550

        pos_x = {'A': ancho / 4, 'B': ancho / 2, 'C': 3 * ancho / 4}
        base_y = alto - 50
        altura_estaca = 300

        # Dibujar base general
        self.canvas.create_rectangle(50, base_y, ancho - 50, base_y + 20, fill="#8B4513", outline="#5c2d0c")

        # Dibujar las 3 estacas y sus etiquetas
        for clave, x in pos_x.items():
            self.canvas.create_rectangle(x - 8, base_y - altura_estaca, x + 8, base_y, fill="#CD853F", outline="#8B4513")
            self.canvas.create_text(x, base_y + 35, text=f"Torre {clave}", font=("Arial", 14, "bold"), fill="#333333")

        # Ajuste dinámico de la altura de los discos según la cantidad elegida
        ancho_max_disco = (ancho / 4) - 20
        alto_disco = max(2, (altura_estaca - 10) / self.num_discos)

        colores = ["#FF5722", "#E91E63", "#9C27B0", "#673AB7", "#3F51B5", "#2196F3", "#00BCD4", "#009688"]

        for clave, x in pos_x.items():
            for i, disco in enumerate(self.torres[clave]):
                ancho_disco = 20 + (disco / self.num_discos) * (ancho_max_disco - 20)
                y_centrado = base_y - (i * alto_disco) - (alto_disco / 2)

                x1 = x - (ancho_disco / 2)
                y1 = y_centrado - (alto_disco / 2)
                x2 = x + (ancho_disco / 2)
                y2 = y_centrado + (alto_disco / 2)

                color = colores[(disco - 1) % len(colores)]

                borde = 2 if (clave == self.torre_origen and i == len(self.torres[clave]) - 1 and self.disco_seleccionado) else 0
                color_borde = "yellow" if borde == 2 else ""

                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline=color_borde, width=borde)

    def al_hacer_clic(self, event):
        ancho = self.canvas.winfo_width()
        x_clic = event.x

        if x_clic < ancho / 3:
            torre_clic = 'A'
        elif x_clic < 2 * ancho / 3:
            torre_clic = 'B'
        else:
            torre_clic = 'C'

        if self.disco_seleccionado is None:
            if self.torres[torre_clic]:
                self.torre_origen = torre_clic
                self.disco_seleccionado = self.torres[torre_clic][-1]
        else:
            if self.torre_origen == torre_clic:
                self.disco_seleccionado = None
                self.torre_origen = None
            else:
                if not self.torres[torre_clic] or self.torres[torre_clic][-1] > self.disco_seleccionado:
                    disco = self.torres[self.torre_origen].pop()
                    self.torres[torre_clic].append(disco)
                    self.movimientos += 1
                    self.label_movs.config(text=f"Movimientos: {self.movimientos}")

                    if len(self.torres['C']) == self.num_discos or len(self.torres['B']) == self.num_discos:
                        self.dibujar_escenario()
                        min_movs = (2 ** self.num_discos) - 1
                        messagebox.showinfo("¡Felicidades!", f"¡Has completado la Torre de Hanói!\nMovimientos: {self.movimientos}\n(Mínimo teórico: {min_movs:,})")
                else:
                    messagebox.showwarning("Movimiento inválido", "No puedes colocar un disco más grande sobre uno más pequeño.")

                self.disco_seleccionado = None
                self.torre_origen = None

        self.dibujar_escenario()

    def resolver_automatico(self):
        if self.num_discos > 15:
            if not messagebox.askyesno("Advertencia", f"Resolver automáticamente {self.num_discos} discos tomaría miles o millones de pasos. ¿Seguro que deseas iniciar la animación?"):
                return

        self.reiniciar_juego()
        pasos = []

        def hanoi_rec(n, origen, destino, auxiliar):
            if n == 1:
                pasos.append((origen, destino))
                return
            hanoi_rec(n - 1, origen, auxiliar, destino)
            pasos.append((origen, destino))
            hanoi_rec(n - 1, auxiliar, destino, origen)

        hanoi_rec(self.num_discos, 'A', 'C', 'B')

        def animar_paso(i=0):
            if i < len(pasos):
                origen, destino = pasos[i]
                disco = self.torres[origen].pop()
                self.torres[destino].append(disco)
                self.movimientos += 1
                self.label_movs.config(text=f"Movimientos: {self.movimientos}")
                self.dibujar_escenario()
                self.root.after(100, lambda: animar_paso(i + 1))

        animar_paso()

if __name__ == "__main__":
    root = tk.Tk()
    app = JuegoHanoiGUI(root)
    root.mainloop()