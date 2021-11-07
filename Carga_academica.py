import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
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

class CargaAcademica(tk.Toplevel):
	def __init__(self,master = None):
		super().__init__(master)
		# Config:
		self.master = master
		self.title('Carga Académica')
		self.geometry('940x620')
		self.resizable(width=0,height=0)
		self.iconbitmap(uptpc)
		# Menu:
		self.menubar = tk.Menu(self)
		self.filemenu1 = tk.Menu(self.menubar, tearoff=0)
		self.filemenu1.add_command(label="Reportes", command=self.reportes)
		self.filemenu1.add_command(label="Información adicional docente", command=self.informacionAdcional)
		self.filemenu1.add_command(label="Volver", command=self.volver)
		self.filemenu1.add_command(label="Salir", command=self.salir)
		self.menubar.add_cascade(label="Opciones", menu=self.filemenu1)
		self.filemenu2 = tk.Menu(self.menubar, tearoff=0)
		self.filemenu2.add_command(label="Manual")
		self.menubar.add_cascade(label="Ayuda", menu=self.filemenu2)
		self.config(menu=self.menubar)
		# Frame:
		self.Frame = ttk.Labelframe(self)
		self.Frame.grid(column=0,row=0,pady=30,padx=10)
		ttk.Label(self, text='CARGA ACADÉMICA',font=('Helvetica',14)).place(x=370,y=5)
		ttk.Label(self.Frame, text='Nombre y Apellido:',font=('Helvetica',11)).grid(column=0,row=0 ,padx=5,pady=5)
		self.EntryNombreApellido = ttk.Entry(self.Frame,width=45)
		self.EntryNombreApellido.grid(column=1,row=0,padx=5,pady=5)
		ttk.Label(self.Frame,text='Cédula de Identidad N°:',font=('Helvetica',11)).grid(column=2,row=0,padx=5)
		self.EntryCedula = ttk.Entry(self.Frame,width=45)
		self.EntryCedula.grid(column=3,row=0,padx=5,pady=5)
		ttk.Label(self.Frame,text='Categoría:',font=('Helvetica',11)).grid(column=0,row=1,padx=5,pady=5)
		self.EntryCategoria = ttk.Entry(self.Frame,width=45)
		self.EntryCategoria.grid(column=1,row=1,padx=5,pady=5)
		ttk.Label(self.Frame, text='Dedicación:',font=('Helvetica',11)).grid(column=2,row=1,padx=5,pady=5)
		self.EntryDedicacion = ttk.Entry(self.Frame,width=45)
		self.EntryDedicacion.grid(column=3,row=1,padx=5,pady=5)
		ttk.Label(self.Frame,text='Título de Pre-Grado:',font=('Helvetica',11)).grid(column=0,row=2,padx=5,pady=5)
		self.EntryTPregado = ttk.Entry(self.Frame,width=45)
		self.EntryTPregado.grid(column=1,row=2,padx=5,pady=5)
		ttk.Label(self.Frame, text='Título de Post-Grado:',font=('Helvetica',11)).grid(column=2,row=2,padx=5,pady=5)
		self.EntryTPosgrado = ttk.Entry(self.Frame,width=45)
		self.EntryTPosgrado.grid(column=3,row=2,padx=5,pady=5)
		ttk.Label(self.Frame, text='Descarga Académica:',font=('Helvetica',11)).grid(column=0,row=3,padx=5,pady=5)
		self.DescargaAcademica = tk.StringVar()
		ttk.Radiobutton(self.Frame, text='Si', value='Si',variable=self.DescargaAcademica).grid(column=1,row=3,padx=5,pady=5)
		ttk.Radiobutton(self.Frame, text='No', value='No',variable=self.DescargaAcademica).grid(column=2,row=3,padx=5,pady=5)
		ttk.Label(self.Frame, text='Condición Laboral:',font=('Helvetica',11)).grid(column=0,row=4,padx=5,pady=5)
		self.CondicionLaboral = tk.StringVar()
		ttk.Radiobutton(self.Frame, text='Ordinario', value='Ordinario',variable=self.CondicionLaboral).grid(column=1,row=4,padx=5,pady=5)
		ttk.Radiobutton(self.Frame, text='Contratado', value='Contratado',variable=self.CondicionLaboral).grid(column=2,row=4,padx=5,pady=5)
		ttk.Label(self.Frame,text='Razón de la descarga:',font=('Helvetica',11)).grid(column=0,row=5,padx=5,pady=5)
		self.EntryRazon = ttk.Entry(self.Frame,width=45)
		self.EntryRazon.grid(column=1,row=5,padx=5,pady=5)
		ttk.Label(self.Frame,text='Numero telefónico:',font=('Helvetica',11)).grid(column=2,row=5,padx=5,pady=5)
		self.EntryTelefono = ttk.Entry(self.Frame,width=45)
		self.EntryTelefono.grid(column=3,row=5,padx=5,pady=5) 
		ttk.Button(self.Frame,text = 'REGISTRAR DOCENTE', command = self.RegistrarDocente).grid(column=0,row=6,sticky = tk.W + tk.E ,padx=5,pady=5)
		ttk.Button(self.Frame,text = 'GESTIONAR MATERIAS', command = self.gestionarMaterias).grid(column=1,row=6,sticky = tk.W + tk.E ,padx=5,pady=5)
		# Treeview:
		self.tree = ttk.Treeview(self, columns = ['#1','#2','#3'], show='headings')
		self.tree.grid(column=0,row=1, sticky='nsew',padx=5)
		self.tree.heading('#1', text = 'Id')
		self.tree.heading('#2', text = 'Nombre y Apellido')
		self.tree.heading('#3', text = 'Cedula')
		
		self.scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
		self.tree.configure(yscroll=self.scrollbar.set)
		self.scrollbar.grid(column=1,row=1, sticky='ns')
		# # Button:
		ttk.Button(self,text = 'EDITAR DOCENTE', command = self.editar).grid(column=0,row=2, sticky = tk.W + tk.E, padx=5)
		ttk.Button(self,text = 'ELIMINAR CODENTE', command =self.eliminar).grid(column=0,row=3,sticky = tk.W + tk.E, padx=5)

		self.MostrarDatos()
		# self.mostarCohorte()

	def volver(self):
		self.destroy()

	def salir(self):
		self.master.destroy()

	def limpiarTabla(self):
		self.DeleteChildren = self.tree.get_children()
		for element in self.DeleteChildren:
			self.tree.delete(element)

	def LimpiarCeldas(self):
		self.EntryNombreApellido.delete(0, tk.END)
		self.EntryCedula.delete(0, tk.END)
		self.EntryCategoria.delete(0, tk.END)
		self.EntryDedicacion.delete(0, tk.END)
		self.EntryTPregado.delete(0, tk.END)
		self.EntryTPosgrado.delete(0, tk.END)
		self.DescargaAcademica.set(0)
		self.CondicionLaboral.set(0)
		self.EntryRazon.delete(0, tk.END)
		self.EntryTelefono.delete(0, tk.END)

	def ValidarCeldas(self):
		return len(self.EntryNombreApellido.get()) != 0 and len(self.EntryCedula.get()) != 0 and len(self.EntryCategoria.get()) != 0 and len(self.EntryDedicacion.get()) != 0 and len(self.EntryTPregado.get()) != 0 and len(self.EntryTPosgrado.get()) != 0 and len(self.DescargaAcademica.get()) != 0 and len(self.CondicionLaboral.get()) != 0 and len(self.EntryRazon.get())  != 0 and len(self.EntryTelefono.get())  != 0       

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

	def MostrarDatos(self):
		self.limpiarTabla()
		self.rows = self.TraerDatos("SELECT Id,NombreApellido,Cedula FROM docente")
		for row in self.rows:
			self.tree.insert('',tk.END,values=row)

	def RegistrarDocente(self):
		if self.ValidarCeldas():
			self.query = 'INSERT INTO docente VALUES (NULL,?,?,?,?,?,?,?,?,?,?)'
			self.parametros = (self.EntryNombreApellido.get(),self.EntryCedula.get(),self.EntryCategoria.get(),self.EntryDedicacion.get(),self.EntryTPregado.get(),self.EntryTPosgrado.get(),self.DescargaAcademica.get(), self.CondicionLaboral.get(), self.EntryRazon.get(), self.EntryTelefono.get())
			if self.conexion(self.query,self.parametros):
				self.MostrarDatos()
				self.LimpiarCeldas()
				messagebox.showinfo(title='Info', message='Docente Registrado.')
			else:
				messagebox.showinfo(title='Info', message='Esta cedula ya esta registrada')
		else:
			messagebox.showwarning(title='Warning', message='Introduzca un valor.')
	
	def selecionarFila(self):
		self.item = self.tree.focus()
		self.data = self.tree.item(self.item)
		self.id = self.data['values'][0]
		return self.id

	def eliminar(self):
		if self.tree.selection():
			if messagebox.askyesno('Delete','¿Desea eliminar al docente selecionado?'):
				self.parametros = self.selecionarFila()
				self.query1 = 'DELETE FROM docente WHERE Id = ?'
				self.query2 = 'DELETE FROM materias_asignadas WHERE materias_asignadas.Id_docente = ?'
				self.query3 = 'DELETE FROM materias_docentes WHERE materias_docentes.Id_docente = ?'
				self.query4 = 'DELETE FROM materias_laboratorios WHERE materias_laboratorios.Id_docente = ?'
				self.conexion(self.query1, (self.parametros,))
				self.conexion(self.query2, (self.parametros,))
				self.conexion(self.query3, (self.parametros,))
				self.conexion(self.query4, (self.parametros,))
				self.MostrarDatos()
				messagebox.showinfo(title='Info', message='Docente eliminado correctamente.')
			else:
				self.MostrarDatos()
		else:
			messagebox.showwarning(title='Wanning', message='Seleccione un docente a eliminar.')

	def editar(self):
		if self.tree.selection():
			if messagebox.askyesno('Edit','¿Desea editar al docente selecionado?'):
				self.seleccion = self.selecionarFila()
				self.new = tk.Toplevel()
				self.new.title('Editar Docente')
				self.new.geometry('400x400')
				self.new.resizable(width=0,height=0)
				self.new.iconbitmap(uptpc)
				self.frame = ttk.Labelframe(self.new)
				self.frame.grid(column=0,row=0,pady=5,padx=5,ipadx=0,ipady=5)
				ttk.Label(self.frame,text='Nombre y Apellido:').grid(row=0,column=0,padx=5,pady=5)
				self.entryEditarNombre = ttk.Entry(self.frame,width=40)
				self.entryEditarNombre.grid(row=0,column=1,pady=5,padx=5)
				ttk.Label(self.frame,text='Cedula:').grid(row=1,column=0,padx=5,pady=5)
				self.entryEditarCedula = ttk.Entry(self.frame, width=40)
				self.entryEditarCedula.grid(row=1,column=1,padx=5,pady=5)
				ttk.Label(self.frame,text='Categoria:').grid(row=2,column=0,padx=5,pady=5)
				self.entryEditarCategoria = ttk.Entry(self.frame, width=40)
				self.entryEditarCategoria.grid(row=2,column=1,padx=5,pady=5)
				ttk.Label(self.frame,text='Dedicación:').grid(row=3,column=0,padx=5,pady=5)
				self.entryEditarDedicación = ttk.Entry(self.frame, width=40)
				self.entryEditarDedicación.grid(row=3,column=1,padx=5,pady=5)
				ttk.Label(self.frame,text='Titulo de Pre-grado:').grid(row=4,column=0,padx=5,pady=5)
				self.entryEditarTpregado = ttk.Entry(self.frame, width=40)
				self.entryEditarTpregado.grid(row=4,column=1,padx=5,pady=5)
				ttk.Label(self.frame,text='Titulo de Posgrado:').grid(row=5,column=0,padx=5,pady=5)
				self.entryEditarTposgrado = ttk.Entry(self.frame, width=40)
				self.entryEditarTposgrado.grid(row=5,column=1,padx=5,pady=5)
				self.DescargaAcademicaEditar = tk.StringVar()
				ttk.Label(self.frame,text='Descarga Academica').grid(row=6,column=0)
				ttk.Radiobutton(self.frame, text='Si', value='Si',variable=self.DescargaAcademicaEditar).grid(row=7,column=0)
				ttk.Radiobutton(self.frame, text='No', value='No',variable=self.DescargaAcademicaEditar).grid(row=7,column=1)
				self.CondicionLaboralEditar = tk.StringVar()
				ttk.Label(self.frame, text='Condición Laboral:').grid(row=8,column=0)
				ttk.Radiobutton(self.frame, text='Ordinario', value='Ordinario',variable=self.CondicionLaboralEditar).grid(row=9,column=0)
				ttk.Radiobutton(self.frame, text='Contratado', value='Contratado',variable=self.CondicionLaboralEditar).grid(row=9,column=1)
				ttk.Label(self.frame,text='Razon de la descarga:').grid(row=10,column=0,padx=5,pady=5)
				self.entryEditarRazon = ttk.Entry(self.frame,width=40)
				self.entryEditarRazon.grid(row=10,column=1,padx=5,pady=5)
				ttk.Label(self.frame,text='Numero telefónico:').grid(row=11,column=0,padx=5,pady=5)
				self.entryEditarTelefono = ttk.Entry(self.frame,width=40)
				self.entryEditarTelefono.grid(row=11,column=1,padx=5,pady=5)
				ttk.Button(self.new,text='Editar', command=self.botonEditar).grid(row=1,column=0,pady=5,padx=5)				
				self.new.mainloop()		
			else:
				self.MostrarDatos()		
		else: 
			messagebox.showwarning(title='Wanning', message='Seleccione un docente a editar.')
	

	def validarCeldasEditar(self):
		return len(self.entryEditarNombre.get()) != 0 and len(self.entryEditarCedula.get()) != 0 and len(self.entryEditarCategoria.get()) != 0 and len(self.entryEditarDedicación.get()) != 0 and len(self.entryEditarTpregado.get()) != 0 and  len(self.entryEditarTposgrado.get()) != 0 and len(self.DescargaAcademicaEditar.get()) != 0 and  len(self.CondicionLaboralEditar.get()) != 0 and  len(self.entryEditarRazon.get()) != 0 and len(self.entryEditarTelefono.get()) != 0
	
	def LimpiarCeldasEditar(self):
		self.entryEditarNombre.delete(0, tk.END)
		self.entryEditarCedula.delete(0, tk.END)
		self.entryEditarCategoria.delete(0, tk.END)
		self.entryEditarDedicación.delete(0, tk.END)
		self.entryEditarTpregado.delete(0, tk.END)
		self.entryEditarTposgrado.delete(0, tk.END)
		self.DescargaAcademicaEditar.set(0)
		self.CondicionLaboralEditar.set(0)
		self.entryEditarRazon.delete(0, tk.END)
		self.entryEditarTelefono.delete(0,tk.END)

	def botonEditar(self):
		if self.validarCeldasEditar():
			self.query1 = 'UPDATE docente SET NombreApellido = ? WHERE id = ?'
			self.query2 = 'UPDATE docente SET Cedula = ? WHERE id = ?'
			self.query3 = 'UPDATE docente SET Categoria = ? WHERE id = ?'
			self.query4 = 'UPDATE docente SET Dedicacion = ? WHERE id = ?'
			self.query5 = 'UPDATE docente SET Pregrado = ? WHERE id = ?'
			self.query6 = 'UPDATE docente SET Postgrado = ? WHERE id = ?'
			self.query7 = 'UPDATE docente SET DescargaAcademica = ? WHERE id = ?'
			self.query8 = 'UPDATE docente SET CondicionLaboral = ? WHERE id = ?'
			self.query9 = 'UPDATE docente SET RazonDescarga = ? WHERE id = ?'
			self.query10 = 'UPDATE docente SET Telefono = ? WHERE id = ?'
			self.id = self.seleccion
			self.conexion(self.query1,(self.entryEditarNombre.get(), self.id))
			self.conexion(self.query2,(self.entryEditarCedula.get(), self.id))
			self.conexion(self.query3,(self.entryEditarCategoria.get(), self.id))
			self.conexion(self.query4,(self.entryEditarDedicación.get(), self.id))
			self.conexion(self.query5,(self.entryEditarTpregado.get(), self.id))
			self.conexion(self.query6,(self.entryEditarTposgrado.get(), self.id))
			self.conexion(self.query7,(self.DescargaAcademicaEditar.get(), self.id))
			self.conexion(self.query8,(self.CondicionLaboralEditar.get(), self.id))
			self.conexion(self.query9,(self.entryEditarRazon.get(), self.id))
			self.conexion(self.query10,(self.entryEditarTelefono.get(), self.id))
			self.LimpiarCeldasEditar()
			self.LimpiarCeldas()
			self.new.destroy()
			self.MostrarDatos()
			messagebox.showinfo(title='Info', message='Docente Editado Correctamente.')
		else:
			messagebox.showinfo(title='info', message='Introduzca un valor en las celdas')

	def gestionarMaterias(self):
		if self.tree.selection():
			self.lower()
			self.seleccion = self.selecionarFila()
			self.MostrarDatos()
			self.new = tk.Toplevel()
			self.new.title('Gestionar Materias')
			self.new.attributes("-fullscreen", False)
			self.w, self.h = self.new.winfo_screenwidth(), self.new.winfo_screenheight()
			self.new.geometry("%dx%d" % (self.w, self.h))
			self.new.iconbitmap(uptpc)

			ttk.Label(self.new, text='AÑADIR MATERIAS',font=('Helvetica',14)).place(x=550,y=5)
			self.container = ttk.Labelframe(self.new)
			self.container.grid(column=0,row=0,ipady=5,ipadx=0,pady=30)

			self.frameLapsoAcademico = ttk.Labelframe(self.container)
			self.frameLapsoAcademico.grid(column=0,row=0,pady=0,padx=5)
			self.treeLapsoAcademico = ttk.Treeview(self.frameLapsoAcademico, columns=['#1',"#2"],show='headings',height=3)
			self.treeLapsoAcademico.grid(row=0,column=0)
			self.treeLapsoAcademico.heading('#1', text = 'Id',)
			self.treeLapsoAcademico.heading('#2', text = 'Lapso Académico')
			self.treeLapsoAcademico.column('#1', width=50)
			self.treeLapsoAcademico.column('#2', width=120)
			self.scrollbarLapsoAcademico = ttk.Scrollbar(self.frameLapsoAcademico, orient=tk.VERTICAL, command=self.treeLapsoAcademico.yview)
			self.treeLapsoAcademico.configure(yscroll=self.scrollbarLapsoAcademico.set)
			self.scrollbarLapsoAcademico.grid(column=1,row=0, sticky='ns')

			self.frameCohorte = ttk.Labelframe(self.container)
			self.frameCohorte.grid(column=1,row=0,pady=0,padx=5)
			self.treeCohorte = ttk.Treeview(self.frameCohorte, columns=['#1',"#2"],show='headings',height=3)
			self.treeCohorte.grid(row=0,column=0)
			self.treeCohorte.heading('#1', text = 'Id',)
			self.treeCohorte.heading('#2', text = 'Cohorte')
			self.treeCohorte.column('#1', width=50)
			self.treeCohorte.column('#2', width=120)
			self.scrollbarCohorte = ttk.Scrollbar(self.frameCohorte, orient=tk.VERTICAL, command=self.treeCohorte.yview)
			self.treeCohorte.configure(yscroll=self.scrollbarCohorte.set)
			self.scrollbarCohorte.grid(column=1,row=0, sticky='ns')

			self.frameTrayecto = ttk.Labelframe(self.container)
			self.frameTrayecto.grid(column=2,row=0,pady=0,padx=5)
			self.treeTrayecto = ttk.Treeview(self.frameTrayecto, columns=['#1',"#2"],show='headings',height=3)
			self.treeTrayecto.grid(row=0,column=0)
			self.treeTrayecto.heading('#1', text = 'Id',)
			self.treeTrayecto.heading('#2', text = 'Trayecto')
			self.treeTrayecto.column('#1', width=50)
			self.treeTrayecto.column('#2', width=120)
			self.scrollbarTrayecto = ttk.Scrollbar(self.frameTrayecto, orient=tk.VERTICAL, command=self.treeTrayecto.yview)
			self.treeTrayecto.configure(yscroll=self.scrollbarTrayecto.set)
			self.scrollbarTrayecto.grid(column=1,row=0, sticky='ns')

			self.frameTrimestre = ttk.Labelframe(self.container)
			self.frameTrimestre.grid(column=3,row=0,pady=0,padx=5)
			self.treeTrimestre = ttk.Treeview(self.frameTrimestre, columns=['#1',"#2"],show='headings',height=3)
			self.treeTrimestre.grid(row=0,column=0)
			self.treeTrimestre.heading('#1', text = 'Id',)
			self.treeTrimestre.heading('#2', text = 'Trimestre')
			self.treeTrimestre.column('#1', width=50)
			self.treeTrimestre.column('#2', width=120)
			self.scrollbarTrimestre = ttk.Scrollbar(self.frameTrimestre, orient=tk.VERTICAL, command=self.treeTrimestre.yview)
			self.treeTrimestre.configure(yscroll=self.scrollbarTrimestre.set)
			self.scrollbarTrimestre.grid(column=1,row=0, sticky='ns')

			self.frameSeccion = ttk.Labelframe(self.container)
			self.frameSeccion.grid(column=4,row=0,pady=0,padx=5)
			self.treeSeccion = ttk.Treeview(self.frameSeccion, columns=['#1',"#2"],show='headings',height=3)
			self.treeSeccion.grid(row=0,column=0)
			self.treeSeccion.heading('#1', text = 'Id',)
			self.treeSeccion.heading('#2', text = 'Sección')
			self.treeSeccion.column('#1', width=50)
			self.treeSeccion.column('#2', width=120)
			self.scrollbarSeccion = ttk.Scrollbar(self.frameSeccion, orient=tk.VERTICAL, command=self.treeSeccion.yview)
			self.treeSeccion.configure(yscroll=self.scrollbarSeccion.set)
			self.scrollbarSeccion.grid(column=1,row=0, sticky='ns')

			self.frameTurno = ttk.Labelframe(self.container)
			self.frameTurno.grid(column=0,row=1,pady=0,padx=5)
			self.treeTurno = ttk.Treeview(self.frameTurno, columns=['#1',"#2"],show='headings',height=3)
			self.treeTurno.grid(row=0,column=0)
			self.treeTurno.heading('#1', text = 'Id',)
			self.treeTurno.heading('#2', text = 'Turno')
			self.treeTurno.column('#1', width=50)
			self.treeTurno.column('#2', width=120)
			self.scrollbarTurno = ttk.Scrollbar(self.frameTurno, orient=tk.VERTICAL, command=self.treeTurno.yview)
			self.treeTurno.configure(yscroll=self.scrollbarTurno.set)
			self.scrollbarTurno.grid(column=1,row=0, sticky='ns')

			self.frameDia = ttk.Labelframe(self.container)
			self.frameDia.grid(column=1,row=1,pady=0,padx=5)
			self.treeDia = ttk.Treeview(self.frameDia, columns=['#1',"#2"],show='headings',height=3)
			self.treeDia.grid(row=0,column=0)
			self.treeDia.heading('#1', text = 'Id',)
			self.treeDia.heading('#2', text = 'Día')
			self.treeDia.column('#1', width=50)
			self.treeDia.column('#2', width=120)
			self.scrollbarDia = ttk.Scrollbar(self.frameDia, orient=tk.VERTICAL, command=self.treeDia.yview)
			self.treeDia.configure(yscroll=self.scrollbarDia.set)
			self.scrollbarDia.grid(column=1,row=0, sticky='ns')

			self.frameHoraInicial = ttk.Labelframe(self.container)
			self.frameHoraInicial.grid(column=2,row=1,pady=0,padx=5)
			self.treeHoraInicial = ttk.Treeview(self.frameHoraInicial, columns=['#1',"#2"],show='headings',height=3)
			self.treeHoraInicial.grid(row=0,column=0)
			self.treeHoraInicial.heading('#1', text = 'Id',)
			self.treeHoraInicial.heading('#2', text = 'Hora Inicial')
			self.treeHoraInicial.column('#1', width=50)
			self.treeHoraInicial.column('#2', width=120)
			self.scrollbarHoraInicial = ttk.Scrollbar(self.frameHoraInicial, orient=tk.VERTICAL, command=self.treeHoraInicial.yview)
			self.treeHoraInicial.configure(yscroll=self.scrollbarHoraInicial.set)
			self.scrollbarHoraInicial.grid(column=1,row=0, sticky='ns')

			self.frameHoraFinal = ttk.Labelframe(self.container)
			self.frameHoraFinal.grid(column=3,row=1,pady=0,padx=5)
			self.treeHoraFinal = ttk.Treeview(self.frameHoraFinal, columns=['#1',"#2"],show='headings',height=3)
			self.treeHoraFinal.grid(row=0,column=0)
			self.treeHoraFinal.heading('#1', text = 'Id',)
			self.treeHoraFinal.heading('#2', text = 'Hora final')
			self.treeHoraFinal.column('#1', width=50)
			self.treeHoraFinal.column('#2', width=120)
			self.scrollbarHoraFinal = ttk.Scrollbar(self.frameHoraFinal, orient=tk.VERTICAL, command=self.treeHoraFinal.yview)
			self.treeHoraFinal.configure(yscroll=self.scrollbarHoraFinal.set)
			self.scrollbarHoraFinal.grid(column=1,row=0, sticky='ns')

			self.frameUnidadCurricular = ttk.Labelframe(self.container)
			self.frameUnidadCurricular.grid(column=4,row=1,pady=0,padx=5)
			self.treeUnidadCurricular = ttk.Treeview(self.frameUnidadCurricular, columns=['#1',"#2"],show='headings',height=3)
			self.treeUnidadCurricular.grid(row=0,column=0)
			self.treeUnidadCurricular.heading('#1', text = 'Id',)
			self.treeUnidadCurricular.heading('#2', text = 'Unidad Curricular')
			self.treeUnidadCurricular.column('#1', width=50)
			self.treeUnidadCurricular.column('#2', width=250)
			self.scrollbarUnidadCurricular = ttk.Scrollbar(self.frameUnidadCurricular, orient=tk.VERTICAL, command=self.treeUnidadCurricular.yview)
			self.treeUnidadCurricular.configure(yscroll=self.scrollbarUnidadCurricular.set)
			self.scrollbarUnidadCurricular.grid(column=1,row=0, sticky='ns')

			self.frameLaboratorio = ttk.Labelframe(self.container)
			self.frameLaboratorio.grid(column=0,row=3,pady=0,padx=5)
			self.treeLaboratorio = ttk.Treeview(self.frameLaboratorio, columns=['#1',"#2"],show='headings',height=3)
			self.treeLaboratorio.grid(row=0,column=0)
			self.treeLaboratorio.heading('#1', text = 'Id',)
			self.treeLaboratorio.heading('#2', text = 'Laboratorio')
			self.treeLaboratorio.column('#1', width=50)
			self.treeLaboratorio.column('#2', width=120)
			self.scrollbarLaboratorio = ttk.Scrollbar(self.frameLaboratorio, orient=tk.VERTICAL, command=self.treeLaboratorio.yview)
			self.treeLaboratorio.configure(yscroll=self.scrollbarLaboratorio.set)
			self.scrollbarLaboratorio.grid(column=1,row=0, sticky='ns')
   
			self.frameCheckButton = ttk.Labelframe(self.container)
			self.frameCheckButton.grid(column=1,row=3,ipadx=5,ipady=5)
			ttk.Label(self.frameCheckButton,text='LABORATORIO').grid(column=0,row=0)
			self.laboratorio = tk.StringVar()
			ttk.Radiobutton(self.frameCheckButton, text='Si', value='Si',variable=self.laboratorio).grid(column=0,row=1)
			ttk.Radiobutton(self.frameCheckButton, text='No', value='No',variable=self.laboratorio).grid(column=1,row=1)
   

			ttk.Button(self.new, text='REGISTRAR MATERIA', command=self.registrarMateria).grid(row=1,column=0)

			self.frameGestionar = ttk.Labelframe(self.new)
			self.frameGestionar.grid(column=0,row=2,pady=0,padx=10)
			self.treeGestionar = ttk.Treeview(self.frameGestionar, columns = ['#1','#2','#3','#4','#5','#6','#7','#8','#9','#10','#11','#12'], show='headings',height=9)
			self.treeGestionar.grid(row=0,column=0,padx=0,pady=10)
			self.treeGestionar.heading('#1', text = 'Id',)
			self.treeGestionar.heading('#2', text = 'Nombre y Apellido')
			self.treeGestionar.heading('#3', text = 'Lapso Académico')
			self.treeGestionar.heading('#4', text = 'Cohorte')
			self.treeGestionar.heading('#5', text = 'Trayecto')
			self.treeGestionar.heading('#6', text = 'Trimestre')
			self.treeGestionar.heading('#7', text = 'Sección')
			self.treeGestionar.heading('#8', text = 'Turno')
			self.treeGestionar.heading('#9', text = 'Día')
			self.treeGestionar.heading('#10', text = 'Hora Inicial')
			self.treeGestionar.heading('#11', text = 'Hora Final')
			self.treeGestionar.heading('#12', text = 'Unidad Curricular')
			self.treeGestionar.column('#1', width=40)
			self.treeGestionar.column('#2', width=120)
			self.treeGestionar.column('#3', width=120)
			self.treeGestionar.column('#4', width=100)
			self.treeGestionar.column('#5', width=80)
			self.treeGestionar.column('#6', width=80)
			self.treeGestionar.column('#7', width=80)
			self.treeGestionar.column('#8', width=80)
			self.treeGestionar.column('#9', width=80)
			self.treeGestionar.column('#10', width=100)
			self.treeGestionar.column('#11', width=100)
			self.treeGestionar.column('#12', width=250)
			self.scrollbarGestionar = ttk.Scrollbar(self.frameGestionar, orient=tk.VERTICAL, command=self.treeGestionar.yview)
			self.treeGestionar.configure(yscroll=self.scrollbarGestionar.set)
			self.scrollbarGestionar.grid(column=1,row=0, sticky='ns')

			ttk.Button(self.frameGestionar, text='EDITAR MATERIA', command=self.editarMateria).grid(row=1,column=0,sticky = tk.W + tk.E)
			ttk.Button(self.frameGestionar, text='ELIMINAR MATERIA', command=self.eliminarMateria).grid(row=2,column=0,sticky = tk.W + tk.E)
			
			self.MostrarDatosGestionar()
			self.MostrarLapsoAcademico()
			self.MostrarCohorte()
			self.MostrarTrayecto()
			self.MostrarTrimestre()
			self.MostrarSeccion()
			self.MostrarTurno()
			self.MostrarDia()
			self.MostrarHoraInicial()
			self.MostrarHoraFinal()
			self.MostrarUnidadCurricular()
			self.MostrarLaboratorio()
			
			self.new.mainloop()
		else:
			messagebox.showinfo(title='Info', message='Selecione un docente')

	def limpiarTablaGestionar(self):
		self.DeleteChildren = self.treeGestionar.get_children()
		for element in self.DeleteChildren:
			self.treeGestionar.delete(element)

	def limpiarTablaLapsoAcademico(self):
		self.DeleteChildren = self.treeLapsoAcademico.get_children()
		for element in self.DeleteChildren:
			self.treeLapsoAcademico.delete(element)

	def limpiarTablaCohorte(self):
		self.DeleteChildren = self.treeCohorte.get_children()
		for element in self.DeleteChildren:
			self.treeCohorte.delete(element)

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

	def limpiarTablaTurno(self):
		self.DeleteChildren = self.treeTurno.get_children()
		for element in self.DeleteChildren:
			self.treeTurno.delete(element)

	def limpiarTablaDia(self):
		self.DeleteChildren = self.treeDia.get_children()
		for element in self.DeleteChildren:
			self.treeDia.delete(element)

	def limpiarTablaHoraInicial(self):
		self.DeleteChildren = self.treeHoraInicial.get_children()
		for element in self.DeleteChildren:
			self.treeHoraInicial.delete(element)

	def limpiarTablaHoraFinal(self):
		self.DeleteChildren = self.treeHoraFinal.get_children()
		for element in self.DeleteChildren:
			self.treeHoraFinal.delete(element)

	def limpiarTablaUnidadCurricular(self):
		self.DeleteChildren = self.treeUnidadCurricular.get_children()
		for element in self.DeleteChildren:
			self.treeUnidadCurricular.delete(element)

	def limpiarTablaLaboratorio(self):
		self.DeleteChildren = self.treeLaboratorio.get_children()
		for element in self.DeleteChildren:
			self.treeLaboratorio.delete(element)

	def MostrarDatosGestionar(self):
		self.limpiarTablaGestionar()
		self.query = ("SELECT materias_asignadas.Id ,docente.NombreApellido, lapso_academico.LapsoAcademico, cohorte.Cohorte, trayecto.Trayecto, trimestre.Trimestre, seccion.Seccion, modalidad.Turno,semana.Dia, hora_inicial.Hora, hora_final.Hora, unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN docente ON  docente.Id = materias_asignadas.Id_docente INNER JOIN lapso_academico ON  lapso_academico.Id = materias_asignadas.Id_lapso_academico INNER JOIN cohorte ON  cohorte.Id = materias_asignadas.Id_cohorte INNER JOIN trayecto ON trayecto.Id = materias_asignadas.Id_trayecto INNER JOIN trimestre ON trimestre.Id = materias_asignadas.Id_trimestre INNER JOIN seccion ON seccion.Id = materias_asignadas.Id_seccion INNER JOIN modalidad ON modalidad.Id = materias_asignadas.Id_modalidad INNER JOIN semana ON semana.Id = materias_asignadas.Id_semana INNER JOIN hora_inicial ON hora_inicial.Id = materias_asignadas.Id_hora_inicial INNER JOIN hora_final ON hora_final.Id = materias_asignadas.Id_hora_final INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ?")
		self.parametros = self.seleccion
		self.mostrar =  self.conexion(self.query, (self.parametros,))
		self.rows = self.mostrar.fetchall()
		for row in self.rows:
			self.treeGestionar.insert('',tk.END,values=row)

	def MostrarLapsoAcademico(self):
		self.limpiarTablaLapsoAcademico()
		self.rows = self.TraerDatos("SELECT * FROM lapso_academico")
		for row in self.rows:
			self.treeLapsoAcademico.insert('',tk.END,values=row)
	
	def MostrarCohorte(self):
		self.limpiarTablaCohorte()
		self.rows = self.TraerDatos("SELECT * FROM cohorte")
		for row in self.rows:
			self.treeCohorte.insert('',tk.END,values=row)

	def MostrarTrayecto(self):
		self.limpiarTablaTrayecto()
		self.rows = self.TraerDatos("SELECT * FROM trayecto")
		for row in self.rows:
			self.treeTrayecto.insert('',tk.END,values=row)

	def MostrarTrimestre(self):
		self.limpiarTablaTrimestre()
		self.rows = self.TraerDatos("SELECT * FROM trimestre")
		for row in self.rows:
			self.treeTrimestre.insert('',tk.END,values=row)

	def MostrarSeccion(self):
		self.limpiarTablaSeccion()
		self.rows = self.TraerDatos("SELECT * FROM seccion")
		for row in self.rows:
			self.treeSeccion.insert('',tk.END,values=row)

	def MostrarTurno(self):
		self.limpiarTablaTurno()
		self.rows = self.TraerDatos("SELECT * FROM modalidad")
		for row in self.rows:
			self.treeTurno.insert('',tk.END,values=row)

	def MostrarDia(self):
		self.limpiarTablaDia()
		self.rows = self.TraerDatos("SELECT * FROM semana")
		for row in self.rows:
			self.treeDia.insert('',tk.END,values=row)

	def MostrarHoraInicial(self):
		self.limpiarTablaHoraInicial()
		self.rows = self.TraerDatos("SELECT * FROM hora_inicial")
		for row in self.rows:
			self.treeHoraInicial.insert('',tk.END,values=row)

	def MostrarHoraFinal(self):
		self.limpiarTablaHoraFinal()
		self.rows = self.TraerDatos("SELECT * FROM hora_final")
		for row in self.rows:
			self.treeHoraFinal.insert('',tk.END,values=row)

	def MostrarUnidadCurricular(self):
		self.limpiarTablaUnidadCurricular()
		self.rows = self.TraerDatos("SELECT Id,UnidadCurricular COLLATE utf8_spanish2_ci FROM unidad_curricular ORDER BY UnidadCurricular")
		for row in self.rows:
			self.treeUnidadCurricular.insert('',tk.END,values=row)

	def MostrarLaboratorio(self):
		self.limpiarTablaLaboratorio()
		self.rows = self.TraerDatos("SELECT * FROM laboratorio")
		for row in self.rows:
			self.treeLaboratorio.insert('',tk.END,values=row)

	def registrarMateria(self):
		if self.treeLapsoAcademico.selection() and self.treeCohorte.selection() and self.treeTrayecto.selection() and self.treeTrimestre.selection() and self.treeSeccion.selection() and self.treeTurno.selection() and self.treeDia.selection and self.treeHoraInicial.selection() and self.treeHoraFinal.selection() and self.treeUnidadCurricular.selection():
			if messagebox.askyesno('Registrar','¿Añadir selección?'):
				self.parametros = (self.seleccion,self.selecionarFilaLapsoAcademico(),self.selecionarFilaCohorte(),self.selecionarFilaTrayecto(),self.selecionarFilaTrimestre(),self.selecionarFilaSeccion(),self.selecionarFilaTurno(),self.selecionarFilaDia(),self.selecionarFilaHoraInicial(),self.selecionarFilaHoraFinal(),self.selecionarFilaUnidadCurricular())
				self.queryValidar = ("SELECT materias_asignadas.Id ,docente.NombreApellido, lapso_academico.LapsoAcademico,cohorte.Cohorte, trayecto.Trayecto, trimestre.Trimestre, seccion.Seccion, modalidad.Turno, semana.Dia, hora_inicial.Hora, hora_final.Hora, unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN docente ON  docente.Id = materias_asignadas.Id_docente  INNER JOIN lapso_academico ON  lapso_academico.Id = materias_asignadas.Id_lapso_academico INNER JOIN cohorte ON  cohorte.Id = materias_asignadas.Id_cohorte INNER JOIN trayecto ON trayecto.Id = materias_asignadas.Id_trayecto INNER JOIN trimestre ON trimestre.Id = materias_asignadas.Id_trimestre INNER JOIN seccion ON seccion.Id = materias_asignadas.Id_seccion INNER JOIN modalidad ON modalidad.Id = materias_asignadas.Id_modalidad INNER JOIN semana ON semana.Id = materias_asignadas.Id_semana INNER JOIN hora_inicial ON hora_inicial.Id = materias_asignadas.Id_hora_inicial INNER JOIN hora_final ON hora_final.Id = materias_asignadas.Id_hora_final INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_semana = ? AND materias_asignadas.Id_hora_inicial = ? AND materias_asignadas.Id_hora_final = ? AND materias_asignadas.Id_unidad_curricular = ?")
				self.mostrar =  self.conexion(self.queryValidar,self.parametros)
				if self.mostrar.fetchall():
					messagebox.showwarning(title='warning', message="Registro ya exixte")	
				else:
					self.same = self.conexion(
						'SELECT lapso_academico.LapsoAcademico, cohorte.Cohorte, trayecto.Trayecto, trimestre.Trimestre, seccion.Seccion, modalidad.Turno, semana.Dia, hora_inicial.Hora, hora_final.Hora, unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN lapso_academico ON  lapso_academico.Id = materias_asignadas.Id_lapso_academico INNER JOIN cohorte ON  cohorte.Id = materias_asignadas.Id_cohorte INNER JOIN trayecto ON trayecto.Id = materias_asignadas.Id_trayecto INNER JOIN trimestre ON trimestre.Id = materias_asignadas.Id_trimestre INNER JOIN seccion ON seccion.Id = materias_asignadas.Id_seccion INNER JOIN modalidad ON modalidad.Id = materias_asignadas.Id_modalidad INNER JOIN semana ON semana.Id = materias_asignadas.Id_semana INNER JOIN hora_inicial ON hora_inicial.Id = materias_asignadas.Id_hora_inicial INNER JOIN hora_final ON hora_final.Id = materias_asignadas.Id_hora_final INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_semana = ? AND materias_asignadas.Id_hora_inicial = ? AND materias_asignadas.Id_hora_final = ? AND materias_asignadas.Id_unidad_curricular = ?',
					(self.selecionarFilaLapsoAcademico(),self.selecionarFilaCohorte(),self.selecionarFilaTrayecto(),self.selecionarFilaTrimestre(),self.selecionarFilaSeccion(),self.selecionarFilaTurno(),self.selecionarFilaDia(),self.selecionarFilaHoraInicial(),self.selecionarFilaHoraFinal(),self.selecionarFilaUnidadCurricular())
					).fetchall()
					if self.same:
						messagebox.showwarning(title='warning', message="Este registro ya le pertenece a otro docente")	
					else:
						if self.laboratorio.get() == 'Si':
							if self.treeLaboratorio.selection():
								self.parametros = (self.seleccion,self.selecionarFilaLapsoAcademico(),self.selecionarFilaCohorte(),self.selecionarFilaTrayecto(),self.selecionarFilaTrimestre(),self.selecionarFilaSeccion(),self.selecionarFilaTurno(),self.selecionarFilaDia(),self.selecionarFilaHoraInicial(),self.selecionarFilaHoraFinal(),self.selecionarFilaUnidadCurricular())
								self.query = ("INSERT INTO materias_asignadas VALUES (NULL,?,?,?,?,?,?,?,?,?,?,?)")
								self.conexion(self.query,self.parametros)
				
								self.data = self.conexion(
								'SELECT Id FROM materias_asignadas WHERE  materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_semana = ? AND  materias_asignadas.Id_hora_inicial = ? AND materias_asignadas.Id_hora_final = ? AND materias_asignadas.Id_unidad_curricular = ?',
								self.parametros).fetchone()
								self.id_materias_asignadas = self.data[0]
								
								self.materiaDocente = ('Cohorte ' + str(self.dataCohorte()) + ' Trayecto ' + str(self.dataTrayecto()) + ' Trimestre ' + str(self.dataTrimestre()) + ' Sección ' + str(self.dataSeccion()) + ' ' + str(self.dataUnidadCurricular()))
								self.query1 = ("INSERT INTO materias_docentes VALUES (NULL,?,?,?,?,?,?,?,?)")
								self.conexion(self.query1,(self.id_materias_asignadas,self.seleccion,self.selecionarFilaLapsoAcademico(),self.selecionarFilaTurno(),self.materiaDocente,self.selecionarFilaDia(),self.selecionarFilaHoraInicial(),self.selecionarFilaHoraFinal()))

								self.query2 = ('INSERT INTO materias_laboratorios VALUES (NULL,?,?,?,?,?,?,?,?,?)')
								self.conexion(self.query2,(self.id_materias_asignadas,self.seleccion,self.selecionarFilaLaboratorio(),self.selecionarFilaLapsoAcademico(),self.selecionarFilaTurno(),self.materiaDocente,self.selecionarFilaDia(),self.selecionarFilaHoraInicial(),self.selecionarFilaHoraFinal()))
		
								self.MostrarDatosGestionar()
								messagebox.showinfo(title='info', message='Materia registrada  SI')
							else:
								messagebox.showwarning(title='Warning', message='Seleccione un laboratorio')
						elif self.laboratorio.get() == 'No':
							self.parametros = (self.seleccion,self.selecionarFilaLapsoAcademico(),self.selecionarFilaCohorte(),self.selecionarFilaTrayecto(),self.selecionarFilaTrimestre(),self.selecionarFilaSeccion(),self.selecionarFilaTurno(),self.selecionarFilaDia(),self.selecionarFilaHoraInicial(),self.selecionarFilaHoraFinal(),self.selecionarFilaUnidadCurricular())
							self.query = ("INSERT INTO materias_asignadas VALUES (NULL,?,?,?,?,?,?,?,?,?,?,?)")
							self.conexion(self.query,self.parametros)
			
							self.data = self.conexion(
							'SELECT Id FROM materias_asignadas WHERE  materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_semana = ? AND  materias_asignadas.Id_hora_inicial = ? AND materias_asignadas.Id_hora_final = ? AND materias_asignadas.Id_unidad_curricular = ?',
							self.parametros).fetchone()
							self.id_materias_asignadas = self.data[0]
							
							self.materiaDocente = ('Cohorte ' + str(self.dataCohorte()) + ' Trayecto ' + str(self.dataTrayecto()) + ' Trimestre ' + str(self.dataTrimestre()) + ' Sección ' + str(self.dataSeccion()) + ' ' + str(self.dataUnidadCurricular()))
							self.query1 = ("INSERT INTO materias_docentes VALUES (NULL,?,?,?,?,?,?,?,?)")
							self.conexion(self.query1,(self.id_materias_asignadas,self.seleccion,self.selecionarFilaLapsoAcademico(),self.selecionarFilaTurno(),self.materiaDocente,self.selecionarFilaDia(),self.selecionarFilaHoraInicial(),self.selecionarFilaHoraFinal()))
							
							self.MostrarDatosGestionar()
							messagebox.showinfo(title='info', message='Materia registrada correctamente NO')
						else:
							messagebox.showwarning(title='Warning', message='Debe seleccionar una opción entre las casillas de "Laboratorio"')
			else:
				self.MostrarDatosGestionar()
		else:
			messagebox.showwarning(title='Warning', message='Seleccione todas las celdas')

	def selecionarFilaLapsoAcademico(self):
		self.item = self.treeLapsoAcademico.focus()
		self.data = self.treeLapsoAcademico.item(self.item)
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

	def selecionarFilaTurno(self):
		self.item = self.treeTurno.focus()
		self.data = self.treeTurno.item(self.item)
		self.id = self.data['values'][0]
		return self.id

	def selecionarFilaDia(self):
		self.item = self.treeDia.focus()
		self.data = self.treeDia.item(self.item)
		self.id = self.data['values'][0]
		return self.id

	def selecionarFilaHoraInicial(self):
		self.item = self.treeHoraInicial.focus()
		self.data = self.treeHoraInicial.item(self.item)
		self.id = self.data['values'][0]
		return self.id

	def selecionarFilaHoraFinal(self):
		self.item = self.treeHoraFinal.focus()
		self.data = self.treeHoraFinal.item(self.item)
		self.id = self.data['values'][0]
		return self.id

	def selecionarFilaUnidadCurricular(self):
		self.item = self.treeUnidadCurricular.focus()
		self.data = self.treeUnidadCurricular.item(self.item)
		self.id = self.data['values'][0]
		return self.id

	def selecionarFilaLaboratorio(self):
		self.item = self.treeLaboratorio.focus()
		self.data = self.treeLaboratorio.item(self.item)
		self.id = self.data['values'][0]
		return self.id

	def dataCohorte(self):
		self.item = self.treeCohorte.focus()
		self.data = self.treeCohorte.item(self.item)
		self.id = self.data['values'][1]
		return self.id

	def dataTrayecto(self):
		self.item = self.treeTrayecto.focus()
		self.data = self.treeTrayecto.item(self.item)
		self.id = self.data['values'][1]
		return self.id

	def dataTrimestre(self):
		self.item = self.treeTrimestre.focus()
		self.data = self.treeTrimestre.item(self.item)
		self.id = self.data['values'][1]
		return self.id

	def dataSeccion(self):
		self.item = self.treeSeccion.focus()
		self.data = self.treeSeccion.item(self.item)
		self.id = self.data['values'][1]
		return self.id

	def dataUnidadCurricular(self):
		self.item = self.treeUnidadCurricular.focus()
		self.data = self.treeUnidadCurricular.item(self.item)
		self.id = self.data['values'][1]
		return self.id
	
	def eliminarMateria(self):
		if self.treeGestionar.selection():
			if messagebox.askyesno('Delete','¿Desea eliminar la materia selecionada?'):
				self.query = 'DELETE FROM materias_asignadas WHERE Id = ?'
				self.parametros = self.selecionarFilaGestionar()
				self.conexion(self.query, (self.parametros,))
				self.query1 = 'DELETE FROM materias_docentes WHERE materias_docentes.Id_materias_asignadas = ?'
				self.conexion(self.query1, (self.parametros,))
				self.query2 = 'DELETE FROM materias_laboratorios WHERE materias_laboratorios.Id_materias_asignadas = ?'
				self.conexion(self.query2, (self.parametros,))
				self.MostrarDatosGestionar()
				messagebox.showinfo(title='Info', message='Materia eliminada correctamente.')
			else:
				self.MostrarDatosGestionar()
		else:
			messagebox.showwarning(title='Wanning', message='Seleccione una materia a eliminar.')
		pass

	def selecionarFilaGestionar(self):
		self.item = self.treeGestionar.focus()
		self.data = self.treeGestionar.item(self.item)
		self.id = self.data['values'][0]
		return self.id

	def editarMateria(self):
		if self.treeGestionar.selection():
			if self.treeLapsoAcademico.selection() and self.treeCohorte.selection() and self.treeTrayecto.selection() and self.treeTrimestre.selection() and self.treeSeccion.selection() and self.treeTurno.selection() and self.treeDia.selection and self.treeHoraInicial.selection() and self.treeHoraFinal.selection() and self.treeUnidadCurricular.selection():
				if messagebox.askyesno('Delete','¿Desea editar el registro seleccionado?'):
					self.parametros = (self.seleccion,self.selecionarFilaLapsoAcademico(),self.selecionarFilaCohorte(),self.selecionarFilaTrayecto(),self.selecionarFilaTrimestre(),self.selecionarFilaSeccion(),self.selecionarFilaTurno(),self.selecionarFilaDia(),self.selecionarFilaHoraInicial(),self.selecionarFilaHoraFinal(),self.selecionarFilaUnidadCurricular())
					self.queryValidar = ("SELECT materias_asignadas.Id ,docente.NombreApellido, lapso_academico.LapsoAcademico,cohorte.Cohorte, trayecto.Trayecto, trimestre.Trimestre, seccion.Seccion, modalidad.Turno, semana.Dia, hora_inicial.Hora, hora_final.Hora, unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN docente ON  docente.Id = materias_asignadas.Id_docente  INNER JOIN lapso_academico ON  lapso_academico.Id = materias_asignadas.Id_lapso_academico INNER JOIN cohorte ON  cohorte.Id = materias_asignadas.Id_cohorte INNER JOIN trayecto ON trayecto.Id = materias_asignadas.Id_trayecto INNER JOIN trimestre ON trimestre.Id = materias_asignadas.Id_trimestre INNER JOIN seccion ON seccion.Id = materias_asignadas.Id_seccion INNER JOIN modalidad ON modalidad.Id = materias_asignadas.Id_modalidad INNER JOIN semana ON semana.Id = materias_asignadas.Id_semana INNER JOIN hora_inicial ON hora_inicial.Id = materias_asignadas.Id_hora_inicial INNER JOIN hora_final ON hora_final.Id = materias_asignadas.Id_hora_final INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_semana = ? AND materias_asignadas.Id_hora_inicial = ? AND materias_asignadas.Id_hora_final = ? AND materias_asignadas.Id_unidad_curricular = ?")
					self.mostrar =  self.conexion(self.queryValidar,self.parametros)
					if self.mostrar.fetchall():
						messagebox.showwarning(title='warning', message="Registro ya exixte")	
					else:
						self.same = self.conexion(
						'SELECT lapso_academico.LapsoAcademico, cohorte.Cohorte, trayecto.Trayecto, trimestre.Trimestre, seccion.Seccion, modalidad.Turno, semana.Dia, hora_inicial.Hora, hora_final.Hora, unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN lapso_academico ON  lapso_academico.Id = materias_asignadas.Id_lapso_academico INNER JOIN cohorte ON  cohorte.Id = materias_asignadas.Id_cohorte INNER JOIN trayecto ON trayecto.Id = materias_asignadas.Id_trayecto INNER JOIN trimestre ON trimestre.Id = materias_asignadas.Id_trimestre INNER JOIN seccion ON seccion.Id = materias_asignadas.Id_seccion INNER JOIN modalidad ON modalidad.Id = materias_asignadas.Id_modalidad INNER JOIN semana ON semana.Id = materias_asignadas.Id_semana INNER JOIN hora_inicial ON hora_inicial.Id = materias_asignadas.Id_hora_inicial INNER JOIN hora_final ON hora_final.Id = materias_asignadas.Id_hora_final INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_semana = ? AND materias_asignadas.Id_hora_inicial = ? AND materias_asignadas.Id_hora_final = ? AND materias_asignadas.Id_unidad_curricular = ?',
						(self.selecionarFilaLapsoAcademico(),self.selecionarFilaCohorte(),self.selecionarFilaTrayecto(),self.selecionarFilaTrimestre(),self.selecionarFilaSeccion(),self.selecionarFilaTurno(),self.selecionarFilaDia(),self.selecionarFilaHoraInicial(),self.selecionarFilaHoraFinal(),self.selecionarFilaUnidadCurricular())).fetchall()
						if self.same:
							messagebox.showwarning(title='warning', message="Este registro ya le pertenece a otro docente")	
						else:
							if self.laboratorio.get() == 'Si':
								if self.treeLaboratorio.selection():
									self.query1 = ('UPDATE materias_asignadas SET Id_lapso_academico = ? WHERE Id = ?')
									self.query2 = ('UPDATE materias_asignadas SET Id_cohorte = ? WHERE Id = ?')
									self.query3 = ('UPDATE materias_asignadas SET Id_trayecto = ? WHERE Id = ?')
									self.query4 = ('UPDATE materias_asignadas SET Id_trimestre = ? WHERE Id = ?')
									self.query5 = ('UPDATE materias_asignadas SET Id_seccion = ? WHERE Id = ?')
									self.query6 = ('UPDATE materias_asignadas SET Id_modalidad = ? WHERE Id = ?')
									self.query7 = ('UPDATE materias_asignadas SET Id_semana = ? WHERE Id = ?')
									self.query8 = ('UPDATE materias_asignadas SET Id_hora_inicial = ? WHERE Id = ?')
									self.query9 = ('UPDATE materias_asignadas SET Id_hora_final = ? WHERE Id = ?')
									self.query10 = ('UPDATE materias_asignadas SET Id_unidad_curricular = ? WHERE Id = ?')
									self.conexion(self.query1,(self.selecionarFilaLapsoAcademico(),self.selecionarFilaGestionar()))
									self.conexion(self.query2,(self.selecionarFilaCohorte(),self.selecionarFilaGestionar()))
									self.conexion(self.query3,(self.selecionarFilaTrayecto(),self.selecionarFilaGestionar()))
									self.conexion(self.query4,(self.selecionarFilaTrimestre(),self.selecionarFilaGestionar()))
									self.conexion(self.query5,(self.selecionarFilaSeccion(),self.selecionarFilaGestionar()))
									self.conexion(self.query6,(self.selecionarFilaTurno(),self.selecionarFilaGestionar()))
									self.conexion(self.query7,(self.selecionarFilaDia(),self.selecionarFilaGestionar()))
									self.conexion(self.query8,(self.selecionarFilaHoraInicial(),self.selecionarFilaGestionar()))
									self.conexion(self.query9,(self.selecionarFilaHoraFinal(),self.selecionarFilaGestionar()))
									self.conexion(self.query10,(self.selecionarFilaUnidadCurricular(),self.selecionarFilaGestionar()))
					
									self.query11 = ('UPDATE materias_docentes SET Id_lapso_academico = ? WHERE Id_materias_asignadas = ?')
									self.query12 = ('UPDATE materias_docentes SET Id_modalidad = ? WHERE Id_materias_asignadas = ?')
									self.query13 = ('UPDATE materias_docentes SET materia = ? WHERE Id_materias_asignadas = ?')
									self.query14 = ('UPDATE materias_docentes SET Id_semana = ? WHERE Id_materias_asignadas = ?')
									self.query15 = ('UPDATE materias_docentes SET Id_hora_inicial = ? WHERE Id_materias_asignadas = ?')
									self.query16 = ('UPDATE materias_docentes SET Id_hora_final = ? WHERE Id_materias_asignadas = ?')
									self.conexion(self.query11,(self.selecionarFilaLapsoAcademico(),self.selecionarFilaGestionar()))
									self.conexion(self.query12,(self.selecionarFilaTurno(),self.selecionarFilaGestionar()))
									self.materiaDocente = ('Cohorte ' + str(self.dataCohorte()) + ' Trayecto ' + str(self.dataTrayecto()) + ' Trimestre ' + str(self.dataTrimestre()) + ' Sección ' + str(self.dataSeccion()) + ' ' + str(self.dataUnidadCurricular()))
									self.conexion(self.query13,(self.materiaDocente,self.selecionarFilaGestionar()))
									self.conexion(self.query14,(self.selecionarFilaDia(),self.selecionarFilaGestionar()))
									self.conexion(self.query15,(self.selecionarFilaHoraInicial(),self.selecionarFilaGestionar()))
									self.conexion(self.query16,(self.selecionarFilaHoraFinal(),self.selecionarFilaGestionar()))

									self.same = self.conexion('SELECT * FROM materias_laboratorios WHERE materias_laboratorios.Id_materias_asignadas = ?',
									(self.selecionarFilaGestionar(),)).fetchall()

									if self.same:
										self.query17 = ('UPDATE materias_laboratorios SET Id_laboratorio = ? WHERE Id_materias_asignadas = ?')
										self.query18 = ('UPDATE materias_laboratorios SET Id_lapso_academico = ? WHERE Id_materias_asignadas = ?')
										self.query19 = ('UPDATE materias_laboratorios SET Id_modalidad = ? WHERE Id_materias_asignadas = ?')
										self.query20 = ('UPDATE materias_laboratorios SET materia = ? WHERE Id_materias_asignadas = ?')
										self.query21 = ('UPDATE materias_laboratorios SET Id_semana = ? WHERE Id_materias_asignadas = ?')
										self.query22 = ('UPDATE materias_laboratorios SET Id_hora_inicial = ? WHERE Id_materias_asignadas = ?')
										self.query23 = ('UPDATE materias_laboratorios SET Id_hora_final = ? WHERE Id_materias_asignadas = ?')
										self.conexion(self.query17,(self.selecionarFilaLaboratorio(),self.selecionarFilaGestionar()))
										self.conexion(self.query18,(self.selecionarFilaLapsoAcademico(),self.selecionarFilaGestionar()))
										self.conexion(self.query19,(self.selecionarFilaTurno(),self.selecionarFilaGestionar()))
										self.materiaDocente = ('Cohorte ' + str(self.dataCohorte()) + ' Trayecto ' + str(self.dataTrayecto()) + ' Trimestre ' + str(self.dataTrimestre()) + ' Sección ' + str(self.dataSeccion()) + ' ' + str(self.dataUnidadCurricular()))
										self.conexion(self.query20,(self.materiaDocente,self.selecionarFilaGestionar()))
										self.conexion(self.query21,(self.selecionarFilaDia(),self.selecionarFilaGestionar()))
										self.conexion(self.query22,(self.selecionarFilaHoraInicial(),self.selecionarFilaGestionar()))
										self.conexion(self.query23,(self.selecionarFilaHoraFinal(),self.selecionarFilaGestionar()))
									else:
										self.query2 = ('INSERT INTO materias_laboratorios VALUES (NULL,?,?,?,?,?,?,?,?,?)')
										self.materiaDocente = ('Cohorte ' + str(self.dataCohorte()) + ' Trayecto ' + str(self.dataTrayecto()) + ' Trimestre ' + str(self.dataTrimestre()) + ' Sección ' + str(self.dataSeccion()) + ' ' + str(self.dataUnidadCurricular()))
										self.conexion(self.query2,(self.selecionarFilaGestionar(),self.seleccion,self.selecionarFilaLaboratorio(),self.selecionarFilaLapsoAcademico(),self.selecionarFilaTurno(),self.materiaDocente,self.selecionarFilaDia(),self.selecionarFilaHoraInicial(),self.selecionarFilaHoraFinal()))
		
									self.MostrarDatosGestionar()
									self.MostrarLapsoAcademico()
									self.MostrarCohorte()
									self.MostrarTrayecto()
									self.MostrarTrimestre()
									self.MostrarSeccion()
									self.MostrarTurno()
									self.MostrarDia()
									self.MostrarHoraInicial()
									self.MostrarHoraFinal()
									self.MostrarUnidadCurricular()
									messagebox.showinfo(title='Info', message='Registro editado correctamente.')
								else:
									messagebox.showwarning(title='Warning', message='Seleccione un laboratorio')
							elif self.laboratorio.get() == 'No':
								self.query1 = ('UPDATE materias_asignadas SET Id_lapso_academico = ? WHERE Id = ?')
								self.query2 = ('UPDATE materias_asignadas SET Id_cohorte = ? WHERE Id = ?')
								self.query3 = ('UPDATE materias_asignadas SET Id_trayecto = ? WHERE Id = ?')
								self.query4 = ('UPDATE materias_asignadas SET Id_trimestre = ? WHERE Id = ?')
								self.query5 = ('UPDATE materias_asignadas SET Id_seccion = ? WHERE Id = ?')
								self.query6 = ('UPDATE materias_asignadas SET Id_modalidad = ? WHERE Id = ?')
								self.query7 = ('UPDATE materias_asignadas SET Id_semana = ? WHERE Id = ?')
								self.query8 = ('UPDATE materias_asignadas SET Id_hora_inicial = ? WHERE Id = ?')
								self.query9 = ('UPDATE materias_asignadas SET Id_hora_final = ? WHERE Id = ?')
								self.query10 = ('UPDATE materias_asignadas SET Id_unidad_curricular = ? WHERE Id = ?')
								self.conexion(self.query1,(self.selecionarFilaLapsoAcademico(),self.selecionarFilaGestionar()))
								self.conexion(self.query2,(self.selecionarFilaCohorte(),self.selecionarFilaGestionar()))
								self.conexion(self.query3,(self.selecionarFilaTrayecto(),self.selecionarFilaGestionar()))
								self.conexion(self.query4,(self.selecionarFilaTrimestre(),self.selecionarFilaGestionar()))
								self.conexion(self.query5,(self.selecionarFilaSeccion(),self.selecionarFilaGestionar()))
								self.conexion(self.query6,(self.selecionarFilaTurno(),self.selecionarFilaGestionar()))
								self.conexion(self.query7,(self.selecionarFilaDia(),self.selecionarFilaGestionar()))
								self.conexion(self.query8,(self.selecionarFilaHoraInicial(),self.selecionarFilaGestionar()))
								self.conexion(self.query9,(self.selecionarFilaHoraFinal(),self.selecionarFilaGestionar()))
								self.conexion(self.query10,(self.selecionarFilaUnidadCurricular(),self.selecionarFilaGestionar()))
				
								self.query11 = ('UPDATE materias_docentes SET Id_lapso_academico = ? WHERE Id_materias_asignadas = ?')
								self.query12 = ('UPDATE materias_docentes SET Id_modalidad = ? WHERE Id_materias_asignadas = ?')
								self.query13 = ('UPDATE materias_docentes SET materia = ? WHERE Id_materias_asignadas = ?')
								self.query14 = ('UPDATE materias_docentes SET Id_semana = ? WHERE Id_materias_asignadas = ?')
								self.query15 = ('UPDATE materias_docentes SET Id_hora_inicial = ? WHERE Id_materias_asignadas = ?')
								self.query16 = ('UPDATE materias_docentes SET Id_hora_final = ? WHERE Id_materias_asignadas = ?')
								self.conexion(self.query11,(self.selecionarFilaLapsoAcademico(),self.selecionarFilaGestionar()))
								self.conexion(self.query12,(self.selecionarFilaTurno(),self.selecionarFilaGestionar()))
								self.materiaDocente = ('Cohorte ' + str(self.dataCohorte()) + ' Trayecto ' + str(self.dataTrayecto()) + ' Trimestre ' + str(self.dataTrimestre()) + ' Sección ' + str(self.dataSeccion()) + ' ' + str(self.dataUnidadCurricular()))
								self.conexion(self.query13,(self.materiaDocente,self.selecionarFilaGestionar()))
								self.conexion(self.query14,(self.selecionarFilaDia(),self.selecionarFilaGestionar()))
								self.conexion(self.query15,(self.selecionarFilaHoraInicial(),self.selecionarFilaGestionar()))
								self.conexion(self.query16,(self.selecionarFilaHoraFinal(),self.selecionarFilaGestionar()))

								self.same = self.conexion('SELECT * FROM materias_laboratorios WHERE materias_laboratorios.Id_materias_asignadas = ?',
								(self.selecionarFilaGestionar(),)).fetchall()

								if self.same:
									self.query2 = 'DELETE FROM materias_laboratorios WHERE materias_laboratorios.Id_materias_asignadas = ?'
									self.conexion(self.query2, (self.selecionarFilaGestionar(),))

								self.MostrarDatosGestionar()
								self.MostrarLapsoAcademico()
								self.MostrarCohorte()
								self.MostrarTrayecto()
								self.MostrarTrimestre()
								self.MostrarSeccion()
								self.MostrarTurno()
								self.MostrarDia()
								self.MostrarHoraInicial()
								self.MostrarHoraFinal()
								self.MostrarUnidadCurricular()
								messagebox.showinfo(title='Info', message='Registro editado correctamente.')
								
							else:
								messagebox.showwarning(title='Warning', message='Seleccione la casilla')
				else:
					self.MostrarDatosGestionar()
			else:
				messagebox.showwarning(title='Wanning', message='Seleccione datos a editar.')
		else:
			messagebox.showwarning(title='Wanning', message='Seleccione una registro a editar.')

	def reportes(self):
		self.newReportes = tk.Toplevel()
		self.newReportes.title('Reportes')
		self.newReportes.geometry('350x360')
		self.newReportes.resizable(width=0,height=0)
		self.newReportes.iconbitmap(uptpc)
		ttk.Label(self.newReportes, text='REPORTES DE DOCENTES',font=('Helvetica',14)).place(x=45,y=5)

		self.framecontainer2 = ttk.Labelframe(self.newReportes)
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

		ttk.Button(self.framecontainer2, text='GENERAR REPORTE', command=self.generarReporte).grid(row=3,column=0,padx=0,pady=0)

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
		
		self.newReportes.mainloop()

	def informacionAdcional(self):
		pass

	def generarReporte(self):
		self.docenteId = self.selecionarFilaReporteDocente()
		self.lapsoId = self.selecionarFilaReporteLapso()
		self.docente = self.ReporteDocente()
		self.lapso = self.ReporteLapso()

		self.parametrosReportes = (self.docenteId, self.lapsoId)

		self.pdf = canvas.Canvas('reporte.pdf', pagesize = A3)
		self.pdf.setFontSize(size=12)
		self.pdf.drawString(375,1150,'CARGA ACADÉMICA')
		self.pdf.drawString(368,1135,'Lapso Académico ' + self.lapso)
		self.pdf.drawImage(logoPDF,690,1100,width=80,height=80)
		self.tablaInicio()
		self.pdf.drawString(10,980,'Por medio de la presente se le notifica que Usted, ha sido designado(a) para dictar la(s) unidad(es) curricular(es) que a continuación se especifica(n):')
		self.tablaMaterias()
		self.listadoMaterias()
		if self.counter == 10: 
			self.pdf.drawString(375,880,'Horarios de clases')
			print('horario de clases---10')
		elif self.counter == 9: 
			self.pdf.drawString(375,880,'Horarios de clases')
			print('horario de clases---9')
		elif self.counter == 8: 
			self.pdf.drawString(375,880,'Horarios de clases')
			print('horario de clases---8')
		elif self.counter == 7: 
			self.pdf.drawString(375,880,'Horarios de clases')
			print('horario de clases---7')
		elif self.counter == 6: 
			self.pdf.drawString(375,880,'Horarios de clases')
			print('horario de clases---6')
		elif self.counter == 5: 
			self.pdf.drawString(375,880,'Horarios de clases')
			print('horario de clases---5')
		elif self.counter == 4: 
			self.pdf.drawString(375,880,'Horarios de clases')
			print('horario de clases---4')
		elif self.counter == 3: 
			self.pdf.drawString(375,880,'Horarios de clases')
			print('horario de clases---3')
		elif self.counter == 2: 
			self.pdf.drawString(375,880,'Horarios de clases')
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
			self.pdf.drawString(330,305,'Adscripción Académico-administrativa')
			print('adscripcion---10')
		elif self.counter == 9: 
			self.pdf.drawString(330,305,'Adscripción Académico-administrativa')
			print('adscripcion---9')
		elif self.counter == 8: 
			self.pdf.drawString(330,305,'Adscripción Académico-administrativa')
			print('adscripcion---8')
		elif self.counter == 7: 
			self.pdf.drawString(330,305,'Adscripción Académico-administrativa')
			print('adscripcion---7')
		elif self.counter == 6: 
			self.pdf.drawString(330,305,'Adscripción Académico-administrativa')
			print('adscripcion---6')
		elif self.counter == 5: 
			self.pdf.drawString(330,305,'Adscripción Académico-administrativa')
			print('adscripcion---5')
		elif self.counter == 4: 
			self.pdf.drawString(330,305,'Adscripción Académico-administrativa')
			print('adscripcion---4')
		elif self.counter == 3: 
			self.pdf.drawString(330,305,'Adscripción Académico-administrativa')
			print('adscripcion---3')
		elif self.counter == 2: 
			self.pdf.drawString(330,305,'Adscripción Académico-administrativa')
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

	def MostrarReporteDocente(self):
		self.rows = self.TraerDatos("SELECT Id, NombreApellido FROM docente")
		for row in self.rows:
			self.treeReportes.insert('',tk.END,values=row)
			
	def MostrarReporteLapso(self):
		self.rows = self.TraerDatos("SELECT * FROM lapso_academico")
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
            [Paragraph('Título de Post-grado',self.center)],
            [Paragraph('Descarga Academica:',self.center)],
            [Paragraph('Razon de la descarga:',self.center)]
        ]
		
		self.nombre = self.materia('SELECT docente.NombreApellido from docente WHERE docente.Id = ?',(self.docenteId,))
		self.tabla1[0].append(Paragraph(self.nombre,self.center))
		self.tabla1[0].append(Paragraph('Cedula:',self.center))
		self.cedula = self.materia('SELECT docente.Cedula from docente WHERE docente.Id = ?',(self.docenteId,))
		self.tabla1[0].append(Paragraph(self.cedula,self.center))
		self.categoria = self.materia('SELECT docente.Categoria from docente WHERE docente.Id = ?',(self.docenteId,))
		self.tabla1[1].append(Paragraph(self.categoria,self.left))
		self.setStyles.append(('SPAN',(1,1),(3,1)))
		self.dedicacion = self.materia('SELECT docente.Dedicacion from docente WHERE docente.Id = ?',(self.docenteId,))
		self.tabla1[2].append(Paragraph(self.dedicacion,self.left))
		self.setStyles.append(('SPAN',(1,2),(3,2)))
		self.pregrado = self.materia('SELECT docente.Pregrado from docente WHERE docente.Id = ?',(self.docenteId,))
		self.tabla1[3].append(Paragraph(self.pregrado,self.left))
		self.setStyles.append(('SPAN',(1,3),(3,3)))
		self.postgrado = self.materia('SELECT docente.Postgrado from docente WHERE docente.Id = ?',(self.docenteId,))
		self.tabla1[4].append(Paragraph(self.postgrado,self.left))
		self.setStyles.append(('SPAN',(1,4),(3,4)))
		self.descargaAcademica = self.materia('SELECT docente.DescargaAcademica from docente WHERE docente.Id = ?',(self.docenteId,))
		self.tabla1[5].append(Paragraph(self.descargaAcademica,self.left))
		self.tabla1[5].append(Paragraph('Condicion laboral:',self.left))
		self.condicionLaboral = self.materia('SELECT docente.CondicionLaboral from docente WHERE docente.Id = ?',(self.docenteId,))
		self.tabla1[5].append(Paragraph(self.condicionLaboral,self.left))
		self.razonDescarga = self.materia('SELECT docente.RazonDescarga from docente WHERE docente.Id = ?',(self.docenteId,))
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
			# self.pdf.showPage()
			self.listadoMateria.drawOn(self.pdf,68,125)
			print('materia----10')
		elif self.counter == 9: 
			self.listadoMateria.drawOn(self.pdf,68,125)
			print('materia-----9')
		elif self.counter == 8: 
			self.listadoMateria.drawOn(self.pdf,68,125)
			print('materia-----8')
		elif self.counter == 7: 
			self.listadoMateria.drawOn(self.pdf,68,125)
			print('materia-----7')
		elif self.counter == 6: 
			self.listadoMateria.drawOn(self.pdf,68,125)
			print('materia-----6')
		elif self.counter == 5: 
			self.listadoMateria.drawOn(self.pdf,68,125)
			print('materia-----5')
		elif self.counter == 4: 
			self.listadoMateria.drawOn(self.pdf,68,125)
			print('materia-----4')
		elif self.counter == 3: 
			self.listadoMateria.drawOn(self.pdf,68,125)
			print('materia-----3')
		elif self.counter == 2: 
			self.listadoMateria.drawOn(self.pdf,10,890)
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
            'SELECT unidad_curricular.UnidadCurricular,seccion.Seccion,unidad_curricular.hora, unidad_curricular.departamento,cohorte.Cohorte, trayecto.Trayecto, trimestre.Trimestre, unidad_curricular.Pt FROM materias_asignadas INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular INNER JOIN seccion ON seccion.Id = materias_asignadas.Id_seccion INNER JOIN cohorte ON  cohorte.Id = materias_asignadas.Id_cohorte INNER JOIN trayecto ON trayecto.Id = materias_asignadas.Id_trayecto INNER JOIN trimestre ON trimestre.Id = materias_asignadas.Id_trimestre WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ?',
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
			# self.pdf.showPage()
			self.tableHorarioMorning.drawOn(self.pdf,11,690)
			print('mornig----10')
		elif self.counter == 9: 
			self.tableHorarioMorning.drawOn(self.pdf,11,690)
			print('mornig-----9')
		elif self.counter == 8: 
			self.tableHorarioMorning.drawOn(self.pdf,11,690)
			print('mornig-----8')
		elif self.counter == 7: 
			self.tableHorarioMorning.drawOn(self.pdf,11,690)
			print('mornig-----7')
		elif self.counter == 6: 
			self.tableHorarioMorning.drawOn(self.pdf,11,690)
			print('mornig-----6')
		elif self.counter == 5: 
			self.tableHorarioMorning.drawOn(self.pdf,11,690)
			print('mornig-----5')
		elif self.counter == 4: 
			self.tableHorarioMorning.drawOn(self.pdf,11,690)
			print('mornig-----4')
		elif self.counter == 3: 
			self.tableHorarioMorning.drawOn(self.pdf,11,690)
			print('mornig-----3')
		elif self.counter == 2: 
			self.tableHorarioMorning.drawOn(self.pdf,11,690)
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
            [Paragraph('Horario de Clases Mañana',self.center),Paragraph('Lunes',self.center),Paragraph('Martes',self.center),Paragraph('Miercoles',self.center),Paragraph('Jueves',self.center),Paragraph('Viernes',self.center)],
            [Paragraph('7:10 - 7:55',self.center)],
            [Paragraph('8:00 - 8:45',self.center)],
            [Paragraph('8:50 - 9:35',self.center)],
            [Paragraph('9:40 - 10:25',self.center)],
            [Paragraph('10:30 - 11:15',self.center)],
            [Paragraph('11:20 - 12:05',self.center)],
        ]
		
		return self.morning

	def tablaHorarioAfternon(self):
		self.tableHorarioAfternon = Table(self.obtenerTablaHorarioAfternon(),colWidths=137, rowHeights=25)
		self.tableHorarioAfternon.setStyle(TableStyle(self.setStyles5))
		self.tableHorarioAfternon.wrapOn(self.pdf,self.width,self.heigth)
		if self.counter == 10: 
			# self.pdf.showPage()
			self.tableHorarioAfternon.drawOn(self.pdf,11,510)
			print('afternon----10')
		elif self.counter == 9: 
			self.tableHorarioAfternon.drawOn(self.pdf,11,510)
			print('afternon-----9')
		elif self.counter == 8: 
			self.tableHorarioAfternon.drawOn(self.pdf,11,510)
			print('afternon-----8')
		elif self.counter == 7: 
			self.tableHorarioAfternon.drawOn(self.pdf,11,510)
			print('afternon-----7')
		elif self.counter == 6: 
			self.tableHorarioAfternon.drawOn(self.pdf,11,510)
			print('afternon-----6')
		elif self.counter == 5: 
			self.tableHorarioAfternon.drawOn(self.pdf,11,510)
			print('afternon-----5')
		elif self.counter == 4: 
			self.tableHorarioAfternon.drawOn(self.pdf,11,510)
			print('afternon-----4')
		elif self.counter == 3: 
			self.tableHorarioAfternon.drawOn(self.pdf,11,510)
			print('afternon-----3')
		elif self.counter == 2: 
			self.tableHorarioAfternon.drawOn(self.pdf,11,510)
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
            [Paragraph('Horario de Clases Tarde',self.center),Paragraph('Lunes',self.center),Paragraph('Martes',self.center),Paragraph('Miercoles',self.center),Paragraph('Jueves',self.center),Paragraph('Viernes',self.center)],
            [Paragraph('1:05 - 1:55',self.center)],
            [Paragraph('1:55 - 2:40',self.center)],
            [Paragraph('2:45 - 3:30',self.center)],
            [Paragraph('3:45 - 4:20',self.center)],
            [Paragraph('4:25 - 5:10',self.center)],
            [Paragraph('5:15 - 6:00',self.center)]
        ]
		
		return self.afternon

	def tablaHorarioNinght(self):
		self.tableHorarioNinght = Table(self.obtenerTablaHorarioNinght(),colWidths=137, rowHeights=25)
		self.tableHorarioNinght.setStyle(TableStyle(self.setStyles6))
		self.tableHorarioNinght.wrapOn(self.pdf,self.width,self.heigth)
		if self.counter == 10: 
			# self.pdf.showPage()
			self.tableHorarioNinght.drawOn(self.pdf,11,330)
			print('ninght----10')
		elif self.counter == 9: 
			self.tableHorarioNinght.drawOn(self.pdf,11,330)
			print('ninght-----9')
		elif self.counter == 8: 
			self.tableHorarioNinght.drawOn(self.pdf,11,330)
			print('ninght-----8')
		elif self.counter == 7: 
			self.tableHorarioNinght.drawOn(self.pdf,11,330)
			print('ninght-----7')
		elif self.counter == 6: 
			self.tableHorarioNinght.drawOn(self.pdf,11,330)
			print('ninght-----6')
		elif self.counter == 5: 
			self.tableHorarioNinght.drawOn(self.pdf,11,330)
			print('ninght-----5')
		elif self.counter == 4: 
			self.tableHorarioNinght.drawOn(self.pdf,11,330)
			print('ninght-----4')
		elif self.counter == 3: 
			self.tableHorarioNinght.drawOn(self.pdf,11,330)
			print('ninght-----3')
		elif self.counter == 2: 
			self.tableHorarioNinght.drawOn(self.pdf,11,330)
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
            [Paragraph('Horario de Clases Noche',self.center),Paragraph('Lunes',self.center),Paragraph('Martes',self.center),Paragraph('Miercoles',self.center),Paragraph('Jueves',self.center),Paragraph('Viernes',self.center)],
            [Paragraph('6:00 - 6:45',self.center)],
            [Paragraph('6:45 - 7:30',self.center)],
            [Paragraph('7:35 - 8:20',self.center)],
            [Paragraph('8:20 - 9:05',self.center)],
            [Paragraph('9:05 - 9:50',self.center)],
            [Paragraph('9:50 - 10:35',self.center)]
        ]
		
		return self.ninght

	def tablaHorarioAdcrispcion(self):
		self.tableHorarioAdcrispcion = Table(self.obtenerTablaHorarioAdcrispcion(),colWidths=206, rowHeights=17)
		self.tableHorarioAdcrispcion.setStyle(TableStyle(self.setStyles7))
		self.tableHorarioAdcrispcion.wrapOn(self.pdf,self.width,self.heigth)
		if self.counter == 10: 
			# self.pdf.showPage()
			self.tableHorarioAdcrispcion.drawOn(self.pdf,10,255)
			print('jefe----10')
		elif self.counter == 9: 
			self.tableHorarioAdcrispcion.drawOn(self.pdf,10,255)
			print('jefe-----9')
		elif self.counter == 8: 
			self.tableHorarioAdcrispcion.drawOn(self.pdf,10,255)
			print('jefe-----8')
		elif self.counter == 7: 
			self.tableHorarioAdcrispcion.drawOn(self.pdf,10,255)
			print('jefe-----7')
		elif self.counter == 6: 
			self.tableHorarioAdcrispcion.drawOn(self.pdf,10,255)
			print('jefe-----6')
		elif self.counter == 5: 
			self.tableHorarioAdcrispcion.drawOn(self.pdf,10,255)
			print('jefe-----5')
		elif self.counter == 4: 
			self.tableHorarioAdcrispcion.drawOn(self.pdf,10,255)
			print('jefe-----4')
		elif self.counter == 3: 
			self.tableHorarioAdcrispcion.drawOn(self.pdf,10,255)
			print('jefe-----3')
		elif self.counter == 2: 
			self.tableHorarioAdcrispcion.drawOn(self.pdf,10,255)
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
		self.adcrispcion[0].append(Paragraph('Informática',self.center))
		self.adcrispcion[0].append('')
		self.setStyles7.append(('SPAN',(2,0),(3,0)))
		self.adcrispcion[1].append(Paragraph('jose',self.center))
		self.adcrispcion[1].append(Paragraph('Cargo:',self.center))
		self.adcrispcion[1].append(Paragraph('jefe',self.center))
		
		return self.adcrispcion
	
	def tablaHorarioObservacion(self):
		self.tableHorarioObservacion = Table(self.obtenerTablaHorarioObservacion(),colWidths=117, rowHeights=25)
		self.tableHorarioObservacion.setStyle(TableStyle(self.setStyles8))
		self.tableHorarioObservacion.wrapOn(self.pdf,self.width,self.heigth)
		if self.counter == 10: 
			# self.pdf.showPage()
			self.tableHorarioObservacion.drawOn(self.pdf,12,180)
			print('observacion----10')
		elif self.counter == 9: 
			self.tableHorarioObservacion.drawOn(self.pdf,12,180)
			print('observacion-----9')
		elif self.counter == 8: 
			self.tableHorarioObservacion.drawOn(self.pdf,12,180)
			print('observacion-----8')
		elif self.counter == 7: 
			self.tableHorarioObservacion.drawOn(self.pdf,12,180)
			print('observacion-----7')
		elif self.counter == 6: 
			self.tableHorarioObservacion.drawOn(self.pdf,12,180)
			print('observacion-----6')
		elif self.counter == 5: 
			self.tableHorarioObservacion.drawOn(self.pdf,12,180)
			print('observacion-----5')
		elif self.counter == 4: 
			self.tableHorarioObservacion.drawOn(self.pdf,12,180)
			print('observacion-----4')
		elif self.counter == 3: 
			self.tableHorarioObservacion.drawOn(self.pdf,12,180)
			print('observacion-----3')
		elif self.counter == 2: 
			self.tableHorarioObservacion.drawOn(self.pdf,12,180)
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
			[Paragraph('Leyenda:',self.center),Paragraph('PNF',self.center),Paragraph('Programa Nacional de Formación',self.center),Paragraph('PT',self.center),Paragraph('Programa Traicional',self.center),Paragraph('TI',self.center),Paragraph('Trayecto Inicial',self.center)]
        ]
		
		self.observacion[0].append(Paragraph('Si',self.center))
		self.observacion[0].append(Paragraph('Especifique:',self.center))
		self.setStyles8.append(('SPAN',(3,0),(6,0)))

		return self.observacion