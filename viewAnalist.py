import tkinter as tk
import json
import socket
import subprocess
import matplotlib.pyplot as plt
from tkinter import ttk
from tkinter import messagebox
from database import databaseServer

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sv_addr = ('localhost', 5000)
print(f'connecting to {sv_addr[0]} to port {sv_addr[1]}')
sock.connect(sv_addr)

class DataViewWindow:
    def __init__(self, db_server):
        self.db_server = db_server
        self.root = tk.Tk()
        self.root.title("Vista de Datos de Noticias")

        self.back = tk.Button(self.root, text="Volver", command=self.back)
        self.back.pack()

        self.tree = ttk.Treeview(self.root, columns=("ID Noticia", "Positivos", "Neutros", "Negativos"), show="headings")
        self.tree.heading("ID Noticia", text="ID Noticia")
        self.tree.heading("Positivos", text="Positivos")
        self.tree.heading("Neutros", text="Neutros")
        self.tree.heading("Negativos", text="Negativos")
        self.tree.pack()

        self.load_data_button = tk.Button(self.root, text="Cargar Datos", command=self.load_data)
        self.load_data_button.pack()

        self.percentages_button = tk.Button(self.root, text="Porcentajes Totales por Ubicación", command=self.show_percentages)
        self.percentages_button.pack()

        self.root.mainloop()

    def back(self):
        # Cerrar la ventana actual
        self.root.destroy()
        
        # Ejecutar el programa de registro
        subprocess.run(["python", "guiMenu.py"])

    def load_data(self):
        try:
            message = f'vernt'
            data = '{:05d}'.format(len(message)) + message
            sock.sendall(bytes(data, 'latin-1'))

            response = sock.recv(1024)
            json_data = json.loads(response[12:].decode('latin-1').replace("'", '"'))

            for item in self.tree.get_children():
                self.tree.delete(item)

            for item in json_data:
                self.tree.insert("", "end", values=(
                    item['id'],
                    str(item['positivo']),
                    str(item['neutro']),
                    str(item['negativo'])
                ))
        except json.JSONDecodeError as e:
            messagebox.showerror("Error", f"Error al decodificar JSON: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar datos: {e}")

    def show_percentages(self):
        try:
            message = f'stats'
            data = '{:05d}'.format(len(message)) + message
            sock.sendall(bytes(data, 'latin-1'))

            response = sock.recv(1024)
            porcentajes = json.loads(response[12:].decode('latin-1').replace("'", '"'))

            localizaciones = [resultado['localizacion'] for resultado in porcentajes]
            porcentaje_positivo = [resultado['positivo'] for resultado in porcentajes]
            porcentaje_negativo = [resultado['negativo'] for resultado in porcentajes]
            porcentaje_neutro = [resultado['neutro'] for resultado in porcentajes]

            # Crear el gráfico de barras
            bar_width = 0.3
            r1 = range(len(localizaciones))
            r2 = [x + bar_width for x in r1]
            r3 = [x + bar_width for x in r2]

            plt.bar(r1, porcentaje_positivo, color='green', width=bar_width, edgecolor='grey', label='Positivo')
            plt.bar(r2, porcentaje_negativo, color='red', width=bar_width, edgecolor='grey', label='Negativo')
            plt.bar(r3, porcentaje_neutro, color='grey', width=bar_width, edgecolor='grey', label='Neutro')

            # Agregar etiquetas
            plt.xlabel('Localización', fontweight='bold')
            plt.xticks([r + bar_width for r in range(len(localizaciones))], localizaciones)

            # Agregar leyenda
            plt.legend()

            # Mostrar el gráfico
            plt.show()
        except Exception as e:
             messagebox.showerror("Error", f"Error al mostrar graficos: {e}")

if __name__ == "__main__":
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
      db_server = databaseServer("localhost", "5432", "ArquiSoft", "postgres", "")
      db_server.create_connection()
      data_view_window = DataViewWindow(db_server)
    except Exception as e:
     print(f"Error: {e}")
