import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3
from rutas import *
import traceback
import sys

class Usuarios(tk.Toplevel):
    def __init__(self,master = None):
        super().__init__(master)
        # Config:
        self.title('Usuarios')
        self.geometry('485x400')
        self.resizable(width=0,height=0)
        self.iconbitmap(uptpc)
		# Menu:
        self.menubar = tk.Menu(self)
        self.menubar.add_cascade(label="Volver", command=self.volver)
        self.config(menu=self.menubar)
        
        ttk.Label(self, text='GESTIÓN DE USUARIOS',font=('Helvetica',14)).place(x='125',y='10')

    def volver(self):
        self.destroy()