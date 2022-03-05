import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3
from rutas import *
import traceback
import sys

class Gestor(tk.Toplevel):
    def __init__(self,master):
        super().__init__(master)
        # Config:
        self.title('Gestionar tablas')
        self.geometry('470x400')
        self.resizable(width=0, height=0)
        self.iconbitmap(uptpc)

        # Menu:
        self.menubar = tk.Menu(self)
        self.menubar.add_cascade(label="Volver", command=self.volver)
        self.config(menu=self.menubar)
        
        # create a notebook
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(pady=0,padx=5,expand=True)

        # create frames
        self.noteCohorte = ttk.Frame(self.notebook, width=470, height=400)
        self.noteLapsoAcademico = ttk.Frame(self.notebook,width=470, height=400)
        self.noteTrayecto = ttk.Frame(self.notebook, width=470, height=400)
        self.noteTrimestre = ttk.Frame(self.notebook, width=470, height=400)
        self.noteSeccion = ttk.Frame(self.notebook, width=470, height=400)
        self.noteLaboratorio = ttk.Frame(self.notebook, width=470, height=400)

        # create frames
        self.noteCohorte.pack(fill='both', expand=True)
        self.noteLapsoAcademico.pack(fill='both', expand=True)
        self.noteTrayecto.pack(fill='both', expand=True)
        self.noteTrimestre.pack(fill='both', expand=True)
        self.noteSeccion.pack(fill='both', expand=True)
        self.noteLaboratorio.pack(fill='both', expand=True)

        # add frames to notebook
        self.notebook.add(self.noteCohorte, text='Cohorte')
        self.notebook.add(self.noteLapsoAcademico, text='Lapso académico')
        self.notebook.add(self.noteTrayecto, text='Trayecto')
        self.notebook.add(self.noteTrimestre, text='Trimestre')
        self.notebook.add(self.noteSeccion, text='Sección')
        self.notebook.add(self.noteLaboratorio, text='Laboratorio')
            
        # Pantalla Cohorte 0/3
        self.frameCohorte = ttk.LabelFrame(self.noteCohorte)
        self.frameCohorte.grid(column=0,row=0,pady=10, padx=15)

        # Cohorte frame 1/3
        ttk.Label(self.frameCohorte,text='Cohorte').grid(column=0,row=0)
        self.entryCohorte = ttk.Entry(self.frameCohorte,width=45)
        self.entryCohorte.grid(column=1,row=0,padx=0,pady=5)
        ttk.Button(self.frameCohorte, text='REGISTRAR COHORTE', command= self.RegistrarCohorte).grid(row=1,column=0, sticky = tk.W + tk.E)
        ttk.Button(self.frameCohorte, text='EDITAR COHORTE', command=self.editarCohorte).grid(row=1,column=1, sticky = tk.W + tk.E)

        # Cohorte Tabla 2/3
        self.treeCohorte = ttk.Treeview(self.noteCohorte,columns = ['#1','#2'], show='headings')
        self.treeCohorte.grid(column=0,row=1, sticky='nsew')
        self.treeCohorte.heading('#1', text = 'Id')
        self.treeCohorte.heading('#2', text = 'Cohorte')
        self.treeCohorte.bind('<Double-1>',lambda e, tree = self.treeCohorte: self.doubleClick(tree,self.entryCohorte))
        self.scrollbarCohorte = ttk.Scrollbar(self.noteCohorte, orient=tk.VERTICAL, command=self.treeCohorte.yview)
        self.treeCohorte.configure(yscroll=self.scrollbarCohorte.set)
        self.scrollbarCohorte.grid(column=1,row=1, sticky='ns')

        # Cohorte Botones 3/3
        ttk.Button(self.noteCohorte,text = 'DESHABILITAR COHORTE', command = self.eliminarCohorte).grid(column=0,row=2,sticky = tk.W + tk.E)

        # Pantalla LapsoAcademico 0/3
        self.frameLapsoAcademico = ttk.LabelFrame(self.noteLapsoAcademico)
        self.frameLapsoAcademico.grid(column=0,row=0,pady=10, padx=3)

        # LapsoAcademico frame 1/3
        ttk.Label(self.frameLapsoAcademico,text='Lapso académico').grid(column=0,row=0)
        self.entryLapsoAcademico = ttk.Entry(self.frameLapsoAcademico,width=40)
        self.entryLapsoAcademico.grid(column=1,row=0,padx=0,pady=5)
        ttk.Button(self.frameLapsoAcademico, text='REGISTRAR LAPSO ACADÉMICO', command=self.RegistrarLapsoAcademico).grid(row=1,column=0, sticky = tk.W + tk.E)
        ttk.Button(self.frameLapsoAcademico, text='EDITAR LAPSO ACADÉMICO', command=self.editarLapsoAcademico).grid(row=1,column=1, sticky = tk.W + tk.E)

        # LapsoAcademico Tabla 2/3
        self.treeLapsoAcademico = ttk.Treeview(self.noteLapsoAcademico,columns = ['#1','#2'], show='headings')
        self.treeLapsoAcademico.grid(column=0,row=1, sticky='nsew')
        self.treeLapsoAcademico.heading('#1', text = 'Id')
        self.treeLapsoAcademico.heading('#2', text = 'Lapso académico')
        self.treeLapsoAcademico.bind('<Double-1>',lambda e, tree = self.treeLapsoAcademico: self.doubleClick(tree,self.entryLapsoAcademico))
        self.scrollbarLapsoAcademico = ttk.Scrollbar(self.noteLapsoAcademico, orient=tk.VERTICAL, command=self.treeLapsoAcademico.yview)
        self.treeLapsoAcademico.configure(yscroll=self.scrollbarLapsoAcademico.set)
        self.scrollbarLapsoAcademico.grid(column=1,row=1, sticky='ns')

        # LapsoAcademico Botones 3/3
        ttk.Button(self.noteLapsoAcademico,text = 'DESHABILITAR LAPSO ACADÉMICO', command = self.eliminarLapsoAcademico).grid(column=0,row=2,sticky = tk.W + tk.E)

        # Pantalla Trayecto 0/3
        self.frameTrayecto = ttk.LabelFrame(self.noteTrayecto)
        self.frameTrayecto.grid(column=0,row=0,pady=10,padx=12)

        # Trayecto frame 1/3
        ttk.Label(self.frameTrayecto,text='Trayecto').grid(column=0,row=0)
        self.entryTrayecto = ttk.Entry(self.frameTrayecto,width=45)
        self.entryTrayecto.grid(column=1,row=0,padx=0,pady=5)
        ttk.Button(self.frameTrayecto, text='REGISTRAR TRAYECTO', command= self.RegistrarTrayecto).grid(row=1,column=0, sticky = tk.W + tk.E)
        ttk.Button(self.frameTrayecto, text='EDITAR TRAYECTO', command= self.editarTrayecto).grid(row=1,column=1, sticky = tk.W + tk.E)

        # Trayecto Tabla 2/3
        self.treeTrayecto = ttk.Treeview(self.noteTrayecto,columns = ['#1','#2'], show='headings')
        self.treeTrayecto.grid(column=0,row=1, sticky='nsew')
        self.treeTrayecto.heading('#1', text = 'Id')
        self.treeTrayecto.heading('#2', text = 'Trayecto')
        self.treeTrayecto.bind('<Double-1>',lambda e, tree = self.treeTrayecto: self.doubleClick(tree,self.entryTrayecto))
        self.scrollbarTrayecto = ttk.Scrollbar(self.noteTrayecto, orient=tk.VERTICAL, command=self.treeTrayecto.yview)
        self.treeTrayecto.configure(yscroll=self.scrollbarTrayecto.set)
        self.scrollbarTrayecto.grid(column=1,row=1, sticky='ns')

        # Trayecto Botones 3/3
        ttk.Button(self.noteTrayecto,text = 'DESHABILITAR TRAYECTO', command = self.eliminarTrayecto).grid(column=0,row=2,sticky = tk.W + tk.E)

        # Pantalla trimestre 0/3
        self.frameTrimestre = ttk.LabelFrame(self.noteTrimestre)
        self.frameTrimestre.grid(column=0,row=0,pady=10,padx=11)

        # Trimestre frame 1/3
        ttk.Label(self.frameTrimestre,text='Trimestre').grid(column=0,row=0)
        self.entryTrimestre = ttk.Entry(self.frameTrimestre,width=45)
        self.entryTrimestre.grid(column=1,row=0,padx=0,pady=5)
        ttk.Button(self.frameTrimestre, text='REGISTRAR TRIMESTRE', command= self.RegistrarTrimestre).grid(row=1,column=0, sticky = tk.W + tk.E)
        ttk.Button(self.frameTrimestre, text='EDITAR TRIMESTRE', command= self.editarTrimestre).grid(row=1,column=1, sticky = tk.W + tk.E)

        # Trimestre Tabla 2/3
        self.treeTrimestre = ttk.Treeview(self.noteTrimestre,columns =['#1','#2'], show='headings')
        self.treeTrimestre.grid(column=0,row=1, sticky='nsew')
        self.treeTrimestre.heading('#1', text = 'Id')
        self.treeTrimestre.heading('#2', text = 'Trimestre')
        self.treeTrimestre.bind('<Double-1>',lambda e, tree = self.treeTrimestre: self.doubleClick(tree,self.entryTrimestre))
        self.scrollbarTrimestre = ttk.Scrollbar(self.noteTrimestre, orient=tk.VERTICAL, command=self.treeTrimestre.yview)
        self.treeTrimestre.configure(yscroll=self.scrollbarTrimestre.set)
        self.scrollbarTrimestre.grid(column=1,row=1, sticky='ns')

        # Trimestre Botones 3/3
        ttk.Button(self.noteTrimestre,text = 'DESHABILITAR TRIMESTRE', command = self.eliminarTrimestre).grid(column=0,row=2,sticky = tk.W + tk.E)      
        
        # Pantalla Seccion 0/3
        self.frameSeccion = ttk.LabelFrame(self.noteSeccion)
        self.frameSeccion.grid(column=0,row=0,pady=10,padx=22)

        # Seccion frame 1/3
        ttk.Label(self.frameSeccion,text='Sección').grid(column=0,row=0)
        self.entrySeccion = ttk.Entry(self.frameSeccion,width=45)
        self.entrySeccion.grid(column=1,row=0,padx=0,pady=5)
        ttk.Button(self.frameSeccion, text='REGISTAR SECCIÓN', command= self.RegistrarSeccion).grid(row=1,column=0, sticky = tk.W + tk.E)
        ttk.Button(self.frameSeccion, text='EDITAR SECCIÓN', command=  self.editarSeccion).grid(row=1,column=1, sticky = tk.W + tk.E)

        # Seccion Tabla 2/3
        self.treeSeccion = ttk.Treeview(self.noteSeccion,columns = ['#1','#2'], show='headings')
        self.treeSeccion.grid(column=0,row=1, sticky='nsew')
        self.treeSeccion.heading('#1', text = 'Id')
        self.treeSeccion.heading('#2', text = 'Sección')
        self.treeSeccion.bind('<Double-1>',lambda e, tree = self.treeSeccion: self.doubleClick(tree,self.entrySeccion))
        self.scrollbarSeccion = ttk.Scrollbar(self.noteSeccion, orient=tk.VERTICAL, command=self.treeSeccion.yview)
        self.treeSeccion.configure(yscroll=self.scrollbarSeccion.set)
        self.scrollbarSeccion.grid(column=1,row=1, sticky='ns')

        # Seccion Botones 3/3
        ttk.Button(self.noteSeccion,text = 'DESHABILITAR SECCIÓN', command = self.eliminarSeccion).grid(column=0,row=2,sticky = tk.W + tk.E)

        # Pantalla Laboratorio 0/3
        self.frameLaboratorio = ttk.LabelFrame(self.noteLaboratorio)
        self.frameLaboratorio.grid(column=0,row=0,pady=10,padx=23)

        # UnidadLaboratorio 1/3
        ttk.Label(self.frameLaboratorio,text='Laboratorio').grid(column=0,row=0)
        self.entryLaboratorio = ttk.Entry(self.frameLaboratorio,width=38)
        self.entryLaboratorio.grid(column=1,row=0,padx=0,pady=5)
        ttk.Button(self.frameLaboratorio, text='REGISTRAR LABORATOIRO', command= self.RegistrarLaboratorio).grid(row=1,column=0, sticky = tk.W + tk.E)
        ttk.Button(self.frameLaboratorio, text='EDITAR LABORATORIO ', command= self.editarLaboratorio).grid(row=1,column=1, sticky = tk.W + tk.E)

        # UnidadLaboratorio 2/3
        self.treeLaboratorio = ttk.Treeview(self.noteLaboratorio,columns =['#1','#2'], show='headings')
        self.treeLaboratorio.grid(column=0,row=1, sticky='nsew')
        self.treeLaboratorio.heading('#1', text = 'Id')
        self.treeLaboratorio.heading('#2', text = 'Laboratorio')
        self.treeLaboratorio.bind('<Double-1>',lambda e, tree = self.treeLaboratorio: self.doubleClick(tree,self.entryLaboratorio))
        self.treeLaboratorio.column('#1',width=60)
        self.scrollbarLaboratorio = ttk.Scrollbar(self.noteLaboratorio, orient=tk.VERTICAL, command=self.treeLaboratorio.yview)
        self.treeLaboratorio.configure(yscroll=self.scrollbarLaboratorio.set)
        self.scrollbarLaboratorio.grid(column=1,row=1, sticky='ns')

        # Unidad CLaboratorio 3/3
        ttk.Button(self.noteLaboratorio,text = 'DESHABILITAR LABORATORIO', command = self.eliminarLaboratorio).grid(column=0,row=2,sticky = tk.W + tk.E)

        self.MostrarDatosCohorte()
        self.MostrarDatosLapsoAcademico()
        self.MostrarDatosTrayecto()
        self.MostrarDatosTrimestre()
        self.MostrarDatosSeccion()
        self.MostrarDatosLaboratorio()

    def volver(self):
        self.destroy()

    def doubleClick(self,tree,entry):
        item = tree.focus()
        data = tree.item(item)
        id = data['values'][1]
        entry.delete(0, tk.END)
        entry.insert(0,id)

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

    def limpiarTablaCohorte(self):
        self.DeleteChildren = self.treeCohorte.get_children()
        for element in self.DeleteChildren:
            self.treeCohorte.delete(element)
    
    def limpiarTablaLapsoAcademico(self):
        self.DeleteChildren = self.treeLapsoAcademico.get_children()
        for element in self.DeleteChildren:
            self.treeLapsoAcademico.delete(element)

    def limpiarTablaTrayecto(self):
        self.DeleteChildren = self.treeTrayecto.get_children()
        for element in self.DeleteChildren:
            self.treeTrayecto.delete(element)

    def limpiarTablaTrimestre(self):
        self.DeleteChildren = self.treeTrimestre.get_children()
        for element in self.DeleteChildren:
            self.treeTrimestre.delete(element)

    def limpiarTablaSeccion(self):
        self.DeleteChildren = self.treeSeccion.get_children()
        for element in self.DeleteChildren:
            self.treeSeccion.delete(element)

    def limpiarTablaLaboratorio(self):
        self.DeleteChildren = self.treeLaboratorio.get_children()
        for element in self.DeleteChildren:
            self.treeLaboratorio.delete(element)
        
    def MostrarDatosCohorte(self):
        self.limpiarTablaCohorte()
        self.rows = self.TraerDatos("SELECT * FROM cohorte WHERE cohorte.Estado = 'Activo'")
        for row in self.rows:
            self.treeCohorte.insert('',tk.END,values=row)
    
    def MostrarDatosLapsoAcademico(self):
        self.limpiarTablaLapsoAcademico()
        self.rows = self.TraerDatos("SELECT * FROM lapso_academico WHERE lapso_academico.Estado = 'Activo'")
        for row in self.rows:
            self.treeLapsoAcademico.insert('',tk.END,values=row)

    def MostrarDatosTrayecto(self):
        self.limpiarTablaTrayecto()
        self.rows = self.TraerDatos("SELECT * FROM trayecto WHERE trayecto.Estado = 'Activo'")
        for row in self.rows:
            self.treeTrayecto.insert('',tk.END,values=row)

    def MostrarDatosTrimestre(self):
        self.limpiarTablaTrimestre()
        self.rows = self.TraerDatos("SELECT * FROM trimestre WHERE trimestre.Estado = 'Activo'")
        for row in self.rows:
            self.treeTrimestre.insert('',tk.END,values=row)

    def MostrarDatosSeccion(self):
        self.limpiarTablaSeccion()
        self.rows = self.TraerDatos("SELECT * FROM seccion WHERE seccion.Estado = 'Activo'")
        for row in self.rows:
            self.treeSeccion.insert('',tk.END,values=row)

    def MostrarDatosLaboratorio(self):
        self.limpiarTablaLaboratorio()
        self.rows = self.TraerDatos("SELECT * FROM laboratorio WHERE laboratorio.Estado = 'Activo'")
        for row in self.rows:
            self.treeLaboratorio.insert('',tk.END,values=row)

    def selecionarFilaCohorte(self):
        self.item = self.treeCohorte.focus()
        self.data = self.treeCohorte.item(self.item)
        self.id = self.data['values'][0]
        return self.id

    def selecionarFilaLapsoAcademico(self):
        self.item = self.treeLapsoAcademico.focus()
        self.data = self.treeLapsoAcademico.item(self.item)
        self.id = self.data['values'][0]
        return self.id
    
    def selecionarFilaTrayecto(self):
        self.item = self.treeTrayecto.focus()
        self.data = self.treeTrayecto.item(self.item)
        self.id = self.data['values'][0]
        return self.id

    def selecionarFilaTrimestre(self):
        self.item = self.treeTrimestre.focus()
        self.data = self.treeTrimestre.item(self.item)
        self.id = self.data['values'][0]
        return self.id

    def selecionarFilaSeccion(self):
        self.item = self.treeSeccion.focus()
        self.data = self.treeSeccion.item(self.item)
        self.id = self.data['values'][0]
        return self.id

    def selecionarFilaLaboratorio(self):
        self.item = self.treeLaboratorio.focus()
        self.data = self.treeLaboratorio.item(self.item)
        self.id = self.data['values'][0]
        return self.id

    def eliminarCohorte(self):
        if self.treeCohorte.selection():
            if messagebox.askyesno('Deshabilitar','¿Desea deshabilitar el cohorte selecionado?',parent=self):
                self.query = 'UPDATE cohorte SET Estado = "Inactivo" WHERE cohorte.id = ? and cohorte.Estado = "Activo" '
                self.parametros = self.selecionarFilaCohorte()
                self.conexion(self.query, (self.parametros,)) 
                self.MostrarDatosCohorte()
                messagebox.showinfo(title='Info', message='Cohorte deshabilitado correctamente.',parent=self)
            else:
                self.MostrarDatosCohorte()
        else:
            messagebox.showwarning(title='Warning', message='Seleccione un cohorte a deshabilitar.',parent=self)

    def eliminarLapsoAcademico(self):
        if self.treeLapsoAcademico.selection():
            if messagebox.askyesno('Deshabilitar','¿Desea deshabilitar el lapso académico selecionado?',parent=self):
                self.query = 'UPDATE lapso_academico SET Estado = "Inactivo" WHERE lapso_academico.id = ? and lapso_academico.Estado = "Activo" '
                self.parametros = self.selecionarFilaLapsoAcademico()
                self.conexion(self.query, (self.parametros,)) 
                self.MostrarDatosLapsoAcademico()
                messagebox.showinfo(title='Info', message='Lapso académico deshabilitado correctamente.',parent=self)
            else:
                self.MostrarDatosLapsoAcademico()
        else:
            messagebox.showwarning(title='Warning', message='Seleccione un Lapso académico a deshabilitar.',parent=self)

    def eliminarTrayecto(self):
        if self.treeTrayecto.selection():
            if messagebox.askyesno('Deshabilitar','¿Desea deshabilitar el trayecto selecionado?',parent=self):
                self.query = 'UPDATE trayecto SET Estado = "Inactivo" WHERE trayecto.id = ? and trayecto.Estado = "Activo" '
                self.parametros = self.selecionarFilaTrayecto()
                self.conexion(self.query, (self.parametros,)) 
                self.MostrarDatosTrayecto()
                messagebox.showinfo(title='Info', message='Trayecto deshabilitado correctamente.',parent=self)
            else:
                self.MostrarDatosTrayecto()
        else:
            messagebox.showwarning(title='Warning', message='Seleccione un tracyecto a deshabilitar.',parent=self)

    def eliminarTrimestre(self):
        if self.treeTrimestre.selection():
            if messagebox.askyesno('Deshabilitar','¿Desea deshabilitar el trimestre selecionado?',parent=self):
                self.query = 'UPDATE trimestre SET Estado = "Inactivo" WHERE trimestre.id = ? and trimestre.Estado = "Activo"'
                self.parametros = self.selecionarFilaTrimestre()
                self.conexion(self.query, (self.parametros,)) 
                self.MostrarDatosTrimestre()
                messagebox.showinfo(title='Info', message='Trimestre deshabilitado correctamente.',parent=self)
            else:
                self.MostrarDatosTrimestre()
        else:
            messagebox.showwarning(title='Warning', message='Seleccione un trimestre a deshabilitar.',parent=self)

    def eliminarSeccion(self):
        if self.treeSeccion.selection():
            if messagebox.askyesno('Deshabilitar','¿Desea deshabilitarla sección selecionado?',parent=self):
                self.query = 'UPDATE seccion SET Estado = "Inactivo" WHERE seccion.id = ? and seccion.Estado = "Activo"'
                self.parametros = self.selecionarFilaSeccion()
                self.conexion(self.query, (self.parametros,)) 
                self.MostrarDatosSeccion()
                messagebox.showinfo(title='Info', message='Sección deshabilitado correctamente.',parent=self)
            else:
                self.MostrarDatosSeccion()
        else:
            messagebox.showwarning(title='Warning', message='Seleccione un sección a deshabilitar.',parent=self)

    def eliminarLaboratorio(self):
        if self.treeLaboratorio.selection():
            if messagebox.askyesno('Deshabilitar','¿Desea deshabilitar el laboratoiro selecionado?',parent=self):
                self.query = 'UPDATE laboratorio SET Estado = "Inactivo" WHERE laboratorio.id = ? and laboratorio.Estado = "Activo"'
                self.parametros = self.selecionarFilaLaboratorio()
                self.conexion(self.query, (self.parametros,)) 
                self.MostrarDatosLaboratorio()
                messagebox.showinfo(title='Info', message='Laboratorio deshabilitado correctamente.',parent=self)
            else:
                self.MostrarDatosLaboratorio()
        else:
            messagebox.showwarning(title='Warning', message='Seleccione un laboratorio a deshabilitar.',parent=self)
 
    def ValidarCeldaCohorte(self):
        return len(self.entryCohorte.get())

    def ValidarCeldaLapsoAcademico(self):
        return len(self.entryLapsoAcademico.get())
    
    def ValidarCeldaTrayecto(self):
        return len(self.entryTrayecto.get())
    
    def ValidarCeldaTrimestre(self):
        return len(self.entryTrimestre.get())

    def ValidarCeldaSeccion(self):
        return len(self.entrySeccion.get())

    def ValidarCeldaLaboratorio(self):
        return len(self.entryLaboratorio.get())

    def LimpiarCeldaCohorte(self):
        self.entryCohorte.delete(0, tk.END)

    def LimpiarCeldaLapsoAcademico(self):
        self.entryLapsoAcademico.delete(0, tk.END) 

    def LimpiarCeldaTrayecto(self):
        self.entryTrayecto.delete(0, tk.END)

    def LimpiarCeldaTrimestre(self):
        self.entryTrimestre.delete(0, tk.END)

    def LimpiarCeldaSeccion(self):
        self.entrySeccion.delete(0, tk.END)

    def LimpiarCeldaLaboratorio(self):
        self.entryLaboratorio.delete(0, tk.END)

    def RegistrarCohorte(self):
        if self.ValidarCeldaCohorte():
            self.query = 'INSERT INTO cohorte VALUES (NUll,?,"Activo")'
            self.parametros = (self.entryCohorte.get())
            if self.conexion(self.query,(self.parametros,)):
                self.MostrarDatosCohorte()
                self.LimpiarCeldaCohorte()
                messagebox.showinfo(title='Info', message='Cohorte Registrado.',parent=self)
            else:
                messagebox.showwarning(title='Warning', message='Cohorte ya esta registrado.',parent=self)
        else:
            messagebox.showwarning(title='Warning', message='Introduzca un valor.',parent=self)

    def RegistrarLapsoAcademico(self):
        if self.ValidarCeldaLapsoAcademico():
            self.query = 'INSERT INTO lapso_academico VALUES (NUll,?,"Activo")'
            self.parametros = (self.entryLapsoAcademico.get())
            if self.conexion(self.query,(self.parametros,)):
                self.MostrarDatosLapsoAcademico()
                self.LimpiarCeldaLapsoAcademico()
                messagebox.showinfo(title='Info', message='Lapso académico Registrado.',parent=self)
            else:
                messagebox.showwarning(title='Warning', message='Lapso académico ya esta registrado.',parent=self)
        else:
            messagebox.showwarning(title='Warning', message='Introduzca un valor.',parent=self)

    def RegistrarTrayecto(self):
        if self.ValidarCeldaTrayecto():
            self.query = 'INSERT INTO trayecto VALUES (NUll,?,"Activo")'
            self.parametros = (self.entryTrayecto.get())
            if self.conexion(self.query,(self.parametros,)):
                self.MostrarDatosTrayecto()
                self.LimpiarCeldaTrayecto()
                messagebox.showinfo(title='Info', message='Trayecto Registrado.',parent=self)
            else:
                messagebox.showwarning(title='Warning', message='Trayecto ya esta registrado.',parent=self)
        else:
            messagebox.showwarning(title='Warning', message='Introduzca un valor.',parent=self)

    def RegistrarTrimestre(self):
        if self.ValidarCeldaTrimestre():
            self.query = 'INSERT INTO trimestre VALUES (NUll,?,"Activo")'
            self.parametros = (self.entryTrimestre.get())
            if self.conexion(self.query,(self.parametros,)):
                self.MostrarDatosTrimestre()   
                self.LimpiarCeldaTrimestre()
                messagebox.showinfo(title='Info', message='Trimestre Registrado.',parent=self)
            else:
                messagebox.showwarning(title='Warning', message='Trimestre ya esta registrado.',parent=self)
        else:
            messagebox.showwarning(title='Warning', message='Introduzca un valor.',parent=self)

    def RegistrarSeccion(self):
        if self.ValidarCeldaSeccion():
            self.query = 'INSERT INTO seccion VALUES (NUll,?,"Activo")'
            self.parametros = (self.entrySeccion.get())
            if self.conexion(self.query,(self.parametros,)):
                self.MostrarDatosSeccion()
                self.LimpiarCeldaSeccion()
                messagebox.showinfo(title='Info', message='Sección Registrado.',parent=self)
            else:
                messagebox.showwarning(title='Warning', message='Sección ya esta registrada.',parent=self)
        else:
            messagebox.showwarning(title='Warning', message='Introduzca un valor.',parent=self)

    def RegistrarLaboratorio(self):
        if self.ValidarCeldaLaboratorio():
            self.query = 'INSERT INTO laboratorio VALUES (NUll,?,"Activo")'
            self.parametros = (self.entryLaboratorio.get())
            if self.conexion(self.query,(self.parametros,)):
                self.MostrarDatosLaboratorio()
                self.LimpiarCeldaLaboratorio()
                messagebox.showinfo(title='Info', message='Laboratorio Registrado.',parent=self)
            else:
                messagebox.showwarning(title='Warning', message='Laboratorio ya esta registrado.',parent=self)
        else:
            messagebox.showwarning(title='Warning', message='Introduzca un valor.',parent=self)

    def editarCohorte(self):
        if self.ValidarCeldaCohorte() and self.treeCohorte.selection():
            if messagebox.askyesno('Edit','¿Desea editar el Cohorte selecionado?',parent=self):
                self.query = 'UPDATE cohorte SET Cohorte = ? WHERE cohorte.id = ? and cohorte.Estado = "Activo"'
                self.parametros = (self.entryCohorte.get())
                self.id = self.selecionarFilaCohorte()
                self.conexion(self.query,(self.parametros, self.id))
                self.MostrarDatosCohorte()
                self.LimpiarCeldaCohorte()
                messagebox.showinfo(title='Info', message='Cohorte Editado Correctamente.',parent=self)
            else:
                self.MostrarDatosCohorte()
                self.LimpiarCeldaCohorte()
        else:
            messagebox.showwarning(title='Warning', message='Introduzca un valor y seleccione el cohorte a editar.',parent=self)

    def editarLapsoAcademico(self):
        if self.ValidarCeldaLapsoAcademico() and self.treeLapsoAcademico.selection():
            if messagebox.askyesno('Edit','¿Desea editar el lapso académico selecionado?',parent=self):
                self.query = 'UPDATE lapso_academico SET LapsoAcademico = ? WHERE lapso_academico.id = ? and lapso_academico.Estado = "Activo"'
                self.parametros = (self.entryLapsoAcademico.get())
                self.id = self.selecionarFilaLapsoAcademico()
                self.conexion(self.query,(self.parametros, self.id))
                self.MostrarDatosLapsoAcademico()
                self.LimpiarCeldaLapsoAcademico()
                messagebox.showinfo(title='Info', message='Cohorte Editado Correctamente.',parent=self)
            else:
                self.MostrarDatosLapsoAcademico()
                self.LimpiarCeldaLapsoAcademico()
        else:
            messagebox.showwarning(title='Warning', message='Introduzca un valor y seleccione el cohorte a editar.',parent=self)

    def editarTrayecto(self):
        if self.ValidarCeldaTrayecto() and self.treeTrayecto.selection():
            if messagebox.askyesno('Edit','¿Desea editar el trayecto selecionado?',parent=self):
                self.query = 'UPDATE trayecto SET Trayecto = ? WHERE trayecto.id = ? and trayecto.Estado = "Activo"'
                self.parametros = (self.entryTrayecto.get())
                self.id = self.selecionarFilaTrayecto()
                self.conexion(self.query,(self.parametros, self.id))
                self.MostrarDatosTrayecto()
                self.LimpiarCeldaTrayecto()
                messagebox.showinfo(title='Info', message='Trayecto Editado Correctamente.',parent=self)
            else:
                self.MostrarDatosTrayecto()
                self.LimpiarCeldaTrayecto()
        else:
            messagebox.showwarning(title='Warning', message='Introduzca un valor y seleccione el trayecto a editar.',parent=self)

    def editarTrimestre(self):
        if self.ValidarCeldaTrimestre() and self.treeTrimestre.selection():
            if messagebox.askyesno('Edit','¿Desea editar el trimestre selecionado?',parent=self):
                self.query = 'UPDATE trimestre SET Trimestre = ? WHERE trimestre.id = ? and trimestre.Estado = "Activo"'
                self.parametros = (self.entryTrimestre.get())
                self.id = self.selecionarFilaTrimestre()
                self.conexion(self.query,(self.parametros, self.id))
                self.MostrarDatosTrimestre()
                self.LimpiarCeldaTrimestre()
                messagebox.showinfo(title='Info', message='Trimestre Editado Correctamente.',parent=self)
            else:
                self.MostrarDatosTrimestre()
                self.LimpiarCeldaTrimestre()
        else:
            messagebox.showwarning(title='Warning', message='Introduzca un valor y el trimestre a editar.',parent=self)

    def editarSeccion(self):
        if self.ValidarCeldaSeccion() and self.treeSeccion.selection():
            if messagebox.askyesno('Edit','¿Desea editar la sección selecionada?',parent=self):
                self.query = 'UPDATE seccion SET Seccion = ? WHERE seccion.id = ? and seccion.Estado = "Activo"'
                self.parametros = (self.entrySeccion.get())
                self.id = self.selecionarFilaSeccion()
                self.conexion(self.query,(self.parametros, self.id))
                self.MostrarDatosSeccion()
                self.LimpiarCeldaSeccion()
                messagebox.showinfo(title='Info', message='Sección Editado Correctamente.',parent=self)
            else:
                self.MostrarDatosSeccion()
                self.LimpiarCeldaSeccion()
        else:
            messagebox.showwarning(title='Warning', message='Introduzca un valor y seleccione la sección a editar.',parent=self)

    def editarLaboratorio(self):
        if self.ValidarCeldaLaboratorio() and self.treeLaboratorio.selection():
            if messagebox.askyesno('Edit','¿Desea editar el laboratorio selecionado?',parent=self):
                self.query = 'UPDATE laboratorio SET Laboratorio = ? WHERE laboratorio.id = ? and laboratorio.Estado = "Activo"'
                self.parametros = (self.entryLaboratorio.get())
                self.id = self.selecionarFilaLaboratorio()
                self.conexion(self.query,(self.parametros, self.id))
                self.MostrarDatosLaboratorio()
                self.LimpiarCeldaLaboratorio()
                messagebox.showinfo(title='Info', message='Laboratorio Editado Correctamente.',parent=self)
            else:
                self.MostrarDatosLaboratorio()
                self.LimpiarCeldaLaboratorio()
        else:
            messagebox.showwarning(title='Warning', message='Introduzca un valor y seleccione el laboratorio a editar.',parent=self)