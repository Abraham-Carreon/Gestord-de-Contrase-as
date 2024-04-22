from cryptography.fernet import Fernet
import os

def generaClave():
    # Revisar que exista una clave, sino la crea
    try:
        open("c/clave.key", "r")
    except FileNotFoundError:
        os.mkdir("c")
        clave = Fernet.generate_key()
        with open("c/clave.key","wb") as archivo_clave:
            archivo_clave.write(clave)

def cargarClave():
	return open("c/clave.key","rb").read()

generaClave()
clave = cargarClave()

# Inicio de Fernet
f = Fernet(clave)

# Encriptar Archivo
def cifrado(nom, clave):
    f = Fernet(clave)   
    with open(nom, "rb") as file:
        info = file.read()
    infoEncriptada = f.encrypt(info)
    with open(nom, "wb") as file:
        file.write(infoEncriptada)

# Desencriptar Archivo
def descifrado(nom, clave):
    f = Fernet(clave)
    with open(nom, "rb") as file:
        infoEncriptada = file.read()
    info = f.decrypt(infoEncriptada)
    with open(nom, "wb") as file:
        file.write(info)

# Prueba 
# Cifrado
"""
clave = cargarClave()
nom = "prueba.txt"
cifrado(nom, clave)
"""

# Desencriptar
"""
clave = cargarClave()
nom = "prueba.txt"
descifrado(nom, clave)
"""