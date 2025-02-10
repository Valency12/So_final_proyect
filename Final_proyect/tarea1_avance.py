import psutil
import subprocess
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

#Funcion para mostrar el menu
def mostrar_menu(): 
    salir = False
    while not salir:
        print("\n Gestion de  Procesos")
        print("1. Iniciar un proceso")
        print("2. Matar un proceso")
        print("3. Monitorear un proceso")
        print("4. Salir")

        opcion = input("Seleccione una opcion: ")

        if opcion == "4":
            print("Saliendo...")
            salir = True
        #aqui faltaria meter el proceso de cada opcion
        elif opcion == "1":
            iniciar_proceso()
        elif opcion == "2": 
            print("Procedimiento para detener un proceso")
        elif opcion == "3":
            print("Procedimiento para monitorear un proceso")
        else: 
            print("Opcion no valida, intente de nuevo")

#Punto de entrada principal del programa
if __name__ == "__main__":
    listar_procesos()
    mostrar_menu()


