import socket
import psutil
import subprocess
from prettytable import PrettyTable
import time

def monitor_proceso(pid):
    """
    Monitorea un proceso dado su PID.
    Retorna información sobre el proceso, incluyendo nombre, estado, uso de CPU y memoria.
    
    :param pid: Identificador del proceso a monitorear
    :return: Cadena con la información del proceso o mensaje de error si no se encuentra
    """
    try:
        p = psutil.Process(pid)
        info = f"Monitoring process {pid}:\n"
        info += f"Name: {p.name()}\n"
        info += f"Status: {p.status()}\n"
        info += f"CPU Usage: {p.cpu_percent(interval=1.0)}%\n"
        info += f"Memory Usage: {p.memory_percent()}%\n"
        return info
    except psutil.NoSuchProcess:
        return f"No se encontró ningún proceso con PID {pid}."
    except psutil.AccessDenied:
        return f"Acceso denegado al intentar monitorear el proceso con PID {pid}."
    except Exception as e:
        return f"Error al monitorear el proceso con PID {pid}: {e}"

def listar_procesos():
    """
    Lista los procesos activos en el sistema.
    Devuelve una tabla con los PID, nombres, uso de CPU y memoria de cada proceso.
    
    :return: Cadena con la tabla de procesos en formato de texto
    """
    tabla = PrettyTable()
    tabla.field_names = ["PID", "Nombre", "Uso de CPU (%)", "Uso de Memoria (%)"]
    
    for proceso in psutil.process_iter(attrs=['pid', 'name', 'cpu_percent', 'memory_percent']):
        info = proceso.info
        tabla.add_row([info['pid'], info['name'], info['cpu_percent'], info['memory_percent']])
    
    return tabla.get_string()

def iniciar_proceso(nombre_proceso):
    """
    Inicia un nuevo proceso dado su nombre.
    
    :param nombre_proceso: Nombre del proceso a iniciar
    :return: Mensaje indicando si el proceso se inició correctamente o si hubo un error
    """
    try:
        subprocess.Popen(nombre_proceso, shell=True)
        return f"Proceso {nombre_proceso} iniciado correctamente"
    except Exception as e:
        return f"Error al iniciar el proceso: {e}"

def matar_proceso(pid):
    """
    Termina un proceso dado su PID.
    
    :param pid: Identificador del proceso a terminar
    :return: Mensaje indicando si el proceso se cerró correctamente o si hubo un error
    """
    try:
        p = psutil.Process(pid)
        p.terminate()
        return f"Proceso con PID {pid} terminado correctamente."
    except psutil.NoSuchProcess:
        return f"No se encontró ningún proceso con PID {pid}."
    except psutil.AccessDenied:
        return f"Acceso denegado al intentar matar el proceso con PID {pid}."
    except Exception as e:
        return f"Error al matar el proceso con PID {pid}: {e}"

def monitorear_proceso(pid):
    try:
        p = psutil.Process(pid)
        info = p.as_dict(attrs=['pid', 'name', 'cpu_percent', 'memory_percent'])
        return f"PID: {info['pid']}, Nombre: {info['name']}, Uso de CPU: {info['cpu_percent']}%, Uso de Memoria: {info['memory_percent']}%"
    except psutil.NoSuchProcess:
        return f"No se encontró ningún proceso con PID {pid}."
    except Exception as e:
        return f"Error al monitorear el proceso con PID {pid}: {e}"


def manejo_cliente(conex, addr):
    """
    Maneja la conexión con un cliente, procesando sus solicitudes.
    
    :param conex: Objeto de conexión del socket
    :param addr: Dirección del cliente conectado
    """
    with conex:
        print('Conectado por', addr)
        try:
            while True:
                data = conex.recv(1024)
                if not data:
                    break
                comando = data.decode('utf-8').split()
                if comando[0] == "listar":
                    respuesta = listar_procesos()
                elif comando[0] == "iniciar":
                    respuesta = iniciar_proceso(comando[1])
                elif comando[0] == "matar":
                    respuesta = matar_proceso(int(comando[1]))
                elif comando[0] == "monitorear":
                    respuesta = monitor_proceso(int(comando[1]))
                elif comando[0] == "monitorear":
                    respuesta = monitorear_proceso(int(comando[1]))
                else:
                    respuesta = "Comando no reconocido"
                conex.sendall(respuesta.encode('utf-8'))
        except Exception as e:
            print(f"Error en manejo de cliente {addr}: {e}")

def get_private_ipv4():
    """
    Obtiene la dirección IPv4 privada del servidor.
    
    :return: Dirección IP privada o mensaje de error si no se puede determinar
    """
    try:
        nombre_host = socket.gethostname()
        dir_IP = socket.gethostbyname(nombre_host)
        return dir_IP
    except socket.gaierror:
        return "Could not determine private IP address"

ip_privada = get_private_ipv4()
print(f"Server IP: {ip_privada}")
HOST = ip_privada
PORT = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"Server listening on {HOST}:{PORT}")
    while True:
        try:
            conex, addr = s.accept()
            manejo_cliente(conex, addr)
        except Exception as e:
            print(f"Error accepting connections: {e}")

if __name__ == "__main__":
    listar_procesos()
    mostrar_menu()