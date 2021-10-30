import tkinter as tk
from Carga_academica import CargaAcademica
from Gestor_bd import Gestor
from gestionar_horarios import Horarios
from unidades_curriculares import unidades_curriculares
from rutas import *

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        # Config: 
        self.title('UPTPC')
        self.geometry('800x450')
        self.resizable(width=0, height=0)
        self.imagen = tk.PhotoImage(file = fondo)
        tk.Label(self, image = self.imagen,bd=0).place(x=0, y=0)
        self.iconbitmap(uptpc)
        
        # Menu:
        self.menubar = tk.Menu(self)
        self.filemenu1 = tk.Menu(self.menubar, tearoff=0)
        self.filemenu1.add_command(label="Base de datos", command=self.gestor)
        self.filemenu1.add_command(label="Unidades curriculares", command=self.unidades_curriculares)
        self.filemenu1.add_command(label="Salir", command=self.Salir)
        self.menubar.add_cascade(label="Adminitración del Sistema", menu=self.filemenu1)
        self.filemenu2 = tk.Menu(self.menubar, tearoff=0)
        self.filemenu2.add_command(label="Manual")
        self.menubar.add_cascade(label="Ayuda", menu=self.filemenu2)
        self.config(menu=self.menubar)
        # Label:
        tk.Button(self, text="Carga Académica", width=15, height=2,command=self.cargaAcademica).place(x = 60,y = 160)
        tk.Button(self, text="Gestionar Horarios",width=15, height=2, command=self.horarios).place(x = 60,y = 220)
        
    def cargaAcademica(self):
        self.lower()
        CargaAcademica(self)

    def gestor(self):
        Gestor(self)

    def horarios(self):
        Horarios(self)

    def unidades_curriculares(self):
        unidades_curriculares(self)
                
    def Salir(self):
        self.destroy()
        