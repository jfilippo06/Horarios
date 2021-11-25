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
        self.geometry('350x470')
        self.resizable(width=0,height=0)
        self.iconbitmap(uptpc)
        
        ttk.Label(self, text='REPORTES DE DOCENTES',font=('Helvetica',14)).place(x=45,y=5)
        
        self.framecontainer2 = ttk.Labelframe(self)
        self.framecontainer2.grid(column=0, row=0,ipadx=5,ipady=5,pady=35,padx=35)
        
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
        
        self.frameAdscripcion = ttk.Labelframe(self.framecontainer2)
        self.frameAdscripcion.grid(column=0,row=2,pady=5,padx=5)
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

    