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
        self.newCrear = tk.Toplevel()
        self.newCrear.title('Crear usuarios')
        self.newCrear.geometry('390x145')
        self.newCrear.resizable(width=0,height=0)
        self.newCrear.iconbitmap(uptpc)
        ttk.Label(self.newCrear, text='Usuario:').grid(row=0,column=0,padx=5,pady=5)
        self.newUser = ttk.Entry(self.newCrear,width=40)
        self.newUser.grid(row=0,column=1,padx=5,pady=5)
        self.newUser.focus()
        ttk.Label(self.newCrear, text='Contraseña:').grid(row=1,column=0,padx=5,pady=5)
        self.newPassword = ttk.Entry(self.newCrear,width=40)
        self.newPassword.grid(row=1,column=1,padx=5,pady=5)
        self.newPassword.config(show='*')
        ttk.Label(self.newCrear, text='Repetir contraseña:').grid(row=2,column=0,padx=5,pady=5)
        self.newPassword2 = ttk.Entry(self.newCrear,width=40)
        self.newPassword2.grid(row=2,column=1,padx=5,pady=5)
        self.newPassword2.config(show='*')
        ttk.Button(self.newCrear,text='CREAR USUARIO', command=self.encriptar,width=40).grid(row=3,column=1)
        ttk.Button(self.newCrear,text='CANCELAR', command=self.cancelarUser,width=40).grid(row=4,column=1)
        self.newCrear.mainloop()

    def cancelarUser(self):
        self.newCrear.destroy()

    def editar(self):
        if self.treeUsuarios.selection():
            self.id = self.selecionarFila()
            self.newEditar = tk.Toplevel()
            self.newEditar.title('Editar usuario')
            self.newEditar.geometry('390x145')
            self.newEditar.resizable(width=0,height=0)
            self.newEditar.iconbitmap(uptpc)
            ttk.Label(self.newEditar, text='Usuario:').grid(row=0,column=0,padx=5,pady=5)
            self.newUserEditar = ttk.Entry(self.newEditar,width=40)
            self.newUserEditar.grid(row=0,column=1,padx=5,pady=5)
            ttk.Label(self.newEditar, text='Contraseña:').grid(row=1,column=0,padx=5,pady=5)
            self.newPasswordEditar = ttk.Entry(self.newEditar,width=40)
            self.newPasswordEditar.grid(row=1,column=1,padx=5,pady=5)
            self.newPasswordEditar.config(show='*')
            ttk.Label(self.newEditar, text='Repiter contraseña:').grid(row=2,column=0,padx=5,pady=5)
            self.newPasswordEditar2 = ttk.Entry(self.newEditar,width=40)
            self.newPasswordEditar2.grid(row=2,column=1,padx=5,pady=5)
            self.newPasswordEditar2.config(show='*')
            ttk.Button(self.newEditar,text='EDITAR USUARIO', command=self.editarUsuario,width=40).grid(row=3,column=1)
            ttk.Button(self.newEditar,text='CANCELAR', command=self.cancelarEdit,width=40).grid(row=4,column=1)
            self.newEditar.mainloop()
        else:
            messagebox.showwarning(title='Warning', message='Seleccione un usuario')

    def cancelarEdit(self):
        self.newEditar.destroy()

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
        if len(self.newUser.get()) != 0 and len(self.newPassword.get()) != 0 and len(self.newPassword2.get()) != 0:
            if self.newPassword.get() == self.newPassword2.get():   
                blake2b = hashlib.blake2b(self.newPassword.get().encode()).hexdigest()
                self.conexion('INSERT INTO usuario_admin VALUES (NULL,?,?,"Activo")', (self.newUser.get(),blake2b))
                self.mostrarDatosUsuarios()
                self.newCrear.destroy()
                messagebox.showinfo(title='Info', message='Usuario creado')
            else:
                messagebox.showwarning(title='Warning', message='Contraseña no coinciden')
                self.newPassword.delete(0,tk.END)
                self.newPassword2.delete(0,tk.END)
        else:
            messagebox.showwarning(title='Warning', message='Introduzca un valor')

    def editarUsuario(self):
        if len(self.newUserEditar.get()) != 0 and len(self.newPasswordEditar.get()) != 0 and len(self.newPasswordEditar2.get()) != 0:
            if self.newPasswordEditar.get() == self.newPasswordEditar2.get(): 
                blake2b = hashlib.blake2b(self.newPasswordEditar.get().encode()).hexdigest()
                self.conexion('UPDATE usuario_admin SET Usuario = ?, Contraseña = ? WHERE usuario_admin.Id = ? and usuario_admin.Estado = "Activo"', (self.newUserEditar.get(),blake2b, self.id))
                self.mostrarDatosUsuarios()
                self.newEditar.destroy()
                messagebox.showinfo(title='Info', message='Usuario Editado')
            else:
                messagebox.showwarning(title='Warning', message='Contraseña no coiciden')
        else:
            messagebox.showwarning(title='Warning', message='Introduzca un valor')