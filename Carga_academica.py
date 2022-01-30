import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3
from rutas import *
import traceback
import sys

class CargaAcademica(tk.Toplevel):
	def __init__(self,master = None):
		super().__init__(master)
		# Config:
		self.title('Carga Académica')
		self.geometry('485x400')
		self.resizable(width=0,height=0)
		self.iconbitmap(uptpc)
		# Menu:
		self.menubar = tk.Menu(self)
		self.menubar.add_cascade(label="Volver", command=self.volver)
		self.config(menu=self.menubar)
		# Frame:
		self.Frame = ttk.Labelframe(self)
		self.Frame.grid(column=0,row=0,pady=25,padx=11)
		ttk.Label(self, text='CONSULTAR CEDULA',font=('Helvetica',14)).place(x=150,y=5)
		ttk.Label(self.Frame, text='Cedula:',font=('Helvetica',11)).grid(column=0,row=0 ,padx=5,pady=5)
		self.cedula = ttk.Entry(self.Frame, width=45)
		self.cedula.grid(column=1,row=0,padx=5,pady=5)
		self.cedula.focus()		
		self.cedula.bind('<KeyRelease>',lambda e: self.verificar(self.cedula))
		ttk.Button(self.Frame, text='CONSULTAR', command =self.consultar).grid(column=2,row=0,padx=5,pady=5)
		# Treeview:
		self.tree = ttk.Treeview(self, columns = ['#1','#2','#3'], show='headings', height=8)
		self.tree.grid(column=0,row=1, sticky='nsew',padx=5)
		self.tree.heading('#1', text = 'Id')
		self.tree.heading('#2', text = 'Nombre y Apellido')
		self.tree.heading('#3', text = 'Cedula')
		self.tree.column('#1', width=40)
		self.tree.column('#2', width=150)
		self.tree.column('#3', width=50)
		self.scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
		self.tree.configure(yscroll=self.scrollbar.set)
		self.scrollbar.grid(column=1,row=1, sticky='ns')
		# # Button:
		ttk.Button(self,text = 'GESTIONAR MATERIAS', command = self.gestionarMaterias).grid(column=0,row=2, sticky = tk.W + tk.E, padx=5)
		ttk.Button(self,text = 'CARGA ACADÉMICA DOCENTE', command = self.editar).grid(column=0,row=3, sticky = tk.W + tk.E, padx=5)
		ttk.Button(self,text = 'DESHABILITAR DODENTE', command =self.eliminar).grid(column=0,row=4,sticky = tk.W + tk.E, padx=5)

		self.MostrarDatos()

	def volver(self):
		self.destroy()

	def limpiarTabla(self,tree):
		self.DeleteChildren = tree.get_children()
		for element in self.DeleteChildren:
			tree.delete(element)

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
		self.limpiarTabla(self.tree)
		self.rows = self.TraerDatos("SELECT Id,NombreApellido,Cedula FROM docente WHERE docente.Estado = 'Activo'")
		for row in self.rows:
			self.tree.insert('',tk.END,values=row)

	def verificar(self,entry):
		codigo = entry.get()
		for i in codigo:
			if i not in '0123456789.':
				entry.delete(codigo.index(i), codigo.index(i)+1)

	def consultar(self):
		if len(self.cedula.get()) != 0:
			cedula = self.conexion('SELECT * FROM docente WHERE docente.Cedula = ? and docente.Estado = "Activo"',(self.cedula.get(),)).fetchall()
			if cedula:
				messagebox.showwarning(title='Warning', message='Cedula ya esta registrada')
				self.cedula.delete(0, tk.END)
				self.cedula.focus()
			else:
				if messagebox.askyesno('Registrar','Cedula no existe, ¿Desea registrala?'):
					valor = self.cedula.get()
					self.cedula.delete(0, tk.END)
					self.docente(valor)
				else:
					self.cedula.delete(0, tk.END)
					self.cedula.focus()
		else:
			messagebox.showwarning(title='Warning', message='Introduzca una cedula')
			self.cedula.delete(0, tk.END)
			self.cedula.focus()

	def docente(self,valor):
		self.new = tk.Toplevel()
		self.new.title('Registrar docente')
		self.new.resizable(width=0,height=0)
		self.new.iconbitmap(uptpc)
		ttk.Label(self.new,text='Cédula de Identidad N°:').grid(column=0,row=0,padx=5)
		self.entryCedula = ttk.Entry(self.new,width=45)
		self.entryCedula.grid(column=1,row=0,padx=5,pady=5)
		self.entryCedula.insert(0,valor)
		self.entryCedula.config(state=tk.DISABLED)
		ttk.Label(self.new, text='Nombre y Apellido:').grid(column=0,row=1 ,padx=5,pady=5)
		self.entryNombreApellido = ttk.Entry(self.new,width=45)
		self.entryNombreApellido.grid(column=1,row=1,padx=5,pady=5)
		self.entryNombreApellido.focus()
		ttk.Button(self.new, text='REGISTRAR DOCENTE', command=self.registrarDocente).grid(column=0,row=3,padx=5,pady=5)		
		ttk.Button(self.new, text='CANCELAR', command=self.docenteCancelar).grid(column=1,row=3,padx=5,pady=5)	
		self.new.mainloop()

	def docenteCancelar(self):
		self.new.destroy()

	def registrarDocente(self):
		if len(self.entryNombreApellido.get()) != 0:
			if messagebox.askyesno('Registrar','Registrar docente'):
				self.conexion('INSERT INTO docente VALUES (NULL,?,?,"","","","","Si","","","","No","","Activo")',(self.entryNombreApellido.get(),self.entryCedula.get()))
				self.MostrarDatos()
				messagebox.showinfo(title='Info', message='Docente Registrado.')
				self.docenteCancelar()
			else:
				self.entryNombreApellido.delete(0, tk.END)
				self.entryNombreApellido.focus()
		else:
			messagebox.showwarning(title='Warning', message='Introduzca un valor.')
	
	def selecionarFila(self):
		self.item = self.tree.focus()
		self.data = self.tree.item(self.item)
		self.id = self.data['values'][0]
		return self.id

	def eliminar(self):
		if self.tree.selection():
			if messagebox.askyesno('Deshabilitado','¿Desea deshabilitar al docente selecionado?'):
				self.parametros = self.selecionarFila()
				self.query1 = 'UPDATE docente SET Estado = "Inactivo" WHERE docente.Id = ? AND docente.Estado = "Activo"'
				self.query2 = 'UPDATE materias_asignadas SET Estado = "Inactivo" WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Estado = "Activo"'
				self.query3 = 'UPDATE materias_docentes SET Estado = "Inactivo" WHERE materias_docentes.Id_docente = ? AND materias_docentes.Estado = "Activo"'
				self.query4 = 'UPDATE materias_laboratorios SET Estado = "Inactivo" WHERE materias_laboratorios.Id_docente = ? AND materias_laboratorios.Estado = "Activo"'
				self.conexion(self.query1, (self.parametros,))
				self.conexion(self.query2, (self.parametros,))
				self.conexion(self.query3, (self.parametros,))
				self.conexion(self.query4, (self.parametros,))
				self.MostrarDatos()
				messagebox.showinfo(title='Info', message='Docente y todos sus registros deshabilitados correctamente.')
			else:
				self.MostrarDatos()
		else:
			messagebox.showwarning(title='Wanning', message='Seleccione un docente a deshabilitar.')

	def editar(self):
		if self.tree.selection():
			self.seleccion = self.selecionarFila()
			self.new = tk.Toplevel()
			self.new.title('Carga Académica Docente')
			self.new.geometry('410x440')
			self.new.resizable(width=0,height=0)
			self.new.iconbitmap(uptpc)
			self.frame = ttk.Labelframe(self.new)
			self.frame.grid(column=0,row=0,pady=5,padx=5,ipadx=0,ipady=5)
			ttk.Label(self.frame,text='Nombre y Apellido:').grid(row=0,column=0,padx=5,pady=5)
			self.entryEditarNombre = ttk.Entry(self.frame,width=40)
			self.entryEditarNombre.grid(row=0,column=1,pady=5,padx=5)
			ttk.Label(self.frame,text='Categoria:').grid(row=1,column=0,padx=5,pady=5)
			self.entryEditarCategoria = ttk.Entry(self.frame, width=40)
			self.entryEditarCategoria.grid(row=1,column=1,padx=5,pady=5)
			ttk.Label(self.frame,text='Dedicación:').grid(row=2,column=0,padx=5,pady=5)
			self.entryEditarDedicación = ttk.Entry(self.frame, width=40)
			self.entryEditarDedicación.grid(row=2,column=1,padx=5,pady=5)
			ttk.Label(self.frame,text='Titulo de Pre-grado:').grid(row=3,column=0,padx=5,pady=5)
			self.entryEditarTpregado = ttk.Entry(self.frame, width=40)
			self.entryEditarTpregado.grid(row=3,column=1,padx=5,pady=5)
			ttk.Label(self.frame,text='Titulo de Post-grado:').grid(row=4,column=0,padx=5,pady=5)
			self.entryEditarTposgrado = ttk.Entry(self.frame, width=40)
			self.entryEditarTposgrado.grid(row=4,column=1,padx=5,pady=5)
			self.DescargaAcademicaEditar = tk.StringVar()
			ttk.Label(self.frame,text='Descarga Académica').grid(row=5,column=0)
			ttk.Radiobutton(self.frame, text='Si', value='Si',variable=self.DescargaAcademicaEditar, command= self.descargaAcademicaSi).grid(row=6,column=0)
			ttk.Radiobutton(self.frame, text='No', value='No',variable=self.DescargaAcademicaEditar, command= self.descargaAcademicaNo).grid(row=6,column=1)
			ttk.Label(self.frame,text='Razon de la descarga:').grid(row=7,column=0,padx=5,pady=5)
			self.entryEditarRazon = ttk.Entry(self.frame,width=40)
			self.entryEditarRazon.grid(row=7,column=1,padx=5,pady=5)
			self.entryEditarRazon.config(state=tk.DISABLED)
			self.CondicionLaboralEditar = tk.StringVar()
			ttk.Label(self.frame, text='Condición Laboral').grid(row=8,column=0)
			ttk.Radiobutton(self.frame, text='Ordinario', value='Ordinario',variable=self.CondicionLaboralEditar).grid(row=9,column=0)
			ttk.Radiobutton(self.frame, text='Contratado', value='Contratado',variable=self.CondicionLaboralEditar).grid(row=9,column=1)
			ttk.Label(self.frame,text='Telefono/Correo:').grid(row=10,column=0,padx=5,pady=5)
			self.entryEditarTelefono = ttk.Entry(self.frame,width=40)
			self.entryEditarTelefono.grid(row=10,column=1,padx=5,pady=5)
			self.laboraEditar = tk.StringVar()
			ttk.Label(self.frame, text='Labora en otra empresa:').grid(row=11,column=0)
			ttk.Radiobutton(self.frame, text='Si', value='Si',variable=self.laboraEditar, command=self.especifiqueSi).grid(row=12,column=0)
			ttk.Radiobutton(self.frame, text='No', value='No',variable=self.laboraEditar, command=self.especifiqueNo).grid(row=12,column=1)
			ttk.Label(self.frame,text='Especifique:').grid(row=13,column=0,padx=5,pady=5)
			self.entryEditarEspecifique = ttk.Entry(self.frame,width=40)
			self.entryEditarEspecifique.grid(row=13,column=1,padx=5,pady=5)
			self.entryEditarEspecifique.config(state=tk.DISABLED)
			ttk.Button(self.new,text='ACTUALIZAR', command=self.editar2).grid(row=1,column=0)
			self.dataDocente(self.seleccion)
			self.new.mainloop()	
		else: 
			messagebox.showwarning(title='Wanning', message='Seleccione un docente a editar.')
	
	def especifiqueSi(self):
		self.entryEditarEspecifique.config(state=tk.NORMAL)

	def especifiqueNo(self):
		self.entryEditarEspecifique.config(state=tk.DISABLED)

	def descargaAcademicaSi(self):
		self.entryEditarRazon.config(state=tk.NORMAL)

	def descargaAcademicaNo(self):
		self.entryEditarRazon.config(state=tk.DISABLED)

	def dataDocente(self,id):
		nombreApellido = self.conexion('SELECT NombreApellido FROM docente WHERE docente.Id = ? and docente.Estado = "Activo"', (id,)).fetchone()
		self.entryEditarNombre.insert(0,nombreApellido[0])
		categoria = self.conexion('SELECT Categoria FROM docente WHERE docente.Id = ? and docente.Estado = "Activo"', (id,)).fetchone()
		self.entryEditarCategoria.insert(0,categoria[0])
		dedicacion = self.conexion('SELECT Dedicacion FROM docente WHERE docente.Id = ? and docente.Estado = "Activo"', (id,)).fetchone()
		self.entryEditarDedicación.insert(0,dedicacion[0])
		pregrado = self.conexion('SELECT Pregrado FROM docente WHERE docente.Id = ? and docente.Estado = "Activo"', (id,)).fetchone()
		self.entryEditarTpregado.insert(0,pregrado[0])
		postgrado = self.conexion('SELECT Postgrado FROM docente WHERE docente.Id = ? and docente.Estado = "Activo"', (id,)).fetchone()
		self.entryEditarTposgrado.insert(0,postgrado[0])
		descargaAcademica = self.conexion('SELECT DescargaAcademica FROM docente WHERE docente.Id = ? and docente.Estado = "Activo"', (id,)).fetchone()
		if descargaAcademica[0] == 'Si':
			self.DescargaAcademicaEditar.set(value='Si')
			self.entryEditarRazon.config(state=tk.NORMAL)
			razonDescarga = self.conexion('SELECT RazonDescarga FROM docente WHERE docente.Id = ? and docente.Estado = "Activo"', (id,)).fetchone()
			self.entryEditarRazon.insert(0,razonDescarga[0])		
		elif descargaAcademica[0] == 'No':
			self.DescargaAcademicaEditar.set(value='No')
			self.entryEditarRazon.config(state=tk.DISABLED)
		else:
			self.DescargaAcademicaEditar.set(value='No')
			self.entryEditarRazon.config(state=tk.DISABLED)
		condicionLaboral = self.conexion('SELECT CondicionLaboral FROM docente WHERE docente.Id = ? and docente.Estado = "Activo"', (id,)).fetchone()
		self.CondicionLaboralEditar.set(value=condicionLaboral[0])
		telefono = self.conexion('SELECT Telefono FROM docente WHERE docente.Id = ? and docente.Estado = "Activo"', (id,)).fetchone()
		self.entryEditarTelefono.insert(0,telefono[0])
		labore = self.conexion('SELECT Labore FROM docente WHERE docente.Id = ? and docente.Estado = "Activo"', (id,)).fetchone()
		if labore[0] == 'Si':
			self.laboraEditar.set(value='Si')
			self.entryEditarEspecifique.config(state=tk.NORMAL)
			especifique = self.conexion('SELECT Especifique FROM docente WHERE docente.Id = ? and docente.Estado = "Activo"', (id,)).fetchone()
			self.entryEditarEspecifique.insert(0,especifique[0])
		elif labore[0] == 'No':
			self.laboraEditar.set(value='No')
			self.entryEditarEspecifique.config(state=tk.DISABLED)
		else:
			self.laboraEditar.set(value='No')
			self.entryEditarEspecifique.config(state=tk.DISABLED)

	def razon(self):
		if self.DescargaAcademicaEditar.get() == 'Si':
			return self.entryEditarRazon.get()
		elif self.DescargaAcademicaEditar.get() == 'No':
			return ''
		else:
			return ''

	def especifique(self):
		if self.laboraEditar.get() == 'Si':
			return self.entryEditarEspecifique.get()
		elif self.laboraEditar.get() == 'No':
			return ''
		else:
			return ''

	def condicion(self):
		if self.CondicionLaboralEditar.get() == 'Ordinario':
			return self.CondicionLaboralEditar.get()
		elif self.CondicionLaboralEditar.get() == 'Contratado':
			return self.CondicionLaboralEditar.get()
		else: 
			return ''

	def editar2(self):
		if messagebox.askyesno('actualizar','¿Desea actualizar la data?'):
			self.conexion('UPDATE docente SET NombreApellido = ?, Categoria = ?, Dedicacion = ?, Pregrado = ?, Postgrado = ?, DescargaAcademica = ?, CondicionLaboral = ?, RazonDescarga = ?, Telefono = ?, Labore = ?, Especifique = ? WHERE docente.Id = ? and docente.Estado = "Activo"',(self.entryEditarNombre.get(), self.entryEditarCategoria.get(),self.entryEditarDedicación.get(),self.entryEditarTpregado.get(),self.entryEditarTposgrado.get(),self.DescargaAcademicaEditar.get(),self.condicion(),self.razon(),self.entryEditarTelefono.get(),self.laboraEditar.get(),self.especifique(),self.seleccion))
			messagebox.showinfo(title='Info', message='Data actualizada.')
			self.new.destroy()

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
			self.treeLaboratorio.state(('disabled',))
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
			self.laboratorio.set(value='No')
			ttk.Radiobutton(self.frameCheckButton, text='Si', value='Si',variable=self.laboratorio, command=self.laboratorioSi).grid(column=0,row=1)
			ttk.Radiobutton(self.frameCheckButton, text='No', value='No',variable=self.laboratorio, command=self.laboratorioNo).grid(column=1,row=1)
   

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
			ttk.Button(self.frameGestionar, text='DESHABILITAR MATERIA', command=self.eliminarMateria).grid(row=2,column=0,sticky = tk.W + tk.E)
			
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

	def laboratorioSi(self):
		self.treeLaboratorio.state(('!disabled',))

	def laboratorioNo(self):
		self.treeLaboratorio.state(('disabled',))

	def MostrarDatosGestionar(self):
		self.limpiarTabla(self.treeGestionar)
		self.query = ("SELECT materias_asignadas.Id ,docente.NombreApellido, lapso_academico.LapsoAcademico, cohorte.Cohorte, trayecto.Trayecto, trimestre.Trimestre, seccion.Seccion, modalidad.Turno,semana.Dia, hora_inicial.Hora, hora_final.Hora, unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN docente ON  docente.Id = materias_asignadas.Id_docente INNER JOIN lapso_academico ON  lapso_academico.Id = materias_asignadas.Id_lapso_academico INNER JOIN cohorte ON  cohorte.Id = materias_asignadas.Id_cohorte INNER JOIN trayecto ON trayecto.Id = materias_asignadas.Id_trayecto INNER JOIN trimestre ON trimestre.Id = materias_asignadas.Id_trimestre INNER JOIN seccion ON seccion.Id = materias_asignadas.Id_seccion INNER JOIN modalidad ON modalidad.Id = materias_asignadas.Id_modalidad INNER JOIN semana ON semana.Id = materias_asignadas.Id_semana INNER JOIN hora_inicial ON hora_inicial.Id = materias_asignadas.Id_hora_inicial INNER JOIN hora_final ON hora_final.Id = materias_asignadas.Id_hora_final INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? and materias_asignadas.Estado = 'Activo'")
		self.parametros = self.seleccion
		self.mostrar =  self.conexion(self.query, (self.parametros,))
		self.rows = self.mostrar.fetchall()
		for row in self.rows:
			self.treeGestionar.insert('',tk.END,values=row)

	def MostrarLapsoAcademico(self):
		self.limpiarTabla(self.treeLapsoAcademico)
		self.rows = self.TraerDatos("SELECT * FROM lapso_academico WHERE lapso_academico.Estado = 'Activo'")
		for row in self.rows:
			self.treeLapsoAcademico.insert('',tk.END,values=row)
	
	def MostrarCohorte(self):
		self.limpiarTabla(self.treeCohorte)
		self.rows = self.TraerDatos("SELECT * FROM cohorte WHERE cohorte.Estado = 'Activo'")
		for row in self.rows:
			self.treeCohorte.insert('',tk.END,values=row)

	def MostrarTrayecto(self):
		self.limpiarTabla(self.treeTrayecto)
		self.rows = self.TraerDatos("SELECT * FROM trayecto WHERE trayecto.Estado = 'Activo'")
		for row in self.rows:
			self.treeTrayecto.insert('',tk.END,values=row)

	def MostrarTrimestre(self):
		self.limpiarTabla(self.treeTrimestre)
		self.rows = self.TraerDatos("SELECT * FROM trimestre WHERE trimestre.Estado = 'Activo'")
		for row in self.rows:
			self.treeTrimestre.insert('',tk.END,values=row)

	def MostrarSeccion(self):
		self.limpiarTabla(self.treeSeccion)
		self.rows = self.TraerDatos("SELECT * FROM seccion WHERE seccion.Estado = 'Activo'")
		for row in self.rows:
			self.treeSeccion.insert('',tk.END,values=row)

	def MostrarTurno(self):
		self.limpiarTabla(self.treeTurno)
		self.rows = self.TraerDatos("SELECT * FROM modalidad WHERE modalidad.Estado = 'Activo'")
		for row in self.rows:
			self.treeTurno.insert('',tk.END,values=row)

	def MostrarDia(self):
		self.limpiarTabla(self.treeDia)
		self.rows = self.TraerDatos("SELECT * FROM semana WHERE semana.Estado = 'Activo'")
		for row in self.rows:
			self.treeDia.insert('',tk.END,values=row)

	def MostrarHoraInicial(self):
		self.limpiarTabla(self.treeHoraInicial)
		self.rows = self.TraerDatos("SELECT * FROM hora_inicial WHERE hora_inicial.Estado = 'Activo'")
		for row in self.rows:
			self.treeHoraInicial.insert('',tk.END,values=row)

	def MostrarHoraFinal(self):
		self.limpiarTabla(self.treeHoraFinal)
		self.rows = self.TraerDatos("SELECT * FROM hora_final WHERE hora_final.Estado = 'Activo'")
		for row in self.rows:
			self.treeHoraFinal.insert('',tk.END,values=row)

	def MostrarUnidadCurricular(self):
		self.limpiarTabla(self.treeUnidadCurricular)
		self.rows = self.TraerDatos("SELECT Id,UnidadCurricular,Hora,Departamento,Pt FROM unidad_curricular WHERE unidad_curricular.Estado = 'Activo' ORDER BY UnidadCurricular")
		for row in self.rows:
			self.treeUnidadCurricular.insert('',tk.END,values=row)

	def MostrarLaboratorio(self):
		self.limpiarTabla(self.treeLaboratorio)
		self.rows = self.TraerDatos("SELECT * FROM laboratorio WHERE laboratorio.Estado = 'Activo'")
		for row in self.rows:
			self.treeLaboratorio.insert('',tk.END,values=row)

	def obtenerHoraMateria(self):
		data = self.conexion('SELECT unidad_curricular.Hora FROM unidad_curricular WHERE unidad_curricular.Id = ? and unidad_curricular.Estado = "Activo"',(self.selecionarFilaUnidadCurricular(),)).fetchone()
		return data[0]

	def obtenerHoraInicial(self):
		data = self.conexion('SELECT hora_inicial.Id FROM hora_inicial WHERE hora_inicial.Id = ? and hora_inicial.Estado = "Activo"',(self.selecionarFilaHoraInicial(),)).fetchone()
		return data[0]

	def obtenerHoraFinal(self):
		data = self.conexion('SELECT hora_final.Id FROM hora_final WHERE hora_final.Id = ? and hora_final.Estado = "Activo"',(self.selecionarFilaHoraFinal(),)).fetchone()
		return data[0]

	def maximo(self):
		data = self.conexion('SELECT count(lapso_academico.LapsoAcademico) FROM materias_asignadas INNER JOIN lapso_academico ON lapso_academico.Id = materias_asignadas.Id_lapso_academico WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? and materias_asignadas.Estado = "Activo"',(self.seleccion,self.selecionarFilaLapsoAcademico())).fetchone()
		return data[0]				

	def registrarMateria(self):
		if self.treeLapsoAcademico.selection() and self.treeCohorte.selection() and self.treeTrayecto.selection() and self.treeTrimestre.selection() and self.treeSeccion.selection() and self.treeTurno.selection() and self.treeDia.selection and self.treeHoraInicial.selection() and self.treeHoraFinal.selection() and self.treeUnidadCurricular.selection():
			if messagebox.askyesno('Registrar','¿Añadir selección?'):
				mostrar =  self.conexion("SELECT materias_asignadas.Id ,docente.NombreApellido, lapso_academico.LapsoAcademico,cohorte.Cohorte, trayecto.Trayecto, trimestre.Trimestre, seccion.Seccion, modalidad.Turno, semana.Dia, hora_inicial.Hora, hora_final.Hora, unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN docente ON  docente.Id = materias_asignadas.Id_docente  INNER JOIN lapso_academico ON  lapso_academico.Id = materias_asignadas.Id_lapso_academico INNER JOIN cohorte ON  cohorte.Id = materias_asignadas.Id_cohorte INNER JOIN trayecto ON trayecto.Id = materias_asignadas.Id_trayecto INNER JOIN trimestre ON trimestre.Id = materias_asignadas.Id_trimestre INNER JOIN seccion ON seccion.Id = materias_asignadas.Id_seccion INNER JOIN modalidad ON modalidad.Id = materias_asignadas.Id_modalidad INNER JOIN semana ON semana.Id = materias_asignadas.Id_semana INNER JOIN hora_inicial ON hora_inicial.Id = materias_asignadas.Id_hora_inicial INNER JOIN hora_final ON hora_final.Id = materias_asignadas.Id_hora_final INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_semana = ? AND materias_asignadas.Id_hora_inicial = ? AND materias_asignadas.Id_hora_final = ? AND materias_asignadas.Id_unidad_curricular = ? AND materias_asignadas.Estado = 'Activo'",(self.seleccion,self.selecionarFilaLapsoAcademico(),self.selecionarFilaCohorte(),self.selecionarFilaTrayecto(),self.selecionarFilaTrimestre(),self.selecionarFilaSeccion(),self.selecionarFilaTurno(),self.selecionarFilaDia(),self.selecionarFilaHoraInicial(),self.selecionarFilaHoraFinal(),self.selecionarFilaUnidadCurricular())).fetchall()
				if mostrar:
					messagebox.showwarning(title='warning', message="Registro ya exixte")	
				else:
					same = self.conexion('SELECT lapso_academico.LapsoAcademico, cohorte.Cohorte, trayecto.Trayecto, trimestre.Trimestre, seccion.Seccion, modalidad.Turno, semana.Dia, hora_inicial.Hora, hora_final.Hora, unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN lapso_academico ON  lapso_academico.Id = materias_asignadas.Id_lapso_academico INNER JOIN cohorte ON  cohorte.Id = materias_asignadas.Id_cohorte INNER JOIN trayecto ON trayecto.Id = materias_asignadas.Id_trayecto INNER JOIN trimestre ON trimestre.Id = materias_asignadas.Id_trimestre INNER JOIN seccion ON seccion.Id = materias_asignadas.Id_seccion INNER JOIN modalidad ON modalidad.Id = materias_asignadas.Id_modalidad INNER JOIN semana ON semana.Id = materias_asignadas.Id_semana INNER JOIN hora_inicial ON hora_inicial.Id = materias_asignadas.Id_hora_inicial INNER JOIN hora_final ON hora_final.Id = materias_asignadas.Id_hora_final INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_semana = ? AND materias_asignadas.Id_hora_inicial = ? AND materias_asignadas.Id_hora_final = ? AND materias_asignadas.Id_unidad_curricular = ? AND materias_asignadas.Estado = "Activo"',(self.selecionarFilaLapsoAcademico(),self.selecionarFilaCohorte(),self.selecionarFilaTrayecto(),self.selecionarFilaTrimestre(),self.selecionarFilaSeccion(),self.selecionarFilaTurno(),self.selecionarFilaDia(),self.selecionarFilaHoraInicial(),self.selecionarFilaHoraFinal(),self.selecionarFilaUnidadCurricular())).fetchall()
					if same:
						messagebox.showwarning(title='warning', message="Este registro ya le pertenece a otro docente")	
					else:
						validarMateria = self.conexion('SELECT materias_asignadas.Id ,docente.NombreApellido, lapso_academico.LapsoAcademico,cohorte.Cohorte, trayecto.Trayecto, trimestre.Trimestre, seccion.Seccion, modalidad.Turno, semana.Dia, hora_inicial.Hora, hora_final.Hora FROM materias_asignadas INNER JOIN docente ON  docente.Id = materias_asignadas.Id_docente INNER JOIN lapso_academico ON  lapso_academico.Id = materias_asignadas.Id_lapso_academico INNER JOIN cohorte ON  cohorte.Id = materias_asignadas.Id_cohorte INNER JOIN trayecto ON trayecto.Id = materias_asignadas.Id_trayecto INNER JOIN trimestre ON trimestre.Id = materias_asignadas.Id_trimestre INNER JOIN seccion ON seccion.Id = materias_asignadas.Id_seccion  INNER JOIN modalidad ON modalidad.Id = materias_asignadas.Id_modalidad INNER JOIN semana ON semana.Id = materias_asignadas.Id_semana  INNER JOIN hora_inicial ON hora_inicial.Id = materias_asignadas.Id_hora_inicial  INNER JOIN hora_final ON hora_final.Id = materias_asignadas.Id_hora_final  WHERE  materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_cohorte = ? AND  materias_asignadas.Id_trayecto = ? AND  materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND  materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_semana = ? AND  materias_asignadas.Id_hora_inicial = ? AND  materias_asignadas.Id_hora_final = ? AND materias_asignadas.Estado = "Activo"',(self.seleccion,self.selecionarFilaLapsoAcademico(),self.selecionarFilaCohorte(),self.selecionarFilaTrayecto(),self.selecionarFilaTrimestre(),self.selecionarFilaSeccion(),self.selecionarFilaTurno(),self.selecionarFilaDia(),self.selecionarFilaHoraInicial(),self.selecionarFilaHoraFinal())).fetchall()
						if validarMateria:
							messagebox.showwarning(title='warning', message="No puede inscribir otra materia en este registro")	
						else:
							validarMateriaOtroDocente = self.conexion('SELECT materias_asignadas.Id ,lapso_academico.LapsoAcademico, cohorte.Cohorte, trayecto.Trayecto, trimestre.Trimestre, seccion.Seccion, modalidad.Turno, semana.Dia, hora_inicial.Hora, hora_final.Hora FROM materias_asignadas INNER JOIN lapso_academico ON  lapso_academico.Id = materias_asignadas.Id_lapso_academico INNER JOIN cohorte ON  cohorte.Id = materias_asignadas.Id_cohorte INNER JOIN trayecto ON trayecto.Id = materias_asignadas.Id_trayecto INNER JOIN trimestre ON trimestre.Id = materias_asignadas.Id_trimestre INNER JOIN seccion ON seccion.Id = materias_asignadas.Id_seccion  INNER JOIN modalidad ON modalidad.Id = materias_asignadas.Id_modalidad INNER JOIN semana ON semana.Id = materias_asignadas.Id_semana  INNER JOIN hora_inicial ON hora_inicial.Id = materias_asignadas.Id_hora_inicial  INNER JOIN hora_final ON hora_final.Id = materias_asignadas.Id_hora_final  WHERE  materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_cohorte = ? AND  materias_asignadas.Id_trayecto = ? AND  materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND  materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_semana = ? AND  materias_asignadas.Id_hora_inicial = ? AND  materias_asignadas.Id_hora_final = ? AND materias_asignadas.Estado = "Activo"',(self.selecionarFilaLapsoAcademico(),self.selecionarFilaCohorte(),self.selecionarFilaTrayecto(),self.selecionarFilaTrimestre(),self.selecionarFilaSeccion(),self.selecionarFilaTurno(),self.selecionarFilaDia(),self.selecionarFilaHoraInicial(),self.selecionarFilaHoraFinal())).fetchall()
							if validarMateriaOtroDocente:
								messagebox.showwarning(title='warning', message="Este registro ya le pertenece a otro docente")
							else:	
								if self.laboratorio.get() == 'Si':
									if self.treeLaboratorio.selection():
										if self.maximo() == 10:
											messagebox.showinfo(title='info', message='Limite de materias asignadas por lapso academico excedido')
										else:	
											if self.obtenerHoraMateria() == '6':
												# BLOQUE 6
												# Horario Mañana
												if self.obtenerHoraInicial() == 1 and self.obtenerHoraFinal() == 2:
													self.registrarSi()
												elif self.obtenerHoraInicial() == 2 and self.obtenerHoraFinal() == 3:
													self.registrarSi()
												elif self.obtenerHoraInicial() == 3 and self.obtenerHoraFinal() == 4:
													self.registrarSi()
												elif self.obtenerHoraInicial() == 4 and self.obtenerHoraFinal() == 5:
													self.registrarSi()
												elif self.obtenerHoraInicial() == 5 and self.obtenerHoraFinal() == 6:
													self.registrarSi()
												# Horario Tarde
												elif self.obtenerHoraInicial() == 7 and self.obtenerHoraFinal() == 8:
													self.registrarSi()
												elif self.obtenerHoraInicial() == 8 and self.obtenerHoraFinal() == 9:
													self.registrarSi()
												elif self.obtenerHoraInicial() == 9 and self.obtenerHoraFinal() == 10:
													self.registrarSi()
												elif self.obtenerHoraInicial() == 10 and self.obtenerHoraFinal() == 11:
													self.registrarSi()
												elif self.obtenerHoraInicial() == 11 and self.obtenerHoraFinal() == 12:
													self.registrarSi()
												# Horario Noche
												elif self.obtenerHoraInicial() == 13 and self.obtenerHoraFinal() == 14:
													self.registrarSi()
												elif self.obtenerHoraInicial() == 14 and self.obtenerHoraFinal() == 15:
													self.registrarSi()
												elif self.obtenerHoraInicial() == 15 and self.obtenerHoraFinal() == 16:
													self.registrarSi()
												elif self.obtenerHoraInicial() == 16 and self.obtenerHoraFinal() == 17:
													self.registrarSi()
												elif self.obtenerHoraInicial() == 17 and self.obtenerHoraFinal() == 18:
													self.registrarSi()
													# BLOQUE 3
												elif self.obtenerHoraInicial() == 1 and self.obtenerHoraFinal() == 3:
													self.registrarSi()
												elif self.obtenerHoraInicial() == 2 and self.obtenerHoraFinal() == 4:
													self.registrarSi()
												elif self.obtenerHoraInicial() == 3 and self.obtenerHoraFinal() == 5:
													self.registrarSi()
												elif self.obtenerHoraInicial() == 4 and self.obtenerHoraFinal() == 6:
													self.registrarSi()
												elif self.obtenerHoraInicial() == 7 and self.obtenerHoraFinal() == 9:
													self.registrarSi()
												elif self.obtenerHoraInicial() == 8 and self.obtenerHoraFinal() == 10:
													self.registrarSi()
												elif self.obtenerHoraInicial() == 9 and self.obtenerHoraFinal() == 11:
													self.registrarSi()
												elif self.obtenerHoraInicial() == 10 and self.obtenerHoraFinal() == 12:
													self.registrarSi()												
												elif self.obtenerHoraInicial() == 13 and self.obtenerHoraFinal() == 15:
													self.registrarSi()
												elif self.obtenerHoraInicial() == 14 and self.obtenerHoraFinal() == 16:
													self.registrarSi()
												elif self.obtenerHoraInicial() == 15 and self.obtenerHoraFinal() == 17:
													self.registrarSi()
												elif self.obtenerHoraInicial() == 16 and self.obtenerHoraFinal() == 18:
													self.registrarSi()											
													#  BLOQUE 4
												elif self.obtenerHoraInicial() == 1 and self.obtenerHoraFinal() == 4:
													self.registrarSi()												
												elif self.obtenerHoraInicial() == 2 and self.obtenerHoraFinal() == 5:
													self.registrarSi()
												elif self.obtenerHoraInicial() == 3 and self.obtenerHoraFinal() == 6:
													self.registrarSi()
												elif self.obtenerHoraInicial() == 7 and self.obtenerHoraFinal() == 10:
													self.registrarSi()
												elif self.obtenerHoraInicial() == 8 and self.obtenerHoraFinal() == 11:
													self.registrarSi()
												elif self.obtenerHoraInicial() == 9 and self.obtenerHoraFinal() == 12:
													self.registrarSi()
												elif self.obtenerHoraInicial() == 13 and self.obtenerHoraFinal() == 16:
													self.registrarSi()
												elif self.obtenerHoraInicial() == 14 and self.obtenerHoraFinal() == 17:
													self.registrarSi()
												elif self.obtenerHoraInicial() == 15 and self.obtenerHoraFinal() == 18:
													self.registrarSi()
												# BLOQUE 6  
												elif self.obtenerHoraInicial() == 1 and self.obtenerHoraFinal() == 6:
													self.registrarSi()
												elif self.obtenerHoraInicial() == 7 and self.obtenerHoraFinal() == 12:
													self.registrarSi()
												elif self.obtenerHoraInicial() == 13 and self.obtenerHoraFinal() == 18:
													self.registrarSi()
												else:
													messagebox.showinfo(title='info', message='Hora no permitida')
											elif self.obtenerHoraMateria() == '5':
												# BLOQUE 2
												# Horario Mañana
												if self.obtenerHoraInicial() == 1 and self.obtenerHoraFinal() == 2:
													self.registrarSi()
												elif self.obtenerHoraInicial() == 2 and self.obtenerHoraFinal() == 3:
													self.registrarSi()
												elif self.obtenerHoraInicial() == 3 and self.obtenerHoraFinal() == 4:
													self.registrarSi()
												elif self.obtenerHoraInicial() == 4 and self.obtenerHoraFinal() == 5:
													self.registrarSi()
												elif self.obtenerHoraInicial() == 5 and self.obtenerHoraFinal() == 6:
													self.registrarSi()
												# Horario Tarde
												elif self.obtenerHoraInicial() == 7 and self.obtenerHoraFinal() == 8:
													self.registrarSi()
												elif self.obtenerHoraInicial() == 8 and self.obtenerHoraFinal() == 9:
													self.registrarSi()
												elif self.obtenerHoraInicial() == 9 and self.obtenerHoraFinal() == 10:
													self.registrarSi()
												elif self.obtenerHoraInicial() == 10 and self.obtenerHoraFinal() == 11:
													self.registrarSi()
												elif self.obtenerHoraInicial() == 11 and self.obtenerHoraFinal() == 12:
													self.registrarSi()
												# Horario Noche
												elif self.obtenerHoraInicial() == 13 and self.obtenerHoraFinal() == 14:
													self.registrarSi()
												elif self.obtenerHoraInicial() == 14 and self.obtenerHoraFinal() == 15:
													self.registrarSi()
												elif self.obtenerHoraInicial() == 15 and self.obtenerHoraFinal() == 16:
													self.registrarSi()
												elif self.obtenerHoraInicial() == 16 and self.obtenerHoraFinal() == 17:
													self.registrarSi()
												elif self.obtenerHoraInicial() == 17 and self.obtenerHoraFinal() == 18:
													self.registrarSi()
												# BLOQUE 3
												# Horario Mañana
												elif self.obtenerHoraInicial() == 1 and self.obtenerHoraFinal() == 3:
													self.registrarSi()
												elif self.obtenerHoraInicial() == 2 and self.obtenerHoraFinal() == 4:
													self.registrarSi()
												elif self.obtenerHoraInicial() == 3 and self.obtenerHoraFinal() == 5:
													self.registrarSi()
												elif self.obtenerHoraInicial() == 4 and self.obtenerHoraFinal() == 6:
													self.registrarSi()
												elif self.obtenerHoraInicial() == 7 and self.obtenerHoraFinal() == 9:
													self.registrarSi()
												elif self.obtenerHoraInicial() == 8 and self.obtenerHoraFinal() == 10:
													self.registrarSi()
												elif self.obtenerHoraInicial() == 9 and self.obtenerHoraFinal() == 11:
													self.registrarSi()
												elif self.obtenerHoraInicial() == 10 and self.obtenerHoraFinal() == 12:
													self.registrarSi()												
												elif self.obtenerHoraInicial() == 13 and self.obtenerHoraFinal() == 15:
													self.registrarSi()
												elif self.obtenerHoraInicial() == 14 and self.obtenerHoraFinal() == 16:
													self.registrarSi()
												elif self.obtenerHoraInicial() == 15 and self.obtenerHoraFinal() == 17:
													self.registrarSi()
												elif self.obtenerHoraInicial() == 16 and self.obtenerHoraFinal() == 18:
													self.registrarSi()
												# BLOQUE 5
												elif self.obtenerHoraInicial() == 1 and self.obtenerHoraFinal() == 5:
													self.registrarSi()
												elif self.obtenerHoraInicial() == 2 and self.obtenerHoraFinal() == 6:
													self.registrarSi()
												elif self.obtenerHoraInicial() == 7 and self.obtenerHoraFinal() == 11:
													self.registrarSi()
												elif self.obtenerHoraInicial() == 8 and self.obtenerHoraFinal() == 12:
													self.registrarSi()
												elif self.obtenerHoraInicial() == 13 and self.obtenerHoraFinal() == 17:
													self.registrarSi()
												elif self.obtenerHoraInicial() == 14 and self.obtenerHoraFinal() == 18:
													self.registrarSi()
												else:
													messagebox.showinfo(title='info', message='Hora no permitida')
											elif self.obtenerHoraMateria() == '4':
												# BLOQUE 2
												# Horario Mañana
												if self.obtenerHoraInicial() == 1 and self.obtenerHoraFinal() == 2:
													self.registrarSi()
												elif self.obtenerHoraInicial() == 2 and self.obtenerHoraFinal() == 3:
													self.registrarSi()
												elif self.obtenerHoraInicial() == 3 and self.obtenerHoraFinal() == 4:
													self.registrarSi()
												elif self.obtenerHoraInicial() == 4 and self.obtenerHoraFinal() == 5:
													self.registrarSi()
												elif self.obtenerHoraInicial() == 5 and self.obtenerHoraFinal() == 6:
													self.registrarSi()
												# Horario Tarde
												elif self.obtenerHoraInicial() == 7 and self.obtenerHoraFinal() == 8:
													self.registrarSi()
												elif self.obtenerHoraInicial() == 8 and self.obtenerHoraFinal() == 9:
													self.registrarSi()
												elif self.obtenerHoraInicial() == 9 and self.obtenerHoraFinal() == 10:
													self.registrarSi()
												elif self.obtenerHoraInicial() == 10 and self.obtenerHoraFinal() == 11:
													self.registrarSi()
												elif self.obtenerHoraInicial() == 11 and self.obtenerHoraFinal() == 12:
													self.registrarSi()
												# Horario Noche
												elif self.obtenerHoraInicial() == 13 and self.obtenerHoraFinal() == 14:
													self.registrarSi()
												elif self.obtenerHoraInicial() == 14 and self.obtenerHoraFinal() == 15:
													self.registrarSi()
												elif self.obtenerHoraInicial() == 15 and self.obtenerHoraFinal() == 16:
													self.registrarSi()
												elif self.obtenerHoraInicial() == 16 and self.obtenerHoraFinal() == 17:
													self.registrarSi()
												elif self.obtenerHoraInicial() == 17 and self.obtenerHoraFinal() == 18:
													self.registrarSi()												
													# BLOQUE 4
												elif self.obtenerHoraInicial() == 1 and self.obtenerHoraFinal() == 4:
													self.registrarSi()												
												elif self.obtenerHoraInicial() == 2 and self.obtenerHoraFinal() == 5:
													self.registrarSi()
												elif self.obtenerHoraInicial() == 3 and self.obtenerHoraFinal() == 6:
													self.registrarSi()
												elif self.obtenerHoraInicial() == 7 and self.obtenerHoraFinal() == 10:
													self.registrarSi()
												elif self.obtenerHoraInicial() == 8 and self.obtenerHoraFinal() == 11:
													self.registrarSi()
												elif self.obtenerHoraInicial() == 9 and self.obtenerHoraFinal() == 12:
													self.registrarSi()
												elif self.obtenerHoraInicial() == 13 and self.obtenerHoraFinal() == 16:
													self.registrarSi()
												elif self.obtenerHoraInicial() == 14 and self.obtenerHoraFinal() == 17:
													self.registrarSi()
												elif self.obtenerHoraInicial() == 15 and self.obtenerHoraFinal() == 18:
													self.registrarSi()
												else:
													messagebox.showinfo(title='info', message='Hora no permitida')
											elif self.obtenerHoraMateria() == '3':
												# Horario Mañana
												if self.obtenerHoraInicial() == 1 and self.obtenerHoraFinal() == 3:
													self.registrarSi()
												elif self.obtenerHoraInicial() == 2 and self.obtenerHoraFinal() == 4:
													self.registrarSi()
												elif self.obtenerHoraInicial() == 3 and self.obtenerHoraFinal() == 5:
													self.registrarSi()
												elif self.obtenerHoraInicial() == 4 and self.obtenerHoraFinal() == 6:
													self.registrarSi()
												elif self.obtenerHoraInicial() == 7 and self.obtenerHoraFinal() == 9:
													self.registrarSi()
												elif self.obtenerHoraInicial() == 8 and self.obtenerHoraFinal() == 10:
													self.registrarSi()
												elif self.obtenerHoraInicial() == 9 and self.obtenerHoraFinal() == 11:
													self.registrarSi()
												elif self.obtenerHoraInicial() == 10 and self.obtenerHoraFinal() == 12:
													self.registrarSi()												
												elif self.obtenerHoraInicial() == 13 and self.obtenerHoraFinal() == 15:
													self.registrarSi()
												elif self.obtenerHoraInicial() == 14 and self.obtenerHoraFinal() == 16:
													self.registrarSi()
												elif self.obtenerHoraInicial() == 15 and self.obtenerHoraFinal() == 17:
													self.registrarSi()
												elif self.obtenerHoraInicial() == 16 and self.obtenerHoraFinal() == 18:
													self.registrarSi()
												else:
													messagebox.showinfo(title='info', message='Hora no permitida')
											elif self.obtenerHoraMateria() == '2':
												# Horario Mañana
												if self.obtenerHoraInicial() == 1 and self.obtenerHoraFinal() == 2:
													self.registrarSi()
												elif self.obtenerHoraInicial() == 2 and self.obtenerHoraFinal() == 3:
													self.registrarSi()
												elif self.obtenerHoraInicial() == 3 and self.obtenerHoraFinal() == 4:
													self.registrarSi()
												elif self.obtenerHoraInicial() == 4 and self.obtenerHoraFinal() == 5:
													self.registrarSi()
												elif self.obtenerHoraInicial() == 5 and self.obtenerHoraFinal() == 6:
													self.registrarSi()
												# Horario Tarde
												elif self.obtenerHoraInicial() == 7 and self.obtenerHoraFinal() == 8:
													self.registrarSi()
												elif self.obtenerHoraInicial() == 8 and self.obtenerHoraFinal() == 9:
													self.registrarSi()
												elif self.obtenerHoraInicial() == 9 and self.obtenerHoraFinal() == 10:
													self.registrarSi()
												elif self.obtenerHoraInicial() == 10 and self.obtenerHoraFinal() == 11:
													self.registrarSi()
												elif self.obtenerHoraInicial() == 11 and self.obtenerHoraFinal() == 12:
													self.registrarSi()
												# Horario Noche
												elif self.obtenerHoraInicial() == 13 and self.obtenerHoraFinal() == 14:
													self.registrarSi()
												elif self.obtenerHoraInicial() == 14 and self.obtenerHoraFinal() == 15:
													self.registrarSi()
												elif self.obtenerHoraInicial() == 15 and self.obtenerHoraFinal() == 16:
													self.registrarSi()
												elif self.obtenerHoraInicial() == 16 and self.obtenerHoraFinal() == 17:
													self.registrarSi()
												elif self.obtenerHoraInicial() == 17 and self.obtenerHoraFinal() == 18:
													self.registrarSi()
												else:
													messagebox.showinfo(title='info', message='Hora no permitida')
											elif self.obtenerHoraMateria() == ' ':
												messagebox.showinfo(title='info', message='Debe de asignarle una hora académica a esta materia, antes de añadir la materia a un docente')
									else:
										messagebox.showwarning(title='Warning', message='Seleccione un laboratorio')
								elif self.laboratorio.get() == 'No':
									if self.maximo() == 10:
										messagebox.showinfo(title='info', message='Limite de materias asignadas por lapso academico excedido')
									else:
										if self.obtenerHoraMateria() == '6':
											# BLOQUE 6
											# Horario Mañana
											if self.obtenerHoraInicial() == 1 and self.obtenerHoraFinal() == 2:
												self.registrarNo()
											elif self.obtenerHoraInicial() == 2 and self.obtenerHoraFinal() == 3:
												self.registrarNo()
											elif self.obtenerHoraInicial() == 3 and self.obtenerHoraFinal() == 4:
												self.registrarNo()
											elif self.obtenerHoraInicial() == 4 and self.obtenerHoraFinal() == 5:
												self.registrarNo()
											elif self.obtenerHoraInicial() == 5 and self.obtenerHoraFinal() == 6:
												self.registrarNo()
											# Horario Tarde
											elif self.obtenerHoraInicial() == 7 and self.obtenerHoraFinal() == 8:
												self.registrarNo()
											elif self.obtenerHoraInicial() == 8 and self.obtenerHoraFinal() == 9:
												self.registrarNo()
											elif self.obtenerHoraInicial() == 9 and self.obtenerHoraFinal() == 10:
												self.registrarNo()
											elif self.obtenerHoraInicial() == 10 and self.obtenerHoraFinal() == 11:
												self.registrarNo()
											elif self.obtenerHoraInicial() == 11 and self.obtenerHoraFinal() == 12:
												self.registrarNo()
											# Horario Noche
											elif self.obtenerHoraInicial() == 13 and self.obtenerHoraFinal() == 14:
												self.registrarNo()
											elif self.obtenerHoraInicial() == 14 and self.obtenerHoraFinal() == 15:
												self.registrarNo()
											elif self.obtenerHoraInicial() == 15 and self.obtenerHoraFinal() == 16:
												self.registrarNo()
											elif self.obtenerHoraInicial() == 16 and self.obtenerHoraFinal() == 17:
												self.registrarNo()
											elif self.obtenerHoraInicial() == 17 and self.obtenerHoraFinal() == 18:
												self.registrarNo()
											# BLOQUE 3
											elif self.obtenerHoraInicial() == 1 and self.obtenerHoraFinal() == 3:
												self.registrarNo()
											elif self.obtenerHoraInicial() == 2 and self.obtenerHoraFinal() == 4:
												self.registrarNo()
											elif self.obtenerHoraInicial() == 3 and self.obtenerHoraFinal() == 5:
												self.registrarNo()
											elif self.obtenerHoraInicial() == 4 and self.obtenerHoraFinal() == 6:
												self.registrarNo()
											elif self.obtenerHoraInicial() == 7 and self.obtenerHoraFinal() == 9:
												self.registrarNo()
											elif self.obtenerHoraInicial() == 8 and self.obtenerHoraFinal() == 10:
												self.registrarNo()
											elif self.obtenerHoraInicial() == 9 and self.obtenerHoraFinal() == 11:
												self.registrarNo()
											elif self.obtenerHoraInicial() == 10 and self.obtenerHoraFinal() == 12:
												self.registrarNo()											
											elif self.obtenerHoraInicial() == 13 and self.obtenerHoraFinal() == 15:
												self.registrarNo()
											elif self.obtenerHoraInicial() == 14 and self.obtenerHoraFinal() == 16:
												self.registrarNo()
											elif self.obtenerHoraInicial() == 15 and self.obtenerHoraFinal() == 17:
												self.registrarNo()
											elif self.obtenerHoraInicial() == 16 and self.obtenerHoraFinal() == 18:
												self.registrarNo()											
											#  BLOQUE 4
											elif self.obtenerHoraInicial() == 1 and self.obtenerHoraFinal() == 4:
												self.registrarNo()											
											elif self.obtenerHoraInicial() == 2 and self.obtenerHoraFinal() == 5:
												self.registrarNo()
											elif self.obtenerHoraInicial() == 3 and self.obtenerHoraFinal() == 6:
												self.registrarNo()
											elif self.obtenerHoraInicial() == 7 and self.obtenerHoraFinal() == 10:
												self.registrarNo()
											elif self.obtenerHoraInicial() == 8 and self.obtenerHoraFinal() == 11:
												self.registrarNo()
											elif self.obtenerHoraInicial() == 9 and self.obtenerHoraFinal() == 12:
												self.registrarNo()
											elif self.obtenerHoraInicial() == 13 and self.obtenerHoraFinal() == 16:
												self.registrarNo()
											elif self.obtenerHoraInicial() == 14 and self.obtenerHoraFinal() == 17:
												self.registrarNo()
											elif self.obtenerHoraInicial() == 15 and self.obtenerHoraFinal() == 18:
												self.registrarNo()
											# BLOQUE 6  
											elif self.obtenerHoraInicial() == 1 and self.obtenerHoraFinal() == 6:
												self.registrarNo()
											elif self.obtenerHoraInicial() == 7 and self.obtenerHoraFinal() == 12:
												self.registrarNo()
											elif self.obtenerHoraInicial() == 13 and self.obtenerHoraFinal() == 18:
												self.registrarNo()
											else:
												messagebox.showinfo(title='info', message='Hora no permitida')
										elif self.obtenerHoraMateria() == '5':
											# BLOQUE 2
											# Horario Mañana
											if self.obtenerHoraInicial() == 1 and self.obtenerHoraFinal() == 2:
												self.registrarNo()
											elif self.obtenerHoraInicial() == 2 and self.obtenerHoraFinal() == 3:
												self.registrarNo()
											elif self.obtenerHoraInicial() == 3 and self.obtenerHoraFinal() == 4:
												self.registrarNo()
											elif self.obtenerHoraInicial() == 4 and self.obtenerHoraFinal() == 5:
												self.registrarNo()
											elif self.obtenerHoraInicial() == 5 and self.obtenerHoraFinal() == 6:
												self.registrarNo()
											# Horario Tarde
											elif self.obtenerHoraInicial() == 7 and self.obtenerHoraFinal() == 8:
												self.registrarNo()
											elif self.obtenerHoraInicial() == 8 and self.obtenerHoraFinal() == 9:
												self.registrarNo()
											elif self.obtenerHoraInicial() == 9 and self.obtenerHoraFinal() == 10:
												self.registrarNo()
											elif self.obtenerHoraInicial() == 10 and self.obtenerHoraFinal() == 11:
												self.registrarNo()
											elif self.obtenerHoraInicial() == 11 and self.obtenerHoraFinal() == 12:
												self.registrarNo()
											# Horario Noche
											elif self.obtenerHoraInicial() == 13 and self.obtenerHoraFinal() == 14:
												self.registrarNo()
											elif self.obtenerHoraInicial() == 14 and self.obtenerHoraFinal() == 15:
												self.registrarNo()
											elif self.obtenerHoraInicial() == 15 and self.obtenerHoraFinal() == 16:
												self.registrarNo()
											elif self.obtenerHoraInicial() == 16 and self.obtenerHoraFinal() == 17:
												self.registrarNo()
											elif self.obtenerHoraInicial() == 17 and self.obtenerHoraFinal() == 18:
												self.registrarNo()
											# BLOQUE 3
											# Horario Mañana
											elif self.obtenerHoraInicial() == 1 and self.obtenerHoraFinal() == 3:
												self.registrarNo()
											elif self.obtenerHoraInicial() == 2 and self.obtenerHoraFinal() == 4:
												self.registrarNo()
											elif self.obtenerHoraInicial() == 3 and self.obtenerHoraFinal() == 5:
												self.registrarNo()
											elif self.obtenerHoraInicial() == 4 and self.obtenerHoraFinal() == 6:
												self.registrarNo()
											elif self.obtenerHoraInicial() == 7 and self.obtenerHoraFinal() == 9:
												self.registrarNo()
											elif self.obtenerHoraInicial() == 8 and self.obtenerHoraFinal() == 10:
												self.registrarNo()
											elif self.obtenerHoraInicial() == 9 and self.obtenerHoraFinal() == 11:
												self.registrarNo()
											elif self.obtenerHoraInicial() == 10 and self.obtenerHoraFinal() == 12:
												self.registrarNo()											
											elif self.obtenerHoraInicial() == 13 and self.obtenerHoraFinal() == 15:
												self.registrarNo()
											elif self.obtenerHoraInicial() == 14 and self.obtenerHoraFinal() == 16:
												self.registrarNo()
											elif self.obtenerHoraInicial() == 15 and self.obtenerHoraFinal() == 17:
												self.registrarNo()
											elif self.obtenerHoraInicial() == 16 and self.obtenerHoraFinal() == 18:
												self.registrarNo()
											# BLOQUE 5
											elif self.obtenerHoraInicial() == 1 and self.obtenerHoraFinal() == 5:
												self.registrarNo()
											elif self.obtenerHoraInicial() == 2 and self.obtenerHoraFinal() == 6:
												self.registrarNo()
											elif self.obtenerHoraInicial() == 7 and self.obtenerHoraFinal() == 11:
												self.registrarNo()
											elif self.obtenerHoraInicial() == 8 and self.obtenerHoraFinal() == 12:
												self.registrarNo()
											elif self.obtenerHoraInicial() == 13 and self.obtenerHoraFinal() == 17:
												self.registrarNo()
											elif self.obtenerHoraInicial() == 14 and self.obtenerHoraFinal() == 18:
												self.registrarNo()
											else:
												messagebox.showinfo(title='info', message='Hora no permitida')
										elif self.obtenerHoraMateria() == '4':
											# BLOQUE 2
											# Horario Mañana
											if self.obtenerHoraInicial() == 1 and self.obtenerHoraFinal() == 2:
												self.registrarNo()
											elif self.obtenerHoraInicial() == 2 and self.obtenerHoraFinal() == 3:
												self.registrarNo()
											elif self.obtenerHoraInicial() == 3 and self.obtenerHoraFinal() == 4:
												self.registrarNo()
											elif self.obtenerHoraInicial() == 4 and self.obtenerHoraFinal() == 5:
												self.registrarNo()
											elif self.obtenerHoraInicial() == 5 and self.obtenerHoraFinal() == 6:
												self.registrarNo()
											# Horario Tarde
											elif self.obtenerHoraInicial() == 7 and self.obtenerHoraFinal() == 8:
												self.registrarNo()
											elif self.obtenerHoraInicial() == 8 and self.obtenerHoraFinal() == 9:
												self.registrarNo()
											elif self.obtenerHoraInicial() == 9 and self.obtenerHoraFinal() == 10:
												self.registrarNo()
											elif self.obtenerHoraInicial() == 10 and self.obtenerHoraFinal() == 11:
												self.registrarNo()
											elif self.obtenerHoraInicial() == 11 and self.obtenerHoraFinal() == 12:
												self.registrarNo()
											# Horario Noche
											elif self.obtenerHoraInicial() == 13 and self.obtenerHoraFinal() == 14:
												self.registrarNo()
											elif self.obtenerHoraInicial() == 14 and self.obtenerHoraFinal() == 15:
												self.registrarNo()
											elif self.obtenerHoraInicial() == 15 and self.obtenerHoraFinal() == 16:
												self.registrarNo()
											elif self.obtenerHoraInicial() == 16 and self.obtenerHoraFinal() == 17:
												self.registrarNo()
											elif self.obtenerHoraInicial() == 17 and self.obtenerHoraFinal() == 18:
												self.registrarNo()											
												# BLOQUE 4
											elif self.obtenerHoraInicial() == 1 and self.obtenerHoraFinal() == 4:
												self.registrarNo()											
											elif self.obtenerHoraInicial() == 2 and self.obtenerHoraFinal() == 5:
												self.registrarNo()
											elif self.obtenerHoraInicial() == 3 and self.obtenerHoraFinal() == 6:
												self.registrarNo()
											elif self.obtenerHoraInicial() == 7 and self.obtenerHoraFinal() == 10:
												self.registrarNo()
											elif self.obtenerHoraInicial() == 8 and self.obtenerHoraFinal() == 11:
												self.registrarNo()
											elif self.obtenerHoraInicial() == 9 and self.obtenerHoraFinal() == 12:
												self.registrarNo()
											elif self.obtenerHoraInicial() == 13 and self.obtenerHoraFinal() == 16:
												self.registrarNo()
											elif self.obtenerHoraInicial() == 14 and self.obtenerHoraFinal() == 17:
												self.registrarNo()
											elif self.obtenerHoraInicial() == 15 and self.obtenerHoraFinal() == 18:
												self.registrarNo()
											else:
												messagebox.showinfo(title='info', message='Hora no permitida')
										elif self.obtenerHoraMateria() == '3':
											# Horario Mañana
											if self.obtenerHoraInicial() == 1 and self.obtenerHoraFinal() == 3:
												self.registrarNo()
											elif self.obtenerHoraInicial() == 2 and self.obtenerHoraFinal() == 4:
												self.registrarNo()
											elif self.obtenerHoraInicial() == 3 and self.obtenerHoraFinal() == 5:
												self.registrarNo()
											elif self.obtenerHoraInicial() == 4 and self.obtenerHoraFinal() == 6:
												self.registrarNo()
											elif self.obtenerHoraInicial() == 7 and self.obtenerHoraFinal() == 9:
												self.registrarNo()
											elif self.obtenerHoraInicial() == 8 and self.obtenerHoraFinal() == 10:
												self.registrarNo()
											elif self.obtenerHoraInicial() == 9 and self.obtenerHoraFinal() == 11:
												self.registrarNo()
											elif self.obtenerHoraInicial() == 10 and self.obtenerHoraFinal() == 12:
												self.registrarNo()											
											elif self.obtenerHoraInicial() == 13 and self.obtenerHoraFinal() == 15:
												self.registrarNo()
											elif self.obtenerHoraInicial() == 14 and self.obtenerHoraFinal() == 16:
												self.registrarNo()
											elif self.obtenerHoraInicial() == 15 and self.obtenerHoraFinal() == 17:
												self.registrarNo()
											elif self.obtenerHoraInicial() == 16 and self.obtenerHoraFinal() == 18:
												self.registrarNo()
											else:
												messagebox.showinfo(title='info', message='Hora no permitida')
										elif self.obtenerHoraMateria() == '2':
											# Horario Mañana
											if self.obtenerHoraInicial() == 1 and self.obtenerHoraFinal() == 2:
												self.registrarNo()
											elif self.obtenerHoraInicial() == 2 and self.obtenerHoraFinal() == 3:
												self.registrarNo()
											elif self.obtenerHoraInicial() == 3 and self.obtenerHoraFinal() == 4:
												self.registrarNo()
											elif self.obtenerHoraInicial() == 4 and self.obtenerHoraFinal() == 5:
												self.registrarNo()
											elif self.obtenerHoraInicial() == 5 and self.obtenerHoraFinal() == 6:	
												self.registrarNo()
											# Horario Tarde
											elif self.obtenerHoraInicial() == 7 and self.obtenerHoraFinal() == 8:
												self.registrarNo()
											elif self.obtenerHoraInicial() == 8 and self.obtenerHoraFinal() == 9:
												self.registrarNo()
											elif self.obtenerHoraInicial() == 9 and self.obtenerHoraFinal() == 10:
												self.registrarNo()
											elif self.obtenerHoraInicial() == 10 and self.obtenerHoraFinal() == 11:
												self.registrarNo()
											elif self.obtenerHoraInicial() == 11 and self.obtenerHoraFinal() == 12:
												self.registrarNo()
											# Horario Noche
											elif self.obtenerHoraInicial() == 13 and self.obtenerHoraFinal() == 14:
												self.registrarNo()
											elif self.obtenerHoraInicial() == 14 and self.obtenerHoraFinal() == 15:
												self.registrarNo()
											elif self.obtenerHoraInicial() == 15 and self.obtenerHoraFinal() == 16:
												self.registrarNo()
											elif self.obtenerHoraInicial() == 16 and self.obtenerHoraFinal() == 17:
												self.registrarNo()
											elif self.obtenerHoraInicial() == 17 and self.obtenerHoraFinal() == 18:
												self.registrarNo()
											else:
												messagebox.showinfo(title='info', message='Hora no permitida')
										elif self.obtenerHoraMateria() == ' ':
											messagebox.showinfo(title='info', message='Debe de asignarle una hora académica a esta materia, antes de añadir la materia a un docente')
								else:
									messagebox.showwarning(title='Warning', message='Debe seleccionar una opción entre las casillas de "Laboratorio"')
			else:
				self.MostrarDatosGestionar()
		else:
			messagebox.showwarning(title='Warning', message='Seleccione todas las celdas')

	def registrarNo(self):
		self.conexion("INSERT INTO materias_asignadas VALUES (NULL,?,?,?,?,?,?,?,?,?,?,?,'Activo')",(self.seleccion,self.selecionarFilaLapsoAcademico(),self.selecionarFilaCohorte(),self.selecionarFilaTrayecto(),self.selecionarFilaTrimestre(),self.selecionarFilaSeccion(),self.selecionarFilaTurno(),self.selecionarFilaDia(),self.selecionarFilaHoraInicial(),self.selecionarFilaHoraFinal(),self.selecionarFilaUnidadCurricular()))
		self.data = self.conexion('SELECT Id FROM materias_asignadas WHERE  materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_semana = ? AND  materias_asignadas.Id_hora_inicial = ? AND materias_asignadas.Id_hora_final = ? AND materias_asignadas.Id_unidad_curricular = ? AND materias_asignadas.Estado = "Activo"',(self.seleccion,self.selecionarFilaLapsoAcademico(),self.selecionarFilaCohorte(),self.selecionarFilaTrayecto(),self.selecionarFilaTrimestre(),self.selecionarFilaSeccion(),self.selecionarFilaTurno(),self.selecionarFilaDia(),self.selecionarFilaHoraInicial(),self.selecionarFilaHoraFinal(),self.selecionarFilaUnidadCurricular())).fetchone()
		self.id_materias_asignadas = self.data[0]
		self.materiaDocente = ('Cohorte ' + str(self.dataCohorte()) + ' Trayecto ' + str(self.dataTrayecto()) + ' Trimestre ' + str(self.dataTrimestre()) + ' Sección ' + str(self.dataSeccion()) + ' ' + str(self.dataUnidadCurricular()))
		self.conexion("INSERT INTO materias_docentes VALUES (NULL,?,?,?,?,?,?,?,?,'Activo')",(self.id_materias_asignadas,self.seleccion,self.selecionarFilaLapsoAcademico(),self.selecionarFilaTurno(),self.materiaDocente,self.selecionarFilaDia(),self.selecionarFilaHoraInicial(),self.selecionarFilaHoraFinal()))
		self.MostrarDatosGestionar()
		messagebox.showinfo(title='info', message='Materia registrada correctamente NO')

	def registrarSi(self):
		self.conexion("INSERT INTO materias_asignadas VALUES (NULL,?,?,?,?,?,?,?,?,?,?,?,'Activo')",(self.seleccion,self.selecionarFilaLapsoAcademico(),self.selecionarFilaCohorte(),self.selecionarFilaTrayecto(),self.selecionarFilaTrimestre(),self.selecionarFilaSeccion(),self.selecionarFilaTurno(),self.selecionarFilaDia(),self.selecionarFilaHoraInicial(),self.selecionarFilaHoraFinal(),self.selecionarFilaUnidadCurricular()))
		self.data = self.conexion('SELECT Id FROM materias_asignadas WHERE  materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto  = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_semana = ? AND  materias_asignadas.Id_hora_inicial = ? AND materias_asignadas.Id_hora_final = ? AND materias_asignadas.Id_unidad_curricular = ? AND materias_asignadas.Estado = "Activo"',(self.seleccion,self.selecionarFilaLapsoAcademico(),self.selecionarFilaCohorte(),self.selecionarFilaTrayecto(),self.selecionarFilaTrimestre(),self.selecionarFilaSeccion(),self.selecionarFilaTurno(),self.selecionarFilaDia(),self.selecionarFilaHoraInicial(),self.selecionarFilaHoraFinal(),self.selecionarFilaUnidadCurricular())).fetchone()
		self.id_materias_asignadas = self.data[0]
		self.materiaDocente = ('Cohorte ' + str(self.dataCohorte()) + ' Trayecto ' + str(self.dataTrayecto()) + ' Trimestre ' + str(self.dataTrimestre()) + ' Sección ' + str(self.dataSeccion()) + ' ' + str(self.dataUnidadCurricular()))
		self.conexion("INSERT INTO materias_docentes VALUES (NULL,?,?,?,?,?,?,?,?,'Activo')",(self.id_materias_asignadas,self.seleccion,self.selecionarFilaLapsoAcademico(),self.selecionarFilaTurno(),self.materiaDocente,self.selecionarFilaDia(),self.selecionarFilaHoraInicial(),self.selecionarFilaHoraFinal()))
		self.conexion('INSERT INTO materias_laboratorios VALUES (NULL,?,?,?,?,?,?,?,?,?,"Activo")',(self.id_materias_asignadas,self.seleccion,self.selecionarFilaLaboratorio(),self.selecionarFilaLapsoAcademico(),self.selecionarFilaTurno(),self.materiaDocente,self.selecionarFilaDia(),self.selecionarFilaHoraInicial(),self.selecionarFilaHoraFinal()))
		self.MostrarDatosGestionar()
		messagebox.showinfo(title='info', message='Materia registrada  SI')

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
			if messagebox.askyesno('Deshabilitar','¿Desea deshabilitar la materia selecionada?'):
				self.query = 'UPDATE materias_asignadas SET Estado = "Inactivo" WHERE materias_asignadas.Id = ? AND materias_asignadas.Estado = "Activo"'
				self.parametros = self.selecionarFilaGestionar()
				self.conexion(self.query, (self.parametros,))
				self.query1 = 'UPDATE materias_docentes SET Estado = "Inactivo" WHERE materias_docentes.Id_materias_asignadas = ? AND materias_docentes.Estado = "Activo"'
				self.conexion(self.query1, (self.parametros,))
				self.query2 = 'UPDATE materias_laboratorios SET Estado = "Inactivo" WHERE materias_laboratorios.Id_materias_asignadas = ? AND materias_laboratorios.Estado = "Activo"'
				self.conexion(self.query2, (self.parametros,))
				self.MostrarDatosGestionar()
				messagebox.showinfo(title='Info', message='Materia deshabilitada correctamente.')
			else:
				self.MostrarDatosGestionar()
		else:
			messagebox.showwarning(title='Wanning', message='Seleccione una materia a deshabilitar.')
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
					mostrar =  self.conexion("SELECT materias_asignadas.Id ,docente.NombreApellido, lapso_academico.LapsoAcademico,cohorte.Cohorte, trayecto.Trayecto, trimestre.Trimestre, seccion.Seccion, modalidad.Turno, semana.Dia, hora_inicial.Hora, hora_final.Hora, unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN docente ON  docente.Id = materias_asignadas.Id_docente  INNER JOIN lapso_academico ON  lapso_academico.Id = materias_asignadas.Id_lapso_academico INNER JOIN cohorte ON  cohorte.Id = materias_asignadas.Id_cohorte INNER JOIN trayecto ON trayecto.Id = materias_asignadas.Id_trayecto INNER JOIN trimestre ON trimestre.Id = materias_asignadas.Id_trimestre INNER JOIN seccion ON seccion.Id = materias_asignadas.Id_seccion INNER JOIN modalidad ON modalidad.Id = materias_asignadas.Id_modalidad INNER JOIN semana ON semana.Id = materias_asignadas.Id_semana INNER JOIN hora_inicial ON hora_inicial.Id = materias_asignadas.Id_hora_inicial INNER JOIN hora_final ON hora_final.Id = materias_asignadas.Id_hora_final INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_semana = ? AND materias_asignadas.Id_hora_inicial = ? AND materias_asignadas.Id_hora_final = ? AND materias_asignadas.Id_unidad_curricular = ? AND materias_asignadas.Estado = 'Activo'",(self.seleccion,self.selecionarFilaLapsoAcademico(),self.selecionarFilaCohorte(),self.selecionarFilaTrayecto(),self.selecionarFilaTrimestre(),self.selecionarFilaSeccion(),self.selecionarFilaTurno(),self.selecionarFilaDia(),self.selecionarFilaHoraInicial(),self.selecionarFilaHoraFinal(),self.selecionarFilaUnidadCurricular())).fetchall()
					if mostrar:
						messagebox.showwarning(title='warning', message="Registro ya exixte")	
					else:
						same = self.conexion('SELECT lapso_academico.LapsoAcademico, cohorte.Cohorte, trayecto.Trayecto, trimestre.Trimestre, seccion.Seccion, modalidad.Turno, semana.Dia, hora_inicial.Hora, hora_final.Hora, unidad_curricular.UnidadCurricular FROM materias_asignadas INNER JOIN lapso_academico ON  lapso_academico.Id = materias_asignadas.Id_lapso_academico INNER JOIN cohorte ON  cohorte.Id = materias_asignadas.Id_cohorte INNER JOIN trayecto ON trayecto.Id = materias_asignadas.Id_trayecto INNER JOIN trimestre ON trimestre.Id = materias_asignadas.Id_trimestre INNER JOIN seccion ON seccion.Id = materias_asignadas.Id_seccion INNER JOIN modalidad ON modalidad.Id = materias_asignadas.Id_modalidad INNER JOIN semana ON semana.Id = materias_asignadas.Id_semana INNER JOIN hora_inicial ON hora_inicial.Id = materias_asignadas.Id_hora_inicial INNER JOIN hora_final ON hora_final.Id = materias_asignadas.Id_hora_final INNER JOIN unidad_curricular ON unidad_curricular.Id = materias_asignadas.Id_unidad_curricular WHERE materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_cohorte = ? AND materias_asignadas.Id_trayecto = ? AND materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_semana = ? AND materias_asignadas.Id_hora_inicial = ? AND materias_asignadas.Id_hora_final = ? AND materias_asignadas.Id_unidad_curricular = ? AND materias_asignadas.Estado = "Activo"',(self.selecionarFilaLapsoAcademico(),self.selecionarFilaCohorte(),self.selecionarFilaTrayecto(),self.selecionarFilaTrimestre(),self.selecionarFilaSeccion(),self.selecionarFilaTurno(),self.selecionarFilaDia(),self.selecionarFilaHoraInicial(),self.selecionarFilaHoraFinal(),self.selecionarFilaUnidadCurricular())).fetchall()
						if same:
							messagebox.showwarning(title='warning', message="Este registro ya le pertenece a otro docente")	
						else:
							validarMateria = self.conexion('SELECT materias_asignadas.Id ,docente.NombreApellido, lapso_academico.LapsoAcademico,cohorte.Cohorte, trayecto.Trayecto, trimestre.Trimestre, seccion.Seccion, modalidad.Turno, semana.Dia, hora_inicial.Hora, hora_final.Hora FROM materias_asignadas INNER JOIN docente ON  docente.Id = materias_asignadas.Id_docente INNER JOIN lapso_academico ON  lapso_academico.Id = materias_asignadas.Id_lapso_academico INNER JOIN cohorte ON  cohorte.Id = materias_asignadas.Id_cohorte INNER JOIN trayecto ON trayecto.Id = materias_asignadas.Id_trayecto INNER JOIN trimestre ON trimestre.Id = materias_asignadas.Id_trimestre INNER JOIN seccion ON seccion.Id = materias_asignadas.Id_seccion  INNER JOIN modalidad ON modalidad.Id = materias_asignadas.Id_modalidad INNER JOIN semana ON semana.Id = materias_asignadas.Id_semana  INNER JOIN hora_inicial ON hora_inicial.Id = materias_asignadas.Id_hora_inicial  INNER JOIN hora_final ON hora_final.Id = materias_asignadas.Id_hora_final  WHERE  materias_asignadas.Id_docente = ? AND materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_cohorte = ? AND  materias_asignadas.Id_trayecto = ? AND  materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND  materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_semana = ? AND  materias_asignadas.Id_hora_inicial = ? AND  materias_asignadas.Id_hora_final = ? AND materias_asignadas.Estado = "Activo"',(self.seleccion,self.selecionarFilaLapsoAcademico(),self.selecionarFilaCohorte(),self.selecionarFilaTrayecto(),self.selecionarFilaTrimestre(),self.selecionarFilaSeccion(),self.selecionarFilaTurno(),self.selecionarFilaDia(),self.selecionarFilaHoraInicial(),self.selecionarFilaHoraFinal())).fetchall()
							if validarMateria:
								messagebox.showwarning(title='warning', message="No puede inscribir otra materia en este registro")	
							else:
								validarMateriaOtroDocente = self.conexion('SELECT materias_asignadas.Id ,lapso_academico.LapsoAcademico, cohorte.Cohorte, trayecto.Trayecto, trimestre.Trimestre, seccion.Seccion, modalidad.Turno, semana.Dia, hora_inicial.Hora, hora_final.Hora FROM materias_asignadas INNER JOIN lapso_academico ON  lapso_academico.Id = materias_asignadas.Id_lapso_academico INNER JOIN cohorte ON  cohorte.Id = materias_asignadas.Id_cohorte INNER JOIN trayecto ON trayecto.Id = materias_asignadas.Id_trayecto INNER JOIN trimestre ON trimestre.Id = materias_asignadas.Id_trimestre INNER JOIN seccion ON seccion.Id = materias_asignadas.Id_seccion  INNER JOIN modalidad ON modalidad.Id = materias_asignadas.Id_modalidad INNER JOIN semana ON semana.Id = materias_asignadas.Id_semana  INNER JOIN hora_inicial ON hora_inicial.Id = materias_asignadas.Id_hora_inicial  INNER JOIN hora_final ON hora_final.Id = materias_asignadas.Id_hora_final  WHERE  materias_asignadas.Id_lapso_academico = ? AND materias_asignadas.Id_cohorte = ? AND  materias_asignadas.Id_trayecto = ? AND  materias_asignadas.Id_trimestre = ? AND materias_asignadas.Id_seccion = ? AND  materias_asignadas.Id_modalidad = ? AND materias_asignadas.Id_semana = ? AND  materias_asignadas.Id_hora_inicial = ? AND  materias_asignadas.Id_hora_final = ? AND materias_asignadas.Estado = "Activo"',(self.selecionarFilaLapsoAcademico(),self.selecionarFilaCohorte(),self.selecionarFilaTrayecto(),self.selecionarFilaTrimestre(),self.selecionarFilaSeccion(),self.selecionarFilaTurno(),self.selecionarFilaDia(),self.selecionarFilaHoraInicial(),self.selecionarFilaHoraFinal())).fetchall()
								if validarMateriaOtroDocente:
									messagebox.showwarning(title='warning', message="Este registro ya le pertenece a otro docente2")
								else:
									if self.laboratorio.get() == 'Si':
										if self.treeLaboratorio.selection():
											if self.obtenerHoraMateria() == '6':
												# BLOQUE 2
												# Horario Mañana
												if self.obtenerHoraInicial() == 1 and self.obtenerHoraFinal() == 2:
													self.editarSi()
												elif self.obtenerHoraInicial() == 2 and self.obtenerHoraFinal() == 3:
													self.editarSi()
												elif self.obtenerHoraInicial() == 3 and self.obtenerHoraFinal() == 4:
													self.editarSi()
												elif self.obtenerHoraInicial() == 4 and self.obtenerHoraFinal() == 5:
													self.editarSi()
												elif self.obtenerHoraInicial() == 5 and self.obtenerHoraFinal() == 6:
													self.editarSi()
												# Horario Tarde
												elif self.obtenerHoraInicial() == 7 and self.obtenerHoraFinal() == 8:
													self.editarSi()
												elif self.obtenerHoraInicial() == 8 and self.obtenerHoraFinal() == 9:
													self.editarSi()
												elif self.obtenerHoraInicial() == 9 and self.obtenerHoraFinal() == 10:
													self.editarSi()
												elif self.obtenerHoraInicial() == 10 and self.obtenerHoraFinal() == 11:
													self.editarSi()
												elif self.obtenerHoraInicial() == 11 and self.obtenerHoraFinal() == 12:
													self.editarSi()
												# Horario Noche
												elif self.obtenerHoraInicial() == 13 and self.obtenerHoraFinal() == 14:
													self.editarSi()
												elif self.obtenerHoraInicial() == 14 and self.obtenerHoraFinal() == 15:
													self.editarSi()
												elif self.obtenerHoraInicial() == 15 and self.obtenerHoraFinal() == 16:
													self.editarSi()
												elif self.obtenerHoraInicial() == 16 and self.obtenerHoraFinal() == 17:
													self.editarSi()
												elif self.obtenerHoraInicial() == 17 and self.obtenerHoraFinal() == 18:
													self.editarSi()
													# BLOQUE 3
												elif self.obtenerHoraInicial() == 1 and self.obtenerHoraFinal() == 3:
													self.editarSi()
												elif self.obtenerHoraInicial() == 2 and self.obtenerHoraFinal() == 4:
													self.editarSi()
												elif self.obtenerHoraInicial() == 3 and self.obtenerHoraFinal() == 5:
													self.editarSi()
												elif self.obtenerHoraInicial() == 4 and self.obtenerHoraFinal() == 6:
													self.editarSi()
												elif self.obtenerHoraInicial() == 7 and self.obtenerHoraFinal() == 9:
													self.editarSi()
												elif self.obtenerHoraInicial() == 8 and self.obtenerHoraFinal() == 10:
													self.editarSi()
												elif self.obtenerHoraInicial() == 9 and self.obtenerHoraFinal() == 11:
													self.editarSi()
												elif self.obtenerHoraInicial() == 10 and self.obtenerHoraFinal() == 12:
													self.editarSi()												
												elif self.obtenerHoraInicial() == 13 and self.obtenerHoraFinal() == 15:
													self.editarSi()
												elif self.obtenerHoraInicial() == 14 and self.obtenerHoraFinal() == 16:
													self.editarSi()
												elif self.obtenerHoraInicial() == 15 and self.obtenerHoraFinal() == 17:
													self.editarSi()
												elif self.obtenerHoraInicial() == 16 and self.obtenerHoraFinal() == 18:
													self.editarSi()											
													#  BLOQUE 4
												elif self.obtenerHoraInicial() == 1 and self.obtenerHoraFinal() == 4:
													self.editarSi()												
												elif self.obtenerHoraInicial() == 2 and self.obtenerHoraFinal() == 5:
													self.editarSi()
												elif self.obtenerHoraInicial() == 3 and self.obtenerHoraFinal() == 6:
													self.editarSi()
												elif self.obtenerHoraInicial() == 7 and self.obtenerHoraFinal() == 10:
													self.editarSi()
												elif self.obtenerHoraInicial() == 8 and self.obtenerHoraFinal() == 11:
													self.editarSi()
												elif self.obtenerHoraInicial() == 9 and self.obtenerHoraFinal() == 12:
													self.editarSi()
												elif self.obtenerHoraInicial() == 13 and self.obtenerHoraFinal() == 16:
													self.editarSi()
												elif self.obtenerHoraInicial() == 14 and self.obtenerHoraFinal() == 17:
													self.editarSi()
												elif self.obtenerHoraInicial() == 15 and self.obtenerHoraFinal() == 18:
													self.editarSi()
													# BLOQUE 6  
												elif self.obtenerHoraInicial() == 1 and self.obtenerHoraFinal() == 6:
													self.editarSi()
												elif self.obtenerHoraInicial() == 7 and self.obtenerHoraFinal() == 12:
													self.editarSi()
												elif self.obtenerHoraInicial() == 13 and self.obtenerHoraFinal() == 18:
													self.editarSi()
												else:
													messagebox.showinfo(title='info', message='Hora no permitida')
											elif self.obtenerHoraMateria() == '5':
												# BLOQUE 2
												# Horario Mañana
												if self.obtenerHoraInicial() == 1 and self.obtenerHoraFinal() == 2:
													self.editarSi()
												elif self.obtenerHoraInicial() == 2 and self.obtenerHoraFinal() == 3:
													self.editarSi()
												elif self.obtenerHoraInicial() == 3 and self.obtenerHoraFinal() == 4:
													self.editarSi()
												elif self.obtenerHoraInicial() == 4 and self.obtenerHoraFinal() == 5:
													self.editarSi()
												elif self.obtenerHoraInicial() == 5 and self.obtenerHoraFinal() == 6:
													self.editarSi()
												# Horario Tarde
												elif self.obtenerHoraInicial() == 7 and self.obtenerHoraFinal() == 8:
													self.editarSi()
												elif self.obtenerHoraInicial() == 8 and self.obtenerHoraFinal() == 9:
													self.editarSi()
												elif self.obtenerHoraInicial() == 9 and self.obtenerHoraFinal() == 10:
													self.editarSi()
												elif self.obtenerHoraInicial() == 10 and self.obtenerHoraFinal() == 11:
													self.editarSi()
												elif self.obtenerHoraInicial() == 11 and self.obtenerHoraFinal() == 12:
													self.editarSi()
												# Horario Noche
												elif self.obtenerHoraInicial() == 13 and self.obtenerHoraFinal() == 14:
													self.editarSi()
												elif self.obtenerHoraInicial() == 14 and self.obtenerHoraFinal() == 15:
													self.editarSi()
												elif self.obtenerHoraInicial() == 15 and self.obtenerHoraFinal() == 16:
													self.editarSi()
												elif self.obtenerHoraInicial() == 16 and self.obtenerHoraFinal() == 17:
													self.editarSi()
												elif self.obtenerHoraInicial() == 17 and self.obtenerHoraFinal() == 18:
													self.editarSi()
												# BLOQUE 3
												# Horario Mañana
												elif self.obtenerHoraInicial() == 1 and self.obtenerHoraFinal() == 3:
													self.editarSi()
												elif self.obtenerHoraInicial() == 2 and self.obtenerHoraFinal() == 4:
													self.editarSi()
												elif self.obtenerHoraInicial() == 3 and self.obtenerHoraFinal() == 5:
													self.editarSi()
												elif self.obtenerHoraInicial() == 4 and self.obtenerHoraFinal() == 6:
													self.editarSi()
												elif self.obtenerHoraInicial() == 7 and self.obtenerHoraFinal() == 9:
													self.editarSi()
												elif self.obtenerHoraInicial() == 8 and self.obtenerHoraFinal() == 10:
													self.editarSi()
												elif self.obtenerHoraInicial() == 9 and self.obtenerHoraFinal() == 11:
													self.editarSi()
												elif self.obtenerHoraInicial() == 10 and self.obtenerHoraFinal() == 12:
													self.editarSi()											
												elif self.obtenerHoraInicial() == 13 and self.obtenerHoraFinal() == 15:
													self.editarSi()
												elif self.obtenerHoraInicial() == 14 and self.obtenerHoraFinal() == 16:
													self.editarSi()
												elif self.obtenerHoraInicial() == 15 and self.obtenerHoraFinal() == 17:
													self.editarSi()
												elif self.obtenerHoraInicial() == 16 and self.obtenerHoraFinal() == 18:
													self.editarSi()
												# BLOQUE 5
												elif self.obtenerHoraInicial() == 1 and self.obtenerHoraFinal() == 5:
													self.editarSi()
												elif self.obtenerHoraInicial() == 2 and self.obtenerHoraFinal() == 6:
													self.editarSi()
												elif self.obtenerHoraInicial() == 7 and self.obtenerHoraFinal() == 11:
													self.editarSi()
												elif self.obtenerHoraInicial() == 8 and self.obtenerHoraFinal() == 12:
													self.editarSi()
												elif self.obtenerHoraInicial() == 13 and self.obtenerHoraFinal() == 17:
													self.editarSi()
												elif self.obtenerHoraInicial() == 14 and self.obtenerHoraFinal() == 18:
													self.editarSi()
												else:
													messagebox.showinfo(title='info', message='Hora no permitida')
											elif self.obtenerHoraMateria() == '4':
												# BLOQUE 2
												# Horario Mañana
												if self.obtenerHoraInicial() == 1 and self.obtenerHoraFinal() == 2:
													self.editarSi()
												elif self.obtenerHoraInicial() == 2 and self.obtenerHoraFinal() == 3:
													self.editarSi()
												elif self.obtenerHoraInicial() == 3 and self.obtenerHoraFinal() == 4:
													self.editarSi()
												elif self.obtenerHoraInicial() == 4 and self.obtenerHoraFinal() == 5:
													self.editarSi()
												elif self.obtenerHoraInicial() == 5 and self.obtenerHoraFinal() == 6:
													self.editarSi()
												# Horario Tarde
												elif self.obtenerHoraInicial() == 7 and self.obtenerHoraFinal() == 8:
													self.editarSi()
												elif self.obtenerHoraInicial() == 8 and self.obtenerHoraFinal() == 9:
													self.editarSi()
												elif self.obtenerHoraInicial() == 9 and self.obtenerHoraFinal() == 10:
													self.editarSi()
												elif self.obtenerHoraInicial() == 10 and self.obtenerHoraFinal() == 11:
													self.editarSi()
												elif self.obtenerHoraInicial() == 11 and self.obtenerHoraFinal() == 12:
													self.editarSi()
												# Horario Noche
												elif self.obtenerHoraInicial() == 13 and self.obtenerHoraFinal() == 14:
													self.editarSi()
												elif self.obtenerHoraInicial() == 14 and self.obtenerHoraFinal() == 15:
													self.editarSi()
												elif self.obtenerHoraInicial() == 15 and self.obtenerHoraFinal() == 16:
													self.editarSi()
												elif self.obtenerHoraInicial() == 16 and self.obtenerHoraFinal() == 17:
													self.editarSi()
												elif self.obtenerHoraInicial() == 17 and self.obtenerHoraFinal() == 18:
													self.editarSi()											
												# BLOQUE 4
												elif self.obtenerHoraInicial() == 1 and self.obtenerHoraFinal() == 4:
													self.editarSi()											
												elif self.obtenerHoraInicial() == 2 and self.obtenerHoraFinal() == 5:
													self.editarSi()
												elif self.obtenerHoraInicial() == 3 and self.obtenerHoraFinal() == 6:
													self.editarSi()
												elif self.obtenerHoraInicial() == 7 and self.obtenerHoraFinal() == 10:
													self.editarSi()
												elif self.obtenerHoraInicial() == 8 and self.obtenerHoraFinal() == 11:
													self.editarSi()
												elif self.obtenerHoraInicial() == 9 and self.obtenerHoraFinal() == 12:
													self.editarSi()
												elif self.obtenerHoraInicial() == 13 and self.obtenerHoraFinal() == 16:
													self.editarSi()
												elif self.obtenerHoraInicial() == 14 and self.obtenerHoraFinal() == 17:
													self.editarSi()
												elif self.obtenerHoraInicial() == 15 and self.obtenerHoraFinal() == 18:
													self.editarSi()
												else:
													messagebox.showinfo(title='info', message='Hora no permitida')
											elif self.obtenerHoraMateria() == '3':
												if self.obtenerHoraInicial() == 1 and self.obtenerHoraFinal() == 3:
													self.editarSi()
												elif self.obtenerHoraInicial() == 2 and self.obtenerHoraFinal() == 4:
													self.editarSi()
												elif self.obtenerHoraInicial() == 3 and self.obtenerHoraFinal() == 5:
													self.editarSi()
												elif self.obtenerHoraInicial() == 4 and self.obtenerHoraFinal() == 6:
													self.editarSi()
												elif self.obtenerHoraInicial() == 7 and self.obtenerHoraFinal() == 9:
													self.editarSi()
												elif self.obtenerHoraInicial() == 8 and self.obtenerHoraFinal() == 10:
													self.editarSi()
												elif self.obtenerHoraInicial() == 9 and self.obtenerHoraFinal() == 11:
													self.editarSi()
												elif self.obtenerHoraInicial() == 10 and self.obtenerHoraFinal() == 12:
													self.editarSi()											
												elif self.obtenerHoraInicial() == 13 and self.obtenerHoraFinal() == 15:
													self.editarSi()
												elif self.obtenerHoraInicial() == 14 and self.obtenerHoraFinal() == 16:
													self.editarSi()
												elif self.obtenerHoraInicial() == 15 and self.obtenerHoraFinal() == 17:
													self.editarSi()
												elif self.obtenerHoraInicial() == 16 and self.obtenerHoraFinal() == 18:
													self.editarSi()
												else:
													messagebox.showinfo(title='info', message='Hora no permitida')
											elif self.obtenerHoraMateria() == '2':
												# Horario Mañana
												if self.obtenerHoraInicial() == 1 and self.obtenerHoraFinal() == 2:
													self.editarSi()
												elif self.obtenerHoraInicial() == 2 and self.obtenerHoraFinal() == 3:
													self.editarSi()
												elif self.obtenerHoraInicial() == 3 and self.obtenerHoraFinal() == 4:
													self.editarSi()
												elif self.obtenerHoraInicial() == 4 and self.obtenerHoraFinal() == 5:
													self.editarSi()
												elif self.obtenerHoraInicial() == 5 and self.obtenerHoraFinal() == 6:
													self.editarSi()
												# Horario Tarde
												elif self.obtenerHoraInicial() == 7 and self.obtenerHoraFinal() == 8:
													self.editarSi()
												elif self.obtenerHoraInicial() == 8 and self.obtenerHoraFinal() == 9:
													self.editarSi()
												elif self.obtenerHoraInicial() == 9 and self.obtenerHoraFinal() == 10:
													self.editarSi()
												elif self.obtenerHoraInicial() == 10 and self.obtenerHoraFinal() == 11:
													self.editarSi()
												elif self.obtenerHoraInicial() == 11 and self.obtenerHoraFinal() == 12:
													self.editarSi()
												# Horario Noche
												elif self.obtenerHoraInicial() == 13 and self.obtenerHoraFinal() == 14:
													self.editarSi()
												elif self.obtenerHoraInicial() == 14 and self.obtenerHoraFinal() == 15:
													self.editarSi()
												elif self.obtenerHoraInicial() == 15 and self.obtenerHoraFinal() == 16:
													self.editarSi()
												elif self.obtenerHoraInicial() == 16 and self.obtenerHoraFinal() == 17:
													self.editarSi()
												elif self.obtenerHoraInicial() == 17 and self.obtenerHoraFinal() == 18:
													self.editarSi()
												else:
													messagebox.showinfo(title='info', message='Hora no permitida')
											elif self.obtenerHoraMateria() == ' ':
												messagebox.showinfo(title='info', message='Debe de asignarle una hora académica a esta materia, antes de añadir la materia a un docente')
										else:
											messagebox.showwarning(title='Warning', message='Seleccione un laboratorio')
									elif self.laboratorio.get() == 'No':
										if self.obtenerHoraMateria() == '6':
											# BLOQUE 6
											# Horario Mañana
											if self.obtenerHoraInicial() == 1 and self.obtenerHoraFinal() == 2:
												self.editarNo()
											elif self.obtenerHoraInicial() == 2 and self.obtenerHoraFinal() == 3:
												self.editarNo()
											elif self.obtenerHoraInicial() == 3 and self.obtenerHoraFinal() == 4:
												self.editarNo()
											elif self.obtenerHoraInicial() == 4 and self.obtenerHoraFinal() == 5:
												self.editarNo()
											elif self.obtenerHoraInicial() == 5 and self.obtenerHoraFinal() == 6:
												self.editarNo()
											# Horario Tarde
											elif self.obtenerHoraInicial() == 7 and self.obtenerHoraFinal() == 8:
												self.editarNo()
											elif self.obtenerHoraInicial() == 8 and self.obtenerHoraFinal() == 9:
												self.editarNo()
											elif self.obtenerHoraInicial() == 9 and self.obtenerHoraFinal() == 10:
												self.editarNo()
											elif self.obtenerHoraInicial() == 10 and self.obtenerHoraFinal() == 11:
												self.editarNo()
											elif self.obtenerHoraInicial() == 11 and self.obtenerHoraFinal() == 12:
												self.editarNo()
											# Horario Noche
											elif self.obtenerHoraInicial() == 13 and self.obtenerHoraFinal() == 14:
												self.editarNo()
											elif self.obtenerHoraInicial() == 14 and self.obtenerHoraFinal() == 15:
												self.editarNo()
											elif self.obtenerHoraInicial() == 15 and self.obtenerHoraFinal() == 16:
												self.editarNo()
											elif self.obtenerHoraInicial() == 16 and self.obtenerHoraFinal() == 17:
												self.editarNo()
											elif self.obtenerHoraInicial() == 17 and self.obtenerHoraFinal() == 18:
												self.editarNo()
												# BLOQUE 3
											elif self.obtenerHoraInicial() == 1 and self.obtenerHoraFinal() == 3:
												self.editarNo()
											elif self.obtenerHoraInicial() == 2 and self.obtenerHoraFinal() == 4:
												self.editarNo()
											elif self.obtenerHoraInicial() == 3 and self.obtenerHoraFinal() == 5:
												self.editarNo()
											elif self.obtenerHoraInicial() == 4 and self.obtenerHoraFinal() == 6:
												self.editarNo()
											elif self.obtenerHoraInicial() == 7 and self.obtenerHoraFinal() == 9:
												self.editarNo()
											elif self.obtenerHoraInicial() == 8 and self.obtenerHoraFinal() == 10:
												self.editarNo()
											elif self.obtenerHoraInicial() == 9 and self.obtenerHoraFinal() == 11:
												self.editarNo()
											elif self.obtenerHoraInicial() == 10 and self.obtenerHoraFinal() == 12:
												self.editarNo()												
											elif self.obtenerHoraInicial() == 13 and self.obtenerHoraFinal() == 15:
												self.editarNo()
											elif self.obtenerHoraInicial() == 14 and self.obtenerHoraFinal() == 16:
												self.editarNo()
											elif self.obtenerHoraInicial() == 15 and self.obtenerHoraFinal() == 17:
												self.editarNo()
											elif self.obtenerHoraInicial() == 16 and self.obtenerHoraFinal() == 18:
												self.editarNo()											
												#  BLOQUE 4
											elif self.obtenerHoraInicial() == 1 and self.obtenerHoraFinal() == 4:
												self.editarNo()												
											elif self.obtenerHoraInicial() == 2 and self.obtenerHoraFinal() == 5:
												self.editarNo()
											elif self.obtenerHoraInicial() == 3 and self.obtenerHoraFinal() == 6:
												self.editarNo()
											elif self.obtenerHoraInicial() == 7 and self.obtenerHoraFinal() == 10:
												self.editarNo()
											elif self.obtenerHoraInicial() == 8 and self.obtenerHoraFinal() == 11:
												self.editarNo()
											elif self.obtenerHoraInicial() == 9 and self.obtenerHoraFinal() == 12:
												self.editarNo()
											elif self.obtenerHoraInicial() == 13 and self.obtenerHoraFinal() == 16:
												self.editarNo()
											elif self.obtenerHoraInicial() == 14 and self.obtenerHoraFinal() == 17:
												self.editarNo()
											elif self.obtenerHoraInicial() == 15 and self.obtenerHoraFinal() == 18:
												self.editarNo()
											# BLOQUE 6  
											elif self.obtenerHoraInicial() == 1 and self.obtenerHoraFinal() == 6:
												self.editarNo()
											elif self.obtenerHoraInicial() == 7 and self.obtenerHoraFinal() == 12:
												self.editarNo()
											elif self.obtenerHoraInicial() == 13 and self.obtenerHoraFinal() == 18:
												self.editarNo()
											else:
												messagebox.showinfo(title='info', message='Hora no permitida')
										elif self.obtenerHoraMateria() == '5':
											# BLOQUE 2
											# Horario Mañana
											if self.obtenerHoraInicial() == 1 and self.obtenerHoraFinal() == 2:
												self.editarNo()
											elif self.obtenerHoraInicial() == 2 and self.obtenerHoraFinal() == 3:
												self.editarNo()
											elif self.obtenerHoraInicial() == 3 and self.obtenerHoraFinal() == 4:
												self.editarNo()
											elif self.obtenerHoraInicial() == 4 and self.obtenerHoraFinal() == 5:
												self.editarNo()
											elif self.obtenerHoraInicial() == 5 and self.obtenerHoraFinal() == 6:
												self.editarNo()
											# Horario Tarde
											elif self.obtenerHoraInicial() == 7 and self.obtenerHoraFinal() == 8:
												self.editarNo()
											elif self.obtenerHoraInicial() == 8 and self.obtenerHoraFinal() == 9:
												self.editarNo()
											elif self.obtenerHoraInicial() == 9 and self.obtenerHoraFinal() == 10:
												self.editarNo()
											elif self.obtenerHoraInicial() == 10 and self.obtenerHoraFinal() == 11:
												self.editarNo()
											elif self.obtenerHoraInicial() == 11 and self.obtenerHoraFinal() == 12:
												self.editarNo()
											# Horario Noche
											elif self.obtenerHoraInicial() == 13 and self.obtenerHoraFinal() == 14:
												self.editarNo()
											elif self.obtenerHoraInicial() == 14 and self.obtenerHoraFinal() == 15:
												self.editarNo()
											elif self.obtenerHoraInicial() == 15 and self.obtenerHoraFinal() == 16:
												self.editarNo()
											elif self.obtenerHoraInicial() == 16 and self.obtenerHoraFinal() == 17:
												self.editarNo()
											elif self.obtenerHoraInicial() == 17 and self.obtenerHoraFinal() == 18:
												self.editarNo()
											# BLOQUE 3
											# Horario Mañana
											elif self.obtenerHoraInicial() == 1 and self.obtenerHoraFinal() == 3:
												self.editarNo()
											elif self.obtenerHoraInicial() == 2 and self.obtenerHoraFinal() == 4:
												self.editarNo()
											elif self.obtenerHoraInicial() == 3 and self.obtenerHoraFinal() == 5:
												self.editarNo()
											elif self.obtenerHoraInicial() == 4 and self.obtenerHoraFinal() == 6:
												self.editarNo()
											elif self.obtenerHoraInicial() == 7 and self.obtenerHoraFinal() == 9:
												self.editarNo()
											elif self.obtenerHoraInicial() == 8 and self.obtenerHoraFinal() == 10:
												self.editarNo()
											elif self.obtenerHoraInicial() == 9 and self.obtenerHoraFinal() == 11:
												self.editarNo()
											elif self.obtenerHoraInicial() == 10 and self.obtenerHoraFinal() == 12:
												self.editarNo()											
											elif self.obtenerHoraInicial() == 13 and self.obtenerHoraFinal() == 15:
												self.editarNo()
											elif self.obtenerHoraInicial() == 14 and self.obtenerHoraFinal() == 16:
												self.editarNo()
											elif self.obtenerHoraInicial() == 15 and self.obtenerHoraFinal() == 17:
												self.editarNo()
											elif self.obtenerHoraInicial() == 16 and self.obtenerHoraFinal() == 18:
												self.editarNo()
											# BLOQUE 5
											elif self.obtenerHoraInicial() == 1 and self.obtenerHoraFinal() == 5:
												self.editarNo()
											elif self.obtenerHoraInicial() == 2 and self.obtenerHoraFinal() == 6:
												self.editarNo()
											elif self.obtenerHoraInicial() == 7 and self.obtenerHoraFinal() == 11:
												self.editarNo()
											elif self.obtenerHoraInicial() == 8 and self.obtenerHoraFinal() == 12:
												self.editarNo()
											elif self.obtenerHoraInicial() == 13 and self.obtenerHoraFinal() == 17:
												self.editarNo()
											elif self.obtenerHoraInicial() == 14 and self.obtenerHoraFinal() == 18:
												self.editarNo()
											else:
												messagebox.showinfo(title='info', message='Hora no permitida')
										elif self.obtenerHoraMateria() == '4':
											# BLOQUE 2
											# Horario Mañana
											if self.obtenerHoraInicial() == 1 and self.obtenerHoraFinal() == 2:
												self.editarNo()
											elif self.obtenerHoraInicial() == 2 and self.obtenerHoraFinal() == 3:
												self.editarNo()
											elif self.obtenerHoraInicial() == 3 and self.obtenerHoraFinal() == 4:
												self.editarNo()
											elif self.obtenerHoraInicial() == 4 and self.obtenerHoraFinal() == 5:
												self.editarNo()
											elif self.obtenerHoraInicial() == 5 and self.obtenerHoraFinal() == 6:
												self.editarNo()
											# Horario Tarde
											elif self.obtenerHoraInicial() == 7 and self.obtenerHoraFinal() == 8:
												self.editarNo()
											elif self.obtenerHoraInicial() == 8 and self.obtenerHoraFinal() == 9:
												self.editarNo()
											elif self.obtenerHoraInicial() == 9 and self.obtenerHoraFinal() == 10:
												self.editarNo()
											elif self.obtenerHoraInicial() == 10 and self.obtenerHoraFinal() == 11:
												self.editarNo()
											elif self.obtenerHoraInicial() == 11 and self.obtenerHoraFinal() == 12:
												self.editarNo()
											# Horario Noche
											elif self.obtenerHoraInicial() == 13 and self.obtenerHoraFinal() == 14:
												self.editarNo()
											elif self.obtenerHoraInicial() == 14 and self.obtenerHoraFinal() == 15:
												self.editarNo()
											elif self.obtenerHoraInicial() == 15 and self.obtenerHoraFinal() == 16:
												self.editarNo()
											elif self.obtenerHoraInicial() == 16 and self.obtenerHoraFinal() == 17:
												self.editarNo()
											elif self.obtenerHoraInicial() == 17 and self.obtenerHoraFinal() == 18:
												self.editarNo()											
											# BLOQUE 4
											elif self.obtenerHoraInicial() == 1 and self.obtenerHoraFinal() == 4:
												self.editarNo()											
											elif self.obtenerHoraInicial() == 2 and self.obtenerHoraFinal() == 5:
												self.editarNo()
											elif self.obtenerHoraInicial() == 3 and self.obtenerHoraFinal() == 6:
												self.editarNo()
											elif self.obtenerHoraInicial() == 7 and self.obtenerHoraFinal() == 10:
												self.editarNo()
											elif self.obtenerHoraInicial() == 8 and self.obtenerHoraFinal() == 11:
												self.editarNo()
											elif self.obtenerHoraInicial() == 9 and self.obtenerHoraFinal() == 12:
												self.editarNo()
											elif self.obtenerHoraInicial() == 13 and self.obtenerHoraFinal() == 16:
												self.editarNo()
											elif self.obtenerHoraInicial() == 14 and self.obtenerHoraFinal() == 17:
												self.editarNo()
											elif self.obtenerHoraInicial() == 15 and self.obtenerHoraFinal() == 18:
												self.editarNo()
											else:
												messagebox.showinfo(title='info', message='Hora no permitida')
										elif self.obtenerHoraMateria() == '3':
											# Horario Mañana
											if self.obtenerHoraInicial() == 1 and self.obtenerHoraFinal() == 3:
												self.editarNo()
											elif self.obtenerHoraInicial() == 2 and self.obtenerHoraFinal() == 4:
												self.editarNo()
											elif self.obtenerHoraInicial() == 3 and self.obtenerHoraFinal() == 5:
												self.editarNo()
											elif self.obtenerHoraInicial() == 4 and self.obtenerHoraFinal() == 6:
												self.editarNo()
											elif self.obtenerHoraInicial() == 7 and self.obtenerHoraFinal() == 9:
												self.editarNo()
											elif self.obtenerHoraInicial() == 8 and self.obtenerHoraFinal() == 10:
												self.editarNo()
											elif self.obtenerHoraInicial() == 9 and self.obtenerHoraFinal() == 11:
												self.editarNo()
											elif self.obtenerHoraInicial() == 10 and self.obtenerHoraFinal() == 12:
												self.editarNo()											
											elif self.obtenerHoraInicial() == 13 and self.obtenerHoraFinal() == 15:
												self.editarNo()
											elif self.obtenerHoraInicial() == 14 and self.obtenerHoraFinal() == 16:
												self.editarNo()
											elif self.obtenerHoraInicial() == 15 and self.obtenerHoraFinal() == 17:
												self.editarNo()
											elif self.obtenerHoraInicial() == 16 and self.obtenerHoraFinal() == 18:
												self.editarNo()
											else:
												messagebox.showinfo(title='info', message='Hora no permitida')
										elif self.obtenerHoraMateria() == '2':
											# Horario Mañana
											if self.obtenerHoraInicial() == 1 and self.obtenerHoraFinal() == 2:
												self.editarNo()
											elif self.obtenerHoraInicial() == 2 and self.obtenerHoraFinal() == 3:
												self.editarNo()
											elif self.obtenerHoraInicial() == 3 and self.obtenerHoraFinal() == 4:
												self.editarNo()
											elif self.obtenerHoraInicial() == 4 and self.obtenerHoraFinal() == 5:
												self.editarNo()
											elif self.obtenerHoraInicial() == 5 and self.obtenerHoraFinal() == 6:
												self.editarNo()
											# Horario Tarde
											elif self.obtenerHoraInicial() == 7 and self.obtenerHoraFinal() == 8:
												self.editarNo()
											elif self.obtenerHoraInicial() == 8 and self.obtenerHoraFinal() == 9:
												self.editarNo()
											elif self.obtenerHoraInicial() == 9 and self.obtenerHoraFinal() == 10:
												self.editarNo()
											elif self.obtenerHoraInicial() == 10 and self.obtenerHoraFinal() == 11:
												self.editarNo()
											elif self.obtenerHoraInicial() == 11 and self.obtenerHoraFinal() == 12:
												self.editarNo()
											# Horario Noche
											elif self.obtenerHoraInicial() == 13 and self.obtenerHoraFinal() == 14:
												self.editarNo()
											elif self.obtenerHoraInicial() == 14 and self.obtenerHoraFinal() == 15:
												self.editarNo()
											elif self.obtenerHoraInicial() == 15 and self.obtenerHoraFinal() == 16:
												self.editarNo()
											elif self.obtenerHoraInicial() == 16 and self.obtenerHoraFinal() == 17:
												self.editarNo()
											elif self.obtenerHoraInicial() == 17 and self.obtenerHoraFinal() == 18:
												self.editarNo()
											else:
												messagebox.showinfo(title='info', message='Hora no permitida')
										elif self.obtenerHoraMateria() == ' ':
											messagebox.showinfo(title='info', message='Debe de asignarle una hora académica a esta materia, antes de añadir la materia a un docente')
						
									else:
										messagebox.showwarning(title='Warning', message='Seleccione la casilla')
				else:
					self.MostrarDatosGestionar()
			else:
				messagebox.showwarning(title='Wanning', message='Seleccione datos a editar.')
		else:
			messagebox.showwarning(title='Wanning', message='Seleccione una registro a editar.')

	def editarNo(self):
		self.conexion('UPDATE materias_asignadas SET Id_lapso_academico = ? WHERE materias_asignadas.Id = ? AND materias_asignadas.Estado = "Activo"',(self.selecionarFilaLapsoAcademico(),self.selecionarFilaGestionar()))
		self.conexion('UPDATE materias_asignadas SET Id_cohorte = ? WHERE materias_asignadas.Id = ? AND materias_asignadas.Estado = "Activo"',(self.selecionarFilaCohorte(),self.selecionarFilaGestionar()))
		self.conexion('UPDATE materias_asignadas SET Id_trayecto = ? WHERE materias_asignadas.Id = ? AND materias_asignadas.Estado = "Activo"',(self.selecionarFilaTrayecto(),self.selecionarFilaGestionar()))
		self.conexion('UPDATE materias_asignadas SET Id_trimestre = ? WHERE materias_asignadas.Id = ? AND materias_asignadas.Estado = "Activo"',(self.selecionarFilaTrimestre(),self.selecionarFilaGestionar()))
		self.conexion('UPDATE materias_asignadas SET Id_seccion = ? WHERE materias_asignadas.Id = ? AND materias_asignadas.Estado = "Activo"',(self.selecionarFilaSeccion(),self.selecionarFilaGestionar()))
		self.conexion('UPDATE materias_asignadas SET Id_modalidad = ? WHERE materias_asignadas.Id = ? AND materias_asignadas.Estado = "Activo"',(self.selecionarFilaTurno(),self.selecionarFilaGestionar()))
		self.conexion('UPDATE materias_asignadas SET Id_semana = ? WHERE materias_asignadas.Id = ? AND materias_asignadas.Estado = "Activo"',(self.selecionarFilaDia(),self.selecionarFilaGestionar()))
		self.conexion('UPDATE materias_asignadas SET Id_hora_inicial = ? WHERE materias_asignadas.Id = ? AND materias_asignadas.Estado = "Activo"',(self.selecionarFilaHoraInicial(),self.selecionarFilaGestionar()))
		self.conexion('UPDATE materias_asignadas SET Id_hora_final = ? WHERE materias_asignadas.Id = ? AND materias_asignadas.Estado = "Activo"',(self.selecionarFilaHoraFinal(),self.selecionarFilaGestionar()))
		self.conexion('UPDATE materias_asignadas SET Id_unidad_curricular = ? WHERE materias_asignadas.Id = ? AND materias_asignadas.Estado = "Activo"',(self.selecionarFilaUnidadCurricular(),self.selecionarFilaGestionar()))
		self.conexion('UPDATE materias_docentes SET Id_lapso_academico = ? WHERE materias_docentes.Id_materias_asignadas = ? AND materias_docentes.Estado = "Activo"',(self.selecionarFilaLapsoAcademico(),self.selecionarFilaGestionar()))
		self.conexion('UPDATE materias_docentes SET Id_modalidad = ? WHERE materias_docentes.Id_materias_asignadas = ? AND materias_docentes.Estado = "Activo"',(self.selecionarFilaTurno(),self.selecionarFilaGestionar()))
		materiaDocente = ('Cohorte ' + str(self.dataCohorte()) + ' Trayecto ' + str(self.dataTrayecto()) + ' Trimestre ' + str(self.dataTrimestre()) + ' Sección ' + str(self.dataSeccion()) + ' ' + str(self.dataUnidadCurricular()))
		self.conexion('UPDATE materias_docentes SET materia = ? WHERE materias_docentes.Id_materias_asignadas = ? AND materias_docentes.Estado = "Activo"',(materiaDocente,self.selecionarFilaGestionar()))
		self.conexion('UPDATE materias_docentes SET Id_semana = ? WHERE materias_docentes.Id_materias_asignadas = ? AND materias_docentes.Estado = "Activo"',(self.selecionarFilaDia(),self.selecionarFilaGestionar()))
		self.conexion('UPDATE materias_docentes SET Id_hora_inicial = ? WHERE materias_docentes.Id_materias_asignadas = ? AND materias_docentes.Estado = "Activo"',(self.selecionarFilaHoraInicial(),self.selecionarFilaGestionar()))
		self.conexion('UPDATE materias_docentes SET Id_hora_final = ? WHERE materias_docentes.Id_materias_asignadas = ? AND materias_docentes.Estado = "Activo"',(self.selecionarFilaHoraFinal(),self.selecionarFilaGestionar()))
		same = self.conexion('SELECT * FROM materias_laboratorios WHERE materias_laboratorios.Id_materias_asignadas = ? AND materias_laboratorios.Estado = "Activo"',(self.selecionarFilaGestionar(),)).fetchall()
		if same:
			self.conexion('DELETE FROM materias_laboratorios WHERE materias_laboratorios.Id_materias_asignadas = ?', (self.selecionarFilaGestionar(),))
		messagebox.showinfo(title='Info', message='Registro editado correctamente.')
		self.MostrarDatosGestionar()

	def editarSi(self):
		self.conexion('UPDATE materias_asignadas SET Id_lapso_academico = ? WHERE materias_asignadas.Id = ? AND materias_asignadas.Estado = "Activo"',(self.selecionarFilaLapsoAcademico(),self.selecionarFilaGestionar()))
		self.conexion('UPDATE materias_asignadas SET Id_cohorte = ? WHERE materias_asignadas.Id = ? AND materias_asignadas.Estado = "Activo"',(self.selecionarFilaCohorte(),self.selecionarFilaGestionar()))
		self.conexion('UPDATE materias_asignadas SET Id_trayecto = ? WHERE materias_asignadas.Id = ? AND materias_asignadas.Estado = "Activo"',(self.selecionarFilaTrayecto(),self.selecionarFilaGestionar()))
		self.conexion('UPDATE materias_asignadas SET Id_trimestre = ? WHERE materias_asignadas.Id = ? AND materias_asignadas.Estado = "Activo"',(self.selecionarFilaTrimestre(),self.selecionarFilaGestionar()))
		self.conexion('UPDATE materias_asignadas SET Id_seccion = ? WHERE materias_asignadas.Id = ? AND materias_asignadas.Estado = "Activo"',(self.selecionarFilaSeccion(),self.selecionarFilaGestionar()))
		self.conexion('UPDATE materias_asignadas SET Id_modalidad = ? WHERE materias_asignadas.Id = ? AND materias_asignadas.Estado = "Activo"',(self.selecionarFilaTurno(),self.selecionarFilaGestionar()))
		self.conexion('UPDATE materias_asignadas SET Id_semana = ? WHERE materias_asignadas.Id = ? AND materias_asignadas.Estado = "Activo"',(self.selecionarFilaDia(),self.selecionarFilaGestionar()))
		self.conexion('UPDATE materias_asignadas SET Id_hora_inicial = ? WHERE materias_asignadas.Id = ? AND materias_asignadas.Estado = "Activo"',(self.selecionarFilaHoraInicial(),self.selecionarFilaGestionar()))
		self.conexion('UPDATE materias_asignadas SET Id_hora_final = ? WHERE materias_asignadas.Id = ? AND materias_asignadas.Estado = "Activo"',(self.selecionarFilaHoraFinal(),self.selecionarFilaGestionar()))
		self.conexion('UPDATE materias_asignadas SET Id_unidad_curricular = ? WHERE materias_asignadas.Id = ? AND materias_asignadas.Estado = "Activo"',(self.selecionarFilaUnidadCurricular(),self.selecionarFilaGestionar()))
		self.conexion('UPDATE materias_docentes SET Id_lapso_academico = ? WHERE materias_docentes.Id_materias_asignadas = ? AND materias_docentes.Estado = "Activo"',(self.selecionarFilaLapsoAcademico(),self.selecionarFilaGestionar()))
		self.conexion('UPDATE materias_docentes SET Id_modalidad = ? WHERE materias_docentes.Id_materias_asignadas = ? AND materias_docentes.Estado = "Activo"',(self.selecionarFilaTurno(),self.selecionarFilaGestionar()))
		materiaDocente = ('Cohorte ' + str(self.dataCohorte()) + ' Trayecto ' + str(self.dataTrayecto()) + ' Trimestre ' + str(self.dataTrimestre()) + ' Sección ' + str(self.dataSeccion()) + ' ' + str(self.dataUnidadCurricular()))
		self.conexion('UPDATE materias_docentes SET materia = ? WHERE materias_docentes.Id_materias_asignadas = ? AND materias_docentes.Estado = "Activo"',(materiaDocente,self.selecionarFilaGestionar()))
		self.conexion('UPDATE materias_docentes SET Id_semana = ? WHERE materias_docentes.Id_materias_asignadas = ? AND materias_docentes.Estado = "Activo"',(self.selecionarFilaDia(),self.selecionarFilaGestionar()))
		self.conexion('UPDATE materias_docentes SET Id_hora_inicial = ? WHERE materias_docentes.Id_materias_asignadas = ? AND materias_docentes.Estado = "Activo"',(self.selecionarFilaHoraInicial(),self.selecionarFilaGestionar()))
		self.conexion('UPDATE materias_docentes SET Id_hora_final = ? WHERE materias_docentes.Id_materias_asignadas = ? AND materias_docentes.Estado = "Activo"',(self.selecionarFilaHoraFinal(),self.selecionarFilaGestionar()))
		same = self.conexion('SELECT * FROM materias_laboratorios WHERE materias_laboratorios.Id_materias_asignadas = ? AND materias_laboratorios.Estado = "Activo"',(self.selecionarFilaGestionar(),)).fetchall()
		if same:
			self.conexion('UPDATE materias_laboratorios SET Id_laboratorio = ? WHERE materias_laboratorios.Id_materias_asignadas = ? AND materias_laboratorios.Estado = "Activo"',(self.selecionarFilaLaboratorio(),self.selecionarFilaGestionar()))
			self.conexion('UPDATE materias_laboratorios SET Id_lapso_academico = ? WHERE materias_laboratorios.Id_materias_asignadas = ? AND materias_laboratorios.Estado = "Activo"',(self.selecionarFilaLapsoAcademico(),self.selecionarFilaGestionar()))
			self.conexion('UPDATE materias_laboratorios SET Id_modalidad = ? WHERE materias_laboratorios.Id_materias_asignadas = ? AND materias_laboratorios.Estado = "Activo"',(self.selecionarFilaTurno(),self.selecionarFilaGestionar()))
			materiaDocente = ('Cohorte ' + str(self.dataCohorte()) + ' Trayecto ' + str(self.dataTrayecto()) + ' Trimestre ' + str(self.dataTrimestre()) + ' Sección ' + str(self.dataSeccion()) + ' ' + str(self.dataUnidadCurricular()))
			self.conexion('UPDATE materias_laboratorios SET materia = ? WHERE materias_laboratorios.Id_materias_asignadas = ? AND materias_laboratorios.Estado = "Activo"',(materiaDocente,self.selecionarFilaGestionar()))
			self.conexion('UPDATE materias_laboratorios SET Id_semana = ? WHERE materias_laboratorios.Id_materias_asignadas = ? AND materias_laboratorios.Estado = "Activo"',(self.selecionarFilaDia(),self.selecionarFilaGestionar()))
			self.conexion('UPDATE materias_laboratorios SET Id_hora_inicial = ? WHERE materias_laboratorios.Id_materias_asignadas = ? AND materias_laboratorios.Estado = "Activo"',(self.selecionarFilaHoraInicial(),self.selecionarFilaGestionar()))
			self.conexion('UPDATE materias_laboratorios SET Id_hora_final = ? WHERE materias_laboratorios.Id_materias_asignadas = ? AND materias_laboratorios.Estado = "Activo"',(self.selecionarFilaHoraFinal(),self.selecionarFilaGestionar()))
		else:
			materiaDocente = ('Cohorte ' + str(self.dataCohorte()) + ' Trayecto ' + str(self.dataTrayecto()) + ' Trimestre ' + str(self.dataTrimestre()) + ' Sección ' + str(self.dataSeccion()) + ' ' + str(self.dataUnidadCurricular()))
			self.conexion('INSERT INTO materias_laboratorios VALUES (NULL,?,?,?,?,?,?,?,?,?,"Activo")',(self.selecionarFilaGestionar(),self.seleccion,self.selecionarFilaLaboratorio(),self.selecionarFilaLapsoAcademico(),self.selecionarFilaTurno(),materiaDocente,self.selecionarFilaDia(),self.selecionarFilaHoraInicial(),self.selecionarFilaHoraFinal()))
		messagebox.showinfo(title='Info', message='Registro editado correctamente.')