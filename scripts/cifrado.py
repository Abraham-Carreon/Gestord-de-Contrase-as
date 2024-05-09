from cryptography.fernet import Fernet
import os

rot13 = str.maketrans(
    'ABCDEFGHIJKLMabcdefghijklmNOPQRSTUVWXYZnopqrstuvwxyz',
    'NOPQRSTUVWXYZnopqrstuvwxyzABCDEFGHIJKLMabcdefghijklm')

def generaClave():
    # Revisar que exista una clave, sino la crea
    try:
        open("c/clave.key", "r")
    except FileNotFoundError:
        os.mkdir("c")
        clave = Fernet.generate_key()
        with open("c/clave.key","wb") as archivo_clave:
            clave.translate(rot13)
            archivo_clave.write(clave)
            
# Carga la clave y le quita el rot13 para poder usarlo
def cargarClave():
    with open("c/clave.key","rb") as archivo_clave:
        clave = archivo_clave.read()
        clave = clave.decode()
        clave = clave.translate(rot13)
        return clave.encode()

# Encriptar Archivo
def cifrado(nom, clave):
    generaClave()
    clave = cargarClave()
    f = Fernet(clave)   
    with open(nom, "rb") as file:
        info = file.read()
    infoEncriptada = f.encrypt(info)
    with open(nom, "wb") as file:
        file.write(infoEncriptada)

# Desencriptar Archivo
def descifrado(nom, clave):
    generaClave()
    clave = cargarClave()
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