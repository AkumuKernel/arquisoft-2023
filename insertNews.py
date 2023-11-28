import tkinter as tk
from tkinter import messagebox
import subprocess
import socket
import sys

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sv_addr = ('localhost', 5000)
print(f'connecting to {sv_addr[0]} to port {sv_addr[1]}')
sock.connect(sv_addr)

# Función para enviar la noticia
def enviar_noticia():
    nombre_noticia = entry_nombre_noticia.get()
    red_social = entry_red_social.get()
    link_noticia = entry_link_noticia.get()
    tags = entry_tags.get()  # Si los tags están separados por comas
    
    if nombre_noticia and red_social and link_noticia and tags:
        message=f'addnt{nombre_noticia} {red_social} {link_noticia} {tags}'
        data= '{:05d}'.format(len(message))+message
        sock.sendall(bytes(data, 'latin-1'))
        success = sock.recv(17).decode()
        if 'True' in success:
         messagebox.showinfo('Exito', "Noticia insertada con éxito")
        else:
         messagebox.showerror('Error', 'Error al insertar noticia: Reintente')
    else:
        messagebox.showwarning("Campos vacíos", "Por favor, rellene todos los campos antes de enviar.")

def back():
    # Cerrar la ventana actual
    root.destroy()
    
    # Ejecutar el programa de registro
    subprocess.run(["python", "guiMenu.py"])

try:
    logged = f"consu"
    dato = '{:05d}'.format(len(logged))+logged
    sock.sendall(bytes(dato, 'latin-1'))
    logged_in = sock.recv(64).decode()
    if 'None' in logged_in:
     messagebox.showerror('Error', 'No hay usuario autenticado')
    elif 'False' in logged_in:
     messagebox.showerror('Error', 'Error al acceder a la base de datos')
    else:
     # Crear la ventana principal
     root = tk.Tk()
     root.title("Formulario de Noticias")
     
     back = tk.Button(root, text="Volver", command=back)
     back.pack()
     # Crear etiquetas y entradas para cada campo
     label_nombre_noticia = tk.Label(root, text="Nombre de la noticia:")
     label_nombre_noticia.pack()
     entry_nombre_noticia = tk.Entry(root)
     entry_nombre_noticia.pack()

     label_red_social = tk.Label(root, text="Red social obtenida:")
     label_red_social.pack()
     entry_red_social = tk.Entry(root)
     entry_red_social.pack()

     label_link_noticia = tk.Label(root, text="Link de la noticia:")
     label_link_noticia.pack()
     entry_link_noticia = tk.Entry(root)
     entry_link_noticia.pack()

     label_tags = tk.Label(root, text="Tags (separados por coma):")
     label_tags.pack()
     entry_tags = tk.Entry(root)
     entry_tags.pack()

     # Botón para enviar la noticia
     enviar_button = tk.Button(root, text="Enviar Noticia", command=enviar_noticia)
     enviar_button.pack()

     # Ejecutar el bucle principal de la aplicación
     root.mainloop()

except Exception as e:
    print(f"Error: {e}")
