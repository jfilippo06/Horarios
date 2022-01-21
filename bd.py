import re
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import sqlite3
from rutas import *
import traceback
import sys
import shutil

class BD(tk.Toplevel):
    def __init__(self,master = None):
        super().__init__(master)
        # Config:
        self.title('BD mantenimiento')
        self.geometry('380x160')
        self.resizable(width=0,height=0)
        self.iconbitmap(uptpc)
        # Menu:
        self.menubar = tk.Menu(self)
        self.menubar.add_cascade(label="Volver", command=self.volver)
        self.config(menu=self.menubar)

        ttk.Button(self, text='Compactar Base de datos', command=self.compactar, width=60).grid(row=0,column=0,padx=5,pady=5)
        ttk.Button(self, text= 'Indexar Base de datos', command=self.indexar, width=60).grid(row=1,column=0,padx=5,pady=5)
        ttk.Button(self, text='Respaldar Base de datos', command=self.respaldar, width=60).grid(row=2,column=0,padx=5,pady=5)
        ttk.Button(self, text='Restaurar Base de datos', command=self.restaurar, width=60).grid(row=3,column=0,padx=5,pady=5)

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

    def compactar(self):
        if messagebox.askyesno('Compactar','¿Desea compactar la base de datos?'):    
            self.conexion('VACUUM')
            messagebox.showinfo(title='Info', message='Base de datos compactada')

    def indexar(self):
        pass

    def respaldar(self):
        if messagebox.askyesno('Respaldar','¿Desea respaldar la base de datos?'):    
            guardar = filedialog.asksaveasfilename(initialdir= "/", title="Select file", defaultextension=".*",filetypes=(("DB files","*.db"),("all files","*.*")))
            shutil.copyfile(baseDeDatos, guardar)
            messagebox.showinfo(title='Info', message='Base de datos respaldada')

    def restaurar(self):
        if messagebox.askyesno('Restaurar','¿Desea restaurar la base de datos?'):    
            guardar = filedialog.asksaveasfilename(initialdir= "/", title="Select file", defaultextension=".*",filetypes=(("DB files","*.db"),("all files","*.*")))
            shutil.copyfile(guardar, baseDeDatos)
            messagebox.showinfo(title='Info', message='Base de datos restaurada')
        