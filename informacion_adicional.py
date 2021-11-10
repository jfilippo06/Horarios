import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3
from rutas import *
import traceback
import sys

class informacion_Adicional(tk.Toplevel):
    def __init__(self,master):
        super().__init__(master)
        # Config:
        self.title('Informacion Adicional Docente')
        self.geometry('1050x470')
        self.resizable(width=0, height=0)
        self.iconbitmap(uptpc)

        self.container = ttk.Labelframe(self)
        self.container.grid(column=0,row=0)

        self.frameDocente = ttk.Labelframe(self.container)
        self.frameDocente.grid(column=0,row=0,padx=5,pady=5)
        self.treeDocente = ttk.Treeview(self.frameDocente, columns=['#1',"#2"],show='headings',height=5)
        self.treeDocente.grid(row=0,column=0)
        self.treeDocente.heading('#1', text = 'Id',)
        self.treeDocente.heading('#2', text = 'Hora')
        self.treeDocente.column('#1', width=50)
        self.treeDocente.column('#2', width=110)
        self.scrollbarDocente = ttk.Scrollbar(self.frameDocente, orient=tk.VERTICAL, command=self.treeDocente.yview)
        self.treeDocente.configure(yscroll=self.scrollbarDocente.set)
        self.scrollbarDocente.grid(column=1,row=0, sticky='ns')

        self.frameEjecutar = ttk.Labelframe(self.container)
        self.frameEjecutar.grid(column=1,row=0)
        ttk.Button(self.frameEjecutar, text='AÑADIR DOCENTE', command='',width=26).grid(row=1,column=0)
        ttk.Button(self.frameEjecutar, text='ELIMINAR DEPARTAMENTO', command='',width=26).grid(row=3,column=0)

        # self.framePEntry = ttk.Labelframe(self.container)
        # self.framePEntry.grid(column=4,row=0)
        # ttk.Label(self.framePEntry,text='Pt').grid(column=0,row=0)
        # self.entryPEntry = ttk.Entry(self.framePEntry,width=15)
        # self.entryPEntry.grid(column=1,row=0)
        # ttk.Button(self.framePEntry, text='REGISTRAR PT', command=self.RegistrarPt,width=15).grid(row=1,column=0)
        # ttk.Button(self.framePEntry, text='EDITAR PT', command=self.editarPt,width=15).grid(row=2,column=0)
        # ttk.Button(self.framePEntry, text='ELIMINAR PT', command=self.eliminarPt,width=15).grid(row=3,column=0)

        self.frameUnidadesCurriculares = ttk.Labelframe(self)
        self.frameUnidadesCurriculares.grid(column=0,row=1,padx=5)
        self.treeUnidadesCurriculares = ttk.Treeview(self.frameUnidadesCurriculares, columns=['#1',"#2",'#3','#4'],show='headings',height=10)
        self.treeUnidadesCurriculares.grid(row=0,column=0)
        self.treeUnidadesCurriculares.heading('#1', text = 'Id',)
        self.treeUnidadesCurriculares.heading('#2', text = 'Docente')
        self.treeUnidadesCurriculares.heading('#3', text = 'Labora en otra enpresa')
        self.treeUnidadesCurriculares.heading('#4', text = 'Especifique')
        self.treeUnidadesCurriculares.column('#1', width=50)
        self.treeUnidadesCurriculares.column('#2', width=240)
        self.treeUnidadesCurriculares.column('#3', width=240)
        self.treeUnidadesCurriculares.column('#4', width=240)
        self.scrollbarUnidadesCurriculares = ttk.Scrollbar(self.frameUnidadesCurriculares, orient=tk.VERTICAL, command=self.treeUnidadesCurriculares.yview)
        self.treeUnidadesCurriculares.configure(yscroll=self.scrollbarUnidadesCurriculares.set)
        self.scrollbarUnidadesCurriculares.grid(column=1,row=0, sticky='ns')

        # self.frameButton = ttk.Labelframe(self)
        # self.frameButton.grid(column=0,row=2,padx=5)
        # ttk.Button(self.frameButton, text='AGREGAR/MODIFICAR - HORA',width=55, command=self.modificarHora).grid(row=0,column=0)
        # ttk.Button(self.frameButton, text='AGREGAR/MODIFICAR - DEPARTAMENTO',width=55, command=self.modificarDepartamento).grid(row=0,column=1)
        # ttk.Button(self.frameButton, text='AGREGAR/MODIFICAR - PT',width=55, command=self.modificarPt).grid(row=0,column=2)

    def conexion(self,query,parametros = ()):
        try:
            self.con = sqlite3.connect(baseDeDatos)
            self.cursor = self.con.cursor()
            self.cursor.execute(query,parametros)
            self.con.commit()
            return self.cursor
        except sqlite3.IntegrityError:
            pass
        except IndexError:
            pass
        except sqlite3.Error as er:
            print('SQLite error: %s' % (' '.join(er.args)))
            print("Exception class is: ", er.__class__)
            print('SQLite traceback: ')
            exc_type, exc_value, exc_tb = sys.exc_info()
            print(traceback.format_exception(exc_type, exc_value, exc_tb))

    def TraerDatos(self,query):
        self.mostrar = self.conexion(query)
        self.rows = self.mostrar.fetchall()
        return self.rows
