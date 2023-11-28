import tkinter as tk
import subprocess
import socket
from tkinter import messagebox

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sv_addr = ('localhost', 5000)
print(f'connecting to {sv_addr[0]} to port {sv_addr[1]}')
sock.connect(sv_addr)

def on_insertar_noticia_click():
    root.destroy()
    
    subprocess.run(["python", "insertNews.py"])

def on_ver_noticias_click():
    root.destroy()
    
    subprocess.run(["python", "viewNews.py"])

def on_ver_analisis_click():
    root.destroy()
    
    subprocess.run(["python", "viewAnalist.py"])

def logout():
    message = f'logou'
    data= '{:05d}'.format(len(message))+message
    sock.sendall(bytes(data, 'latin-1'))
    success = sock.recv(17).decode()
    if not 'False' in success:
        messagebox.showinfo("Cierre de sesión exitoso", "¡Hasta Luego!")
        root.destroy()
        subprocess.run(["python", "guiAuth.py"])

def consultar_login():
    try:
        message= f'consu'
        data= '{:05d}'.format(len(message))+message
        sock.sendall(bytes(data, 'latin-1'))

        response = sock.recv(1024)

        response = response[12:].decode('latin-1').replace("'", '"').replace("(","").replace(")","")
        return response

    except Exception as e:
          messagebox.showerror("Error", f"Error al cargar usuario: {e}")
          

consultar_login()
# Crear la ventana principal
root = tk.Tk()
root.title("Menú de Noticias")

# Crear botones
insertar_noticia_button = tk.Button(root, text="Insertar Noticia", command=on_insertar_noticia_click)
ver_noticias_button = tk.Button(root, text="Ver Noticias", command=on_ver_noticias_click)
ver_analisis_button = tk.Button(root, text="Ver Análisis", command=on_ver_analisis_click)
logout = tk.Button(root, text="Cerrar Sesión", command=logout)

# Organizar los botones en la ventana
insertar_noticia_button.pack(pady=10)
ver_noticias_button.pack(pady=10)
ver_analisis_button.pack(pady=10)
logout.pack(pady=10)

# Iniciar el bucle principal de Tkinter
root.mainloop()

