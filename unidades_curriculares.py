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
        self.geometry('1050x470')
        self.resizable(width=0, height=0)
        self.iconbitmap(uptpc)

        self.container = ttk.Labelframe(self)
        self.container.grid(column=0,row=0)

        self.frameHora = ttk.Labelframe(self.container)
        self.frameHora.grid(column=0,row=0,padx=5,pady=5)
        self.treeHora = ttk.Treeview(self.frameHora, columns=['#1',"#2"],show='headings',height=5)
        self.treeHora.grid(row=0,column=0)
        self.treeHora.heading('#1', text = 'Id',)
        self.treeHora.heading('#2', text = 'Hora')
        self.treeHora.column('#1', width=50)
        self.treeHora.column('#2', width=110)
        self.scrollbarHora = ttk.Scrollbar(self.frameHora, orient=tk.VERTICAL, command=self.treeHora.yview)
        self.treeHora.configure(yscroll=self.scrollbarHora.set)
        self.scrollbarHora.grid(column=1,row=0, sticky='ns')


        self.frameDepartamento = ttk.Labelframe(self.container)
        self.frameDepartamento.grid(column=1,row=0)
        self.treeDepartamento = ttk.Treeview(self.frameDepartamento, columns=['#1',"#2"],show='headings',height=5)
        self.treeDepartamento.grid(row=0,column=0)
        self.treeDepartamento.heading('#1', text = 'Id',)
        self.treeDepartamento.heading('#2', text = 'Deparmento')
        self.treeDepartamento.column('#1', width=50)
        self.treeDepartamento.column('#2', width=120)
        self.scrollbaeDepartamento = ttk.Scrollbar(self.frameDepartamento, orient=tk.VERTICAL, command=self.treeDepartamento.yview)
        self.treeDepartamento.configure(yscroll=self.scrollbaeDepartamento.set)
        self.scrollbaeDepartamento.grid(column=1,row=0, sticky='ns')

        self.framePt = ttk.Labelframe(self.container)
        self.framePt.grid(column=2,row=0)
        self.treePt = ttk.Treeview(self.framePt, columns=['#1',"#2"],show='headings',height=5)
        self.treePt.grid(row=0,column=0)
        self.treePt.heading('#1', text = 'Id',)
        self.treePt.heading('#2', text = 'Pt')
        self.treePt.column('#1', width=50)
        self.treePt.column('#2', width=110)
        self.scrollbaePt = ttk.Scrollbar(self.framePt, orient=tk.VERTICAL, command=self.treePt.yview)
        self.treePt.configure(yscroll=self.scrollbaePt.set)
        self.scrollbaePt.grid(column=1,row=0, sticky='ns')

        self.frameDEntry = ttk.Labelframe(self.container)
        self.frameDEntry.grid(column=3,row=0)
        ttk.Label(self.frameDEntry,text='Departamento').grid(column=0,row=0)
        self.entryDEntry = ttk.Entry(self.frameDEntry,width=15)
        self.entryDEntry.grid(column=1,row=0)
        ttk.Button(self.frameDEntry, text='REGISTRAR DEPARTAMENTO', command=self.RegistrarDepartamento,width=26).grid(row=1,column=0)
        ttk.Button(self.frameDEntry, text='EDITAR DEPARTAMENTO', command=self.editarDepartamento,width=26).grid(row=2,column=0)
        ttk.Button(self.frameDEntry, text='ELIMINAR DEPARTAMENTO', command='',width=26).grid(row=3,column=0)

        self.framePEntry = ttk.Labelframe(self.container)
        self.framePEntry.grid(column=4,row=0)
        ttk.Label(self.framePEntry,text='Pt').grid(column=0,row=0)
        self.entryPEntry = ttk.Entry(self.framePEntry,width=15)
        self.entryPEntry.grid(column=1,row=0)
        ttk.Button(self.framePEntry, text='REGISTRAR PT', command=self.RegistrarPt,width=15).grid(row=1,column=0)
        ttk.Button(self.framePEntry, text='EDITAR PT', command=self.editarPt,width=15).grid(row=2,column=0)
        ttk.Button(self.framePEntry, text='ELIMINAR PT', command='',width=15).grid(row=3,column=0)

        self.frameUnidadesCurriculares = ttk.Labelframe(self)
        self.frameUnidadesCurriculares.grid(column=0,row=1,padx=5)
        self.treeUnidadesCurriculares = ttk.Treeview(self.frameUnidadesCurriculares, columns=['#1',"#2",'#3','#4','#5'],show='headings',height=10)
        self.treeUnidadesCurriculares.grid(row=0,column=0)
        self.treeUnidadesCurriculares.heading('#1', text = 'Id',)
        self.treeUnidadesCurriculares.heading('#2', text = 'Unidad Curricular')
        self.treeUnidadesCurriculares.heading('#3', text = 'Hora')
        self.treeUnidadesCurriculares.heading('#4', text = 'Departamento')
        self.treeUnidadesCurriculares.heading('#5', text = 'PT')
        self.treeUnidadesCurriculares.column('#1', width=50)
        self.treeUnidadesCurriculares.column('#2', width=240)
        self.treeUnidadesCurriculares.column('#3', width=240)
        self.treeUnidadesCurriculares.column('#4', width=240)
        self.treeUnidadesCurriculares.column('#5', width=240)
        self.scrollbarUnidadesCurriculares = ttk.Scrollbar(self.frameUnidadesCurriculares, orient=tk.VERTICAL, command=self.treeUnidadesCurriculares.yview)
        self.treeUnidadesCurriculares.configure(yscroll=self.scrollbarUnidadesCurriculares.set)
        self.scrollbarUnidadesCurriculares.grid(column=1,row=0, sticky='ns')

        self.frameButton = ttk.Labelframe(self)
        self.frameButton.grid(column=0,row=2,padx=5)
        ttk.Button(self.frameButton, text='AGREGAR/MODIFICAR - HORA',width=55).grid(row=0,column=0)
        ttk.Button(self.frameButton, text='AGREGAR/MODIFICAR - DEPARTAMENTO',width=55).grid(row=0,column=1)
        ttk.Button(self.frameButton, text='AGREGAR/MODIFICAR - PT',width=55).grid(row=0,column=2)

        self.MostrarDatosHora()
        self.MostrarDatosDepartamento()
        self.MostrarDatosPt()
        self.MostrarDatosUnidadesCurriculares()

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

    def limpiarTablaHora(self):
        self.DeleteChildren = self.treeHora.get_children()
        for element in self.DeleteChildren:
            self.treeHora.delete(element)
    
    def limpiarTablaDepartamento(self):
        self.DeleteChildren = self.treeDepartamento.get_children()
        for element in self.DeleteChildren:
            self.treeDepartamento.delete(element)

    def limpiarTablaPt(self):
        self.DeleteChildren = self.treePt.get_children()
        for element in self.DeleteChildren:
            self.treePt.delete(element)
    
    def limpiarTablaUnidadesCurriculares(self):
        self.DeleteChildren = self.treeUnidadesCurriculares.get_children()
        for element in self.DeleteChildren:
            self.treeUnidadesCurriculares.delete(element)

    def MostrarDatosHora(self):
        self.limpiarTablaHora()
        self.rows = self.TraerDatos("SELECT * FROM hora")
        for row in self.rows:
            self.treeHora.insert('',tk.END,values=row)
    
    def MostrarDatosDepartamento(self):
        self.limpiarTablaDepartamento()
        self.rows = self.TraerDatos("SELECT * FROM departamento")
        for row in self.rows:
            self.treeDepartamento.insert('',tk.END,values=row)

    def MostrarDatosPt(self):
        self.limpiarTablaPt()
        self.rows = self.TraerDatos("SELECT * FROM pt")
        for row in self.rows:
            self.treePt.insert('',tk.END,values=row)

    def MostrarDatosUnidadesCurriculares(self):
        self.limpiarTablaUnidadesCurriculares()
        self.rows = self.TraerDatos("SELECT Id,UnidadCurricular,Hora,Departamento,Pt COLLATE utf8_spanish2_ci FROM unidad_curricular ORDER BY UnidadCurricular")
        for row in self.rows:
            self.treeUnidadesCurriculares.insert('',tk.END,values=row)

    def ValidarCeldaDEntry(self):
        return len(self.entryDEntry.get())

    def ValidarCeldaPEntry(self):
        return len(self.entryPEntry.get())

    def LimpiarCeldaDEntry(self):
        self.entryDEntry.delete(0, tk.END)

    def LimpiarCeldaPEntry(self):
        self.entryPEntry.delete(0, tk.END) 

    def hora(self):
        self.item = self.treeHora.focus()
        self.data = self.treeHora.item(self.item)
        self.id = self.data['values'][1]
        return self.id

    def departamento(self):
        self.item = self.treeDepartamento.focus()
        self.data = self.treeDepartamento.item(self.item)
        self.id = self.data['values'][1]
        return self.id

    def pt(self):
        self.item = self.treePt.focus()
        self.data = self.treePt.item(self.item)
        self.id = self.data['values'][1]
        return self.id

    def selecionarFilaDepartamento(self):
        self.item = self.treeDepartamento.focus()
        self.data = self.treeDepartamento.item(self.item)
        self.id = self.data['values'][0]
        return self.id

    def selecionarFilaPt(self):
        self.item = self.treePt.focus()
        self.data = self.treePt.item(self.item)
        self.id = self.data['values'][0]
        return self.id

    def selecionarFilaUnidadesCurriculares(self):
        self.item = self.treeUnidadesCurriculares.focus()
        self.data = self.treeUnidadesCurriculares.item(self.item)
        self.id = self.data['values'][0]
        return self.id

    def RegistrarDepartamento(self):
        if self.ValidarCeldaDEntry():
            self.query = 'INSERT INTO departamento VALUES (NUll,?)'
            self.parametros = (self.entryDEntry.get())
            if self.conexion(self.query,(self.parametros,)):
                self.MostrarDatosDepartamento()
                self.LimpiarCeldaDEntry()
                messagebox.showinfo(title='Info', message='Departamento Registrado.')
            else:
                messagebox.showwarning(title='Warning', message='Departamento ya esta registrado.')
        else:
            messagebox.showwarning(title='Warning', message='Introduzca un valor.')

    def RegistrarPt(self):
        if self.ValidarCeldaPEntry():
            self.query = 'INSERT INTO pt VALUES (NUll,?)'
            self.parametros = (self.entryPEntry.get())
            if self.conexion(self.query,(self.parametros,)):
                self.MostrarDatosPt()
                self.LimpiarCeldaPEntry()
                messagebox.showinfo(title='Info', message='PT Registrado.')
            else:
                messagebox.showwarning(title='Warning', message='PT ya esta registrado.')
        else:
            messagebox.showwarning(title='Warning', message='Introduzca un valor.')

    def editarDepartamento(self):
        if self.ValidarCeldaDEntry() and self.treeDepartamento.selection():
            if messagebox.askyesno('Edit','¿Desea editar el departamento selecionado?'):
                self.query = 'UPDATE departamento SET Departamento = ? WHERE Id = ?'
                self.parametros = (self.entryDEntry.get())
                self.id = self.selecionarFilaDepartamento()
                self.conexion(self.query,(self.parametros, self.id))
                self.MostrarDatosDepartamento()
                self.LimpiarCeldaDEntry()
                messagebox.showinfo(title='Info', message='Departamento Editado Correctamente.')
            else:
                self.MostrarDatosDepartamento()
                self.LimpiarCeldaDEntry()
        else:
            messagebox.showwarning(title='Warning', message='Introduzca un valor y seleccione el departamento a editar.')

    def editarPt(self):
        if self.ValidarCeldaPEntry() and self.treePt.selection():
            if messagebox.askyesno('Edit','¿Desea editar el PT selecionado?'):
                self.query = 'UPDATE pt SET Pt = ? WHERE Id = ?'
                self.parametros = (self.entryPEntry.get())
                self.id = self.selecionarFilaPt()
                self.conexion(self.query,(self.parametros, self.id))
                self.MostrarDatosPt()
                self.LimpiarCeldaPEntry()
                messagebox.showinfo(title='Info', message='PT Editado Correctamente.')
            else:
                self.MostrarDatosPt()
                self.LimpiarCeldaPEntry()
        else:
            messagebox.showwarning(title='Warning', message='Introduzca un valor y seleccione el PT a editar.')
