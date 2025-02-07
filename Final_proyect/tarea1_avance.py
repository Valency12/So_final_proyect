import psutil
import subprocess
import time

def iniciar_calculadora():
  """Inicia la calculadora y devuelve el objeto del proceso."""
  try:
    ruta_calculadora = "C:\\Windows\\System32\\calc.exe"
    proceso = subprocess.Popen([ruta_calculadora])
    print("Calculadora iniciada con éxito.")
    return proceso
  except FileNotFoundError:
    print(f"Error: No se encontró el ejecutable de la calculadora.")
    return None
  except Exception as e:
    print(f"Error al iniciar la calculadora: {e}")
    return None

def interactuar_con_proceso(proceso):
  """Interactúa con el proceso usando psutil."""
  try:
    while True:
      try:
        proceso_psutil = psutil.Process(proceso.pid)
        break 
      except psutil.NoSuchProcess:
        time.sleep(0.1)

    print(f"Nombre del proceso (psutil): {proceso_psutil.name()}")
    print(f"Estado del proceso (psutil): {proceso_psutil.status()}")
    print(f"Uso de CPU del proceso (psutil): {proceso_psutil.cpu_percent(interval=1)}")
    print(f"Uso de memoria del proceso (psutil): {proceso_psutil.memory_percent()}")

  except psutil.NoSuchProcess:
    print("Error: El proceso ya no existe o terminó demasiado rápido.")
  except Exception as e:
    print(f"Error al interactuar con el proceso: {e}")

if __name__ == "__main__":
  proceso_calculadora = iniciar_calculadora()

  if proceso_calculadora:
    interactuar_con_proceso(proceso_calculadora)

#Comunicacion de red y protocolo TCP/IP

#aplicacion cliente que pueda enviar comandos al servidor para gestionar los procesos
#Utiliza sockets para la comunicacion entre el cliente y el servidor. 
import socket
import subprocess
import sys

HOST = '127.0.0.1'  # Dirección IP del servidor
PORT = 5000        # Puerto del servidor

def manejar_comando(comando):
    try:
        # Ejecutar el comando y obtener la salida
        resultado = subprocess.check_output(comando, shell=True, stderr=subprocess.STDOUT)
        return resultado.decode('utf-8')
    except subprocess.CalledProcessError as e:
        return f"Error: {e.output.decode('utf-8')}"
    except FileNotFoundError:
        return "Error: Comando no encontrado"

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Servidor escuchando en {HOST}:{PORT}")

        while True:
            try:  # Bloque try para manejar excepciones de conexión
                conn, addr = s.accept()
                with conn:
                    print(f"Conexión establecida desde {addr}")
                    while True:
                        data = conn.recv(1024)
                        if not data:
                            break

                        comando = data.decode('utf-8')

                        if comando.lower() == "salir" or comando.lower() == "exit":
                            print("Cliente solicitó cerrar el servidor. Cerrando...")
                            conn.sendall("Servidor cerrado.".encode('utf-8'))
                            break  # Sale del bucle interno while

                        resultado = manejar_comando(comando)
                        conn.sendall(resultado.encode('utf-8'))
            except ConnectionResetError: # Captura el error si el cliente cierra la conexión inesperadamente
                print("Cliente cerró la conexión inesperadamente.")
                break # Sale del bucle interno while
            except Exception as e: # Captura cualquier otro error de conexión
                print(f"Error de conexión: {e}")
                break # Sale del bucle interno while
            if comando.lower() == "salir" or comando.lower() == "exit":
                break  # Sale del bucle externo while
except OSError as e:  # Captura el error de puerto en uso
    if e.errno == 10048:  # Código de error de Windows para "puerto en uso"
        print(f"Error: El puerto {PORT} ya está en uso. Cierre la instancia anterior del servidor o use otro puerto.")
    else:
        print(f"Error al iniciar el servidor: {e}")
finally:
    print("Servidor finalizado.")
    sys.exit(0)
