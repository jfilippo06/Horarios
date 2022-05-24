import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import sqlite3
from tkinter.constants import DISABLED, NORMAL
from rutas import *
import traceback
import sys
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER

class Horarios(tk.Toplevel):
    def __init__(self,master):
        super().__init__(master)
        # Config:
        self.title('Horarios')
        self.geometry('980x490')
        self.resizable(width=0, height=0)
        self.iconbitmap(uptpc)

        self.menubar = tk.Menu(self)
        self.menubar.add_cascade(label="Configuración", command=self.configuracion)
        self.menubar.add_cascade(label="Volver", command=self.volver)
        self.config(menu=self.menubar)

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(pady=0,padx=0,expand=True)

        # create frames
        self.noteHorariosClases = ttk.Frame(self.notebook, width=980, height=480)
        self.noteHorariosDocentes = ttk.Frame(self.notebook,width=980, height=480)
        self.noteHorariosLaboratorios = ttk.Frame(self.notebook,width=980, height=480)

        # create frames
        self.noteHorariosClases.pack(fill='both', expand=True)
        self.noteHorariosDocentes.pack(fill='both', expand=True)
        self.noteHorariosLaboratorios.pack(fill='both', expand=True)

        # add frames to notebook
        self.notebook.add(self.noteHorariosClases, text='Horarios de clases')
        self.notebook.add(self.noteHorariosDocentes, text='Horarios de docentes')
        self.notebook.add(self.noteHorariosLaboratorios, text='Horarios de laboratorios')

        ttk.Label(self.noteHorariosClases, text='GENERAR HORARIO DE CLASES',font=('Helvetica',14)).place(x=350,y=5)
        # LapsoAcademico
        self.container = ttk.Labelframe(self.noteHorariosClases)
        self.container.grid(column=0,row=0,ipadx=10,ipady=15,padx=30,pady=10)

        self.frameLapsoAcademico = ttk.Labelframe(self.container)
        self.frameLapsoAcademico.grid(column=0,row=0,pady=5,padx=5)
        self.treeLapsoAcademico = ttk.Treeview(self.frameLapsoAcademico, columns=['#1',"#2"],show='headings',height=2)
        self.treeLapsoAcademico.grid(row=0,column=0)
        self.treeLapsoAcademico.heading('#1', text = 'Id',)
        self.treeLapsoAcademico.heading('#2', text = 'Lapso Académico')
        self.treeLapsoAcademico.column('#1', width=50)
        self.treeLapsoAcademico.column('#2', width=120)
        self.scrollbarLapsoAcademico = ttk.Scrollbar(self.frameLapsoAcademico, orient=tk.VERTICAL, command=self.treeLapsoAcademico.yview)
        self.treeLapsoAcademico.configure(yscroll=self.scrollbarLapsoAcademico.set)
        self.scrollbarLapsoAcademico.grid(column=1,row=0, sticky='ns')
        # Modalidad
        self.frameModalidad = ttk.Labelframe(self.container)
        self.frameModalidad.grid(column=1,row=0,pady=5,padx=5)
        self.treeModalidad = ttk.Treeview(self.frameModalidad, columns=['#1',"#2"],show='headings',height=2)
        self.treeModalidad.grid(row=0,column=0)
        self.treeModalidad.heading('#1', text = 'Id',)
        self.treeModalidad.heading('#2', text = 'Modalidad')
        self.treeModalidad.column('#1', width=50)
        self.treeModalidad.column('#2', width=120)
        self.scrollbarModalidad = ttk.Scrollbar(self.frameModalidad, orient=tk.VERTICAL, command=self.treeModalidad.yview)
        self.treeModalidad.configure(yscroll=self.scrollbarModalidad.set)
        self.scrollbarModalidad.grid(column=1,row=0, sticky='ns')
        # Cohorte
        self.frameCohorte = ttk.Labelframe(self.container)
        self.frameCohorte.grid(column=0,row=1,pady=5,padx=5)
        self.treeCohorte = ttk.Treeview(self.frameCohorte, columns=['#1',"#2"],show='headings',height=2)
        self.treeCohorte.grid(row=0,column=0)
        self.treeCohorte.heading('#1', text = 'Id',)
        self.treeCohorte.heading('#2', text = 'Cohorte')
        self.treeCohorte.column('#1', width=50)
        self.treeCohorte.column('#2', width=120)
        self.scrollbarCohorte = ttk.Scrollbar(self.frameCohorte, orient=tk.VERTICAL, command=self.treeCohorte.yview)
        self.treeCohorte.configure(yscroll=self.scrollbarCohorte.set)
        self.scrollbarCohorte.grid(column=1,row=0, sticky='ns')
        # Trayecto
        self.frameTrayecto = ttk.Labelframe(self.container)
        self.frameTrayecto.grid(column=1,row=1,pady=5,padx=5)
        self.treeTrayecto = ttk.Treeview(self.frameTrayecto, columns=['#1',"#2"],show='headings',height=2)
        self.treeTrayecto.grid(row=0,column=0)
        self.treeTrayecto.heading('#1', text = 'Id',)
        self.treeTrayecto.heading('#2', text = 'Trayecto')
        self.treeTrayecto.column('#1', width=50)
        self.treeTrayecto.column('#2', width=120)
        self.scrollbarTrayecto = ttk.Scrollbar(self.frameTrayecto, orient=tk.VERTICAL, command=self.treeTrayecto.yview)
        self.treeTrayecto.configure(yscroll=self.scrollbarTrayecto.set)
        self.scrollbarTrayecto.grid(column=1,row=0, sticky='ns')
        # Trimestre
        self.frameTrimestre = ttk.Labelframe(self.container)
        self.frameTrimestre.grid(column=0,row=2,pady=5,padx=5)
        self.treeTrimestre = ttk.Treeview(self.frameTrimestre, columns=['#1',"#2"],show='headings',height=2)
        self.treeTrimestre.grid(row=0,column=0)
        self.treeTrimestre.heading('#1', text = 'Id',)
        self.treeTrimestre.heading('#2', text = 'Trimestre')
        self.treeTrimestre.column('#1', width=50)
        self.treeTrimestre.column('#2', width=120)
        self.scrollbarTrimestre = ttk.Scrollbar(self.frameTrimestre, orient=tk.VERTICAL, command=self.treeTrimestre.yview)
        self.treeTrimestre.configure(yscroll=self.scrollbarTrimestre.set)
        self.scrollbarTrimestre.grid(column=1,row=0, sticky='ns')
        # Seccion
        self.frameSeccion = ttk.Labelframe(self.container)
        self.frameSeccion.grid(column=1,row=2,pady=5,padx=5)
        self.treeSeccion = ttk.Treeview(self.frameSeccion, columns=['#1',"#2"],show='headings',height=2)
        self.treeSeccion.grid(row=0,column=0)
        self.treeSeccion.heading('#1', text = 'Id',)
        self.treeSeccion.heading('#2', text = 'Sección')
        self.treeSeccion.column('#1', width=50)
        self.treeSeccion.column('#2', width=120)
        self.scrollbarSeccion = ttk.Scrollbar(self.frameSeccion, orient=tk.VERTICAL, command=self.treeSeccion.yview)
        self.treeSeccion.configure(yscroll=self.scrollbarSeccion.set)
        self.scrollbarSeccion.grid(column=1,row=0, sticky='ns')

        ttk.Button(self.container, text='GENERAR HORARIO DE CLASES',command=self.generarHorarioClases).grid(column=0,row=3,pady=5,padx=5, sticky = tk.W + tk.E)

        self.frameContenedor = ttk.Labelframe(self.noteHorariosClases)
        self.frameContenedor.grid(column=1, row=0,ipadx=5,ipady=5,pady=30,padx=10)

        ttk.Label(self.frameContenedor, text='Inicio clase').grid(column=0, row=0,pady=5,padx=5)
        self.entryInicio = ttk.Entry(self.frameContenedor, state=DISABLED)
        self.entryInicio.grid(column=1,row=0,pady=5,padx=5)
        self.activarInicio = ttk.Button(self.frameContenedor, text='ACTIVAR', command=self.botonActivarInicio).grid(column=2,row=0)
        self.desactivarInicio = ttk.Button(self.frameContenedor, text='DESACTIVAR', command=self.botonDesactivarInicio).grid(column=3,row=0)

        ttk.Label(self.frameContenedor, text='Inicio pausa vacacional').grid(column=0, row=1,pady=5,padx=5)
        self.entryPausa = ttk.Entry(self.frameContenedor, state=DISABLED)
        self.entryPausa.grid(column=1,row=1,pady=5,padx=5)
        self.activarPausa = ttk.Button(self.frameContenedor, text='ACTIVAR', command=self.botonActivarPausa).grid(column=2,row=1)
        self.desactivarPausa = ttk.Button(self.frameContenedor, text='DESACTIVAR', command=self.botonDesactivarPausa).grid(column=3,row=1)

        ttk.Label(self.frameContenedor, text='Reinicio clase').grid(column=0, row=2,pady=5,padx=5)
        self.entryReinicio = ttk.Entry(self.frameContenedor, state=DISABLED)
        self.entryReinicio.grid(column=1,row=2,pady=5,padx=5)
        self.activarReinicio = ttk.Button(self.frameContenedor, text='ACTIVAR', command=self.botonActivarReinicio).grid(column=2,row=2)
        self.desactivarReinicio = ttk.Button(self.frameContenedor, text='DESACTIVAR', command=self.botonDesactivarReinicio).grid(column=3,row=2)

        ttk.Label(self.frameContenedor, text='Culminación clase').grid(column=0, row=3,pady=5,padx=5)
        self.entryCulminacion = ttk.Entry(self.frameContenedor, state=DISABLED)
        self.entryCulminacion.grid(column=1,row=3,pady=5,padx=5)
        self.activarCulminacion = ttk.Button(self.frameContenedor, text='ACTIVAR', command=self.botonActivarCuminacion).grid(column=2,row=3)
        self.desactivarCulminacion = ttk.Button(self.frameContenedor, text='DESACTIVAR', command=self.botonDesactivarCulminacion).grid(column=3,row=3)

        ttk.Label(self.frameContenedor, text='Aula').grid(column=0, row=4,pady=5,padx=5)
        self.entryAula = ttk.Entry(self.frameContenedor, state=DISABLED)
        self.entryAula.grid(column=1,row=4,pady=5,padx=5)
        self.activarAula = ttk.Button(self.frameContenedor, text='ACTIVAR', command=self.botonActivarAula).grid(column=2,row=4)
        self.desactivarAula = ttk.Button(self.frameContenedor, text='DESACTIVAR', command=self.botonDesactivarAula).grid(column=3,row=4)

        ttk.Label(self.frameContenedor, text='Nota').grid(column=0, row=5,pady=5,padx=5)
        self.entryNota = ttk.Entry(self.frameContenedor, state=DISABLED)
        self.entryNota.grid(column=1,row=5,pady=5,padx=5)
        self.activarNota = ttk.Button(self.frameContenedor, text='ACTIVAR', command=self.botonActivarNota).grid(column=2,row=5)
        self.desactivarNota = ttk.Button(self.frameContenedor, text='DESACTIVAR', command=self.botonDesactivarNota).grid(column=3,row=5)

        ttk.Label(self.frameContenedor, text='Lunes').grid(column=0, row=6,pady=5,padx=5)
        self.entryLunes = ttk.Entry(self.frameContenedor, state=DISABLED)
        self.entryLunes.grid(column=1,row=6,pady=5,padx=5)
        self.activarLunes = ttk.Button(self.frameContenedor, text='ACTIVAR', command=self.botonActivarLunes).grid(column=2,row=6)
        self.desactivarLunes = ttk.Button(self.frameContenedor, text='DESACTIVAR', command=self.botonDesactivarLunes).grid(column=3,row=6)

        ttk.Label(self.frameContenedor, text='Martes').grid(column=0, row=7,pady=7,padx=5)
        self.entryMartes = ttk.Entry(self.frameContenedor, state=DISABLED)
        self.entryMartes.grid(column=1,row=7,pady=5,padx=5)
        self.activarMartes = ttk.Button(self.frameContenedor, text='ACTIVAR', command=self.botonActivarMartes).grid(column=2,row=7)
        self.desactivarMartes = ttk.Button(self.frameContenedor, text='DESACTIVAR', command=self.botonDesactivarMartes).grid(column=3,row=7)

        ttk.Label(self.frameContenedor, text='Miércoles').grid(column=0, row=8,pady=5,padx=5)
        self.entryMiercoles = ttk.Entry(self.frameContenedor, state=DISABLED)
        self.entryMiercoles.grid(column=1,row=8,pady=5,padx=5)
        self.activarMiercoles = ttk.Button(self.frameContenedor, text='ACTIVAR', command=self.botonActivarMiercoles).grid(column=2,row=8)
        self.desactivarMiercoles = ttk.Button(self.frameContenedor, text='DESACTIVAR', command=self.botonDesactivarMiercoles).grid(column=3,row=8)

        ttk.Label(self.frameContenedor, text='Jueves').grid(column=0, row=9,pady=5,padx=5)
        self.entryJueves = ttk.Entry(self.frameContenedor, state=DISABLED)
        self.entryJueves.grid(column=1,row=9,pady=5,padx=5)
        self.activarJueves = ttk.Button(self.frameContenedor, text='ACTIVAR', command=self.botonActivarJueves).grid(column=2,row=9)
        self.desactivarJueves = ttk.Button(self.frameContenedor, text='DESACTIVAR', command=self.botonDesactivarJueves).grid(column=3,row=9)

        ttk.Label(self.frameContenedor, text='Viernes').grid(column=0, row=10,pady=5,padx=5)
        self.entryViernes = ttk.Entry(self.frameContenedor, state=DISABLED)
        self.entryViernes.grid(column=1,row=10,pady=5,padx=5)
        self.activarViernes = ttk.Button(self.frameContenedor, text='ACTIVAR', command=self.botonActivarViernes).grid(column=2,row=10)
        self.desactivarViernes = ttk.Button(self.frameContenedor, text='DESACTIVAR', command=self.botonDesactivarViernes).grid(column=3,row=10)

        self.container2 = ttk.Labelframe(self.noteHorariosDocentes)
        self.container2.grid(column=0,row=0,ipadx=10,ipady=20,padx=30,pady=30)
        
        ttk.Label(self.noteHorariosDocentes, text='GENERAR HORARIO DE DOCENTES',font=('Helvetica',14)).place(x=350,y=5)
        
        self.frameDocente = ttk.Labelframe(self.container2)
        self.frameDocente.grid(column=0,row=0,pady=5,padx=5)
        self.treeDocente = ttk.Treeview(self.frameDocente, columns=['#1',"#2"],show='headings',height=6)
        self.treeDocente.grid(row=0,column=0)
        self.treeDocente.heading('#1', text = 'Id',)
        self.treeDocente.heading('#2', text = 'Docente')
        self.treeDocente.column('#1', width=50)
        self.treeDocente.column('#2', width=120)
        self.scrollbarDocente = ttk.Scrollbar(self.frameDocente, orient=tk.VERTICAL, command=self.treeDocente.yview)
        self.treeDocente.configure(yscroll=self.scrollbarDocente.set)
        self.scrollbarDocente.grid(column=1,row=0, sticky='ns')
        
        self.frameDocenteLapsoAcademico = ttk.Labelframe(self.container2)
        self.frameDocenteLapsoAcademico.grid(column=1,row=0,pady=5,padx=5)
        self.treeDocenteLapsoAcademico = ttk.Treeview(self.frameDocenteLapsoAcademico, columns=['#1',"#2"],show='headings',height=6)
        self.treeDocenteLapsoAcademico.grid(row=0,column=0)
        self.treeDocenteLapsoAcademico.heading('#1', text = 'Id',)
        self.treeDocenteLapsoAcademico.heading('#2', text = 'Lapso Académico')
        self.treeDocenteLapsoAcademico.column('#1', width=50)
        self.treeDocenteLapsoAcademico.column('#2', width=120)
        self.scrollbarDocenteLapsoAcademico = ttk.Scrollbar(self.frameDocenteLapsoAcademico, orient=tk.VERTICAL, command=self.treeDocenteLapsoAcademico.yview)
        self.treeDocenteLapsoAcademico.configure(yscroll=self.scrollbarDocenteLapsoAcademico.set)
        self.scrollbarDocenteLapsoAcademico.grid(column=1,row=0, sticky='ns')
        
        self.frameDocenteModalidad = ttk.Labelframe(self.container2)
        self.frameDocenteModalidad.grid(column=0,row=1,pady=5,padx=5)
        self.treeDocenteModalidad = ttk.Treeview(self.frameDocenteModalidad, columns=['#1',"#2"],show='headings',height=2)
        self.treeDocenteModalidad.grid(row=0,column=0)
        self.treeDocenteModalidad.heading('#1', text = 'Id',)
        self.treeDocenteModalidad.heading('#2', text = 'Modalidad')
        self.treeDocenteModalidad.column('#1', width=50)
        self.treeDocenteModalidad.column('#2', width=120)
        self.scrollbarDocenteModalidad = ttk.Scrollbar(self.frameDocenteModalidad, orient=tk.VERTICAL, command=self.treeDocenteModalidad.yview)
        self.treeDocenteModalidad.configure(yscroll=self.scrollbarDocenteModalidad.set)
        self.scrollbarDocenteModalidad.grid(column=1,row=0, sticky='ns')
        
        ttk.Button(self.container2, text='GENERAR HORARIO DOCENTE',command=self.generarHorariosDocentes,width=30).grid(column=0,row=2,padx=5,pady=5)
        
        self.frameContenedor2 = ttk.Labelframe(self.noteHorariosDocentes)
        self.frameContenedor2.grid(column=1, row=0,ipadx=5,ipady=5,pady=30,padx=10)

        ttk.Label(self.frameContenedor2, text='Inicio clase').grid(column=0, row=0,pady=5,padx=5)
        self.entryInicio2 = ttk.Entry(self.frameContenedor2, state=DISABLED)
        self.entryInicio2.grid(column=1,row=0,pady=5,padx=5)
        self.activarInicio2 = ttk.Button(self.frameContenedor2, text='ACTIVAR', command=self.botonActivarInicio2).grid(column=2,row=0)
        self.desactivarInicio2 = ttk.Button(self.frameContenedor2, text='DESACTIVAR', command=self.botonDesactivarInicio2).grid(column=3,row=0)
        
        ttk.Label(self.frameContenedor2, text='Inicio pausa vacacional').grid(column=0, row=1,pady=5,padx=5)
        self.entryPausa2 = ttk.Entry(self.frameContenedor2, state=DISABLED)
        self.entryPausa2.grid(column=1,row=1,pady=5,padx=5)
        self.activarPausa2 = ttk.Button(self.frameContenedor2, text='ACTIVAR', command=self.botonActivarPausa2).grid(column=2,row=1)
        self.desactivarPausa2 = ttk.Button(self.frameContenedor2, text='DESACTIVAR', command=self.botonDesactivarPausa2).grid(column=3,row=1)

        ttk.Label(self.frameContenedor2, text='Reinicio clase').grid(column=0, row=2,pady=5,padx=5)
        self.entryReinicio2 = ttk.Entry(self.frameContenedor2, state=DISABLED)
        self.entryReinicio2.grid(column=1,row=2,pady=5,padx=5)
        self.activarReinicio2 = ttk.Button(self.frameContenedor2, text='ACTIVAR', command=self.botonActivarReinicio2).grid(column=2,row=2)
        self.desactivarReinicio2 = ttk.Button(self.frameContenedor2, text='DESACTIVAR', command=self.botonDesactivarReinicio2).grid(column=3,row=2)

        ttk.Label(self.frameContenedor2, text='Culminación clase').grid(column=0, row=3,pady=5,padx=5)
        self.entryCulminacion2 = ttk.Entry(self.frameContenedor2, state=DISABLED)
        self.entryCulminacion2.grid(column=1,row=3,pady=5,padx=5)
        self.activarCulminacion2 = ttk.Button(self.frameContenedor2, text='ACTIVAR', command=self.botonActivarCuminacion2).grid(column=2,row=3)
        self.desactivarCulminacion2 = ttk.Button(self.frameContenedor2, text='DESACTIVAR', command=self.botonDesactivarCulminacion2).grid(column=3,row=3)

        ttk.Label(self.frameContenedor2, text='Aula').grid(column=0, row=4,pady=5,padx=5)
        self.entryAula2 = ttk.Entry(self.frameContenedor2, state=DISABLED)
        self.entryAula2.grid(column=1,row=4,pady=5,padx=5)
        self.activarAula2 = ttk.Button(self.frameContenedor2, text='ACTIVAR', command=self.botonActivarAula2).grid(column=2,row=4)
        self.desactivarAula2 = ttk.Button(self.frameContenedor2, text='DESACTIVAR', command=self.botonDesactivarAula2).grid(column=3,row=4)

        ttk.Label(self.frameContenedor2, text='Nota').grid(column=0, row=5,pady=5,padx=5)
        self.entryNota2 = ttk.Entry(self.frameContenedor2, state=DISABLED)
        self.entryNota2.grid(column=1,row=5,pady=5,padx=5)
        self.activarNota2 = ttk.Button(self.frameContenedor2, text='ACTIVAR', command=self.botonActivarNota2).grid(column=2,row=5)
        self.desactivarNota2 = ttk.Button(self.frameContenedor2, text='DESACTIVAR', command=self.botonDesactivarNota2).grid(column=3,row=5)

        ttk.Label(self.frameContenedor2, text='Lunes').grid(column=0, row=6,pady=5,padx=5)
        self.entryLunes2 = ttk.Entry(self.frameContenedor2, state=DISABLED)
        self.entryLunes2.grid(column=1,row=6,pady=5,padx=5)
        self.activarLunes2 = ttk.Button(self.frameContenedor2, text='ACTIVAR', command=self.botonActivarLunes2).grid(column=2,row=6)
        self.desactivarLunes2 = ttk.Button(self.frameContenedor2, text='DESACTIVAR', command=self.botonDesactivarLunes2).grid(column=3,row=6)

        ttk.Label(self.frameContenedor2, text='Martes').grid(column=0, row=7,pady=7,padx=5)
        self.entryMartes2 = ttk.Entry(self.frameContenedor2, state=DISABLED)
        self.entryMartes2.grid(column=1,row=7,pady=5,padx=5)
        self.activarMartes2 = ttk.Button(self.frameContenedor2, text='ACTIVAR', command=self.botonActivarMartes2).grid(column=2,row=7)
        self.desactivarMartes2 = ttk.Button(self.frameContenedor2, text='DESACTIVAR', command=self.botonDesactivarMartes2).grid(column=3,row=7)

        ttk.Label(self.frameContenedor2, text='Miércoles').grid(column=0, row=8,pady=5,padx=5)
        self.entryMiercoles2 = ttk.Entry(self.frameContenedor2, state=DISABLED)
        self.entryMiercoles2.grid(column=1,row=8,pady=5,padx=5)
        self.activarMiercoles2 = ttk.Button(self.frameContenedor2, text='ACTIVAR', command=self.botonActivarMiercoles2).grid(column=2,row=8)
        self.desactivarMiercoles2 = ttk.Button(self.frameContenedor2, text='DESACTIVAR', command=self.botonDesactivarMiercoles2).grid(column=3,row=8)

        ttk.Label(self.frameContenedor2, text='Jueves').grid(column=0, row=9,pady=5,padx=5)
        self.entryJueves2 = ttk.Entry(self.frameContenedor2, state=DISABLED)
        self.entryJueves2.grid(column=1,row=9,pady=5,padx=5)
        self.activarJueves2 = ttk.Button(self.frameContenedor2, text='ACTIVAR', command=self.botonActivarJueves2).grid(column=2,row=9)
        self.desactivarJueves2 = ttk.Button(self.frameContenedor2, text='DESACTIVAR', command=self.botonDesactivarJueves2).grid(column=3,row=9)

        ttk.Label(self.frameContenedor2, text='Viernes').grid(column=0, row=10,pady=5,padx=5)
        self.entryViernes2 = ttk.Entry(self.frameContenedor2, state=DISABLED)
        self.entryViernes2.grid(column=1,row=10,pady=5,padx=5)
        self.activarViernes2 = ttk.Button(self.frameContenedor2, text='ACTIVAR', command=self.botonActivarViernes2).grid(column=2,row=10)
        self.desactivarViernes2 = ttk.Button(self.frameContenedor2, text='DESACTIVAR', command=self.botonDesactivarViernes2).grid(column=3,row=10)

        self.container3 = ttk.Labelframe(self.noteHorariosLaboratorios)
        self.container3.grid(column=0,row=0,ipadx=10,ipady=20,padx=30,pady=10)
        
        ttk.Label(self.noteHorariosLaboratorios, text='GENERAR HORARIO DE LABORATORIOS',font=('Helvetica',14)).place(x=325,y=5)

        self.frameLaboratorio = ttk.Labelframe(self.container3)
        self.frameLaboratorio.grid(column=0,row=0,pady=5,padx=5)
        self.treeLaboratorio = ttk.Treeview(self.frameLaboratorio, columns=['#1',"#2"],show='headings',height=6)
        self.treeLaboratorio.grid(row=0,column=0)
        self.treeLaboratorio.heading('#1', text = 'Id',)
        self.treeLaboratorio.heading('#2', text = 'Laboratorio')
        self.treeLaboratorio.column('#1', width=50)
        self.treeLaboratorio.column('#2', width=120)
        self.scrollbarLaboratorio = ttk.Scrollbar(self.frameLaboratorio, orient=tk.VERTICAL, command=self.treeLaboratorio.yview)
        self.treeLaboratorio.configure(yscroll=self.scrollbarLaboratorio.set)
        self.scrollbarLaboratorio.grid(column=1,row=0, sticky='ns')
        
        self.frameLaboratorioLapso = ttk.Labelframe(self.container3)
        self.frameLaboratorioLapso.grid(column=1,row=0,pady=5,padx=5)
        self.treeLaboratorioLapso = ttk.Treeview(self.frameLaboratorioLapso, columns=['#1',"#2"],show='headings',height=6)
        self.treeLaboratorioLapso.grid(row=0,column=0)
        self.treeLaboratorioLapso.heading('#1', text = 'Id',)
        self.treeLaboratorioLapso.heading('#2', text = 'Lapso Académico')
        self.treeLaboratorioLapso.column('#1', width=50)
        self.treeLaboratorioLapso.column('#2', width=120)
        self.scrollbarLaboratorioLapso = ttk.Scrollbar(self.frameLaboratorioLapso, orient=tk.VERTICAL, command=self.treeLaboratorioLapso.yview)
        self.treeLaboratorioLapso.configure(yscroll=self.scrollbarLaboratorioLapso.set)
        self.scrollbarLaboratorioLapso.grid(column=1,row=0, sticky='ns')

        self.frameLaboratorioModalidad = ttk.Labelframe(self.container3)
        self.frameLaboratorioModalidad.grid(column=0,row=2,pady=5,padx=5)
        self.treeLaboratorioModalidad = ttk.Treeview(self.frameLaboratorioModalidad, columns=['#1',"#2"],show='headings',height=2)
        self.treeLaboratorioModalidad.grid(row=0,column=0)
        self.treeLaboratorioModalidad.heading('#1', text = 'Id',)
        self.treeLaboratorioModalidad.heading('#2', text = 'Modalidad')
        self.treeLaboratorioModalidad.column('#1', width=50)
        self.treeLaboratorioModalidad.column('#2', width=120)
        self.scrollbarLaboratorioModalidad = ttk.Scrollbar(self.frameLaboratorioModalidad, orient=tk.VERTICAL, command=self.treeLaboratorioModalidad.yview)
        self.treeLaboratorioModalidad.configure(yscroll=self.scrollbarLaboratorioModalidad.set)
        self.scrollbarLaboratorioModalidad.grid(column=1,row=0, sticky='ns')

        ttk.Button(self.container3, text='GENERAR HORARIO LABORATORIO',command=self.generarHorariosLaboratorio,width=32).grid(column=0,row=3,padx=5,pady=5)
        
        self.frameContenedor3 = ttk.Labelframe(self.noteHorariosLaboratorios)
        self.frameContenedor3.grid(column=1, row=0,ipadx=5,ipady=5,pady=30,padx=10)

        ttk.Label(self.frameContenedor3, text='Inicio clase').grid(column=0, row=0,pady=5,padx=5)
        self.entryInicio3 = ttk.Entry(self.frameContenedor3, state=DISABLED)
        self.entryInicio3.grid(column=1,row=0,pady=5,padx=5)
        self.activarInicio3 = ttk.Button(self.frameContenedor3, text='ACTIVAR', command=self.botonActivarInicio3).grid(column=2,row=0)
        self.desactivarInicio3 = ttk.Button(self.frameContenedor3, text='DESACTIVAR', command=self.botonDesactivarInicio3).grid(column=3,row=0)
        
        ttk.Label(self.frameContenedor3, text='Inicio pausa vacacional').grid(column=0, row=1,pady=5,padx=5)
        self.entryPausa3 = ttk.Entry(self.frameContenedor3, state=DISABLED)
        self.entryPausa3.grid(column=1,row=1,pady=5,padx=5)
        self.activarPausa3 = ttk.Button(self.frameContenedor3, text='ACTIVAR', command=self.botonActivarPausa3).grid(column=2,row=1)
        self.desactivarPausa3 = ttk.Button(self.frameContenedor3, text='DESACTIVAR', command=self.botonDesactivarPausa3).grid(column=3,row=1)

        ttk.Label(self.frameContenedor3, text='Reinicio clase').grid(column=0, row=2,pady=5,padx=5)
        self.entryReinicio3 = ttk.Entry(self.frameContenedor3, state=DISABLED)
        self.entryReinicio3.grid(column=1,row=2,pady=5,padx=5)
        self.activarReinicio3 = ttk.Button(self.frameContenedor3, text='ACTIVAR', command=self.botonActivarReinicio3).grid(column=2,row=2)
        self.desactivarReinicio3 = ttk.Button(self.frameContenedor3, text='DESACTIVAR', command=self.botonDesactivarReinicio3).grid(column=3,row=2)

        ttk.Label(self.frameContenedor3, text='Culminación clase').grid(column=0, row=3,pady=5,padx=5)
        self.entryCulminacion3 = ttk.Entry(self.frameContenedor3, state=DISABLED)
        self.entryCulminacion3.grid(column=1,row=3,pady=5,padx=5)
        self.activarCulminacion3 = ttk.Button(self.frameContenedor3, text='ACTIVAR', command=self.botonActivarCuminacion3).grid(column=2,row=3)
        self.desactivarCulminacion3 = ttk.Button(self.frameContenedor3, text='DESACTIVAR', command=self.botonDesactivarCulminacion3).grid(column=3,row=3)

        ttk.Label(self.frameContenedor3, text='Aula').grid(column=0, row=4,pady=5,padx=5)
        self.entryAula3 = ttk.Entry(self.frameContenedor3, state=DISABLED)
        self.entryAula3.grid(column=1,row=4,pady=5,padx=5)
        self.activarAula3 = ttk.Button(self.frameContenedor3, text='ACTIVAR', command=self.botonActivarAula3).grid(column=2,row=4)
        self.desactivarAula3 = ttk.Button(self.frameContenedor3, text='DESACTIVAR', command=self.botonDesactivarAula3).grid(column=3,row=4)

        ttk.Label(self.frameContenedor3, text='Nota').grid(column=0, row=5,pady=5,padx=5)
        self.entryNota3 = ttk.Entry(self.frameContenedor3, state=DISABLED)
        self.entryNota3.grid(column=1,row=5,pady=5,padx=5)
        self.activarNota3 = ttk.Button(self.frameContenedor3, text='ACTIVAR', command=self.botonActivarNota3).grid(column=2,row=5)
        self.desactivarNota3 = ttk.Button(self.frameContenedor3, text='DESACTIVAR', command=self.botonDesactivarNota3).grid(column=3,row=5)

        ttk.Label(self.frameContenedor3, text='Lunes').grid(column=0, row=6,pady=5,padx=5)
        self.entryLunes3 = ttk.Entry(self.frameContenedor3, state=DISABLED)
        self.entryLunes3.grid(column=1,row=6,pady=5,padx=5)
        self.activarLunes3 = ttk.Button(self.frameContenedor3, text='ACTIVAR', command=self.botonActivarLunes3).grid(column=2,row=6)
        self.desactivarLunes3 = ttk.Button(self.frameContenedor3, text='DESACTIVAR', command=self.botonDesactivarLunes3).grid(column=3,row=6)

        ttk.Label(self.frameContenedor3, text='Martes').grid(column=0, row=7,pady=7,padx=5)
        self.entryMartes3 = ttk.Entry(self.frameContenedor3, state=DISABLED)
        self.entryMartes3.grid(column=1,row=7,pady=5,padx=5)
        self.activarMartes3 = ttk.Button(self.frameContenedor3, text='ACTIVAR', command=self.botonActivarMartes3).grid(column=2,row=7)
        self.desactivarMartes3 = ttk.Button(self.frameContenedor3, text='DESACTIVAR', command=self.botonDesactivarMartes3).grid(column=3,row=7)

        ttk.Label(self.frameContenedor3, text='Miércoles').grid(column=0, row=8,pady=5,padx=5)
        self.entryMiercoles3 = ttk.Entry(self.frameContenedor3, state=DISABLED)
        self.entryMiercoles3.grid(column=1,row=8,pady=5,padx=5)
        self.activarMiercoles3 = ttk.Button(self.frameContenedor3, text='ACTIVAR', command=self.botonActivarMiercoles3).grid(column=2,row=8)
        self.desactivarMiercoles3 = ttk.Button(self.frameContenedor3, text='DESACTIVAR', command=self.botonDesactivarMiercoles3).grid(column=3,row=8)

        ttk.Label(self.frameContenedor3, text='Jueves').grid(column=0, row=9,pady=5,padx=5)
        self.entryJueves3 = ttk.Entry(self.frameContenedor3, state=DISABLED)
        self.entryJueves3.grid(column=1,row=9,pady=5,padx=5)
        self.activarJueves3 = ttk.Button(self.frameContenedor3, text='ACTIVAR', command=self.botonActivarJueves3).grid(column=2,row=9)
        self.desactivarJueves3 = ttk.Button(self.frameContenedor3, text='DESACTIVAR', command=self.botonDesactivarJueves3).grid(column=3,row=9)

        ttk.Label(self.frameContenedor3, text='Viernes').grid(column=0, row=10,pady=5,padx=5)
        self.entryViernes3 = ttk.Entry(self.frameContenedor3, state=DISABLED)
        self.entryViernes3.grid(column=1,row=10,pady=5,padx=5)
        self.activarViernes3 = ttk.Button(self.frameContenedor3, text='ACTIVAR', command=self.botonActivarViernes3).grid(column=2,row=10)
        self.desactivarViernes3 = ttk.Button(self.frameContenedor3, text='DESACTIVAR', command=self.botonDesactivarViernes3).grid(column=3,row=10)

        self.MostrarLapsoAcademico()
        self.MostrarModalidad()
        self.MostrarCohorte()
        self.MostrarTrayecto()
        self.MostrarTrimestre()
        self.MostrarSeccion()
        self.MostrarDocente()
        self.MostrarDocenteLapsoAcademico()
        self.MostrarDocenteModalidad()
        self.MostrarLaboratorioLapsoAcademico()
        self.MostrarLaboratorioModalidad()
        self.MostrarLaboratorio()

        self.width, self.heigth = A4
        self.styles = getSampleStyleSheet()
        self.center = self.styles["BodyText"]
        self.center.alignment = TA_CENTER
        self.counter = 0
        self.counterLaboratorio = 0

        self.setStyles = [
            ('GRID',(0,0),(-1,-1),0.5,colors.black),
            ('BBOX',(0,0),(-1,-1),0.5,colors.black),
            ('ALIGN',(0,0),(-1,-1),'CENTER'),
            ('VALIGN',(0,0),(-1,-1),'MIDDLE')
        ]

        self.setStylesCeldas = [
            ('GRID',(0,0),(-1,-1),0.5,colors.black),
            ('BBOX',(0,0),(-1,-1),0.5,colors.black),
            ('ALIGN',(0,0),(-1,-1),'CENTER'),
            ('VALIGN',(0,0),(-1,-1),'MIDDLE')
        ]
        
        self.celdaDiurno = [
            [Paragraph('N°',self.center)],
            [Paragraph('1',self.center)],
            [Paragraph('2',self.center)],
            [Paragraph('3',self.center)],
            [Paragraph('4',self.center)],
            [Paragraph('5',self.center)],
            [Paragraph('6',self.center)],
            [Paragraph('1',self.center)],
            [Paragraph('2',self.center)],
            [Paragraph('3',self.center)],
            [Paragraph('4',self.center)],
            [Paragraph('5',self.center)],
            [Paragraph('6',self.center)]
        ]

        self.celdaNocturno = [
            [Paragraph('N°',self.center)],
            [Paragraph('1',self.center)],
            [Paragraph('2',self.center)],
            [Paragraph('3',self.center)],
            [Paragraph('4',self.center)],
            [Paragraph('5',self.center)],
            [Paragraph('6',self.center)]
        ]
    
    def volver(self):
        self.destroy()

    def botonActivarInicio(self):
        self.entryInicio.config(state=NORMAL)
        self.entryInicio.focus()

    def botonDesactivarInicio(self):
        self.entryInicio.config(state=DISABLED)

    def botonActivarPausa(self):
        self.entryPausa.config(state=NORMAL)
        self.entryPausa.focus()

    def botonDesactivarPausa(self):
        self.entryPausa.config(state=DISABLED)

    def botonActivarReinicio(self):
        self.entryReinicio.config(state=NORMAL)
        self.entryReinicio.focus()

    def botonDesactivarReinicio(self):
        self.entryReinicio.config(state=DISABLED)

    def botonActivarCuminacion(self):
        self.entryCulminacion.config(state=NORMAL)
        self.entryCulminacion.focus()

    def botonDesactivarCulminacion(self):
        self.entryCulminacion.config(state=DISABLED)

    def botonActivarAula(self):
        self.entryAula.config(state=NORMAL)
        self.entryAula.focus()

    def botonDesactivarAula(self):
        self.entryAula.config(state=DISABLED)

    def botonActivarNota(self):
        self.entryNota.config(state=NORMAL)
        self.entryNota.focus()

    def botonDesactivarNota(self):
        self.entryNota.config(state=DISABLED)

    def botonActivarLunes(self):
        self.entryLunes.config(state=NORMAL)
        self.entryLunes.focus()

    def botonDesactivarLunes(self):
        self.entryLunes.config(state=DISABLED)

    def botonActivarMartes(self):
        self.entryMartes.config(state=NORMAL)
        self.entryMartes.focus()

    def botonDesactivarMartes(self):
        self.entryMartes.config(state=DISABLED)

    def botonActivarMiercoles(self):
        self.entryMiercoles.config(state=NORMAL)
        self.entryMiercoles.focus()

    def botonDesactivarMiercoles(self):
        self.entryMiercoles.config(state=DISABLED)

    def botonActivarJueves(self):
        self.entryJueves.config(state=NORMAL)
        self.entryJueves.focus()

    def botonDesactivarJueves(self):
        self.entryJueves.config(state=DISABLED)

    def botonActivarViernes(self):
        self.entryViernes.config(state=NORMAL)
        self.entryViernes.focus()

    def botonDesactivarViernes(self):
        self.entryViernes.config(state=DISABLED)
        
    # Pantalla Docente-------------------------------------
    
    def botonActivarInicio2(self):
        self.entryInicio2.config(state=NORMAL)
        self.entryInicio2.focus()

    def botonDesactivarInicio2(self):
        self.entryInicio2.config(state=DISABLED)

    def botonActivarPausa2(self):
        self.entryPausa2.config(state=NORMAL)
        self.entryPausa2.focus()

    def botonDesactivarPausa2(self):
        self.entryPausa2.config(state=DISABLED)

    def botonActivarReinicio2(self):
        self.entryReinicio2.config(state=NORMAL)
        self.entryReinicio2.focus()

    def botonDesactivarReinicio2(self):
        self.entryReinicio2.config(state=DISABLED)

    def botonActivarCuminacion2(self):
        self.entryCulminacion2.config(state=NORMAL)
        self.entryCulminacion2.focus()

    def botonDesactivarCulminacion2(self):
        self.entryCulminacion2.config(state=DISABLED)

    def botonActivarAula2(self):
        self.entryAula2.config(state=NORMAL)
        self.entryAula2.focus()

    def botonDesactivarAula2(self):
        self.entryAula2.config(state=DISABLED)

    def botonActivarNota2(self):
        self.entryNota2.config(state=NORMAL)
        self.entryNota2.focus()

    def botonDesactivarNota2(self):
        self.entryNota2.config(state=DISABLED)

    def botonActivarLunes2(self):
        self.entryLunes2.config(state=NORMAL)
        self.entryLunes2.focus()

    def botonDesactivarLunes2(self):
        self.entryLunes2.config(state=DISABLED)

    def botonActivarMartes2(self):
        self.entryMartes2.config(state=NORMAL)
        self.entryMartes2.focus()

    def botonDesactivarMartes2(self):
        self.entryMartes2.config(state=DISABLED)

    def botonActivarMiercoles2(self):
        self.entryMiercoles2.config(state=NORMAL)
        self.entryMiercoles2.focus()

    def botonDesactivarMiercoles2(self):
        self.entryMiercoles2.config(state=DISABLED)

    def botonActivarJueves2(self):
        self.entryJueves2.config(state=NORMAL)
        self.entryJueves2.focus()

    def botonDesactivarJueves2(self):
        self.entryJueves2.config(state=DISABLED)

    def botonActivarViernes2(self):
        self.entryViernes2.config(state=NORMAL)
        self.entryViernes2.focus()

    def botonDesactivarViernes2(self):
        self.entryViernes2.config(state=DISABLED)

    # Pantalla Laboratorio-----------------------------------

    def botonActivarInicio3(self):
        self.entryInicio3.config(state=NORMAL)
        self.entryInicio3.focus()

    def botonDesactivarInicio3(self):
        self.entryInicio3.config(state=DISABLED)

    def botonActivarPausa3(self):
        self.entryPausa3.config(state=NORMAL)
        self.entryPausa3.focus()

    def botonDesactivarPausa3(self):
        self.entryPausa3.config(state=DISABLED)

    def botonActivarReinicio3(self):
        self.entryReinicio3.config(state=NORMAL)
        self.entryReinicio3.focus()

    def botonDesactivarReinicio3(self):
        self.entryReinicio3.config(state=DISABLED)

    def botonActivarCuminacion3(self):
        self.entryCulminacion3.config(state=NORMAL)
        self.entryCulminacion3.focus()

    def botonDesactivarCulminacion3(self):
        self.entryCulminacion3.config(state=DISABLED)

    def botonActivarAula3(self):
        self.entryAula3.config(state=NORMAL)
        self.entryAula3.focus()

    def botonDesactivarAula3(self):
        self.entryAula3.config(state=DISABLED)

    def botonActivarNota3(self):
        self.entryNota3.config(state=NORMAL)
        self.entryNota3.focus()

    def botonDesactivarNota3(self):
        self.entryNota3.config(state=DISABLED)

    def botonActivarLunes3(self):
        self.entryLunes3.config(state=NORMAL)
        self.entryLunes3.focus()

    def botonDesactivarLunes3(self):
        self.entryLunes3.config(state=DISABLED)

    def botonActivarMartes3(self):
        self.entryMartes3.config(state=NORMAL)
        self.entryMartes3.focus()

    def botonDesactivarMartes3(self):
        self.entryMartes3.config(state=DISABLED)

    def botonActivarMiercoles3(self):
        self.entryMiercoles3.config(state=NORMAL)
        self.entryMiercoles3.focus()

    def botonDesactivarMiercoles3(self):
        self.entryMiercoles3.config(state=DISABLED)

    def botonActivarJueves3(self):
        self.entryJueves3.config(state=NORMAL)
        self.entryJueves3.focus()

    def botonDesactivarJueves3(self):
        self.entryJueves3.config(state=DISABLED)

    def botonActivarViernes3(self):
        self.entryViernes3.config(state=NORMAL)
        self.entryViernes3.focus()

    def botonDesactivarViernes3(self):
        self.entryViernes3.config(state=DISABLED)

    def conexion(self,query,parametros = ()):
        try:
            self.con = sqlite3.connect(baseDeDatos)
            self.cursor = self.con.cursor()
            self.cursor.execute(query,parametros)
            self.con.commit()
            return self.cursor
        except IndexError:
            pass
        except TypeError:
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

    def limpiarTablaTitulo(self):
        self.DeleteChildren = self.treeTitulo.get_children()
        for element in self.DeleteChildren:
            self.treeTitulo.delete(element)

    def MostrarTitulo(self):
        self.limpiarTablaTitulo()
        self.rows = self.TraerDatos("SELECT * FROM titulo")
        for row in self.rows:
            self.treeTitulo.insert('',tk.END,values=row)

    def MostrarLapsoAcademico(self):
        self.rows = self.TraerDatos("SELECT * FROM lapso_academico WHERE lapso_academico.Estado = 'Activo'")
        for row in self.rows:
            self.treeLapsoAcademico.insert('',tk.END,values=row)

    def MostrarModalidad(self):
        self.rows = self.TraerDatos("SELECT * FROM modalidad WHERE modalidad.Estado = 'Activo'")
        for row in self.rows:
            self.treeModalidad.insert('',tk.END,values=row)
            
    def MostrarCohorte(self):
        self.rows = self.TraerDatos("SELECT * FROM cohorte WHERE cohorte.Estado = 'Activo'")
        for row in self.rows:
            self.treeCohorte.insert('',tk.END,values=row)
            
    def MostrarTrayecto(self):
        self.rows = self.TraerDatos("SELECT * FROM trayecto WHERE trayecto.Estado = 'Activo'")
        for row in self.rows:
            self.treeTrayecto.insert('',tk.END,values=row)
            
    def MostrarTrimestre(self):
        self.rows = self.TraerDatos("SELECT * FROM trimestre WHERE trimestre.Estado = 'Activo'")
        for row in self.rows:
            self.treeTrimestre.insert('',tk.END,values=row)
            
    def MostrarSeccion(self):
        self.rows = self.TraerDatos("SELECT * FROM seccion WHERE seccion.Estado = 'Activo'")
        for row in self.rows:
            self.treeSeccion.insert('',tk.END,values=row)
            
    def MostrarDocente(self):
        self.rows = self.TraerDatos("SELECT Id, NombreApellido FROM docente WHERE docente.Estado = 'Activo'")
        for row in self.rows:
            self.treeDocente.insert('',tk.END,values=row)
            
    def MostrarDocenteLapsoAcademico(self):
        self.rows = self.TraerDatos("SELECT * FROM lapso_academico WHERE lapso_academico.Estado = 'Activo'")
        for row in self.rows:
            self.treeDocenteLapsoAcademico.insert('',tk.END,values=row)

    def MostrarDocenteModalidad(self):
        self.rows = self.TraerDatos("SELECT * FROM modalidad WHERE modalidad.Estado = 'Activo'")
        for row in self.rows:
            self.treeDocenteModalidad.insert('',tk.END,values=row)

    def MostrarLaboratorio(self):
        self.rows = self.TraerDatos("SELECT * FROM laboratorio WHERE laboratorio.Estado = 'Activo'")
        for row in self.rows:
            self.treeLaboratorio.insert('',tk.END,values=row)

    def MostrarLaboratorioLapsoAcademico(self):
        self.rows = self.TraerDatos("SELECT * FROM lapso_academico WHERE lapso_academico.Estado = 'Activo'")
        for row in self.rows:
            self.treeLaboratorioLapso.insert('',tk.END,values=row)

    def MostrarLaboratorioModalidad(self):
        self.rows = self.TraerDatos("SELECT * FROM modalidad WHERE modalidad.Estado = 'Activo'")
        for row in self.rows:
            self.treeLaboratorioModalidad.insert('',tk.END,values=row)
            
    def selecionarFilaLapsoAcademico(self):
        self.item = self.treeLapsoAcademico.focus()
        self.data = self.treeLapsoAcademico.item(self.item)
        self.id = self.data['values'][0]
        return self.id
        
    def selecionarFilaModalidad(self):
        self.item = self.treeModalidad.focus()
        self.data = self.treeModalidad.item(self.item)
        self.id = self.data['values'][0]
        return self.id
        
    def selecionarFilaCohorte(self):
        self.item = self.treeCohorte.focus()
        self.data = self.treeCohorte.item(self.item)
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
    
    def selecionarFilaDocente(self):
        self.item = self.treeDocente.focus()
        self.data = self.treeDocente.item(self.item)
        self.id = self.data['values'][0]
        return self.id
    
    def selecionarFilaDocenteLapsoAcademico(self):
        self.item = self.treeDocenteLapsoAcademico.focus()
        self.data = self.treeDocenteLapsoAcademico.item(self.item)
        self.id = self.data['values'][0]
        return self.id
        
    def selecionarFilaDocenteModalidad(self):
        self.item = self.treeDocenteModalidad.focus()
        self.data = self.treeDocenteModalidad.item(self.item)
        self.id = self.data['values'][0]
        return self.id

    def selecionarFilaLaboratorio(self):
        self.item = self.treeLaboratorio.focus()
        self.data = self.treeLaboratorio.item(self.item)
        self.id = self.data['values'][0]
        return self.id

    def selecionarFilaLaboratorioLapso(self):
        self.item = self.treeLaboratorioLapso.focus()
        self.data = self.treeLaboratorioLapso.item(self.item)
        self.id = self.data['values'][0]
        return self.id
        
    def selecionarFilaLaboratorioModalidad(self):
        self.item = self.treeLaboratorioModalidad.focus()
        self.data = self.treeLaboratorioModalidad.item(self.item)
        self.id = self.data['values'][0]
        return self.id

    def LapsoAcademico(self):
        self.item = self.treeLapsoAcademico.focus()
        self.data = self.treeLapsoAcademico.item(self.item)
        self.id = self.data['values'][1]
        return self.id
        
    def Modalidad(self):
        self.item = self.treeModalidad.focus()
        self.data = self.treeModalidad.item(self.item)
        self.id = self.data['values'][1]
        return self.id
        
    def Cohorte(self):
        self.item = self.treeCohorte.focus()
        self.data = self.treeCohorte.item(self.item)
        self.id = self.data['values'][1]
        return self.id
        
    def Trayecto(self):
        self.item = self.treeTrayecto.focus()
        self.data = self.treeTrayecto.item(self.item)
        self.id = self.data['values'][1]
        return self.id
        
    def Trimestre(self):
        self.item = self.treeTrimestre.focus()
        self.data = self.treeTrimestre.item(self.item)
        self.id = self.data['values'][1]
        return self.id
        
    def Seccion(self):
        self.item = self.treeSeccion.focus()
        self.data = self.treeSeccion.item(self.item)
        self.id = self.data['values'][1]
        return self.id
    
    def Docente(self):
        self.item = self.treeDocente.focus()
        self.data = self.treeDocente.item(self.item)
        self.id = self.data['values'][1]
        return self.id
    
    def DocenteLapsoAcademico(self):
        self.item = self.treeDocenteLapsoAcademico.focus()
        self.data = self.treeDocenteLapsoAcademico.item(self.item)
        self.id = self.data['values'][1]
        return self.id
        
    def DocenteModalidad(self):
        self.item = self.treeDocenteModalidad.focus()
        self.data = self.treeDocenteModalidad.item(self.item)
        self.id = self.data['values'][1]
        return self.id

    def Laboratorio(self):
        self.item = self.treeLaboratorio.focus()
        self.data = self.treeLaboratorio.item(self.item)
        self.id = self.data['values'][1]
        return self.id

    def LaboratorioLapso(self):
        self.item = self.treeLaboratorioLapso.focus()
        self.data = self.treeLaboratorioLapso.item(self.item)
        self.id = self.data['values'][1]
        return self.id
        
    def LaboratorioModalidad(self):
        self.item = self.treeLaboratorioModalidad.focus()
        self.data = self.treeLaboratorioModalidad.item(self.item)
        self.id = self.data['values'][1]
        return self.id

    def generarHorarioClases(self):
        if self.treeLapsoAcademico.selection() and self.treeModalidad.selection() and self.treeCohorte.selection() and self.treeTrayecto.selection() and self.treeTrimestre.selection() and self.treeSeccion.selection():
            self.selecionarLaspoId = self.selecionarFilaLapsoAcademico()
            self.selecionarModalidadId = self.selecionarFilaModalidad()
            self.selecionarCohorteId = self.selecionarFilaCohorte()
            self.selecionarTrayectoId = self.selecionarFilaTrayecto()
            self.selecionarTrimestreId = self.selecionarFilaTrimestre()
            self.selecionarSeccionId = self.selecionarFilaSeccion()
            self.parametros = (self.selecionarLaspoId, self.selecionarModalidadId, self.selecionarCohorteId, self.selecionarTrayectoId, self.selecionarTrimestreId, self.selecionarSeccionId)
            self.lapso = str(self.LapsoAcademico())
            self.modalidad = str(self.Modalidad())
            self.cohorte = str(self.Cohorte())
            self.trayecto = str(self.Trayecto())
            self.trimestre = str(self.Trimestre())
            self.seccion = str(self.Seccion())

            self.guardar = filedialog.asksaveasfilename(initialdir= "/", title="Select file", defaultextension=".*",filetypes=(("PDF files","*.pdf"),("all files","*.*")),parent=self)
            self.archivo = open(self.guardar,'w')
            self.pdf = canvas.Canvas(self.guardar, pagesize = landscape(A4))
            self.pdf.setFontSize(10)
            self.pdf.drawString(301,550, self.obtenerTitulo() + '  Lapso Académico ' + self.lapso + ' (Cohorte' + self.cohorte + ')')
            self.pdf.line(299,549,605,549)
            self.pdf.drawString(388,529,'TRAYECTO ' + self.trayecto + ' TRIMESTRE ' + self.trimestre)
            self.verificarLinea()
            self.pdf.drawString(425,504, 'SECCIÓN: ' + self.seccion)
            self.pdf.drawImage(logoPDF,680,485,width=100,height=100)
            self.validarTree()
            self.validarCelda()
            self.validarModalidad()        
            self.tablaDocente()
            
            self.pdf.save()
            self.archivo.close()
            self.setStyles.clear()
            self.setStyles.append(('GRID',(0,0),(-1,-1),0.5,colors.black))
            self.setStyles.append(('BBOX',(0,0),(-1,-1),0.5,colors.black))
            self.setStyles.append(('VALIGN',(0,0),(-1,-1),'MIDDLE'))
            self.setStyles.append(('ALIGN',(0,0),(-1,-1),'CENTER'))
            self.counter = 0
            
            messagebox.showinfo(title='Horario', message='Horario generado correctamente',parent=self)
        else:
            messagebox.showwarning(title='Error', message='Debe seleccionar todas las celdas',parent=self)
            
    def generarHorariosDocentes(self):
        if self.treeDocente.selection() and self.treeDocenteLapsoAcademico.selection() and self.treeDocenteModalidad.selection():
            self.docenteId = self.selecionarFilaDocente()
            self.lapsoAcademicoId = self.selecionarFilaDocenteLapsoAcademico()
            self.modalidadId = self.selecionarFilaDocenteModalidad()
            self.parametrosDocentes = (self.docenteId, self.lapsoAcademicoId, self.modalidadId)
            self.dataDocente = self.Docente()
            self.dataLapso = self.DocenteLapsoAcademico()
            self.dataModalidad = self.DocenteModalidad()
            
            self.guardar = filedialog.asksaveasfilename(initialdir= "/", title="Select file", defaultextension=".*",filetypes=(("PDF files","*.pdf"),("all files","*.*")),parent=self)
            self.archivo = open(self.guardar,'w')
            
            self.pdfDocente = canvas.Canvas(self.guardar, pagesize = landscape(A4))
            self.pdfDocente.setFontSize(10)
            self.pdfDocente.drawString(301,550, self.obtenerTitulo() + '  Lapso Académico ' + self.dataLapso)
            self.pdfDocente.line(299,549,530,549)
            self.pdfDocente.drawString(300,535,'Docente: ' + self.dataDocente)
            self.pdfDocente.drawString(300,525,'Modalidad: ' + self.dataModalidad)
            self.pdfDocente.drawImage(logoPDF,680,485,width=100,height=100)
            self.validarTreeDocente()
            self.validarCeldaDocente()
            self.validarModalidadDocente()        
            
            self.pdfDocente.save()
            self.archivo.close()
            self.setStyles.clear()
            self.setStyles.append(('GRID',(0,0),(-1,-1),0.5,colors.black))
            self.setStyles.append(('BBOX',(0,0),(-1,-1),0.5,colors.black))
            self.setStyles.append(('VALIGN',(0,0),(-1,-1),'MIDDLE'))
            self.setStyles.append(('ALIGN',(0,0),(-1,-1),'CENTER'))
        
            messagebox.showinfo(title='Horario', message='Horario docente generado correctamente',parent=self)
        else:
            messagebox.showwarning(title='Error', message='Debe seleccionar todas las celdas',parent=self)

    def generarHorariosLaboratorio(self):
        if self.treeLaboratorio.selection()  and self.treeLaboratorioLapso.selection() and self.treeLaboratorioModalidad.selection():
            self.laboratorioId = self.selecionarFilaLaboratorio()
            self.laboratorioLapsoId = self.selecionarFilaLaboratorioLapso()
            self.laboratorioModalidadId = self.selecionarFilaLaboratorioModalidad()
            self.parametrosLaboratorios = (self.laboratorioId,self.laboratorioLapsoId, self.laboratorioModalidadId)
            self.dataLaboratorio = self.Laboratorio()
            self.dataLaboratorioLapso = self.LaboratorioLapso()
            self.dataLaboratorioModalidad = self.LaboratorioModalidad()

            self.guardar = filedialog.asksaveasfilename(initialdir= "/", title="Select file", defaultextension=".*",filetypes=(("PDF files","*.pdf"),("all files","*.*")),parent=self)
            self.archivo = open(self.guardar,'w')

            self.pdfLaboratorio = canvas.Canvas(self.guardar, pagesize = landscape(A4))
            self.pdfLaboratorio.setFontSize(10)
            self.pdfLaboratorio.drawString(301,550, self.obtenerTitulo() + '  Lapso Académico ' + self.dataLaboratorioLapso)
            self.pdfLaboratorio.line(299,549,530,549)
            self.pdfLaboratorio.drawString(300,535,'Laboratorio: ' + self.dataLaboratorio)
            self.pdfLaboratorio.drawString(300,525,'Modalidad: ' + self.dataLaboratorioModalidad)
            self.pdfLaboratorio.drawImage(logoPDF,680,485,width=100,height=100)
            self.validarTreeLaboratorio()
            self.validarCeldaLaboratorio()
            self.validarModalidadLaboratorio() 
            self.tablaDocenteLaboratorio()    
            
            self.pdfLaboratorio.save()
            self.archivo.close()  
            self.setStyles.clear()
            self.setStyles.append(('GRID',(0,0),(-1,-1),0.5,colors.black))
            self.setStyles.append(('BBOX',(0,0),(-1,-1),0.5,colors.black))
            self.setStyles.append(('VALIGN',(0,0),(-1,-1),'MIDDLE'))
            self.setStyles.append(('ALIGN',(0,0),(-1,-1),'CENTER'))
            self.counterLaboratorio = 0

            messagebox.showinfo(title='Horario', message='Horario Laboratorio generado correctamente',parent=self)
        else:
            messagebox.showwarning(title='Error', message='Debe seleccionar todas las celdas',parent=self)     

    def verificarLinea(self):
        if self.trayecto == 'Inicial' and self.trimestre == 'Inicial':
            return self.pdf.line(386,528,563,528)
        else: 
            return self.pdf.line(386,528,522,528)
     
    def validarTree(self):
        if not self.entryInicio.state() and not self.entryPausa.state()  and not self.entryReinicio.state() and not self.entryCulminacion.state():
            self.pdf.drawString(70,537, 'Inicio clase: ' + self.entryInicio.get()) 
            self.pdf.drawString(70,527, 'Pausa vacacional: ' + self.entryPausa.get()) 
            self.pdf.drawString(70,517, 'Reinicio: ' + self.entryReinicio.get()) 
            self.pdf.drawString(70,507, 'Culminación clase: ' + self.entryCulminacion.get())
        else:
            if not self.entryInicio.state() and not self.entryCulminacion.state():
                self.pdf.drawString(70,537, 'Inicio clase: ' + self.entryInicio.get()) 
                self.pdf.drawString(70,527, 'Culminación clase: ' + self.entryCulminacion.get())
        if not self.entryAula.state():
            self.pdf.drawString(510,504, 'Aula: ' + self.entryAula.get())
        if not self.entryNota.state():
            self.pdf.drawString(70,487, 'NOTA: ' + self.entryNota.get())
            
    def validarTreeDocente(self):
        if not self.entryInicio2.state() and not self.entryPausa2.state()  and not self.entryReinicio2.state() and not self.entryCulminacion2.state():
            self.pdfDocente.drawString(70,537, 'Inicio clase: ' + self.entryInicio2.get()) 
            self.pdfDocente.drawString(70,527, 'Pausa vacacional: ' + self.entryPausa2.get()) 
            self.pdfDocente.drawString(70,517, 'Reinicio: ' + self.entryReinicio2.get()) 
            self.pdfDocente.drawString(70,507, 'Culminación clase: ' + self.entryCulminacion2.get())
        else:
            if not self.entryInicio2.state() and not self.entryCulminacion2.state():
                self.pdfDocente.drawString(70,537, 'Inicio clase: ' + self.entryInicio2.get()) 
                self.pdfDocente.drawString(70,527, 'Culminación clase: ' + self.entryCulminacion2.get())
        if not self.entryAula2.state():
            self.pdfDocente.drawString(510,504, 'Aula: ' + self.entryAula2.get())
        if not self.entryNota2.state():
            self.pdfDocente.drawString(70,487, 'NOTA: ' + self.entryNota2.get())

    def validarTreeLaboratorio(self):
        if not self.entryInicio3.state() and not self.entryPausa3.state()  and not self.entryReinicio3.state() and not self.entryCulminacion3.state():
            self.pdfLaboratorio.drawString(70,537, 'Inicio clase: ' + self.entryInicio3.get()) 
            self.pdfLaboratorio.drawString(70,527, 'Pausa vacacional: ' + self.entryPausa3.get()) 
            self.pdfLaboratorio.drawString(70,517, 'Reinicio: ' + self.entryReinicio3.get()) 
            self.pdfLaboratorio.drawString(70,507, 'Culminación clase: ' + self.entryCulminacion2.get())
        else:
            if not self.entryInicio3.state() and not self.entryCulminacion3.state():
                self.pdfLaboratorio.drawString(70,537, 'Inicio clase: ' + self.entryInicio3.get()) 
                self.pdfLaboratorio.drawString(70,527, 'Culminación clase: ' + self.entryCulminacion3.get())
        if not self.entryAula3.state():
            self.pdfLaboratorio.drawString(510,504, 'Aula: ' + self.entryAula3.get())
        if not self.entryNota3.state():
            self.pdfLaboratorio.drawString(70,487, 'NOTA: ' + self.entryNota3.get())

    def validarCelda(self):
        if self.modalidad == 'Diurno':
            self.celda = Table(self.celdaDiurno,colWidths=50, rowHeights=25)
            self.celda.setStyle(TableStyle(self.setStylesCeldas))
            self.celda.wrapOn(self.pdf,self.width,self.heigth)
            self.celda.drawOn(self.pdf,68,157)
            return self.celda
        if self.modalidad == 'Nocturno':
            self.celda = Table(self.celdaNocturno,colWidths=50, rowHeights=25)
            self.celda.setStyle(TableStyle(self.setStylesCeldas))
            self.celda.wrapOn(self.pdf,self.width,self.heigth)
            self.celda.drawOn(self.pdf,68,307)
            return self.celda
        
    def validarCeldaDocente(self):
        if self.dataModalidad == 'Diurno':
            self.celda = Table(self.celdaDiurno,colWidths=50, rowHeights=36)
            self.celda.setStyle(TableStyle(self.setStylesCeldas))
            self.celda.wrapOn(self.pdfDocente,self.width,self.heigth)
            self.celda.drawOn(self.pdfDocente,68,14)
            return self.celda
        if self.dataModalidad == 'Nocturno':
            self.celda = Table(self.celdaNocturno,colWidths=50, rowHeights=36)
            self.celda.setStyle(TableStyle(self.setStylesCeldas))
            self.celda.wrapOn(self.pdfDocente,self.width,self.heigth)
            self.celda.drawOn(self.pdfDocente,68,230)
            return self.celda

    def validarCeldaLaboratorio(self):
        if self.dataLaboratorioModalidad == 'Diurno':
            self.celda = Table(self.celdaDiurno,colWidths=50, rowHeights=25)
            self.celda.setStyle(TableStyle(self.setStylesCeldas))
            self.celda.wrapOn(self.pdfLaboratorio,self.width,self.heigth)
            self.celda.drawOn(self.pdfLaboratorio,68,157)
            return self.celda
        if self.dataLaboratorioModalidad == 'Nocturno':
            self.celda = Table(self.celdaNocturno,colWidths=50, rowHeights=25)
            self.celda.setStyle(TableStyle(self.setStylesCeldas))
            self.celda.wrapOn(self.pdfLaboratorio,self.width,self.heigth)
            self.celda.drawOn(self.pdfLaboratorio,68,307)
            return self.celda

    def validarModalidad(self):
        if self.modalidad == 'Diurno':
            self.table = Table(self.obtenerHorarioDiurno(),colWidths=110, rowHeights=25)
            self.table.setStyle(TableStyle(self.setStyles))
            self.table.wrapOn(self.pdf,self.width,self.heigth)
            self.table.drawOn(self.pdf,118,157)
            return self.table
        if self.modalidad == 'Nocturno':
            self.table = Table(self.obtenerHorarioNocturno(),colWidths=110, rowHeights=25)
            self.table.setStyle(TableStyle(self.setStyles))
            self.table.wrapOn(self.pdf,self.width,self.heigth)
            self.table.drawOn(self.pdf,118,307)
            return self.table
        
    def validarModalidadDocente(self):
        if self.dataModalidad == 'Diurno':
            self.table = Table(self.obtenerHorarioDiurnoDocente(),colWidths=110, rowHeights=36)
            self.table.setStyle(TableStyle(self.setStyles))
            self.table.wrapOn(self.pdfDocente,self.width,self.heigth)
            self.table.drawOn(self.pdfDocente,118,14)
            return self.table
        if self.dataModalidad == 'Nocturno':
            self.table = Table(self.obtenerHorarioNocturnoDocente(),colWidths=110, rowHeights=36)
            self.table.setStyle(TableStyle(self.setStyles))
            self.table.wrapOn(self.pdfDocente,self.width,self.heigth)
            self.table.drawOn(self.pdfDocente,118,230)
            return self.table

    def validarModalidadLaboratorio(self):
        if self.dataLaboratorioModalidad == 'Diurno':
            self.table = Table(self.obtenerHorarioDiurnoLaboratorio(),colWidths=110, rowHeights=25)
            self.table.setStyle(TableStyle(self.setStyles))
            self.table.wrapOn(self.pdfLaboratorio,self.width,self.heigth)
            self.table.drawOn(self.pdfLaboratorio,118,157)
            return self.table
        if self.dataLaboratorioModalidad == 'Nocturno':
            self.table = Table(self.obtenerHorarioNocturnoLaboratorio(),colWidths=110, rowHeights=25)
            self.table.setStyle(TableStyle(self.setStyles))
            self.table.wrapOn(self.pdfLaboratorio,self.width,self.heigth)
            self.table.drawOn(self.pdfLaboratorio,118,307)
            return self.table

    def tablaDocente(self):
        if self.modalidad == 'Diurno':
            self.tableDocente = Table(self.obtenertablaDocenteDiurno(),colWidths=237, rowHeights=18)
            self.tableDocente.setStyle(TableStyle(self.setStylesCeldas))
            self.tableDocente.wrapOn(self.pdf,self.width,self.heigth)
            if self.counter == 15: 
                self.pdf.showPage()
                self.tableDocente.drawOn(self.pdf,68,270)
                print('-----------15')
            elif self.counter == 14: 
                self.pdf.showPage()
                self.tableDocente.drawOn(self.pdf,68,290)
                print('-----------14')
            elif self.counter == 13: 
                self.pdf.showPage()
                self.tableDocente.drawOn(self.pdf,68,310)
                print('-----------13')
            elif self.counter == 12: 
                self.pdf.showPage()
                self.tableDocente.drawOn(self.pdf,68,330)
                print('-----------12')
            elif self.counter == 11: 
                self.pdf.showPage()
                self.tableDocente.drawOn(self.pdf,68,350)
                print('-----------11')
            elif self.counter == 10:
                self.pdf.showPage() 
                self.tableDocente.drawOn(self.pdf,68,370)
                print('-----------10')
            elif self.counter == 9: 
                self.pdf.showPage()
                self.tableDocente.drawOn(self.pdf,68,390)
                print('-----------9')
            elif self.counter == 8: 
                self.pdf.showPage()
                self.tableDocente.drawOn(self.pdf,68,410)
                print('-----------8')
            elif self.counter == 7: 
                self.pdf.showPage()
                self.tableDocente.drawOn(self.pdf,68,430)
                print('-----------7')
            elif self.counter == 6: 
                self.pdf.showPage()
                self.tableDocente.drawOn(self.pdf,68,450)
                print('-----------6')
            elif self.counter == 5: 
                self.tableDocente.drawOn(self.pdf,68,25)
                print('-----------5')
            elif self.counter == 4: 
                self.tableDocente.drawOn(self.pdf,68,45)
                print('-----------4')
            elif self.counter == 3: 
                self.tableDocente.drawOn(self.pdf,68,65)
                print('-----------3')
            elif self.counter == 2: 
                self.tableDocente.drawOn(self.pdf,68,85)
                print('-----------2')
            elif self.counter == 1: 
                self.tableDocente.drawOn(self.pdf,68,105)
                print('-----------1')
            else:
                self.tableDocente.drawOn(self.pdf,68,125)
                print('-----------0')
            return self.tableDocente
        if self.modalidad == 'Nocturno':
            self.tableDocente = Table(self.obtenertablaDocenteNocturno(),colWidths=237, rowHeights=18)
            self.tableDocente.setStyle(TableStyle(self.setStylesCeldas))
            self.tableDocente.wrapOn(self.pdf,self.width,self.heigth)
            if self.counter == 15: 
                self.tableDocente.drawOn(self.pdf,68,5)
                print('-----------15')
            elif self.counter == 14: 
                self.tableDocente.drawOn(self.pdf,68,20)
                print('-----------14')
            elif self.counter == 13: 
                self.tableDocente.drawOn(self.pdf,68,40)
                print('-----------13')
            elif self.counter == 12: 
                self.tableDocente.drawOn(self.pdf,68,60)
                print('-----------12')
            elif self.counter == 11: 
                self.tableDocente.drawOn(self.pdf,68,75)
                print('-----------11')
            elif self.counter == 10: 
                self.tableDocente.drawOn(self.pdf,68,95)
                print('-----------10')
            elif self.counter == 9: 
                self.tableDocente.drawOn(self.pdf,68,115)
                print('-----------9')
            elif self.counter == 8: 
                self.tableDocente.drawOn(self.pdf,68,130)
                print('-----------8')
            elif self.counter == 7: 
                self.tableDocente.drawOn(self.pdf,68,150)
                print('-----------7')
            elif self.counter == 6: 
                self.tableDocente.drawOn(self.pdf,68,170)
                print('-----------6')
            elif self.counter == 5: 
                self.tableDocente.drawOn(self.pdf,68,185)
                print('-----------5')
            elif self.counter == 4: 
                self.tableDocente.drawOn(self.pdf,68,200)
                print('-----------4')
            elif self.counter == 3: 
                self.tableDocente.drawOn(self.pdf,68,220)
                print('-----------3')
            elif self.counter == 2: 
                self.tableDocente.drawOn(self.pdf,68,240)
                print('-----------2')
            elif self.counter == 1: 
                self.tableDocente.drawOn(self.pdf,68,260)
                print('-----------1')
            else:
                self.tableDocente.drawOn(self.pdf,68,280)
                print('-----------0')
            return self.tableDocente

    def tablaDocenteLaboratorio(self):
        if self.dataLaboratorioModalidad == 'Diurno':
            self.tableDocenteLaboratorio = Table(self.obtenertablaDocenteDiurnoLaboratorio(),colWidths=237, rowHeights=18)
            self.tableDocenteLaboratorio.setStyle(TableStyle(self.setStylesCeldas))
            self.tableDocenteLaboratorio.wrapOn(self.pdfLaboratorio,self.width,self.heigth)
            if self.counterLaboratorio == 15: 
                self.pdfLaboratorio.showPage()
                self.tableDocenteLaboratorio.drawOn(self.pdfLaboratorio,68,270)
                print('-----------15')
            elif self.counterLaboratorio == 14: 
                self.pdfLaboratorio.showPage()
                self.tableDocenteLaboratorio.drawOn(self.pdfLaboratorio,68,290)
                print('-----------14')
            elif self.counterLaboratorio == 13: 
                self.pdf.showPage()
                self.tableDocenteLaboratorio.drawOn(self.pdfLaboratorio,68,310)
                print('-----------13')
            elif self.counterLaboratorio == 12: 
                self.pdfLaboratorio.showPage()
                self.tableDocenteLaboratorio.drawOn(self.pdfLaboratorio,68,330)
                print('-----------12')
            elif self.counterLaboratorio == 11: 
                self.pdfLaboratorio.showPage()
                self.tableDocenteLaboratorio.drawOn(self.pdfLaboratorio,68,350)
                print('-----------11')
            elif self.counterLaboratorio == 10:
                self.pdfLaboratorio.showPage() 
                self.tableDocenteLaboratorio.drawOn(self.pdfLaboratorio,68,370)
                print('-----------10')
            elif self.counterLaboratorio == 9: 
                self.pdfLaboratorio.showPage()
                self.tableDocenteLaboratorio.drawOn(self.pdfLaboratorio,68,390)
                print('-----------9')
            elif self.counterLaboratorio == 8: 
                self.pdfLaboratorio.showPage()
                self.tableDocenteLaboratorio.drawOn(self.pdfLaboratorio,68,410)
                print('-----------8')
            elif self.counterLaboratorio == 7: 
                self.pdfLaboratorio.showPage()
                self.tableDocenteLaboratorio.drawOn(self.pdfLaboratorio,68,430)
                print('-----------7')
            elif self.counterLaboratorio == 6: 
                self.pdfLaboratorio.showPage()
                self.tableDocenteLaboratorio.drawOn(self.pdfLaboratorio,68,450)
                print('-----------6')
            elif self.counterLaboratorio == 5: 
                self.tableDocenteLaboratorio.drawOn(self.pdfLaboratorio,68,25)
                print('-----------5')
            elif self.counterLaboratorio == 4: 
                self.tableDocenteLaboratorio.drawOn(self.pdfLaboratorio,68,45)
                print('-----------4')
            elif self.counterLaboratorio == 3: 
                self.tableDocenteLaboratorio.drawOn(self.pdfLaboratorio,68,65)
                print('-----------3')
            elif self.counterLaboratorio == 2: 
                self.tableDocenteLaboratorio.drawOn(self.pdfLaboratorio,68,85)
                print('-----------2')
            elif self.counterLaboratorio == 1: 
                self.tableDocenteLaboratorio.drawOn(self.pdfLaboratorio,68,105)
                print('-----------1')
            else:
                self.tableDocenteLaboratorio.drawOn(self.pdfLaboratorio,68,125)
                print('-----------0')
            return self.tableDocenteLaboratorio
        if self.dataLaboratorioModalidad == 'Nocturno':
            self.tableDocenteLaboratorio = Table(self.obtenertablaDocenteNocturnoLaboratorio(),colWidths=237, rowHeights=18)
            self.tableDocenteLaboratorio.setStyle(TableStyle(self.setStylesCeldas))
            self.tableDocenteLaboratorio.wrapOn(self.pdfLaboratorio,self.width,self.heigth)
            if self.counterLaboratorio == 15: 
                self.tableDocenteLaboratorio.drawOn(self.pdfLaboratorio,68,5)
                print('-----------15')
            elif self.counterLaboratorio == 14: 
                self.tableDocenteLaboratorio.drawOn(self.pdfLaboratorio,68,20)
                print('-----------14')
            elif self.counterLaboratorio == 13: 
                self.tableDocenteLaboratorio.drawOn(self.pdfLaboratorio,68,40)
                print('-----------13')
            elif self.counterLaboratorio == 12: 
                self.tableDocenteLaboratorio.drawOn(self.pdfLaboratorio,68,60)
                print('-----------12')
            elif self.counterLaboratorio == 11: 
                self.tableDocenteLaboratorio.drawOn(self.pdfLaboratorio,68,75)
                print('-----------11')
            elif self.counterLaboratorio == 10: 
                self.tableDocenteLaboratorio.drawOn(self.pdfLaboratorio,68,95)
                print('-----------10')
            elif self.counterLaboratorio == 9: 
                self.tableDocenteLaboratorio.drawOn(self.pdfLaboratorio,68,115)
                print('-----------9')
            elif self.counterLaboratorio == 8: 
                self.tableDocenteLaboratorio.drawOn(self.pdfLaboratorio,68,130)
                print('-----------8')
            elif self.counterLaboratorio == 7: 
                self.tableDocenteLaboratorio.drawOn(self.pdfLaboratorio,68,150)
                print('-----------7')
            elif self.counterLaboratorio == 6: 
                self.tableDocenteLaboratorio.drawOn(self.pdfLaboratorio,68,170)
                print('-----------6')
            elif self.counterLaboratorio == 5: 
                self.tableDocenteLaboratorio.drawOn(self.pdfLaboratorio,68,185)
                print('-----------5')
            elif self.counterLaboratorio == 4: 
                self.tableDocenteLaboratorio.drawOn(self.pdfLaboratorio,68,200)
                print('-----------4')
            elif self.counterLaboratorio == 3: 
                self.tableDocenteLaboratorio.drawOn(self.pdfLaboratorio,68,220)
                print('-----------3')
            elif self.counterLaboratorio == 2: 
                self.tableDocenteLaboratorio.drawOn(self.pdfLaboratorio,68,240)
                print('-----------2')
            elif self.counterLaboratorio == 1: 
                self.tableDocenteLaboratorio.drawOn(self.pdfLaboratorio,68,260)
                print('-----------1')
            else:
                self.tableDocenteLaboratorio.drawOn(self.pdfLaboratorio,68,280)
                print('-----------0')
            return self.tableDocenteLaboratorio

    def materia(self,query,parametros):
        if self.conexion(query,parametros):
            if self.conexion(query,parametros).fetchone():
                self.data = self.conexion(query,parametros).fetchone()
                return self.data[0]
            else:
                return ''

    def celda1x6(self,
    parametros,
    query1,coorX0,coorY0,coorX1,coorY1,
    query2,coorX2,coorY2,coorX3,coorY3,
    query3,coorX4,coorY4,coorX5,coorY5,
    query4,coorX6,coorY6,coorX7,coorY7,
    query5,coorX8,coorY8,coorX9,coorY9,
    celda,modalidad
    ):
        consulta = self.materia(query1,parametros)
        if len(consulta) != 0:
            modalidad[celda].append(Paragraph(consulta,self.center))
            self.setStyles.append(('SPAN',(coorX0,coorY0),(coorX1,coorY1)))
            print('CONSULTA 1 EXITOSA')
        else:
            consulta = self.materia(query2,parametros)
            if len(consulta) != 0:
                modalidad[celda].append(Paragraph(consulta,self.center))
                self.setStyles.append(('SPAN',(coorX2,coorY2),(coorX3,coorY3)))
                print('CONSULTA 2 EXITOSA')
            else:
                consulta = self.materia(query3,parametros)
                if len(consulta) != 0:
                    modalidad[celda].append(Paragraph(consulta,self.center))
                    self.setStyles.append(('SPAN',(coorX4,coorY4),(coorX5,coorY5)))
                    print('CONSULTA 3 EXITOSA')
                else:
                    consulta = self.materia(query4,parametros)
                    if len(consulta) != 0:
                        modalidad[celda].append(Paragraph(consulta,self.center))
                        self.setStyles.append(('SPAN',(coorX6,coorY6),(coorX7,coorY7)))
                        print('CONSULTA 4 EXITOSA')
                    else:
                        consulta = self.materia(query5,parametros)
                        if len(consulta) != 0:
                            modalidad[celda].append(Paragraph(consulta,self.center))
                            self.setStyles.append(('SPAN',(coorX8,coorY8),(coorX9,coorY9)))
                            print('CONSULTA 5 EXITOSA')
                        else:
                            modalidad[celda].append(Paragraph(' ',self.center))
                            print('DENEGADO CAMARADA')

    def celda1x5(self,
    parametros,
    query1,coorX0,coorY0,coorX1,coorY1,
    query2,coorX2,coorY2,coorX3,coorY3,
    query3,coorX4,coorY4,coorX5,coorY5,
    query4,coorX6,coorY6,coorX7,coorY7,
    celda,modalidad
    ):
        consulta = self.materia(query1,parametros)
        if len(consulta) != 0:
            modalidad[celda].append(Paragraph(consulta,self.center))
            self.setStyles.append(('SPAN',(coorX0,coorY0),(coorX1,coorY1)))
            print('CONSULTA 1 EXITOSA')
        else:
            consulta = self.materia(query2,parametros)
            if len(consulta) != 0:
                modalidad[celda].append(Paragraph(consulta,self.center))
                self.setStyles.append(('SPAN',(coorX2,coorY2),(coorX3,coorY3)))
                print('CONSULTA 2 EXITOSA')
            else:
                consulta = self.materia(query3,parametros)
                if len(consulta) != 0:
                    modalidad[celda].append(Paragraph(consulta,self.center))
                    self.setStyles.append(('SPAN',(coorX4,coorY4),(coorX5,coorY5)))
                    print('CONSULTA 3 EXITOSA')
                else:
                    consulta = self.materia(query4,parametros)
                    if len(consulta) != 0:
                        modalidad[celda].append(Paragraph(consulta,self.center))
                        self.setStyles.append(('SPAN',(coorX6,coorY6),(coorX7,coorY7)))
                        print('CONSULTA 4 EXITOSA')
                    else:
                        modalidad[celda].append(Paragraph(' ',self.center))
                        print('DENEGADO CAMARADA')

    def celda1x4(self,
    parametros,
    query1,coorX0,coorY0,coorX1,coorY1,
    query2,coorX2,coorY2,coorX3,coorY3,
    query3,coorX4,coorY4,coorX5,coorY5,
    celda,modalidad
    ):
        consulta = self.materia(query1,parametros)
        if len(consulta) != 0:
            modalidad[celda].append(Paragraph(consulta,self.center))
            self.setStyles.append(('SPAN',(coorX0,coorY0),(coorX1,coorY1)))
            print('CONSULTA 1 EXITOSA')
        else:
            consulta = self.materia(query2,parametros)
            if len(consulta) != 0:
                modalidad[celda].append(Paragraph(consulta,self.center))
                self.setStyles.append(('SPAN',(coorX2,coorY2),(coorX3,coorY3)))
                print('CONSULTA 2 EXITOSA')
            else:
                consulta = self.materia(query3,parametros)
                if len(consulta) != 0:
                    modalidad[celda].append(Paragraph(consulta,self.center))
                    self.setStyles.append(('SPAN',(coorX4,coorY4),(coorX5,coorY5)))
                    print('CONSULTA 3 EXITOSA')
                else:
                    modalidad[celda].append(Paragraph(' ',self.center))
                    print('DENEGADO CAMARADA')

    def celda1x3(self,
    parametros,
    query1,coorX0,coorY0,coorX1,coorY1,
    query2,coorX2,coorY2,coorX3,coorY3,
    celda,modalidad
    ):
        consulta = self.materia(query1,parametros)
        if len(consulta) != 0:
            modalidad[celda].append(Paragraph(consulta,self.center))
            self.setStyles.append(('SPAN',(coorX0,coorY0),(coorX1,coorY1)))
            print('CONSULTA 1 EXITOSA')
        else:
            consulta = self.materia(query2,parametros)
            if len(consulta) != 0:
                modalidad[celda].append(Paragraph(consulta,self.center))
                self.setStyles.append(('SPAN',(coorX2,coorY2),(coorX3,coorY3)))
                print('CONSULTA 2 EXITOSA')
            else:
                modalidad[celda].append(Paragraph(' ',self.center))
                print('DENEGADO CAMARADA')

    def celda1x2(self,
    parametros,
    query1,coorX0,coorY0,coorX1,coorY1,
    celda,modalidad
    ):
        consulta = self.materia(query1,parametros)
        if len(consulta) != 0:
            modalidad[celda].append(Paragraph(consulta,self.center))
            self.setStyles.append(('SPAN',(coorX0,coorY0),(coorX1,coorY1)))
            print('CONSULTA 1 EXITOSA')
        else:
            modalidad[celda].append(Paragraph(' ',self.center))
            print('DENEGADO CAMARADA')

    def validarSemana(self,array,celda):
        if self.modalidad == 'Diurno':
            if not self.entryLunes.state() and not self.entryMartes.state() and not self.entryMiercoles.state() and not self.entryMiercoles.state() and not self.entryJueves.state() and not self.entryViernes.state():
                array[celda].clear()
                array[celda].append(Paragraph('bloque de horas diurno',self.center))
                array[celda].append(Paragraph('Lunes (' + self.entryLunes.get() + ')',self.center))
                array[celda].append(Paragraph('Martes (' + self.entryMartes.get() + ')',self.center))
                array[celda].append(Paragraph('Miércoles (' + self.entryMiercoles.get() + ')',self.center))
                array[celda].append(Paragraph('Jueves (' + self.entryMiercoles.get() + ')',self.center))
                array[celda].append(Paragraph('Viernes (' + self.entryMiercoles.get() + ')',self.center))
        if self.modalidad == 'Nocturno':
            if not self.entryLunes.state() and not self.entryMartes.state() and not self.entryMiercoles.state() and not self.entryMiercoles.state() and not self.entryJueves.state() and not self.entryViernes.state():
                array[celda].clear()
                array[celda].append(Paragraph('bloque de horas nocturno',self.center))
                array[celda].append(Paragraph('Lunes (' + self.entryLunes.get() + ')',self.center))
                array[celda].append(Paragraph('Martes (' + self.entryMartes.get() + ')',self.center))
                array[celda].append(Paragraph('Miércoles (' + self.entryMiercoles.get() + ')',self.center))
                array[celda].append(Paragraph('Jueves (' + self.entryMiercoles.get() + ')',self.center))
                array[celda].append(Paragraph('Viernes (' + self.entryMiercoles.get() + ')',self.center))
                
    def validarSemanaCeldas(self,array,celda):
        if self.dataModalidad == 'Diurno':
            if not self.entryLunes2.state() and not self.entryMartes2.state() and not self.entryMiercoles2.state() and not self.entryMiercoles2.state() and not self.entryJueves2.state() and not self.entryViernes2.state():
                array[celda].clear()
                array[celda].append(Paragraph('bloque de horas diurno',self.center))
                array[celda].append(Paragraph('Lunes (' + self.entryLunes2.get() + ')',self.center))
                array[celda].append(Paragraph('Martes (' + self.entryMartes2.get() + ')',self.center))
                array[celda].append(Paragraph('Miércoles (' + self.entryMiercoles2.get() + ')',self.center))
                array[celda].append(Paragraph('Jueves (' + self.entryMiercoles2.get() + ')',self.center))
                array[celda].append(Paragraph('Viernes (' + self.entryMiercoles2.get() + ')',self.center))
        if self.dataModalidad == 'Nocturno':
            if not self.entryLunes2.state() and not self.entryMartes2.state() and not self.entryMiercoles2.state() and not self.entryMiercoles2.state() and not self.entryJueves2.state() and not self.entryViernes2.state():
                array[celda].clear()
                array[celda].append(Paragraph('bloque de horas nocturno',self.center))
                array[celda].append(Paragraph('Lunes (' + self.entryLunes2.get() + ')',self.center))
                array[celda].append(Paragraph('Martes (' + self.entryMartes2.get() + ')',self.center))
                array[celda].append(Paragraph('Miércoles (' + self.entryMiercoles2.get() + ')',self.center))
                array[celda].append(Paragraph('Jueves (' + self.entryMiercoles2.get() + ')',self.center))
                array[celda].append(Paragraph('Viernes (' + self.entryMiercoles2.get() + ')',self.center))

    def validarSemanaLaboratorio(self,array,celda):
        if self.dataLaboratorioModalidad == 'Diurno':
            if not self.entryLunes3.state() and not self.entryMartes3.state() and not self.entryMiercoles3.state() and not self.entryMiercoles3.state() and not self.entryJueves3.state() and not self.entryViernes3.state():
                array[celda].clear()
                array[celda].append(Paragraph('bloque de horas diurno',self.center))
                array[celda].append(Paragraph('Lunes (' + self.entryLunes3.get() + ')',self.center))
                array[celda].append(Paragraph('Martes (' + self.entryMartes3.get() + ')',self.center))
                array[celda].append(Paragraph('Miércoles (' + self.entryMiercoles3.get() + ')',self.center))
                array[celda].append(Paragraph('Jueves (' + self.entryMiercoles3.get() + ')',self.center))
                array[celda].append(Paragraph('Viernes (' + self.entryMiercoles3.get() + ')',self.center))
        if self.dataLaboratorioModalidad == 'Nocturno':
            if not self.entryLunes3.state() and not self.entryMartes3.state() and not self.entryMiercoles3.state() and not self.entryMiercoles3.state() and not self.entryJueves3.state() and not self.entryViernes3.state():
                array[celda].clear()
                array[celda].append(Paragraph('bloque de horas nocturno',self.center))
                array[celda].append(Paragraph('Lunes (' + self.entryLunes3.get() + ')',self.center))
                array[celda].append(Paragraph('Martes (' + self.entryMartes3.get() + ')',self.center))
                array[celda].append(Paragraph('Miércoles (' + self.entryMiercoles3.get() + ')',self.center))
                array[celda].append(Paragraph('Jueves (' + self.entryMiercoles3.get() + ')',self.center))
                array[celda].append(Paragraph('Viernes (' + self.entryMiercoles3.get() + ')',self.center))

    def obtenerHorarioDiurno(self):
        self.diurno = [
            [Paragraph('bloque de horas diurno',self.center),Paragraph('Lunes',self.center),Paragraph('Martes',self.center),Paragraph('Miércoles',self.center),Paragraph('Jueves',self.center),Paragraph('Viernes',self.center)],
            [Paragraph('7:10 - 7:55',self.center)],
            [Paragraph('8:00 - 8:45',self.center)],
            [Paragraph('8:50 - 9:35',self.center)],
            [Paragraph('9:40 - 10:25',self.center)],
            [Paragraph('10:30 - 11:15',self.center)],
            [Paragraph('11:20 - 12:05',self.center)],
            [Paragraph('1:05 - 1:55',self.center)],
            [Paragraph('1:55 - 2:40',self.center)],
            [Paragraph('2:45 - 3:30',self.center)],
            [Paragraph('3:45 - 4:20',self.center)],
            [Paragraph('4:25 - 5:10',self.center)],
            [Paragraph('5:15 - 6:00',self.center)]
        ] 

        self.validarSemana(self.diurno,0)

        print('Primera linea ----------------')
        # Primera linea lunes
        self.celda1x6(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 1 AND materias_asignadas.Id_hora_inicial = 1 AND materias_asignadas.Id_hora_final = 2 AND materias_asignadas.Estado = "Activo"',
            1,1,1,2,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 1 AND materias_asignadas.Id_hora_inicial = 1 AND materias_asignadas.Id_hora_final = 3 AND materias_asignadas.Estado = "Activo"',
            1,1,1,3,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 1 AND materias_asignadas.Id_hora_inicial = 1 AND materias_asignadas.Id_hora_final = 4 AND materias_asignadas.Estado = "Activo"',
            1,1,1,4,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 1 AND materias_asignadas.Id_hora_inicial = 1 AND materias_asignadas.Id_hora_final = 5 AND materias_asignadas.Estado = "Activo"',
            1,1,1,5,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 1 AND materias_asignadas.Id_hora_inicial = 1 AND materias_asignadas.Id_hora_final = 6 AND materias_asignadas.Estado = "Activo"',
            1,1,1,6,
            1,self.diurno
        )

        # Primera linea Martes
        self.celda1x6(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 2 AND materias_asignadas.Id_hora_inicial = 1 AND materias_asignadas.Id_hora_final = 2 AND materias_asignadas.Estado = "Activo"',
            2,1,2,2,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 2 AND materias_asignadas.Id_hora_inicial = 1 AND materias_asignadas.Id_hora_final = 3 AND materias_asignadas.Estado = "Activo"',
            2,1,2,3,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 2 AND materias_asignadas.Id_hora_inicial = 1 AND materias_asignadas.Id_hora_final = 4 AND materias_asignadas.Estado = "Activo"',
            2,1,2,4,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 2 AND materias_asignadas.Id_hora_inicial = 1 AND materias_asignadas.Id_hora_final = 5 AND materias_asignadas.Estado = "Activo"',
            2,1,2,5,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 2 AND materias_asignadas.Id_hora_inicial = 1 AND materias_asignadas.Id_hora_final = 6 AND materias_asignadas.Estado = "Activo"',
            2,1,2,6,
            1,self.diurno
        ) 
        
        # Primera linea Miercoles
        self.celda1x6(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 3 AND materias_asignadas.Id_hora_inicial = 1 AND materias_asignadas.Id_hora_final = 2 AND materias_asignadas.Estado = "Activo"',
            3,1,3,2,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 3 AND materias_asignadas.Id_hora_inicial = 1 AND materias_asignadas.Id_hora_final = 3 AND materias_asignadas.Estado = "Activo"',
            3,1,3,3,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 3 AND materias_asignadas.Id_hora_inicial = 1 AND materias_asignadas.Id_hora_final = 4 AND materias_asignadas.Estado = "Activo"',
            3,1,3,4,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 3 AND materias_asignadas.Id_hora_inicial = 1 AND materias_asignadas.Id_hora_final = 5 AND materias_asignadas.Estado = "Activo"',
            3,1,3,5,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 3 AND materias_asignadas.Id_hora_inicial = 1 AND materias_asignadas.Id_hora_final = 6 AND materias_asignadas.Estado = "Activo"',
            3,1,3,6,
            1,self.diurno
        )

        # Primera linea Jueves
        self.celda1x6(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 4 AND materias_asignadas.Id_hora_inicial = 1 AND materias_asignadas.Id_hora_final = 2 AND materias_asignadas.Estado = "Activo"',
            4,1,4,2,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 4 AND materias_asignadas.Id_hora_inicial = 1 AND materias_asignadas.Id_hora_final = 3 AND materias_asignadas.Estado = "Activo"',
            4,1,4,3,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 4 AND materias_asignadas.Id_hora_inicial = 1 AND materias_asignadas.Id_hora_final = 4 AND materias_asignadas.Estado = "Activo"',
            4,1,4,4,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 4 AND materias_asignadas.Id_hora_inicial = 1 AND materias_asignadas.Id_hora_final = 5 AND materias_asignadas.Estado = "Activo"',
            4,1,4,5,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 4 AND materias_asignadas.Id_hora_inicial = 1 AND materias_asignadas.Id_hora_final = 6 AND materias_asignadas.Estado = "Activo"',
            4,1,4,6,
            1,self.diurno
        )

        # Primera linea Viernes
        self.celda1x6(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 5 AND materias_asignadas.Id_hora_inicial = 1 AND materias_asignadas.Id_hora_final = 2 AND materias_asignadas.Estado = "Activo"',
            5,1,5,2,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 5 AND materias_asignadas.Id_hora_inicial = 1 AND materias_asignadas.Id_hora_final = 3 AND materias_asignadas.Estado = "Activo"',
            5,1,5,3,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 5 AND materias_asignadas.Id_hora_inicial = 1 AND materias_asignadas.Id_hora_final = 4 AND materias_asignadas.Estado = "Activo"',
            5,1,5,4,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 5 AND materias_asignadas.Id_hora_inicial = 1 AND materias_asignadas.Id_hora_final = 5 AND materias_asignadas.Estado = "Activo"',
            5,1,5,5,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 5 AND materias_asignadas.Id_hora_inicial = 1 AND materias_asignadas.Id_hora_final = 6 AND materias_asignadas.Estado = "Activo"',
            5,1,5,6,
            1,self.diurno
        )
        print('Segunda linea ----------------')

        # Segunda linea lunes
        self.celda1x5(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 1 AND materias_asignadas.Id_hora_inicial = 2 AND materias_asignadas.Id_hora_final = 3 AND materias_asignadas.Estado = "Activo"',
            1,2,1,3,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 1 AND materias_asignadas.Id_hora_inicial = 2 AND materias_asignadas.Id_hora_final = 4 AND materias_asignadas.Estado = "Activo"',
            1,2,1,4,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 1 AND materias_asignadas.Id_hora_inicial = 2 AND materias_asignadas.Id_hora_final = 5 AND materias_asignadas.Estado = "Activo"',
            1,2,1,5,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 1 AND materias_asignadas.Id_hora_inicial = 2 AND materias_asignadas.Id_hora_final = 6 AND materias_asignadas.Estado = "Activo"',
            1,2,1,6,
            2,self.diurno
        )

        # Segunda linea Martes
        self.celda1x5(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 2 AND materias_asignadas.Id_hora_inicial = 2 AND materias_asignadas.Id_hora_final = 3 AND materias_asignadas.Estado = "Activo"',
            2,2,2,3,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 2 AND materias_asignadas.Id_hora_inicial = 2 AND materias_asignadas.Id_hora_final = 4 AND materias_asignadas.Estado = "Activo"',
            2,2,2,4,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 2 AND materias_asignadas.Id_hora_inicial = 2 AND materias_asignadas.Id_hora_final = 5 AND materias_asignadas.Estado = "Activo"',
            2,2,2,5,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 2 AND materias_asignadas.Id_hora_inicial = 2 AND materias_asignadas.Id_hora_final = 6 AND materias_asignadas.Estado = "Activo"',
            2,2,2,6,
            2,self.diurno
        )

        # Segunda linea Miercoles
        self.celda1x5(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 3 AND materias_asignadas.Id_hora_inicial = 2 AND materias_asignadas.Id_hora_final = 3 AND materias_asignadas.Estado = "Activo"',
            3,2,3,3,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 3 AND materias_asignadas.Id_hora_inicial = 2 AND materias_asignadas.Id_hora_final = 4 AND materias_asignadas.Estado = "Activo"',
            3,2,3,4,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 3 AND materias_asignadas.Id_hora_inicial = 2 AND materias_asignadas.Id_hora_final = 5 AND materias_asignadas.Estado = "Activo"',
            3,2,3,5,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 3 AND materias_asignadas.Id_hora_inicial = 2 AND materias_asignadas.Id_hora_final = 6 AND materias_asignadas.Estado = "Activo"',
            3,2,3,6,
            2,self.diurno
        )

        # Segunda linea Jueves
        self.celda1x5(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 4 AND materias_asignadas.Id_hora_inicial = 2 AND materias_asignadas.Id_hora_final = 3 AND materias_asignadas.Estado = "Activo"',
            4,2,4,3,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 4 AND materias_asignadas.Id_hora_inicial = 2 AND materias_asignadas.Id_hora_final = 4 AND materias_asignadas.Estado = "Activo"',
            4,2,4,4,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 4 AND materias_asignadas.Id_hora_inicial = 2 AND materias_asignadas.Id_hora_final = 5 AND materias_asignadas.Estado = "Activo"',
            4,2,4,5,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 4 AND materias_asignadas.Id_hora_inicial = 2 AND materias_asignadas.Id_hora_final = 6 AND materias_asignadas.Estado = "Activo"',
            4,2,4,6,
            2,self.diurno
        )

        # Segunda linea Vierves
        self.celda1x5(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 5 AND materias_asignadas.Id_hora_inicial = 2 AND materias_asignadas.Id_hora_final = 3 AND materias_asignadas.Estado = "Activo"',
            5,2,5,3,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 5 AND materias_asignadas.Id_hora_inicial = 2 AND materias_asignadas.Id_hora_final = 4 AND materias_asignadas.Estado = "Activo"',
            5,2,5,4,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 5 AND materias_asignadas.Id_hora_inicial = 2 AND materias_asignadas.Id_hora_final = 5 AND materias_asignadas.Estado = "Activo"',
            5,2,5,5,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 5 AND materias_asignadas.Id_hora_inicial = 2 AND materias_asignadas.Id_hora_final = 6 AND materias_asignadas.Estado = "Activo"',
            5,2,5,6,
            2,self.diurno
        )

        print('Tercera linea ----------------')

        # Tercera linea lunes
        self.celda1x4(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 1 AND materias_asignadas.Id_hora_inicial = 3 AND materias_asignadas.Id_hora_final = 4 AND materias_asignadas.Estado = "Activo"',
            1,3,1,4,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 1 AND materias_asignadas.Id_hora_inicial = 3 AND materias_asignadas.Id_hora_final = 5 AND materias_asignadas.Estado = "Activo"',
            1,3,1,5,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 1 AND materias_asignadas.Id_hora_inicial = 3 AND materias_asignadas.Id_hora_final = 6 AND materias_asignadas.Estado = "Activo"',
            1,3,1,6,
            3,self.diurno
        )

         # Tercera linea Martes
        self.celda1x4(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 2 AND materias_asignadas.Id_hora_inicial = 3 AND materias_asignadas.Id_hora_final = 4 AND materias_asignadas.Estado = "Activo"',
            2,3,2,4,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 2 AND materias_asignadas.Id_hora_inicial = 3 AND materias_asignadas.Id_hora_final = 5 AND materias_asignadas.Estado = "Activo"',
            2,3,2,5,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 2 AND materias_asignadas.Id_hora_inicial = 3 AND materias_asignadas.Id_hora_final = 6 AND materias_asignadas.Estado = "Activo"',
            2,3,2,6,
            3,self.diurno
        )

         # Tercera linea Miercoles
        self.celda1x4(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 3 AND materias_asignadas.Id_hora_inicial = 3 AND materias_asignadas.Id_hora_final = 4 AND materias_asignadas.Estado = "Activo"',
            3,3,3,4,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 3 AND materias_asignadas.Id_hora_inicial = 3 AND materias_asignadas.Id_hora_final = 5 AND materias_asignadas.Estado = "Activo"',
            3,3,3,5,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 3 AND materias_asignadas.Id_hora_inicial = 3 AND materias_asignadas.Id_hora_final = 6 AND materias_asignadas.Estado = "Activo"',
            3,3,3,6,
            3,self.diurno
        )

         # Tercera linea Jueves
        self.celda1x4(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 4 AND materias_asignadas.Id_hora_inicial = 3 AND materias_asignadas.Id_hora_final = 4 AND materias_asignadas.Estado = "Activo"',
            4,3,4,4,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 4 AND materias_asignadas.Id_hora_inicial = 3 AND materias_asignadas.Id_hora_final = 5 AND materias_asignadas.Estado = "Activo"',
            4,3,4,5,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 4 AND materias_asignadas.Id_hora_inicial = 3 AND materias_asignadas.Id_hora_final = 6 AND materias_asignadas.Estado = "Activo"',
            4,3,4,6,
            3,self.diurno
        )

         # Tercera linea Viernes
        self.celda1x4(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 5 AND materias_asignadas.Id_hora_inicial = 3 AND materias_asignadas.Id_hora_final = 4 AND materias_asignadas.Estado = "Activo"',
            5,3,5,4,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 5 AND materias_asignadas.Id_hora_inicial = 3 AND materias_asignadas.Id_hora_final = 5 AND materias_asignadas.Estado = "Activo"',
            5,3,5,5,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 5 AND materias_asignadas.Id_hora_inicial = 3 AND materias_asignadas.Id_hora_final = 6 AND materias_asignadas.Estado = "Activo"',
            5,3,5,6,
            3,self.diurno
        )

        print('Cuarta linea ----------------')

        # Cuarta linea lunes
        self.celda1x3(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 1 AND materias_asignadas.Id_hora_inicial = 4 AND materias_asignadas.Id_hora_final = 5 AND materias_asignadas.Estado = "Activo"',
            1,4,1,5,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 1 AND materias_asignadas.Id_hora_inicial = 4 AND materias_asignadas.Id_hora_final = 6 AND materias_asignadas.Estado = "Activo"',
            1,4,1,6,
            4,self.diurno
        )

        # Cuarta linea Martes
        self.celda1x3(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 2 AND materias_asignadas.Id_hora_inicial = 4 AND materias_asignadas.Id_hora_final = 5 AND materias_asignadas.Estado = "Activo"',
            2,4,2,5,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 2 AND materias_asignadas.Id_hora_inicial = 4 AND materias_asignadas.Id_hora_final = 6 AND materias_asignadas.Estado = "Activo"',
            2,4,2,6,
            4,self.diurno
        )

        # Cuarta linea Miercoles
        self.celda1x3(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 3 AND materias_asignadas.Id_hora_inicial = 4 AND materias_asignadas.Id_hora_final = 5 AND materias_asignadas.Estado = "Activo"',
            3,4,3,5,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 3 AND materias_asignadas.Id_hora_inicial = 4 AND materias_asignadas.Id_hora_final = 6 AND materias_asignadas.Estado = "Activo"',
            3,4,3,6,
            4,self.diurno
        )

        # Cuarta linea Jueves
        self.celda1x3(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 4 AND materias_asignadas.Id_hora_inicial = 4 AND materias_asignadas.Id_hora_final = 5 AND materias_asignadas.Estado = "Activo"',
            4,4,4,5,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 4 AND materias_asignadas.Id_hora_inicial = 4 AND materias_asignadas.Id_hora_final = 6 AND materias_asignadas.Estado = "Activo"',
            4,4,4,6,
            4,self.diurno
        )

        # Cuarta linea Viernes
        self.celda1x3(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 5 AND materias_asignadas.Id_hora_inicial = 4 AND materias_asignadas.Id_hora_final = 5 AND materias_asignadas.Estado = "Activo"',
            5,4,5,5,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 5 AND materias_asignadas.Id_hora_inicial = 4 AND materias_asignadas.Id_hora_final = 6 AND materias_asignadas.Estado = "Activo"',
            5,4,5,6,
            4,self.diurno
        )

        print('Quinta linea ----------------')

        # Quinta linea lunes
        self.celda1x2(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 1 AND materias_asignadas.Id_hora_inicial = 5 AND materias_asignadas.Id_hora_final = 6 AND materias_asignadas.Estado = "Activo"',
            1,5,1,6,
            5,self.diurno
        )

        # Quinta linea Martes
        self.celda1x2(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 2 AND materias_asignadas.Id_hora_inicial = 5 AND materias_asignadas.Id_hora_final = 6 AND materias_asignadas.Estado = "Activo"',
            2,5,2,6,
            5,self.diurno
        )

        # Quinta linea Miercoles
        self.celda1x2(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 3 AND materias_asignadas.Id_hora_inicial = 5 AND materias_asignadas.Id_hora_final = 6 AND materias_asignadas.Estado = "Activo"',
            3,5,3,6,
            5,self.diurno
        )

        # Quinta linea Jueves
        self.celda1x2(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 4 AND materias_asignadas.Id_hora_inicial = 5 AND materias_asignadas.Id_hora_final = 6 AND materias_asignadas.Estado = "Activo"',
            4,5,4,6,
            5,self.diurno
        )

        # Quinta linea Viernes
        self.celda1x2(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 5 AND materias_asignadas.Id_hora_inicial = 5 AND materias_asignadas.Id_hora_final = 6 AND materias_asignadas.Estado = "Activo"',
            5,5,5,6,
            5,self.diurno
        )

        print('Septima linea ----------------')

        # Septima linea lunes
        self.celda1x6(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 1 AND materias_asignadas.Id_hora_inicial = 7 AND materias_asignadas.Id_hora_final = 8 AND materias_asignadas.Estado = "Activo"',
            1,7,1,8,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 1 AND materias_asignadas.Id_hora_inicial = 7 AND materias_asignadas.Id_hora_final = 9 AND materias_asignadas.Estado = "Activo"',
            1,7,1,9,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 1 AND materias_asignadas.Id_hora_inicial = 7 AND materias_asignadas.Id_hora_final = 10 AND materias_asignadas.Estado = "Activo"',
            1,7,1,10,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 1 AND materias_asignadas.Id_hora_inicial = 7 AND materias_asignadas.Id_hora_final = 11 AND materias_asignadas.Estado = "Activo"',
            1,7,1,11,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 1 AND materias_asignadas.Id_hora_inicial = 7 AND materias_asignadas.Id_hora_final = 12 AND materias_asignadas.Estado = "Activo"',
            1,7,1,12,
            7,self.diurno
        )

        # Septima linea Martes
        self.celda1x6(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 2 AND materias_asignadas.Id_hora_inicial = 7 AND materias_asignadas.Id_hora_final = 8 AND materias_asignadas.Estado = "Activo"',
            2,7,2,8,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 2 AND materias_asignadas.Id_hora_inicial = 7 AND materias_asignadas.Id_hora_final = 9 AND materias_asignadas.Estado = "Activo"',
            2,7,2,9,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 2 AND materias_asignadas.Id_hora_inicial = 7 AND materias_asignadas.Id_hora_final = 10 AND materias_asignadas.Estado = "Activo"',
            2,7,2,10,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 2 AND materias_asignadas.Id_hora_inicial = 7 AND materias_asignadas.Id_hora_final = 11 AND materias_asignadas.Estado = "Activo"',
            2,7,2,11,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 2 AND materias_asignadas.Id_hora_inicial = 7 AND materias_asignadas.Id_hora_final = 12 AND materias_asignadas.Estado = "Activo"',
            2,7,2,12,
            7,self.diurno
        )

        # Septima linea Miercoles
        self.celda1x6(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 3 AND materias_asignadas.Id_hora_inicial = 7 AND materias_asignadas.Id_hora_final = 8 AND materias_asignadas.Estado = "Activo"',
            3,7,3,8,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 3 AND materias_asignadas.Id_hora_inicial = 7 AND materias_asignadas.Id_hora_final = 9 AND materias_asignadas.Estado = "Activo"',
            3,7,3,9,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 3 AND materias_asignadas.Id_hora_inicial = 7 AND materias_asignadas.Id_hora_final = 10 AND materias_asignadas.Estado = "Activo"',
            3,7,3,10,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 3 AND materias_asignadas.Id_hora_inicial = 7 AND materias_asignadas.Id_hora_final = 11 AND materias_asignadas.Estado = "Activo"',
            3,7,3,11,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 3 AND materias_asignadas.Id_hora_inicial = 7 AND materias_asignadas.Id_hora_final = 12 AND materias_asignadas.Estado = "Activo"',
            3,7,3,12,
            7,self.diurno
        )

        # Septima linea Jueves
        self.celda1x6(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 4 AND materias_asignadas.Id_hora_inicial = 7 AND materias_asignadas.Id_hora_final = 8 AND materias_asignadas.Estado = "Activo"',
            4,7,4,8,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 4 AND materias_asignadas.Id_hora_inicial = 7 AND materias_asignadas.Id_hora_final = 9 AND materias_asignadas.Estado = "Activo"',
            4,7,4,9,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 4 AND materias_asignadas.Id_hora_inicial = 7 AND materias_asignadas.Id_hora_final = 10 AND materias_asignadas.Estado = "Activo"',
            4,7,4,10,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 4 AND materias_asignadas.Id_hora_inicial = 7 AND materias_asignadas.Id_hora_final = 11 AND materias_asignadas.Estado = "Activo"',
            4,7,4,11,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 4 AND materias_asignadas.Id_hora_inicial = 7 AND materias_asignadas.Id_hora_final = 12 AND materias_asignadas.Estado = "Activo"',
            4,7,4,12,
            7,self.diurno
        )

        # Septima linea Viernes
        self.celda1x6(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 5 AND materias_asignadas.Id_hora_inicial = 7 AND materias_asignadas.Id_hora_final = 8 AND materias_asignadas.Estado = "Activo"',
            5,7,5,8,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 5 AND materias_asignadas.Id_hora_inicial = 7 AND materias_asignadas.Id_hora_final = 9 AND materias_asignadas.Estado = "Activo"',
            5,7,5,9,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 5 AND materias_asignadas.Id_hora_inicial = 7 AND materias_asignadas.Id_hora_final = 10 AND materias_asignadas.Estado = "Activo"',
            5,7,5,10,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 5 AND materias_asignadas.Id_hora_inicial = 7 AND materias_asignadas.Id_hora_final = 11 AND materias_asignadas.Estado = "Activo"',
            5,7,5,11,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 5 AND materias_asignadas.Id_hora_inicial = 7 AND materias_asignadas.Id_hora_final = 12 AND materias_asignadas.Estado = "Activo"',
            5,7,5,12,
            7,self.diurno
        )

        print('Octava linea ----------------')

        # Octava linea lunes
        self.celda1x5(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 1 AND materias_asignadas.Id_hora_inicial = 8 AND materias_asignadas.Id_hora_final = 9 AND materias_asignadas.Estado = "Activo"',
            1,8,1,9,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 1 AND materias_asignadas.Id_hora_inicial = 8 AND materias_asignadas.Id_hora_final = 10 AND materias_asignadas.Estado = "Activo"',
            1,8,1,10,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 1 AND materias_asignadas.Id_hora_inicial = 8 AND materias_asignadas.Id_hora_final = 11 AND materias_asignadas.Estado = "Activo"',
            1,8,1,11,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 1 AND materias_asignadas.Id_hora_inicial = 8 AND materias_asignadas.Id_hora_final = 12 AND materias_asignadas.Estado = "Activo"',
            1,8,1,12,
            8,self.diurno
        )

        # Octava linea Martes
        self.celda1x5(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 2 AND materias_asignadas.Id_hora_inicial = 8 AND materias_asignadas.Id_hora_final = 9 AND materias_asignadas.Estado = "Activo"',
            2,8,2,9,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 2 AND materias_asignadas.Id_hora_inicial = 8 AND materias_asignadas.Id_hora_final = 10 AND materias_asignadas.Estado = "Activo"',
            2,8,2,10,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 2 AND materias_asignadas.Id_hora_inicial = 8 AND materias_asignadas.Id_hora_final = 11 AND materias_asignadas.Estado = "Activo"',
            2,8,2,11,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 2 AND materias_asignadas.Id_hora_inicial = 8 AND materias_asignadas.Id_hora_final = 12 AND materias_asignadas.Estado = "Activo"',
            2,8,2,12,
            8,self.diurno
        )

        # Octava linea Miercoles
        self.celda1x5(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 3 AND materias_asignadas.Id_hora_inicial = 8 AND materias_asignadas.Id_hora_final = 9 AND materias_asignadas.Estado = "Activo"',
            3,8,3,9,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 3 AND materias_asignadas.Id_hora_inicial = 8 AND materias_asignadas.Id_hora_final = 10 AND materias_asignadas.Estado = "Activo"',
            3,8,3,10,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 3 AND materias_asignadas.Id_hora_inicial = 8 AND materias_asignadas.Id_hora_final = 11 AND materias_asignadas.Estado = "Activo"',
            3,8,3,11,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 3 AND materias_asignadas.Id_hora_inicial = 8 AND materias_asignadas.Id_hora_final = 12 AND materias_asignadas.Estado = "Activo"',
            3,8,3,12,
            8,self.diurno
        )

        # Octava linea jueves
        self.celda1x5(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 4 AND materias_asignadas.Id_hora_inicial = 8 AND materias_asignadas.Id_hora_final = 9 AND materias_asignadas.Estado = "Activo"',
            4,8,4,9,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 4 AND materias_asignadas.Id_hora_inicial = 8 AND materias_asignadas.Id_hora_final = 10 AND materias_asignadas.Estado = "Activo"',
            4,8,4,10,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 4 AND materias_asignadas.Id_hora_inicial = 8 AND materias_asignadas.Id_hora_final = 11 AND materias_asignadas.Estado = "Activo"',
            4,8,4,11,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 4 AND materias_asignadas.Id_hora_inicial = 8 AND materias_asignadas.Id_hora_final = 12 AND materias_asignadas.Estado = "Activo"',
            4,8,4,12,
            8,self.diurno
        )

        # Octava linea 
        self.celda1x5(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 5 AND materias_asignadas.Id_hora_inicial = 8 AND materias_asignadas.Id_hora_final = 9 AND materias_asignadas.Estado = "Activo"',
            5,8,5,9,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 5 AND materias_asignadas.Id_hora_inicial = 8 AND materias_asignadas.Id_hora_final = 10 AND materias_asignadas.Estado = "Activo"',
            5,8,5,10,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 5 AND materias_asignadas.Id_hora_inicial = 8 AND materias_asignadas.Id_hora_final = 11 AND materias_asignadas.Estado = "Activo"',
            5,8,5,11,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 5 AND materias_asignadas.Id_hora_inicial = 8 AND materias_asignadas.Id_hora_final = 12 AND materias_asignadas.Estado = "Activo"',
            5,8,5,12,
            8,self.diurno
        )

        print('Noveno linea ----------------')

        # Noveno linea lunes
        self.celda1x4(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 1 AND materias_asignadas.Id_hora_inicial = 9 AND materias_asignadas.Id_hora_final = 10 AND materias_asignadas.Estado = "Activo"',
            1,9,1,10,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 1 AND materias_asignadas.Id_hora_inicial = 9 AND materias_asignadas.Id_hora_final = 11 AND materias_asignadas.Estado = "Activo"',
            1,9,1,11,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 1 AND materias_asignadas.Id_hora_inicial = 9 AND materias_asignadas.Id_hora_final = 12 AND materias_asignadas.Estado = "Activo"',
            1,9,1,12,
            9,self.diurno
        )

        # Noveno linea Martes
        self.celda1x4(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 2 AND materias_asignadas.Id_hora_inicial = 9 AND materias_asignadas.Id_hora_final = 10 AND materias_asignadas.Estado = "Activo"',
            2,9,2,10,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 2 AND materias_asignadas.Id_hora_inicial = 9 AND materias_asignadas.Id_hora_final = 11 AND materias_asignadas.Estado = "Activo"',
            2,9,2,11,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 2 AND materias_asignadas.Id_hora_inicial = 9 AND materias_asignadas.Id_hora_final = 12 AND materias_asignadas.Estado = "Activo"',
            2,9,2,12,
            9,self.diurno
        )

        # Noveno linea Miercoles
        self.celda1x4(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 3 AND materias_asignadas.Id_hora_inicial = 9 AND materias_asignadas.Id_hora_final = 10 AND materias_asignadas.Estado = "Activo"',
            3,9,3,10,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 3 AND materias_asignadas.Id_hora_inicial = 9 AND materias_asignadas.Id_hora_final = 11 AND materias_asignadas.Estado = "Activo"',
            3,9,3,11,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 3 AND materias_asignadas.Id_hora_inicial = 9 AND materias_asignadas.Id_hora_final = 12 AND materias_asignadas.Estado = "Activo"',
            3,9,3,12,
            9,self.diurno
        )

        # Noveno linea Jueves
        self.celda1x4(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 4 AND materias_asignadas.Id_hora_inicial = 9 AND materias_asignadas.Id_hora_final = 10 AND materias_asignadas.Estado = "Activo"',
            4,9,4,10,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 4 AND materias_asignadas.Id_hora_inicial = 9 AND materias_asignadas.Id_hora_final = 11 AND materias_asignadas.Estado = "Activo"',
            4,9,4,11,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 4 AND materias_asignadas.Id_hora_inicial = 9 AND materias_asignadas.Id_hora_final = 12 AND materias_asignadas.Estado = "Activo"',
            4,9,4,12,
            9,self.diurno
        )

        # Noveno linea Viernes
        self.celda1x4(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 5 AND materias_asignadas.Id_hora_inicial = 9 AND materias_asignadas.Id_hora_final = 10 AND materias_asignadas.Estado = "Activo"',
            5,9,5,10,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 5 AND materias_asignadas.Id_hora_inicial = 9 AND materias_asignadas.Id_hora_final = 11 AND materias_asignadas.Estado = "Activo"',
            5,9,5,11,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 5 AND materias_asignadas.Id_hora_inicial = 9 AND materias_asignadas.Id_hora_final = 12 AND materias_asignadas.Estado = "Activo"',
            5,9,5,12,
            9,self.diurno
        )

        print('Decimo linea ----------------')

        # Decimo linea lunes
        self.celda1x3(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 1 AND materias_asignadas.Id_hora_inicial = 10 AND materias_asignadas.Id_hora_final = 11 AND materias_asignadas.Estado = "Activo"',
            1,10,1,11,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 1 AND materias_asignadas.Id_hora_inicial = 10 AND materias_asignadas.Id_hora_final = 12 AND materias_asignadas.Estado = "Activo"',
            1,10,1,12,
            10,self.diurno
        )

        # Decimo linea Martes
        self.celda1x3(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 2 AND materias_asignadas.Id_hora_inicial = 10 AND materias_asignadas.Id_hora_final = 11 AND materias_asignadas.Estado = "Activo"',
            2,10,2,11,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 2 AND materias_asignadas.Id_hora_inicial = 10 AND materias_asignadas.Id_hora_final = 12 AND materias_asignadas.Estado = "Activo"',
            2,10,2,12,
            10,self.diurno
        )

        # Decimo linea Miercoles
        self.celda1x3(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 3 AND materias_asignadas.Id_hora_inicial = 10 AND materias_asignadas.Id_hora_final = 11 AND materias_asignadas.Estado = "Activo"',
            3,10,3,11,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 3 AND materias_asignadas.Id_hora_inicial = 10 AND materias_asignadas.Id_hora_final = 12 AND materias_asignadas.Estado = "Activo"',
            3,10,3,12,
            10,self.diurno
        )

        # Decimo linea Jueves
        self.celda1x3(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 4 AND materias_asignadas.Id_hora_inicial = 10 AND materias_asignadas.Id_hora_final = 11 AND materias_asignadas.Estado = "Activo"',
            4,10,4,11,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 4 AND materias_asignadas.Id_hora_inicial = 10 AND materias_asignadas.Id_hora_final = 12 AND materias_asignadas.Estado = "Activo"',
            4,10,4,12,
            10,self.diurno
        )

        # Decimo linea Viernes
        self.celda1x3(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 5 AND materias_asignadas.Id_hora_inicial = 10 AND materias_asignadas.Id_hora_final = 11 AND materias_asignadas.Estado = "Activo"',
            5,10,5,11,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 5 AND materias_asignadas.Id_hora_inicial = 10 AND materias_asignadas.Id_hora_final = 12 AND materias_asignadas.Estado = "Activo"',
            5,10,5,12,
            10,self.diurno
        )

        print('Decima primera linea ----------------')

        # Decima primera lunes
        self.celda1x2(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 1 AND materias_asignadas.Id_hora_inicial = 11 AND materias_asignadas.Id_hora_final = 12 AND materias_asignadas.Estado = "Activo"',
            1,11,1,12,
            11,self.diurno
        )

        # Decima primera Martes
        self.celda1x2(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 2 AND materias_asignadas.Id_hora_inicial = 11 AND materias_asignadas.Id_hora_final = 12 AND materias_asignadas.Estado = "Activo"',
            2,11,2,12,
            11,self.diurno
        )

        # Decima primera Miercoles
        self.celda1x2(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 3 AND materias_asignadas.Id_hora_inicial = 11 AND materias_asignadas.Id_hora_final = 12 AND materias_asignadas.Estado = "Activo"',
            3,11,3,12,
            11,self.diurno
        )

        # Decima primera Jueves
        self.celda1x2(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 4 AND materias_asignadas.Id_hora_inicial = 11 AND materias_asignadas.Id_hora_final = 12 AND materias_asignadas.Estado = "Activo"',
            4,11,4,12,
            11,self.diurno
        )

        # Decima primera Viernes
        self.celda1x2(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 5 AND materias_asignadas.Id_hora_inicial = 11 AND materias_asignadas.Id_hora_final = 12 AND materias_asignadas.Estado = "Activo"',
            5,11,5,12,
            11,self.diurno
        )
        return self.diurno

    def obtenerHorarioNocturno(self):
        self.nocturno = [
            [Paragraph('bloque de horas noche',self.center),Paragraph('Lunes',self.center),Paragraph('Martes',self.center),Paragraph('Miércoles',self.center),Paragraph('Jueves',self.center),Paragraph('Viernes',self.center)],
            [Paragraph('6:00 - 6:45',self.center)],
            [Paragraph('6:45 - 7:30',self.center)],
            [Paragraph('7:35 - 8:20',self.center)],
            [Paragraph('8:20 - 9:05',self.center)],
            [Paragraph('9:05 - 9:50',self.center)],
            [Paragraph('9:50 - 10:35',self.center)]
        ] 
        
        self.validarSemana(self.nocturno,0)

        print('Primera linea ----------------')
        # Primera linea lunes
        self.celda1x6(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 1 AND materias_asignadas.Id_hora_inicial = 13 AND materias_asignadas.Id_hora_final = 14 AND materias_asignadas.Estado = "Activo"',
            1,1,1,2,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 1 AND materias_asignadas.Id_hora_inicial = 13 AND materias_asignadas.Id_hora_final = 15 AND materias_asignadas.Estado = "Activo"',
            1,1,1,3,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 1 AND materias_asignadas.Id_hora_inicial = 13 AND materias_asignadas.Id_hora_final = 16 AND materias_asignadas.Estado = "Activo"',
            1,1,1,4,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 1 AND materias_asignadas.Id_hora_inicial = 13 AND materias_asignadas.Id_hora_final = 17 AND materias_asignadas.Estado = "Activo"',
            1,1,1,5,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 1 AND materias_asignadas.Id_hora_inicial = 13 AND materias_asignadas.Id_hora_final = 18 AND materias_asignadas.Estado = "Activo"',
            1,1,1,6,
            1,self.nocturno
        )

        # Primera linea Martes
        self.celda1x6(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 2 AND materias_asignadas.Id_hora_inicial = 13 AND materias_asignadas.Id_hora_final = 14 AND materias_asignadas.Estado = "Activo"',
            2,1,2,2,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 2 AND materias_asignadas.Id_hora_inicial = 13 AND materias_asignadas.Id_hora_final = 15 AND materias_asignadas.Estado = "Activo"',
            2,1,2,3,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 2 AND materias_asignadas.Id_hora_inicial = 13 AND materias_asignadas.Id_hora_final = 16 AND materias_asignadas.Estado = "Activo"',
            2,1,2,4,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 2 AND materias_asignadas.Id_hora_inicial = 13 AND materias_asignadas.Id_hora_final = 17 AND materias_asignadas.Estado = "Activo"',
            2,1,2,5,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 2 AND materias_asignadas.Id_hora_inicial = 13 AND materias_asignadas.Id_hora_final = 18 AND materias_asignadas.Estado = "Activo"',
            2,1,2,6,
            1,self.nocturno
        )

        # Primera linea Miercoles
        self.celda1x6(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 3 AND materias_asignadas.Id_hora_inicial = 13 AND materias_asignadas.Id_hora_final = 14 AND materias_asignadas.Estado = "Activo"',
            3,1,3,2,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 3 AND materias_asignadas.Id_hora_inicial = 13 AND materias_asignadas.Id_hora_final = 15 AND materias_asignadas.Estado = "Activo"',
            3,1,3,3,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 3 AND materias_asignadas.Id_hora_inicial = 13 AND materias_asignadas.Id_hora_final = 16 AND materias_asignadas.Estado = "Activo"',
            3,1,3,4,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 3 AND materias_asignadas.Id_hora_inicial = 13 AND materias_asignadas.Id_hora_final = 17 AND materias_asignadas.Estado = "Activo"',
            3,1,3,5,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 3 AND materias_asignadas.Id_hora_inicial = 13 AND materias_asignadas.Id_hora_final = 18 AND materias_asignadas.Estado = "Activo"',
            3,1,3,6,
            1,self.nocturno
        )

        # Primera linea Jueves
        self.celda1x6(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 4 AND materias_asignadas.Id_hora_inicial = 13 AND materias_asignadas.Id_hora_final = 14 AND materias_asignadas.Estado = "Activo"',
            4,1,4,2,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 4 AND materias_asignadas.Id_hora_inicial = 13 AND materias_asignadas.Id_hora_final = 15 AND materias_asignadas.Estado = "Activo"',
            4,1,4,3,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 4 AND materias_asignadas.Id_hora_inicial = 13 AND materias_asignadas.Id_hora_final = 16 AND materias_asignadas.Estado = "Activo"',
            4,1,4,4,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 4 AND materias_asignadas.Id_hora_inicial = 13 AND materias_asignadas.Id_hora_final = 17 AND materias_asignadas.Estado = "Activo"',
            4,1,4,5,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 4 AND materias_asignadas.Id_hora_inicial = 13 AND materias_asignadas.Id_hora_final = 18 AND materias_asignadas.Estado = "Activo"',
            4,1,4,6,
            1,self.nocturno
        )

        # Primera linea lunes
        self.celda1x6(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 5 AND materias_asignadas.Id_hora_inicial = 13 AND materias_asignadas.Id_hora_final = 14 AND materias_asignadas.Estado = "Activo"',
            5,1,5,2,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 5 AND materias_asignadas.Id_hora_inicial = 13 AND materias_asignadas.Id_hora_final = 15 AND materias_asignadas.Estado = "Activo"',
            5,1,5,3,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 5 AND materias_asignadas.Id_hora_inicial = 13 AND materias_asignadas.Id_hora_final = 16 AND materias_asignadas.Estado = "Activo"',
            5,1,5,4,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 5 AND materias_asignadas.Id_hora_inicial = 13 AND materias_asignadas.Id_hora_final = 17 AND materias_asignadas.Estado = "Activo"',
            5,1,5,5,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 5 AND materias_asignadas.Id_hora_inicial = 13 AND materias_asignadas.Id_hora_final = 18 AND materias_asignadas.Estado = "Activo"',
            5,1,5,6,
            1,self.nocturno
        )

        print('Segunda linea ----------------')

        # Segunda linea lunes
        self.celda1x5(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 1 AND materias_asignadas.Id_hora_inicial = 14 AND materias_asignadas.Id_hora_final = 15 AND materias_asignadas.Estado = "Activo"',
            1,2,1,3,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 1 AND materias_asignadas.Id_hora_inicial = 14 AND materias_asignadas.Id_hora_final = 16 AND materias_asignadas.Estado = "Activo"',
            1,2,1,4,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 1 AND materias_asignadas.Id_hora_inicial = 14 AND materias_asignadas.Id_hora_final = 17 AND materias_asignadas.Estado = "Activo"',
            1,2,1,5,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 1 AND materias_asignadas.Id_hora_inicial = 14 AND materias_asignadas.Id_hora_final = 18 AND materias_asignadas.Estado = "Activo"',
            1,2,1,6,
            2,self.nocturno
        )

         # Segunda linea Martes
        self.celda1x5(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 2 AND materias_asignadas.Id_hora_inicial = 14 AND materias_asignadas.Id_hora_final = 15 AND materias_asignadas.Estado = "Activo"',
            2,2,2,3,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 2 AND materias_asignadas.Id_hora_inicial = 14 AND materias_asignadas.Id_hora_final = 16 AND materias_asignadas.Estado = "Activo"',
            2,2,2,4,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 2 AND materias_asignadas.Id_hora_inicial = 14 AND materias_asignadas.Id_hora_final = 17 AND materias_asignadas.Estado = "Activo"',
            2,2,2,5,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 2 AND materias_asignadas.Id_hora_inicial = 14 AND materias_asignadas.Id_hora_final = 18 AND materias_asignadas.Estado = "Activo"',
            2,2,2,6,
            2,self.nocturno
        )

         # Segunda linea Miercoles
        self.celda1x5(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 3 AND materias_asignadas.Id_hora_inicial = 14 AND materias_asignadas.Id_hora_final = 15 AND materias_asignadas.Estado = "Activo"',
            3,2,3,3,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 3 AND materias_asignadas.Id_hora_inicial = 14 AND materias_asignadas.Id_hora_final = 16 AND materias_asignadas.Estado = "Activo"',
            3,2,3,4,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 3 AND materias_asignadas.Id_hora_inicial = 14 AND materias_asignadas.Id_hora_final = 17 AND materias_asignadas.Estado = "Activo"',
            3,2,3,5,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 3 AND materias_asignadas.Id_hora_inicial = 14 AND materias_asignadas.Id_hora_final = 18 AND materias_asignadas.Estado = "Activo"',
            3,2,3,6,
            2,self.nocturno
        )

         # Segunda linea Jueves
        self.celda1x5(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 4 AND materias_asignadas.Id_hora_inicial = 14 AND materias_asignadas.Id_hora_final = 15 AND materias_asignadas.Estado = "Activo"',
            4,2,4,3,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 4 AND materias_asignadas.Id_hora_inicial = 14 AND materias_asignadas.Id_hora_final = 16 AND materias_asignadas.Estado = "Activo"',
            4,2,4,4,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 4 AND materias_asignadas.Id_hora_inicial = 14 AND materias_asignadas.Id_hora_final = 17 AND materias_asignadas.Estado = "Activo"',
            4,2,4,5,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 4 AND materias_asignadas.Id_hora_inicial = 14 AND materias_asignadas.Id_hora_final = 18 AND materias_asignadas.Estado = "Activo"',
            4,2,4,6,
            2,self.nocturno
        )

         # Segunda linea Viernes
        self.celda1x5(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 5 AND materias_asignadas.Id_hora_inicial = 14 AND materias_asignadas.Id_hora_final = 15 AND materias_asignadas.Estado = "Activo"',
            5,2,5,3,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 5 AND materias_asignadas.Id_hora_inicial = 14 AND materias_asignadas.Id_hora_final = 16 AND materias_asignadas.Estado = "Activo"',
            5,2,5,4,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 5 AND materias_asignadas.Id_hora_inicial = 14 AND materias_asignadas.Id_hora_final = 17 AND materias_asignadas.Estado = "Activo"',
            5,2,5,5,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 5 AND materias_asignadas.Id_hora_inicial = 14 AND materias_asignadas.Id_hora_final = 18 AND materias_asignadas.Estado = "Activo"',
            5,2,5,6,
            2,self.nocturno
        )

        print('Tercera linea ----------------')

        # Tercera linea lunes
        self.celda1x4(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 1 AND materias_asignadas.Id_hora_inicial = 15 AND materias_asignadas.Id_hora_final = 16 AND materias_asignadas.Estado = "Activo"',
            1,3,1,4,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 1 AND materias_asignadas.Id_hora_inicial = 15 AND materias_asignadas.Id_hora_final = 17 AND materias_asignadas.Estado = "Activo"',
            1,3,1,5,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 1 AND materias_asignadas.Id_hora_inicial = 15 AND materias_asignadas.Id_hora_final = 18 AND materias_asignadas.Estado = "Activo"',
            1,3,1,6,
            3,self.nocturno
        )

        # Tercera linea Martes
        self.celda1x4(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 2 AND materias_asignadas.Id_hora_inicial = 15 AND materias_asignadas.Id_hora_final = 16 AND materias_asignadas.Estado = "Activo"',
            2,3,2,4,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 2 AND materias_asignadas.Id_hora_inicial = 15 AND materias_asignadas.Id_hora_final = 17 AND materias_asignadas.Estado = "Activo"',
            2,3,2,5,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 2 AND materias_asignadas.Id_hora_inicial = 15 AND materias_asignadas.Id_hora_final = 18 AND materias_asignadas.Estado = "Activo"',
            2,3,2,6,
            3,self.nocturno
        )

        # Tercera linea Miercoles
        self.celda1x4(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 3 AND materias_asignadas.Id_hora_inicial = 15 AND materias_asignadas.Id_hora_final = 16 AND materias_asignadas.Estado = "Activo"',
            3,3,3,4,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 3 AND materias_asignadas.Id_hora_inicial = 15 AND materias_asignadas.Id_hora_final = 17 AND materias_asignadas.Estado = "Activo"',
            3,3,3,5,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 3 AND materias_asignadas.Id_hora_inicial = 15 AND materias_asignadas.Id_hora_final = 18 AND materias_asignadas.Estado = "Activo"',
            3,3,3,6,
            3,self.nocturno
        )

        # Tercera linea jueves
        self.celda1x4(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 4 AND materias_asignadas.Id_hora_inicial = 15 AND materias_asignadas.Id_hora_final = 16 AND materias_asignadas.Estado = "Activo"',
            4,3,4,4,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 4 AND materias_asignadas.Id_hora_inicial = 15 AND materias_asignadas.Id_hora_final = 17 AND materias_asignadas.Estado = "Activo"',
            4,3,4,5,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 4 AND materias_asignadas.Id_hora_inicial = 15 AND materias_asignadas.Id_hora_final = 18 AND materias_asignadas.Estado = "Activo"',
            4,3,4,6,
            3,self.nocturno
        )

        # Tercera linea Viernes
        self.celda1x4(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 5 AND materias_asignadas.Id_hora_inicial = 15 AND materias_asignadas.Id_hora_final = 16 AND materias_asignadas.Estado = "Activo"',
            5,3,5,4,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 5 AND materias_asignadas.Id_hora_inicial = 15 AND materias_asignadas.Id_hora_final = 17 AND materias_asignadas.Estado = "Activo"',
            5,3,5,5,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 5 AND materias_asignadas.Id_hora_inicial = 15 AND materias_asignadas.Id_hora_final = 18 AND materias_asignadas.Estado = "Activo"',
            5,3,5,6,
            3,self.nocturno
        )

        print('Cuarta linea ----------------')

        # Cuarta linea lunes
        self.celda1x3(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 1 AND materias_asignadas.Id_hora_inicial = 16 AND materias_asignadas.Id_hora_final = 17 AND materias_asignadas.Estado = "Activo"',
            1,4,1,5,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 1 AND materias_asignadas.Id_hora_inicial = 16 AND materias_asignadas.Id_hora_final = 18 AND materias_asignadas.Estado = "Activo"',
            1,4,1,6,
            4,self.nocturno
        )

        # Cuarta linea Martes
        self.celda1x3(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 2 AND materias_asignadas.Id_hora_inicial = 16 AND materias_asignadas.Id_hora_final = 17 AND materias_asignadas.Estado = "Activo"',
            2,4,2,5,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 2 AND materias_asignadas.Id_hora_inicial = 16 AND materias_asignadas.Id_hora_final = 18 AND materias_asignadas.Estado = "Activo"',
            2,4,2,6,
            4,self.nocturno
        )

        # Cuarta linea Miercoles
        self.celda1x3(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 3 AND materias_asignadas.Id_hora_inicial = 16 AND materias_asignadas.Id_hora_final = 17 AND materias_asignadas.Estado = "Activo"',
            3,4,3,5,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 3 AND materias_asignadas.Id_hora_inicial = 16 AND materias_asignadas.Id_hora_final = 18 AND materias_asignadas.Estado = "Activo"',
            3,4,3,6,
            4,self.nocturno
        )

        # Cuarta linea Jueves
        self.celda1x3(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 4 AND materias_asignadas.Id_hora_inicial = 16 AND materias_asignadas.Id_hora_final = 17 AND materias_asignadas.Estado = "Activo"',
            4,4,4,5,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 4 AND materias_asignadas.Id_hora_inicial = 16 AND materias_asignadas.Id_hora_final = 18 AND materias_asignadas.Estado = "Activo"',
            4,4,4,6,
            4,self.nocturno
        )

        # Cuarta linea Viernes
        self.celda1x3(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 5 AND materias_asignadas.Id_hora_inicial = 16 AND materias_asignadas.Id_hora_final = 17 AND materias_asignadas.Estado = "Activo"',
            5,4,5,5,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 5 AND materias_asignadas.Id_hora_inicial = 16 AND materias_asignadas.Id_hora_final = 18 AND materias_asignadas.Estado = "Activo"',
            5,4,5,6,
            4,self.nocturno
        )

        print('Quinta primera linea ----------------')

        # Quinta primera lunes
        self.celda1x2(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 1 AND materias_asignadas.Id_hora_inicial = 17 AND materias_asignadas.Id_hora_final = 18 AND materias_asignadas.Estado = "Activo"',
            1,5,1,6,
            5,self.nocturno
        )

        # Quinta primera Martes
        self.celda1x2(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 2 AND materias_asignadas.Id_hora_inicial = 17 AND materias_asignadas.Id_hora_final = 18 AND materias_asignadas.Estado = "Activo"',
            2,5,2,6,
            5,self.nocturno
        )

        # Quinta primera Miercoles
        self.celda1x2(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 3 AND materias_asignadas.Id_hora_inicial = 17 AND materias_asignadas.Id_hora_final = 18 AND materias_asignadas.Estado = "Activo"',
            3,5,3,6,
            5,self.nocturno
        )

        # Quinta primera Jueves
        self.celda1x2(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 4 AND materias_asignadas.Id_hora_inicial = 17 AND materias_asignadas.Id_hora_final = 18 AND materias_asignadas.Estado = "Activo"',
            4,5,4,6,
            5,self.nocturno
        )

        # Quinta primera Viernes
        self.celda1x2(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 5 AND materias_asignadas.Id_hora_inicial = 17 AND materias_asignadas.Id_hora_final = 18 AND materias_asignadas.Estado = "Activo"',
            5,5,5,6,
            5,self.nocturno
        )

        return self.nocturno

    def obtenertablaDocenteDiurno(self):
        self.tablaInformacion = [
            [Paragraph('UNIDAD CURRICULAR',self.center),Paragraph('NOMBRE DEL DOCENTE',self.center),Paragraph('TELEFONO DE CONTACTO',self.center)]
        ]
        self.tabla = self.conexion(
            'SELECT DISTINCT unidad_curricular.UnidadCurricular, docente.NombreApellido, docente.Telefono FROM materias_asignadas  INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular INNER JOIN docente ON docente.Id = materias_asignadas.Id_docente  WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Estado = "Activo"',
            self.parametros).fetchall()
        for row in self.tabla:
            self.tablaInformacion.append(row)
            self.counter = self.counter + 1
            print(self.counter)
    
        return self.tablaInformacion

    
    def obtenertablaDocenteNocturno(self):
        self.tablaInformacion = [
            [Paragraph('UNIDAD CURRICULAR',self.center),Paragraph('NOMBRE DEL DOCENTE',self.center),Paragraph('TELEFONO DE CONTACTO',self.center)]
        ]
        self.tabla = self.conexion(
            'SELECT DISTINCT unidad_curricular.UnidadCurricular, docente.NombreApellido, docente.Telefono FROM materias_asignadas  INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular INNER JOIN docente ON docente.Id = materias_asignadas.Id_docente  WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Estado = "Activo"',
            self.parametros).fetchall()
        for row in self.tabla:
            self.tablaInformacion.append(row)
            self.counter = self.counter + 1
            print(self.counter)
        
        return self.tablaInformacion
    
    def obtenerHorarioDiurnoDocente(self):
        self.diurnoDocente = [
            [Paragraph('bloque de horas diurno',self.center),Paragraph('Lunes',self.center),Paragraph('Martes',self.center),Paragraph('Miércoles',self.center),Paragraph('Jueves',self.center),Paragraph('Viernes',self.center)],
            [Paragraph('7:10 - 7:55',self.center)],
            [Paragraph('8:00 - 8:45',self.center)],
            [Paragraph('8:50 - 9:35',self.center)],
            [Paragraph('9:40 - 10:25',self.center)],
            [Paragraph('10:30 - 11:15',self.center)],
            [Paragraph('11:20 - 12:05',self.center)],
            [Paragraph('1:05 - 1:55',self.center)],
            [Paragraph('1:55 - 2:40',self.center)],
            [Paragraph('2:45 - 3:30',self.center)],
            [Paragraph('3:45 - 4:20',self.center)],
            [Paragraph('4:25 - 5:10',self.center)],
            [Paragraph('5:15 - 6:00',self.center)]
        ]
        self.validarSemanaCeldas(self.diurnoDocente,0)
        
        print('Primera linea ----------------')
        # Primera linea lunes
        
        self.celda1x6(
            self.parametrosDocentes,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 1 AND materias_docentes.Id_hora_inicial = 1 AND materias_docentes.Id_hora_final = 2 AND materias_docentes.Estado = "Activo"',
            1,1,1,2,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 1 AND materias_docentes.Id_hora_inicial = 1 AND materias_docentes.Id_hora_final = 3 AND materias_docentes.Estado = "Activo"',
            1,1,1,3,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 1 AND materias_docentes.Id_hora_inicial = 1 AND materias_docentes.Id_hora_final = 4 AND materias_docentes.Estado = "Activo"',
            1,1,1,4,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 1 AND materias_docentes.Id_hora_inicial = 1 AND materias_docentes.Id_hora_final = 5 AND materias_docentes.Estado = "Activo"',
            1,1,1,5,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 1 AND materias_docentes.Id_hora_inicial = 1 AND materias_docentes.Id_hora_final = 6 AND materias_docentes.Estado = "Activo"',
            1,1,1,6,
            1,self.diurnoDocente            
        )
        
        # Primera linea Martes
        self.celda1x6(
            self.parametrosDocentes,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 2 AND materias_docentes.Id_hora_inicial = 1 AND materias_docentes.Id_hora_final = 2 AND materias_docentes.Estado = "Activo"',
            2,1,2,2,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 2 AND materias_docentes.Id_hora_inicial = 1 AND materias_docentes.Id_hora_final = 3 AND materias_docentes.Estado = "Activo"',
            2,1,2,3,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 2 AND materias_docentes.Id_hora_inicial = 1 AND materias_docentes.Id_hora_final = 4 AND materias_docentes.Estado = "Activo"',
            2,1,2,4,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 2 AND materias_docentes.Id_hora_inicial = 1 AND materias_docentes.Id_hora_final = 5 AND materias_docentes.Estado = "Activo"',
            2,1,2,5,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 2 AND materias_docentes.Id_hora_inicial = 1 AND materias_docentes.Id_hora_final = 6 AND materias_docentes.Estado = "Activo"',
            2,1,2,6,
            1,self.diurnoDocente            
        )
        
        # Primera linea Miercoles
        self.celda1x6(
            self.parametrosDocentes,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 3 AND materias_docentes.Id_hora_inicial = 1 AND materias_docentes.Id_hora_final = 2 AND materias_docentes.Estado = "Activo"',
            3,1,3,2,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 3 AND materias_docentes.Id_hora_inicial = 1 AND materias_docentes.Id_hora_final = 3 AND materias_docentes.Estado = "Activo"',
            3,1,3,3,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 3 AND materias_docentes.Id_hora_inicial = 1 AND materias_docentes.Id_hora_final = 4 AND materias_docentes.Estado = "Activo"',
            3,1,3,4,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 3 AND materias_docentes.Id_hora_inicial = 1 AND materias_docentes.Id_hora_final = 5 AND materias_docentes.Estado = "Activo"',
            3,1,3,5,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 3 AND materias_docentes.Id_hora_inicial = 1 AND materias_docentes.Id_hora_final = 6 AND materias_docentes.Estado = "Activo"',
            3,1,3,6,
            1,self.diurnoDocente            
        )
        
        # Primera linea Jueves
        self.celda1x6(
            self.parametrosDocentes,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 4 AND materias_docentes.Id_hora_inicial = 1 AND materias_docentes.Id_hora_final = 2 AND materias_docentes.Estado = "Activo"',
            4,1,4,2,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 4 AND materias_docentes.Id_hora_inicial = 1 AND materias_docentes.Id_hora_final = 3 AND materias_docentes.Estado = "Activo"',
            4,1,4,3,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 4 AND materias_docentes.Id_hora_inicial = 1 AND materias_docentes.Id_hora_final = 4 AND materias_docentes.Estado = "Activo"',
            4,1,4,4,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 4 AND materias_docentes.Id_hora_inicial = 1 AND materias_docentes.Id_hora_final = 5 AND materias_docentes.Estado = "Activo"',
            4,1,4,5,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 4 AND materias_docentes.Id_hora_inicial = 1 AND materias_docentes.Id_hora_final = 6 AND materias_docentes.Estado = "Activo"',
            4,1,4,6,
            1,self.diurnoDocente            
        )
        
        # Primera linea Viernes
        self.celda1x6(
            self.parametrosDocentes,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 5 AND materias_docentes.Id_hora_inicial = 1 AND materias_docentes.Id_hora_final = 2 AND materias_docentes.Estado = "Activo"',
            5,1,5,2,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 5 AND materias_docentes.Id_hora_inicial = 1 AND materias_docentes.Id_hora_final = 3 AND materias_docentes.Estado = "Activo"',
            5,1,5,3,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 5 AND materias_docentes.Id_hora_inicial = 1 AND materias_docentes.Id_hora_final = 4 AND materias_docentes.Estado = "Activo"',
            5,1,5,4,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 5 AND materias_docentes.Id_hora_inicial = 1 AND materias_docentes.Id_hora_final = 5 AND materias_docentes.Estado = "Activo"',
            5,1,5,5,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 5 AND materias_docentes.Id_hora_inicial = 1 AND materias_docentes.Id_hora_final = 6 AND materias_docentes.Estado = "Activo"',
            5,1,5,6,
            1,self.diurnoDocente            
        )
        
        print('Segunda linea ----------------')
        
        # Segunda linea lunes
        self.celda1x5(
            self.parametrosDocentes,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 1 AND materias_docentes.Id_hora_inicial = 2 AND materias_docentes.Id_hora_final = 3 AND materias_docentes.Estado = "Activo"',
            1,2,1,3,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 1 AND materias_docentes.Id_hora_inicial = 2 AND materias_docentes.Id_hora_final = 4 AND materias_docentes.Estado = "Activo"',
            1,2,1,4,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 1 AND materias_docentes.Id_hora_inicial = 2 AND materias_docentes.Id_hora_final = 5 AND materias_docentes.Estado = "Activo"',
            1,2,1,5,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 1 AND materias_docentes.Id_hora_inicial = 2 AND materias_docentes.Id_hora_final = 6 AND materias_docentes.Estado = "Activo"',
            1,2,1,6,
            2,self.diurnoDocente        
        )
        
        # Segunda linea Martes
        self.celda1x5(
            self.parametrosDocentes,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 2 AND materias_docentes.Id_hora_inicial = 2 AND materias_docentes.Id_hora_final = 3 AND materias_docentes.Estado = "Activo"',
            2,2,2,3,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 2 AND materias_docentes.Id_hora_inicial = 2 AND materias_docentes.Id_hora_final = 4 AND materias_docentes.Estado = "Activo"',
            2,2,2,4,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 2 AND materias_docentes.Id_hora_inicial = 2 AND materias_docentes.Id_hora_final = 5 AND materias_docentes.Estado = "Activo"',
            2,2,2,5,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 2 AND materias_docentes.Id_hora_inicial = 2 AND materias_docentes.Id_hora_final = 6 AND materias_docentes.Estado = "Activo"',
            2,2,2,6,
            2,self.diurnoDocente        
        )
        
        # Segunda linea Miercoles
        self.celda1x5(
            self.parametrosDocentes,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 3 AND materias_docentes.Id_hora_inicial = 2 AND materias_docentes.Id_hora_final = 3 AND materias_docentes.Estado = "Activo"',
            3,2,3,3,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 3 AND materias_docentes.Id_hora_inicial = 2 AND materias_docentes.Id_hora_final = 4 AND materias_docentes.Estado = "Activo"',
            3,2,3,4,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 3 AND materias_docentes.Id_hora_inicial = 2 AND materias_docentes.Id_hora_final = 5 AND materias_docentes.Estado = "Activo"',
            3,2,3,5,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 3 AND materias_docentes.Id_hora_inicial = 2 AND materias_docentes.Id_hora_final = 6 AND materias_docentes.Estado = "Activo"',
            3,2,3,6,
            2,self.diurnoDocente        
        )
        
        # Segunda linea Jueves
        self.celda1x5(
            self.parametrosDocentes,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 4 AND materias_docentes.Id_hora_inicial = 2 AND materias_docentes.Id_hora_final = 3 AND materias_docentes.Estado = "Activo"',
            4,2,4,3,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 4 AND materias_docentes.Id_hora_inicial = 2 AND materias_docentes.Id_hora_final = 4 AND materias_docentes.Estado = "Activo"',
            4,2,4,4,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 4 AND materias_docentes.Id_hora_inicial = 2 AND materias_docentes.Id_hora_final = 5 AND materias_docentes.Estado = "Activo"',
            4,2,4,5,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 4 AND materias_docentes.Id_hora_inicial = 2 AND materias_docentes.Id_hora_final = 6 AND materias_docentes.Estado = "Activo"',
            4,2,4,6,
            2,self.diurnoDocente        
        )
        
        # Segunda linea Viernes
        self.celda1x5(
            self.parametrosDocentes,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 5 AND materias_docentes.Id_hora_inicial = 2 AND materias_docentes.Id_hora_final = 3 AND materias_docentes.Estado = "Activo"',
            5,2,5,3,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 5 AND materias_docentes.Id_hora_inicial = 2 AND materias_docentes.Id_hora_final = 4 AND materias_docentes.Estado = "Activo"',
            5,2,5,4,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 5 AND materias_docentes.Id_hora_inicial = 2 AND materias_docentes.Id_hora_final = 5 AND materias_docentes.Estado = "Activo"',
            5,2,5,5,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 5 AND materias_docentes.Id_hora_inicial = 2 AND materias_docentes.Id_hora_final = 6 AND materias_docentes.Estado = "Activo"',
            5,2,5,6,
            2,self.diurnoDocente        
        )
        
        print('Tercera linea ----------------')
        
        # Tercera linea lunes
        self.celda1x4(
            self.parametrosDocentes,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 1 AND materias_docentes.Id_hora_inicial = 3 AND materias_docentes.Id_hora_final = 4 AND materias_docentes.Estado = "Activo"',
            1,3,1,4,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 1 AND materias_docentes.Id_hora_inicial = 3 AND materias_docentes.Id_hora_final = 5 AND materias_docentes.Estado = "Activo"',
            1,3,1,5,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 1 AND materias_docentes.Id_hora_inicial = 3 AND materias_docentes.Id_hora_final = 6 AND materias_docentes.Estado = "Activo"',
            1,3,1,6,
            3,self.diurnoDocente        
        )
        
        # Tercera linea Martes
        self.celda1x4(
            self.parametrosDocentes,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 2 AND materias_docentes.Id_hora_inicial = 3 AND materias_docentes.Id_hora_final = 4 AND materias_docentes.Estado = "Activo"',
            2,3,2,4,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 2 AND materias_docentes.Id_hora_inicial = 3 AND materias_docentes.Id_hora_final = 5 AND materias_docentes.Estado = "Activo"',
            2,3,2,5,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 2 AND materias_docentes.Id_hora_inicial = 3 AND materias_docentes.Id_hora_final = 6 AND materias_docentes.Estado = "Activo"',
            2,3,2,6,
            3,self.diurnoDocente        
        )
        
        # Tercera linea Miercoles
        self.celda1x4(
            self.parametrosDocentes,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 3 AND materias_docentes.Id_hora_inicial = 3 AND materias_docentes.Id_hora_final = 4 AND materias_docentes.Estado = "Activo"',
            3,3,3,4,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 3 AND materias_docentes.Id_hora_inicial = 3 AND materias_docentes.Id_hora_final = 5 AND materias_docentes.Estado = "Activo"',
            3,3,3,5,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 3 AND materias_docentes.Id_hora_inicial = 3 AND materias_docentes.Id_hora_final = 6 AND materias_docentes.Estado = "Activo"',
            3,3,3,6,
            3,self.diurnoDocente        
        )
        
        # Tercera linea Jueves
        self.celda1x4(
            self.parametrosDocentes,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 4 AND materias_docentes.Id_hora_inicial = 3 AND materias_docentes.Id_hora_final = 4 AND materias_docentes.Estado = "Activo"',
            4,3,4,4,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 4 AND materias_docentes.Id_hora_inicial = 3 AND materias_docentes.Id_hora_final = 5 AND materias_docentes.Estado = "Activo"',
            4,3,4,5,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 4 AND materias_docentes.Id_hora_inicial = 3 AND materias_docentes.Id_hora_final = 6 AND materias_docentes.Estado = "Activo"',
            4,3,4,6,
            3,self.diurnoDocente        
        )
        
        # Tercera linea Viernes
        self.celda1x4(
            self.parametrosDocentes,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 5 AND materias_docentes.Id_hora_inicial = 3 AND materias_docentes.Id_hora_final = 4 AND materias_docentes.Estado = "Activo"',
            5,3,5,4,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 5 AND materias_docentes.Id_hora_inicial = 3 AND materias_docentes.Id_hora_final = 5 AND materias_docentes.Estado = "Activo"',
            5,3,5,5,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 5 AND materias_docentes.Id_hora_inicial = 3 AND materias_docentes.Id_hora_final = 6 AND materias_docentes.Estado = "Activo"',
            5,3,5,6,
            3,self.diurnoDocente        
        )
        
        print('Cuarta linea ----------------')
        
        #  Cuarta linea lunes
        self.celda1x3(
            self.parametrosDocentes,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 1 AND materias_docentes.Id_hora_inicial = 4 AND materias_docentes.Id_hora_final = 5 AND materias_docentes.Estado = "Activo"',
            1,4,1,5,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 1 AND materias_docentes.Id_hora_inicial = 4 AND materias_docentes.Id_hora_final = 6 AND materias_docentes.Estado = "Activo"',
            1,4,1,6,
            4,self.diurnoDocente        
        )
        
        #  Cuarta linea Martes
        self.celda1x3(
            self.parametrosDocentes,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 2 AND materias_docentes.Id_hora_inicial = 4 AND materias_docentes.Id_hora_final = 5 AND materias_docentes.Estado = "Activo"',
            2,4,2,5,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 2 AND materias_docentes.Id_hora_inicial = 4 AND materias_docentes.Id_hora_final = 6 AND materias_docentes.Estado = "Activo"',
            2,4,2,6,
            4,self.diurnoDocente        
        )
        
        #  Cuarta linea Miercoles
        self.celda1x3(
            self.parametrosDocentes,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 3 AND materias_docentes.Id_hora_inicial = 4 AND materias_docentes.Id_hora_final = 5 AND materias_docentes.Estado = "Activo"',
            3,4,3,5,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 3 AND materias_docentes.Id_hora_inicial = 4 AND materias_docentes.Id_hora_final = 6 AND materias_docentes.Estado = "Activo"',
            3,4,3,6,
            4,self.diurnoDocente        
        )
        
        #  Cuarta linea Jueves
        self.celda1x3(
            self.parametrosDocentes,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 4 AND materias_docentes.Id_hora_inicial = 4 AND materias_docentes.Id_hora_final = 5 AND materias_docentes.Estado = "Activo"',
            4,4,4,5,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 4 AND materias_docentes.Id_hora_inicial = 4 AND materias_docentes.Id_hora_final = 6 AND materias_docentes.Estado = "Activo"',
            4,4,4,6,
            4,self.diurnoDocente        
        )
        
        #  Cuarta linea Viernes
        self.celda1x3(
            self.parametrosDocentes,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 5 AND materias_docentes.Id_hora_inicial = 4 AND materias_docentes.Id_hora_final = 5 AND materias_docentes.Estado = "Activo"',
            5,4,5,5,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 5 AND materias_docentes.Id_hora_inicial = 4 AND materias_docentes.Id_hora_final = 6 AND materias_docentes.Estado = "Activo"',
            5,4,5,6,
            4,self.diurnoDocente        
        )
        
        print('Quinta linea ----------------')
        
        #  Quinta linea lunes
        self.celda1x2(
            self.parametrosDocentes,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 1 AND materias_docentes.Id_hora_inicial = 5 AND materias_docentes.Id_hora_final = 6 AND materias_docentes.Estado = "Activo"',
            1,5,1,6,
            5,self.diurnoDocente        
        )
        
        #  Quinta linea Martes
        self.celda1x2(
            self.parametrosDocentes,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 1 AND materias_docentes.Id_hora_inicial = 5 AND materias_docentes.Id_hora_final = 6 AND materias_docentes.Estado = "Activo"',
            2,5,2,6,
            5,self.diurnoDocente        
        )
        
        #  Quinta linea Miercoles
        self.celda1x2(
            self.parametrosDocentes,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 1 AND materias_docentes.Id_hora_inicial = 5 AND materias_docentes.Id_hora_final = 6 AND materias_docentes.Estado = "Activo"',
            3,5,3,6,
            5,self.diurnoDocente        
        )
        
        #  Quinta linea Jueves
        self.celda1x2(
            self.parametrosDocentes,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 1 AND materias_docentes.Id_hora_inicial = 5 AND materias_docentes.Id_hora_final = 6 AND materias_docentes.Estado = "Activo"',
            4,5,4,6,
            5,self.diurnoDocente        
        )
        
        #  Quinta linea Viernes
        self.celda1x2(
            self.parametrosDocentes,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 1 AND materias_docentes.Id_hora_inicial = 5 AND materias_docentes.Id_hora_final = 6 AND materias_docentes.Estado = "Activo"',
            5,5,5,6,
            5,self.diurnoDocente        
        )
        
        print('Septima linea ----------------')
        # Septima linea lunes
        
        self.celda1x6(
            self.parametrosDocentes,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 1 AND materias_docentes.Id_hora_inicial = 7 AND materias_docentes.Id_hora_final = 8 AND materias_docentes.Estado = "Activo"',
            1,7,1,8,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 1 AND materias_docentes.Id_hora_inicial = 7 AND materias_docentes.Id_hora_final = 9 AND materias_docentes.Estado = "Activo"',
            1,7,1,9,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 1 AND materias_docentes.Id_hora_inicial = 7 AND materias_docentes.Id_hora_final = 10 AND materias_docentes.Estado = "Activo"',
            1,7,1,10,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 1 AND materias_docentes.Id_hora_inicial = 7 AND materias_docentes.Id_hora_final = 11 AND materias_docentes.Estado = "Activo"',
            1,7,1,11,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 1 AND materias_docentes.Id_hora_inicial = 7 AND materias_docentes.Id_hora_final = 12 AND materias_docentes.Estado = "Activo"',
            1,7,1,12,
            7,self.diurnoDocente            
        )
        
        # Septima linea Martes
        
        self.celda1x6(
            self.parametrosDocentes,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 2 AND materias_docentes.Id_hora_inicial = 7 AND materias_docentes.Id_hora_final = 8 AND materias_docentes.Estado = "Activo"',
            2,7,2,8,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 2 AND materias_docentes.Id_hora_inicial = 7 AND materias_docentes.Id_hora_final = 9 AND materias_docentes.Estado = "Activo"',
            2,7,2,9,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 2 AND materias_docentes.Id_hora_inicial = 7 AND materias_docentes.Id_hora_final = 10 AND materias_docentes.Estado = "Activo"',
            2,7,2,10,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 2 AND materias_docentes.Id_hora_inicial = 7 AND materias_docentes.Id_hora_final = 11 AND materias_docentes.Estado = "Activo"',
            2,7,2,11,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 2 AND materias_docentes.Id_hora_inicial = 7 AND materias_docentes.Id_hora_final = 12 AND materias_docentes.Estado = "Activo"',
            2,7,2,12,
            7,self.diurnoDocente            
        )
        
        # Septima linea Miercoles
        
        self.celda1x6(
            self.parametrosDocentes,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 3 AND materias_docentes.Id_hora_inicial = 7 AND materias_docentes.Id_hora_final = 8 AND materias_docentes.Estado = "Activo"',
            3,7,3,8,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 3 AND materias_docentes.Id_hora_inicial = 7 AND materias_docentes.Id_hora_final = 9 AND materias_docentes.Estado = "Activo"',
            3,7,3,9,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 3 AND materias_docentes.Id_hora_inicial = 7 AND materias_docentes.Id_hora_final = 10 AND materias_docentes.Estado = "Activo"',
            3,7,3,10,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 3 AND materias_docentes.Id_hora_inicial = 7 AND materias_docentes.Id_hora_final = 11 AND materias_docentes.Estado = "Activo"',
            3,7,3,11,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 3 AND materias_docentes.Id_hora_inicial = 7 AND materias_docentes.Id_hora_final = 12 AND materias_docentes.Estado = "Activo"',
            3,7,3,12,
            7,self.diurnoDocente            
        )
        
        # Septima linea Jueves
        
        self.celda1x6(
            self.parametrosDocentes,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 4 AND materias_docentes.Id_hora_inicial = 7 AND materias_docentes.Id_hora_final = 8 AND materias_docentes.Estado = "Activo"',
            4,7,4,8,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 4 AND materias_docentes.Id_hora_inicial = 7 AND materias_docentes.Id_hora_final = 9 AND materias_docentes.Estado = "Activo"',
            4,7,4,9,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 4 AND materias_docentes.Id_hora_inicial = 7 AND materias_docentes.Id_hora_final = 10 AND materias_docentes.Estado = "Activo"',
            4,7,4,10,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 4 AND materias_docentes.Id_hora_inicial = 7 AND materias_docentes.Id_hora_final = 11 AND materias_docentes.Estado = "Activo"',
            4,7,4,11,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 4 AND materias_docentes.Id_hora_inicial = 7 AND materias_docentes.Id_hora_final = 12 AND materias_docentes.Estado = "Activo"',
            4,7,4,12,
            7,self.diurnoDocente            
        )
        # Septima linea Viernes
        
        self.celda1x6(
            self.parametrosDocentes,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 5 AND materias_docentes.Id_hora_inicial = 7 AND materias_docentes.Id_hora_final = 8 AND materias_docentes.Estado = "Activo"',
            5,7,5,8,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 5 AND materias_docentes.Id_hora_inicial = 7 AND materias_docentes.Id_hora_final = 9 AND materias_docentes.Estado = "Activo"',
            5,7,5,9,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 5 AND materias_docentes.Id_hora_inicial = 7 AND materias_docentes.Id_hora_final = 10 AND materias_docentes.Estado = "Activo"',
            5,7,5,10,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 5 AND materias_docentes.Id_hora_inicial = 7 AND materias_docentes.Id_hora_final = 11 AND materias_docentes.Estado = "Activo"',
            5,7,5,11,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 5 AND materias_docentes.Id_hora_inicial = 7 AND materias_docentes.Id_hora_final = 12 AND materias_docentes.Estado = "Activo"',
            5,7,5,12,
            7,self.diurnoDocente            
        )
        
        print('Octava linea ----------------')
        # Octava linea lunes
        
        self.celda1x5(
            self.parametrosDocentes,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 1 AND materias_docentes.Id_hora_inicial = 8 AND materias_docentes.Id_hora_final = 9 AND materias_docentes.Estado = "Activo"',
            1,8,1,9,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 1 AND materias_docentes.Id_hora_inicial = 8 AND materias_docentes.Id_hora_final = 10 AND materias_docentes.Estado = "Activo"',
            1,8,1,10,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 1 AND materias_docentes.Id_hora_inicial = 8 AND materias_docentes.Id_hora_final = 11 AND materias_docentes.Estado = "Activo"',
            1,8,1,11,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 1 AND materias_docentes.Id_hora_inicial = 8 AND materias_docentes.Id_hora_final = 12 AND materias_docentes.Estado = "Activo"',
            1,8,1,12,
            8,self.diurnoDocente            
        )
        
        # Octava linea Martes
        
        self.celda1x5(
            self.parametrosDocentes,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 2 AND materias_docentes.Id_hora_inicial = 8 AND materias_docentes.Id_hora_final = 9 AND materias_docentes.Estado = "Activo"',
            2,8,2,9,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 2 AND materias_docentes.Id_hora_inicial = 8 AND materias_docentes.Id_hora_final = 10 AND materias_docentes.Estado = "Activo"',
            2,8,2,10,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 2 AND materias_docentes.Id_hora_inicial = 8 AND materias_docentes.Id_hora_final = 11 AND materias_docentes.Estado = "Activo"',
            2,8,2,11,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 2 AND materias_docentes.Id_hora_inicial = 8 AND materias_docentes.Id_hora_final = 12 AND materias_docentes.Estado = "Activo"',
            2,8,2,12,
            8,self.diurnoDocente            
        )
        
        # Octava linea Miercoles
        
        self.celda1x5(
            self.parametrosDocentes,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 3 AND materias_docentes.Id_hora_inicial = 8 AND materias_docentes.Id_hora_final = 9 AND materias_docentes.Estado = "Activo"',
            3,8,3,9,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 3 AND materias_docentes.Id_hora_inicial = 8 AND materias_docentes.Id_hora_final = 10 AND materias_docentes.Estado = "Activo"',
            3,8,3,10,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 3 AND materias_docentes.Id_hora_inicial = 8 AND materias_docentes.Id_hora_final = 11 AND materias_docentes.Estado = "Activo"',
            3,8,3,11,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 3 AND materias_docentes.Id_hora_inicial = 8 AND materias_docentes.Id_hora_final = 12 AND materias_docentes.Estado = "Activo"',
            3,8,3,12,
            8,self.diurnoDocente            
        )
        
        # Octava linea Jueves
        
        self.celda1x5(
            self.parametrosDocentes,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 4 AND materias_docentes.Id_hora_inicial = 8 AND materias_docentes.Id_hora_final = 9 AND materias_docentes.Estado = "Activo"',
            4,8,4,9,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 4 AND materias_docentes.Id_hora_inicial = 8 AND materias_docentes.Id_hora_final = 10 AND materias_docentes.Estado = "Activo"',
            4,8,4,10,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 4 AND materias_docentes.Id_hora_inicial = 8 AND materias_docentes.Id_hora_final = 11 AND materias_docentes.Estado = "Activo"',
            4,8,4,11,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 4 AND materias_docentes.Id_hora_inicial = 8 AND materias_docentes.Id_hora_final = 12 AND materias_docentes.Estado = "Activo"',
            4,8,4,12,
            8,self.diurnoDocente            
        )
        
        # Octava linea Viernes
        
        self.celda1x5(
            self.parametrosDocentes,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 5 AND materias_docentes.Id_hora_inicial = 8 AND materias_docentes.Id_hora_final = 9 AND materias_docentes.Estado = "Activo"',
            5,8,5,9,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 5 AND materias_docentes.Id_hora_inicial = 8 AND materias_docentes.Id_hora_final = 10 AND materias_docentes.Estado = "Activo"',
            5,8,5,10,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 5 AND materias_docentes.Id_hora_inicial = 8 AND materias_docentes.Id_hora_final = 11 AND materias_docentes.Estado = "Activo"',
            5,8,5,11,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 5 AND materias_docentes.Id_hora_inicial = 8 AND materias_docentes.Id_hora_final = 12 AND materias_docentes.Estado = "Activo"',
            5,8,5,12,
            8,self.diurnoDocente            
        )
        
        print('Novena linea ----------------')
        # Novena linea lunes
        
        self.celda1x4(
            self.parametrosDocentes,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 1 AND materias_docentes.Id_hora_inicial = 9 AND materias_docentes.Id_hora_final = 10 AND materias_docentes.Estado = "Activo"',
            1,9,1,10,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 1 AND materias_docentes.Id_hora_inicial = 9 AND materias_docentes.Id_hora_final = 11 AND materias_docentes.Estado = "Activo"',
            1,9,1,11,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 1 AND materias_docentes.Id_hora_inicial = 9 AND materias_docentes.Id_hora_final = 12 AND materias_docentes.Estado = "Activo"',
            1,9,1,12,
            9,self.diurnoDocente            
        )
        
        # Novena linea Martes
        
        self.celda1x4(
            self.parametrosDocentes,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 2 AND materias_docentes.Id_hora_inicial = 9 AND materias_docentes.Id_hora_final = 10 AND materias_docentes.Estado = "Activo"',
            2,9,2,10,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 2 AND materias_docentes.Id_hora_inicial = 9 AND materias_docentes.Id_hora_final = 11 AND materias_docentes.Estado = "Activo"',
            2,9,2,11,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 2 AND materias_docentes.Id_hora_inicial = 9 AND materias_docentes.Id_hora_final = 12 AND materias_docentes.Estado = "Activo"',
            2,9,2,12,
            9,self.diurnoDocente            
        )
        
        # Novena linea Miercoles
        
        self.celda1x4(
            self.parametrosDocentes,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 3 AND materias_docentes.Id_hora_inicial = 9 AND materias_docentes.Id_hora_final = 10 AND materias_docentes.Estado = "Activo"',
            3,9,3,10,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 3 AND materias_docentes.Id_hora_inicial = 9 AND materias_docentes.Id_hora_final = 11 AND materias_docentes.Estado = "Activo"',
            3,9,3,11,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 3 AND materias_docentes.Id_hora_inicial = 9 AND materias_docentes.Id_hora_final = 12 AND materias_docentes.Estado = "Activo"',
            3,9,3,12,
            9,self.diurnoDocente            
        )
        
        # Novena linea Jueves
        
        self.celda1x4(
            self.parametrosDocentes,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 4 AND materias_docentes.Id_hora_inicial = 9 AND materias_docentes.Id_hora_final = 10 AND materias_docentes.Estado = "Activo"',
            4,9,4,10,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 4 AND materias_docentes.Id_hora_inicial = 9 AND materias_docentes.Id_hora_final = 11 AND materias_docentes.Estado = "Activo"',
            4,9,4,11,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 4 AND materias_docentes.Id_hora_inicial = 9 AND materias_docentes.Id_hora_final = 12 AND materias_docentes.Estado = "Activo"',
            4,9,4,12,
            9,self.diurnoDocente            
        )
        
        # Novena linea Viernes
        
        self.celda1x4(
            self.parametrosDocentes,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 5 AND materias_docentes.Id_hora_inicial = 9 AND materias_docentes.Id_hora_final = 10 AND materias_docentes.Estado = "Activo"',
            5,9,5,10,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 5 AND materias_docentes.Id_hora_inicial = 9 AND materias_docentes.Id_hora_final = 11 AND materias_docentes.Estado = "Activo"',
            5,9,5,11,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 5 AND materias_docentes.Id_hora_inicial = 9 AND materias_docentes.Id_hora_final = 12 AND materias_docentes.Estado = "Activo"',
            5,9,5,12,
            9,self.diurnoDocente            
        )
        
        
        print('Decima linea ----------------')
        # Decima linea lunes
        
        self.celda1x3(
            self.parametrosDocentes,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 1 AND materias_docentes.Id_hora_inicial = 10 AND materias_docentes.Id_hora_final = 11 AND materias_docentes.Estado = "Activo"',
            1,10,1,11,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 1 AND materias_docentes.Id_hora_inicial = 10 AND materias_docentes.Id_hora_final = 12 AND materias_docentes.Estado = "Activo"',
            1,10,1,12,
            10,self.diurnoDocente            
        )
        
        # Decima linea Martes
        
        self.celda1x3(
            self.parametrosDocentes,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 2 AND materias_docentes.Id_hora_inicial = 10 AND materias_docentes.Id_hora_final = 11 AND materias_docentes.Estado = "Activo"',
            2,10,2,11,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 2 AND materias_docentes.Id_hora_inicial = 10 AND materias_docentes.Id_hora_final = 12 AND materias_docentes.Estado = "Activo"',
            2,10,2,12,
            10,self.diurnoDocente            
        )
        
        # Decima linea Miercoles
        
        self.celda1x3(
            self.parametrosDocentes,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 3 AND materias_docentes.Id_hora_inicial = 10 AND materias_docentes.Id_hora_final = 11 AND materias_docentes.Estado = "Activo"',
            3,10,3,11,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 3 AND materias_docentes.Id_hora_inicial = 10 AND materias_docentes.Id_hora_final = 12 AND materias_docentes.Estado = "Activo"',
            3,10,3,12,
            10,self.diurnoDocente            
        )
        
        # Decima linea Jueves
        
        self.celda1x3(
            self.parametrosDocentes,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 4 AND materias_docentes.Id_hora_inicial = 10 AND materias_docentes.Id_hora_final = 11 AND materias_docentes.Estado = "Activo"',
            4,10,4,11,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 4 AND materias_docentes.Id_hora_inicial = 10 AND materias_docentes.Id_hora_final = 12 AND materias_docentes.Estado = "Activo"',
            4,10,4,12,
            10,self.diurnoDocente            
        )
        
        # Decima linea Viernes
        
        self.celda1x3(
            self.parametrosDocentes,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 5 AND materias_docentes.Id_hora_inicial = 10 AND materias_docentes.Id_hora_final = 11 AND materias_docentes.Estado = "Activo"',
            5,10,5,11,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 5 AND materias_docentes.Id_hora_inicial = 10 AND materias_docentes.Id_hora_final = 12 AND materias_docentes.Estado = "Activo"',
            5,10,5,12,
            10,self.diurnoDocente            
        )
        
        print('Decima primera linea ----------------')
        # Decima primera linea lunes
        
        self.celda1x2(
            self.parametrosDocentes,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 1 AND materias_docentes.Id_hora_inicial = 11 AND materias_docentes.Id_hora_final = 12 AND materias_docentes.Estado = "Activo"',
            1,11,1,12,
            11,self.diurnoDocente            
        )
        
        # Decima primera linea Martes
        
        self.celda1x2(
            self.parametrosDocentes,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 2 AND materias_docentes.Id_hora_inicial = 11 AND materias_docentes.Id_hora_final = 12 AND materias_docentes.Estado = "Activo"',
            2,11,2,12,
            11,self.diurnoDocente            
        )
        
        # Decima primera linea Miercoles
        
        self.celda1x2(
            self.parametrosDocentes,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 3 AND materias_docentes.Id_hora_inicial = 11 AND materias_docentes.Id_hora_final = 12 AND materias_docentes.Estado = "Activo"',
            3,11,3,12,
            11,self.diurnoDocente            
        )
        
        # Decima primera linea Jueves
        
        self.celda1x2(
            self.parametrosDocentes,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 4 AND materias_docentes.Id_hora_inicial = 11 AND materias_docentes.Id_hora_final = 12 AND materias_docentes.Estado = "Activo"',
            4,11,4,12,
            11,self.diurnoDocente            
        )
        
        # Decima primera linea Viernes
        
        self.celda1x2(
            self.parametrosDocentes,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 5 AND materias_docentes.Id_hora_inicial = 11 AND materias_docentes.Id_hora_final = 12 AND materias_docentes.Estado = "Activo"',
            5,11,5,12,
            11,self.diurnoDocente            
        )
        
        return self.diurnoDocente
    
    def obtenerHorarioNocturnoDocente(self):
        self.nocturnoDocente = [
            [Paragraph('bloque de horas noche',self.center),Paragraph('Lunes',self.center),Paragraph('Martes',self.center),Paragraph('Miércoles',self.center),Paragraph('Jueves',self.center),Paragraph('Viernes',self.center)],
            [Paragraph('6:00 - 6:45',self.center)],
            [Paragraph('6:45 - 7:30',self.center)],
            [Paragraph('7:35 - 8:20',self.center)],
            [Paragraph('8:20 - 9:05',self.center)],
            [Paragraph('9:05 - 9:50',self.center)],
            [Paragraph('9:50 - 10:35',self.center)]
        ]
        self.validarSemanaCeldas(self.nocturnoDocente,0)
        
        print('Primera linea ----------------')
        # Primera linea lunes
        
        self.celda1x6(
            self.parametrosDocentes,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 1 AND materias_docentes.Id_hora_inicial = 13 AND materias_docentes.Id_hora_final = 14 AND materias_docentes.Estado = "Activo"',
            1,1,1,2,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 1 AND materias_docentes.Id_hora_inicial = 13 AND materias_docentes.Id_hora_final = 15 AND materias_docentes.Estado = "Activo"',
            1,1,1,3,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 1 AND materias_docentes.Id_hora_inicial = 13 AND materias_docentes.Id_hora_final = 16 AND materias_docentes.Estado = "Activo"',
            1,1,1,4,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 1 AND materias_docentes.Id_hora_inicial = 13 AND materias_docentes.Id_hora_final = 17 AND materias_docentes.Estado = "Activo"',
            1,1,1,5,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 1 AND materias_docentes.Id_hora_inicial = 13 AND materias_docentes.Id_hora_final = 18 AND materias_docentes.Estado = "Activo"',
            1,1,1,6,
            1,self.nocturnoDocente          
        )
        
        # Primera linea Martes
        
        self.celda1x6(
            self.parametrosDocentes,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 2 AND materias_docentes.Id_hora_inicial = 13 AND materias_docentes.Id_hora_final = 14 AND materias_docentes.Estado = "Activo"',
            2,1,2,2,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 2 AND materias_docentes.Id_hora_inicial = 13 AND materias_docentes.Id_hora_final = 15 AND materias_docentes.Estado = "Activo"',
            2,1,2,3,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 2 AND materias_docentes.Id_hora_inicial = 13 AND materias_docentes.Id_hora_final = 16 AND materias_docentes.Estado = "Activo"',
            2,1,2,4,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 2 AND materias_docentes.Id_hora_inicial = 13 AND materias_docentes.Id_hora_final = 17 AND materias_docentes.Estado = "Activo"',
            2,1,2,5,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 2 AND materias_docentes.Id_hora_inicial = 13 AND materias_docentes.Id_hora_final = 18 AND materias_docentes.Estado = "Activo"',
            2,1,2,6,
            1,self.nocturnoDocente          
        )
        
        # Primera linea Miercoles
        
        self.celda1x6(
            self.parametrosDocentes,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 3 AND materias_docentes.Id_hora_inicial = 13 AND materias_docentes.Id_hora_final = 14 AND materias_docentes.Estado = "Activo"',
            3,1,3,2,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 3 AND materias_docentes.Id_hora_inicial = 13 AND materias_docentes.Id_hora_final = 15 AND materias_docentes.Estado = "Activo"',
            3,1,3,3,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 3 AND materias_docentes.Id_hora_inicial = 13 AND materias_docentes.Id_hora_final = 16 AND materias_docentes.Estado = "Activo"',
            3,1,3,4,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 3 AND materias_docentes.Id_hora_inicial = 13 AND materias_docentes.Id_hora_final = 17 AND materias_docentes.Estado = "Activo"',
            3,1,3,5,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 3 AND materias_docentes.Id_hora_inicial = 13 AND materias_docentes.Id_hora_final = 18 AND materias_docentes.Estado = "Activo"',
            3,1,3,6,
            1,self.nocturnoDocente          
        )
        
        # Primera linea Jueves
        
        self.celda1x6(
            self.parametrosDocentes,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 4 AND materias_docentes.Id_hora_inicial = 13 AND materias_docentes.Id_hora_final = 14 AND materias_docentes.Estado = "Activo"',
            4,1,4,2,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 4 AND materias_docentes.Id_hora_inicial = 13 AND materias_docentes.Id_hora_final = 15 AND materias_docentes.Estado = "Activo"',
            4,1,4,3,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 4 AND materias_docentes.Id_hora_inicial = 13 AND materias_docentes.Id_hora_final = 16 AND materias_docentes.Estado = "Activo"',
            4,1,4,4,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 4 AND materias_docentes.Id_hora_inicial = 13 AND materias_docentes.Id_hora_final = 17 AND materias_docentes.Estado = "Activo"',
            4,1,4,5,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 4 AND materias_docentes.Id_hora_inicial = 13 AND materias_docentes.Id_hora_final = 18 AND materias_docentes.Estado = "Activo"',
            4,1,4,6,
            1,self.nocturnoDocente          
        )
        
        # Primera linea Viernes
        
        self.celda1x6(
            self.parametrosDocentes,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 5 AND materias_docentes.Id_hora_inicial = 13 AND materias_docentes.Id_hora_final = 14 AND materias_docentes.Estado = "Activo"',
            5,1,5,2,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 5 AND materias_docentes.Id_hora_inicial = 13 AND materias_docentes.Id_hora_final = 15 AND materias_docentes.Estado = "Activo"',
            5,1,5,3,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 5 AND materias_docentes.Id_hora_inicial = 13 AND materias_docentes.Id_hora_final = 16 AND materias_docentes.Estado = "Activo"',
            5,1,5,4,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 5 AND materias_docentes.Id_hora_inicial = 13 AND materias_docentes.Id_hora_final = 17 AND materias_docentes.Estado = "Activo"',
            5,1,5,5,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 5 AND materias_docentes.Id_hora_inicial = 13 AND materias_docentes.Id_hora_final = 18 AND materias_docentes.Estado = "Activo"',
            5,1,5,6,
            1,self.nocturnoDocente          
        )
        
        print('Segunda linea ----------------')
        # Segunda linea lunes
        
        self.celda1x5(
            self.parametrosDocentes,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 1 AND materias_docentes.Id_hora_inicial = 14 AND materias_docentes.Id_hora_final = 15 AND materias_docentes.Estado = "Activo"',
            1,2,1,3,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 1 AND materias_docentes.Id_hora_inicial = 14 AND materias_docentes.Id_hora_final = 16 AND materias_docentes.Estado = "Activo"',
            1,2,1,4,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 1 AND materias_docentes.Id_hora_inicial = 14 AND materias_docentes.Id_hora_final = 17 AND materias_docentes.Estado = "Activo"',
            1,2,1,5,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 1 AND materias_docentes.Id_hora_inicial = 14 AND materias_docentes.Id_hora_final = 18 AND materias_docentes.Estado = "Activo"',
            1,2,1,6,
            2,self.nocturnoDocente          
        )
        
        # Segunda linea Martes
        
        self.celda1x5(
            self.parametrosDocentes,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 2 AND materias_docentes.Id_hora_inicial = 14 AND materias_docentes.Id_hora_final = 15 AND materias_docentes.Estado = "Activo"',
            2,2,2,3,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 2 AND materias_docentes.Id_hora_inicial = 14 AND materias_docentes.Id_hora_final = 16 AND materias_docentes.Estado = "Activo"',
            2,2,2,4,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 2 AND materias_docentes.Id_hora_inicial = 14 AND materias_docentes.Id_hora_final = 17 AND materias_docentes.Estado = "Activo"',
            2,2,2,5,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 2 AND materias_docentes.Id_hora_inicial = 14 AND materias_docentes.Id_hora_final = 18 AND materias_docentes.Estado = "Activo"',
            2,2,2,6,
            2,self.nocturnoDocente          
        )
        
        # Segunda linea Miercoles
        
        self.celda1x5(
            self.parametrosDocentes,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 3 AND materias_docentes.Id_hora_inicial = 14 AND materias_docentes.Id_hora_final = 15 AND materias_docentes.Estado = "Activo"',
            3,2,3,3,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 3 AND materias_docentes.Id_hora_inicial = 14 AND materias_docentes.Id_hora_final = 16 AND materias_docentes.Estado = "Activo"',
            3,2,3,4,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 3 AND materias_docentes.Id_hora_inicial = 14 AND materias_docentes.Id_hora_final = 17 AND materias_docentes.Estado = "Activo"',
            3,2,3,5,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 3 AND materias_docentes.Id_hora_inicial = 14 AND materias_docentes.Id_hora_final = 18 AND materias_docentes.Estado = "Activo"',
            3,2,3,6,
            2,self.nocturnoDocente          
        )
        
        # Segunda linea Jueves
        
        self.celda1x5(
            self.parametrosDocentes,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 4 AND materias_docentes.Id_hora_inicial = 14 AND materias_docentes.Id_hora_final = 15 AND materias_docentes.Estado = "Activo"',
            4,2,4,3,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 4 AND materias_docentes.Id_hora_inicial = 14 AND materias_docentes.Id_hora_final = 16 AND materias_docentes.Estado = "Activo"',
            4,2,4,4,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 4 AND materias_docentes.Id_hora_inicial = 14 AND materias_docentes.Id_hora_final = 17 AND materias_docentes.Estado = "Activo"',
            4,2,4,5,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 4 AND materias_docentes.Id_hora_inicial = 14 AND materias_docentes.Id_hora_final = 18 AND materias_docentes.Estado = "Activo"',
            4,2,4,6,
            2,self.nocturnoDocente          
        )
        
        # Segunda linea Viernes
        
        self.celda1x5(
            self.parametrosDocentes,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 5 AND materias_docentes.Id_hora_inicial = 14 AND materias_docentes.Id_hora_final = 15 AND materias_docentes.Estado = "Activo"',
            5,2,5,3,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 5 AND materias_docentes.Id_hora_inicial = 14 AND materias_docentes.Id_hora_final = 16 AND materias_docentes.Estado = "Activo"',
            5,2,5,4,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 5 AND materias_docentes.Id_hora_inicial = 14 AND materias_docentes.Id_hora_final = 17 AND materias_docentes.Estado = "Activo"',
            5,2,5,5,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 5 AND materias_docentes.Id_hora_inicial = 14 AND materias_docentes.Id_hora_final = 18 AND materias_docentes.Estado = "Activo"',
            5,2,5,6,
            2,self.nocturnoDocente          
        )
        
        print('Tercera linea ----------------')
        # Tercera linea lunes
        
        self.celda1x4(
            self.parametrosDocentes,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 1 AND materias_docentes.Id_hora_inicial = 15 AND materias_docentes.Id_hora_final = 16 AND materias_docentes.Estado = "Activo"',
            1,3,1,4,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 1 AND materias_docentes.Id_hora_inicial = 15 AND materias_docentes.Id_hora_final = 17 AND materias_docentes.Estado = "Activo"',
            1,3,1,5,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 1 AND materias_docentes.Id_hora_inicial = 15 AND materias_docentes.Id_hora_final = 18 AND materias_docentes.Estado = "Activo"',
            1,3,1,6,
            3,self.nocturnoDocente          
        )
        
        # Tercera linea Martes
        
        self.celda1x4(
            self.parametrosDocentes,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 2 AND materias_docentes.Id_hora_inicial = 15 AND materias_docentes.Id_hora_final = 16 AND materias_docentes.Estado = "Activo"',
            2,3,2,4,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 2 AND materias_docentes.Id_hora_inicial = 15 AND materias_docentes.Id_hora_final = 17 AND materias_docentes.Estado = "Activo"',
            2,3,2,5,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 2 AND materias_docentes.Id_hora_inicial = 15 AND materias_docentes.Id_hora_final = 18 AND materias_docentes.Estado = "Activo"',
            2,3,2,6,
            3,self.nocturnoDocente          
        )
        
        # Tercera linea Miercoles
        
        self.celda1x4(
            self.parametrosDocentes,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 3 AND materias_docentes.Id_hora_inicial = 15 AND materias_docentes.Id_hora_final = 16 AND materias_docentes.Estado = "Activo"',
            3,3,3,4,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 3 AND materias_docentes.Id_hora_inicial = 15 AND materias_docentes.Id_hora_final = 17 AND materias_docentes.Estado = "Activo"',
            3,3,3,5,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 3 AND materias_docentes.Id_hora_inicial = 15 AND materias_docentes.Id_hora_final = 18 AND materias_docentes.Estado = "Activo"',
            3,3,3,6,
            3,self.nocturnoDocente          
        )
        
        # Tercera linea Jueves
        
        self.celda1x4(
            self.parametrosDocentes,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 4 AND materias_docentes.Id_hora_inicial = 15 AND materias_docentes.Id_hora_final = 16 AND materias_docentes.Estado = "Activo"',
            4,3,4,4,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 4 AND materias_docentes.Id_hora_inicial = 15 AND materias_docentes.Id_hora_final = 17 AND materias_docentes.Estado = "Activo"',
            4,3,4,5,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 4 AND materias_docentes.Id_hora_inicial = 15 AND materias_docentes.Id_hora_final = 18 AND materias_docentes.Estado = "Activo"',
            4,3,4,6,
            3,self.nocturnoDocente          
        )
        
        # Tercera linea Viernes
        
        self.celda1x4(
            self.parametrosDocentes,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 5 AND materias_docentes.Id_hora_inicial = 15 AND materias_docentes.Id_hora_final = 16 AND materias_docentes.Estado = "Activo"',
            5,3,5,4,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 5 AND materias_docentes.Id_hora_inicial = 15 AND materias_docentes.Id_hora_final = 17 AND materias_docentes.Estado = "Activo"',
            5,3,5,5,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 5 AND materias_docentes.Id_hora_inicial = 15 AND materias_docentes.Id_hora_final = 18 AND materias_docentes.Estado = "Activo"',
            5,3,5,6,
            3,self.nocturnoDocente          
        )
        
        print('Cuarta linea ----------------')
        # Cuarta linea lunes
        
        self.celda1x3(
            self.parametrosDocentes,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 1 AND materias_docentes.Id_hora_inicial = 16 AND materias_docentes.Id_hora_final = 17 AND materias_docentes.Estado = "Activo"',
            1,4,1,5,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 1 AND materias_docentes.Id_hora_inicial = 16 AND materias_docentes.Id_hora_final = 18 AND materias_docentes.Estado = "Activo"',
            1,4,1,6,
            4,self.nocturnoDocente          
        )
        
        # Cuarta linea Martes
        
        self.celda1x3(
            self.parametrosDocentes,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 2 AND materias_docentes.Id_hora_inicial = 16 AND materias_docentes.Id_hora_final = 17 AND materias_docentes.Estado = "Activo"',
            2,4,2,5,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 2 AND materias_docentes.Id_hora_inicial = 16 AND materias_docentes.Id_hora_final = 18 AND materias_docentes.Estado = "Activo"',
            2,4,2,6,
            4,self.nocturnoDocente          
        )
        
        # Cuarta linea Miercoles
        
        self.celda1x3(
            self.parametrosDocentes,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 3 AND materias_docentes.Id_hora_inicial = 16 AND materias_docentes.Id_hora_final = 17 AND materias_docentes.Estado = "Activo"',
            3,4,3,5,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 3 AND materias_docentes.Id_hora_inicial = 16 AND materias_docentes.Id_hora_final = 18 AND materias_docentes.Estado = "Activo"',
            3,4,3,6,
            4,self.nocturnoDocente          
        )
        
        # Cuarta linea Jueves
        
        self.celda1x3(
            self.parametrosDocentes,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 4 AND materias_docentes.Id_hora_inicial = 16 AND materias_docentes.Id_hora_final = 17 AND materias_docentes.Estado = "Activo"',
            4,4,4,5,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 4 AND materias_docentes.Id_hora_inicial = 16 AND materias_docentes.Id_hora_final = 18 AND materias_docentes.Estado = "Activo"',
            4,4,4,6,
            4,self.nocturnoDocente          
        )
        
        # Cuarta linea Viernes
        
        self.celda1x3(
            self.parametrosDocentes,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 5 AND materias_docentes.Id_hora_inicial = 16 AND materias_docentes.Id_hora_final = 17 AND materias_docentes.Estado = "Activo"',
            5,4,5,5,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 5 AND materias_docentes.Id_hora_inicial = 16 AND materias_docentes.Id_hora_final = 18 AND materias_docentes.Estado = "Activo"',
            5,4,5,6,
            4,self.nocturnoDocente          
        )
        
        print('Quinta linea ----------------')
        # Quinta linea lunes
        
        self.celda1x2(
            self.parametrosDocentes,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 1 AND materias_docentes.Id_hora_inicial = 17 AND materias_docentes.Id_hora_final = 18 AND materias_docentes.Estado = "Activo"',
            1,5,1,6,
            5,self.nocturnoDocente          
        )
        
        # Quinta linea Martes
        
        self.celda1x2(
            self.parametrosDocentes,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 2 AND materias_docentes.Id_hora_inicial = 17 AND materias_docentes.Id_hora_final = 18 AND materias_docentes.Estado = "Activo"',
            2,5,2,6,
            5,self.nocturnoDocente          
        )
        
        # Quinta linea Miercoles
        
        self.celda1x2(
            self.parametrosDocentes,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 3 AND materias_docentes.Id_hora_inicial = 17 AND materias_docentes.Id_hora_final = 18 AND materias_docentes.Estado = "Activo"',
            3,5,3,6,
            5,self.nocturnoDocente          
        )
        
        # Quinta linea Jueves
        
        self.celda1x2(
            self.parametrosDocentes,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 4 AND materias_docentes.Id_hora_inicial = 17 AND materias_docentes.Id_hora_final = 18 AND materias_docentes.Estado = "Activo"',
            4,5,4,6,
            5,self.nocturnoDocente          
        )
        
        # Quinta linea Viernes
        
        self.celda1x2(
            self.parametrosDocentes,
            'SELECT materias_docentes.materia FROM materias_docentes WHERE materias_docentes.Id_docente = ? AND materias_docentes.Id_lapso_academico = ? AND materias_docentes.Id_modalidad = ? AND materias_docentes.Id_semana = 5 AND materias_docentes.Id_hora_inicial = 17 AND materias_docentes.Id_hora_final = 18 AND materias_docentes.Estado = "Activo"',
            5,5,5,6,
            5,self.nocturnoDocente          
        )
        return self.nocturnoDocente 

    def obtenerHorarioDiurnoLaboratorio(self):
        self.diurnoLaboratorio = [
            [Paragraph('bloque de horas diurno',self.center),Paragraph('Lunes',self.center),Paragraph('Martes',self.center),Paragraph('Miércoles',self.center),Paragraph('Jueves',self.center),Paragraph('Viernes',self.center)],
            [Paragraph('7:10 - 7:55',self.center)],
            [Paragraph('8:00 - 8:45',self.center)],
            [Paragraph('8:50 - 9:35',self.center)],
            [Paragraph('9:40 - 10:25',self.center)],
            [Paragraph('10:30 - 11:15',self.center)],
            [Paragraph('11:20 - 12:05',self.center)],
            [Paragraph('1:05 - 1:55',self.center)],
            [Paragraph('1:55 - 2:40',self.center)],
            [Paragraph('2:45 - 3:30',self.center)],
            [Paragraph('3:45 - 4:20',self.center)],
            [Paragraph('4:25 - 5:10',self.center)],
            [Paragraph('5:15 - 6:00',self.center)]
        ]
        self.validarSemanaLaboratorio(self.diurnoLaboratorio,0)

        print('Primera linea ----------------')
        # Primera linea lunes

        self.celda1x6(
            self.parametrosLaboratorios,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 1  AND materias_laboratorios.Id_hora_inicial = 1 AND materias_laboratorios.Id_hora_final = 2 AND materias_laboratorios.Estado = "Activo"',
            1,1,1,2,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 1  AND materias_laboratorios.Id_hora_inicial = 1 AND materias_laboratorios.Id_hora_final = 3 AND materias_laboratorios.Estado = "Activo"',
            1,1,1,3,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 1  AND materias_laboratorios.Id_hora_inicial = 1 AND materias_laboratorios.Id_hora_final = 4 AND materias_laboratorios.Estado = "Activo"',
            1,1,1,4,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 1  AND materias_laboratorios.Id_hora_inicial = 1 AND materias_laboratorios.Id_hora_final = 5 AND materias_laboratorios.Estado = "Activo"',
            1,1,1,5,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 1  AND materias_laboratorios.Id_hora_inicial = 1 AND materias_laboratorios.Id_hora_final = 6 AND materias_laboratorios.Estado = "Activo"',
            1,1,1,6,
            1,self.diurnoLaboratorio
        )

        # Primera linea Martes

        self.celda1x6(
            self.parametrosLaboratorios,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 2  AND materias_laboratorios.Id_hora_inicial = 1 AND materias_laboratorios.Id_hora_final = 2 AND materias_laboratorios.Estado = "Activo"',
            2,1,2,2,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 2  AND materias_laboratorios.Id_hora_inicial = 1 AND materias_laboratorios.Id_hora_final = 3 AND materias_laboratorios.Estado = "Activo"',
            2,1,2,3,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 2  AND materias_laboratorios.Id_hora_inicial = 1 AND materias_laboratorios.Id_hora_final = 4 AND materias_laboratorios.Estado = "Activo"',
            2,1,2,4,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 2  AND materias_laboratorios.Id_hora_inicial = 1 AND materias_laboratorios.Id_hora_final = 5 AND materias_laboratorios.Estado = "Activo"',
            2,1,2,5,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 2  AND materias_laboratorios.Id_hora_inicial = 1 AND materias_laboratorios.Id_hora_final = 6 AND materias_laboratorios.Estado = "Activo"',
            2,1,2,6,
            1,self.diurnoLaboratorio
        )

        # Primera linea Miercoles

        self.celda1x6(
            self.parametrosLaboratorios,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 3  AND materias_laboratorios.Id_hora_inicial = 1 AND materias_laboratorios.Id_hora_final = 2 AND materias_laboratorios.Estado = "Activo"',
            3,1,3,2,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 3  AND materias_laboratorios.Id_hora_inicial = 1 AND materias_laboratorios.Id_hora_final = 3 AND materias_laboratorios.Estado = "Activo"',
            3,1,3,3,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 3  AND materias_laboratorios.Id_hora_inicial = 1 AND materias_laboratorios.Id_hora_final = 4 AND materias_laboratorios.Estado = "Activo"',
            3,1,3,4,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 3  AND materias_laboratorios.Id_hora_inicial = 1 AND materias_laboratorios.Id_hora_final = 5 AND materias_laboratorios.Estado = "Activo"',
            3,1,3,5,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 3  AND materias_laboratorios.Id_hora_inicial = 1 AND materias_laboratorios.Id_hora_final = 6 AND materias_laboratorios.Estado = "Activo"',
            3,1,3,6,
            1,self.diurnoLaboratorio
        )

        # Primera linea Jueves

        self.celda1x6(
            self.parametrosLaboratorios,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 4  AND materias_laboratorios.Id_hora_inicial = 1 AND materias_laboratorios.Id_hora_final = 2 AND materias_laboratorios.Estado = "Activo"',
            4,1,4,2,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 4  AND materias_laboratorios.Id_hora_inicial = 1 AND materias_laboratorios.Id_hora_final = 3 AND materias_laboratorios.Estado = "Activo"',
            4,1,4,3,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 4  AND materias_laboratorios.Id_hora_inicial = 1 AND materias_laboratorios.Id_hora_final = 4 AND materias_laboratorios.Estado = "Activo"',
            4,1,4,4,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 4  AND materias_laboratorios.Id_hora_inicial = 1 AND materias_laboratorios.Id_hora_final = 5 AND materias_laboratorios.Estado = "Activo"',
            4,1,4,5,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 4 AND materias_laboratorios.Id_hora_inicial = 1 AND materias_laboratorios.Id_hora_final = 6 AND materias_laboratorios.Estado = "Activo"',
            4,1,4,6,
            1,self.diurnoLaboratorio
        )

        # Primera linea Viernes

        self.celda1x6(
            self.parametrosLaboratorios,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 5  AND materias_laboratorios.Id_hora_inicial = 1 AND materias_laboratorios.Id_hora_final = 2 AND materias_laboratorios.Estado = "Activo"',
            5,1,5,2,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 5  AND materias_laboratorios.Id_hora_inicial = 1 AND materias_laboratorios.Id_hora_final = 3 AND materias_laboratorios.Estado = "Activo"',
            5,1,5,3,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 5  AND materias_laboratorios.Id_hora_inicial = 1 AND materias_laboratorios.Id_hora_final = 4 AND materias_laboratorios.Estado = "Activo"',
            5,1,5,4,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 5  AND materias_laboratorios.Id_hora_inicial = 1 AND materias_laboratorios.Id_hora_final = 5 AND materias_laboratorios.Estado = "Activo"',
            5,1,5,5,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 5  AND materias_laboratorios.Id_hora_inicial = 1 AND materias_laboratorios.Id_hora_final = 6 AND materias_laboratorios.Estado = "Activo"',
            5,1,5,6,
            1,self.diurnoLaboratorio
        )

        print('Segunda linea ----------------')
        # Segunda linea lunes

        self.celda1x5(
            self.parametrosLaboratorios,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 1  AND materias_laboratorios.Id_hora_inicial = 2 AND materias_laboratorios.Id_hora_final = 3 AND materias_laboratorios.Estado = "Activo"',
            1,2,1,3,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 1  AND materias_laboratorios.Id_hora_inicial = 2 AND materias_laboratorios.Id_hora_final = 4 AND materias_laboratorios.Estado = "Activo"',
            1,2,1,4,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 1  AND materias_laboratorios.Id_hora_inicial = 2 AND materias_laboratorios.Id_hora_final = 5 AND materias_laboratorios.Estado = "Activo"',
            1,2,1,5,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 1  AND materias_laboratorios.Id_hora_inicial = 2 AND materias_laboratorios.Id_hora_final = 6 AND materias_laboratorios.Estado = "Activo"',
            1,2,1,6,
            2,self.diurnoLaboratorio
        )

        # Segunda linea Martes

        self.celda1x5(
            self.parametrosLaboratorios,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 2  AND materias_laboratorios.Id_hora_inicial = 2 AND materias_laboratorios.Id_hora_final = 3 AND materias_laboratorios.Estado = "Activo"',
            2,2,2,3,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 2  AND materias_laboratorios.Id_hora_inicial = 2 AND materias_laboratorios.Id_hora_final = 4 AND materias_laboratorios.Estado = "Activo"',
            2,2,2,4,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 2  AND materias_laboratorios.Id_hora_inicial = 2 AND materias_laboratorios.Id_hora_final = 5 AND materias_laboratorios.Estado = "Activo"',
            2,2,2,5,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 2  AND materias_laboratorios.Id_hora_inicial = 2 AND materias_laboratorios.Id_hora_final = 6 AND materias_laboratorios.Estado = "Activo"',
            2,2,2,6,
            2,self.diurnoLaboratorio
        )

        # Segunda linea Miercoles

        self.celda1x5(
            self.parametrosLaboratorios,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 3  AND materias_laboratorios.Id_hora_inicial = 2 AND materias_laboratorios.Id_hora_final = 3 AND materias_laboratorios.Estado = "Activo"',
            3,2,3,3,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 3  AND materias_laboratorios.Id_hora_inicial = 2 AND materias_laboratorios.Id_hora_final = 4 AND materias_laboratorios.Estado = "Activo"',
            3,2,3,4,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 3  AND materias_laboratorios.Id_hora_inicial = 2 AND materias_laboratorios.Id_hora_final = 5 AND materias_laboratorios.Estado = "Activo"',
            3,2,3,5,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 3  AND materias_laboratorios.Id_hora_inicial = 2 AND materias_laboratorios.Id_hora_final = 6 AND materias_laboratorios.Estado = "Activo"',
            3,2,3,6,
            2,self.diurnoLaboratorio
        )

        # Segunda linea Jueves

        self.celda1x5(
            self.parametrosLaboratorios,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 4  AND materias_laboratorios.Id_hora_inicial = 2 AND materias_laboratorios.Id_hora_final = 3 AND materias_laboratorios.Estado = "Activo"',
            4,2,4,3,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 4  AND materias_laboratorios.Id_hora_inicial = 2 AND materias_laboratorios.Id_hora_final = 4 AND materias_laboratorios.Estado = "Activo"',
            4,2,4,4,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 4  AND materias_laboratorios.Id_hora_inicial = 2 AND materias_laboratorios.Id_hora_final = 5 AND materias_laboratorios.Estado = "Activo"',
            4,2,4,5,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 4  AND materias_laboratorios.Id_hora_inicial = 2 AND materias_laboratorios.Id_hora_final = 6 AND materias_laboratorios.Estado = "Activo"',
            4,2,4,6,
            2,self.diurnoLaboratorio
        )

        # Segunda linea Viernes

        self.celda1x5(
            self.parametrosLaboratorios,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 5  AND materias_laboratorios.Id_hora_inicial = 2 AND materias_laboratorios.Id_hora_final = 3 AND materias_laboratorios.Estado = "Activo"',
            5,2,5,3,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 5  AND materias_laboratorios.Id_hora_inicial = 2 AND materias_laboratorios.Id_hora_final = 4 AND materias_laboratorios.Estado = "Activo"',
            5,2,5,4,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 5  AND materias_laboratorios.Id_hora_inicial = 2 AND materias_laboratorios.Id_hora_final = 5 AND materias_laboratorios.Estado = "Activo"',
            5,2,5,5,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 5  AND materias_laboratorios.Id_hora_inicial = 2 AND materias_laboratorios.Id_hora_final = 6 AND materias_laboratorios.Estado = "Activo"',
            5,2,5,6,
            2,self.diurnoLaboratorio
        )

        print('Tercera linea ----------------')
        # Tercera linea lunes

        self.celda1x4(
            self.parametrosLaboratorios,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 1  AND materias_laboratorios.Id_hora_inicial = 3 AND materias_laboratorios.Id_hora_final = 4 AND materias_laboratorios.Estado = "Activo"',
            1,3,1,4,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 1  AND materias_laboratorios.Id_hora_inicial = 3 AND materias_laboratorios.Id_hora_final = 5 AND materias_laboratorios.Estado = "Activo"',
            1,3,1,5,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 1  AND materias_laboratorios.Id_hora_inicial = 3 AND materias_laboratorios.Id_hora_final = 6 AND materias_laboratorios.Estado = "Activo"',
            1,3,1,6,
            3,self.diurnoLaboratorio
        )

        # Tercera linea Martes

        self.celda1x4(
            self.parametrosLaboratorios,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 2  AND materias_laboratorios.Id_hora_inicial = 3 AND materias_laboratorios.Id_hora_final = 4 AND materias_laboratorios.Estado = "Activo"',
            2,3,2,4,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 2  AND materias_laboratorios.Id_hora_inicial = 3 AND materias_laboratorios.Id_hora_final = 5 AND materias_laboratorios.Estado = "Activo"',
            2,3,2,5,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 2  AND materias_laboratorios.Id_hora_inicial = 3 AND materias_laboratorios.Id_hora_final = 6 AND materias_laboratorios.Estado = "Activo"',
            2,3,2,6,
            3,self.diurnoLaboratorio
        )

        # Tercera linea Miercoles

        self.celda1x4(
            self.parametrosLaboratorios,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 3  AND materias_laboratorios.Id_hora_inicial = 3 AND materias_laboratorios.Id_hora_final = 4 AND materias_laboratorios.Estado = "Activo"',
            3,3,3,4,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 3  AND materias_laboratorios.Id_hora_inicial = 3 AND materias_laboratorios.Id_hora_final = 5 AND materias_laboratorios.Estado = "Activo"',
            3,3,3,5,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 3  AND materias_laboratorios.Id_hora_inicial = 3 AND materias_laboratorios.Id_hora_final = 6 AND materias_laboratorios.Estado = "Activo"',
            3,3,3,6,
            3,self.diurnoLaboratorio
        )

        # Tercera linea Jueves

        self.celda1x4(
            self.parametrosLaboratorios,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 4  AND materias_laboratorios.Id_hora_inicial = 3 AND materias_laboratorios.Id_hora_final = 4 AND materias_laboratorios.Estado = "Activo"',
            4,3,4,4,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 4  AND materias_laboratorios.Id_hora_inicial = 3 AND materias_laboratorios.Id_hora_final = 5 AND materias_laboratorios.Estado = "Activo"',
            4,3,4,5,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 4  AND materias_laboratorios.Id_hora_inicial = 3 AND materias_laboratorios.Id_hora_final = 6 AND materias_laboratorios.Estado = "Activo"',
            4,3,4,6,
            3,self.diurnoLaboratorio
        )

        # Tercera linea Viernes

        self.celda1x4(
            self.parametrosLaboratorios,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 5  AND materias_laboratorios.Id_hora_inicial = 3 AND materias_laboratorios.Id_hora_final = 4 AND materias_laboratorios.Estado = "Activo"',
            5,3,5,4,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 5  AND materias_laboratorios.Id_hora_inicial = 3 AND materias_laboratorios.Id_hora_final = 5 AND materias_laboratorios.Estado = "Activo"',
            5,3,5,5,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 5  AND materias_laboratorios.Id_hora_inicial = 3 AND materias_laboratorios.Id_hora_final = 6 AND materias_laboratorios.Estado = "Activo"',
            5,3,5,6,
            3,self.diurnoLaboratorio
        )

        print('Cuarta linea ----------------')
        # Cuarta linea lunes

        self.celda1x3(
            self.parametrosLaboratorios,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 1  AND materias_laboratorios.Id_hora_inicial = 4 AND materias_laboratorios.Id_hora_final = 5 AND materias_laboratorios.Estado = "Activo"',
            1,4,1,5,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 1  AND materias_laboratorios.Id_hora_inicial = 4 AND materias_laboratorios.Id_hora_final = 6 AND materias_laboratorios.Estado = "Activo"',
            1,4,1,6,
            4,self.diurnoLaboratorio
        )

        # Cuarta linea Martes

        self.celda1x3(
            self.parametrosLaboratorios,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 2  AND materias_laboratorios.Id_hora_inicial = 4 AND materias_laboratorios.Id_hora_final = 5 AND materias_laboratorios.Estado = "Activo"',
            2,4,2,5,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 2  AND materias_laboratorios.Id_hora_inicial = 4 AND materias_laboratorios.Id_hora_final = 6 AND materias_laboratorios.Estado = "Activo"',
            2,4,2,6,
            4,self.diurnoLaboratorio
        )

        # Cuarta linea Miercoles

        self.celda1x3(
            self.parametrosLaboratorios,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 3  AND materias_laboratorios.Id_hora_inicial = 4 AND materias_laboratorios.Id_hora_final = 5 AND materias_laboratorios.Estado = "Activo"',
            3,4,3,5,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 3  AND materias_laboratorios.Id_hora_inicial = 4 AND materias_laboratorios.Id_hora_final = 6 AND materias_laboratorios.Estado = "Activo"',
            3,4,3,6,
            4,self.diurnoLaboratorio
        )

        # Cuarta linea Jueves

        self.celda1x3(
            self.parametrosLaboratorios,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 4  AND materias_laboratorios.Id_hora_inicial = 4 AND materias_laboratorios.Id_hora_final = 5 AND materias_laboratorios.Estado = "Activo"',
            4,4,4,5,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 4  AND materias_laboratorios.Id_hora_inicial = 4 AND materias_laboratorios.Id_hora_final = 6 AND materias_laboratorios.Estado = "Activo"',
            4,4,4,6,
            4,self.diurnoLaboratorio
        )

        # Cuarta linea Viernes

        self.celda1x3(
            self.parametrosLaboratorios,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 5  AND materias_laboratorios.Id_hora_inicial = 4 AND materias_laboratorios.Id_hora_final = 5 AND materias_laboratorios.Estado = "Activo"',
            5,4,5,5,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 5  AND materias_laboratorios.Id_hora_inicial = 4 AND materias_laboratorios.Id_hora_final = 6 AND materias_laboratorios.Estado = "Activo"',
            5,4,5,6,
            4,self.diurnoLaboratorio
        )

        print('Quinta linea ----------------')
        # Quinta linea lunes

        self.celda1x2(
            self.parametrosLaboratorios,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 1  AND materias_laboratorios.Id_hora_inicial = 5 AND materias_laboratorios.Id_hora_final = 6 AND materias_laboratorios.Estado = "Activo"',
            1,5,1,6,
            5,self.diurnoLaboratorio
        )

        # Quinta linea Martes

        self.celda1x2(
            self.parametrosLaboratorios,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 2  AND materias_laboratorios.Id_hora_inicial = 5 AND materias_laboratorios.Id_hora_final = 6 AND materias_laboratorios.Estado = "Activo"',
            2,5,2,6,
            5,self.diurnoLaboratorio
        )

        # Quinta linea Miercoles

        self.celda1x2(
            self.parametrosLaboratorios,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 3  AND materias_laboratorios.Id_hora_inicial = 5 AND materias_laboratorios.Id_hora_final = 6 AND materias_laboratorios.Estado = "Activo"',
            3,5,3,6,
            5,self.diurnoLaboratorio
        )

        # Quinta linea Jueves

        self.celda1x2(
            self.parametrosLaboratorios,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 4  AND materias_laboratorios.Id_hora_inicial = 5 AND materias_laboratorios.Id_hora_final = 6 AND materias_laboratorios.Estado = "Activo"',
            4,5,4,6,
            5,self.diurnoLaboratorio
        )

        # Quinta linea Viernes

        self.celda1x2(
            self.parametrosLaboratorios,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 5  AND materias_laboratorios.Id_hora_inicial = 5 AND materias_laboratorios.Id_hora_final = 6 AND materias_laboratorios.Estado = "Activo"',
            5,5,5,6,
            5,self.diurnoLaboratorio
        )

        print('Septima linea ----------------')
        # Septima linea lunes

        self.celda1x6(
            self.parametrosLaboratorios,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 1  AND materias_laboratorios.Id_hora_inicial = 7 AND materias_laboratorios.Id_hora_final = 8 AND materias_laboratorios.Estado = "Activo"',
            1,7,1,8,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 1  AND materias_laboratorios.Id_hora_inicial = 7 AND materias_laboratorios.Id_hora_final = 9 AND materias_laboratorios.Estado = "Activo"',
            1,7,1,9,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 1  AND materias_laboratorios.Id_hora_inicial = 7 AND materias_laboratorios.Id_hora_final = 10 AND materias_laboratorios.Estado = "Activo"',
            1,7,1,10,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 1  AND materias_laboratorios.Id_hora_inicial = 7 AND materias_laboratorios.Id_hora_final = 11 AND materias_laboratorios.Estado = "Activo"',
            1,7,1,11,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 1  AND materias_laboratorios.Id_hora_inicial = 7 AND materias_laboratorios.Id_hora_final = 12 AND materias_laboratorios.Estado = "Activo"',
            1,7,1,12,
            7,self.diurnoLaboratorio
        )

        # Septima linea Martes

        self.celda1x6(
            self.parametrosLaboratorios,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 2  AND materias_laboratorios.Id_hora_inicial = 7 AND materias_laboratorios.Id_hora_final = 8 AND materias_laboratorios.Estado = "Activo"',
            2,7,2,8,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 2  AND materias_laboratorios.Id_hora_inicial = 7 AND materias_laboratorios.Id_hora_final = 9 AND materias_laboratorios.Estado = "Activo"',
            2,7,2,9,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 2  AND materias_laboratorios.Id_hora_inicial = 7 AND materias_laboratorios.Id_hora_final = 10 AND materias_laboratorios.Estado = "Activo"',
            2,7,2,10,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 2  AND materias_laboratorios.Id_hora_inicial = 7 AND materias_laboratorios.Id_hora_final = 11 AND materias_laboratorios.Estado = "Activo"',
            2,7,2,11,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 2  AND materias_laboratorios.Id_hora_inicial = 7 AND materias_laboratorios.Id_hora_final = 12 AND materias_laboratorios.Estado = "Activo"',
            2,7,2,12,
            7,self.diurnoLaboratorio
        )

        # Septima linea Miercoles

        self.celda1x6(
            self.parametrosLaboratorios,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 3  AND materias_laboratorios.Id_hora_inicial = 7 AND materias_laboratorios.Id_hora_final = 8 AND materias_laboratorios.Estado = "Activo"',
            3,7,3,8,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 3  AND materias_laboratorios.Id_hora_inicial = 7 AND materias_laboratorios.Id_hora_final = 9 AND materias_laboratorios.Estado = "Activo"',
            3,7,3,9,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 3  AND materias_laboratorios.Id_hora_inicial = 7 AND materias_laboratorios.Id_hora_final = 10 AND materias_laboratorios.Estado = "Activo"',
            3,7,3,10,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 3  AND materias_laboratorios.Id_hora_inicial = 7 AND materias_laboratorios.Id_hora_final = 11 AND materias_laboratorios.Estado = "Activo"',
            3,7,3,11,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 3  AND materias_laboratorios.Id_hora_inicial = 7 AND materias_laboratorios.Id_hora_final = 12 AND materias_laboratorios.Estado = "Activo"',
            3,7,3,12,
            7,self.diurnoLaboratorio
        )

        # Septima linea Jueves

        self.celda1x6(
            self.parametrosLaboratorios,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 4  AND materias_laboratorios.Id_hora_inicial = 7 AND materias_laboratorios.Id_hora_final = 8 AND materias_laboratorios.Estado = "Activo"',
            4,7,4,8,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 4  AND materias_laboratorios.Id_hora_inicial = 7 AND materias_laboratorios.Id_hora_final = 9 AND materias_laboratorios.Estado = "Activo"',
            4,7,4,9,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 4  AND materias_laboratorios.Id_hora_inicial = 7 AND materias_laboratorios.Id_hora_final = 10 AND materias_laboratorios.Estado = "Activo"',
            4,7,4,10,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 4  AND materias_laboratorios.Id_hora_inicial = 7 AND materias_laboratorios.Id_hora_final = 11 AND materias_laboratorios.Estado = "Activo"',
            4,7,4,11,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 4  AND materias_laboratorios.Id_hora_inicial = 7 AND materias_laboratorios.Id_hora_final = 12 AND materias_laboratorios.Estado = "Activo"',
            4,7,4,12,
            7,self.diurnoLaboratorio
        )

        # Septima linea Viernes

        self.celda1x6(
            self.parametrosLaboratorios,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 5  AND materias_laboratorios.Id_hora_inicial = 7 AND materias_laboratorios.Id_hora_final = 8 AND materias_laboratorios.Estado = "Activo"',
            5,7,5,8,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 5  AND materias_laboratorios.Id_hora_inicial = 7 AND materias_laboratorios.Id_hora_final = 9 AND materias_laboratorios.Estado = "Activo"',
            5,7,5,9,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 5  AND materias_laboratorios.Id_hora_inicial = 7 AND materias_laboratorios.Id_hora_final = 10 AND materias_laboratorios.Estado = "Activo"',
            5,7,5,10,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 5  AND materias_laboratorios.Id_hora_inicial = 7 AND materias_laboratorios.Id_hora_final = 11 AND materias_laboratorios.Estado = "Activo"',
            5,7,5,11,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 5  AND materias_laboratorios.Id_hora_inicial = 7 AND materias_laboratorios.Id_hora_final = 12 AND materias_laboratorios.Estado = "Activo"',
            5,7,5,12,
            7,self.diurnoLaboratorio
        )

        print('Octava linea ----------------')
        # Octava linea lunes

        self.celda1x5(
            self.parametrosLaboratorios,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 1  AND materias_laboratorios.Id_hora_inicial = 8 AND materias_laboratorios.Id_hora_final = 9 AND materias_laboratorios.Estado = "Activo"',
            1,8,1,9,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 1  AND materias_laboratorios.Id_hora_inicial = 8 AND materias_laboratorios.Id_hora_final = 10 AND materias_laboratorios.Estado = "Activo"',
            1,8,1,10,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 1  AND materias_laboratorios.Id_hora_inicial = 8 AND materias_laboratorios.Id_hora_final = 11 AND materias_laboratorios.Estado = "Activo"',
            1,8,1,11,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 1  AND materias_laboratorios.Id_hora_inicial = 8 AND materias_laboratorios.Id_hora_final = 12 AND materias_laboratorios.Estado = "Activo"',
            1,8,1,12,
            8,self.diurnoLaboratorio
        )

        # Octava linea Martes

        self.celda1x5(
            self.parametrosLaboratorios,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 2  AND materias_laboratorios.Id_hora_inicial = 8 AND materias_laboratorios.Id_hora_final = 9 AND materias_laboratorios.Estado = "Activo"',
            2,8,2,9,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 2  AND materias_laboratorios.Id_hora_inicial = 8 AND materias_laboratorios.Id_hora_final = 10 AND materias_laboratorios.Estado = "Activo"',
            2,8,2,10,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 2  AND materias_laboratorios.Id_hora_inicial = 8 AND materias_laboratorios.Id_hora_final = 11 AND materias_laboratorios.Estado = "Activo"',
            2,8,2,11,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 2  AND materias_laboratorios.Id_hora_inicial = 8 AND materias_laboratorios.Id_hora_final = 12 AND materias_laboratorios.Estado = "Activo"',
            2,8,2,12,
            8,self.diurnoLaboratorio
        )

        # Octava linea Miercoles

        self.celda1x5(
            self.parametrosLaboratorios,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 3  AND materias_laboratorios.Id_hora_inicial = 8 AND materias_laboratorios.Id_hora_final = 9 AND materias_laboratorios.Estado = "Activo"',
            3,8,3,9,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 3  AND materias_laboratorios.Id_hora_inicial = 8 AND materias_laboratorios.Id_hora_final = 10 AND materias_laboratorios.Estado = "Activo"',
            3,8,3,10,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 3  AND materias_laboratorios.Id_hora_inicial = 8 AND materias_laboratorios.Id_hora_final = 11 AND materias_laboratorios.Estado = "Activo"',
            3,8,3,11,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 3  AND materias_laboratorios.Id_hora_inicial = 8 AND materias_laboratorios.Id_hora_final = 12 AND materias_laboratorios.Estado = "Activo"',
            3,8,3,12,
            8,self.diurnoLaboratorio
        )

        # Octava linea Jueves

        self.celda1x5(
            self.parametrosLaboratorios,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 4  AND materias_laboratorios.Id_hora_inicial = 8 AND materias_laboratorios.Id_hora_final = 9 AND materias_laboratorios.Estado = "Activo"',
            4,8,4,9,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 4  AND materias_laboratorios.Id_hora_inicial = 8 AND materias_laboratorios.Id_hora_final = 10 AND materias_laboratorios.Estado = "Activo"',
            4,8,4,10,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 4  AND materias_laboratorios.Id_hora_inicial = 8 AND materias_laboratorios.Id_hora_final = 11 AND materias_laboratorios.Estado = "Activo"',
            4,8,4,11,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 4  AND materias_laboratorios.Id_hora_inicial = 8 AND materias_laboratorios.Id_hora_final = 12 AND materias_laboratorios.Estado = "Activo"',
            4,8,4,12,
            8,self.diurnoLaboratorio
        )

        # Octava linea Viernes

        self.celda1x5(
            self.parametrosLaboratorios,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 5  AND materias_laboratorios.Id_hora_inicial = 8 AND materias_laboratorios.Id_hora_final = 9 AND materias_laboratorios.Estado = "Activo"',
            5,8,5,9,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 5  AND materias_laboratorios.Id_hora_inicial = 8 AND materias_laboratorios.Id_hora_final = 10 AND materias_laboratorios.Estado = "Activo"',
            5,8,5,10,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 5  AND materias_laboratorios.Id_hora_inicial = 8 AND materias_laboratorios.Id_hora_final = 11 AND materias_laboratorios.Estado = "Activo"',
            5,8,5,11,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 5  AND materias_laboratorios.Id_hora_inicial = 8 AND materias_laboratorios.Id_hora_final = 12 AND materias_laboratorios.Estado = "Activo"',
            5,8,5,12,
            8,self.diurnoLaboratorio
        )

        print('Octava linea ----------------')
        # Octava linea lunes

        self.celda1x4(
            self.parametrosLaboratorios,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 1  AND materias_laboratorios.Id_hora_inicial = 9 AND materias_laboratorios.Id_hora_final = 10 AND materias_laboratorios.Estado = "Activo"',
            1,9,1,10,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 1  AND materias_laboratorios.Id_hora_inicial = 9 AND materias_laboratorios.Id_hora_final = 11 AND materias_laboratorios.Estado = "Activo"',
            1,9,1,11,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 1  AND materias_laboratorios.Id_hora_inicial = 9 AND materias_laboratorios.Id_hora_final = 12 AND materias_laboratorios.Estado = "Activo"',
            1,9,1,12,
            9,self.diurnoLaboratorio
        )

        # Octava linea Martes

        self.celda1x4(
            self.parametrosLaboratorios,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 2  AND materias_laboratorios.Id_hora_inicial = 9 AND materias_laboratorios.Id_hora_final = 10 AND materias_laboratorios.Estado = "Activo"',
            2,9,2,10,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 2  AND materias_laboratorios.Id_hora_inicial = 9 AND materias_laboratorios.Id_hora_final = 11 AND materias_laboratorios.Estado = "Activo"',
            2,9,2,11,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 2  AND materias_laboratorios.Id_hora_inicial = 9 AND materias_laboratorios.Id_hora_final = 12 AND materias_laboratorios.Estado = "Activo"',
            2,9,2,12,
            9,self.diurnoLaboratorio
        )

        # Octava linea Miercoles

        self.celda1x4(
            self.parametrosLaboratorios,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 3  AND materias_laboratorios.Id_hora_inicial = 9 AND materias_laboratorios.Id_hora_final = 10 AND materias_laboratorios.Estado = "Activo"',
            3,9,3,10,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 3  AND materias_laboratorios.Id_hora_inicial = 9 AND materias_laboratorios.Id_hora_final = 11 AND materias_laboratorios.Estado = "Activo"',
            3,9,3,11,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 3  AND materias_laboratorios.Id_hora_inicial = 9 AND materias_laboratorios.Id_hora_final = 12 AND materias_laboratorios.Estado = "Activo"',
            3,9,3,12,
            9,self.diurnoLaboratorio
        )

        # Octava linea Jueves

        self.celda1x4(
            self.parametrosLaboratorios,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 4  AND materias_laboratorios.Id_hora_inicial = 9 AND materias_laboratorios.Id_hora_final = 10 AND materias_laboratorios.Estado = "Activo"',
            4,9,4,10,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 4  AND materias_laboratorios.Id_hora_inicial = 9 AND materias_laboratorios.Id_hora_final = 11 AND materias_laboratorios.Estado = "Activo"',
            4,9,4,11,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 4  AND materias_laboratorios.Id_hora_inicial = 9 AND materias_laboratorios.Id_hora_final = 12 AND materias_laboratorios.Estado = "Activo"',
            4,9,4,12,
            9,self.diurnoLaboratorio
        )

        # Octava linea Viernes

        self.celda1x4(
            self.parametrosLaboratorios,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 5  AND materias_laboratorios.Id_hora_inicial = 9 AND materias_laboratorios.Id_hora_final = 10 AND materias_laboratorios.Estado = "Activo"',
            5,9,5,10,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 5  AND materias_laboratorios.Id_hora_inicial = 9 AND materias_laboratorios.Id_hora_final = 11 AND materias_laboratorios.Estado = "Activo"',
            5,9,5,11,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 5  AND materias_laboratorios.Id_hora_inicial = 9 AND materias_laboratorios.Id_hora_final = 12 AND materias_laboratorios.Estado = "Activo"',
            5,9,5,12,
            9,self.diurnoLaboratorio
        )

        print('Decima linea ----------------')
        # Decima linea lunes

        self.celda1x3(
            self.parametrosLaboratorios,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 1  AND materias_laboratorios.Id_hora_inicial = 10 AND materias_laboratorios.Id_hora_final = 11 AND materias_laboratorios.Estado = "Activo"',
            1,10,1,11,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 1  AND materias_laboratorios.Id_hora_inicial = 10 AND materias_laboratorios.Id_hora_final = 12 AND materias_laboratorios.Estado = "Activo"',
            1,10,1,12,
            10,self.diurnoLaboratorio
        )

        # Decima linea Martes

        self.celda1x3(
            self.parametrosLaboratorios,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 2  AND materias_laboratorios.Id_hora_inicial = 10 AND materias_laboratorios.Id_hora_final = 11 AND materias_laboratorios.Estado = "Activo"',
            2,10,2,11,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 2  AND materias_laboratorios.Id_hora_inicial = 10 AND materias_laboratorios.Id_hora_final = 12 AND materias_laboratorios.Estado = "Activo"',
            2,10,2,12,
            10,self.diurnoLaboratorio
        )

        # Decima linea Miercoles

        self.celda1x3(
            self.parametrosLaboratorios,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 3  AND materias_laboratorios.Id_hora_inicial = 10 AND materias_laboratorios.Id_hora_final = 11 AND materias_laboratorios.Estado = "Activo"',
            3,10,3,11,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 3  AND materias_laboratorios.Id_hora_inicial = 10 AND materias_laboratorios.Id_hora_final = 12 AND materias_laboratorios.Estado = "Activo"',
            3,10,3,12,
            10,self.diurnoLaboratorio
        )

        # Decima linea Jueves

        self.celda1x3(
            self.parametrosLaboratorios,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 4  AND materias_laboratorios.Id_hora_inicial = 10 AND materias_laboratorios.Id_hora_final = 11 AND materias_laboratorios.Estado = "Activo"',
            4,10,4,11,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 4  AND materias_laboratorios.Id_hora_inicial = 10 AND materias_laboratorios.Id_hora_final = 12 AND materias_laboratorios.Estado = "Activo"',
            4,10,4,12,
            10,self.diurnoLaboratorio
        )

        # Decima linea Viernes

        self.celda1x3(
            self.parametrosLaboratorios,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 5  AND materias_laboratorios.Id_hora_inicial = 10 AND materias_laboratorios.Id_hora_final = 11 AND materias_laboratorios.Estado = "Activo"',
            5,10,5,11,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 5  AND materias_laboratorios.Id_hora_inicial = 10 AND materias_laboratorios.Id_hora_final = 12 AND materias_laboratorios.Estado = "Activo"',
            5,10,5,12,
            10,self.diurnoLaboratorio
        )

        print('Decima primera linea ----------------')
        # Decima primera linea lunes

        self.celda1x2(
            self.parametrosLaboratorios,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 1  AND materias_laboratorios.Id_hora_inicial = 11 AND materias_laboratorios.Id_hora_final = 12 AND materias_laboratorios.Estado = "Activo"',
            1,11,1,12,
            11,self.diurnoLaboratorio
        )

        # Decima primera linea Martes

        self.celda1x2(
            self.parametrosLaboratorios,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 2  AND materias_laboratorios.Id_hora_inicial = 11 AND materias_laboratorios.Id_hora_final = 12 AND materias_laboratorios.Estado = "Activo"',
            2,11,2,12,
            11,self.diurnoLaboratorio
        )

        # Decima primera linea Miercoles

        self.celda1x2(
            self.parametrosLaboratorios,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 3  AND materias_laboratorios.Id_hora_inicial = 11 AND materias_laboratorios.Id_hora_final = 12 AND materias_laboratorios.Estado = "Activo"',
            3,11,3,12,
            11,self.diurnoLaboratorio
        )

        # Decima primera linea Jueves

        self.celda1x2(
            self.parametrosLaboratorios,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 4  AND materias_laboratorios.Id_hora_inicial = 11 AND materias_laboratorios.Id_hora_final = 12 AND materias_laboratorios.Estado = "Activo"',
            4,11,4,12,
            11,self.diurnoLaboratorio
        )

        # Decima primera linea Viernes

        self.celda1x2(
            self.parametrosLaboratorios,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 5  AND materias_laboratorios.Id_hora_inicial = 11 AND materias_laboratorios.Id_hora_final = 12 AND materias_laboratorios.Estado = "Activo"',
            5,11,5,12,
            11,self.diurnoLaboratorio
        )

        return self.diurnoLaboratorio

    
    def obtenerHorarioNocturnoLaboratorio(self):
        self.nocturnoLabolatorio = [
            [Paragraph('bloque de horas noche',self.center),Paragraph('Lunes',self.center),Paragraph('Martes',self.center),Paragraph('Miércoles',self.center),Paragraph('Jueves',self.center),Paragraph('Viernes',self.center)],
            [Paragraph('6:00 - 6:45',self.center)],
            [Paragraph('6:45 - 7:30',self.center)],
            [Paragraph('7:35 - 8:20',self.center)],
            [Paragraph('8:20 - 9:05',self.center)],
            [Paragraph('9:05 - 9:50',self.center)],
            [Paragraph('9:50 - 10:35',self.center)]
        ]
        self.validarSemanaLaboratorio(self.nocturnoLabolatorio,0)

        print('Primera linea ----------------')
        # Primera linea lunes

        self.celda1x6(
            self.parametrosLaboratorios,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 1  AND materias_laboratorios.Id_hora_inicial = 13 AND materias_laboratorios.Id_hora_final = 14 AND materias_laboratorios.Estado = "Activo"',
            1,1,1,2,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 1  AND materias_laboratorios.Id_hora_inicial = 13 AND materias_laboratorios.Id_hora_final = 15 AND materias_laboratorios.Estado = "Activo"',
            1,1,1,3,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 1  AND materias_laboratorios.Id_hora_inicial = 13 AND materias_laboratorios.Id_hora_final = 16 AND materias_laboratorios.Estado = "Activo"',
            1,1,1,4,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 1  AND materias_laboratorios.Id_hora_inicial = 13 AND materias_laboratorios.Id_hora_final = 17 AND materias_laboratorios.Estado = "Activo"',
            1,1,1,5,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 1  AND materias_laboratorios.Id_hora_inicial = 13 AND materias_laboratorios.Id_hora_final = 18 AND materias_laboratorios.Estado = "Activo"',
            1,1,1,6,
            1,self.nocturnoLabolatorio
        )

        # Primera linea Martes

        self.celda1x6(
            self.parametrosLaboratorios,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 2  AND materias_laboratorios.Id_hora_inicial = 13 AND materias_laboratorios.Id_hora_final = 14 AND materias_laboratorios.Estado = "Activo"',
            2,1,2,2,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 2  AND materias_laboratorios.Id_hora_inicial = 13 AND materias_laboratorios.Id_hora_final = 15 AND materias_laboratorios.Estado = "Activo"',
            2,1,2,3,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 2  AND materias_laboratorios.Id_hora_inicial = 13 AND materias_laboratorios.Id_hora_final = 16 AND materias_laboratorios.Estado = "Activo"',
            2,1,2,4,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 2  AND materias_laboratorios.Id_hora_inicial = 13 AND materias_laboratorios.Id_hora_final = 17 AND materias_laboratorios.Estado = "Activo"',
            2,1,2,5,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 2  AND materias_laboratorios.Id_hora_inicial = 13 AND materias_laboratorios.Id_hora_final = 18 AND materias_laboratorios.Estado = "Activo"',
            2,1,2,6,
            1,self.nocturnoLabolatorio
        )

        # Primera linea Miercoles

        self.celda1x6(
            self.parametrosLaboratorios,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 3  AND materias_laboratorios.Id_hora_inicial = 13 AND materias_laboratorios.Id_hora_final = 14 AND materias_laboratorios.Estado = "Activo"',
            3,1,3,2,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 3  AND materias_laboratorios.Id_hora_inicial = 13 AND materias_laboratorios.Id_hora_final = 15 AND materias_laboratorios.Estado = "Activo"',
            3,1,3,3,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 3  AND materias_laboratorios.Id_hora_inicial = 13 AND materias_laboratorios.Id_hora_final = 16 AND materias_laboratorios.Estado = "Activo"',
            3,1,3,4,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 3  AND materias_laboratorios.Id_hora_inicial = 13 AND materias_laboratorios.Id_hora_final = 17 AND materias_laboratorios.Estado = "Activo"',
            3,1,3,5,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 3  AND materias_laboratorios.Id_hora_inicial = 13 AND materias_laboratorios.Id_hora_final = 18 AND materias_laboratorios.Estado = "Activo"',
            3,1,3,6,
            1,self.nocturnoLabolatorio
        )

        # Primera linea Jueves

        self.celda1x6(
            self.parametrosLaboratorios,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 4  AND materias_laboratorios.Id_hora_inicial = 13 AND materias_laboratorios.Id_hora_final = 14 AND materias_laboratorios.Estado = "Activo"',
            4,1,4,2,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 4  AND materias_laboratorios.Id_hora_inicial = 13 AND materias_laboratorios.Id_hora_final = 15 AND materias_laboratorios.Estado = "Activo"',
            4,1,4,3,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 4  AND materias_laboratorios.Id_hora_inicial = 13 AND materias_laboratorios.Id_hora_final = 16 AND materias_laboratorios.Estado = "Activo"',
            4,1,4,4,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 4  AND materias_laboratorios.Id_hora_inicial = 13 AND materias_laboratorios.Id_hora_final = 17 AND materias_laboratorios.Estado = "Activo"',
            4,1,4,5,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 4  AND materias_laboratorios.Id_hora_inicial = 13 AND materias_laboratorios.Id_hora_final = 18 AND materias_laboratorios.Estado = "Activo"',
            4,1,4,6,
            1,self.nocturnoLabolatorio
        )

        # Primera linea Viernes

        self.celda1x6(
            self.parametrosLaboratorios,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 5  AND materias_laboratorios.Id_hora_inicial = 13 AND materias_laboratorios.Id_hora_final = 14 AND materias_laboratorios.Estado = "Activo"',
            5,1,5,2,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 5  AND materias_laboratorios.Id_hora_inicial = 13 AND materias_laboratorios.Id_hora_final = 15 AND materias_laboratorios.Estado = "Activo"',
            5,1,5,3,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 5  AND materias_laboratorios.Id_hora_inicial = 13 AND materias_laboratorios.Id_hora_final = 16 AND materias_laboratorios.Estado = "Activo"',
            5,1,5,4,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 5  AND materias_laboratorios.Id_hora_inicial = 13 AND materias_laboratorios.Id_hora_final = 17 AND materias_laboratorios.Estado = "Activo"',
            5,1,5,5,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 5  AND materias_laboratorios.Id_hora_inicial = 13 AND materias_laboratorios.Id_hora_final = 18 AND materias_laboratorios.Estado = "Activo"',
            5,1,5,6,
            1,self.nocturnoLabolatorio
        )

        print('Segunda linea ----------------')
        # Segunda linea lunes

        self.celda1x5(
            self.parametrosLaboratorios,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 1  AND materias_laboratorios.Id_hora_inicial = 14 AND materias_laboratorios.Id_hora_final = 15 AND materias_laboratorios.Estado = "Activo"',
            1,2,1,3,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 1  AND materias_laboratorios.Id_hora_inicial = 14 AND materias_laboratorios.Id_hora_final = 16 AND materias_laboratorios.Estado = "Activo"',
            1,2,1,4,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 1  AND materias_laboratorios.Id_hora_inicial = 14 AND materias_laboratorios.Id_hora_final = 17 AND materias_laboratorios.Estado = "Activo"',
            1,2,1,5,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 1  AND materias_laboratorios.Id_hora_inicial = 14 AND materias_laboratorios.Id_hora_final = 18 AND materias_laboratorios.Estado = "Activo"',
            1,2,1,6,
            2,self.nocturnoLabolatorio
        )

        # Segunda linea Martes

        self.celda1x5(
            self.parametrosLaboratorios,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 2  AND materias_laboratorios.Id_hora_inicial = 14 AND materias_laboratorios.Id_hora_final = 15 AND materias_laboratorios.Estado = "Activo"',
            2,2,2,3,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 2  AND materias_laboratorios.Id_hora_inicial = 14 AND materias_laboratorios.Id_hora_final = 16 AND materias_laboratorios.Estado = "Activo"',
            2,2,2,4,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 2  AND materias_laboratorios.Id_hora_inicial = 14 AND materias_laboratorios.Id_hora_final = 17 AND materias_laboratorios.Estado = "Activo"',
            2,2,2,5,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 2  AND materias_laboratorios.Id_hora_inicial = 14 AND materias_laboratorios.Id_hora_final = 18 AND materias_laboratorios.Estado = "Activo"',
            2,2,2,6,
            2,self.nocturnoLabolatorio
        )

        # Segunda linea Miercoles

        self.celda1x5(
            self.parametrosLaboratorios,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 3  AND materias_laboratorios.Id_hora_inicial = 14 AND materias_laboratorios.Id_hora_final = 15 AND materias_laboratorios.Estado = "Activo"',
            3,2,3,3,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 3  AND materias_laboratorios.Id_hora_inicial = 14 AND materias_laboratorios.Id_hora_final = 16 AND materias_laboratorios.Estado = "Activo"',
            3,2,3,4,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 3  AND materias_laboratorios.Id_hora_inicial = 14 AND materias_laboratorios.Id_hora_final = 17 AND materias_laboratorios.Estado = "Activo"',
            3,2,3,5,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 3  AND materias_laboratorios.Id_hora_inicial = 14 AND materias_laboratorios.Id_hora_final = 18 AND materias_laboratorios.Estado = "Activo"',
            3,2,3,6,
            2,self.nocturnoLabolatorio
        )

        # Segunda linea Jueves

        self.celda1x5(
            self.parametrosLaboratorios,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 4  AND materias_laboratorios.Id_hora_inicial = 14 AND materias_laboratorios.Id_hora_final = 15 AND materias_laboratorios.Estado = "Activo"',
            4,2,4,3,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 4  AND materias_laboratorios.Id_hora_inicial = 14 AND materias_laboratorios.Id_hora_final = 16 AND materias_laboratorios.Estado = "Activo"',
            4,2,4,4,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 4  AND materias_laboratorios.Id_hora_inicial = 14 AND materias_laboratorios.Id_hora_final = 17 AND materias_laboratorios.Estado = "Activo"',
            4,2,4,5,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 4  AND materias_laboratorios.Id_hora_inicial = 14 AND materias_laboratorios.Id_hora_final = 18 AND materias_laboratorios.Estado = "Activo"',
            4,2,4,6,
            2,self.nocturnoLabolatorio
        )

        # Segunda linea Viernes

        self.celda1x5(
            self.parametrosLaboratorios,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 5  AND materias_laboratorios.Id_hora_inicial = 14 AND materias_laboratorios.Id_hora_final = 15 AND materias_laboratorios.Estado = "Activo"',
            5,2,5,3,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 5  AND materias_laboratorios.Id_hora_inicial = 14 AND materias_laboratorios.Id_hora_final = 16 AND materias_laboratorios.Estado = "Activo"',
            5,2,5,4,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 5  AND materias_laboratorios.Id_hora_inicial = 14 AND materias_laboratorios.Id_hora_final = 17 AND materias_laboratorios.Estado = "Activo"',
            5,2,5,5,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 5  AND materias_laboratorios.Id_hora_inicial = 14 AND materias_laboratorios.Id_hora_final = 18 AND materias_laboratorios.Estado = "Activo"',
            5,2,5,6,
            2,self.nocturnoLabolatorio
        )

        print('Tercera linea ----------------')
        # Tercera linea lunes

        self.celda1x4(
            self.parametrosLaboratorios,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 1  AND materias_laboratorios.Id_hora_inicial = 15 AND materias_laboratorios.Id_hora_final = 16 AND materias_laboratorios.Estado = "Activo"',
            1,3,1,4,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 1  AND materias_laboratorios.Id_hora_inicial = 15 AND materias_laboratorios.Id_hora_final = 17 AND materias_laboratorios.Estado = "Activo"',
            1,3,1,5,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 1  AND materias_laboratorios.Id_hora_inicial = 15 AND materias_laboratorios.Id_hora_final = 18 AND materias_laboratorios.Estado = "Activo"',
            1,3,1,6,
            3,self.nocturnoLabolatorio
        )

        # Tercera linea Martes

        self.celda1x4(
            self.parametrosLaboratorios,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 2  AND materias_laboratorios.Id_hora_inicial = 15 AND materias_laboratorios.Id_hora_final = 16 AND materias_laboratorios.Estado = "Activo"',
            2,3,2,4,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 2  AND materias_laboratorios.Id_hora_inicial = 15 AND materias_laboratorios.Id_hora_final = 17 AND materias_laboratorios.Estado = "Activo"',
            2,3,2,5,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 2  AND materias_laboratorios.Id_hora_inicial = 15 AND materias_laboratorios.Id_hora_final = 18 AND materias_laboratorios.Estado = "Activo"',
            2,3,2,6,
            3,self.nocturnoLabolatorio
        )

        # Tercera linea Miercoles

        self.celda1x4(
            self.parametrosLaboratorios,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 3  AND materias_laboratorios.Id_hora_inicial = 15 AND materias_laboratorios.Id_hora_final = 16 AND materias_laboratorios.Estado = "Activo"',
            3,3,3,4,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 3  AND materias_laboratorios.Id_hora_inicial = 15 AND materias_laboratorios.Id_hora_final = 17 AND materias_laboratorios.Estado = "Activo"',
            3,3,3,5,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 3  AND materias_laboratorios.Id_hora_inicial = 15 AND materias_laboratorios.Id_hora_final = 18 AND materias_laboratorios.Estado = "Activo"',
            3,3,3,6,
            3,self.nocturnoLabolatorio
        )

        # Tercera linea Jueves

        self.celda1x4(
            self.parametrosLaboratorios,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 4  AND materias_laboratorios.Id_hora_inicial = 15 AND materias_laboratorios.Id_hora_final = 16 AND materias_laboratorios.Estado = "Activo"',
            4,3,4,4,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 4  AND materias_laboratorios.Id_hora_inicial = 15 AND materias_laboratorios.Id_hora_final = 17 AND materias_laboratorios.Estado = "Activo"',
            4,3,4,5,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 4  AND materias_laboratorios.Id_hora_inicial = 15 AND materias_laboratorios.Id_hora_final = 18 AND materias_laboratorios.Estado = "Activo"',
            4,3,4,6,
            3,self.nocturnoLabolatorio
        )

        # Tercera linea Viernes

        self.celda1x4(
            self.parametrosLaboratorios,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 5  AND materias_laboratorios.Id_hora_inicial = 15 AND materias_laboratorios.Id_hora_final = 16 AND materias_laboratorios.Estado = "Activo"',
            5,3,5,4,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 5  AND materias_laboratorios.Id_hora_inicial = 15 AND materias_laboratorios.Id_hora_final = 17 AND materias_laboratorios.Estado = "Activo"',
            5,3,5,5,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 5  AND materias_laboratorios.Id_hora_inicial = 15 AND materias_laboratorios.Id_hora_final = 18 AND materias_laboratorios.Estado = "Activo"',
            5,3,5,6,
            3,self.nocturnoLabolatorio
        )

        print('Cuarta linea ----------------')
        # Cuarta linea lunes

        self.celda1x3(
            self.parametrosLaboratorios,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 1  AND materias_laboratorios.Id_hora_inicial = 16 AND materias_laboratorios.Id_hora_final = 17 AND materias_laboratorios.Estado = "Activo"',
            1,4,1,5,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 1  AND materias_laboratorios.Id_hora_inicial = 16 AND materias_laboratorios.Id_hora_final = 18 AND materias_laboratorios.Estado = "Activo"',
            1,4,1,6,
            4,self.nocturnoLabolatorio
        )

        # Cuarta linea Martes

        self.celda1x3(
            self.parametrosLaboratorios,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 2  AND materias_laboratorios.Id_hora_inicial = 16 AND materias_laboratorios.Id_hora_final = 17 AND materias_laboratorios.Estado = "Activo"',
            2,4,2,5,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 2  AND materias_laboratorios.Id_hora_inicial = 16 AND materias_laboratorios.Id_hora_final = 18 AND materias_laboratorios.Estado = "Activo"',
            2,4,2,6,
            4,self.nocturnoLabolatorio
        )

        # Cuarta linea Miercoles

        self.celda1x3(
            self.parametrosLaboratorios,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 3  AND materias_laboratorios.Id_hora_inicial = 16 AND materias_laboratorios.Id_hora_final = 17 AND materias_laboratorios.Estado = "Activo"',
            3,4,3,5,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 3  AND materias_laboratorios.Id_hora_inicial = 16 AND materias_laboratorios.Id_hora_final = 18 AND materias_laboratorios.Estado = "Activo"',
            3,4,3,6,
            4,self.nocturnoLabolatorio
        )

        # Cuarta linea Jueves

        self.celda1x3(
            self.parametrosLaboratorios,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 4  AND materias_laboratorios.Id_hora_inicial = 16 AND materias_laboratorios.Id_hora_final = 17 AND materias_laboratorios.Estado = "Activo"',
            4,4,4,5,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 4  AND materias_laboratorios.Id_hora_inicial = 16 AND materias_laboratorios.Id_hora_final = 18 AND materias_laboratorios.Estado = "Activo"',
            4,4,4,6,
            4,self.nocturnoLabolatorio
        )

        # Cuarta linea Viernes

        self.celda1x3(
            self.parametrosLaboratorios,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 5  AND materias_laboratorios.Id_hora_inicial = 16 AND materias_laboratorios.Id_hora_final = 17 AND materias_laboratorios.Estado = "Activo"',
            5,4,5,5,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 5  AND materias_laboratorios.Id_hora_inicial = 16 AND materias_laboratorios.Id_hora_final = 18 AND materias_laboratorios.Estado = "Activo"',
            5,4,5,6,
            4,self.nocturnoLabolatorio
        )

        print('Quinta linea ----------------')
        # Quinta linea lunes

        self.celda1x2(
            self.parametrosLaboratorios,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 1  AND materias_laboratorios.Id_hora_inicial = 17 AND materias_laboratorios.Id_hora_final = 18 AND materias_laboratorios.Estado = "Activo"',
            1,5,1,6,
            5,self.nocturnoLabolatorio
        )

        # Quinta linea Martes

        self.celda1x2(
            self.parametrosLaboratorios,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 2  AND materias_laboratorios.Id_hora_inicial = 17 AND materias_laboratorios.Id_hora_final = 18 AND materias_laboratorios.Estado = "Activo"',
            2,5,2,6,
            5,self.nocturnoLabolatorio
        )

        # Quinta linea Miercoles

        self.celda1x2(
            self.parametrosLaboratorios,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 3  AND materias_laboratorios.Id_hora_inicial = 17 AND materias_laboratorios.Id_hora_final = 18 AND materias_laboratorios.Estado = "Activo"',
            3,5,3,6,
            5,self.nocturnoLabolatorio
        )

        # Quinta linea Jueves

        self.celda1x2(
            self.parametrosLaboratorios,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 4  AND materias_laboratorios.Id_hora_inicial = 17 AND materias_laboratorios.Id_hora_final = 18 AND materias_laboratorios.Estado = "Activo"',
            4,5,4,6,
            5,self.nocturnoLabolatorio
        )

        # Quinta linea Viernes

        self.celda1x2(
            self.parametrosLaboratorios,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_laboratorios INNER JOIN unidad_curricular on unidad_curricular.Id = materias_laboratorios.materia  WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Id_semana = 5  AND materias_laboratorios.Id_hora_inicial = 17 AND materias_laboratorios.Id_hora_final = 18 AND materias_laboratorios.Estado = "Activo"',
            5,5,5,6,
            5,self.nocturnoLabolatorio
        )

        return self.nocturnoLabolatorio

    def obtenertablaDocenteDiurnoLaboratorio(self):
        self.tablaInformacionLaboratorio = [
            [Paragraph('UNIDAD CURRICULAR',self.center),Paragraph('NOMBRE DEL DOCENTE',self.center),Paragraph('TELEFONO DE CONTACTO',self.center)]
        ]
        self.tablaLaboratorio = self.conexion(
            'SELECT DISTINCT unidad_curricular.UnidadCurricular, docente.NombreApellido, docente.Telefono FROM materias_laboratorios INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_laboratorios.materia INNER JOIN docente ON docente.Id = materias_laboratorios.Id_docente WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Estado = "Activo"',
            self.parametrosLaboratorios).fetchall()
        for row in self.tablaLaboratorio:
            self.tablaInformacionLaboratorio.append(row)
            self.counterLaboratorio = self.counterLaboratorio + 1
            print(self.counterLaboratorio)
    
        return self.tablaInformacionLaboratorio

    
    def obtenertablaDocenteNocturnoLaboratorio(self):
        self.tablaInformacionLaboratorio = [
            [Paragraph('UNIDAD CURRICULAR',self.center),Paragraph('NOMBRE DEL DOCENTE',self.center),Paragraph('TELEFONO DE CONTACTO',self.center)]
        ]
        self.tablaLaboratorio = self.conexion(
            'SELECT DISTINCT unidad_curricular.UnidadCurricular, docente.NombreApellido, docente.Telefono FROM materias_laboratorios INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_laboratorios.materia INNER JOIN docente ON docente.Id = materias_laboratorios.Id_docente WHERE materias_laboratorios.Id_laboratorio = ? AND materias_laboratorios.Id_lapso_academico = ? AND materias_laboratorios.Id_modalidad = ? AND materias_laboratorios.Estado = "Activo"',
            self.parametrosLaboratorios).fetchall()
        for row in self.tablaLaboratorio:
            self.tablaInformacionLaboratorio.append(row)
            self.counterLaboratorio = self.counterLaboratorio + 1
            print(self.counterLaboratorio)
        
        return self.tablaInformacionLaboratorio
    
    def configuracion(self):
        self.new = tk.Toplevel()
        self.new.title('Configuracion Horarios')
        self.new.resizable(width=0, height=0)
        self.new.geometry('300x240')
        self.new.iconbitmap(uptpc)

        self.container2 = ttk.Labelframe(self.new)
        self.container2.grid(column=0,row=0,padx=15,pady=5)

        self.treeTitulo = ttk.Treeview(self.container2, columns=['#1'],show='headings',height=2)
        self.treeTitulo.grid(row=0,column=0,padx=5,pady=5)
        self.treeTitulo.heading('#1', text = 'Titulo Horario',)
        self.treeTitulo.column('#1', width=250)

        ttk.Label(self.container2, text='Titulo de Horario:').grid(row=1,column=0,padx=5,pady=5)
        self.titulo = ttk.Entry(self.container2,width=40)
        self.titulo.grid(row=2,column=0,padx=5,pady=5)
        self.titulo.focus()

        ttk.Button(self.container2,width=40,text='ACTUALIZAR', command=self.editarTitulo).grid(row=3,column=0,padx=5,pady=5)
        ttk.Button(self.container2,width=40,text='CANCELAR', command=self.cancelar).grid(row=4,column=0,padx=5,pady=5)

        self.MostrarTitulo()
        self.new.mainloop()

    def cancelar(self):
        self.new.destroy()

    def editarTitulo(self):
        if len(self.titulo.get()) != 0:
            if messagebox.askyesno('Edit','¿Realmente desea cambiar el nombre?',parent=self.new):
                self.query = 'UPDATE titulo SET Titulo = ?'
                self.parametros = (self.titulo.get())
                self.conexion(self.query,(self.parametros,))
                self.MostrarTitulo()
                self.titulo.delete(0, tk.END)
                messagebox.showinfo(title='Info', message='Titulo actualizado.',parent=self.new)
            else:
                self.MostrarTitulo()
        else:
            messagebox.showwarning(title='Warning', message='Introdusca un valor.',parent=self.new)

    def obtenerTitulo(self):
        self.obtener = self.conexion('SELECT * FROM titulo').fetchone()
        return self.obtener[0]