import tkinter as tk
from carga_academica import CargaAcademica
from gestor_bd import Gestor
from gestionar_horarios import Horarios
from unidades_curriculares import Unidades_curriculares
from reporte_carga_academica import ReporteCargaAcademica
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
        self.filemenu1.add_command(label="Carga Académica", command=self.cargaAcademica)
        self.filemenu1.add_command(label="Unidades curriculares", command=self.unidades_curriculares)
        self.menubar.add_cascade(label="Adminitración del Sistema", menu=self.filemenu1)
        self.menubar.add_cascade(label="Datos basicos", command=self.gestor)
        self.filemenu3 = tk.Menu(self.menubar, tearoff=0)
        self.filemenu3.add_command(label='Compartar BD')
        self.filemenu3.add_command(label='Indexar BD')
        self.filemenu3.add_command(label='Respaldar BD')
        self.filemenu3.add_command(label='Restaurar BD')
        self.menubar.add_cascade(label="Mantenimiento", menu=self.filemenu3)
        self.filemenu4 = tk.Menu(self.menubar, tearoff=0)
        self.filemenu4.add_command(label='Horarios de clase', command=self.horarios)
        self.filemenu4.add_command(label='Carga academica docente', command=self.reporteCargaAcademica)
        self.menubar.add_cascade(label="Reportes", menu=self.filemenu4)
        self.menubar.add_cascade(label="Salir", command=self.salir)
        self.config(menu=self.menubar)
    
    def cargaAcademica(self):
        self.lower()
        CargaAcademica(self)

    def gestor(self):
        self.lower()
        Gestor(self)

    def horarios(self):
        self.lower()
        Horarios(self)

    def unidades_curriculares(self):
        self.lower()
        Unidades_curriculares(self)

    def reporteCargaAcademica(self):
        self.lower()
        ReporteCargaAcademica(self)
                
    def salir(self):
        self.destroy()
        