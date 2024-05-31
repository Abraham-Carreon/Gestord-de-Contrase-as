
from cryptography.fernet import Fernet
import os

rot13 = str.maketrans(
    'ABCDEFGHIJKLMabcdefghijklmNOPQRSTUVWXYZnopqrstuvwxyz',
    'NOPQRSTUVWXYZnopqrstuvwxyzABCDEFGHIJKLMabcdefghijklm')

def generaClave():
    # Verificar si el directorio 'c' existe, si no, crearlo
    if not os.path.exists("c"):
        os.mkdir("c")
        generaClave()

    clave_file = "c/clave.key"
    # Verificar si el archivo de clave ya existe
    if not os.path.exists(clave_file):
        # Generar la clave
        clave_bytes = Fernet.generate_key()
        clave_str = clave_bytes.decode()  # Convertir bytes a str
        clave_str_rot13 = clave_str.translate(rot13)  # Aplicar rot13 a la clave en formato str
        with open(clave_file, "wb") as archivo_clave:
            archivo_clave.write(clave_str_rot13.encode())  # Escribir la clave codificada en formato bytes
            print("Archivo de clave generado exitosamente.")
    else:
        print("El archivo de clave ya existe.")
            
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
