from tkinter import *
from tkinter import messagebox
from asimetrico import generarCertificado, leerLlavePublica
from bd import guardarRegistro, verificarUsuario, guardarDatos, eliminarDatos
import cifrado as cif
from cifrado import cargarClave, cifrado, descifrado, cargarClave, generaClave

def registro():
    usuario = entry_usuario.get()
    password = entry_password.get()

    if password and usuario:
        privateKeyHex, publicKeyHex = generarCertificado(password)
        guardarRegistro(usuario, publicKeyHex, privateKeyHex)
        messagebox.showinfo("Registro exitoso", f"Recuerde guardar su llave privada para iniciar sesion: {privateKeyHex}")
    else:
        messagebox.showerror("Error", "Ingrese un usuario y contraseña válidos")

def iniciar_sesion():
    privateKeyHex = entry_clave_privada.get()
    usuario = entry_usuario.get()
    if verificarUsuario(usuario, privateKeyHex):
        messagebox.showinfo("Inicio de sesión", "Inicio de sesión exitoso")
        opcion = entry_opcion.get()
        guardar_opcion(opcion)  
        if opcion == "1":
            ventana_guardar(usuario)
        elif opcion == "2":
            ventana_borrar(usuario)
        elif opcion == "3":
            ventana_cifrar_descifrar(usuario)
        else:
            messagebox.showerror("Error", "Opción inválida")
    else:
        messagebox.showerror("Error", "Usuario o clave incorrecta")

def guardar_opcion(opcion):
    with open("opcion.txt", "w") as file:
        file.write(opcion)

def ventana_guardar(usuario):
    top = Toplevel()
    top.title("Guardar Datos")

    Label(top, text="Correo:").pack()
    entry_correo = Entry(top)
    entry_correo.pack()

    Label(top, text="Nombre:").pack()
    entry_nombre = Entry(top)
    entry_nombre.pack()

    Label(top, text="Contraseña:").pack()
    entry_contrasena = Entry(top, show="*")
    entry_contrasena.pack()

    Button(top, text="Guardar", command=lambda: guardar_datos(usuario, entry_correo.get(), entry_nombre.get(), entry_contrasena.get())).pack()

def ventana_borrar(usuario):
    top = Toplevel()
    top.title("Borrar Datos")

    Label(top, text="Nombre:").pack()
    entry_nombre = Entry(top)
    entry_nombre.pack()

    Button(top, text="Borrar", command=lambda: borrar_datos(usuario, entry_nombre.get())).pack()

def ventana_cifrar_descifrar(usuario):
    top = Toplevel()
    top.title("Cifrar o Descifrar Archivo")

    Label(top, text="Nombre del archivo:").pack()
    entry_nombre_archivo = Entry(top)
    entry_nombre_archivo.pack()

    Button(top, text="Cifrar", command=lambda: cifrar_archivo(entry_nombre_archivo.get())).pack()
    Button(top, text="Descifrar", command=lambda: descifrar_archivo(entry_nombre_archivo.get())).pack()

def guardar_datos(usuario, correo, nombre, contrasena):
    guardarDatos(usuario, correo, nombre, contrasena)
    messagebox.showinfo("Datos guardados", "Datos guardados exitosamente")

def borrar_datos(usuario, nombre):
    opcion = messagebox.askquestion("Borrar datos", "¿Está seguro de que desea borrar sus datos?")
    if opcion == "yes":
        eliminarDatos(usuario, nombre)
        messagebox.showinfo("Datos eliminados", "Datos eliminados exitosamente")
    else:
        messagebox.showinfo("Operación cancelada", "Operación cancelada")

def cifrar_archivo(nombre_archivo):
    generaClave()
    clave = cargarClave()
    if clave:
        cifrado(nombre_archivo, clave)
        messagebox.showinfo("Archivo cifrado", f"El archivo {nombre_archivo} ha sido cifrado correctamente.")

def descifrar_archivo(nombre_archivo):
    clave = cargarClave()
    if clave:
        descifrado(nombre_archivo, clave)
        messagebox.showinfo("Archivo descifrado", f"El archivo {nombre_archivo} ha sido descifrado correctamente.")

root = Tk()
root.title("Sistema de Registro y Cifrado")

Label(root, text="Usuario:").pack()
entry_usuario = Entry(root)
entry_usuario.pack()

Label(root, text="Contraseña:").pack()
entry_password = Entry(root, show="*")
entry_password.pack()

Button(root, text="Registrar", command=registro).pack()

Label(root, text="Clave privada:").pack()
entry_clave_privada = Entry(root, show="*")
entry_clave_privada.pack()

Label(root, text="Opción (1. Guardar / 2. Borrar / 3. Cifrar):").pack()
entry_opcion = Entry(root)
entry_opcion.pack()

Button(root, text="Iniciar sesión", command=iniciar_sesion).pack()

root.mainloop()

