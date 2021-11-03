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
        self.treeHora.heading('#2', text = 'Horas')
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
        self.entryDepartamento = ttk.Entry(self.frameDEntry,width=15)
        self.entryDepartamento.grid(column=1,row=0)
        ttk.Button(self.frameDEntry, text='REGISTRAR DEPARTAMENTO', command='',width=26).grid(row=1,column=0)
        ttk.Button(self.frameDEntry, text='EDITAR DEPARTAMENTO', command='',width=26).grid(row=2,column=0)
        ttk.Button(self.frameDEntry, text='ELIMINAR DEPARTAMENTO', command='',width=26).grid(row=3,column=0)

        self.framePEntry = ttk.Labelframe(self.container)
        self.framePEntry.grid(column=4,row=0)
        ttk.Label(self.framePEntry,text='Pt').grid(column=0,row=0)
        self.entryPt = ttk.Entry(self.framePEntry,width=15)
        self.entryPt.grid(column=1,row=0)
        ttk.Button(self.framePEntry, text='REGISTRAR PT', command='',width=15).grid(row=1,column=0)
        ttk.Button(self.framePEntry, text='EDITAR PT', command='',width=15).grid(row=2,column=0)
        ttk.Button(self.framePEntry, text='ELIMINAR PT', command='',width=15).grid(row=3,column=0)

        self.frameUnidadesCurriculares = ttk.Labelframe(self)
        self.frameUnidadesCurriculares.grid(column=0,row=1,padx=5)
        self.treeUnidadesCurriculares = ttk.Treeview(self.frameUnidadesCurriculares, columns=['#1',"#2",'#3','#4','#5'],show='headings',height=10)
        self.treeUnidadesCurriculares.grid(row=0,column=0)
        self.treeUnidadesCurriculares.heading('#1', text = 'Id',)
        self.treeUnidadesCurriculares.heading('#2', text = 'Unidad Curricular')
        self.treeUnidadesCurriculares.heading('#3', text = 'Horas')
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