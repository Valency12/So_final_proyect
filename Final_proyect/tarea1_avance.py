import psutil
import subprocess
from prettytable import PrettyTable
import time

#Funcion para listar los procesos en ejecucion
def listar_procesos():
    #Imprimir encabezado de la tabla
    print(f"{'PID':<10}{'Nombre':<30}{'Uso de CPU (%)':<15}{'Uso de Memoria (%)':<15}")
    print("-" * 70)
    #:<15, :<30, :>10.2f son especificadores de formato en python
    #Iterar sobre los procesos en ejecucion y obtener sus atributos
    for proceso in psutil.process_iter(attrs=['pid', 'name', 'cpu_percent', 'memory_percent']):
        info = proceso.info #Obtener informacion del proceso
        print(f"{info['pid']:<10}{info['name']:<30}{info['cpu_percent']:<15.2f}{info['memory_percent']:<15.2f}")

#Funcion para iniciar un proceso
def iniciar_proceso():
    nombre_proceso = input("Ingrese el nombre del proceso a inciar: ")
    try: 
        subprocess.Popen(nombre_proceso, shell=True)
        print(f"Proceso {nombre_proceso} iniciado correctamente")
        print("Actualizando lista de procesos...")
        listar_procesos()
    except Exception as e:
        print(f"Error al iniciar el proceso: {e}")

def matar_proceso():
    try:
        pid = int(input("Ingrese el PID del proceso a matar: "))
        proceso = psutil.Process(pid)
        print(f"Proceso con PID {pid} terminado correctamente.")
        listar_procesos()
    except psutil.NoSuchProcess:
        print(f"No se encontró ningún proceso con PID {pid}.")
    except ValueError:
        print("PID inválido. Debe ser un número entero.")
    except Exception as e:
        print(f"Error al matar el proceso: {e}")

def monitorear_proceso():
    try:
        pid = int(input("Ingrese el PID del proceso a monitorear: "))
        if not psutil.pid_exists(pid):  # Check if PID exists before creating the process object
            raise psutil.NoSuchProcess(pid)
        proceso = psutil.Process(pid)

        while True:
            print(f"Proceso con PID: {pid}")

            # Memory Information (using psutil.virtual_memory)
            vm = psutil.virtual_memory()
            mem_info = proceso.memory_info()
            memory_table = PrettyTable(["Total(GB)", "Usado(GB)", "Disponible(GB)", "Porcentaje"])
            memory_table.add_row([
                f'{vm.total / 1e9:.3f}',
                f'{mem_info.rss / 1e9:.3f}',
                f'{(vm.available + mem_info.rss - mem_info.vms) / 1e9:.3f}',
                vm.percent
            ])
            print(memory_table)

            print("----Procesos----")
            process_table = PrettyTable(['PID', 'PNOMBRE', 'ESTATUS', 'CPU', 'NUM HILOS', 'MEMORIA(MB)'])

            try:  
                p = psutil.Process(pid)  
                cpu_percent = p.cpu_percent(interval=0.1)
                process_table.add_row([
                    p.pid,
                    p.name(),
                    p.status(),
                    cpu_percent,
                    p.num_threads(),
                    f'{p.memory_info().rss / 1e6:.2f}'
                ])
            except psutil.NoSuchProcess:
                print("Proceso terminado")
                break 
            except psutil.AccessDenied:
                print("Acceso denegado")
                break 
            except Exception as e:
                print(f"Error obteniendo información del proceso: {e}")

            print(process_table)

            continuar = input("¿Desea continuar monitoreando? (s/n): ")
            if continuar.lower() != 's':
                break

    except psutil.NoSuchProcess:
        print(f"No se encontró ningún proceso con PID {pid}.")
    except ValueError:
        print("PID inválido. Debe ser un número entero.")
    except Exception as e:
        print(f"Error inesperado: {e}")

        

#Funcion para mostrar el menu
def mostrar_menu(): 
    salir = False
    while not salir:
        print("\n Gestión de Procesos")
        print("1. Iniciar un proceso")
        print("2. Matar un proceso")
        print("3. Monitorear un proceso")
        print("4. Salir")

        opcion = input("Seleccione una opcion: ")

        if opcion == "4":
            print("Saliendo...")
            salir = True
        
        elif opcion == "1":
            iniciar_proceso()

        elif opcion == "2": 
            print("Procedimiento para detener un proceso")
            matar_proceso()

        elif opcion == "3":
            print("Procedimiento para monitorear un proceso")
            monitorear_proceso()

        else: 
            print("Opcion no valida, intente de nuevo")

#Punto de entrada principal del programa
if __name__ == "__main__":
    listar_procesos()
    mostrar_menu()