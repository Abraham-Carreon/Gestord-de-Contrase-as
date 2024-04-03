from cryptography.fernet import Fernet

def generaClave():
	clave = Fernet.generate_key()
	with open("clave.key","wb") as archivo_clave:
		archivo_clave.write(clave)

def cargarClave():
	return open("clave.key","rb").read()

clave = cargarClave()

# Inicio de Fernet
f = Fernet(clave)

# Encriptar Archivo
def crifrado(nom, clave):
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
#"""
clave = cargarClave()
nom = "prueba.txt"
descifrado(nom, clave)
#"""



