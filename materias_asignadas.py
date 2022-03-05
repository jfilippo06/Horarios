import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3
from rutas import *
import traceback
import sys

class Materias_asignadas(tk.Toplevel):
    def __init__(self,master = None):
        super().__init__(master)
        # Config:
        self.title('Materias asignadas')
        self.geometry('1280x290')
        self.resizable(width=0,height=0)
        self.iconbitmap(uptpc)
        self.frame = ttk.Labelframe(self)
        self.frame.grid(column=0,row=1,pady=5,padx=5)
        self.tree = ttk.Treeview(self.frame, columns = ['#1','#2','#3','#4','#5','#6','#7','#8','#9','#10','#11','#12'], show='headings',height=9)
        self.tree.grid(row=0,column=0)
        self.tree.heading('#1', text = 'Id',)
        self.tree.heading('#2', text = 'Nombre y Apellido')
        self.tree.heading('#3', text = 'Lapso Académico')
        self.tree.heading('#4', text = 'Cohorte')
        self.tree.heading('#5', text = 'Trayecto')
        self.tree.heading('#6', text = 'Trimestre')
        self.tree.heading('#7', text = 'Sección')
        self.tree.heading('#8', text = 'Turno')
        self.tree.heading('#9', text = 'Día')
        self.tree.heading('#10', text = 'Hora Inicial')
        self.tree.heading('#11', text = 'Hora Final')
        self.tree.heading('#12', text = 'Unidad Curricular')
        self.tree.column('#1', width=40)
        self.tree.column('#2', width=120)
        self.tree.column('#3', width=120)
        self.tree.column('#4', width=100)
        self.tree.column('#5', width=80)
        self.tree.column('#6', width=80)
        self.tree.column('#7', width=80)
        self.tree.column('#8', width=80)
        self.tree.column('#9', width=80)
        self.tree.column('#10', width=100)
        self.tree.column('#11', width=100)
        self.tree.column('#12', width=250)
        self.scrollbar = ttk.Scrollbar(self.frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=self.scrollbar.set)
        self.scrollbar.grid(column=1,row=0, sticky='ns')
        ttk.Button(self,text='HABILITAR MATERIA',command=self.habilitarMateria, width=205).grid(row=2,column=0)
        ttk.Button(self,text='CANCELAR',command=self.volver, width=205).grid(row=3,column=0)

        self.mostrarMateriasAsignadas()

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

    def limpiarTabla(self,tabla):
        self.DeleteChildren = tabla.get_children()
        for element in self.DeleteChildren:
            tabla.delete(element)

    def mostrarMateriasAsignadas(self):
        self.limpiarTabla(self.tree)
        self.rows = self.TraerDatos("SELECT materias_asignadas.Id ,docente.NombreApellido, lapso_academico.LapsoAcademico, cohorte.Cohorte, trayecto.Trayecto, trimestre.Trimestre, seccion.Seccion, modalidad.Turno,semana.Dia, hora_inicial.Hora, hora_final.Hora, unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN docente ON  docente.Id = materias_asignadas.Id_docente INNER JOIN lapso_academico ON  lapso_academico.Id = materias_asignadas.Id_lapso_academico INNER JOIN cohorte ON  cohorte.Id = materias_asignadas.Id_cohorte INNER JOIN trayecto ON trayecto.Id = materias_asignadas.Id_trayecto INNER JOIN trimestre ON trimestre.Id = materias_asignadas.Id_trimestre INNER JOIN seccion ON seccion.Id = materias_asignadas.Id_seccion INNER JOIN modalidad ON modalidad.Id = materias_asignadas.Id_modalidad INNER JOIN semana ON semana.Id = materias_asignadas.Id_semana INNER JOIN hora_inicial ON hora_inicial.Id = materias_asignadas.Id_hora_inicial INNER JOIN hora_final ON hora_final.Id = materias_asignadas.Id_hora_final INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Estado = 'Inactivo'")
        for row in self.rows:
            self.tree.insert('',tk.END,values=row)

    def habilitarMateria(self):
        if self.tree.selection():
            if messagebox.askyesno('Habilitar','¿Desea habilitar la materia?',parent=self):
                self.conexion('UPDATE materias_asignadas SET Estado = "Activo" WHERE materias_asignadas.Id = ? AND materias_asignadas.Estado = "Inactivo"',(self.selecionarFila(),))
                self.conexion('UPDATE materias_docentes SET Estado = "Activo" WHERE materias_docentes.Id_materias_asignadas = ? AND materias_docentes.Estado = "Inactivo"',(self.selecionarFila(),))
                self.conexion('UPDATE materias_laboratorios SET Estado = "Activo" WHERE materias_laboratorios.Id_materias_asignadas = ? AND materias_laboratorios.Estado = "Inactivo"',(self.selecionarFila(),))
                self.mostrarMateriasAsignadas()
                messagebox.showinfo(title='Info', message='Materia habilitada',parent=self)
        else:
            messagebox.showwarning(title='Wanning', message='Seleccione una celda.',parent=self)