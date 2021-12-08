import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3
from tkinter.constants import X
from rutas import *
import traceback
import sys

class Usuarios(tk.Toplevel):
    def __init__(self,master = None):
        super().__init__(master)
        # Config:
        self.title('Usuarios')
        self.geometry('435x400')
        self.resizable(width=0,height=0)
        self.iconbitmap(uptpc)
		# Menu:
        self.menubar = tk.Menu(self)
        self.menubar.add_cascade(label="Volver", command=self.volver)
        self.config(menu=self.menubar)
        
        ttk.Label(self, text='GESTIÓN DE USUARIOS',font=('Helvetica',14)).place(x='105',y='10')

        self.frame = ttk.LabelFrame(self)
        self.frame.grid(column=0,row=0,padx=5,pady=30)
        self.treeUsuarios = ttk.Treeview(self.frame,columns = ['#1','#2'], show='headings')
        self.treeUsuarios.grid(column=0,row=0, sticky='nsew')
        self.treeUsuarios.heading('#1', text = 'Id')
        self.treeUsuarios.heading('#2', text = 'Usuario')
        self.scrollbarUsuarios = ttk.Scrollbar(self.frame, orient=tk.VERTICAL, command=self.treeUsuarios.yview)
        self.treeUsuarios.configure(yscroll=self.scrollbarUsuarios.set)
        self.scrollbarUsuarios.grid(column=1,row=0, sticky='ns')

        ttk.Button(self, text='CREAR USUARIO', command='', width=65).place(x=10,y=280)
        ttk.Button(self, text='EDITAR USUARIO', command='', width=65).place(x=10,y=305)
        ttk.Button(self, text='DESHABILITAR USUARIO', command='', width=65).place(x=10,y=330)

        self.mostrarDatosUsuarios()

    def volver(self):
        self.destroy()

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

    def limpiarTablaUsuarios(self):
        self.DeleteChildren = self.treeUsuarios.get_children()
        for element in self.DeleteChildren:
            self.treeUsuarios.delete(element)
        
    def mostrarDatosUsuarios(self):
        self.limpiarTablaUsuarios()
        self.rows = self.TraerDatos("SELECT Id, Usuario FROM usuario_admin WHERE usuario_admin.Estado = 'Activo'")
        for row in self.rows:
            self.treeUsuarios.insert('',tk.END,values=row)