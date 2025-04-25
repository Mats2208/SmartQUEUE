import subprocess
import tkinter as tk
from tkinter import messagebox
import os
import qrcode
from PIL import Image, ImageTk
import threading
import requests
import time

# CONFIGURACIÓN
BACKEND_URL = "https://smartqueue-backend.onrender.com"  # Cambia esto con tu URL de Render

# Ejecutable del motor
ejecutable = "cola.exe" if os.name == "nt" else "./cola"

# Iniciar motor
proc = subprocess.Popen(
    [ejecutable],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
    bufsize=1
)

# Cola en memoria
cola_completa = []
turno_numero_actual = 0
lista_admin = None
etiqueta_total = None

def enviar_comando(comando):
    if proc.poll() is not None:
        error = proc.stderr.read()
        messagebox.showerror("Error del Motor", f"El motor se cerró inesperadamente.\nDetalles:\n{error}")
        raise RuntimeError("Motor apagado.")
    proc.stdin.write(comando + "\n")
    proc.stdin.flush()
    return proc.stdout.readline().strip()

def actualizar_admin():
    if lista_admin is not None:
        lista_admin.delete(0, tk.END)
        for i, nombre in enumerate(cola_completa):
            lista_admin.insert(tk.END, f"#{i+1} - {nombre}")
    if etiqueta_total is not None:
        etiqueta_total.config(text=f"Personas en cola: {len(cola_completa)}")

def interfaz_usuario(root):
    ventana = tk.Toplevel(root)
    ventana.title("Turno - Usuario")
    ventana.configure(bg="#2c3e50")
    frame = tk.Frame(ventana, bg="#2c3e50", padx=20, pady=20)
    frame.pack()
    tk.Label(frame, text="Escanea este QR para unirte a la cola:", bg="#2c3e50", fg="white", font=("Arial", 12)).pack(pady=10)
    qr = qrcode.make(BACKEND_URL + "/registro")
    qr = qr.resize((200, 200))
    qr_img = ImageTk.PhotoImage(qr)
    qr_label = tk.Label(frame, image=qr_img, bg="#2c3e50")
    qr_label.image = qr_img
    qr_label.pack()

def interfaz_admin(root, turno_actual):
    global lista_admin, etiqueta_total
    ventana = tk.Toplevel(root)
    ventana.title("Administración")
    ventana.configure(bg="#ecf0f1")
    frame = tk.Frame(ventana, bg="#ecf0f1", padx=20, pady=20)
    frame.pack()

    lista_admin = tk.Listbox(frame, width=40, height=10, font=("Arial", 12))
    lista_admin.pack(pady=10)

    etiqueta_total = tk.Label(frame, text="Personas en cola: 0", bg="#ecf0f1", font=("Arial", 12))
    etiqueta_total.pack()

    def atender():
        global turno_numero_actual
        if cola_completa:
            turno_numero_actual += 1
            atendido = cola_completa.pop(0)
            turno_actual.set(f"Turno #{turno_numero_actual} - {atendido}")
            enviar_comando("siguiente")
            actualizar_admin()
        else:
            turno_actual.set("Esperando...")

    tk.Button(frame, text="Atender siguiente", command=atender,
              bg="#e67e22", fg="white", font=("Arial", 12)).pack(pady=10)

def interfaz_turno(root, turno_actual):
    ventana = tk.Toplevel(root)
    ventana.title("Turno Actual")
    ventana.configure(bg="#1abc9c")
    label = tk.Label(ventana, textvariable=turno_actual,
                     font=("Arial", 40, "bold"), fg="white", bg="#1abc9c", padx=50, pady=50)
    label.pack(expand=True, fill="both")

# ======================
# POLLING A BACKEND REMOTO
# ======================
def polling_remoto():
    while True:
        try:
            res = requests.get(f"{BACKEND_URL}/api/turnos_pendientes")
            nuevos = res.json()
            for nombre in nuevos:
                cola_completa.append(nombre)
                enviar_comando(f"agregar {nombre}")
                actualizar_admin()
        except Exception as e:
            print("Error al conectar con el backend:", e)
        time.sleep(5)

threading.Thread(target=polling_remoto, daemon=True).start()

# ======================
# INICIO
# ======================
root = tk.Tk()
root.withdraw()
turno_actual = tk.StringVar(value="Esperando...")

interfaz_usuario(root)
interfaz_admin(root, turno_actual)
interfaz_turno(root, turno_actual)

root.mainloop()

# Cierre
try:
    enviar_comando("salir")
except:
    pass
proc.terminate()
