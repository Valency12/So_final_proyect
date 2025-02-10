#Objetivo: crear un programa que permita una comunicacion de red entre el servidor y los clientes a traves de sockets TCP/IP 
import socket
import subprocess
import threading

#Configuracion del servidor
HOST = '127.0.0.1' #Direccion IP del servidor
PORT = 65432 #Puerto de escucha del servidor

#Funcion para manejar la conexion con un cliente
def manejar_cliente(conn, addr): 
    print(f"[NUEVA CONEXION] Cliente conectado desde {addr}")
    while True: 
        
        try: 
        #Recibimos datos del cliente
            data = conn.recv(1024).decode('utf-8')
            if not data: 
                break
            print(f"[COMANDO RECIBIDO] {data}")

            if data == 'listar':
                output = subprocess.check_output(['tasklist'], shell=True, text=True)
            elif data.startswith('iniciar'):
                proceso = data.split(' ', 1)[1]
                subprocess.Popen(proceso, shell=True)
                output = f"Proceso '{proceso}' iniciado correctamente"
            elif data.startswith('matar'):
                pid = data.split(' ', 1)[1]
                subprocess.call(['taskkill', '/F', '/PID', pid], shell=True)
                output = f"Proceso con PID {pid} detenido"
            else: 
                output = "Comando no valido"

            conn.sendall(output.encode('utf-8'))
        except Exception as e:
            conn.sendall(f"Error: {str(e)}".encode('utf-8'))
    
    conn.close()
    print(f"[DESCONEXION] Cliente {addr} desconectado")

    #Iniciar servidor
if __name__ == "__main__":
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"[ESCUCHANDO] Servidor en {HOST}:{PORT}")

while True:
    conn, addr = server.accept()
    thread = threading.Thread(target=manejar_cliente, args=(conn, addr))
    thread.start()
    
