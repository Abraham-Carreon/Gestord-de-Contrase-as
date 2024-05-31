import json
import cifrado as cif
import os

def guardarRegistro(usuario, public_key, private_key):
    bd_file = 'bd.json'
    if not os.path.exists(bd_file):
        with open(bd_file, 'w') as file:
            json.dump([], file)
    
    with open(bd_file, 'r') as bd:
        try:
            data = json.load(bd)  # Carga la información del archivo en la variable data
        except json.JSONDecodeError:
            data = []
    
    for entry in data:
        if entry['usuario'] == usuario:
            return False

    data.append({
        'usuario': usuario,
        'public_key': public_key,
        'private_key': private_key
    })

    with open(bd_file, 'w') as bd:
        json.dump(data, bd)
    
    return True

def verificarUsuario(usuario, private_key):
    with open('bd.json', 'r') as bd:
        try:
            data = json.load(bd)
        except json.JSONDecodeError:
            return False
        
    for entry in data:
        if entry['usuario'] == usuario and entry['private_key'] == private_key:
            return True
    
    return False

def guardarDatos(usuario, correo, nombre, contrasena):
    reg_file = 'reg.json'
    if not os.path.exists(reg_file):
        with open(reg_file, 'w') as file:
            json.dump([], file)

    with open(reg_file, 'r') as reg:
        try:
            data = json.load(reg)
        except json.JSONDecodeError:
            data = []
    
    data.append({
        'usuario': usuario,
        'correo': correo,
        'nombre': nombre,
        'contrasena': contrasena
    })

    with open(reg_file, 'w') as reg:
        json.dump(data, reg)

def leerDatos(usuario):
    with open('reg.json', 'r') as reg:
        try:
            data = json.load(reg)
        except json.JSONDecodeError:
            return []

    user_data = [entry for entry in data if entry['usuario'] == usuario]
    return user_data

def eliminarDatos(usuario, nombre):
    with open('reg.json', 'r') as reg:
        try:
            data = json.load(reg)
        except json.JSONDecodeError:
            return False

    new_data = [entry for entry in data if not (entry['usuario'] == usuario and entry['nombre'] == nombre)]

    if len(new_data) == len(data):
        return False

    with open('reg.json', 'w') as reg:
        json.dump(new_data, reg)
    
    return True
