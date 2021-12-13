import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3
from rutas import *
import traceback
import sys
import hashlib

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

        ttk.Button(self, text='CREAR USUARIO', command=self.crear, width=65).place(x=10,y=280)
        ttk.Button(self, text='EDITAR USUARIO', command=self.editar, width=65).place(x=10,y=305)
        ttk.Button(self, text='DESHABILITAR USUARIO', command=self.deshabilitar, width=65).place(x=10,y=330)

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

    def selecionarFila(self):
        self.item = self.treeUsuarios.focus()
        self.data = self.treeUsuarios.item(self.item)
        self.id = self.data['values'][0]
        return self.id

    def crear(self):
        new = tk.Toplevel()
        new.title('Crear usuarios')
        new.geometry('360x100')
        new.resizable(width=0,height=0)
        new.iconbitmap(uptpc)
        ttk.Label(new, text='Usuario:').grid(row=0,column=0,padx=5,pady=5)
        self.newUser = ttk.Entry(new,width=40)
        self.newUser.grid(row=0,column=1,padx=5,pady=5)
        self.newUser.focus()
        ttk.Label(new, text='Contraseña:').grid(row=1,column=0,padx=5,pady=5)
        self.newPassword = ttk.Entry(new,width=40)
        self.newPassword.grid(row=1,column=1,padx=5,pady=5)
        self.newPassword.config(show='*')
        ttk.Button(new,text='CREAR USUARIO', command=self.encriptar,width=40).place(x=80, y=60)
        new.mainloop()

    def editar(self):
        if self.treeUsuarios.selection():
            self.id = self.selecionarFila()
            new = tk.Toplevel()
            new.title('Editar usuario')
            new.geometry('480x80')
            new.resizable(width=0,height=0)
            new.iconbitmap(uptpc)
            ttk.Label(new, text='Usuario:').grid(row=0,column=0,padx=5,pady=5)
            self.newUserEditar = ttk.Entry(new,width=40)
            self.newUserEditar.grid(row=0,column=1,padx=5,pady=5)
            ttk.Button(new,text='EDITAR USUARIO', command=self.editarUsuario,width=20).grid(row=0,column=2,padx=5,pady=5)
            ttk.Label(new, text='Contraseña:').grid(row=1,column=0,padx=5,pady=5)
            self.newPasswordEditar = ttk.Entry(new,width=40)
            self.newPasswordEditar.grid(row=1,column=1,padx=5,pady=5)
            self.newPasswordEditar.config(show='*')
            ttk.Button(new,text='EDITAR CONTRASEÑA', command=self.editarPass,width=20).grid(row=1,column=2,padx=5,pady=5)
            new.mainloop()

        else:
            messagebox.showwarning(title='Warning', message='Seleccione un usuario')

    def deshabilitar(self):
        if self.treeUsuarios.selection():
            if messagebox.askyesno('Deshabilitar','¿Desea deshabilitar el usuario seleccionado?'):
                self.id = self.selecionarFila()
                self.conexion('UPDATE usuario_admin SET Estado = "Inactivo" WHERE usuario_admin.Id = ? and usuario_admin.Estado = "Activo"', (self.id,))
                self.mostrarDatosUsuarios()
                messagebox.showinfo(title='Info', message='Usuario deshabilitado')
            else:
                self.mostrarDatosUsuarios()
        else:
            messagebox.showwarning(title='Warning', message='Seleccione un usuario')

    def encriptar(self):
        if len(self.newUser.get()) != 0 and len(self.newPassword.get()):
            blake2b = hashlib.blake2b(self.newPassword.get().encode()).hexdigest()
            self.conexion('INSERT INTO usuario_admin VALUES (NULL,?,?,"Activo")', (self.newUser.get(),blake2b))
            self.mostrarDatosUsuarios()
            messagebox.showinfo(title='Info', message='Usuario creado')
        else:
            messagebox.showwarning(title='Warning', message='Introduzca un valor')

    def editarUsuario(self):
        if len(self.newUserEditar.get()):
            self.conexion('UPDATE usuario_admin SET Usuario = ? WHERE usuario_admin.Id = ? and usuario_admin.Estado = "Activo"', (self.newUserEditar.get(), self.id))
            self.mostrarDatosUsuarios()
            messagebox.showinfo(title='Info', message='Usuario Editado')
        else:
            messagebox.showwarning(title='Warning', message='Introduzca un valor')

    def editarPass(self):
        if len(self.newPasswordEditar.get()):
            blake2b = hashlib.blake2b(self.newPasswordEditar.get().encode()).hexdigest()
            self.conexion('UPDATE usuario_admin SET Contraseña = ? WHERE usuario_admin.Id = ? and usuario_admin.Estado = "Activo"', (blake2b, self.id))
            self.mostrarDatosUsuarios()
            messagebox.showinfo(title='Info', message='Contraseña Editada')
        else:
            messagebox.showwarning(title='Warning', message='Introduzca un valor')