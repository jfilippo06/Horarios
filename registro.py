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
        self.noteDatos = ttk.Frame(self.notebook, width=800, height=450)
        self.noteCarga = ttk.Frame(self.notebook,width=800, height=450)
        self.noteUnidades = ttk.Frame(self.notebook, width=800, height=450)
        self.noteUsuarios = ttk.Frame(self.notebook, width=800, height=450)
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

        # Notebook datos basicos -----------------------------------------
        self.datos = ttk.Notebook(self.noteDatos)
        self.datos.pack(pady=0,padx=5,expand=True)
        # create frames
        self.noteCohorte = ttk.Frame(self.datos, width=800, height=450)
        self.noteLapsoAcademico = ttk.Frame(self.notebook,width=800, height=450)
        self.noteTrayecto = ttk.Frame(self.notebook, width=800, height=450)
        self.noteTrimestre = ttk.Frame(self.notebook, width=800, height=450)
        self.noteSeccion = ttk.Frame(self.notebook, width=800, height=450)
        self.noteLaboratorio = ttk.Frame(self.notebook, width=800, height=450)
        # create frames
        self.noteCohorte.pack(fill='both', expand=True)
        self.noteLapsoAcademico.pack(fill='both', expand=True)
        self.noteTrayecto.pack(fill='both', expand=True)
        self.noteTrimestre.pack(fill='both', expand=True)
        self.noteSeccion.pack(fill='both', expand=True)
        self.noteLaboratorio.pack(fill='both', expand=True)
        # add frames to notebook
        self.datos.add(self.noteCohorte, text='Cohorte')
        self.datos.add(self.noteLapsoAcademico, text='Lapso Académico')
        self.datos.add(self.noteTrayecto, text='Trayecto')
        self.datos.add(self.noteTrimestre, text='Trimestre')
        self.datos.add(self.noteSeccion, text='sección')
        self.datos.add(self.noteLaboratorio, text='Laboratorio')

        # Pantalla Cohorte 0/1
        self.frameCohorte = ttk.LabelFrame(self.noteCohorte)
        self.frameCohorte.grid(column=0,row=0,pady=5, padx=5)
        # Cohorte Tabla 1/1
        self.treeCohorte = ttk.Treeview(self.frameCohorte,columns = ['#1','#2'], show='headings')
        self.treeCohorte.grid(column=0,row=0, sticky='nsew')
        self.treeCohorte.heading('#1', text = 'Id')
        self.treeCohorte.heading('#2', text = 'Cohorte')
        self.scrollbarCohorte = ttk.Scrollbar(self.frameCohorte, orient=tk.VERTICAL, command=self.treeCohorte.yview)
        self.treeCohorte.configure(yscroll=self.scrollbarCohorte.set)
        self.scrollbarCohorte.grid(column=1,row=0, sticky='ns')
        ttk.Button(self.noteCohorte,text='HABILITAR COHORTE',command='', width=68).grid(row=1,column=0)

        # Pantalla LapsoAcademico 0/1
        self.frameLapsoAcademico = ttk.LabelFrame(self.noteLapsoAcademico)
        self.frameLapsoAcademico.grid(column=0,row=0,pady=5, padx=5)
        # Cohorte Tabla 1/1
        self.treeLapsoAcademico = ttk.Treeview(self.frameLapsoAcademico,columns = ['#1','#2'], show='headings')
        self.treeLapsoAcademico.grid(column=0,row=0, sticky='nsew')
        self.treeLapsoAcademico.heading('#1', text = 'Id')
        self.treeLapsoAcademico.heading('#2', text = 'Lapso Académico')
        self.scrollbarLapsoAcademico = ttk.Scrollbar(self.frameLapsoAcademico, orient=tk.VERTICAL, command=self.treeCohorte.yview)
        self.treeLapsoAcademico.configure(yscroll=self.scrollbarLapsoAcademico.set)
        self.scrollbarLapsoAcademico.grid(column=1,row=0, sticky='ns')
        ttk.Button(self.noteLapsoAcademico,text='HABILITAR LAPSO ACADÉMICO',command='', width=68).grid(row=1,column=0)

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