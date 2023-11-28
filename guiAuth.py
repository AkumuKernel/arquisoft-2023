import tkinter as tk
import subprocess

def on_login_button_click():
    root.destroy()
    
    subprocess.run(["python", "loginUser.py"])

def on_register_button_click():
    # Cerrar la ventana actual
    root.destroy()
    
    # Ejecutar el programa de registro
    subprocess.run(["python", "createUser.py"])

# Crear la ventana principal
root = tk.Tk()
root.title("Login/Register")

# Crear botones
login_button = tk.Button(root, text="Login", command=on_login_button_click)
register_button = tk.Button(root, text="Registro", command=on_register_button_click)

# Organizar los botones en la ventana
login_button.pack(pady=10)
register_button.pack(pady=10)

# Iniciar el bucle principal de Tkinter
root.mainloop()
