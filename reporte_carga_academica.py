import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import sqlite3
from rutas import *
import traceback
import sys
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A3
from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER, TA_LEFT

class ReporteCargaAcademica(tk.Toplevel):
    def __init__(self,master = None):
        super().__init__(master)
		# Config:
        self.master = master
        self.title('Reportes')
        self.geometry('350x540')
        self.resizable(width=0,height=0)
        self.iconbitmap(uptpc)

        self.menubar = tk.Menu(self)
        self.menubar.add_cascade(label="Volver", command=self.volver)
        self.config(menu=self.menubar)
        
        ttk.Label(self, text='REPORTES DE DOCENTES',font=('Helvetica',14)).place(x=45,y=5)
        
        self.framecontainer2 = ttk.Labelframe(self)
        self.framecontainer2.grid(column=0, row=0,ipadx=5,ipady=5,pady=35,padx=30)
        
        self.frameReportes = ttk.Labelframe(self.framecontainer2)
        self.frameReportes.grid(column=0,row=0,pady=5,padx=5)
        self.treeReportes = ttk.Treeview(self.frameReportes, columns=['#1',"#2"],show='headings',height=3)
        self.treeReportes.grid(row=0,column=0,pady=5,padx=5)
        self.treeReportes.heading('#1', text = 'Id',)
        self.treeReportes.heading('#2', text = 'Docente')
        self.treeReportes.column('#1', width=50)
        self.treeReportes.column('#2', width=190)
        self.scrollbarReportes = ttk.Scrollbar(self.frameReportes, orient=tk.VERTICAL, command=self.treeReportes.yview)
        self.treeReportes.configure(yscroll=self.scrollbarReportes.set)
        self.scrollbarReportes.grid(column=1,row=0, sticky='ns')
        
        self.frameReportesLapso = ttk.Labelframe(self.framecontainer2)
        self.frameReportesLapso.grid(column=0,row=1,pady=5,padx=5)
        self.treeReportesLapso = ttk.Treeview(self.frameReportesLapso, columns=['#1',"#2"],show='headings',height=3)
        self.treeReportesLapso.grid(row=0,column=0,pady=5,padx=5)
        self.treeReportesLapso.heading('#1', text = 'Id',)
        self.treeReportesLapso.heading('#2', text = 'Lapso académico')
        self.treeReportesLapso.column('#1', width=50)
        self.treeReportesLapso.column('#2', width=190)
        self.scrollbarReportesLapso = ttk.Scrollbar(self.frameReportesLapso, orient=tk.VERTICAL, command=self.treeReportesLapso.yview)
        self.treeReportesLapso.configure(yscroll=self.scrollbarReportesLapso.set)
        self.scrollbarReportesLapso.grid(column=1,row=0, sticky='ns')
        
        ttk.Label(self, text='ASCRIPCIÓN', font=('Helvetica',14)).place(x=120,y=305)
        self.frameAdscripcion = ttk.Labelframe(self.framecontainer2)
        self.frameAdscripcion.grid(column=0,row=2,pady=22,padx=5)
        ttk.Label(self.frameAdscripcion, text='Departamento de Ascripción:').grid(column=0,row=0)
        self.entryAdscripcion = ttk.Entry(self.frameAdscripcion,width=17)
        self.entryAdscripcion.grid(column= 1, row=0,pady=5,padx=5)
        ttk.Label(self.frameAdscripcion, text='Horario elaborado por:').grid(column=0,row=1)
        self.entryHorario = ttk.Entry(self.frameAdscripcion,width=17)
        self.entryHorario.grid(column= 1, row=1,pady=5,padx=5)
        ttk.Label(self.frameAdscripcion, text='Cargo:').grid(column=0,row=2)
        self.entryCargo = ttk.Entry(self.frameAdscripcion,width=17)
        self.entryCargo.grid(column= 1, row=2,pady=5,padx=5)
        
        ttk.Button(self.framecontainer2, text='GENERAR REPORTE', command=self.generarReporte).grid(row=3,column=0,padx=0,pady=5)
        
        self.MostrarReporteDocente()
        self.MostrarReporteLapso()

        self.setStyles = [
            ('GRID',(0,0),(-1,-1),0.5,colors.black),
            ('BBOX',(0,0),(-1,-1),0.5,colors.black),
            ('ALIGN',(0,0),(-1,-1),'CENTER'),
            ('VALIGN',(0,0),(-1,-1),'MIDDLE')
        ]
        
        self.setStyles2 = [
            ('GRID',(0,0),(-1,-1),0.5,colors.black),
            ('BBOX',(0,0),(-1,-1),0.5,colors.black),
            ('ALIGN',(0,0),(-1,-1),'CENTER'),
            ('VALIGN',(0,0),(-1,-1),'MIDDLE')
        ]
        
        self.setStyles3 = [
            ('GRID',(0,0),(-1,-1),0.5,colors.black),
            ('BBOX',(0,0),(-1,-1),0.5,colors.black),
            ('ALIGN',(0,0),(-1,-1),'CENTER'),
            ('VALIGN',(0,0),(-1,-1),'MIDDLE')
        ]
        
        self.setStyles4 = [
            ('GRID',(0,0),(-1,-1),0.5,colors.black),
            ('BBOX',(0,0),(-1,-1),0.5,colors.black),
            ('ALIGN',(0,0),(-1,-1),'CENTER'),
            ('VALIGN',(0,0),(-1,-1),'MIDDLE')
        ]
        
        self.setStyles5 = [
            ('GRID',(0,0),(-1,-1),0.5,colors.black),
            ('BBOX',(0,0),(-1,-1),0.5,colors.black),
            ('ALIGN',(0,0),(-1,-1),'CENTER'),
            ('VALIGN',(0,0),(-1,-1),'MIDDLE')
        ]
        
        self.setStyles6 = [
            ('GRID',(0,0),(-1,-1),0.5,colors.black),
            ('BBOX',(0,0),(-1,-1),0.5,colors.black),
            ('ALIGN',(0,0),(-1,-1),'CENTER'),
            ('VALIGN',(0,0),(-1,-1),'MIDDLE')
        ]
        
        self.setStyles7 = [
            ('GRID',(0,0),(-1,-1),0.5,colors.black),
            ('BBOX',(0,0),(-1,-1),0.5,colors.black),
            ('ALIGN',(0,0),(-1,-1),'CENTER'),
            ('VALIGN',(0,0),(-1,-1),'MIDDLE')
        ]
        
        self.setStyles8 = [
            ('GRID',(0,0),(-1,-1),0.5,colors.black),
            ('BBOX',(0,0),(-1,-1),0.5,colors.black),
            ('ALIGN',(0,0),(-1,-1),'CENTER'),
            ('VALIGN',(0,0),(-1,-1),'MIDDLE')
        ]
        
        self.width, self.heigth = A3
        self.styles1 = getSampleStyleSheet()
        self.styles2 = getSampleStyleSheet()
        self.center = self.styles1["BodyText"]
        self.center.alignment = TA_CENTER
        self.left = self.styles2["BodyText"]
        self.left.alignment = TA_LEFT
        self.counter = 0

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

    def generarReporte(self):
        if self.treeReportes.selection() and self.treeReportesLapso.selection() and len(self.entryAdscripcion.get()) != 0 and len(self.entryHorario.get()) != 0 and len(self.entryCargo.get()) != 0:
            descargaAcademica = self.conexion('SELECT docente.DescargaAcademica FROM docente WHERE docente.Id = ? and docente.Estado = "Activo"',(self.selecionarFila(self.treeReportes),)).fetchone()
            if descargaAcademica[0] == 'Si':
                self.docenteId = self.selecionarFilaReporteDocente()
                self.lapsoId = self.selecionarFilaReporteLapso()
                self.docente = self.ReporteDocente()
                self.lapso = self.ReporteLapso()
                
                self.parametrosReportes = (self.docenteId, self.lapsoId)
                
                self.guardar = filedialog.asksaveasfilename(initialdir= "/", title="Select file", defaultextension=".*",filetypes=(("PDF files","*.pdf"),("all files","*.*")),parent=self)
                self.archivo = open(self.guardar,'w')
                
                self.pdf = canvas.Canvas(self.guardar, pagesize = A3)
                self.pdf.setFontSize(size=12)
                self.pdf.drawString(375,1150,'CARGA ACADÉMICA')
                self.pdf.drawString(368,1135,'Lapso Académico ' + self.lapso)
                self.pdf.drawImage(logoPDF,690,1100,width=80,height=80)
                self.tablaInicio()
                self.pdf.drawString(10,980,'Por medio de la presente se le notifica que Usted, ha sido designado(a) para dictar la(s) unidad(es) curricular(es) que a continuación se especifica(n):')
                self.tablaMaterias()
                self.listadoMaterias()
                if self.counter == 10: 
                    self.pdf.drawString(375,490,'Horarios de clases')
                    print('horario de clases---10')
                elif self.counter == 9: 
                    self.pdf.drawString(375,530,'Horarios de clases')
                    print('horario de clases---9')
                elif self.counter == 8: 
                    self.pdf.drawString(375,570,'Horarios de clases')
                    print('horario de clases---8')
                elif self.counter == 7: 
                    self.pdf.drawString(375,600,'Horarios de clases')
                    print('horario de clases---7')
                elif self.counter == 6: 
                    self.pdf.drawString(375,640,'Horarios de clases')
                    print('horario de clases---6')
                elif self.counter == 5: 
                    self.pdf.drawString(375,690,'Horarios de clases')
                    print('horario de clases---5')
                elif self.counter == 4: 
                    self.pdf.drawString(375,730,'Horarios de clases')
                    print('horario de clases---4')
                elif self.counter == 3: 
                    self.pdf.drawString(375,770,'Horarios de clases')
                    print('horario de clases---3')
                elif self.counter == 2: 
                    self.pdf.drawString(375,810,'Horarios de clases')
                    print('horario de clases---2')
                elif self.counter == 1: 
                    self.pdf.drawString(375,850,'Horarios de clases')
                    print('horario de clases---1')
                else:
                    self.pdf.drawString(375,850,'Horarios de clases')
                    print('horario de clases---0')
                self.tablaHorarioMorning()
                self.tablaHorarioAfternon()
                self.tablaHorarioNinght()
                if self.counter == 10: 
                    self.pdf.drawString(330,970,'Adscripción Académico-administrativa')
                    print('adscripcion---10')
                elif self.counter == 9: 
                    self.pdf.drawString(330,970,'Adscripción Académico-administrativa')
                    print('adscripcion---9')
                elif self.counter == 8: 
                    self.pdf.showPage()
                    self.pdf.drawString(330,1150,'Adscripción Académico-administrativa')
                    print('adscripcion---8')
                elif self.counter == 7:
                    self.pdf.showPage()
                    self.pdf.drawString(330,1150,'Adscripción Académico-administrativa')
                    print('adscripcion---7')
                elif self.counter == 6:
                    self.pdf.showPage()
                    self.pdf.drawString(330,1150,'Adscripción Académico-administrativa')
                    print('adscripcion---6')
                elif self.counter == 5: 
                    self.pdf.showPage()
                    self.pdf.drawString(330,1150,'Adscripción Académico-administrativa')
                    print('adscripcion---5')
                elif self.counter == 4: 
                    self.pdf.drawString(330,150,'Adscripción Académico-administrativa')
                    print('adscripcion---4')
                elif self.counter == 3: 
                    self.pdf.drawString(330,190,'Adscripción Académico-administrativa')
                    print('adscripcion---3')
                elif self.counter == 2: 
                    self.pdf.drawString(330,230,'Adscripción Académico-administrativa')
                    print('adscripcion---2')
                elif self.counter == 1: 
                    self.pdf.drawString(330,270,'Adscripción Académico-administrativa')
                    print('adscripcion---1')
                else:
                    self.pdf.drawString(330,270,'Adscripción Académico-administrativa')
                    print('adscripcion---0')
                self.tablaHorarioAdcrispcion()
                self.tablaHorarioObservacion()
            
                self.pdf.save()
                self.archivo.close()
                self.setStyles.clear()
                self.setStyles.append(('GRID',(0,0),(-1,-1),0.5,colors.black))
                self.setStyles.append(('BBOX',(0,0),(-1,-1),0.5,colors.black))
                self.setStyles.append(('VALIGN',(0,0),(-1,-1),'MIDDLE'))
                self.setStyles.append(('ALIGN',(0,0),(-1,-1),'CENTER'))

                self.setStyles2.clear()
                self.setStyles2.append(('GRID',(0,0),(-1,-1),0.5,colors.black))
                self.setStyles2.append(('BBOX',(0,0),(-1,-1),0.5,colors.black))
                self.setStyles2.append(('VALIGN',(0,0),(-1,-1),'MIDDLE'))
                self.setStyles2.append(('ALIGN',(0,0),(-1,-1),'CENTER'))

                self.setStyles3.clear()
                self.setStyles3.append(('GRID',(0,0),(-1,-1),0.5,colors.black))
                self.setStyles3.append(('BBOX',(0,0),(-1,-1),0.5,colors.black))
                self.setStyles3.append(('VALIGN',(0,0),(-1,-1),'MIDDLE'))
                self.setStyles3.append(('ALIGN',(0,0),(-1,-1),'CENTER'))

                self.setStyles4.clear()
                self.setStyles4.append(('GRID',(0,0),(-1,-1),0.5,colors.black))
                self.setStyles4.append(('BBOX',(0,0),(-1,-1),0.5,colors.black))
                self.setStyles4.append(('VALIGN',(0,0),(-1,-1),'MIDDLE'))
                self.setStyles4.append(('ALIGN',(0,0),(-1,-1),'CENTER'))

                self.setStyles5.clear()
                self.setStyles5.append(('GRID',(0,0),(-1,-1),0.5,colors.black))
                self.setStyles5.append(('BBOX',(0,0),(-1,-1),0.5,colors.black))
                self.setStyles5.append(('VALIGN',(0,0),(-1,-1),'MIDDLE'))
                self.setStyles5.append(('ALIGN',(0,0),(-1,-1),'CENTER'))

                self.setStyles6.clear()
                self.setStyles6.append(('GRID',(0,0),(-1,-1),0.5,colors.black))
                self.setStyles6.append(('BBOX',(0,0),(-1,-1),0.5,colors.black))
                self.setStyles6.append(('VALIGN',(0,0),(-1,-1),'MIDDLE'))
                self.setStyles6.append(('ALIGN',(0,0),(-1,-1),'CENTER'))

                self.setStyles7.clear()
                self.setStyles7.append(('GRID',(0,0),(-1,-1),0.5,colors.black))
                self.setStyles7.append(('BBOX',(0,0),(-1,-1),0.5,colors.black))
                self.setStyles7.append(('VALIGN',(0,0),(-1,-1),'MIDDLE'))
                self.setStyles7.append(('ALIGN',(0,0),(-1,-1),'CENTER'))

                self.setStyles8.clear()
                self.setStyles8.append(('GRID',(0,0),(-1,-1),0.5,colors.black))
                self.setStyles8.append(('BBOX',(0,0),(-1,-1),0.5,colors.black))
                self.setStyles8.append(('VALIGN',(0,0),(-1,-1),'MIDDLE'))
                self.setStyles8.append(('ALIGN',(0,0),(-1,-1),'CENTER'))
                
                self.counter = 0
                messagebox.showinfo(title='Horario', message='Carga académica docente generada correctamente',parent=self)
            elif descargaAcademica[0] == 'No':
                messagebox.showwarning(title='Warning', message='Descarga Académica no permitada',parent=self)
            else:
                messagebox.showwarning(title='Warning', message='Algo ocurrio mal, consulte con el desarrollador',parent=self)
        else:
            messagebox.showwarning(title='Warning', message='Debe seleccionar todas las casillas y rellenar todas las celdas',parent=self)

    def MostrarReporteDocente(self):
        self.rows = self.TraerDatos("SELECT Id, NombreApellido FROM docente WHERE docente.Estado = 'Activo'")
        for row in self.rows:
            self.treeReportes.insert('',tk.END,values=row)
            
    def MostrarReporteLapso(self):
        self.rows = self.TraerDatos("SELECT * FROM lapso_academico WHERE lapso_academico.Estado = 'Activo'")
        for row in self.rows:
            self.treeReportesLapso.insert('',tk.END,values=row)
            
    def selecionarFilaReporteDocente(self):
        self.item = self.treeReportes.focus()
        self.data = self.treeReportes.item(self.item)
        self.id = self.data['values'][0]
        return self.id
        
    def selecionarFilaReporteLapso(self):
        self.item = self.treeReportesLapso.focus()
        self.data = self.treeReportesLapso.item(self.item)
        self.id = self.data['values'][0]
        return self.id

    def selecionarFila(self,tree):
        item = tree.focus()
        data = tree.item(item)
        id = data['values'][0]
        return id
        
    def ReporteDocente(self):
        self.item = self.treeReportes.focus()
        self.data = self.treeReportes.item(self.item)
        self.id = self.data['values'][1]
        return self.id
        
    def ReporteLapso(self):
        self.item = self.treeReportesLapso.focus()
        self.data = self.treeReportesLapso.item(self.item)
        self.id = self.data['values'][1]
        return self.id

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
    celda,modalidad,estilos
    ):
        consulta = self.materia(query1,parametros)
        if len(consulta) != 0:
            modalidad[celda].append(Paragraph(consulta,self.center))
            estilos.append(('SPAN',(coorX0,coorY0),(coorX1,coorY1)))
            print('CONSULTA 1 EXITOSA')
        else:
            consulta = self.materia(query2,parametros)
            if len(consulta) != 0:
                modalidad[celda].append(Paragraph(consulta,self.center))
                estilos.append(('SPAN',(coorX2,coorY2),(coorX3,coorY3)))
                print('CONSULTA 2 EXITOSA')
            else:
                consulta = self.materia(query3,parametros)
                if len(consulta) != 0:
                    modalidad[celda].append(Paragraph(consulta,self.center))
                    estilos.append(('SPAN',(coorX4,coorY4),(coorX5,coorY5)))
                    print('CONSULTA 3 EXITOSA')
                else:
                    consulta = self.materia(query4,parametros)
                    if len(consulta) != 0:
                        modalidad[celda].append(Paragraph(consulta,self.center))
                        estilos.append(('SPAN',(coorX6,coorY6),(coorX7,coorY7)))
                        print('CONSULTA 4 EXITOSA')
                    else:
                        consulta = self.materia(query5,parametros)
                        if len(consulta) != 0:
                            modalidad[celda].append(Paragraph(consulta,self.center))
                            estilos.append(('SPAN',(coorX8,coorY8),(coorX9,coorY9)))
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
    celda,modalidad,estilos
    ):
        consulta = self.materia(query1,parametros)
        if len(consulta) != 0:
            modalidad[celda].append(Paragraph(consulta,self.center))
            estilos.append(('SPAN',(coorX0,coorY0),(coorX1,coorY1)))
            print('CONSULTA 1 EXITOSA')
        else:
            consulta = self.materia(query2,parametros)
            if len(consulta) != 0:
                modalidad[celda].append(Paragraph(consulta,self.center))
                estilos.append(('SPAN',(coorX2,coorY2),(coorX3,coorY3)))
                print('CONSULTA 2 EXITOSA')
            else:
                consulta = self.materia(query3,parametros)
                if len(consulta) != 0:
                    modalidad[celda].append(Paragraph(consulta,self.center))
                    estilos.append(('SPAN',(coorX4,coorY4),(coorX5,coorY5)))
                    print('CONSULTA 3 EXITOSA')
                else:
                    consulta = self.materia(query4,parametros)
                    if len(consulta) != 0:
                        modalidad[celda].append(Paragraph(consulta,self.center))
                        estilos.append(('SPAN',(coorX6,coorY6),(coorX7,coorY7)))
                        print('CONSULTA 4 EXITOSA')
                    else:
                        modalidad[celda].append(Paragraph(' ',self.center))
                        print('DENEGADO CAMARADA')

    def celda1x4(self,
    parametros,
    query1,coorX0,coorY0,coorX1,coorY1,
    query2,coorX2,coorY2,coorX3,coorY3,
    query3,coorX4,coorY4,coorX5,coorY5,
    celda,modalidad,estilos
    ):
        consulta = self.materia(query1,parametros)
        if len(consulta) != 0:
            modalidad[celda].append(Paragraph(consulta,self.center))
            estilos.append(('SPAN',(coorX0,coorY0),(coorX1,coorY1)))
            print('CONSULTA 1 EXITOSA')
        else:
            consulta = self.materia(query2,parametros)
            if len(consulta) != 0:
                modalidad[celda].append(Paragraph(consulta,self.center))
                estilos.append(('SPAN',(coorX2,coorY2),(coorX3,coorY3)))
                print('CONSULTA 2 EXITOSA')
            else:
                consulta = self.materia(query3,parametros)
                if len(consulta) != 0:
                    modalidad[celda].append(Paragraph(consulta,self.center))
                    estilos.append(('SPAN',(coorX4,coorY4),(coorX5,coorY5)))
                    print('CONSULTA 3 EXITOSA')
                else:
                    modalidad[celda].append(Paragraph(' ',self.center))
                    print('DENEGADO CAMARADA')


    def celda1x3(self,
        parametros,
        query1,coorX0,coorY0,coorX1,coorY1,
        query2,coorX2,coorY2,coorX3,coorY3,
        celda,modalidad,estilos
        ):
            consulta = self.materia(query1,parametros)
            if len(consulta) != 0:
                modalidad[celda].append(Paragraph(consulta,self.center))
                estilos.append(('SPAN',(coorX0,coorY0),(coorX1,coorY1)))
                print('CONSULTA 1 EXITOSA')
            else:
                consulta = self.materia(query2,parametros)
                if len(consulta) != 0:
                    modalidad[celda].append(Paragraph(consulta,self.center))
                    estilos.append(('SPAN',(coorX2,coorY2),(coorX3,coorY3)))
                    print('CONSULTA 2 EXITOSA')
                else:
                    modalidad[celda].append(Paragraph(' ',self.center))
                    print('DENEGADO CAMARADA')

    def celda1x2(self,
        parametros,
        query1,coorX0,coorY0,coorX1,coorY1,
        celda,modalidad,estilos
        ):
            consulta = self.materia(query1,parametros)
            if len(consulta) != 0:
                modalidad[celda].append(Paragraph(consulta,self.center))
                estilos.append(('SPAN',(coorX0,coorY0),(coorX1,coorY1)))
                print('CONSULTA 1 EXITOSA')
            else:
                modalidad[celda].append(Paragraph(' ',self.center))
                print('DENEGADO CAMARADA')

    def tablaInicio(self):
            self.tableInicio = Table(self.obtenerTablaInicio(),colWidths=206, rowHeights=15)
            self.tableInicio.setStyle(TableStyle(self.setStyles))
            self.tableInicio.wrapOn(self.pdf,self.width,self.heigth)
            self.tableInicio.drawOn(self.pdf,10,1000)
            return self.tableInicio

    def obtenerTablaInicio(self):
            self.tabla1 = [
                [Paragraph('Nombre y Apelido:',self.center)],
                [Paragraph('Categoría:',self.center)],
                [Paragraph('Dedicacíon:',self.center)],
                [Paragraph('Título de Pre-Grado:',self.center)],
                [Paragraph('Título de Pos-Grado',self.center)],
                [Paragraph('Descarga Academica:',self.center)],
                [Paragraph('Razon de la descarga:',self.center)]
            ]
            
            self.nombre = self.materia('SELECT docente.NombreApellido from docente WHERE docente.Id = ? AND docente.Estado = "Activo"',(self.docenteId,))
            self.tabla1[0].append(Paragraph(self.nombre,self.center))
            self.tabla1[0].append(Paragraph('Cedula:',self.center))
            self.cedula = self.materia('SELECT docente.Cedula from docente WHERE docente.Id = ? AND docente.Estado = "Activo"',(self.docenteId,))
            self.tabla1[0].append(Paragraph(self.cedula,self.center))
            self.categoria = self.materia('SELECT docente.Categoria from docente WHERE docente.Id = ? AND docente.Estado = "Activo"',(self.docenteId,))
            self.tabla1[1].append(Paragraph(self.categoria,self.left))
            self.setStyles.append(('SPAN',(1,1),(3,1)))
            self.dedicacion = self.materia('SELECT docente.Dedicacion from docente WHERE docente.Id = ? AND docente.Estado = "Activo"',(self.docenteId,))
            self.tabla1[2].append(Paragraph(self.dedicacion,self.left))
            self.setStyles.append(('SPAN',(1,2),(3,2)))
            self.pregrado = self.materia('SELECT docente.Pregrado from docente WHERE docente.Id = ? AND docente.Estado = "Activo"',(self.docenteId,))
            self.tabla1[3].append(Paragraph(self.pregrado,self.left))
            self.setStyles.append(('SPAN',(1,3),(3,3)))
            self.posgrado = self.materia('SELECT docente.Posgrado from docente WHERE docente.Id = ? AND docente.Estado = "Activo"',(self.docenteId,))
            self.tabla1[4].append(Paragraph(self.posgrado,self.left))
            self.setStyles.append(('SPAN',(1,4),(3,4)))
            self.descargaAcademica = self.materia('SELECT docente.DescargaAcademica from docente WHERE docente.Id = ? AND docente.Estado = "Activo"',(self.docenteId,))
            self.tabla1[5].append(Paragraph(self.descargaAcademica,self.left))
            self.tabla1[5].append(Paragraph('Condicion laboral:',self.left))
            self.condicionLaboral = self.materia('SELECT docente.CondicionLaboral from docente WHERE docente.Id = ? AND docente.Estado = "Activo"',(self.docenteId,))
            self.tabla1[5].append(Paragraph(self.condicionLaboral,self.left))
            self.razonDescarga = self.materia('SELECT docente.RazonDescarga from docente WHERE docente.Id = ? AND docente.Estado = "Activo"',(self.docenteId,))
            self.tabla1[6].append(Paragraph(self.razonDescarga,self.left))
            self.setStyles.append(('SPAN',(1,6),(3,6)))

            return self.tabla1

    def tablaMaterias(self):
            self.tableMaterias = Table(self.obtenerTablaMaterias(),colWidths=103, rowHeights=15)
            self.tableMaterias.setStyle(TableStyle(self.setStyles2))
            self.tableMaterias.wrapOn(self.pdf,self.width,self.heigth)
            self.tableMaterias.drawOn(self.pdf,10,910)
            
            return self.tableMaterias

    def obtenerTablaMaterias(self):
            self.tabla2 = [
                [Paragraph('Unidad Curricular',self.center),Paragraph('Sección',self.center),Paragraph('Horas',self.center),Paragraph('Departamento',self.center),Paragraph('Subsistemas de educación de pregrado:',self.center),'','',''],
                ['','','','','PNF','','','PT'],
                ['','','','','Cohorte','Trimestre','Trayecto',''],
                ['','','','','','','','']
            ]
            self.setStyles2.append(('SPAN',(4,0),(7,0)))
            self.setStyles2.append(('SPAN',(0,0),(0,3)))
            self.setStyles2.append(('SPAN',(1,0),(1,3)))
            self.setStyles2.append(('SPAN',(2,0),(2,3)))
            self.setStyles2.append(('SPAN',(3,0),(3,3)))
            self.setStyles2.append(('SPAN',(6,2),(6,3)))
            self.setStyles2.append(('SPAN',(7,1),(7,3)))
            self.setStyles2.append(('SPAN',(4,1),(6,1)))
            self.setStyles2.append(('SPAN',(4,2),(5,2)))
            self.setStyles2.append(('SPAN',(4,2),(4,3)))
            self.setStyles2.append(('SPAN',(5,2),(5,3)))

            return self.tabla2

    def listadoMaterias(self):
            self.listadoMateria = Table(self.obtenerlistadoMaterias(),colWidths=103, rowHeights=40)
            self.listadoMateria.setStyle(TableStyle(self.setStyles3))
            self.listadoMateria.wrapOn(self.pdf,self.width,self.heigth)
            if self.counter == 10: 
                self.listadoMateria.drawOn(self.pdf,10,510)
                print('materia----10')
            elif self.counter == 9: 
                self.listadoMateria.drawOn(self.pdf,10,550)
                print('materia-----9')
            elif self.counter == 8: 
                self.listadoMateria.drawOn(self.pdf,10,590)
                print('materia-----8')
            elif self.counter == 7: 
                self.listadoMateria.drawOn(self.pdf,10,630)
                print('materia-----7')
            elif self.counter == 6: 
                self.listadoMateria.drawOn(self.pdf,10,670)
                print('materia-----6')
            elif self.counter == 5: 
                self.listadoMateria.drawOn(self.pdf,10,710)
                print('materia-----5')
            elif self.counter == 4: 
                self.listadoMateria.drawOn(self.pdf,10,750)
                print('materia-----4')
            elif self.counter == 3: 
                self.listadoMateria.drawOn(self.pdf,10,790)
                print('materia-----3')
            elif self.counter == 2: 
                self.listadoMateria.drawOn(self.pdf,10,830)
                print('materia-----2')
            elif self.counter == 1: 
                self.listadoMateria.drawOn(self.pdf,10,870)
                print('materia-----1')
            else:
                self.listadoMateria.drawOn(self.pdf,10,870)
                print('materia-----0')
            
            return self.listadoMaterias

    def obtenerlistadoMaterias(self):
            self.listado = [
                [Paragraph('',self.center),Paragraph('',self.center),Paragraph('',self.center),Paragraph('',self.center),Paragraph('',self.center),Paragraph('',self.center),Paragraph('',self.center),Paragraph('',self.center)]
            ]

            self.obtenermaterias = self.conexion(
                'SELECT DISTINCT unidad_curricular.UnidadCurricular,seccion.Seccion,unidad_curricular.hora, unidad_curricular.departamento,cohorte.Cohorte, trayecto.Trayecto, trimestre.Trimestre, unidad_curricular.Pt FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular INNER JOIN seccion ON seccion.Id = materias_asignadas.Id_seccion INNER JOIN cohorte ON  cohorte.Id = materias_asignadas.Id_cohorte INNER JOIN trayecto ON trayecto.Id = materias_asignadas.Id_trayecto INNER JOIN trimestre ON trimestre.Id = materias_asignadas.Id_trimestre WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Estado = "Activo"',
                self.parametrosReportes).fetchall()

            array1 = []
            array2 = []
            array3 = []
            array4 = []
            array5 = []
            array6 = []
            array7 = []
            array8 = []
            array9 = []
            array10 = []

            for row in self.obtenermaterias:
                if self.counter == 0: 
                    array1.append(Paragraph(row[0],self.center))
                    array1.append(Paragraph(row[1],self.center))
                    array1.append(Paragraph(row[2],self.center))
                    array1.append(Paragraph(row[3],self.center))
                    array1.append(Paragraph(row[4],self.center))
                    array1.append(Paragraph(row[5],self.center))
                    array1.append(Paragraph(row[6],self.center))
                    array1.append(Paragraph(row[7],self.center))
                    self.counter = self.counter + 1
                    print(self.counter)
                elif self.counter == 1:
                    array2.append(Paragraph(row[0],self.center))
                    array2.append(Paragraph(row[1],self.center))
                    array2.append(Paragraph(row[2],self.center))
                    array2.append(Paragraph(row[3],self.center))
                    array2.append(Paragraph(row[4],self.center))
                    array2.append(Paragraph(row[5],self.center))
                    array2.append(Paragraph(row[6],self.center))
                    array2.append(Paragraph(row[7],self.center))
                    self.counter = self.counter + 1
                    print(self.counter)
                elif self.counter == 2:
                    array3.append(Paragraph(row[0],self.center))
                    array3.append(Paragraph(row[1],self.center))
                    array3.append(Paragraph(row[2],self.center))
                    array3.append(Paragraph(row[3],self.center))
                    array3.append(Paragraph(row[4],self.center))
                    array3.append(Paragraph(row[5],self.center))
                    array3.append(Paragraph(row[6],self.center))
                    array3.append(Paragraph(row[7],self.center))
                    self.counter = self.counter + 1
                    print(self.counter)
                elif self.counter == 3:
                    array4.append(Paragraph(row[0],self.center))
                    array4.append(Paragraph(row[1],self.center))
                    array4.append(Paragraph(row[2],self.center))
                    array4.append(Paragraph(row[3],self.center))
                    array4.append(Paragraph(row[4],self.center))
                    array4.append(Paragraph(row[5],self.center))
                    array4.append(Paragraph(row[6],self.center))
                    array4.append(Paragraph(row[7],self.center))
                    self.counter = self.counter + 1
                    print(self.counter)
                elif self.counter == 4:
                    array5.append(Paragraph(row[0],self.center))
                    array5.append(Paragraph(row[1],self.center))
                    array5.append(Paragraph(row[2],self.center))
                    array5.append(Paragraph(row[3],self.center))
                    array5.append(Paragraph(row[4],self.center))
                    array5.append(Paragraph(row[5],self.center))
                    array5.append(Paragraph(row[6],self.center))
                    array5.append(Paragraph(row[7],self.center))
                    self.counter = self.counter + 1
                    print(self.counter)
                elif self.counter == 5:
                    array6.append(Paragraph(row[0],self.center))
                    array6.append(Paragraph(row[1],self.center))
                    array6.append(Paragraph(row[2],self.center))
                    array6.append(Paragraph(row[3],self.center))
                    array6.append(Paragraph(row[4],self.center))
                    array6.append(Paragraph(row[5],self.center))
                    array6.append(Paragraph(row[6],self.center))
                    array6.append(Paragraph(row[7],self.center))
                    self.counter = self.counter + 1
                    print(self.counter)
                elif self.counter == 6:
                    array7.append(Paragraph(row[0],self.center))
                    array7.append(Paragraph(row[1],self.center))
                    array7.append(Paragraph(row[2],self.center))
                    array7.append(Paragraph(row[3],self.center))
                    array7.append(Paragraph(row[4],self.center))
                    array7.append(Paragraph(row[5],self.center))
                    array7.append(Paragraph(row[6],self.center))
                    array7.append(Paragraph(row[7],self.center))
                    self.counter = self.counter + 1
                    print(self.counter)
                elif self.counter == 7:
                    array8.append(Paragraph(row[0],self.center))
                    array8.append(Paragraph(row[1],self.center))
                    array8.append(Paragraph(row[2],self.center))
                    array8.append(Paragraph(row[3],self.center))
                    array8.append(Paragraph(row[4],self.center))
                    array8.append(Paragraph(row[5],self.center))
                    array8.append(Paragraph(row[6],self.center))
                    array8.append(Paragraph(row[7],self.center))
                    self.counter = self.counter + 1
                    print(self.counter)
                elif self.counter == 8:
                    array9.append(Paragraph(row[0],self.center))
                    array9.append(Paragraph(row[1],self.center))
                    array9.append(Paragraph(row[2],self.center))
                    array9.append(Paragraph(row[3],self.center))
                    array9.append(Paragraph(row[4],self.center))
                    array9.append(Paragraph(row[5],self.center))
                    array9.append(Paragraph(row[6],self.center))
                    array9.append(Paragraph(row[7],self.center))
                    self.counter = self.counter + 1
                    print(self.counter)
                elif self.counter == 9:
                    array10.append(Paragraph(row[0],self.center))
                    array10.append(Paragraph(row[1],self.center))
                    array10.append(Paragraph(row[2],self.center))
                    array10.append(Paragraph(row[3],self.center))
                    array10.append(Paragraph(row[4],self.center))
                    array10.append(Paragraph(row[5],self.center))
                    array10.append(Paragraph(row[6],self.center))
                    array10.append(Paragraph(row[7],self.center))
                    self.counter = self.counter + 1
                    print(self.counter)			
            
            if self.counter == 10:
                self.listado.clear()
                self.listado.append(array1)
                self.listado.append(array2)
                self.listado.append(array3)
                self.listado.append(array4)
                self.listado.append(array5)
                self.listado.append(array6)
                self.listado.append(array7)
                self.listado.append(array8)
                self.listado.append(array9)
                self.listado.append(array10)
            elif self.counter == 9:
                self.listado.clear()
                self.listado.append(array1)
                self.listado.append(array2)
                self.listado.append(array3)
                self.listado.append(array4)
                self.listado.append(array5)
                self.listado.append(array6)
                self.listado.append(array7)
                self.listado.append(array8)
                self.listado.append(array9)
            elif self.counter == 8:
                self.listado.clear()
                self.listado.append(array1)
                self.listado.append(array2)
                self.listado.append(array3)
                self.listado.append(array4)
                self.listado.append(array5)
                self.listado.append(array6)
                self.listado.append(array7)
                self.listado.append(array8)
            elif self.counter == 7:
                self.listado.clear()
                self.listado.append(array1)
                self.listado.append(array2)
                self.listado.append(array3)
                self.listado.append(array4)
                self.listado.append(array5)
                self.listado.append(array6)
                self.listado.append(array7)
            elif self.counter == 6:
                self.listado.clear()
                self.listado.append(array1)
                self.listado.append(array2)
                self.listado.append(array3)
                self.listado.append(array4)
                self.listado.append(array5)
                self.listado.append(array6)
            elif self.counter == 5:
                self.listado.clear()
                self.listado.append(array1)
                self.listado.append(array2)
                self.listado.append(array3)
                self.listado.append(array4)
                self.listado.append(array5)
            elif self.counter == 4:
                self.listado.clear()
                self.listado.append(array1)
                self.listado.append(array2)
                self.listado.append(array3)
                self.listado.append(array4)
            elif self.counter == 3:
                self.listado.clear()
                self.listado.append(array1)
                self.listado.append(array2)
                self.listado.append(array3)
            elif self.counter == 2:
                self.listado.clear()
                self.listado.append(array1)
                self.listado.append(array2)
            elif self.counter == 1:
                self.listado.clear()
                self.listado.append(array1)

            return self.listado

    def tablaHorarioMorning(self):
            self.tableHorarioMorning = Table(self.obtenerTablaHorarioMorning(),colWidths=137, rowHeights=25)
            self.tableHorarioMorning.setStyle(TableStyle(self.setStyles4))
            self.tableHorarioMorning.wrapOn(self.pdf,self.width,self.heigth)
            if self.counter == 10:
                self.tableHorarioMorning.drawOn(self.pdf,11,300)
                print('mornig----10')
            elif self.counter == 9: 
                self.tableHorarioMorning.drawOn(self.pdf,11,340)
                print('mornig-----9')
            elif self.counter == 8: 
                self.tableHorarioMorning.drawOn(self.pdf,11,380)
                print('mornig-----8')
            elif self.counter == 7: 
                self.tableHorarioMorning.drawOn(self.pdf,11,410)
                print('mornig-----7')
            elif self.counter == 6: 
                self.tableHorarioMorning.drawOn(self.pdf,11,450)
                print('mornig-----6')
            elif self.counter == 5: 
                self.tableHorarioMorning.drawOn(self.pdf,11,500)
                print('mornig-----5')
            elif self.counter == 4: 
                self.tableHorarioMorning.drawOn(self.pdf,11,540)
                print('mornig-----4')
            elif self.counter == 3: 
                self.tableHorarioMorning.drawOn(self.pdf,11,580)
                print('mornig-----3')
            elif self.counter == 2: 
                self.tableHorarioMorning.drawOn(self.pdf,11,620)
                print('mornig-----2')
            elif self.counter == 1: 
                self.tableHorarioMorning.drawOn(self.pdf,11,660)
                print('mornig-----1')
            else:
                self.tableHorarioMorning.drawOn(self.pdf,11,660)
                print('mornig-----0')
            return self.tableHorarioMorning

    def obtenerTablaHorarioMorning(self):
            self.morning = [
                [Paragraph('Horario de Clases Mañana',self.center),Paragraph('Lunes',self.center),Paragraph('Martes',self.center),Paragraph('Miércoles',self.center),Paragraph('Jueves',self.center),Paragraph('Viernes',self.center)],
                [Paragraph('7:10 - 7:55',self.center)],
                [Paragraph('8:00 - 8:45',self.center)],
                [Paragraph('8:50 - 9:35',self.center)],
                [Paragraph('9:40 - 10:25',self.center)],
                [Paragraph('10:30 - 11:15',self.center)],
                [Paragraph('11:20 - 12:05',self.center)],
            ]

            print('Primera linea ----------------')
            # Primera linea lunes
            self.celda1x6(
                self.parametrosReportes,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 1 AND materias_asignadas.Id_hora_inicial = 1 AND materias_asignadas.Id_hora_final = 2 AND materias_asignadas.Estado = "Activo"',
                1,1,1,2,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 1 AND materias_asignadas.Id_hora_inicial = 1 AND materias_asignadas.Id_hora_final = 3 AND materias_asignadas.Estado = "Activo"',
                1,1,1,3,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 1 AND materias_asignadas.Id_hora_inicial = 1 AND materias_asignadas.Id_hora_final = 4 AND materias_asignadas.Estado = "Activo"',
                1,1,1,4,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 1 AND materias_asignadas.Id_hora_inicial = 1 AND materias_asignadas.Id_hora_final = 5 AND materias_asignadas.Estado = "Activo"',
                1,1,1,5,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 1 AND materias_asignadas.Id_hora_inicial = 1 AND materias_asignadas.Id_hora_final = 6 AND materias_asignadas.Estado = "Activo"',
                1,1,1,6,
                1,self.morning,self.setStyles4
            )

            # Primera linea Martes
            self.celda1x6(
                self.parametrosReportes,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 2 AND materias_asignadas.Id_hora_inicial = 1 AND materias_asignadas.Id_hora_final = 2 AND materias_asignadas.Estado = "Activo"',
                2,1,2,2,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 2 AND materias_asignadas.Id_hora_inicial = 1 AND materias_asignadas.Id_hora_final = 3 AND materias_asignadas.Estado = "Activo"',
                2,1,2,3,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 2 AND materias_asignadas.Id_hora_inicial = 1 AND materias_asignadas.Id_hora_final = 4 AND materias_asignadas.Estado = "Activo"',
                2,1,2,4,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 2 AND materias_asignadas.Id_hora_inicial = 1 AND materias_asignadas.Id_hora_final = 5 AND materias_asignadas.Estado = "Activo"',
                2,1,2,5,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 2 AND materias_asignadas.Id_hora_inicial = 1 AND materias_asignadas.Id_hora_final = 6 AND materias_asignadas.Estado = "Activo"',
                2,1,2,6,
                1,self.morning,self.setStyles4
            )

            # Primera linea Miercoles
            self.celda1x6(
                self.parametrosReportes,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 3 AND materias_asignadas.Id_hora_inicial = 1 AND materias_asignadas.Id_hora_final = 2 AND materias_asignadas.Estado = "Activo"',
                3,1,3,2,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 3 AND materias_asignadas.Id_hora_inicial = 1 AND materias_asignadas.Id_hora_final = 3 AND materias_asignadas.Estado = "Activo"',
                3,1,3,3,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 3 AND materias_asignadas.Id_hora_inicial = 1 AND materias_asignadas.Id_hora_final = 4 AND materias_asignadas.Estado = "Activo"',
                3,1,3,4,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 3 AND materias_asignadas.Id_hora_inicial = 1 AND materias_asignadas.Id_hora_final = 5 AND materias_asignadas.Estado = "Activo"',
                3,1,3,5,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 3 AND materias_asignadas.Id_hora_inicial = 1 AND materias_asignadas.Id_hora_final = 6 AND materias_asignadas.Estado = "Activo"',
                3,1,3,6,
                1,self.morning,self.setStyles4
            )

            # Primera linea Jueves
            self.celda1x6(
                self.parametrosReportes,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 4 AND materias_asignadas.Id_hora_inicial = 1 AND materias_asignadas.Id_hora_final = 2 AND materias_asignadas.Estado = "Activo"',
                4,1,4,2,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 4 AND materias_asignadas.Id_hora_inicial = 1 AND materias_asignadas.Id_hora_final = 3 AND materias_asignadas.Estado = "Activo"',
                4,1,4,3,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 4 AND materias_asignadas.Id_hora_inicial = 1 AND materias_asignadas.Id_hora_final = 4 AND materias_asignadas.Estado = "Activo"',
                4,1,4,4,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 4 AND materias_asignadas.Id_hora_inicial = 1 AND materias_asignadas.Id_hora_final = 5 AND materias_asignadas.Estado = "Activo"',
                4,1,4,5,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 4 AND materias_asignadas.Id_hora_inicial = 1 AND materias_asignadas.Id_hora_final = 6 AND materias_asignadas.Estado = "Activo"',
                4,1,4,6,
                1,self.morning,self.setStyles4
            )

            # Primera linea Viernes
            self.celda1x6(
                self.parametrosReportes,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 5 AND materias_asignadas.Id_hora_inicial = 1 AND materias_asignadas.Id_hora_final = 2 AND materias_asignadas.Estado = "Activo"',
                5,1,5,2,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 5 AND materias_asignadas.Id_hora_inicial = 1 AND materias_asignadas.Id_hora_final = 3 AND materias_asignadas.Estado = "Activo"',
                5,1,5,3,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 5 AND materias_asignadas.Id_hora_inicial = 1 AND materias_asignadas.Id_hora_final = 4 AND materias_asignadas.Estado = "Activo"',
                5,1,5,4,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 5 AND materias_asignadas.Id_hora_inicial = 1 AND materias_asignadas.Id_hora_final = 5 AND materias_asignadas.Estado = "Activo"',
                5,1,5,5,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 5 AND materias_asignadas.Id_hora_inicial = 1 AND materias_asignadas.Id_hora_final = 6 AND materias_asignadas.Estado = "Activo"',
                5,1,5,6,
                1,self.morning,self.setStyles4
            )

            print('Segunda linea ----------------')
            # Segunda linea lunes
            self.celda1x5(
                self.parametrosReportes,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 1 AND materias_asignadas.Id_hora_inicial = 2 AND materias_asignadas.Id_hora_final = 3 AND materias_asignadas.Estado = "Activo"',
                1,2,1,3,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 1 AND materias_asignadas.Id_hora_inicial = 2 AND materias_asignadas.Id_hora_final = 4 AND materias_asignadas.Estado = "Activo"',
                1,2,1,4,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 1 AND materias_asignadas.Id_hora_inicial = 2 AND materias_asignadas.Id_hora_final = 5 AND materias_asignadas.Estado = "Activo"',
                1,2,1,5,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 1 AND materias_asignadas.Id_hora_inicial = 2 AND materias_asignadas.Id_hora_final = 6 AND materias_asignadas.Estado = "Activo"',
                1,2,1,6,
                2,self.morning,self.setStyles4
            )

            # Segunda linea Martes
            self.celda1x5(
                self.parametrosReportes,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 2 AND materias_asignadas.Id_hora_inicial = 2 AND materias_asignadas.Id_hora_final = 3 AND materias_asignadas.Estado = "Activo"',
                2,2,2,3,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 2 AND materias_asignadas.Id_hora_inicial = 2 AND materias_asignadas.Id_hora_final = 4 AND materias_asignadas.Estado = "Activo"',
                2,2,2,4,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 2 AND materias_asignadas.Id_hora_inicial = 2 AND materias_asignadas.Id_hora_final = 5 AND materias_asignadas.Estado = "Activo"',
                2,2,2,5,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 2 AND materias_asignadas.Id_hora_inicial = 2 AND materias_asignadas.Id_hora_final = 6 AND materias_asignadas.Estado = "Activo"',
                2,2,2,6,
                2,self.morning,self.setStyles4
            )

            # Segunda linea Miercoles
            self.celda1x5(
                self.parametrosReportes,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 3 AND materias_asignadas.Id_hora_inicial = 2 AND materias_asignadas.Id_hora_final = 3 AND materias_asignadas.Estado = "Activo"',
                3,2,3,3,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 3 AND materias_asignadas.Id_hora_inicial = 2 AND materias_asignadas.Id_hora_final = 4 AND materias_asignadas.Estado = "Activo"',
                3,2,3,4,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 3 AND materias_asignadas.Id_hora_inicial = 2 AND materias_asignadas.Id_hora_final = 5 AND materias_asignadas.Estado = "Activo"',
                3,2,3,5,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 3 AND materias_asignadas.Id_hora_inicial = 2 AND materias_asignadas.Id_hora_final = 6 AND materias_asignadas.Estado = "Activo"',
                3,2,3,6,
                2,self.morning,self.setStyles4
            )

            # Segunda linea Jueves
            self.celda1x5(
                self.parametrosReportes,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 4 AND materias_asignadas.Id_hora_inicial = 2 AND materias_asignadas.Id_hora_final = 3 AND materias_asignadas.Estado = "Activo"',
                4,2,4,3,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 4 AND materias_asignadas.Id_hora_inicial = 2 AND materias_asignadas.Id_hora_final = 4 AND materias_asignadas.Estado = "Activo"',
                4,2,4,4,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 4 AND materias_asignadas.Id_hora_inicial = 2 AND materias_asignadas.Id_hora_final = 5 AND materias_asignadas.Estado = "Activo"',
                4,2,4,5,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 4 AND materias_asignadas.Id_hora_inicial = 2 AND materias_asignadas.Id_hora_final = 6 AND materias_asignadas.Estado = "Activo"',
                4,2,4,6,
                2,self.morning,self.setStyles4
            )

            # Segunda linea Viernes
            self.celda1x5(
                self.parametrosReportes,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 5 AND materias_asignadas.Id_hora_inicial = 2 AND materias_asignadas.Id_hora_final = 3 AND materias_asignadas.Estado = "Activo"',
                5,2,5,3,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 5 AND materias_asignadas.Id_hora_inicial = 2 AND materias_asignadas.Id_hora_final = 4 AND materias_asignadas.Estado = "Activo"',
                5,2,5,4,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 5 AND materias_asignadas.Id_hora_inicial = 2 AND materias_asignadas.Id_hora_final = 5 AND materias_asignadas.Estado = "Activo"',
                5,2,5,5,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 5 AND materias_asignadas.Id_hora_inicial = 2 AND materias_asignadas.Id_hora_final = 6 AND materias_asignadas.Estado = "Activo"',
                5,2,5,6,
                2,self.morning,self.setStyles4
            )

            print('Tercera linea ----------------')
            # Tercera linea lunes
            self.celda1x4(
                self.parametrosReportes,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 1 AND materias_asignadas.Id_hora_inicial = 3 AND materias_asignadas.Id_hora_final = 4 AND materias_asignadas.Estado = "Activo"',
                1,3,1,4,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 1 AND materias_asignadas.Id_hora_inicial = 3 AND materias_asignadas.Id_hora_final = 5 AND materias_asignadas.Estado = "Activo"',
                1,3,1,5,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 1 AND materias_asignadas.Id_hora_inicial = 3 AND materias_asignadas.Id_hora_final = 6 AND materias_asignadas.Estado = "Activo"',
                1,3,1,6,
                3,self.morning,self.setStyles4
            )

            # Tercera linea Martes
            self.celda1x4(
                self.parametrosReportes,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 2 AND materias_asignadas.Id_hora_inicial = 3 AND materias_asignadas.Id_hora_final = 4 AND materias_asignadas.Estado = "Activo"',
                2,3,2,4,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 2 AND materias_asignadas.Id_hora_inicial = 3 AND materias_asignadas.Id_hora_final = 5 AND materias_asignadas.Estado = "Activo"',
                2,3,2,5,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 2 AND materias_asignadas.Id_hora_inicial = 3 AND materias_asignadas.Id_hora_final = 6 AND materias_asignadas.Estado = "Activo"',
                2,3,2,6,
                3,self.morning,self.setStyles4
            )

            # Tercera linea Miercoles
            self.celda1x4(
                self.parametrosReportes,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 3 AND materias_asignadas.Id_hora_inicial = 3 AND materias_asignadas.Id_hora_final = 4 AND materias_asignadas.Estado = "Activo"',
                3,3,3,4,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 3 AND materias_asignadas.Id_hora_inicial = 3 AND materias_asignadas.Id_hora_final = 5 AND materias_asignadas.Estado = "Activo"',
                3,3,3,5,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 3 AND materias_asignadas.Id_hora_inicial = 3 AND materias_asignadas.Id_hora_final = 6 AND materias_asignadas.Estado = "Activo"',
                3,3,3,6,
                3,self.morning,self.setStyles4
            )

            # Tercera linea Jueves
            self.celda1x4(
                self.parametrosReportes,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 4 AND materias_asignadas.Id_hora_inicial = 3 AND materias_asignadas.Id_hora_final = 4 AND materias_asignadas.Estado = "Activo"',
                4,3,4,4,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 4 AND materias_asignadas.Id_hora_inicial = 3 AND materias_asignadas.Id_hora_final = 5 AND materias_asignadas.Estado = "Activo"',
                4,3,4,5,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 4 AND materias_asignadas.Id_hora_inicial = 3 AND materias_asignadas.Id_hora_final = 6 AND materias_asignadas.Estado = "Activo"',
                4,3,4,6,
                3,self.morning,self.setStyles4
            )

            # Tercera linea Viernes
            self.celda1x4(
                self.parametrosReportes,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 5 AND materias_asignadas.Id_hora_inicial = 3 AND materias_asignadas.Id_hora_final = 4 AND materias_asignadas.Estado = "Activo"',
                5,3,5,4,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 5 AND materias_asignadas.Id_hora_inicial = 3 AND materias_asignadas.Id_hora_final = 5 AND materias_asignadas.Estado = "Activo"',
                5,3,5,5,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 5 AND materias_asignadas.Id_hora_inicial = 3 AND materias_asignadas.Id_hora_final = 6 AND materias_asignadas.Estado = "Activo"',
                5,3,5,6,
                3,self.morning,self.setStyles4
            )

            print('Cuarta linea ----------------')
            # Cuarta linea lunes
            self.celda1x3(
                self.parametrosReportes,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 1 AND materias_asignadas.Id_hora_inicial = 4 AND materias_asignadas.Id_hora_final = 5 AND materias_asignadas.Estado = "Activo"',
                1,4,1,5,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 1 AND materias_asignadas.Id_hora_inicial = 4 AND materias_asignadas.Id_hora_final = 6 AND materias_asignadas.Estado = "Activo"',
                1,4,1,6,
                4,self.morning,self.setStyles4
            )

            # Cuarta linea Martes
            self.celda1x3(
                self.parametrosReportes,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 2 AND materias_asignadas.Id_hora_inicial = 4 AND materias_asignadas.Id_hora_final = 5 AND materias_asignadas.Estado = "Activo"',
                2,4,2,5,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 2 AND materias_asignadas.Id_hora_inicial = 4 AND materias_asignadas.Id_hora_final = 6 AND materias_asignadas.Estado = "Activo"',
                2,4,2,6,
                4,self.morning,self.setStyles4
            )

            # Cuarta linea Miercoles
            self.celda1x3(
                self.parametrosReportes,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 3 AND materias_asignadas.Id_hora_inicial = 4 AND materias_asignadas.Id_hora_final = 5 AND materias_asignadas.Estado = "Activo"',
                3,4,3,5,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 3 AND materias_asignadas.Id_hora_inicial = 4 AND materias_asignadas.Id_hora_final = 6 AND materias_asignadas.Estado = "Activo"',
                3,4,3,6,
                4,self.morning,self.setStyles4
            )

            # Cuarta linea Jueves
            self.celda1x3(
                self.parametrosReportes,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 4 AND materias_asignadas.Id_hora_inicial = 4 AND materias_asignadas.Id_hora_final = 5 AND materias_asignadas.Estado = "Activo"',
                4,4,4,5,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 4 AND materias_asignadas.Id_hora_inicial = 4 AND materias_asignadas.Id_hora_final = 6 AND materias_asignadas.Estado = "Activo"',
                4,4,4,6,
                4,self.morning,self.setStyles4
            )

            # Cuarta linea Viernes
            self.celda1x3(
                self.parametrosReportes,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 5 AND materias_asignadas.Id_hora_inicial = 4 AND materias_asignadas.Id_hora_final = 5 AND materias_asignadas.Estado = "Activo"',
                5,4,5,5,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 5 AND materias_asignadas.Id_hora_inicial = 4 AND materias_asignadas.Id_hora_final = 6 AND materias_asignadas.Estado = "Activo"',
                5,4,5,6,
                4,self.morning,self.setStyles4
            )

            print('Quinta linea ----------------')
            # Quinta linea lunes
            self.celda1x2(
                self.parametrosReportes,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 1 AND materias_asignadas.Id_hora_inicial = 5 AND materias_asignadas.Id_hora_final = 6 AND materias_asignadas.Estado = "Activo"',
                1,5,1,6,
                5,self.morning,self.setStyles4
            )

            # Quinta linea Martes
            self.celda1x2(
                self.parametrosReportes,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 2 AND materias_asignadas.Id_hora_inicial = 5 AND materias_asignadas.Id_hora_final = 6 AND materias_asignadas.Estado = "Activo"',
                2,5,2,6,
                5,self.morning,self.setStyles4
            )

            # Quinta linea Miercoles
            self.celda1x2(
                self.parametrosReportes,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 3 AND materias_asignadas.Id_hora_inicial = 5 AND materias_asignadas.Id_hora_final = 6 AND materias_asignadas.Estado = "Activo"',
                3,5,3,6,
                5,self.morning,self.setStyles4
            )

            # Quinta linea Jueves
            self.celda1x2(
                self.parametrosReportes,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 4 AND materias_asignadas.Id_hora_inicial = 5 AND materias_asignadas.Id_hora_final = 6 AND materias_asignadas.Estado = "Activo"',
                4,5,4,6,
                5,self.morning,self.setStyles4
            )

            # Quinta linea Viernes
            self.celda1x2(
                self.parametrosReportes,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 5 AND materias_asignadas.Id_hora_inicial = 5 AND materias_asignadas.Id_hora_final = 6 AND materias_asignadas.Estado = "Activo"',
                5,5,5,6,
                5,self.morning,self.setStyles4
            )

            return self.morning


    def tablaHorarioAfternon(self):
            self.tableHorarioAfternon = Table(self.obtenerTablaHorarioAfternon(),colWidths=137, rowHeights=25)
            self.tableHorarioAfternon.setStyle(TableStyle(self.setStyles5))
            self.tableHorarioAfternon.wrapOn(self.pdf,self.width,self.heigth)
            if self.counter == 10: 
                # self.pdf.showPage()
                self.tableHorarioAfternon.drawOn(self.pdf,11,120)
                print('afternon----10')
            elif self.counter == 9: 
                self.tableHorarioAfternon.drawOn(self.pdf,11,160)
                print('afternon-----9')
            elif self.counter == 8: 
                self.tableHorarioAfternon.drawOn(self.pdf,11,195)
                print('afternon-----8')
            elif self.counter == 7: 
                self.tableHorarioAfternon.drawOn(self.pdf,11,230)
                print('afternon-----7')
            elif self.counter == 6: 
                self.tableHorarioAfternon.drawOn(self.pdf,11,270)
                print('afternon-----6')
            elif self.counter == 5: 
                self.tableHorarioAfternon.drawOn(self.pdf,11,320)
                print('afternon-----5')
            elif self.counter == 4: 
                self.tableHorarioAfternon.drawOn(self.pdf,11,360)
                print('afternon-----4')
            elif self.counter == 3: 
                self.tableHorarioAfternon.drawOn(self.pdf,11,400)
                print('afternon-----3')
            elif self.counter == 2: 
                self.tableHorarioAfternon.drawOn(self.pdf,11,440)
                print('afternon-----2')
            elif self.counter == 1: 
                self.tableHorarioAfternon.drawOn(self.pdf,11,480)
                print('afternon-----1')
            else:
                self.tableHorarioAfternon.drawOn(self.pdf,11,480)
                print('afternon-----0')
            return self.tableHorarioAfternon


    def obtenerTablaHorarioAfternon(self):
            self.afternon = [
                [Paragraph('Horario de Clases Tarde',self.center),Paragraph('Lunes',self.center),Paragraph('Martes',self.center),Paragraph('Miércoles',self.center),Paragraph('Jueves',self.center),Paragraph('Viernes',self.center)],
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
                self.parametrosReportes,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 1 AND materias_asignadas.Id_hora_inicial = 7 AND materias_asignadas.Id_hora_final = 8 AND materias_asignadas.Estado = "Activo"',
                1,1,1,2,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 1 AND materias_asignadas.Id_hora_inicial = 7 AND materias_asignadas.Id_hora_final = 9 AND materias_asignadas.Estado = "Activo"',
                1,1,1,3,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 1 AND materias_asignadas.Id_hora_inicial = 7 AND materias_asignadas.Id_hora_final = 10 AND materias_asignadas.Estado = "Activo"',
                1,1,1,4,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 1 AND materias_asignadas.Id_hora_inicial = 7 AND materias_asignadas.Id_hora_final = 11 AND materias_asignadas.Estado = "Activo"',
                1,1,1,5,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 1 AND materias_asignadas.Id_hora_inicial = 7 AND materias_asignadas.Id_hora_final = 12 AND materias_asignadas.Estado = "Activo"',
                1,1,1,6,
                1,self.afternon,self.setStyles5
            )

            # Primera linea Martes
            self.celda1x6(
                self.parametrosReportes,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 2 AND materias_asignadas.Id_hora_inicial = 7 AND materias_asignadas.Id_hora_final = 8 AND materias_asignadas.Estado = "Activo"',
                2,1,2,2,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 2 AND materias_asignadas.Id_hora_inicial = 7 AND materias_asignadas.Id_hora_final = 9 AND materias_asignadas.Estado = "Activo"',
                2,1,2,3,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 2 AND materias_asignadas.Id_hora_inicial = 7 AND materias_asignadas.Id_hora_final = 10 AND materias_asignadas.Estado = "Activo"',
                2,1,2,4,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 2 AND materias_asignadas.Id_hora_inicial = 7 AND materias_asignadas.Id_hora_final = 11 AND materias_asignadas.Estado = "Activo"',
                2,1,2,5,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 2 AND materias_asignadas.Id_hora_inicial = 7 AND materias_asignadas.Id_hora_final = 12 AND materias_asignadas.Estado = "Activo"',
                2,1,2,6,
                1,self.afternon,self.setStyles5
            )

            # Primera linea Miercoles
            self.celda1x6(
                self.parametrosReportes,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 3 AND materias_asignadas.Id_hora_inicial = 7 AND materias_asignadas.Id_hora_final = 8 AND materias_asignadas.Estado = "Activo"',
                3,1,3,2,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 3 AND materias_asignadas.Id_hora_inicial = 7 AND materias_asignadas.Id_hora_final = 9 AND materias_asignadas.Estado = "Activo"',
                3,1,3,3,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 3 AND materias_asignadas.Id_hora_inicial = 7 AND materias_asignadas.Id_hora_final = 10 AND materias_asignadas.Estado = "Activo"',
                3,1,3,4,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 3 AND materias_asignadas.Id_hora_inicial = 7 AND materias_asignadas.Id_hora_final = 11 AND materias_asignadas.Estado = "Activo"',
                3,1,3,5,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 3 AND materias_asignadas.Id_hora_inicial = 7 AND materias_asignadas.Id_hora_final = 12 AND materias_asignadas.Estado = "Activo"',
                3,1,3,6,
                1,self.afternon,self.setStyles5
            )

            # Primera linea Jueves
            self.celda1x6(
                self.parametrosReportes,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 4 AND materias_asignadas.Id_hora_inicial = 7 AND materias_asignadas.Id_hora_final = 8 AND materias_asignadas.Estado = "Activo"',
                4,1,4,2,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 4 AND materias_asignadas.Id_hora_inicial = 7 AND materias_asignadas.Id_hora_final = 9 AND materias_asignadas.Estado = "Activo"',
                4,1,4,3,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 4 AND materias_asignadas.Id_hora_inicial = 7 AND materias_asignadas.Id_hora_final = 10 AND materias_asignadas.Estado = "Activo"',
                4,1,4,4,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 4 AND materias_asignadas.Id_hora_inicial = 7 AND materias_asignadas.Id_hora_final = 11 AND materias_asignadas.Estado = "Activo"',
                4,1,4,5,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 4 AND materias_asignadas.Id_hora_inicial = 7 AND materias_asignadas.Id_hora_final = 12 AND materias_asignadas.Estado = "Activo"',
                4,1,4,6,
                1,self.afternon,self.setStyles5
            )

            # Primera linea Viernes
            self.celda1x6(
                self.parametrosReportes,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 5 AND materias_asignadas.Id_hora_inicial = 7 AND materias_asignadas.Id_hora_final = 8 AND materias_asignadas.Estado = "Activo"',
                5,1,5,2,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 5 AND materias_asignadas.Id_hora_inicial = 7 AND materias_asignadas.Id_hora_final = 9 AND materias_asignadas.Estado = "Activo"',
                5,1,5,3,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 5 AND materias_asignadas.Id_hora_inicial = 7 AND materias_asignadas.Id_hora_final = 10 AND materias_asignadas.Estado = "Activo"',
                5,1,5,4,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 5 AND materias_asignadas.Id_hora_inicial = 7 AND materias_asignadas.Id_hora_final = 11 AND materias_asignadas.Estado = "Activo"',
                5,1,5,5,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 5 AND materias_asignadas.Id_hora_inicial = 7 AND materias_asignadas.Id_hora_final = 12 AND materias_asignadas.Estado = "Activo"',
                5,1,5,6,
                1,self.afternon,self.setStyles5
            )

            print('Segunda linea ----------------')
            # Segunda linea lunes
            self.celda1x5(
                self.parametrosReportes,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 1 AND materias_asignadas.Id_hora_inicial = 8 AND materias_asignadas.Id_hora_final = 9 AND materias_asignadas.Estado = "Activo"',
                1,2,1,3,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 1 AND materias_asignadas.Id_hora_inicial = 8 AND materias_asignadas.Id_hora_final = 10 AND materias_asignadas.Estado = "Activo"',
                1,2,1,4,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 1 AND materias_asignadas.Id_hora_inicial = 8 AND materias_asignadas.Id_hora_final = 11 AND materias_asignadas.Estado = "Activo"',
                1,2,1,5,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 1 AND materias_asignadas.Id_hora_inicial = 8 AND materias_asignadas.Id_hora_final = 12 AND materias_asignadas.Estado = "Activo"',
                1,2,1,6,
                2,self.afternon,self.setStyles5
            )

            # Segunda linea Martes
            self.celda1x5(
                self.parametrosReportes,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 2 AND materias_asignadas.Id_hora_inicial = 8 AND materias_asignadas.Id_hora_final = 9 AND materias_asignadas.Estado = "Activo"',
                2,2,2,3,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 2 AND materias_asignadas.Id_hora_inicial = 8 AND materias_asignadas.Id_hora_final = 10 AND materias_asignadas.Estado = "Activo"',
                2,2,2,4,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 2 AND materias_asignadas.Id_hora_inicial = 8 AND materias_asignadas.Id_hora_final = 11 AND materias_asignadas.Estado = "Activo"',
                2,2,2,5,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 2 AND materias_asignadas.Id_hora_inicial = 8 AND materias_asignadas.Id_hora_final = 12 AND materias_asignadas.Estado = "Activo"',
                2,2,2,6,
                2,self.afternon,self.setStyles5
            )

            # Segunda linea Miercoles
            self.celda1x5(
                self.parametrosReportes,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 3 AND materias_asignadas.Id_hora_inicial = 8 AND materias_asignadas.Id_hora_final = 9 AND materias_asignadas.Estado = "Activo"',
                3,2,3,3,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 3 AND materias_asignadas.Id_hora_inicial = 8 AND materias_asignadas.Id_hora_final = 10 AND materias_asignadas.Estado = "Activo"',
                3,2,3,4,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 3 AND materias_asignadas.Id_hora_inicial = 8 AND materias_asignadas.Id_hora_final = 11 AND materias_asignadas.Estado = "Activo"',
                3,2,3,5,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 3 AND materias_asignadas.Id_hora_inicial = 8 AND materias_asignadas.Id_hora_final = 12 AND materias_asignadas.Estado = "Activo"',
                3,2,3,6,
                2,self.afternon,self.setStyles5
            )

            # Segunda linea Jueves
            self.celda1x5(
                self.parametrosReportes,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 4 AND materias_asignadas.Id_hora_inicial = 8 AND materias_asignadas.Id_hora_final = 9 AND materias_asignadas.Estado = "Activo"',
                4,2,4,3,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 4 AND materias_asignadas.Id_hora_inicial = 8 AND materias_asignadas.Id_hora_final = 10 AND materias_asignadas.Estado = "Activo"',
                4,2,4,4,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 4 AND materias_asignadas.Id_hora_inicial = 8 AND materias_asignadas.Id_hora_final = 11 AND materias_asignadas.Estado = "Activo"',
                4,2,4,5,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 4 AND materias_asignadas.Id_hora_inicial = 8 AND materias_asignadas.Id_hora_final = 12 AND materias_asignadas.Estado = "Activo"',
                4,2,4,6,
                2,self.afternon,self.setStyles5
            )

            # Segunda linea Viernes
            self.celda1x5(
                self.parametrosReportes,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 5 AND materias_asignadas.Id_hora_inicial = 8 AND materias_asignadas.Id_hora_final = 9 AND materias_asignadas.Estado = "Activo"',
                5,2,5,3,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 5 AND materias_asignadas.Id_hora_inicial = 8 AND materias_asignadas.Id_hora_final = 10 AND materias_asignadas.Estado = "Activo"',
                5,2,5,4,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 5 AND materias_asignadas.Id_hora_inicial = 8 AND materias_asignadas.Id_hora_final = 11 AND materias_asignadas.Estado = "Activo"',
                5,2,5,5,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 5 AND materias_asignadas.Id_hora_inicial = 8 AND materias_asignadas.Id_hora_final = 12 AND materias_asignadas.Estado = "Activo"',
                5,2,5,6,
                2,self.afternon,self.setStyles5
            )

            print('Tercera linea ----------------')
            # Tercera linea lunes
            self.celda1x4(
                self.parametrosReportes,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 1 AND materias_asignadas.Id_hora_inicial = 9 AND materias_asignadas.Id_hora_final = 10 AND materias_asignadas.Estado = "Activo"',
                1,3,1,4,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 1 AND materias_asignadas.Id_hora_inicial = 9 AND materias_asignadas.Id_hora_final = 11 AND materias_asignadas.Estado = "Activo"',
                1,3,1,5,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 1 AND materias_asignadas.Id_hora_inicial = 9 AND materias_asignadas.Id_hora_final = 12 AND materias_asignadas.Estado = "Activo"',
                1,3,1,6,
                3,self.afternon,self.setStyles5
            )

            # Tercera linea Martes
            self.celda1x4(
                self.parametrosReportes,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 2 AND materias_asignadas.Id_hora_inicial = 9 AND materias_asignadas.Id_hora_final = 10 AND materias_asignadas.Estado = "Activo"',
                2,3,2,4,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 2 AND materias_asignadas.Id_hora_inicial = 9 AND materias_asignadas.Id_hora_final = 11 AND materias_asignadas.Estado = "Activo"',
                2,3,2,5,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 2 AND materias_asignadas.Id_hora_inicial = 9 AND materias_asignadas.Id_hora_final = 12 AND materias_asignadas.Estado = "Activo"',
                2,3,2,6,
                3,self.afternon,self.setStyles5
            )

            # Tercera linea Miercoles
            self.celda1x4(
                self.parametrosReportes,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 3 AND materias_asignadas.Id_hora_inicial = 9 AND materias_asignadas.Id_hora_final = 10 AND materias_asignadas.Estado = "Activo"',
                3,3,3,4,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 3 AND materias_asignadas.Id_hora_inicial = 9 AND materias_asignadas.Id_hora_final = 11 AND materias_asignadas.Estado = "Activo"',
                3,3,3,5,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 3 AND materias_asignadas.Id_hora_inicial = 9 AND materias_asignadas.Id_hora_final = 12 AND materias_asignadas.Estado = "Activo"',
                3,3,3,6,
                3,self.afternon,self.setStyles5
            )

            # Tercera linea Jueves
            self.celda1x4(
                self.parametrosReportes,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 4 AND materias_asignadas.Id_hora_inicial = 9 AND materias_asignadas.Id_hora_final = 10 AND materias_asignadas.Estado = "Activo"',
                4,3,4,4,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 4 AND materias_asignadas.Id_hora_inicial = 9 AND materias_asignadas.Id_hora_final = 11 AND materias_asignadas.Estado = "Activo"',
                4,3,4,5,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 4 AND materias_asignadas.Id_hora_inicial = 9 AND materias_asignadas.Id_hora_final = 12 AND materias_asignadas.Estado = "Activo"',
                4,3,4,6,
                3,self.afternon,self.setStyles5
            )

            # Tercera linea Viernes
            self.celda1x4(
                self.parametrosReportes,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 5 AND materias_asignadas.Id_hora_inicial = 9 AND materias_asignadas.Id_hora_final = 10 AND materias_asignadas.Estado = "Activo"',
                5,3,5,4,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 5 AND materias_asignadas.Id_hora_inicial = 9 AND materias_asignadas.Id_hora_final = 11 AND materias_asignadas.Estado = "Activo"',
                5,3,5,5,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 5 AND materias_asignadas.Id_hora_inicial = 9 AND materias_asignadas.Id_hora_final = 12 AND materias_asignadas.Estado = "Activo"',
                5,3,5,6,
                3,self.afternon,self.setStyles5
            )

            print('Cuarta linea ----------------')
            # Cuarta linea lunes
            self.celda1x3(
                self.parametrosReportes,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 1 AND materias_asignadas.Id_hora_inicial = 10 AND materias_asignadas.Id_hora_final = 11 AND materias_asignadas.Estado = "Activo"',
                1,4,1,5,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 1 AND materias_asignadas.Id_hora_inicial = 10 AND materias_asignadas.Id_hora_final = 12 AND materias_asignadas.Estado = "Activo"',
                1,4,1,6,
                4,self.afternon,self.setStyles5
            )

            # Cuarta linea Martes
            self.celda1x3(
                self.parametrosReportes,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 2 AND materias_asignadas.Id_hora_inicial = 10 AND materias_asignadas.Id_hora_final = 11 AND materias_asignadas.Estado = "Activo"',
                2,4,2,5,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 2 AND materias_asignadas.Id_hora_inicial = 10 AND materias_asignadas.Id_hora_final = 12 AND materias_asignadas.Estado = "Activo"',
                2,4,2,6,
                4,self.afternon,self.setStyles5
            )

            # Cuarta linea Miercoles
            self.celda1x3(
                self.parametrosReportes,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 3 AND materias_asignadas.Id_hora_inicial = 10 AND materias_asignadas.Id_hora_final = 11 AND materias_asignadas.Estado = "Activo"',
                3,4,3,5,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 3 AND materias_asignadas.Id_hora_inicial = 10 AND materias_asignadas.Id_hora_final = 12 AND materias_asignadas.Estado = "Activo"',
                3,4,3,6,
                4,self.afternon,self.setStyles5
            )

            # Cuarta linea Jueves
            self.celda1x3(
                self.parametrosReportes,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 4 AND materias_asignadas.Id_hora_inicial = 10 AND materias_asignadas.Id_hora_final = 11 AND materias_asignadas.Estado = "Activo"',
                4,4,4,5,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 4 AND materias_asignadas.Id_hora_inicial = 10 AND materias_asignadas.Id_hora_final = 12 AND materias_asignadas.Estado = "Activo"',
                4,4,4,6,
                4,self.afternon,self.setStyles5
            )

            # Cuarta linea Viernes
            self.celda1x3(
                self.parametrosReportes,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 5 AND materias_asignadas.Id_hora_inicial = 10 AND materias_asignadas.Id_hora_final = 11 AND materias_asignadas.Estado = "Activo"',
                5,4,5,5,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 5 AND materias_asignadas.Id_hora_inicial = 10 AND materias_asignadas.Id_hora_final = 12 AND materias_asignadas.Estado = "Activo"',
                5,4,5,6,
                4,self.afternon,self.setStyles5
            )

            print('Quinta linea ----------------')
            # Quinta linea lunes
            self.celda1x2(
                self.parametrosReportes,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 1 AND materias_asignadas.Id_hora_inicial = 11 AND materias_asignadas.Id_hora_final = 12 AND materias_asignadas.Estado = "Activo"',
                1,5,1,6,
                5,self.afternon,self.setStyles5
            )

            # Quinta linea Martes
            self.celda1x2(
                self.parametrosReportes,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 2 AND materias_asignadas.Id_hora_inicial = 11 AND materias_asignadas.Id_hora_final = 12 AND materias_asignadas.Estado = "Activo"',
                2,5,2,6,
                5,self.afternon,self.setStyles5
            )

            # Quinta linea Miercoles
            self.celda1x2(
                self.parametrosReportes,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 3 AND materias_asignadas.Id_hora_inicial = 11 AND materias_asignadas.Id_hora_final = 12 AND materias_asignadas.Estado = "Activo"',
                3,5,3,6,
                5,self.afternon,self.setStyles5
            )

            # Quinta linea Jueves
            self.celda1x2(
                self.parametrosReportes,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 4 AND materias_asignadas.Id_hora_inicial = 11 AND materias_asignadas.Id_hora_final = 12 AND materias_asignadas.Estado = "Activo"',
                4,5,4,6,
                5,self.afternon,self.setStyles5
            )

            # Quinta linea Viernes
            self.celda1x2(
                self.parametrosReportes,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 5 AND materias_asignadas.Id_hora_inicial = 11 AND materias_asignadas.Id_hora_final = 12 AND materias_asignadas.Estado = "Activo"',
                5,5,5,6,
                5,self.afternon,self.setStyles5
            )

            return self.afternon

    def tablaHorarioNinght(self):
            self.tableHorarioNinght = Table(self.obtenerTablaHorarioNinght(),colWidths=137, rowHeights=25)
            self.tableHorarioNinght.setStyle(TableStyle(self.setStyles6))
            self.tableHorarioNinght.wrapOn(self.pdf,self.width,self.heigth)
            if self.counter == 10: 
                self.pdf.showPage()
                self.tableHorarioNinght.drawOn(self.pdf,11,990)
                print('ninght----10')
            elif self.counter == 9: 
                self.pdf.showPage()
                self.tableHorarioNinght.drawOn(self.pdf,11,990)
                print('ninght-----9')
            elif self.counter == 8: 
                self.tableHorarioNinght.drawOn(self.pdf,11,10)
                print('ninght-----8')
            elif self.counter == 7: 
                self.tableHorarioNinght.drawOn(self.pdf,11,50)
                print('ninght-----7')
            elif self.counter == 6: 
                self.tableHorarioNinght.drawOn(self.pdf,11,90)
                print('ninght-----6')
            elif self.counter == 5: 
                self.tableHorarioNinght.drawOn(self.pdf,11,140)
                print('ninght-----5')
            elif self.counter == 4: 
                self.tableHorarioNinght.drawOn(self.pdf,11,180)
                print('ninght-----4')
            elif self.counter == 3: 
                self.tableHorarioNinght.drawOn(self.pdf,11,220)
                print('ninght-----3')
            elif self.counter == 2: 
                self.tableHorarioNinght.drawOn(self.pdf,11,260)
                print('ninght-----2')
            elif self.counter == 1: 
                self.tableHorarioNinght.drawOn(self.pdf,11,300)
                print('ninght-----1')
            else:
                self.tableHorarioNinght.drawOn(self.pdf,11,300)
                print('ninght-----0')
            return self.tableHorarioNinght

    def obtenerTablaHorarioNinght(self):
            self.ninght = [
                [Paragraph('Horario de Clases Noche',self.center),Paragraph('Lunes',self.center),Paragraph('Martes',self.center),Paragraph('Miércoles',self.center),Paragraph('Jueves',self.center),Paragraph('Viernes',self.center)],
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
                self.parametrosReportes,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 1 AND materias_asignadas.Id_hora_inicial = 13 AND materias_asignadas.Id_hora_final = 14 AND materias_asignadas.Estado = "Activo"',
                1,1,1,2,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 1 AND materias_asignadas.Id_hora_inicial = 13 AND materias_asignadas.Id_hora_final = 15 AND materias_asignadas.Estado = "Activo"',
                1,1,1,3,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 1 AND materias_asignadas.Id_hora_inicial = 13 AND materias_asignadas.Id_hora_final = 16 AND materias_asignadas.Estado = "Activo"',
                1,1,1,4,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 1 AND materias_asignadas.Id_hora_inicial = 13 AND materias_asignadas.Id_hora_final = 17 AND materias_asignadas.Estado = "Activo"',
                1,1,1,5,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 1 AND materias_asignadas.Id_hora_inicial = 13 AND materias_asignadas.Id_hora_final = 18 AND materias_asignadas.Estado = "Activo"',
                1,1,1,6,
                1,self.ninght,self.setStyles6
            )

            # Primera linea Martes
            self.celda1x6(
                self.parametrosReportes,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 2 AND materias_asignadas.Id_hora_inicial = 13 AND materias_asignadas.Id_hora_final = 14 AND materias_asignadas.Estado = "Activo"',
                2,1,2,2,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 2 AND materias_asignadas.Id_hora_inicial = 13 AND materias_asignadas.Id_hora_final = 15 AND materias_asignadas.Estado = "Activo"',
                2,1,2,3,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 2 AND materias_asignadas.Id_hora_inicial = 13 AND materias_asignadas.Id_hora_final = 16 AND materias_asignadas.Estado = "Activo"',
                2,1,2,4,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 2 AND materias_asignadas.Id_hora_inicial = 13 AND materias_asignadas.Id_hora_final = 17 AND materias_asignadas.Estado = "Activo"',
                2,1,2,5,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 2 AND materias_asignadas.Id_hora_inicial = 13 AND materias_asignadas.Id_hora_final = 18 AND materias_asignadas.Estado = "Activo"',
                2,1,2,6,
                1,self.ninght,self.setStyles6
            )

            # Primera linea Miercoles
            self.celda1x6(
                self.parametrosReportes,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 3 AND materias_asignadas.Id_hora_inicial = 13 AND materias_asignadas.Id_hora_final = 14 AND materias_asignadas.Estado = "Activo"',
                3,1,3,2,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 3 AND materias_asignadas.Id_hora_inicial = 13 AND materias_asignadas.Id_hora_final = 15 AND materias_asignadas.Estado = "Activo"',
                3,1,3,3,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 3 AND materias_asignadas.Id_hora_inicial = 13 AND materias_asignadas.Id_hora_final = 16 AND materias_asignadas.Estado = "Activo"',
                3,1,3,4,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 3 AND materias_asignadas.Id_hora_inicial = 13 AND materias_asignadas.Id_hora_final = 17 AND materias_asignadas.Estado = "Activo"',
                3,1,3,5,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 3 AND materias_asignadas.Id_hora_inicial = 13 AND materias_asignadas.Id_hora_final = 18 AND materias_asignadas.Estado = "Activo"',
                3,1,3,6,
                1,self.ninght,self.setStyles6
            )

            # Primera linea Jueves
            self.celda1x6(
                self.parametrosReportes,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 4 AND materias_asignadas.Id_hora_inicial = 13 AND materias_asignadas.Id_hora_final = 14 AND materias_asignadas.Estado = "Activo"',
                4,1,4,2,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 4 AND materias_asignadas.Id_hora_inicial = 13 AND materias_asignadas.Id_hora_final = 15 AND materias_asignadas.Estado = "Activo"',
                4,1,4,3,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 4 AND materias_asignadas.Id_hora_inicial = 13 AND materias_asignadas.Id_hora_final = 16 AND materias_asignadas.Estado = "Activo"',
                4,1,4,4,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 4 AND materias_asignadas.Id_hora_inicial = 13 AND materias_asignadas.Id_hora_final = 17 AND materias_asignadas.Estado = "Activo"',
                4,1,4,5,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 4 AND materias_asignadas.Id_hora_inicial = 13 AND materias_asignadas.Id_hora_final = 18 AND materias_asignadas.Estado = "Activo"',
                4,1,4,6,
                1,self.ninght,self.setStyles6
            )

            # Primera linea Viernes
            self.celda1x6(
                self.parametrosReportes,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 5 AND materias_asignadas.Id_hora_inicial = 13 AND materias_asignadas.Id_hora_final = 14 AND materias_asignadas.Estado = "Activo"',
                5,1,5,2,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 5 AND materias_asignadas.Id_hora_inicial = 13 AND materias_asignadas.Id_hora_final = 15 AND materias_asignadas.Estado = "Activo"',
                5,1,5,3,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 5 AND materias_asignadas.Id_hora_inicial = 13 AND materias_asignadas.Id_hora_final = 16 AND materias_asignadas.Estado = "Activo"',
                5,1,5,4,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 5 AND materias_asignadas.Id_hora_inicial = 13 AND materias_asignadas.Id_hora_final = 17 AND materias_asignadas.Estado = "Activo"',
                5,1,5,5,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 5 AND materias_asignadas.Id_hora_inicial = 13 AND materias_asignadas.Id_hora_final = 18 AND materias_asignadas.Estado = "Activo"',
                5,1,5,6,
                1,self.ninght,self.setStyles6
            )

            print('Segunda linea ----------------')
            # Segunda linea lunes
            self.celda1x5(
                self.parametrosReportes,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 1 AND materias_asignadas.Id_hora_inicial = 14 AND materias_asignadas.Id_hora_final = 15 AND materias_asignadas.Estado = "Activo"',
                1,2,1,3,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 1 AND materias_asignadas.Id_hora_inicial = 14 AND materias_asignadas.Id_hora_final = 16 AND materias_asignadas.Estado = "Activo"',
                1,2,1,4,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 1 AND materias_asignadas.Id_hora_inicial = 14 AND materias_asignadas.Id_hora_final = 17 AND materias_asignadas.Estado = "Activo"',
                1,2,1,5,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 1 AND materias_asignadas.Id_hora_inicial = 14 AND materias_asignadas.Id_hora_final = 18 AND materias_asignadas.Estado = "Activo"',
                1,2,1,6,
                2,self.ninght,self.setStyles6
            )

            # Segunda linea Martes
            self.celda1x5(
                self.parametrosReportes,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 2 AND materias_asignadas.Id_hora_inicial = 14 AND materias_asignadas.Id_hora_final = 15 AND materias_asignadas.Estado = "Activo"',
                2,2,2,3,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 2 AND materias_asignadas.Id_hora_inicial = 14 AND materias_asignadas.Id_hora_final = 16 AND materias_asignadas.Estado = "Activo"',
                2,2,2,4,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 2 AND materias_asignadas.Id_hora_inicial = 14 AND materias_asignadas.Id_hora_final = 17 AND materias_asignadas.Estado = "Activo"',
                2,2,2,5,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 2 AND materias_asignadas.Id_hora_inicial = 14 AND materias_asignadas.Id_hora_final = 18 AND materias_asignadas.Estado = "Activo"',
                2,2,2,6,
                2,self.ninght,self.setStyles6
            )

            # Segunda linea Miercoles
            self.celda1x5(
                self.parametrosReportes,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 3 AND materias_asignadas.Id_hora_inicial = 14 AND materias_asignadas.Id_hora_final = 15 AND materias_asignadas.Estado = "Activo"',
                3,2,3,3,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 3 AND materias_asignadas.Id_hora_inicial = 14 AND materias_asignadas.Id_hora_final = 16 AND materias_asignadas.Estado = "Activo"',
                3,2,3,4,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 3 AND materias_asignadas.Id_hora_inicial = 14 AND materias_asignadas.Id_hora_final = 17 AND materias_asignadas.Estado = "Activo"',
                3,2,3,5,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 3 AND materias_asignadas.Id_hora_inicial = 14 AND materias_asignadas.Id_hora_final = 18 AND materias_asignadas.Estado = "Activo"',
                3,2,3,6,
                2,self.ninght,self.setStyles6
            )

            # Segunda linea Jueves
            self.celda1x5(
                self.parametrosReportes,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 4 AND materias_asignadas.Id_hora_inicial = 14 AND materias_asignadas.Id_hora_final = 15 AND materias_asignadas.Estado = "Activo"',
                4,2,4,3,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 4 AND materias_asignadas.Id_hora_inicial = 14 AND materias_asignadas.Id_hora_final = 16 AND materias_asignadas.Estado = "Activo"',
                4,2,4,4,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 4 AND materias_asignadas.Id_hora_inicial = 14 AND materias_asignadas.Id_hora_final = 17 AND materias_asignadas.Estado = "Activo"',
                4,2,4,5,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 4 AND materias_asignadas.Id_hora_inicial = 14 AND materias_asignadas.Id_hora_final = 18 AND materias_asignadas.Estado = "Activo"',
                4,2,4,6,
                2,self.ninght,self.setStyles6
            )
            
            # Segunda linea Viernes
            self.celda1x5(
                self.parametrosReportes,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 5 AND materias_asignadas.Id_hora_inicial = 14 AND materias_asignadas.Id_hora_final = 15 AND materias_asignadas.Estado = "Activo"',
                5,2,5,3,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 5 AND materias_asignadas.Id_hora_inicial = 14 AND materias_asignadas.Id_hora_final = 16 AND materias_asignadas.Estado = "Activo"',
                5,2,5,4,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 5 AND materias_asignadas.Id_hora_inicial = 14 AND materias_asignadas.Id_hora_final = 17 AND materias_asignadas.Estado = "Activo"',
                5,2,5,5,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 5 AND materias_asignadas.Id_hora_inicial = 14 AND materias_asignadas.Id_hora_final = 18 AND materias_asignadas.Estado = "Activo"',
                5,2,5,6,
                2,self.ninght,self.setStyles6
            )

            print('Tercera linea ----------------')
            # Tercera linea lunes
            self.celda1x4(
                self.parametrosReportes,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 1 AND materias_asignadas.Id_hora_inicial = 15 AND materias_asignadas.Id_hora_final = 16 AND materias_asignadas.Estado = "Activo"',
                1,3,1,4,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 1 AND materias_asignadas.Id_hora_inicial = 15 AND materias_asignadas.Id_hora_final = 17 AND materias_asignadas.Estado = "Activo"',
                1,3,1,5,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 1 AND materias_asignadas.Id_hora_inicial = 15 AND materias_asignadas.Id_hora_final = 18 AND materias_asignadas.Estado = "Activo"',
                1,3,1,6,
                3,self.ninght,self.setStyles6
            )

            # Tercera linea Martes
            self.celda1x4(
                self.parametrosReportes,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 2 AND materias_asignadas.Id_hora_inicial = 15 AND materias_asignadas.Id_hora_final = 16 AND materias_asignadas.Estado = "Activo"',
                2,3,2,4,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 2 AND materias_asignadas.Id_hora_inicial = 15 AND materias_asignadas.Id_hora_final = 17 AND materias_asignadas.Estado = "Activo"',
                2,3,2,5,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 2 AND materias_asignadas.Id_hora_inicial = 15 AND materias_asignadas.Id_hora_final = 18 AND materias_asignadas.Estado = "Activo"',
                2,3,2,6,
                3,self.ninght,self.setStyles6
            )

            # Tercera linea Miercoles
            self.celda1x4(
                self.parametrosReportes,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 3 AND materias_asignadas.Id_hora_inicial = 15 AND materias_asignadas.Id_hora_final = 16 AND materias_asignadas.Estado = "Activo"',
                3,3,3,4,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 3 AND materias_asignadas.Id_hora_inicial = 15 AND materias_asignadas.Id_hora_final = 17 AND materias_asignadas.Estado = "Activo"',
                3,3,3,5,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 3 AND materias_asignadas.Id_hora_inicial = 15 AND materias_asignadas.Id_hora_final = 18 AND materias_asignadas.Estado = "Activo"',
                3,3,3,6,
                3,self.ninght,self.setStyles6
            )

            # Tercera linea Jueves
            self.celda1x4(
                self.parametrosReportes,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 4 AND materias_asignadas.Id_hora_inicial = 15 AND materias_asignadas.Id_hora_final = 16 AND materias_asignadas.Estado = "Activo"',
                4,3,4,4,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 4 AND materias_asignadas.Id_hora_inicial = 15 AND materias_asignadas.Id_hora_final = 17 AND materias_asignadas.Estado = "Activo"',
                4,3,4,5,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 4 AND materias_asignadas.Id_hora_inicial = 15 AND materias_asignadas.Id_hora_final = 18 AND materias_asignadas.Estado = "Activo"',
                4,3,4,6,
                3,self.ninght,self.setStyles6
            )

            # Tercera linea Viernes
            self.celda1x4(
                self.parametrosReportes,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 5 AND materias_asignadas.Id_hora_inicial = 15 AND materias_asignadas.Id_hora_final = 16 AND materias_asignadas.Estado = "Activo"',
                5,3,5,4,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 5 AND materias_asignadas.Id_hora_inicial = 15 AND materias_asignadas.Id_hora_final = 17 AND materias_asignadas.Estado = "Activo"',
                5,3,5,5,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 5 AND materias_asignadas.Id_hora_inicial = 15 AND materias_asignadas.Id_hora_final = 18 AND materias_asignadas.Estado = "Activo"',
                5,3,5,6,
                3,self.ninght,self.setStyles6
            )

            print('Cuarta linea ----------------')
            # Cuarta linea lunes
            self.celda1x3(
                self.parametrosReportes,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 1 AND materias_asignadas.Id_hora_inicial = 16 AND materias_asignadas.Id_hora_final = 17 AND materias_asignadas.Estado = "Activo"',
                1,4,1,5,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 1 AND materias_asignadas.Id_hora_inicial = 16 AND materias_asignadas.Id_hora_final = 18 AND materias_asignadas.Estado = "Activo"',
                1,4,1,6,
                4,self.ninght,self.setStyles6
            )

            # Cuarta linea Martes
            self.celda1x3(
                self.parametrosReportes,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 2 AND materias_asignadas.Id_hora_inicial = 16 AND materias_asignadas.Id_hora_final = 17 AND materias_asignadas.Estado = "Activo"',
                2,4,2,5,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 2 AND materias_asignadas.Id_hora_inicial = 16 AND materias_asignadas.Id_hora_final = 18 AND materias_asignadas.Estado = "Activo"',
                2,4,2,6,
                4,self.ninght,self.setStyles6
            )

            # Cuarta linea Miercoles
            self.celda1x3(
                self.parametrosReportes,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 3 AND materias_asignadas.Id_hora_inicial = 16 AND materias_asignadas.Id_hora_final = 17 AND materias_asignadas.Estado = "Activo"',
                3,4,3,5,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 3 AND materias_asignadas.Id_hora_inicial = 16 AND materias_asignadas.Id_hora_final = 18 AND materias_asignadas.Estado = "Activo"',
                3,4,3,6,
                4,self.ninght,self.setStyles6
            )

            # Cuarta linea Jueves
            self.celda1x3(
                self.parametrosReportes,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 4 AND materias_asignadas.Id_hora_inicial = 16 AND materias_asignadas.Id_hora_final = 17 AND materias_asignadas.Estado = "Activo"',
                4,4,4,5,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 4 AND materias_asignadas.Id_hora_inicial = 16 AND materias_asignadas.Id_hora_final = 18 AND materias_asignadas.Estado = "Activo"',
                4,4,4,6,
                4,self.ninght,self.setStyles6
            )

            # Cuarta linea Viernes
            self.celda1x3(
                self.parametrosReportes,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 5 AND materias_asignadas.Id_hora_inicial = 16 AND materias_asignadas.Id_hora_final = 17 AND materias_asignadas.Estado = "Activo"',
                5,4,5,5,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 5 AND materias_asignadas.Id_hora_inicial = 16 AND materias_asignadas.Id_hora_final = 18 AND materias_asignadas.Estado = "Activo"',
                5,4,5,6,
                4,self.ninght,self.setStyles6
            )

            print('Quinta linea ----------------')
            # Quinta linea lunes
            self.celda1x2(
                self.parametrosReportes,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 1 AND materias_asignadas.Id_hora_inicial = 17 AND materias_asignadas.Id_hora_final = 18 AND materias_asignadas.Estado = "Activo"',
                1,5,1,6,
                5,self.ninght,self.setStyles6
            )

            # Quinta linea Martes
            self.celda1x2(
                self.parametrosReportes,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 2 AND materias_asignadas.Id_hora_inicial = 17 AND materias_asignadas.Id_hora_final = 18 AND materias_asignadas.Estado = "Activo"',
                2,5,2,6,
                5,self.ninght,self.setStyles6
            )

            # Quinta linea Miercoles
            self.celda1x2(
                self.parametrosReportes,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 3 AND materias_asignadas.Id_hora_inicial = 17 AND materias_asignadas.Id_hora_final = 18 AND materias_asignadas.Estado = "Activo"',
                3,5,3,6,
                5,self.ninght,self.setStyles6
            )

            # Quinta linea Jueves
            self.celda1x2(
                self.parametrosReportes,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 4 AND materias_asignadas.Id_hora_inicial = 17 AND materias_asignadas.Id_hora_final = 18 AND materias_asignadas.Estado = "Activo"',
                4,5,4,6,
                5,self.ninght,self.setStyles6
            )

            # Quinta linea Viernes
            self.celda1x2(
                self.parametrosReportes,
                'SELECT unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_semana = 5 AND materias_asignadas.Id_hora_inicial = 17 AND materias_asignadas.Id_hora_final = 18 AND materias_asignadas.Estado = "Activo"',
                5,5,5,6,
                5,self.ninght,self.setStyles6
            )
            
            return self.ninght

    def tablaHorarioAdcrispcion(self):
            self.tableHorarioAdcrispcion = Table(self.obtenerTablaHorarioAdcrispcion(),colWidths=206, rowHeights=17)
            self.tableHorarioAdcrispcion.setStyle(TableStyle(self.setStyles7))
            self.tableHorarioAdcrispcion.wrapOn(self.pdf,self.width,self.heigth)
            if self.counter == 10: 
                self.tableHorarioAdcrispcion.drawOn(self.pdf,10,920)
                print('jefe----10')
            elif self.counter == 9: 
                self.tableHorarioAdcrispcion.drawOn(self.pdf,10,920)
                print('jefe-----9')
            elif self.counter == 8: 
                self.tableHorarioAdcrispcion.drawOn(self.pdf,10,1100)
                print('jefe-----8')
            elif self.counter == 7: 
                self.tableHorarioAdcrispcion.drawOn(self.pdf,10,1100)
                print('jefe-----7')
            elif self.counter == 6: 
                self.tableHorarioAdcrispcion.drawOn(self.pdf,10,1100)
                print('jefe-----6')
            elif self.counter == 5: 
                self.tableHorarioAdcrispcion.drawOn(self.pdf,10,1100)
                print('jefe-----5')
            elif self.counter == 4: 
                self.tableHorarioAdcrispcion.drawOn(self.pdf,10,95)
                print('jefe-----4')
            elif self.counter == 3: 
                self.tableHorarioAdcrispcion.drawOn(self.pdf,10,135)
                print('jefe-----3')
            elif self.counter == 2: 
                self.tableHorarioAdcrispcion.drawOn(self.pdf,10,185)
                print('jefe-----2')
            elif self.counter == 1: 
                self.tableHorarioAdcrispcion.drawOn(self.pdf,10,225)
                print('jefe-----1')
            else:
                self.tableHorarioAdcrispcion.drawOn(self.pdf,10,225)
                print('jefe-----0')
            return self.tableHorarioAdcrispcion

    def obtenerTablaHorarioAdcrispcion(self):
            self.adcrispcion = [
                [Paragraph('Departamento de Adscripción',self.center)],
                [Paragraph('Horario elaborado por:',self.center)]
            ]
            
            self.adcrispcion[0].append('')
            self.setStyles7.append(('SPAN',(0,0),(1,0)))
            self.adcrispcion[0].append(Paragraph(self.entryAdscripcion.get(),self.center))
            self.adcrispcion[0].append('')
            self.setStyles7.append(('SPAN',(2,0),(3,0)))
            self.adcrispcion[1].append(Paragraph(self.entryHorario.get(),self.center))
            self.adcrispcion[1].append(Paragraph('Cargo:',self.center))
            self.adcrispcion[1].append(Paragraph(self.entryCargo.get(),self.center))
            
            return self.adcrispcion

    def tablaHorarioObservacion(self):
            self.tableHorarioObservacion = Table(self.obtenerTablaHorarioObservacion(),colWidths=117, rowHeights=25)
            self.tableHorarioObservacion.setStyle(TableStyle(self.setStyles8))
            self.tableHorarioObservacion.wrapOn(self.pdf,self.width,self.heigth)
            if self.counter == 10: 
                self.tableHorarioObservacion.drawOn(self.pdf,12,850)
                print('observacion----10')
            elif self.counter == 9: 
                self.tableHorarioObservacion.drawOn(self.pdf,12,850)
                print('observacion-----9')
            elif self.counter == 8: 
                self.tableHorarioObservacion.drawOn(self.pdf,12,1030)
                print('observacion-----8')
            elif self.counter == 7: 
                self.tableHorarioObservacion.drawOn(self.pdf,12,1030)
                print('observacion-----7')
            elif self.counter == 6: 
                self.tableHorarioObservacion.drawOn(self.pdf,12,1030)
                print('observacion-----6')
            elif self.counter == 5: 
                self.tableHorarioObservacion.drawOn(self.pdf,12,1030)
                print('observacion-----5')
            elif self.counter == 4: 
                self.tableHorarioObservacion.drawOn(self.pdf,12,30)
                print('observacion-----4')
            elif self.counter == 3: 
                self.tableHorarioObservacion.drawOn(self.pdf,12,70)
                print('observacion-----3')
            elif self.counter == 2: 
                self.tableHorarioObservacion.drawOn(self.pdf,12,110)
                print('observacion-----2')
            elif self.counter == 1: 
                self.tableHorarioObservacion.drawOn(self.pdf,12,150)
                print('observacion-----1')
            else:
                self.tableHorarioObservacion.drawOn(self.pdf,12,150)
                print('observacion-----0')
            return self.tableHorarioObservacion

    def obtenerTablaHorarioObservacion(self):
            self.observacion = [
                [Paragraph('Labora en otra empresa: ',self.center)],
                [Paragraph('Leyenda:',self.center),Paragraph('PNF',self.center),Paragraph('Programa Nacional de Formación',self.center),Paragraph('PT',self.center),Paragraph('Programa Tradicional',self.center),Paragraph('TI',self.center),Paragraph('Trayecto Inicial',self.center)]
            ]
            
            self.labore = self.materia('SELECT docente.Labore from docente WHERE docente.Id = ? AND docente.Estado = "Activo"',(self.docenteId,))
            self.observacion[0].append(Paragraph(self.labore,self.center))
            self.observacion[0].append(Paragraph('Especifique:',self.center))
            self.especifique = self.materia('SELECT docente.Especifique from docente WHERE docente.Id = ? AND docente.Estado = "Activo"',(self.docenteId,))
            self.observacion[0].append(Paragraph(self.especifique,self.center))
            self.setStyles8.append(('SPAN',(3,0),(6,0)))

            return self.observacion