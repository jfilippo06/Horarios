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
        self.chosee = tk.StringVar()
        ttk.Radiobutton(self.frameChoose, text='Cohorte', value='Cohorte',variable=self.chosee, command=self.mostrarCohorte).grid(row=0,column=0)
        ttk.Radiobutton(self.frameChoose, text='Lapso académico', value='Lapso académico',variable=self.chosee, command=self.mostrarLapsoAcademico).grid(row=0,column=1)
        ttk.Radiobutton(self.frameChoose, text='Trayecto', value='Trayecto',variable=self.chosee, command=self.mostrarTrayecto).grid(row=0,column=2)
        ttk.Radiobutton(self.frameChoose, text='Trimestre', value='Trimestre',variable=self.chosee, command=self.mostrarTrimestre).grid(row=0,column=3)
        ttk.Radiobutton(self.frameChoose, text='Sección', value='Sección',variable=self.chosee, command=self.mostrarSeccion).grid(row=0,column=4)
        ttk.Radiobutton(self.frameChoose, text='Laboratorio', value='Laboratorio',variable=self.chosee, command=self.mostrarLaboratorio).grid(row=0,column=5)
        
        self.tree = ttk.Treeview(self.noteDatos,columns = ['#1','#2'], show='headings')
        self.tree.grid(column=0,row=1, sticky='nsew',padx=5,pady=5)
        self.scrollbar = ttk.Scrollbar(self.noteDatos, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=self.scrollbar.set)
        self.scrollbar.grid(column=1,row=1, sticky='ns')
        ttk.Button(self.noteDatos,text='HABILITAR',command=self.habilitarDatosBasicos, width=75).grid(row=2,column=0)

        self.frameChoose2 = ttk.Frame(self.noteCarga)
        self.frameChoose2.grid(row=0,column=0)
        self.chosee2 = tk.StringVar()
        ttk.Radiobutton(self.frameChoose2, text='Docente', value='Docente',variable=self.chosee2, command=self.mostrarDocentes).grid(row=0,column=0)
        ttk.Radiobutton(self.frameChoose2, text='Materias asignadas', value='Materias asignadas',variable=self.chosee2, command=self.mostrarMateriasAsignadas).grid(row=0,column=1)

        self.tree2 = ttk.Treeview(self.noteCarga,columns = ['#1','#2'], show='headings')
        self.tree2.grid(column=0,row=1, sticky='nsew',padx=5,pady=5)
        self.scrollbar2 = ttk.Scrollbar(self.noteCarga, orient=tk.VERTICAL, command=self.tree2.yview)
        self.tree2.configure(yscroll=self.scrollbar2.set)
        self.scrollbar2.grid(column=1,row=1, sticky='ns')
        ttk.Button(self.noteCarga,text='HABILITAR',command=self.habilitarCarga, width=75).grid(row=2,column=0)

        self.frameChoose3 = ttk.Frame(self.noteUnidades)
        self.frameChoose3.grid(row=0,column=0)
        self.chosee3 = tk.StringVar()
        ttk.Radiobutton(self.frameChoose3, text='Unidades curriculares', value='Unidades curriculares',variable=self.chosee3, command=self.mostrarMaterias).grid(row=0,column=0)
        ttk.Radiobutton(self.frameChoose3, text='Departamento', value='Departamento',variable=self.chosee3, command=self.mostrarDepartamento).grid(row=0,column=1)
        ttk.Radiobutton(self.frameChoose3, text='Pt', value='Pt',variable=self.chosee3, command=self.mostrarPt).grid(row=0,column=2)

        self.tree3 = ttk.Treeview(self.noteUnidades,columns = ['#1','#2'], show='headings')
        self.tree3.grid(column=0,row=1, sticky='nsew',padx=5,pady=5)
        self.scrollbar3 = ttk.Scrollbar(self.noteUnidades, orient=tk.VERTICAL, command=self.tree3.yview)
        self.tree3.configure(yscroll=self.scrollbar3.set)
        self.scrollbar3.grid(column=1,row=1, sticky='ns')
        ttk.Button(self.noteUnidades,text='HABILITAR',command=self.habilitarUnidades, width=75).grid(row=2,column=0)

        self.frameChoose4 = ttk.Frame(self.noteUsuarios)
        self.frameChoose4.grid(row=0,column=0)
        self.chosee4 = tk.StringVar()
        ttk.Radiobutton(self.frameChoose4, text='Usuarios', value='Usuarios',variable=self.chosee4, command=self.mostrarUsuarios).grid(row=0,column=0)
        
        self.tree4 = ttk.Treeview(self.noteUsuarios,columns = ['#1','#2'], show='headings')
        self.tree4.grid(column=0,row=1, sticky='nsew',padx=5,pady=5)
        self.scrollbar4 = ttk.Scrollbar(self.noteUsuarios, orient=tk.VERTICAL, command=self.tree4.yview)
        self.tree4.configure(yscroll=self.scrollbar4.set)
        self.scrollbar4.grid(column=1,row=1, sticky='ns')
        ttk.Button(self.noteUsuarios,text='HABILITAR',command=self.habilitarUsuarios, width=75).grid(row=2,column=0)

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

    def TraerDatos(self,query):
        self.mostrar = self.conexion(query)
        self.rows = self.mostrar.fetchall()
        return self.rows

    def selecionarFila(self):
        self.item = self.tree.focus()
        self.data = self.tree.item(self.item)
        self.id = self.data['values'][0]
        return self.id

    def selecionarFila2(self):
        self.item = self.tree2.focus()
        self.data = self.tree2.item(self.item)
        self.id = self.data['values'][0]
        return self.id
        
    def selecionarFila3(self):
        self.item = self.tree3.focus()
        self.data = self.tree3.item(self.item)
        self.id = self.data['values'][0]
        return self.id

    def selecionarFila4(self):
        self.item = self.tree4.focus()
        self.data = self.tree4.item(self.item)
        self.id = self.data['values'][0]
        return self.id

    def volver(self):
        self.destroy()

    def limpiarTabla(self,tabla):
        self.DeleteChildren = tabla.get_children()
        for element in self.DeleteChildren:
            tabla.delete(element)

    def mostrarCohorte(self):
        self.tree.heading('#1', text = 'Id')
        self.tree.heading('#2', text = 'Cohorte')
        self.limpiarTabla(self.tree)
        self.rows = self.TraerDatos("SELECT * FROM cohorte WHERE cohorte.Estado = 'Inactivo'")
        for row in self.rows:
            self.tree.insert('',tk.END,values=row)

    def mostrarLapsoAcademico(self):
        self.tree.heading('#1', text = 'Id')
        self.tree.heading('#2', text = 'Lapso Académico')
        self.limpiarTabla(self.tree)
        self.rows = self.TraerDatos("SELECT * FROM lapso_academico WHERE lapso_academico.Estado = 'Inactivo'")
        for row in self.rows:
            self.tree.insert('',tk.END,values=row)

    def mostrarTrayecto(self):
        self.tree.heading('#1', text = 'Id')
        self.tree.heading('#2', text = 'Trayecto')
        self.limpiarTabla(self.tree)
        self.rows = self.TraerDatos("SELECT * FROM trayecto WHERE trayecto.Estado = 'Inactivo'")
        for row in self.rows:
            self.tree.insert('',tk.END,values=row)

    def mostrarTrimestre(self):
        self.tree.heading('#1', text = 'Id')
        self.tree.heading('#2', text = 'Triyecto')
        self.limpiarTabla(self.tree)
        self.rows = self.TraerDatos("SELECT * FROM trimestre WHERE trimestre.Estado = 'Inactivo'")
        for row in self.rows:
            self.tree.insert('',tk.END,values=row)

    def mostrarSeccion(self):
        self.tree.heading('#1', text = 'Id')
        self.tree.heading('#2', text = 'Sección')
        self.limpiarTabla(self.tree)
        self.rows = self.TraerDatos("SELECT * FROM seccion WHERE seccion.Estado = 'Inactivo'")
        for row in self.rows:
            self.tree.insert('',tk.END,values=row)

    def mostrarLaboratorio(self):
        self.tree.heading('#1', text = 'Id')
        self.tree.heading('#2', text = 'Laboratorio')
        self.limpiarTabla(self.tree)
        self.rows = self.TraerDatos("SELECT * FROM laboratorio WHERE laboratorio.Estado = 'Inactivo'")
        for row in self.rows:
            self.tree.insert('',tk.END,values=row)

    def mostrarDocentes(self):
        self.tree2.heading('#1', text = 'Id')
        self.tree2.heading('#2', text = 'Docentes')
        self.limpiarTabla(self.tree2)
        self.rows = self.TraerDatos("SELECT Id,NombreApellido FROM docente WHERE docente.Estado = 'Inactivo'")
        for row in self.rows:
            self.tree2.insert('',tk.END,values=row)

    def mostrarMateriasAsignadas(self):
        self.tree2.heading('#1', text = 'Id')
        self.tree2.heading('#2', text = 'Materias Asignadas')
        self.limpiarTabla(self.tree2)

    def mostrarMaterias(self):
        self.tree3.heading('#1', text = 'Id')
        self.tree3.heading('#2', text = 'Materias')
        self.limpiarTabla(self.tree3)
        self.rows = self.TraerDatos("SELECT Id,UnidadCurricular FROM unidad_curricular WHERE unidad_curricular.Estado = 'Inactivo' ORDER BY UnidadCurricular")
        for row in self.rows:
            self.tree3.insert('',tk.END,values=row)

    def mostrarDepartamento(self):
        self.tree3.heading('#1', text = 'Id')
        self.tree3.heading('#2', text = 'Departamento')
        self.limpiarTabla(self.tree3)
        self.rows = self.TraerDatos("SELECT * FROM departamento WHERE departamento.Estado = 'Inactivo'")
        for row in self.rows:
            self.tree3.insert('',tk.END,values=row)

    def mostrarPt(self):
        self.tree3.heading('#1', text = 'Id')
        self.tree3.heading('#2', text = 'Pt')
        self.limpiarTabla(self.tree3)
        self.rows = self.TraerDatos("SELECT * FROM pt WHERE pt.Estado = 'Inactivo'")
        for row in self.rows:
            self.tree3.insert('',tk.END,values=row)

    def mostrarUsuarios(self):
        self.tree4.heading('#1', text = 'Id')
        self.tree4.heading('#2', text = 'Usuarios')
        self.limpiarTabla(self.tree4)
        self.rows = self.TraerDatos("SELECT Id, Usuario FROM usuario_admin WHERE usuario_admin.Estado = 'Inactivo'")
        for row in self.rows:
            self.tree4.insert('',tk.END,values=row)


    def habilitarDatosBasicos(self):
        if self.chosee.get() == 'Cohorte' and self.tree.selection():
            if messagebox.askyesno('Habilitar','¿Desea habilitar el cohorte?'):
                self.conexion('UPDATE cohorte SET Estado = "Activo" WHERE cohorte.id = ? and cohorte.Estado = "Inactivo"',(self.selecionarFila(),))
                self.mostrarCohorte()
                messagebox.showinfo(title='Info', message='Cohorte habilitado.')
        elif self.chosee.get() == 'Lapso académico' and self.tree.selection():
            if messagebox.askyesno('Habilitar','¿Desea habilitar el lapso académico?'):
                self.conexion('UPDATE lapso_academico SET Estado = "Activo" WHERE lapso_academico.id = ? and lapso_academico.Estado = "Inactivo"',(self.selecionarFila(),))
                self.mostrarLapsoAcademico()
                messagebox.showinfo(title='Info', message='Lapso académico habilitado.')
        elif self.chosee.get() == 'Trayecto' and self.tree.selection():
            if messagebox.askyesno('Habilitar','¿Desea habilitar el trayecto?'):
                self.conexion('UPDATE trayecto SET Estado = "Activo" WHERE trayecto.id = ? and trayecto.Estado = "Inactivo"',(self.selecionarFila(),))
                self.mostrarTrayecto()
                messagebox.showinfo(title='Info', message='Trayecto habilitado.')
        elif self.chosee.get() == 'Trimestre' and self.tree.selection():
            if messagebox.askyesno('Habilitar','¿Desea habilitar el trimestre?'):
                self.conexion('UPDATE trimestre SET Estado = "Activo" WHERE trimestre.id = ? and trimestre.Estado = "Inactivo"',(self.selecionarFila(),))
                self.mostrarTrimestre()
                messagebox.showinfo(title='Info', message='Trimestre habilitado.')
        elif self.chosee.get() == 'Sección' and self.tree.selection():
            if messagebox.askyesno('Habilitar','¿Desea habilitar la sección?'):
                self.conexion('UPDATE seccion SET Estado = "Activo" WHERE seccion.id = ? and seccion.Estado = "Inactivo"',(self.selecionarFila(),))
                self.mostrarSeccion()
                messagebox.showinfo(title='Info', message='Sección habilitada.')
        elif self.chosee.get() == 'Laboratorio' and self.tree.selection():
            if messagebox.askyesno('Habilitar','¿Desea habilitar el laboratorio?'):
                self.conexion('UPDATE laboratorio SET Estado = "Activo" WHERE laboratorio.id = ? and laboratorio.Estado = "Inactivo"',(self.selecionarFila(),))
                self.mostrarLaboratorio()
                messagebox.showinfo(title='Info', message='Laboratorio habilitado.')
        else:
            messagebox.showwarning(title='Wanning', message='Seleccione una celda.')

    def habilitarCarga(self):
        if self.chosee2.get() == 'Docente' and self.tree2.selection():
            if messagebox.askyesno('Habilitar','¿Desea habilitar al docente?'):
                self.conexion('UPDATE docente SET Estado = "Activo" WHERE docente.Id = ? AND docente.Estado = "Inactivo"',(self.selecionarFila2(),))
                self.conexion('UPDATE materias_asignadas SET Estado = "Activo" WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Estado = "Inactivo"',(self.selecionarFila2(),))
                self.conexion('UPDATE materias_docentes SET Estado = "Activo" WHERE materias_docentes.Id_docente = ? AND materias_docentes.Estado = "Inactivo"',(self.selecionarFila2(),))
                self.conexion('UPDATE materias_laboratorios SET Estado = "Activo" WHERE materias_laboratorios.Id_docente = ? AND materias_laboratorios.Estado = "Inactivo"',(self.selecionarFila2(),))
                self.mostrarDocentes()
                messagebox.showinfo(title='Info', message='Docente y todos sus registros habilitados')
        elif self.chosee2.get() == 'Materias asignadas' and self.tree2.selection():
            pass
        else:
            messagebox.showwarning(title='Wanning', message='Seleccione una celda.')

    def habilitarUnidades(self):
        if self.chosee3.get() == 'Unidades curriculares' and self.tree3.selection():
            if messagebox.askyesno('Habilitar','¿Desea habilitar la unidad curricular?'):
                self.conexion('UPDATE unidad_curricular SET Estado = "Activo" WHERE unidad_curricular.id = ? and unidad_curricular.Estado = "Inactivo"',(self.selecionarFila3(),))
                self.mostrarMaterias()
                messagebox.showinfo(title='Info', message='Unidad curricular habilitada')
        elif self.chosee3.get() == 'Departamento' and self.tree3.selection():
            if messagebox.askyesno('Habilitar','¿Desea habilitar el departamento?'):
                self.conexion('UPDATE departamento SET Estado = "Activo" WHERE departamento.Id = ? and departamento.Estado = "Inactivo"',(self.selecionarFila3(),))
                self.mostrarDepartamento()
                messagebox.showinfo(title='Info', message='Departamento habilitado')
        elif self.chosee3.get() == 'Pt' and self.tree3.selection():
            if messagebox.askyesno('Habilitar','¿Desea habilitar el pt?'):
                self.conexion('UPDATE pt SET Estado = "Activo" WHERE pt.Id = ? and pt.Estado = "Inactivo"',(self.selecionarFila3(),))
                self.mostrarPt()
                messagebox.showinfo(title='Info', message='Pt habilitado')
        else:
            messagebox.showwarning(title='Wanning', message='Seleccione una celda.')
        
    def habilitarUsuarios(self):
        if self.chosee4.get() == 'Usuarios' and self.tree4.selection():
            if messagebox.askyesno('Habilitar','¿Desea habilitar el usuario?'):
                self.conexion('UPDATE usuario_admin SET Estado = "Activo" WHERE usuario_admin.Id = ? and usuario_admin.Estado = "Inactivo"',(self.selecionarFila4(),))
                self.mostrarUsuarios()
                messagebox.showinfo(title='Info', message='Usuarios habilitado')
        else:
            messagebox.showwarning(title='Wanning', message='Seleccione una celda.')