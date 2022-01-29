import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3
from rutas import *
import traceback
import sys

class Unidades_curriculares(tk.Toplevel):
    def __init__(self,master):
        super().__init__(master)
        # Config:
        self.title('Unidades Curriculares')
        self.geometry('615x580')
        self.resizable(width=0, height=0)
        self.iconbitmap(uptpc)

        self.menubar = tk.Menu(self)
        self.menubar.add_cascade(label="Volver", command=self.volver)
        self.config(menu=self.menubar)

        self.frame = ttk.Labelframe(self)
        self.frame.grid(column=0,row=0,padx=5,pady=5)
        ttk.Label(self.frame,text='Unidad Curricular:').grid(row=0,column=0,padx=5,pady=5)
        self.entryUnidadCurricular = ttk.Entry(self.frame,width=40)
        self.entryUnidadCurricular.grid(row=0,column=1,padx=5,pady=5)
        self.entryUnidadCurricular.focus()
        ttk.Label(self.frame,text='Departamento:').grid(row=1,column=0,padx=5,pady=5)
        self.entryDepartamento = ttk.Entry(self.frame,width=40)
        self.entryDepartamento.grid(row=1,column=1,padx=5,pady=5)
        self.entryDepartamento.config(state=tk.DISABLED)
        ttk.Button(self.frame, text='ACTIVAR', command=self.activar2).grid(row=2,column=0)
        ttk.Button(self.frame, text='DESACTIVAR', command=self.desactivar2).grid(row=2,column=1)
        ttk.Label(self.frame,text='Programa tradiciónal:').grid(row=3,column=0,padx=5,pady=5)
        self.entryPrograma = ttk.Entry(self.frame,width=40)
        self.entryPrograma.grid(row=3,column=1,padx=5,pady=5)
        self.entryPrograma.config(state=tk.DISABLED)
        ttk.Button(self.frame, text='ACTIVAR', command=self.activar).grid(row=4,column=0)
        ttk.Button(self.frame, text='DESACTIVAR', command=self.desactivar).grid(row=4,column=1)
        ttk.Label(self.frame,text='Hora:').grid(row=5,column=0,padx=5,pady=5)
        self.hora = tk.StringVar()
        self.frameRadio = ttk.Labelframe(self.frame)
        self.frameRadio.grid(row=5,column=1)
        ttk.Radiobutton(self.frameRadio, text='2', value='2',variable=self.hora).grid(row=0,column=0)
        ttk.Radiobutton(self.frameRadio, text='3', value='3',variable=self.hora).grid(row=0,column=1)
        ttk.Radiobutton(self.frameRadio, text='4', value='4',variable=self.hora).grid(row=0,column=2)
        ttk.Radiobutton(self.frameRadio, text='5', value='5',variable=self.hora).grid(row=0,column=3)
        ttk.Radiobutton(self.frameRadio, text='6', value='6',variable=self.hora).grid(row=0,column=4)
        self.frame2 = ttk.LabelFrame(self)
        self.frame2.grid(column=0,row=1)
        ttk.Button(self.frame2, text='REGISTRAR UNIDAD CURRICULAR', command=self.RegistrarUnidadCurricular,width=33).grid(row=0,column=0)
        ttk.Button(self.frame2, text='EDITAR UNIDAD CURRICULAR', command=self.modificarUnidadCurricular,width=33).grid(row=0,column=1)
        
        self.frameUnidadesCurriculares = ttk.Labelframe(self)
        self.frameUnidadesCurriculares.grid(column=0,row=2,padx=5)
        self.treeUnidadesCurriculares = ttk.Treeview(self.frameUnidadesCurriculares, columns=['#1',"#2",'#3','#4','#5'],show='headings',height=10)
        self.treeUnidadesCurriculares.grid(row=0,column=0)
        self.treeUnidadesCurriculares.heading('#1', text = 'Id',)
        self.treeUnidadesCurriculares.heading('#2', text = 'Unidad Curricular')
        self.treeUnidadesCurriculares.heading('#3', text = 'Hora')
        self.treeUnidadesCurriculares.heading('#4', text = 'Departamento')
        self.treeUnidadesCurriculares.heading('#5', text = 'Programa Tradiciónal')
        self.treeUnidadesCurriculares.column('#1', width=50)
        self.treeUnidadesCurriculares.column('#2', width=240)
        self.treeUnidadesCurriculares.column('#3', width=40)
        self.treeUnidadesCurriculares.column('#4', width=120)
        self.treeUnidadesCurriculares.column('#5', width=130)
        self.treeUnidadesCurriculares.bind('<Double-1>',lambda e, tree = self.treeUnidadesCurriculares: self.doubleClick(tree))
        self.scrollbarUnidadesCurriculares = ttk.Scrollbar(self.frameUnidadesCurriculares, orient=tk.VERTICAL, command=self.treeUnidadesCurriculares.yview)
        self.treeUnidadesCurriculares.configure(yscroll=self.scrollbarUnidadesCurriculares.set)
        self.scrollbarUnidadesCurriculares.grid(column=1,row=0, sticky='ns')

        self.frameButton = ttk.LabelFrame(self)
        self.frameButton.grid(column=0,row=3,padx=5)
        ttk.Button(self.frameButton, text='DESHABILITAR UNIDAD CURRICULAR', command=self.eliminarUnidadCurricular,width=33).grid(row=0,column=1)

        self.MostrarDatosUnidadesCurriculares()

    def volver(self):
        self.destroy()

    def activar(self):
        self.entryPrograma.config(state=tk.NORMAL)
        self.entryPrograma.focus()

    def activar2(self):
        self.entryDepartamento.config(state=tk.NORMAL)
        self.entryDepartamento.focus()

    def desactivar(self):
        self.entryPrograma.config(state=tk.DISABLED)
        self.entryUnidadCurricular.focus()
        
    def desactivar2(self):
        self.entryDepartamento.config(state=tk.DISABLED)
        self.entryUnidadCurricular.focus()

    def doubleClick(self,tree):
        item = tree.focus()
        data = tree.item(item)
        unidad = data['values'][1]
        hora = data['values'][2]
        departamento = data['values'][3]
        programa = data['values'][4]
        self.entryUnidadCurricular.delete(0, tk.END)
        self.entryUnidadCurricular.insert(0,unidad)
        self.hora.set(value=hora)
        if not departamento == ' ':
            self.entryDepartamento.config(state=tk.NORMAL)
            self.entryDepartamento.delete(0, tk.END)
            self.entryDepartamento.insert(0,departamento)
        else:
            self.entryDepartamento.delete(0, tk.END)
            self.entryDepartamento.config(state=tk.DISABLED)
        if not programa == ' ':
            self.entryPrograma.config(state=tk.NORMAL)
            self.entryPrograma.delete(0, tk.END)
            self.entryPrograma.insert(0,programa)
        else:
            self.entryPrograma.delete(0, tk.END)
            self.entryPrograma.config(state=tk.DISABLED)        

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

    def limpiarTablaUnidadesCurriculares(self):
        self.DeleteChildren = self.treeUnidadesCurriculares.get_children()
        for element in self.DeleteChildren:
            self.treeUnidadesCurriculares.delete(element)

    def MostrarDatosUnidadesCurriculares(self):
        self.limpiarTablaUnidadesCurriculares()
        self.rows = self.TraerDatos("SELECT Id,UnidadCurricular,Hora,Departamento,Pt FROM unidad_curricular WHERE unidad_curricular.Estado = 'Activo' ORDER BY UnidadCurricular")
        for row in self.rows:
            self.treeUnidadesCurriculares.insert('',tk.END,values=row)

    def selecionarFilaUnidadesCurriculares(self):
        self.item = self.treeUnidadesCurriculares.focus()
        self.data = self.treeUnidadesCurriculares.item(self.item)
        self.id = self.data['values'][0]
        return self.id

    def departamento(self):
        if not self.entryDepartamento.state():
            return self.entryDepartamento.get()
        else:
            return ' '

    def programa(self):
        if not self.entryPrograma.state():
            return self.entryPrograma.get()
        else:
            return ' '
    
    def cantidad(self):
        if self.hora.get():
            return self.hora.get()
        else:
            return ' '        

    def RegistrarUnidadCurricular(self):
        if len(self.entryUnidadCurricular.get()) != 0 and self.hora.get():
            if messagebox.askyesno('Registrar','¿Desea registrar la unidad curricular?'):
                if self.conexion('INSERT INTO unidad_curricular VALUES (NUll,?,?,?,?,"Activo")',(self.entryUnidadCurricular.get(),self.cantidad(),self.departamento(),self.programa())):
                    self.MostrarDatosUnidadesCurriculares()
                    self.entryUnidadCurricular.delete(0, tk.END)
                    self.entryDepartamento.delete(0, tk.END)
                    self.entryPrograma.delete(0, tk.END)
                    self.hora.set(value='')
                    messagebox.showinfo(title='Info', message='Unidad Curricular Registrada.')
                else:
                    messagebox.showwarning(title='Warning', message='Unidad curricilar ya esta registrada')
            else:
                self.entryUnidadCurricular.focus()
        else:
            messagebox.showwarning(title='Warning', message='Introduzca un valor')

    def eliminarUnidadCurricular(self):
        if self.treeUnidadesCurriculares.selection():
            if messagebox.askyesno('Deshabilitar','¿Desea deshabilitar la unidad curricular selecionada?'):
                self.query = 'UPDATE unidad_curricular SET Estado = "Inactivo" WHERE unidad_curricular.id = ? and unidad_curricular.Estado = "Activo"'
                self.parametros = self.selecionarFilaUnidadesCurriculares()
                self.conexion(self.query, (self.parametros,)) 
                self.MostrarDatosUnidadesCurriculares()
                messagebox.showinfo(title='Info', message='Unidad curricular deshabilitada correctamente.')
            else:
                self.MostrarDatosUnidadesCurriculares()
        else:
            messagebox.showwarning(title='Wanning', message='Seleccione una unidad curricular a deshabilitar.')

    def modificarUnidadCurricular(self):
        if len(self.entryUnidadCurricular.get()) != 0 and self.hora.get():
            if messagebox.askyesno('Edit','¿Desea editar la unidad curricular selecionada?'):
                self.conexion('UPDATE unidad_curricular SET UnidadCurricular = ? WHERE unidad_curricular.id = ? and unidad_curricular.Estado = "Activo"',(self.entryUnidadCurricular.get(), self.selecionarFilaUnidadesCurriculares()))
                self.conexion('UPDATE unidad_curricular SET Hora = ? WHERE unidad_curricular.id = ? and unidad_curricular.Estado = "Activo"',(self.cantidad(), self.selecionarFilaUnidadesCurriculares()))
                self.conexion('UPDATE unidad_curricular SET Departamento = ? WHERE unidad_curricular.id = ? and unidad_curricular.Estado = "Activo"',(self.departamento(), self.selecionarFilaUnidadesCurriculares()))
                self.conexion('UPDATE unidad_curricular SET Pt = ? WHERE unidad_curricular.id = ? and unidad_curricular.Estado = "Activo"',(self.programa(), self.selecionarFilaUnidadesCurriculares()))
                self.MostrarDatosUnidadesCurriculares()
                self.entryUnidadCurricular.delete(0, tk.END)
                self.entryDepartamento.delete(0, tk.END)
                self.entryPrograma.delete(0, tk.END)
                self.hora.set(value='')
                messagebox.showinfo(title='Info', message='Unidad curricular Editada Correctamente.')
        else:
            messagebox.showwarning(title='Warning', message='Seleccione una la unidad curricular a editar.')