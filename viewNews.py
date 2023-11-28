import tkinter as tk
import socket
import sys
import webbrowser
import json
import geocoder
import subprocess
from tkinter import messagebox, simpledialog
from tkinter import ttk
from database import databaseServer

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sv_addr = ('localhost', 5000)
print(f'connecting to {sv_addr[0]} to port {sv_addr[1]}')
sock.connect(sv_addr)

db_server = databaseServer("localhost", "5432", "ArquiSoft", "postgres", "")
db_server.create_connection()

class RatingDialog(tk.Toplevel):
    def __init__(self, title):
        super().__init__()

        self.title("Calificación")
        self.result = None

        tk.Label(self, text=f"Calificar '{title}':").pack(pady=10)

        tk.Button(self, text="Positivo", command=self.set_positive).pack(side=tk.LEFT, padx=10)
        tk.Button(self, text="Neutro", command=self.set_neutral).pack(side=tk.LEFT, padx=10)
        tk.Button(self, text="Negativo", command=self.set_negative).pack(side=tk.LEFT, padx=10)

    def set_positive(self):
        self.result = "Positivo"
        self.destroy()

    def set_neutral(self):
        self.result = "Neutro"
        self.destroy()

    def set_negative(self):
        self.result = "Negativo"
        self.destroy()

def consultar_login():
    try:
        message= f'consu'
        data= '{:05d}'.format(len(message))+message
        sock.sendall(bytes(data, 'latin-1'))

        response = sock.recv(1024)

        response[12:].decode('latin-1').replace("'", '"')
        response = response[12:].decode('latin-1').replace("'", '"').replace("(","").replace(")","")
        return response

    except Exception as e:
          messagebox.showerror("Error", f"Error al cargar usuario: {e}")
          
def load_datos():
    try:
        message= f'vernt'
        data= '{:05d}'.format(len(message))+message
        sock.sendall(bytes(data, 'latin-1'))

        response = sock.recv(1024)
        json_data = json.loads(response[12:].decode('latin-1').replace("'", '"'))

        for item in tree.get_children():
         tree.delete(item)
        
        for item in json_data:
         tree.insert("","end", values=(
          item['id'],
          item['titulo'],
          item['rss'],
          str(item['visitas']),
          str(item['tags']['tags']),
          str(item['positivo']),
          str(item['neutro']),
          str(item['negativo']),
          item.get('link', '')
         ))
    except json.JSONDecodeError as e:
          messagebox.showerror("Error", f"Error al decodificar JSON: {e}")
    except Exception as e:
          messagebox.showerror("Error", f"Error al cargar datos: {e}")

def get_location():
    g = geocoder.ip('me')
    if g.city and g.country:
        return f"{g.city}, {g.country}"
    return "Ubicación no encontrada"

def on_tree_click(event):
    item_id = tree.selection()[0]
    url = tree.item(item_id, 'values')[-1]  # Assuming 'link' is the last column
    news_id = tree.item(item_id, 'values')[0]
    if url:
        webbrowser.open_new(url) 
        open_rating_window(news_id)

def search():
    keyword = entry_busqueda.get()
    tree.delete(*tree.get_children())
    try:
        message= f'busca{keyword}'
        data= '{:05d}'.format(len(message))+message
        sock.sendall(bytes(data, 'latin-1'))

        response = sock.recv(1024)
        json_data = json.loads(response[12:].decode('latin-1').replace("'", '"'))

        for item in tree.get_children():
         tree.delete(item)
        
        for item in json_data:
         tree.insert("","end", values=(
          item['id'],
          item['titulo'],
          item['rss'],
          str(item['visitas']),
          str(item['tags']['tags']),
          str(item['positivo']),
          str(item['neutro']),
          str(item['negativo']),
          item.get('link', '')
         ))
    except json.JSONDecodeError as e:
          print(e)
          messagebox.showerror("Error", f"Error al decodificar JSON: {e}")
    except Exception as e:
          messagebox.showerror("Error", f"Error al cargar datos: {e}")
          

def open_rating_window(news_id):
    logged = consultar_login()
    rating_dialog = RatingDialog(news_id)
    rating_dialog.wait_visibility()
    rating_dialog.grab_set()
    rating_dialog.wait_window()
    result = rating_dialog.result
    
    if result:
         try:
             message= f'votar{news_id} {result.lower()} {get_location()} {logged}'
             data= '{:05d}'.format(len(message))+message
             sock.sendall(bytes(data, 'latin-1'))

             response = sock.recv(1024)       
             messagebox.showinfo("Calificación", f"Has calificado '{news_id}' como {result}.")
         except Exception as e:
             messagebox.showerror("Error", f"Error al registrar datos: {e}")

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
     root = tk.Tk()
     root.title("Tabla de Noticias")

     back = tk.Button(root, text="Volver", command=back)
     back.pack()

     # Crear un campo de búsqueda
     label_busqueda = tk.Label(root, text="Buscar por palabra clave:")
     label_busqueda.pack()
     entry_busqueda = tk.Entry(root)
     entry_busqueda.pack()
     buscar_button = tk.Button(root, text="Buscar", command=search)
     buscar_button.pack()

     # Crear la tabla
     tree = ttk.Treeview(root, columns=("ID", "Titulo", "Red Social", "Visitas", "Tags" ,"Positivos", "Neutros", "Negativos" ,"Acceso"), show="headings")
     tree.heading("ID", text="ID")
     tree.heading("Titulo", text="Titulo")
     tree.heading("Red Social", text="Red Social")
     tree.heading("Visitas", text="Visitas")
     tree.heading("Tags", text="Tags")
     tree.heading("Positivos", text="Positivos")
     tree.heading("Neutros", text="Neutros")
     tree.heading("Negativos", text="Negativos")
     tree.heading("Acceso", text="Acceso")
     tree.pack()

     # Cargar datos en la tabla al iniciar la aplicación
     load_datos()

     # Configurar la etiqueta de print(success)botón (simulando un botón)
     tree.tag_configure('button')

     # Asociar la función on_tree_click al evento de clic en la etiqueta de botón
     tree.tag_bind('button', '<ButtonRelease-1>', lambda event: on_tree_click(event))

     # Marcar la última columna como etiqueta de botón
     for item_id in tree.get_children():
         tree.item(item_id, tags=('button',))

     # Ejecutar el bucle principal de la aplicación
     root.mainloop()

except Exception as e:
    print(f"Error: {e}")
