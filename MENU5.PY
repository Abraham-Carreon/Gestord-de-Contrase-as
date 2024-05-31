from tkinter import *
from tkinter import messagebox
from asimetrico import generarCertificado, leerLlavePublica
from bd import guardarRegistro, verificarUsuario, guardarDatos, eliminarDatos, leerDatos
from cifrado import cargarClave, cifrado, descifrado, generaClave
import os

def mostrar_mensaje(titulo, mensaje):
    messagebox.showinfo(titulo, mensaje)

def mostrar_error(titulo, mensaje):
    messagebox.showerror(titulo, mensaje)

def ventana_registro():
    def registrar_usuario():
        usuario = entry_usuario.get()
        password = entry_password.get()
        private_key, public_key = generarCertificado(password)
        generaClave()
        if os.path.exists("bd.json"):
            descifrado("bd.json", cargarClave())
        try:
            if guardarRegistro(usuario, public_key, private_key):
                mostrar_mensaje("Registro", "Usuario registrado exitosamente, recuerde guardar su llave privada")
            else:
                mostrar_error("Error", "El usuario ya existe, elige otro nombre de usuario")
        except Exception as e:
            mostrar_error("Error", str(e))
        finally:
            if os.path.exists("bd.json"):
                cifrado("bd.json", cargarClave())

    ventana_registro = Toplevel(root)
    ventana_registro.title("Registro de Usuario")
    Label(ventana_registro, text="Usuario").grid(row=0, column=0)
    Label(ventana_registro, text="Contraseña").grid(row=1, column=0)
    entry_usuario = Entry(ventana_registro)
    entry_password = Entry(ventana_registro, show="*")
    entry_usuario.grid(row=0, column=1)
    entry_password.grid(row=1, column=1)
    Button(ventana_registro, text="Registrar", command=registrar_usuario).grid(row=2, columnspan=2)

def iniciar_sesion(usuario, privateKeyHex):
    descifrado("bd.json", cargarClave())  # Descifrar el archivo antes de verificar el usuario
    if verificarUsuario(usuario, privateKeyHex):
        messagebox.showinfo("Inicio de sesión", "Inicio de sesión exitoso")
        cifrado("bd.json", cargarClave())
        ventana_opciones(usuario)
        
    else:
        cifrado("bd.json", cargarClave())  # Volver a cifrar el archivo si la verificación falla
        messagebox.showerror("Error", "Usuario o clave incorrecta")

def ventana_inicio_sesion():
    ventana_inicio_sesion = Toplevel(root)
    ventana_inicio_sesion.title("Inicio de Sesión")

    Label(ventana_inicio_sesion, text="Usuario:").pack()
    entry_usuario_sesion = Entry(ventana_inicio_sesion)
    entry_usuario_sesion.pack()

    Label(ventana_inicio_sesion, text="Clave privada:").pack()
    entry_clave_privada_sesion = Entry(ventana_inicio_sesion, show="*")
    entry_clave_privada_sesion.pack()
    Button(ventana_inicio_sesion, text="Iniciar sesión", 
           command=lambda: iniciar_sesion(entry_usuario_sesion.get(), entry_clave_privada_sesion.get())).pack()

def ventana_opciones(usuario):
    def guardar_datos():
        ventana_guardar = Toplevel(root)
        ventana_guardar.title("Guardar Datos")
        Label(ventana_guardar, text="Correo:").pack()
        entry_correo = Entry(ventana_guardar)
        entry_correo.pack()

        Label(ventana_guardar, text="Nombre:").pack()
        entry_nombre = Entry(ventana_guardar)
        entry_nombre.pack()

        Label(ventana_guardar, text="Contraseña:").pack()
        entry_contrasena = Entry(ventana_guardar, show="*")
        entry_contrasena.pack()

        def guardar():
            correo = entry_correo.get()
            nombre = entry_nombre.get()
            contrasena = entry_contrasena.get()
            if os.path.exists("reg.json"):
                descifrado("reg.json", cargarClave())
            guardarDatos(usuario, correo, nombre, contrasena)
            cifrado("reg.json", cargarClave())
            mostrar_mensaje("Guardar Datos", "Datos guardados exitosamente")
            ventana_guardar.destroy()

        Button(ventana_guardar, text="Guardar", command=guardar).pack()

    def mostrar_datos():
        ventana_mostrar = Toplevel(root)
        ventana_mostrar.title("Mostrar Datos")
        if os.path.exists("reg.json"):
            descifrado("reg.json", cargarClave())
            datos = leerDatos(usuario)
            cifrado("reg.json", cargarClave())
            if datos:
                for dato in datos:
                    Label(ventana_mostrar, text=f"Correo: {dato['correo']}").pack()
                    Label(ventana_mostrar, text=f"Nombre: {dato['nombre']}").pack()
                    Label(ventana_mostrar, text=f"Contraseña: {dato['contrasena']}").pack()
            else:
                mostrar_error("Error", "No se encontraron datos para el usuario")
        else:
            mostrar_error("Error", "El archivo reg.json no existe")

    def borrar_datos():
        ventana_eliminar = Toplevel(root)
        ventana_eliminar.title("Eliminar Datos")
        Label(ventana_eliminar, text="Nombre:").pack()
        entry_nombre = Entry(ventana_eliminar)
        entry_nombre.pack()

        def eliminar():
            nombre = entry_nombre.get()
            if os.path.exists("reg.json"):
                descifrado("reg.json", cargarClave())
            if eliminarDatos(usuario, nombre):
                mostrar_mensaje("Eliminar Datos", "Datos eliminados exitosamente")
            else:
                mostrar_error("Error", "No se encontraron datos para eliminar")
            cifrado("reg.json", cargarClave())
            ventana_eliminar.destroy()

        Button(ventana_eliminar, text="Eliminar", command=eliminar).pack()

    ventana_opciones = Toplevel(root)
    ventana_opciones.title("Opciones del Usuario")
    Button(ventana_opciones, text="Guardar Datos", command=guardar_datos).pack()
    Button(ventana_opciones, text="Mostrar Datos", command=mostrar_datos).pack()
    Button(ventana_opciones, text="Eliminar Datos", command=borrar_datos).pack()

root = Tk()
root.title("Sistema de Registro y Cifrado")

Button(root, text="Registrar", command=ventana_registro).pack()

Button(root, text="Iniciar sesión", command=ventana_inicio_sesion).pack()

root.mainloop()
