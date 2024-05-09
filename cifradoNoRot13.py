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
    with open("c/clave.key","rb") as archivo_clave:
        clave = archivo_clave.read()
        return clave

def cifrado(nom, clave):
    f = Fernet(clave)   
    with open(nom, "rb") as file:
        info = file.read()
    infoEncriptada = f.encrypt(info)
    with open(nom, "wb") as file:
        file.write(infoEncriptada)

def descifrado(nom, clave):
    f = Fernet(clave)
    with open(nom, "rb") as file:
        infoEncriptada = file.read()
    info = f.decrypt(infoEncriptada)
    with open(nom, "wb") as file:
        file.write(info)

generaClave()
clave = cargarClave()


