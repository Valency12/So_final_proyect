import psutil
import subprocess
import time

#Mostrar todos los procesos
def mostrar_procesos():
    for proceso in psutil.process_iter(['name', 'pid', 'cmdline']):
        

