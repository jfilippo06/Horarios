import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from carga_academica import CargaAcademica
from gestor_bd import Gestor
from gestionar_horarios import Horarios
from unidades_curriculares import Unidades_curriculares
from reporte_carga_academica import ReporteCargaAcademica
from rutas import *
import sqlite3
import traceback
import sys

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        # Config: 
        self.title('Login')
        self.geometry('300x270')
        self.resizable(width=0, height=0)
        self.iconbitmap(uptpc)

        self.tittleUser = ttk.Label(text='Usuario')
        self.tittleUser.place(x=130,y=110)
        self.userName = ttk.Entry(self,width=40)
        self.userName.place(x=25,y=130)
        self.userName.focus()
        self.tittlePassword = ttk.Label(text='Contraseña')
        self.tittlePassword.place(x=120,y=160)
        self.userPassword = ttk.Entry(self,width=40)
        self.userPassword.config(show='*')
        self.userPassword.place(x=25,y=180)
        self.button = ttk.Button(self, text='Iniciar Sesión', command=self.change)
        self.button.place(x=110,y=210)

    def validarCeldas(self):
        return len(self.userName.get()) != 0 and len(self.userPassword.get()) != 0
   
    def change(self):
        if self.validarCeldas():
            validar = self.conexion('SELECT * FROM usuario_admin WHERE Usuario = ? and Contraseña = ? and Estado = "Activo"', (self.userName.get(),self.userPassword.get())).fetchall()
            if validar:
                self.tittleUser.place_forget()
                self.userName.place_forget()
                self.userPassword.place_forget()
                self.tittlePassword.place_forget()
                self.button.place_forget()
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

    def pantallaPrincipal(self):
        self.title('UPTPC')
        self.geometry('800x450')
        self.resizable(width=0, height=0)
        self.imagen = tk.PhotoImage(file = fondo)
        tk.Label(self, image = self.imagen,bd=0).place(x=0, y=0)
        self.iconbitmap(uptpc)
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
        