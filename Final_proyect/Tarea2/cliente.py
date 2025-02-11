import socket

def send_command(command):
    """
  Envía un comando al servidor a través de un socket.

  Args:
  command (str): El comando a enviar.
  """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(command.encode('utf-8'))
        data = s.recv(4096)
        print(data.decode('utf-8'))

def mostrar_menu():
    """
    Muestra el menú de opciones y maneja la interacción del usuario.
    """
    salir = False
    while not salir:
        print("\n Gestión de Procesos")
        print("1. Listar procesos")
        print("2. Iniciar un proceso")
        print("3. Matar un proceso")
        print("4. Monitorear un proceso")
        print("5. Salir")

        opcion = input("Seleccione una opcion: ")

        if opcion == "5":
            print("Saliendo...")
            salir = True
        elif opcion == "1":
            send_command("listar") # Llama a la función para enviar el comando "listar"
        elif opcion == "2":
            nombre_proceso = input("Ingrese el nombre del proceso a iniciar: ") 
            send_command(f"iniciar {nombre_proceso}") # Envía el comando "iniciar" con el nombre del proceso
        elif opcion == "3":
            pid = input("Ingrese el PID del proceso a matar: ")
            send_command(f"matar {pid}") # Envía el comando "matar" con el PID del proceso
        elif opcion == "4":
            pid = input("Ingrese el PID del proceso a monitorear: ") 
            send_command(f"monitorear {pid}") # Envía el comando "monitorear" con el PID del proceso
        else:
            print("Opcion no valida, intente de nuevo")

if __name__ == "__main__":
    HOST = "192.168.56.1"  # Asegurarse que este numero sea el mismo que el de server.py
    PORT = 65432
    mostrar_menu()  # Llama a la función para mostrar el menú