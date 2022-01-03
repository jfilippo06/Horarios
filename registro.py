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
        self.title('Carga Académica')
        self.geometry('485x400')
        self.resizable(width=0,height=0)
        self.iconbitmap(uptpc)