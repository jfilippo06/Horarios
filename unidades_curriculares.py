import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3
from rutas import *
import traceback
import sys

class unidades_curriculares(tk.Toplevel):
    def __init__(self,master):
        super().__init__(master)
        # Config:
        self.title('Unidades Curriculares')
        self.geometry('800x450')
        self.resizable(width=0, height=0)
        self.iconbitmap(uptpc)