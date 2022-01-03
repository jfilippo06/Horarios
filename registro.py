import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3
from rutas import *
import traceback
import sys

class Registro(tk.Toplevel):
    def __init__(self,master = None):
        super().__init__(master)
        # Config:
        self.title('Registros')
        self.geometry('800x450')
        self.resizable(width=0,height=0)
        self.iconbitmap(uptpc)
        # Menu:
        self.menubar = tk.Menu(self)
        self.menubar.add_cascade(label="Volver", command=self.volver)
        self.config(menu=self.menubar)
        # create a notebook
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(pady=0,padx=5,expand=True)
        # create frames
        self.noteCohorte = ttk.Frame(self.notebook, width=800, height=450)
        self.noteLapsoAcademico = ttk.Frame(self.notebook,width=800, height=450)
        self.noteTrayecto = ttk.Frame(self.notebook, width=800, height=450)
        self.noteTrimestre = ttk.Frame(self.notebook, width=800, height=450)
        # create frames
        self.noteCohorte.pack(fill='both', expand=True)
        self.noteLapsoAcademico.pack(fill='both', expand=True)
        self.noteTrayecto.pack(fill='both', expand=True)
        self.noteTrimestre.pack(fill='both', expand=True)
        # add frames to notebook
        self.notebook.add(self.noteCohorte, text='Datos basicos')
        self.notebook.add(self.noteLapsoAcademico, text='Carga académica')
        self.notebook.add(self.noteTrayecto, text='Unidades curriculares')
        self.notebook.add(self.noteTrimestre, text='Usuarios')


    def conexion(self,query,parametros = ()):
        try:
            self.con = sqlite3.connect(baseDeDatos)
            self.cursor = self.con.cursor()
            self.cursor.execute(query,parametros)
            self.con.commit()
            return self.cursor
        except sqlite3.IntegrityError:
            pass
        except sqlite3.Error as er:
            print('SQLite error: %s' % (' '.join(er.args)))
            print("Exception class is: ", er.__class__)
            print('SQLite traceback: ')
            exc_type, exc_value, exc_tb = sys.exc_info()
            print(traceback.format_exception(exc_type, exc_value, exc_tb))

    def volver(self):
        self.destroy()