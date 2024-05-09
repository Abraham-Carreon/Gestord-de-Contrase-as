from coincurve.keys import PrivateKey
from asimetrico import generarCertificado, leerLlavePublica
from bd import guardarRegistro, verificarUsuario
def registro():
  password = input("ingrese su contraseña: ")
  usuario = input("ingrese su usuario: ")
  if password and usuario:
    privateKeyHex = generarCertificado(password)
    publicKeyHex = password
    guardarRegistro(usuario, publicKeyHex, privateKeyHex)
    print("registro exitoso")
    print("Encryption public key:", publicKeyHex)
    print("Decryption private key:", privateKeyHex)
    
  else:
    print("ingrese un usuario o contraseña valido")

def iniciar_sesion():
  privateKeyHex = input("ingrese su clave privada: ")
  usuario = input("ingrese su usuario: ")
  verificarUsuario(usuario, privateKeyHex)
  
  if verificarUsuario is True:
    print("inicio de sesion exitoso")
  else:
    print("usuario o clave incorrecta")
    






registro()
iniciar_sesion()

