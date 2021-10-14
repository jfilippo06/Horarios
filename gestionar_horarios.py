import tkinter as tk
from tkinter import ttk
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
import json

class Horarios(tk.Toplevel):
    def __init__(self,master):
        super().__init__(master)
        # Config:
        self.title('Horarios')
        self.geometry('460x615')
        self.resizable(width=0, height=0)
        self.iconbitmap(uptpc)

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(pady=0,padx=0,expand=True)

        # create frames
        self.noteHorariosClases = ttk.Frame(self.notebook, width=400, height=400)
        self.noteHorariosLaboratorios = ttk.Frame(self.notebook,width=400, height=400)

        # create frames
        self.noteHorariosClases.pack(fill='both', expand=True)
        self.noteHorariosLaboratorios.pack(fill='both', expand=True)

        # add frames to notebook
        self.notebook.add(self.noteHorariosClases, text='Horarios de clases')
        self.notebook.add(self.noteHorariosLaboratorios, text='Horarios de laboratorios')

        ttk.Label(self.noteHorariosClases, text='GENERAR HORARIO',font=('Helvetica',14)).place(x=130,y=5)
        # LapsoAcademico
        self.container = ttk.Labelframe(self.noteHorariosClases)
        self.container.grid(column=0,row=0,padx=15, pady=30)

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
        self.treeModalidad.configure(yscroll=self.scrollbarLapsoAcademico.set)
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

        self.frameContenedor = ttk.Labelframe(self.noteHorariosClases)
        self.frameContenedor.grid(column=0, row=1)

        ttk.Label(self.frameContenedor, text='Inicio clase').grid(column=0, row=0,pady=5,padx=5)
        self.entryInicio = ttk.Entry(self.frameContenedor, state=DISABLED)
        self.entryInicio.grid(column=1,row=0,pady=5,padx=5)
        self.activarInicio = ttk.Button(self.frameContenedor, text='ACTIVAR', command=self.botonActivarInicio).grid(column=2,row=0)
        self.desactivarInicio = ttk.Button(self.frameContenedor, text='DESACTIVAR', command=self.botonDesactivarInicio).grid(column=3,row=0)

        ttk.Label(self.frameContenedor, text='Inicio Pausa vacacional').grid(column=0, row=1,pady=5,padx=5)
        self.entryPausa = ttk.Entry(self.frameContenedor, state=DISABLED)
        self.entryPausa.grid(column=1,row=1,pady=5,padx=5)
        self.activarPausa = ttk.Button(self.frameContenedor, text='ACTIVAR', command=self.botonActivarIPausa).grid(column=2,row=1)
        self.desactivarPausa = ttk.Button(self.frameContenedor, text='DESACTIVAR', command=self.botonDesactivarPausa).grid(column=3,row=1)

        ttk.Label(self.frameContenedor, text='Rinicio clase').grid(column=0, row=2,pady=5,padx=5)
        self.entryReinicio = ttk.Entry(self.frameContenedor, state=DISABLED)
        self.entryReinicio.grid(column=1,row=2,pady=5,padx=5)
        self.activarReinicio = ttk.Button(self.frameContenedor, text='ACTIVAR', command=self.botonActivarReinicio).grid(column=2,row=2)
        self.desactivarReinicio = ttk.Button(self.frameContenedor, text='DESACTIVAR', command=self.botonDesactivarReinicio).grid(column=3,row=2)

        ttk.Label(self.frameContenedor, text='Culminacion clases').grid(column=0, row=3,pady=5,padx=5)
        self.entryCulminacion = ttk.Entry(self.frameContenedor, state=DISABLED)
        self.entryCulminacion.grid(column=1,row=3,pady=5,padx=5)
        self.activarCulminacion = ttk.Button(self.frameContenedor, text='ACTIVAR', command=self.botonActivarCuminacion).grid(column=2,row=3)
        self.desactivarCulminacion = ttk.Button(self.frameContenedor, text='DESACTIVAR', command=self.botonDesactivarCulminacion).grid(column=3,row=3)

        ttk.Label(self.frameContenedor, text='Inicio clase').grid(column=0, row=4,pady=5,padx=5)
        self.entryAula = ttk.Entry(self.frameContenedor, state=DISABLED)
        self.entryAula.grid(column=1,row=4,pady=5,padx=5)
        self.activarAula = ttk.Button(self.frameContenedor, text='ACTIVAR', command=self.botonActivarAula).grid(column=2,row=4)
        self.desactivarAula = ttk.Button(self.frameContenedor, text='DESACTIVAR', command=self.botonDesactivarAula).grid(column=3,row=4)

        ttk.Button(self.noteHorariosClases, text='GENERAR HORARIO',command=self.generarHorarioClases).grid(column=0,row=2,pady=10)

        self.MostrarLapsoAcademico()
        self.MostrarModalidad()
        self.MostrarCohorte()
        self.MostrarTrayecto()
        self.MostrarTrimestre()
        self.MostrarSeccion()

        self.width, self.heigth = A4
        self.styles = getSampleStyleSheet()
        self.center = self.styles["BodyText"]
        self.center.alignment = TA_CENTER

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
    
    def botonActivarInicio(self):
        self.entryInicio.config(state=NORMAL)
        self.entryInicio.focus()

    def botonDesactivarInicio(self):
        self.entryInicio.config(state=DISABLED)

    def botonActivarIPausa(self):
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

    def MostrarLapsoAcademico(self):
        self.rows = self.TraerDatos("SELECT * FROM lapso_academico")
        for row in self.rows:
            self.treeLapsoAcademico.insert('',tk.END,values=row)

    def MostrarModalidad(self):
        self.rows = self.TraerDatos("SELECT * FROM modalidad")
        for row in self.rows:
            self.treeModalidad.insert('',tk.END,values=row)
            
    def MostrarCohorte(self):
        self.rows = self.TraerDatos("SELECT * FROM cohorte")
        for row in self.rows:
            self.treeCohorte.insert('',tk.END,values=row)
            
    def MostrarTrayecto(self):
        self.rows = self.TraerDatos("SELECT * FROM trayecto")
        for row in self.rows:
            self.treeTrayecto.insert('',tk.END,values=row)
            
    def MostrarTrimestre(self):
        self.rows = self.TraerDatos("SELECT * FROM trimestre")
        for row in self.rows:
            self.treeTrimestre.insert('',tk.END,values=row)
            
    def MostrarSeccion(self):
        self.rows = self.TraerDatos("SELECT * FROM seccion")
        for row in self.rows:
            self.treeSeccion.insert('',tk.END,values=row)
            
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

    def generarHorarioClases(self):
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

        self.pdf = canvas.Canvas('Prueba.pdf', pagesize = landscape(A4))
        self.pdf.setFontSize(10)
        self.pdf.drawString(301,550,'PNF EN INFORMÁTICA  Lapso Académico ' + self.lapso + ' (Cohorte' + self.cohorte + ')')
        self.pdf.line(299,549,605,549)
        self.pdf.drawString(388,529,'TRAYECTO ' + self.trayecto + ' TRIMESTRE ' + self.trimestre)
        self.verificarLinea()
        self.pdf.drawString(425,504, 'SECCIÓN: ' + self.seccion)

        self.validarTree()
        self.validarCelda()
        self.validarModalidad()

        self.pdf.save()
        
        self.setStyles.clear()
        self.setStyles.append(('GRID',(0,0),(-1,-1),0.5,colors.black))
        self.setStyles.append(('BBOX',(0,0),(-1,-1),0.5,colors.black))
        self.setStyles.append(('VALIGN',(0,0),(-1,-1),'MIDDLE'))
        self.setStyles.append(('ALIGN',(0,0),(-1,-1),'CENTER'))

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

    def obtenerHorarioDiurno(self):
        self.diurno = [
            [Paragraph('bloque de horas mañana',self.center),Paragraph('Lunes',self.center),Paragraph('Martes',self.center),Paragraph('Miercoles',self.center),Paragraph('Jueves',self.center),Paragraph('Viernes',self.center)],
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

        print('Primera linea ----------------')
        # Primera linea lunes
        self.celda1x6(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 1 AND materias_asignadas.Id_hora_inicial = 1 AND materias_asignadas.Id_hora_final = 2',
            1,1,1,2,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 1 AND materias_asignadas.Id_hora_inicial = 1 AND materias_asignadas.Id_hora_final = 3',
            1,1,1,3,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 1 AND materias_asignadas.Id_hora_inicial = 1 AND materias_asignadas.Id_hora_final = 4',
            1,1,1,4,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 1 AND materias_asignadas.Id_hora_inicial = 1 AND materias_asignadas.Id_hora_final = 5',
            1,1,1,5,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 1 AND materias_asignadas.Id_hora_inicial = 1 AND materias_asignadas.Id_hora_final = 6',
            1,1,1,6,
            1,self.diurno
        )

        # Primera linea Martes
        self.celda1x6(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 2 AND materias_asignadas.Id_hora_inicial = 1 AND materias_asignadas.Id_hora_final = 2',
            2,1,2,2,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 2 AND materias_asignadas.Id_hora_inicial = 1 AND materias_asignadas.Id_hora_final = 3',
            2,1,2,3,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 2 AND materias_asignadas.Id_hora_inicial = 1 AND materias_asignadas.Id_hora_final = 4',
            2,1,2,4,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 2 AND materias_asignadas.Id_hora_inicial = 1 AND materias_asignadas.Id_hora_final = 5',
            2,1,2,5,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 2 AND materias_asignadas.Id_hora_inicial = 1 AND materias_asignadas.Id_hora_final = 6',
            2,1,2,6,
            1,self.diurno
        ) 
        
        # Primera linea Miercoles
        self.celda1x6(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 3 AND materias_asignadas.Id_hora_inicial = 1 AND materias_asignadas.Id_hora_final = 2',
            3,1,3,2,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 3 AND materias_asignadas.Id_hora_inicial = 1 AND materias_asignadas.Id_hora_final = 3',
            3,1,3,3,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 3 AND materias_asignadas.Id_hora_inicial = 1 AND materias_asignadas.Id_hora_final = 4',
            3,1,3,4,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 3 AND materias_asignadas.Id_hora_inicial = 1 AND materias_asignadas.Id_hora_final = 5',
            3,1,3,5,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 3 AND materias_asignadas.Id_hora_inicial = 1 AND materias_asignadas.Id_hora_final = 6',
            3,1,3,6,
            1,self.diurno
        )

        # Primera linea Jueves
        self.celda1x6(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 4 AND materias_asignadas.Id_hora_inicial = 1 AND materias_asignadas.Id_hora_final = 2',
            4,1,4,2,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 4 AND materias_asignadas.Id_hora_inicial = 1 AND materias_asignadas.Id_hora_final = 3',
            4,1,4,3,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 4 AND materias_asignadas.Id_hora_inicial = 1 AND materias_asignadas.Id_hora_final = 4',
            4,1,4,4,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 4 AND materias_asignadas.Id_hora_inicial = 1 AND materias_asignadas.Id_hora_final = 5',
            4,1,4,5,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 4 AND materias_asignadas.Id_hora_inicial = 1 AND materias_asignadas.Id_hora_final = 6',
            4,1,4,6,
            1,self.diurno
        )

        # Primera linea Viernes
        self.celda1x6(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 5 AND materias_asignadas.Id_hora_inicial = 1 AND materias_asignadas.Id_hora_final = 2',
            5,1,5,2,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 5 AND materias_asignadas.Id_hora_inicial = 1 AND materias_asignadas.Id_hora_final = 3',
            5,1,5,3,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 5 AND materias_asignadas.Id_hora_inicial = 1 AND materias_asignadas.Id_hora_final = 4',
            5,1,5,4,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 5 AND materias_asignadas.Id_hora_inicial = 1 AND materias_asignadas.Id_hora_final = 5',
            5,1,5,5,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 5 AND materias_asignadas.Id_hora_inicial = 1 AND materias_asignadas.Id_hora_final = 6',
            5,1,5,6,
            1,self.diurno
        )
        print('Segunda linea ----------------')

        # Segunda linea lunes
        self.celda1x5(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 1 AND materias_asignadas.Id_hora_inicial = 2 AND materias_asignadas.Id_hora_final = 3',
            1,2,1,3,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 1 AND materias_asignadas.Id_hora_inicial = 2 AND materias_asignadas.Id_hora_final = 4',
            1,2,1,4,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 1 AND materias_asignadas.Id_hora_inicial = 2 AND materias_asignadas.Id_hora_final = 5',
            1,2,1,5,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 1 AND materias_asignadas.Id_hora_inicial = 2 AND materias_asignadas.Id_hora_final = 6',
            1,2,1,6,
            2,self.diurno
        )

        # Segunda linea Martes
        self.celda1x5(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 2 AND materias_asignadas.Id_hora_inicial = 2 AND materias_asignadas.Id_hora_final = 3',
            2,2,2,3,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 2 AND materias_asignadas.Id_hora_inicial = 2 AND materias_asignadas.Id_hora_final = 4',
            2,2,2,4,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 2 AND materias_asignadas.Id_hora_inicial = 2 AND materias_asignadas.Id_hora_final = 5',
            2,2,2,5,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 2 AND materias_asignadas.Id_hora_inicial = 2 AND materias_asignadas.Id_hora_final = 6',
            2,2,2,6,
            2,self.diurno
        )

        # Segunda linea Miercoles
        self.celda1x5(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 3 AND materias_asignadas.Id_hora_inicial = 2 AND materias_asignadas.Id_hora_final = 3',
            3,2,3,3,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 3 AND materias_asignadas.Id_hora_inicial = 2 AND materias_asignadas.Id_hora_final = 4',
            3,2,3,4,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 3 AND materias_asignadas.Id_hora_inicial = 2 AND materias_asignadas.Id_hora_final = 5',
            3,2,3,5,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 3 AND materias_asignadas.Id_hora_inicial = 2 AND materias_asignadas.Id_hora_final = 6',
            3,2,3,6,
            2,self.diurno
        )

        # Segunda linea Jueves
        self.celda1x5(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 4 AND materias_asignadas.Id_hora_inicial = 2 AND materias_asignadas.Id_hora_final = 3',
            4,2,4,3,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 4 AND materias_asignadas.Id_hora_inicial = 2 AND materias_asignadas.Id_hora_final = 4',
            4,2,4,4,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 4 AND materias_asignadas.Id_hora_inicial = 2 AND materias_asignadas.Id_hora_final = 5',
            4,2,4,5,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 4 AND materias_asignadas.Id_hora_inicial = 2 AND materias_asignadas.Id_hora_final = 6',
            4,2,4,6,
            2,self.diurno
        )

        # Segunda linea Vierves
        self.celda1x5(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 5 AND materias_asignadas.Id_hora_inicial = 2 AND materias_asignadas.Id_hora_final = 3',
            5,2,5,3,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 5 AND materias_asignadas.Id_hora_inicial = 2 AND materias_asignadas.Id_hora_final = 4',
            5,2,5,4,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 5 AND materias_asignadas.Id_hora_inicial = 2 AND materias_asignadas.Id_hora_final = 5',
            5,2,5,5,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 5 AND materias_asignadas.Id_hora_inicial = 2 AND materias_asignadas.Id_hora_final = 6',
            5,2,5,6,
            2,self.diurno
        )

        print('Tercera linea ----------------')

        # Tercera linea lunes
        self.celda1x4(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 1 AND materias_asignadas.Id_hora_inicial = 3 AND materias_asignadas.Id_hora_final = 4',
            1,3,1,4,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 1 AND materias_asignadas.Id_hora_inicial = 3 AND materias_asignadas.Id_hora_final = 5',
            1,3,1,5,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 1 AND materias_asignadas.Id_hora_inicial = 3 AND materias_asignadas.Id_hora_final = 6',
            1,3,1,6,
            3,self.diurno
        )

         # Tercera linea Martes
        self.celda1x4(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 2 AND materias_asignadas.Id_hora_inicial = 3 AND materias_asignadas.Id_hora_final = 4',
            2,3,2,4,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 2 AND materias_asignadas.Id_hora_inicial = 3 AND materias_asignadas.Id_hora_final = 5',
            2,3,2,5,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 2 AND materias_asignadas.Id_hora_inicial = 3 AND materias_asignadas.Id_hora_final = 6',
            2,3,2,6,
            3,self.diurno
        )

         # Tercera linea Miercoles
        self.celda1x4(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 3 AND materias_asignadas.Id_hora_inicial = 3 AND materias_asignadas.Id_hora_final = 4',
            3,3,3,4,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 3 AND materias_asignadas.Id_hora_inicial = 3 AND materias_asignadas.Id_hora_final = 5',
            3,3,3,5,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 3 AND materias_asignadas.Id_hora_inicial = 3 AND materias_asignadas.Id_hora_final = 6',
            3,3,3,6,
            3,self.diurno
        )

         # Tercera linea Jueves
        self.celda1x4(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 4 AND materias_asignadas.Id_hora_inicial = 3 AND materias_asignadas.Id_hora_final = 4',
            4,3,4,4,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 4 AND materias_asignadas.Id_hora_inicial = 3 AND materias_asignadas.Id_hora_final = 5',
            4,3,4,5,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 4 AND materias_asignadas.Id_hora_inicial = 3 AND materias_asignadas.Id_hora_final = 6',
            4,3,4,6,
            3,self.diurno
        )

         # Tercera linea Viernes
        self.celda1x4(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 5 AND materias_asignadas.Id_hora_inicial = 3 AND materias_asignadas.Id_hora_final = 4',
            5,3,5,4,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 5 AND materias_asignadas.Id_hora_inicial = 3 AND materias_asignadas.Id_hora_final = 5',
            5,3,5,5,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 5 AND materias_asignadas.Id_hora_inicial = 3 AND materias_asignadas.Id_hora_final = 6',
            5,3,5,6,
            3,self.diurno
        )

        print('Cuarta linea ----------------')

        # Cuarta linea lunes
        self.celda1x3(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 1 AND materias_asignadas.Id_hora_inicial = 4 AND materias_asignadas.Id_hora_final = 5',
            1,4,1,5,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 1 AND materias_asignadas.Id_hora_inicial = 4 AND materias_asignadas.Id_hora_final = 6',
            1,4,1,6,
            4,self.diurno
        )

        # Cuarta linea Martes
        self.celda1x3(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 2 AND materias_asignadas.Id_hora_inicial = 4 AND materias_asignadas.Id_hora_final = 5',
            2,4,2,5,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 2 AND materias_asignadas.Id_hora_inicial = 4 AND materias_asignadas.Id_hora_final = 6',
            2,4,2,6,
            4,self.diurno
        )

        # Cuarta linea Miercoles
        self.celda1x3(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 3 AND materias_asignadas.Id_hora_inicial = 4 AND materias_asignadas.Id_hora_final = 5',
            3,4,3,5,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 3 AND materias_asignadas.Id_hora_inicial = 4 AND materias_asignadas.Id_hora_final = 6',
            3,4,3,6,
            4,self.diurno
        )

        # Cuarta linea Jueves
        self.celda1x3(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 4 AND materias_asignadas.Id_hora_inicial = 4 AND materias_asignadas.Id_hora_final = 5',
            4,4,4,5,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 4 AND materias_asignadas.Id_hora_inicial = 4 AND materias_asignadas.Id_hora_final = 6',
            4,4,4,6,
            4,self.diurno
        )

        # Cuarta linea Viernes
        self.celda1x3(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 5 AND materias_asignadas.Id_hora_inicial = 4 AND materias_asignadas.Id_hora_final = 5',
            5,4,5,5,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 5 AND materias_asignadas.Id_hora_inicial = 4 AND materias_asignadas.Id_hora_final = 6',
            5,4,5,6,
            4,self.diurno
        )

        print('Quinta linea ----------------')

        # Quinta linea lunes
        self.celda1x2(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 1 AND materias_asignadas.Id_hora_inicial = 5 AND materias_asignadas.Id_hora_final = 6',
            1,5,1,6,
            5,self.diurno
        )

        # Quinta linea Martes
        self.celda1x2(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 2 AND materias_asignadas.Id_hora_inicial = 5 AND materias_asignadas.Id_hora_final = 6',
            2,5,2,6,
            5,self.diurno
        )

        # Quinta linea Miercoles
        self.celda1x2(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 3 AND materias_asignadas.Id_hora_inicial = 5 AND materias_asignadas.Id_hora_final = 6',
            3,5,3,6,
            5,self.diurno
        )

        # Quinta linea Jueves
        self.celda1x2(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 4 AND materias_asignadas.Id_hora_inicial = 5 AND materias_asignadas.Id_hora_final = 6',
            4,5,4,6,
            5,self.diurno
        )

        # Quinta linea Viernes
        self.celda1x2(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 5 AND materias_asignadas.Id_hora_inicial = 5 AND materias_asignadas.Id_hora_final = 6',
            5,5,5,6,
            5,self.diurno
        )

        print('Septima linea ----------------')

        # Septima linea lunes
        self.celda1x6(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 1 AND materias_asignadas.Id_hora_inicial = 7 AND materias_asignadas.Id_hora_final = 8',
            1,7,1,8,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 1 AND materias_asignadas.Id_hora_inicial = 7 AND materias_asignadas.Id_hora_final = 9',
            1,7,1,9,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 1 AND materias_asignadas.Id_hora_inicial = 7 AND materias_asignadas.Id_hora_final = 10',
            1,7,1,10,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 1 AND materias_asignadas.Id_hora_inicial = 7 AND materias_asignadas.Id_hora_final = 11',
            1,7,1,11,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 1 AND materias_asignadas.Id_hora_inicial = 7 AND materias_asignadas.Id_hora_final = 12',
            1,7,1,12,
            7,self.diurno
        )

        # Septima linea Martes
        self.celda1x6(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 2 AND materias_asignadas.Id_hora_inicial = 7 AND materias_asignadas.Id_hora_final = 8',
            2,7,2,8,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 2 AND materias_asignadas.Id_hora_inicial = 7 AND materias_asignadas.Id_hora_final = 9',
            2,7,2,9,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 2 AND materias_asignadas.Id_hora_inicial = 7 AND materias_asignadas.Id_hora_final = 10',
            2,7,2,10,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 2 AND materias_asignadas.Id_hora_inicial = 7 AND materias_asignadas.Id_hora_final = 11',
            2,7,2,11,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 2 AND materias_asignadas.Id_hora_inicial = 7 AND materias_asignadas.Id_hora_final = 12',
            2,7,2,12,
            7,self.diurno
        )

        # Septima linea Miercoles
        self.celda1x6(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 3 AND materias_asignadas.Id_hora_inicial = 7 AND materias_asignadas.Id_hora_final = 8',
            3,7,3,8,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 3 AND materias_asignadas.Id_hora_inicial = 7 AND materias_asignadas.Id_hora_final = 9',
            3,7,3,9,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 3 AND materias_asignadas.Id_hora_inicial = 7 AND materias_asignadas.Id_hora_final = 10',
            3,7,3,10,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 3 AND materias_asignadas.Id_hora_inicial = 7 AND materias_asignadas.Id_hora_final = 11',
            3,7,3,11,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 3 AND materias_asignadas.Id_hora_inicial = 7 AND materias_asignadas.Id_hora_final = 12',
            3,7,3,12,
            7,self.diurno
        )

        # Septima linea Jueves
        self.celda1x6(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 4 AND materias_asignadas.Id_hora_inicial = 7 AND materias_asignadas.Id_hora_final = 8',
            4,7,4,8,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 4 AND materias_asignadas.Id_hora_inicial = 7 AND materias_asignadas.Id_hora_final = 9',
            4,7,4,9,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 4 AND materias_asignadas.Id_hora_inicial = 7 AND materias_asignadas.Id_hora_final = 10',
            4,7,4,10,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 4 AND materias_asignadas.Id_hora_inicial = 7 AND materias_asignadas.Id_hora_final = 11',
            4,7,4,11,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 4 AND materias_asignadas.Id_hora_inicial = 7 AND materias_asignadas.Id_hora_final = 12',
            4,7,4,12,
            7,self.diurno
        )

        # Septima linea Viernes
        self.celda1x6(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 5 AND materias_asignadas.Id_hora_inicial = 7 AND materias_asignadas.Id_hora_final = 8',
            5,7,5,8,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 5 AND materias_asignadas.Id_hora_inicial = 7 AND materias_asignadas.Id_hora_final = 9',
            5,7,5,9,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 5 AND materias_asignadas.Id_hora_inicial = 7 AND materias_asignadas.Id_hora_final = 10',
            5,7,5,10,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 5 AND materias_asignadas.Id_hora_inicial = 7 AND materias_asignadas.Id_hora_final = 11',
            5,7,5,11,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 5 AND materias_asignadas.Id_hora_inicial = 7 AND materias_asignadas.Id_hora_final = 12',
            5,7,5,12,
            7,self.diurno
        )

        print('Octava linea ----------------')

        # Octava linea lunes
        self.celda1x5(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 1 AND materias_asignadas.Id_hora_inicial = 8 AND materias_asignadas.Id_hora_final = 9',
            1,8,1,9,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 1 AND materias_asignadas.Id_hora_inicial = 8 AND materias_asignadas.Id_hora_final = 10',
            1,8,1,10,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 1 AND materias_asignadas.Id_hora_inicial = 8 AND materias_asignadas.Id_hora_final = 11',
            1,8,1,11,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 1 AND materias_asignadas.Id_hora_inicial = 8 AND materias_asignadas.Id_hora_final = 12',
            1,8,1,12,
            8,self.diurno
        )

        # Octava linea Martes
        self.celda1x5(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 2 AND materias_asignadas.Id_hora_inicial = 8 AND materias_asignadas.Id_hora_final = 9',
            2,8,2,9,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 2 AND materias_asignadas.Id_hora_inicial = 8 AND materias_asignadas.Id_hora_final = 10',
            2,8,2,10,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 2 AND materias_asignadas.Id_hora_inicial = 8 AND materias_asignadas.Id_hora_final = 11',
            2,8,2,11,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 2 AND materias_asignadas.Id_hora_inicial = 8 AND materias_asignadas.Id_hora_final = 12',
            2,8,2,12,
            8,self.diurno
        )

        # Octava linea Miercoles
        self.celda1x5(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 3 AND materias_asignadas.Id_hora_inicial = 8 AND materias_asignadas.Id_hora_final = 9',
            3,8,3,9,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 3 AND materias_asignadas.Id_hora_inicial = 8 AND materias_asignadas.Id_hora_final = 10',
            3,8,3,10,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 3 AND materias_asignadas.Id_hora_inicial = 8 AND materias_asignadas.Id_hora_final = 11',
            3,8,3,11,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 3 AND materias_asignadas.Id_hora_inicial = 8 AND materias_asignadas.Id_hora_final = 12',
            3,8,3,12,
            8,self.diurno
        )

        # Octava linea jueves
        self.celda1x5(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 4 AND materias_asignadas.Id_hora_inicial = 8 AND materias_asignadas.Id_hora_final = 9',
            4,8,4,9,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 4 AND materias_asignadas.Id_hora_inicial = 8 AND materias_asignadas.Id_hora_final = 10',
            4,8,4,10,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 4 AND materias_asignadas.Id_hora_inicial = 8 AND materias_asignadas.Id_hora_final = 11',
            4,8,4,11,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 4 AND materias_asignadas.Id_hora_inicial = 8 AND materias_asignadas.Id_hora_final = 12',
            4,8,4,12,
            8,self.diurno
        )

        # Octava linea 
        self.celda1x5(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 5 AND materias_asignadas.Id_hora_inicial = 8 AND materias_asignadas.Id_hora_final = 9',
            5,8,5,9,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 5 AND materias_asignadas.Id_hora_inicial = 8 AND materias_asignadas.Id_hora_final = 10',
            5,8,5,10,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 5 AND materias_asignadas.Id_hora_inicial = 8 AND materias_asignadas.Id_hora_final = 11',
            5,8,5,11,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 5 AND materias_asignadas.Id_hora_inicial = 8 AND materias_asignadas.Id_hora_final = 12',
            5,8,5,12,
            8,self.diurno
        )

        print('Noveno linea ----------------')

        # Noveno linea lunes
        self.celda1x4(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 1 AND materias_asignadas.Id_hora_inicial = 9 AND materias_asignadas.Id_hora_final = 10',
            1,9,1,10,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 1 AND materias_asignadas.Id_hora_inicial = 9 AND materias_asignadas.Id_hora_final = 11',
            1,9,1,11,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 1 AND materias_asignadas.Id_hora_inicial = 9 AND materias_asignadas.Id_hora_final = 12',
            1,9,1,12,
            9,self.diurno
        )

        # Noveno linea Martes
        self.celda1x4(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 2 AND materias_asignadas.Id_hora_inicial = 9 AND materias_asignadas.Id_hora_final = 10',
            2,9,2,10,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 2 AND materias_asignadas.Id_hora_inicial = 9 AND materias_asignadas.Id_hora_final = 11',
            2,9,2,11,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 2 AND materias_asignadas.Id_hora_inicial = 9 AND materias_asignadas.Id_hora_final = 12',
            2,9,2,12,
            9,self.diurno
        )

        # Noveno linea Miercoles
        self.celda1x4(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 3 AND materias_asignadas.Id_hora_inicial = 9 AND materias_asignadas.Id_hora_final = 10',
            3,9,3,10,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 3 AND materias_asignadas.Id_hora_inicial = 9 AND materias_asignadas.Id_hora_final = 11',
            3,9,3,11,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 3 AND materias_asignadas.Id_hora_inicial = 9 AND materias_asignadas.Id_hora_final = 12',
            3,9,3,12,
            9,self.diurno
        )

        # Noveno linea Jueves
        self.celda1x4(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 4 AND materias_asignadas.Id_hora_inicial = 9 AND materias_asignadas.Id_hora_final = 10',
            4,9,4,10,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 4 AND materias_asignadas.Id_hora_inicial = 9 AND materias_asignadas.Id_hora_final = 11',
            4,9,4,11,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 4 AND materias_asignadas.Id_hora_inicial = 9 AND materias_asignadas.Id_hora_final = 12',
            4,9,4,12,
            9,self.diurno
        )

        # Noveno linea Viernes
        self.celda1x4(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 5 AND materias_asignadas.Id_hora_inicial = 9 AND materias_asignadas.Id_hora_final = 10',
            5,9,5,10,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 5 AND materias_asignadas.Id_hora_inicial = 9 AND materias_asignadas.Id_hora_final = 11',
            5,9,5,11,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 5 AND materias_asignadas.Id_hora_inicial = 9 AND materias_asignadas.Id_hora_final = 12',
            5,9,5,12,
            9,self.diurno
        )

        print('Decimo linea ----------------')

        # Decimo linea lunes
        self.celda1x3(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 1 AND materias_asignadas.Id_hora_inicial = 10 AND materias_asignadas.Id_hora_final = 11',
            1,10,1,11,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 1 AND materias_asignadas.Id_hora_inicial = 10 AND materias_asignadas.Id_hora_final = 12',
            1,10,1,12,
            10,self.diurno
        )

        # Decimo linea Martes
        self.celda1x3(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 2 AND materias_asignadas.Id_hora_inicial = 10 AND materias_asignadas.Id_hora_final = 11',
            2,10,2,11,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 2 AND materias_asignadas.Id_hora_inicial = 10 AND materias_asignadas.Id_hora_final = 12',
            2,10,2,12,
            10,self.diurno
        )

        # Decimo linea Miercoles
        self.celda1x3(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 3 AND materias_asignadas.Id_hora_inicial = 10 AND materias_asignadas.Id_hora_final = 11',
            3,10,3,11,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 3 AND materias_asignadas.Id_hora_inicial = 10 AND materias_asignadas.Id_hora_final = 12',
            3,10,3,12,
            10,self.diurno
        )

        # Decimo linea Jueves
        self.celda1x3(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 4 AND materias_asignadas.Id_hora_inicial = 10 AND materias_asignadas.Id_hora_final = 11',
            4,10,4,11,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 4 AND materias_asignadas.Id_hora_inicial = 10 AND materias_asignadas.Id_hora_final = 12',
            4,10,4,12,
            10,self.diurno
        )

        # Decimo linea Viernes
        self.celda1x3(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 5 AND materias_asignadas.Id_hora_inicial = 10 AND materias_asignadas.Id_hora_final = 11',
            5,10,5,11,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 5 AND materias_asignadas.Id_hora_inicial = 10 AND materias_asignadas.Id_hora_final = 12',
            5,10,5,12,
            10,self.diurno
        )

        print('Decima primera linea ----------------')

        # Decima primera lunes
        self.celda1x2(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 1 AND materias_asignadas.Id_hora_inicial = 11 AND materias_asignadas.Id_hora_final = 12',
            1,11,1,12,
            11,self.diurno
        )

        # Decima primera Martes
        self.celda1x2(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 2 AND materias_asignadas.Id_hora_inicial = 11 AND materias_asignadas.Id_hora_final = 12',
            2,11,2,12,
            11,self.diurno
        )

        # Decima primera Miercoles
        self.celda1x2(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 3 AND materias_asignadas.Id_hora_inicial = 11 AND materias_asignadas.Id_hora_final = 12',
            3,11,3,12,
            11,self.diurno
        )

        # Decima primera Jueves
        self.celda1x2(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 4 AND materias_asignadas.Id_hora_inicial = 11 AND materias_asignadas.Id_hora_final = 12',
            4,11,4,12,
            11,self.diurno
        )

        # Decima primera Viernes
        self.celda1x2(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 5 AND materias_asignadas.Id_hora_inicial = 11 AND materias_asignadas.Id_hora_final = 12',
            5,11,5,12,
            11,self.diurno
        )
        return self.diurno

    def obtenerHorarioNocturno(self):
        self.nocturno = [
            [Paragraph('bloque de horas mañana',self.center),Paragraph('Lunes',self.center),Paragraph('Martes',self.center),Paragraph('Miercoles',self.center),Paragraph('Jueves',self.center),Paragraph('Viernes',self.center)],
            [Paragraph('6:00 - 6:45',self.center)],
            [Paragraph('6:45 - 7:30',self.center)],
            [Paragraph('7:35 - 8:20',self.center)],
            [Paragraph('8:20 - 9:05',self.center)],
            [Paragraph('9:05 - 9:50',self.center)],
            [Paragraph('9:50 - 10:35',self.center)]
        ] 
        
        print('Primera linea ----------------')
        # Primera linea lunes
        self.celda1x6(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 1 AND materias_asignadas.Id_hora_inicial = 13 AND materias_asignadas.Id_hora_final = 14',
            1,1,1,2,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 1 AND materias_asignadas.Id_hora_inicial = 13 AND materias_asignadas.Id_hora_final = 15',
            1,1,1,3,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 1 AND materias_asignadas.Id_hora_inicial = 13 AND materias_asignadas.Id_hora_final = 16',
            1,1,1,4,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 1 AND materias_asignadas.Id_hora_inicial = 13 AND materias_asignadas.Id_hora_final = 17',
            1,1,1,5,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 1 AND materias_asignadas.Id_hora_inicial = 13 AND materias_asignadas.Id_hora_final = 18',
            1,1,1,6,
            1,self.nocturno
        )

        # Primera linea Martes
        self.celda1x6(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 2 AND materias_asignadas.Id_hora_inicial = 13 AND materias_asignadas.Id_hora_final = 14',
            2,1,2,2,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 2 AND materias_asignadas.Id_hora_inicial = 13 AND materias_asignadas.Id_hora_final = 15',
            2,1,2,3,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 2 AND materias_asignadas.Id_hora_inicial = 13 AND materias_asignadas.Id_hora_final = 16',
            2,1,2,4,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 2 AND materias_asignadas.Id_hora_inicial = 13 AND materias_asignadas.Id_hora_final = 17',
            2,1,2,5,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 2 AND materias_asignadas.Id_hora_inicial = 13 AND materias_asignadas.Id_hora_final = 18',
            2,1,2,6,
            1,self.nocturno
        )

        # Primera linea Miercoles
        self.celda1x6(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 3 AND materias_asignadas.Id_hora_inicial = 13 AND materias_asignadas.Id_hora_final = 14',
            3,1,3,2,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 3 AND materias_asignadas.Id_hora_inicial = 13 AND materias_asignadas.Id_hora_final = 15',
            3,1,3,3,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 3 AND materias_asignadas.Id_hora_inicial = 13 AND materias_asignadas.Id_hora_final = 16',
            3,1,3,4,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 3 AND materias_asignadas.Id_hora_inicial = 13 AND materias_asignadas.Id_hora_final = 17',
            3,1,3,5,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 3 AND materias_asignadas.Id_hora_inicial = 13 AND materias_asignadas.Id_hora_final = 18',
            3,1,3,6,
            1,self.nocturno
        )

        # Primera linea Jueves
        self.celda1x6(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 4 AND materias_asignadas.Id_hora_inicial = 13 AND materias_asignadas.Id_hora_final = 14',
            4,1,4,2,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 4 AND materias_asignadas.Id_hora_inicial = 13 AND materias_asignadas.Id_hora_final = 15',
            4,1,4,3,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 4 AND materias_asignadas.Id_hora_inicial = 13 AND materias_asignadas.Id_hora_final = 16',
            4,1,4,4,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 4 AND materias_asignadas.Id_hora_inicial = 13 AND materias_asignadas.Id_hora_final = 17',
            4,1,4,5,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 4 AND materias_asignadas.Id_hora_inicial = 13 AND materias_asignadas.Id_hora_final = 18',
            4,1,4,6,
            1,self.nocturno
        )

        # Primera linea lunes
        self.celda1x6(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 5 AND materias_asignadas.Id_hora_inicial = 13 AND materias_asignadas.Id_hora_final = 14',
            5,1,5,2,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 5 AND materias_asignadas.Id_hora_inicial = 13 AND materias_asignadas.Id_hora_final = 15',
            5,1,5,3,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 5 AND materias_asignadas.Id_hora_inicial = 13 AND materias_asignadas.Id_hora_final = 16',
            5,1,5,4,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 5 AND materias_asignadas.Id_hora_inicial = 13 AND materias_asignadas.Id_hora_final = 17',
            5,1,5,5,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 5 AND materias_asignadas.Id_hora_inicial = 13 AND materias_asignadas.Id_hora_final = 18',
            5,1,5,6,
            1,self.nocturno
        )

        print('Segunda linea ----------------')

        # Segunda linea lunes
        self.celda1x5(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 1 AND materias_asignadas.Id_hora_inicial = 14 AND materias_asignadas.Id_hora_final = 15',
            1,2,1,3,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 1 AND materias_asignadas.Id_hora_inicial = 14 AND materias_asignadas.Id_hora_final = 16',
            1,2,1,4,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 1 AND materias_asignadas.Id_hora_inicial = 14 AND materias_asignadas.Id_hora_final = 17',
            1,2,1,5,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 1 AND materias_asignadas.Id_hora_inicial = 14 AND materias_asignadas.Id_hora_final = 18',
            1,2,1,6,
            2,self.nocturno
        )

         # Segunda linea Martes
        self.celda1x5(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 2 AND materias_asignadas.Id_hora_inicial = 14 AND materias_asignadas.Id_hora_final = 15',
            2,2,2,3,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 2 AND materias_asignadas.Id_hora_inicial = 14 AND materias_asignadas.Id_hora_final = 16',
            2,2,2,4,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 2 AND materias_asignadas.Id_hora_inicial = 14 AND materias_asignadas.Id_hora_final = 17',
            2,2,2,5,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 2 AND materias_asignadas.Id_hora_inicial = 14 AND materias_asignadas.Id_hora_final = 18',
            2,2,2,6,
            2,self.nocturno
        )

         # Segunda linea Miercoles
        self.celda1x5(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 3 AND materias_asignadas.Id_hora_inicial = 14 AND materias_asignadas.Id_hora_final = 15',
            3,2,3,3,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 3 AND materias_asignadas.Id_hora_inicial = 14 AND materias_asignadas.Id_hora_final = 16',
            3,2,3,4,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 3 AND materias_asignadas.Id_hora_inicial = 14 AND materias_asignadas.Id_hora_final = 17',
            3,2,3,5,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 3 AND materias_asignadas.Id_hora_inicial = 14 AND materias_asignadas.Id_hora_final = 18',
            3,2,3,6,
            2,self.nocturno
        )

         # Segunda linea Jueves
        self.celda1x5(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 4 AND materias_asignadas.Id_hora_inicial = 14 AND materias_asignadas.Id_hora_final = 15',
            4,2,4,3,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 4 AND materias_asignadas.Id_hora_inicial = 14 AND materias_asignadas.Id_hora_final = 16',
            4,2,4,4,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 4 AND materias_asignadas.Id_hora_inicial = 14 AND materias_asignadas.Id_hora_final = 17',
            4,2,4,5,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 4 AND materias_asignadas.Id_hora_inicial = 14 AND materias_asignadas.Id_hora_final = 18',
            4,2,4,6,
            2,self.nocturno
        )

         # Segunda linea Viernes
        self.celda1x5(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 5 AND materias_asignadas.Id_hora_inicial = 14 AND materias_asignadas.Id_hora_final = 15',
            5,2,5,3,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 5 AND materias_asignadas.Id_hora_inicial = 14 AND materias_asignadas.Id_hora_final = 16',
            5,2,5,4,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 5 AND materias_asignadas.Id_hora_inicial = 14 AND materias_asignadas.Id_hora_final = 17',
            5,2,5,5,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 5 AND materias_asignadas.Id_hora_inicial = 14 AND materias_asignadas.Id_hora_final = 18',
            5,2,5,6,
            2,self.nocturno
        )

        print('Tercera linea ----------------')

        # Tercera linea lunes
        self.celda1x4(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 1 AND materias_asignadas.Id_hora_inicial = 15 AND materias_asignadas.Id_hora_final = 16',
            1,3,1,4,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 1 AND materias_asignadas.Id_hora_inicial = 15 AND materias_asignadas.Id_hora_final = 17',
            1,3,1,5,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 1 AND materias_asignadas.Id_hora_inicial = 15 AND materias_asignadas.Id_hora_final = 18',
            1,3,1,6,
            3,self.nocturno
        )

        # Tercera linea Martes
        self.celda1x4(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 2 AND materias_asignadas.Id_hora_inicial = 15 AND materias_asignadas.Id_hora_final = 16',
            2,3,2,4,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 2 AND materias_asignadas.Id_hora_inicial = 15 AND materias_asignadas.Id_hora_final = 17',
            2,3,2,5,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 2 AND materias_asignadas.Id_hora_inicial = 15 AND materias_asignadas.Id_hora_final = 18',
            2,3,2,6,
            3,self.nocturno
        )

        # Tercera linea Miercoles
        self.celda1x4(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 3 AND materias_asignadas.Id_hora_inicial = 15 AND materias_asignadas.Id_hora_final = 16',
            3,3,3,4,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 3 AND materias_asignadas.Id_hora_inicial = 15 AND materias_asignadas.Id_hora_final = 17',
            3,3,3,5,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 3 AND materias_asignadas.Id_hora_inicial = 15 AND materias_asignadas.Id_hora_final = 18',
            3,3,3,6,
            3,self.nocturno
        )

        # Tercera linea jueves
        self.celda1x4(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 4 AND materias_asignadas.Id_hora_inicial = 15 AND materias_asignadas.Id_hora_final = 16',
            4,3,4,4,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 4 AND materias_asignadas.Id_hora_inicial = 15 AND materias_asignadas.Id_hora_final = 17',
            4,3,4,5,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 4 AND materias_asignadas.Id_hora_inicial = 15 AND materias_asignadas.Id_hora_final = 18',
            4,3,4,6,
            3,self.nocturno
        )

        # Tercera linea Viernes
        self.celda1x4(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 5 AND materias_asignadas.Id_hora_inicial = 15 AND materias_asignadas.Id_hora_final = 16',
            5,3,5,4,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 5 AND materias_asignadas.Id_hora_inicial = 15 AND materias_asignadas.Id_hora_final = 17',
            5,3,5,5,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 5 AND materias_asignadas.Id_hora_inicial = 15 AND materias_asignadas.Id_hora_final = 18',
            5,3,5,6,
            3,self.nocturno
        )

        print('Cuarta linea ----------------')

        # Cuarta linea lunes
        self.celda1x3(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 1 AND materias_asignadas.Id_hora_inicial = 16 AND materias_asignadas.Id_hora_final = 17',
            1,4,1,5,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 1 AND materias_asignadas.Id_hora_inicial = 16 AND materias_asignadas.Id_hora_final = 18',
            1,4,1,6,
            4,self.nocturno
        )

        # Cuarta linea Martes
        self.celda1x3(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 2 AND materias_asignadas.Id_hora_inicial = 16 AND materias_asignadas.Id_hora_final = 17',
            2,4,2,5,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 2 AND materias_asignadas.Id_hora_inicial = 16 AND materias_asignadas.Id_hora_final = 18',
            2,4,2,6,
            4,self.nocturno
        )

        # Cuarta linea Miercoles
        self.celda1x3(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 3 AND materias_asignadas.Id_hora_inicial = 16 AND materias_asignadas.Id_hora_final = 17',
            3,4,3,5,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 3 AND materias_asignadas.Id_hora_inicial = 16 AND materias_asignadas.Id_hora_final = 18',
            3,4,3,6,
            4,self.nocturno
        )

        # Cuarta linea Jueves
        self.celda1x3(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 4 AND materias_asignadas.Id_hora_inicial = 16 AND materias_asignadas.Id_hora_final = 17',
            4,4,4,5,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 4 AND materias_asignadas.Id_hora_inicial = 16 AND materias_asignadas.Id_hora_final = 18',
            4,4,4,6,
            4,self.nocturno
        )

        # Cuarta linea Viernes
        self.celda1x3(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 5 AND materias_asignadas.Id_hora_inicial = 16 AND materias_asignadas.Id_hora_final = 17',
            5,4,5,5,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 5 AND materias_asignadas.Id_hora_inicial = 16 AND materias_asignadas.Id_hora_final = 18',
            5,4,5,6,
            4,self.nocturno
        )

        print('Quinta primera linea ----------------')

        # Quinta primera lunes
        self.celda1x2(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 1 AND materias_asignadas.Id_hora_inicial = 17 AND materias_asignadas.Id_hora_final = 18',
            1,5,1,6,
            5,self.nocturno
        )

        # Quinta primera Martes
        self.celda1x2(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 2 AND materias_asignadas.Id_hora_inicial = 17 AND materias_asignadas.Id_hora_final = 18',
            2,5,2,6,
            5,self.nocturno
        )

        # Quinta primera Miercoles
        self.celda1x2(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 3 AND materias_asignadas.Id_hora_inicial = 17 AND materias_asignadas.Id_hora_final = 18',
            3,5,3,6,
            5,self.nocturno
        )

        # Quinta primera Jueves
        self.celda1x2(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 4 AND materias_asignadas.Id_hora_inicial = 17 AND materias_asignadas.Id_hora_final = 18',
            4,5,4,6,
            5,self.nocturno
        )

        # Quinta primera Viernes
        self.celda1x2(
            self.parametros,
            'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_semana = 5 AND materias_asignadas.Id_hora_inicial = 17 AND materias_asignadas.Id_hora_final = 18',
            5,5,5,6,
            5,self.nocturno
        )

        return self.nocturno
    