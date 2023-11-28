import tkinter as tk
import socket
import sys
import subprocess
from tkinter import messagebox

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sv_addr = ('localhost', 5000)
print(f'connecting to {sv_addr[0]} to port {sv_addr[1]}')
sock.connect(sv_addr)

# Función de inicio de sesión
def login():
    correo = entry_correo.get()
    contrasena = entry_contrasena.get()

    if correo and contrasena:
     message = f'login{correo} {contrasena}'
     data= '{:05d}'.format(len(message))+message
     sock.sendall(bytes(data, 'latin-1'))
     success = sock.recv(17).decode()
     print(success)
     
     if 'True' in success:
         messagebox.showinfo("Inicio de sesión exitoso", "¡Bienvenido!")
         root.destroy()
         subprocess.run(["python", "guiMenu.py"])
     elif 'False' in success:
         messagebox.showerror("Error de inicio de sesión", "Servicio no habilitado")
     else:
         messagebox.showerror("Error de inicio de sesión", "Credenciales incorrectas. Inténtalo de nuevo.")

def register():
    # Cerrar la ventana actual
    root.destroy()
    
    # Ejecutar el programa de registro
    subprocess.run(["python", "createUser.py"])

def back():
    # Cerrar la ventana actual
    root.destroy()
    
    # Ejecutar el programa de registro
    subprocess.run(["python", "guiAuth.py"])

# Crear la ventana principal
root = tk.Tk()
root.title("Inicio de sesión")

# Botón de inicio de sesión
go_back = tk.Button(root, text="Volver", command=back)
go_back.pack()

# Crear etiquetas y entradas para correo y contraseña
label_correo = tk.Label(root, text="Correo:")
label_correo.pack()
entry_correo = tk.Entry(root)
entry_correo.pack()

label_contrasena = tk.Label(root, text="Contraseña:")
label_contrasena.pack()
entry_contrasena = tk.Entry(root, show="*")  # El texto de la contraseña se oculta con asteriscos
entry_contrasena.pack()

# Botón de inicio de sesión
login_button = tk.Button(root, text="Iniciar sesión", command=login)
login_button.pack()

# Botón de inicio de sesión
register_button = tk.Button(root, text="Registrarse", command=register)
register_button.pack()


# Ejecutar el bucle principal de la aplicación
root.mainloop()
