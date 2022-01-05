import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3
from rutas import *
import traceback
import sys

class BD(tk.Toplevel):
    def __init__(self,master = None):
        super().__init__(master)
        # Config:
        self.title('BD mantenimiento')
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
        self.noteCompatar = ttk.Frame(self.notebook, width=800, height=450)
        self.noteIndexar = ttk.Frame(self.notebook,width=800, height=450)
        self.noteRespaldar = ttk.Frame(self.notebook, width=800, height=450)
        self.noteRestaurar = ttk.Frame(self.notebook, width=800, height=450)
        # create frames
        self.noteCompatar.pack(fill='both', expand=True)
        self.noteIndexar.pack(fill='both', expand=True)
        self.noteRespaldar.pack(fill='both', expand=True)
        self.noteRestaurar.pack(fill='both', expand=True)
        # add frames to notebook
        self.notebook.add(self.noteCompatar, text='Compactar BD')
        self.notebook.add(self.noteIndexar, text='Indexar BD')
        self.notebook.add(self.noteRespaldar, text='Respaldar BD')
        self.notebook.add(self.noteRestaurar, text='Restaurar BD')

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