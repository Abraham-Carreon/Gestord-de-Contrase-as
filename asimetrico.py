# Librerias para el cifrado asimetrico
from ecies.utils import generate_eth_key, generate_key
from ecies import encrypt, decrypt
from cryptography.fernet import Fernet
import binascii
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet, InvalidToken
import os

def generateKey(pswd):
    password = pswd.encode()  
    salt = b'\x94+\x19\x0bF1\x10\xe0\xe0#\x16\xcd\x7f\x86pg'
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password))  
    return key

# Funcion para guardar la llave privada cifrada con fernet por una contraseña ingresada
def guardarLlavePrivada(privateKeyHex, password):
    with open("keys/private.pem", "wt") as llavePrivada:
        f = Fernet(password)
        privateKey = privateKeyHex.encode()
        llavePrivada.write(privateKey.decode())

# Funcion para guardar la llave publica
def guardarLLavePublica(publicKeyHex):
    with open("keys/public.pem", "wt") as llavePublica:
        llavePublica.write(publicKeyHex)

# Funcion para leer la llave privada, se ingresa la contraseña para descifrarla
def leerLlavePrivada(password):
    with open("keys/private.pem", "rt") as llavePrivada:
        key = generateKey(password)
        f = Fernet(key)
        privateKey = f.decrypt(llavePrivada.read().encode())
        privKeyHex = privateKey.decode()
        return privKeyHex

# Funcion para leer la llave publica
def leerLlavePublica():
    with open("keys/public.pem", "rt") as llavePublica:
        return llavePublica.read()

# Funcion para generar un certificado, se ingresa una contraseña para al guardar la llave privada este cifrada
def generarCertificado(password):
    # Revisa si existe la carpeta keys, si no la crea
    if not os.path.exists('keys'):
        os.makedirs('keys')
    
    # Generar llave privada
    privKey = generate_eth_key()
    privKeyHex = privKey.to_hex()
    #print(privKeyHex)
    # Genera la key para el cifrado
    key = generateKey(password)
    
    # Generar llave publica
    pubKeyHex = privKey.public_key.to_hex()

    # Guardar la llave privada
    guardarLlavePrivada(privKeyHex, key)

    # Guardar la llave publica
    guardarLLavePublica(pubKeyHex)

    return privKeyHex, pubKeyHex

# Funcion para cifrar con la llave publica
def cifrado(texto, publicKeyHex):
    encrypted = encrypt(publicKeyHex, texto)
    return encrypted

# Funcion para descifrar con la llave privada
def descifrado(cifrado, privateKeyHex):
    decrypted = decrypt(privateKeyHex, cifrado)
    return decrypted
