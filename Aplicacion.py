import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from carga_academica import CargaAcademica
from gestor_bd import Gestor
from gestionar_horarios import Horarios
from unidades_curriculares import Unidades_curriculares
from reporte_carga_academica import ReporteCargaAcademica
from usuarios import Usuarios
from registro import Registro
from materias_asignadas import Materias_asignadas
from bd import BD
from rutas import *
import sqlite3
import traceback
import sys
import hashlib

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        # Config: 
        self.title('LOGIN')
        self.geometry('600x450')
        self.resizable(width=0, height=0)
        self.iconbitmap(uptpc)

        self.imagen = tk.PhotoImage(file = login_fondo)
        self.fondo = tk.Label(self, image = self.imagen,bd=0)
        self.fondo.place(x=0, y=0)

        self.imagenPrincipal = tk.PhotoImage(file = fondo)
        self.fondoPrincipal = tk.Label(self, image = self.imagenPrincipal,bd=0)
    
        self.userName = ttk.Entry(self,width=40)
        self.userName.place(x=165,y=200)
        self.userName.focus()
        self.userPassword = ttk.Entry(self,width=40)
        self.userPassword.config(show='*')
        self.userPassword.place(x=165,y=250)
        self.button = ttk.Button(self, text='Iniciar Sesión', command=self.change)
        self.button.place(x=250,y=285)
        
        self.menubar = tk.Menu(self)
        self.filemenu1 = tk.Menu(self.menubar, tearoff=0)
        self.filemenu1.add_command(label="Carga académica", command=self.cargaAcademica)
        self.filemenu1.add_command(label="Datos basicos", command=self.gestor)
        self.filemenu1.add_command(label="Unidades curriculares", command=self.unidades_curriculares)
        self.menubar.add_cascade(label="Administración del sistema", menu=self.filemenu1)
        self.filemenu2 = tk.Menu(self.menubar, tearoff=0)
        self.filemenu2.add_command(label="Usuarios", command=self.usuarios)
        self.menubar.add_cascade(label="Configuración", menu=self.filemenu2)
        self.filemenu3 = tk.Menu(self.menubar, tearoff=0)
        self.filemenu3.add_command(label='Base de datos', command= self.bd)
        self.filemenuRegistro = tk.Menu(self.filemenu3, tearoff=0)
        self.filemenuRegistro.add_command(label='Registros basicos', command=self.registro)
        self.filemenuRegistro.add_command(label='Materias asignadas', command=self.materias)
        self.filemenu3.add_cascade(label="Registros", menu=self.filemenuRegistro)
        self.menubar.add_cascade(label="Mantenimiento", menu=self.filemenu3)
        self.filemenu4 = tk.Menu(self.menubar, tearoff=0)
        self.filemenu4.add_command(label='Horarios de clase', command=self.horarios)
        self.filemenu4.add_command(label='Carga academica docente', command=self.reporteCargaAcademica)
        self.menubar.add_cascade(label="Reportes", menu=self.filemenu4)
        self.menubar.add_cascade(label="Salir", command=self.salir)
        self.config(menu='')

    def conexion(self,query,parametros = ()):
            try:
                self.con = sqlite3.connect(baseDeDatos)
                self.cursor = self.con.cursor()
                self.cursor.execute(query,parametros)
                self.con.commit()
                return self.cursor
            except sqlite3.Error as er:
                print('SQLite error: %s' % (' '.join(er.args)))
                print("Exception class is: ", er.__class__)
                print('SQLite traceback: ')
                exc_type, exc_value, exc_tb = sys.exc_info()
                print(traceback.format_exception(exc_type, exc_value, exc_tb))

    def validarCeldas(self):
        return len(self.userName.get()) != 0 and len(self.userPassword.get()) != 0
   
    def change(self):
        if self.validarCeldas():
            blake2b = hashlib.blake2b(self.userPassword.get().encode()).hexdigest()
            validar = self.conexion('SELECT * FROM usuario_admin WHERE Usuario = ? and Contraseña = ? and Estado = "Activo"', (self.userName.get(),blake2b)).fetchall()
            if validar:
                self.userName.delete(0, tk.END)
                self.userPassword.delete(0, tk.END)
                self.pantallaPrincipal()
            else:
                messagebox.showwarning(title='Warnig', message='Usuario no existe')
                self.userName.delete(0, tk.END)
                self.userPassword.delete(0, tk.END)
                self.userName.focus()
        else:
            messagebox.showwarning(title='Warnig', message='Introdusca un valor en las casillas')
            self.userName.delete(0, tk.END)
            self.userPassword.delete(0, tk.END)
            self.userName.focus()

    def pantallaPrincipal(self):
        self.title('UPTPC')
        self.geometry('800x450') 

        self.userName.place_forget()
        self.userPassword.place_forget()
        self.button.place_forget()
        self.fondo.place_forget()

        self.config(menu=self.menubar)
        self.fondoPrincipal.place(x=0, y=0)

    def salir(self):
        if messagebox.askyesno('Salir','¿Desea salir de la sesión?'):
            self.title('LOGIN')
            self.geometry('600x450')

            self.config(menu='')
            self.fondoPrincipal.place_forget()

            self.fondo.place(x=0, y=0)
            self.userName.place(x=165,y=200)
            self.userName.focus()
            self.userPassword.config(show='*')
            self.userPassword.place(x=165,y=250)
            self.button.place(x=250,y=285)

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

    def usuarios(self):
        self.lower()
        Usuarios(self)

    def registro(self):
        self.lower()
        Registro(self)

    def bd(self):
        self.lower()
        BD(self)

    def materias(self):
        self.lower()
        Materias_asignadas(self)