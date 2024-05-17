import json
import cifrado as cif

# Funcion para guardar los registros de los usuarios con su llave publica y privada
def guardarRegistro(usuario, publicKeyHex, privateKeyHex):
    # Verifica que el archivo exista o no. Si existe lo abre en modo lectura y escritura, si no lo crea
    try:
        with open("bd.json", "r") as bd:
            data = json.load(bd)  # Carga la informacion del archivo en la variable data
    except FileNotFoundError:
        data = {}  # Si no existe el archivo, crea un diccionario vacio
    
    # Verifica que no exista un registro con el mismo user
    for i in data:
        if usuario in data[i]:
            print("Ya existe un usuario con ese nombre")
            return
    # Continua en caso de que no exista el usuario
    # Agrega al diccionario data el usuario con su llave publica y privada solo poniendolo al final
    data[str(len(data))] = {usuario: {"publicKey": publicKeyHex, "privateKey": privateKeyHex}}

    # Guarda los datos actualizados en el archivo "bd.json"
    with open("bd.json", "w") as bd:
        json.dump(data, bd)

# Funcion para leer los registros de los usuarios con sus llaves
def leerRegistro(usuario):
    with open("bd.json", "r") as bd:
        data = json.load(bd)
        for i in data:
            if usuario in data[i]:
                return data[i][usuario]
        return None  # Devuelve None si no encuentra el usuario

# Funcion que verifica si un usuario esta registrado con su llave privada 
def verificarUsuario(usuario, privateKeyHex):
    userData = leerRegistro(usuario)
    if userData is not None and userData["privateKey"] == privateKeyHex:
        return True
    else:
        return False


# Funcion que devuelve la llave publica de un usuario
def obtenerPublicKey(usuario):
    with open("bd.json", "r") as bd:
        data = json.load(bd)
        return data[usuario]['publicKey']

# Funcion para guardar el registro de los datos con el user, el correo, el nombre, y la contraseña
def guardarDatos(usuario, correo, nombre, contrasena):
    # Verifica que el archivo exista o no. Si existe lo abre en modo lectura y escritura, si no lo crea
    try:
        with open("reg.json", "r") as bd:
            data = json.load(bd)  # Carga la informacion del archivo en la variable data
    except FileNotFoundError:
        data = []  # Si no existe el archivo, crea un diccionario vacio
    
    # Agrega al arreglo data los datos del registro
    data.append({"usuario": usuario, "correo": correo, "nombre": nombre, "contrasena": contrasena})

    # Guarda los datos actualizados en el archivo "bd.json"
    with open("reg.json", "w") as bd:
        json.dump(data, bd)

# Funcion para leer los registros de los datos con el user
def leerDatos(usuario):
    with open("reg.json", "r") as bd:
        data = json.load(bd)
        registros = []
        for i in data:
            if usuario in i['usuario']:
                registros.append(i)
        if len(registros) > 0:
            return registros
        else:
            print('No se encontraron coincidencias')
            return None  # Devuelve None si no encuentra el usuario

# Funcion para eliminar un registro de datos
def eliminarDatos(usuario, nombre):
    with open("reg.json", "r") as bd:
        data = json.load(bd)
        for i in data:
            if usuario in i['usuario'] and nombre in i['nombre']:
                data.remove(i)
                with open("reg.json", "w") as bd:
                    json.dump(data, bd)
                return True
        return False  # Devuelve False si no encuentra el usuario a eliminar

# Prueba para cifrar los archivos
#cif.cifrado("bd.json", cif.cargarClave())
#cif.descifrado("bd.json", cif.cargarClave())
# Prueba de las funciones
#"""
usuario = "abraham"
publicKeyHex = "123"

with open("keys/private.pem", "rt") as llavePrivada:
    privateKey = llavePrivada.read()
#"""   

#guardarRegistro(usuario, publicKeyHex, privateKey)

print(verificarUsuario(usuario, "0x9679e35fc49d853ca07539e5a18964a77586b5dbf9bf0d426651e510a7e25627"))  #Deberia imprimir True

#guardarDatos("pedro", "alfjalsd", "uanl", "123")
#print(leerDatos("pedro"))
#eliminarDatos("pedro", "uanl")
#print(leerDatos("pedro"))
