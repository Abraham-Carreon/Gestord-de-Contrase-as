# Librerias para el cifrado asimetrico
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding

# Utilizaremos el método "generate_private_key" para generar nuestra clave, se le asignan algunos parametros
private_key = rsa.generate_private_key(
     public_exponent=65537,
     key_size=2048,
     backend=default_backend()
)

# Se genera la clave pública
public_key = private_key.public_key()

# Se procede a firmar el mensaje con la clave privada
mensaje = b"Mensaje que se va a firmar"
firma = private_key.sign(
     mensaje,
     padding.PSS(
         mgf=padding.MGF1(hashes.SHA256()),
         salt_length=padding.PSS.MAX_LENGTH
     ),
     hashes.SHA256()
)


"""
Al intentar verificar el mensaje que no fue firmado con la misma firma, se marca un error
# Se genera la clave pública
public_key = private_key.public_key()
public_key2 = private_key.public_key()

# Se procede a firmar el mensaje con la clave privada
mensaje = b"Mensaje que se va a firmar"
mensaje2 = b"si"
firma = private_key.sign(
     mensaje,
     padding.PSS(
         mgf=padding.MGF1(hashes.SHA256()),
         salt_length=padding.PSS.MAX_LENGTH
     ),
     hashes.SHA256()
)
firma2 = private_key.sign(
     mensaje2,
     padding.PSS(
         mgf=padding.MGF1(hashes.SHA256()),
         salt_length=padding.PSS.MAX_LENGTH
     ),
     hashes.SHA256()
)
print(firma)
print(public_key.verify(
    firma2,
    mensaje,
    padding.PSS(
        mgf=padding.MGF1(hashes.SHA256()),
        salt_length=padding.PSS.MAX_LENGTH
    ),
    hashes.SHA256()
)) # Imprime True si la firma es correcta

"""

"""
Procedemos a cifrar el dato.
Para ello utilizaremos el método encrytp.
"""
#mensaje = b"Dato para cifrar"
textoCifrado = public_key.encrypt(
     mensaje,
     padding.OAEP(
         mgf=padding.MGF1(algorithm=hashes.SHA256()),
         algorithm=hashes.SHA256(),
         label=None
     )
 )
print(textoCifrado)
"""
Ahora vamos a descifrar el mensaje. Para ello utilizaremos el 
método decrypt.
"""
descifrado = private_key.decrypt(
     textoCifrado,
     padding.OAEP(
         mgf=padding.MGF1(algorithm=hashes.SHA256()),
         algorithm=hashes.SHA256(),
         label=None
     )
 )
 
print(descifrado)


# Guardar la clave
pem = private_key.private_bytes(
   encoding=serialization.Encoding.PEM,
   format=serialization.PrivateFormat.PKCS8,
   encryption_algorithm=serialization.BestAvailableEncryption(b'alv locotr')
)
pem.splitlines()[0]
with open("key.pem","wb") as llavePrivada:
		llavePrivada.write(pem)

# Leer la clave
with open("key.pem", "rb") as llavePrivada:
    llave = serialization.load_pem_private_key(
        llavePrivada.read(),
        password=b'alv locotr',
        backend=default_backend()
    )

# Prueba de que se leyo correctamente
print(llave)

descifrado = llave.decrypt(
     textoCifrado,
     padding.OAEP(
         mgf=padding.MGF1(algorithm=hashes.SHA256()),
         algorithm=hashes.SHA256(),
         label=None
     )
 )
 
print(descifrado)


