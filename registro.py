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
        self.geometry('505x330')
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
        self.noteDatos = ttk.Frame(self.notebook, width=500, height=400)
        self.noteCarga = ttk.Frame(self.notebook,width=500, height=400)
        self.noteUnidades = ttk.Frame(self.notebook, width=500, height=400)
        self.noteUsuarios = ttk.Frame(self.notebook, width=500, height=400)
        # create frames
        self.noteDatos.pack(fill='both', expand=True)
        self.noteCarga.pack(fill='both', expand=True)
        self.noteUnidades.pack(fill='both', expand=True)
        self.noteUsuarios.pack(fill='both', expand=True)
        # add frames to notebook
        self.notebook.add(self.noteDatos, text='Datos basicos')
        self.notebook.add(self.noteCarga, text='Carga académica')
        self.notebook.add(self.noteUnidades, text='Unidades curriculares')
        self.notebook.add(self.noteUsuarios, text='Usuarios')

        self.frameChoose = ttk.Frame(self.noteDatos)
        self.frameChoose.grid(row=0,column=0)
        self.Chosee = tk.StringVar()
        ttk.Radiobutton(self.frameChoose, text='Cohorte', value='Cohorte',variable=self.Chosee, command=self.mostrarCohorte).grid(row=0,column=0)
        ttk.Radiobutton(self.frameChoose, text='Lapso académico', value='Lapso académico',variable=self.Chosee, command=self.mostrarLapsoAcademico).grid(row=0,column=1)
        ttk.Radiobutton(self.frameChoose, text='Trayecto', value='Trayecto',variable=self.Chosee, command=self.mostrarTrayecto).grid(row=0,column=2)
        ttk.Radiobutton(self.frameChoose, text='Trimestre', value='Trimestre',variable=self.Chosee, command=self.mostrarTrimestre).grid(row=0,column=3)
        ttk.Radiobutton(self.frameChoose, text='Sección', value='Sección',variable=self.Chosee, command=self.mostrarSeccion).grid(row=0,column=4)
        ttk.Radiobutton(self.frameChoose, text='Laboratorio', value='Laboratorio',variable=self.Chosee, command=self.mostrarLaboratorio).grid(row=0,column=5)
        
        self.tree = ttk.Treeview(self.noteDatos,columns = ['#1','#2'], show='headings')
        self.tree.grid(column=0,row=1, sticky='nsew',padx=5,pady=5)
        self.scrollbar = ttk.Scrollbar(self.noteDatos, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=self.scrollbar.set)
        self.scrollbar.grid(column=1,row=1, sticky='ns')
        ttk.Button(self.noteDatos,text='HABILITAR',command='', width=75).grid(row=2,column=0)

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

    def mostrarCohorte(self):
        self.tree.heading('#1', text = 'Id')
        self.tree.heading('#2', text = 'Cohorte')

    def mostrarLapsoAcademico(self):
        self.tree.heading('#1', text = 'Id')
        self.tree.heading('#2', text = 'Lapso Académico')

    def mostrarTrayecto(self):
        self.tree.heading('#1', text = 'Id')
        self.tree.heading('#2', text = 'Trayecto')

    def mostrarTrimestre(self):
        self.tree.heading('#1', text = 'Id')
        self.tree.heading('#2', text = 'Triyecto')

    def mostrarSeccion(self):
        self.tree.heading('#1', text = 'Id')
        self.tree.heading('#2', text = 'Sección')

    def mostrarLaboratorio(self):
        self.tree.heading('#1', text = 'Id')
        self.tree.heading('#2', text = 'Laboratorio')