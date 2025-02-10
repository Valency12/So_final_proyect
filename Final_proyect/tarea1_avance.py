import psutil
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

#Funcion para mostrar el menu
def mostrar_menu(): 
    while True:
        print("\n Gestion de  Procesos")
        print("1. Iniciar un proceso")
        print("2. Matar un proceso")
        print("3. Monitorear un proceso")
        print("4. Salir")

        opcion = input("Seleccione una opcion: ")

        if opcion == "4":
            print("Saliendo...")
        #aqui faltaria meter el proceso de cada opcion
        elif opcion in ["1", "2", "3"]:
            print(f"Opcion {opcion} seleccionada")
        else: 
            print("Opcion no valida, intente de nuevo")

#Punto de entrada principal del programa
if __name__ == "__main__":
    listar_procesos()
    mostrar_menu()
