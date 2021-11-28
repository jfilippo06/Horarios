import os

# Principal
rutaPrincipal = 'C:/MisProyectos/Python/Proyecto'

# ICO
ico = 'IMG/uptpc.ico'
uptpc = os.path.join(rutaPrincipal, ico)
uptpc = os.path.abspath(uptpc)

# Fondo
fondoDPantalla = 'IMG/fondo.png'
fondo = os.path.join(rutaPrincipal, fondoDPantalla)
fondo = os.path.abspath(fondo)

# Base de datos
routebd = 'tecnologico.db'
baseDeDatos = os.path.join(rutaPrincipal,routebd)
baseDeDatos = os.path.abspath(baseDeDatos)

# logo PDF
logo = 'IMG/uptpc.jpg'
logoPDF = os.path.join(rutaPrincipal,logo)
logoPDF = os.path.abspath(logoPDF)

# Fondo Login
logo = 'IMG/azul.png'
login = os.path.join(rutaPrincipal,logo)
login_fondo = os.path.abspath(login)
