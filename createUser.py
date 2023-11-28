import tkinter as tk
import geocoder
import socket
import sys
import subprocess
import re
from tkinter import messagebox

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sv_addr = ('localhost', 5000)
print(f'connecting to {sv_addr[0]} to port {sv_addr[1]}')
sock.connect(sv_addr)

def validar_telefono(entrada):
    # Permitir solo '+' y números
    return re.match(r'^\+?\d{11}+$', entrada) is not None

def validar_correo(entrada):
    # Validar el formato del correo electrónico
    return re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', entrada) is not None

def get_location():
    g = geocoder.ip('me')
    if g.city and g.country:
        return f"{g.city}, {g.country}"
    return "Ubicación no encontrada"

def submit():
    nombre = entry_nombre.get()
    email= entry_correo.get()
    password= entry_contrasena.get()
    telefono= entry_telefono.get()
    localizacion= get_location()

    if nombre and email and password and telefono and localizacion:
        message= f'crear{nombre} {email} {password} {telefono} {localizacion}'
        data= '{:05d}'.format(len(message))+message
        sock.sendall(bytes(data, 'latin-1'))
        success = sock.recv(17).decode()
        if not validar_correo(email):
         messagebox.showerror('Falló', 'Correo Inválido')
         return
        if not validar_telefono(telefono):
         messagebox.showerror('Falló', 'Número Inválido')
         return
        if "True" in success:
         messagebox.showinfo('Exito', "Usuario registrado con éxito")
        elif "Mail" in success:
         messagebox.showerror('Falló', 'Ingrese otro correo')
        else:
         messagebox.showerror('Falló', 'Reintente nuevamente')
    else:
        messagebox.showwarning("Campos vacíos", "Por favor, rellene todos los campos antes de enviar.")

def back():
    # Cerrar la ventana actual
    root.destroy()
    
    # Ejecutar el programa de registro
    subprocess.run(["python", "guiAuth.py"])


# Crear la ventana principal
root = tk.Tk()
root.title("Formulario")

# Crear etiquetas y entradas para cada campo
label_nombre = tk.Label(root, text="Nombre completo:")
label_nombre.grid(row=0, column=0)
entry_nombre = tk.Entry(root)
entry_nombre.grid(row=0, column=1)

label_correo = tk.Label(root, text="Correo electrónico:")
label_correo.grid(row=1, column=0)
entry_correo = tk.Entry(root)
entry_correo.grid(row=1, column=1)

label_contrasena = tk.Label(root, text="Contraseña:")
label_contrasena.grid(row=2, column=0)
entry_contrasena = tk.Entry(root, show="*")
entry_contrasena.grid(row=2, column=1)

label_telefono = tk.Label(root, text="Teléfono:")
label_telefono.grid(row=3, column=0)
entry_telefono = tk.Entry(root)
entry_telefono.grid(row=3, column=1)

label_ubicacion = tk.Label(root, text="Ubicación:")
label_ubicacion.grid(row=4, column=0)
entry_ubicacion = tk.Entry(root)
entry_ubicacion.insert(0, get_location())
entry_ubicacion.grid(row=4, column=1)

# Botón para enviar el formulario
submit_button = tk.Button(root, text="Enviar", command=submit)
submit_button.grid(row=5, column=1)

# Botón de inicio de sesión
go_back = tk.Button(root, text="Volver", command=back)
go_back.grid(row=5, column=2)

# Ejecutar el bucle principal de la aplicación
root.mainloop()
