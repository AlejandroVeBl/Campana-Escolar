##############
#   Imports  #
##############

import time                 # Librería control de tiempo
import pygame               # Librería para reproducir audio
import signal               # Librerías para atrapar señales
import sys                  # (se usa para atrapar SIGINT(ctrl-c))
import os                   # Librería cosas SO
import random               # Librería cosas random (Estas dos se usan para coger el fichero random desde el directorio)
from mutagen.mp3 import MP3 # Librería metadatos de audios, sólo mp3 en mi caso
import re                   # Librería expresiones regulares

#################
#   Constantes  #
#################

DIRECTORIO = "/home/usuario/campana/musica/" # Directorio donde se encuenta la música(Con la barra al final)
FADEOUT = 2000                               # Difuminado de la canción en milisegundos

#######################
#   Clases/Funciones  #
#######################

# Función señales
def signal_handler(sig, frame):
    print("\nAdiós :(")
    sys.exit(0)


# Clase Campana para crear objetos campana
class Campana():

    # Función de construcción del objeto
    def __init__(self, tiempo, tiempo_reproduccion):
        super(Campana, self).__init__()
        self.tiempo = list(tiempo)
        self.tiempo_reproduccion = int(tiempo_reproduccion)
        self.fadeout = FADEOUT

    # Función ejecutar campana
    def ejecutar(self):

        # Comprobar si la lista de horas está vacía
        regex_pattern = '^\d+ ?: ?\d+$'
        if (self.tiempo == False or re.match(regex_pattern, str(self.tiempo[:1])) == False or str(self.tiempo[:1]) == "[]"):
            print("La lista de horas está vacía")
            sys.exit(1)

        # Bucle infinito
        while True:

            # Atrapar señales SIGINT
            signal.signal(signal.SIGINT, signal_handler)

            # Comprobar si es hora de la campana, si es así hacerla sonar
            ahora = time.localtime()
            tiempo = str(ahora.tm_hour) + " : " + str(ahora.tm_min)
            if (tiempo in self.tiempo):
                # Coge la canción random
                cancion = random.choice(os.listdir(DIRECTORIO))
                # Si el tiempo de reproducción excede a la duración de la canción hacer que sólo se reproduzca la duración
                cancion_meta = MP3(DIRECTORIO + cancion)
                if (self.tiempo_reproduccion > cancion_meta.info.length):
                    self.tiempo_reproduccion = cancion_meta.info.length + 1
                # Suena la canción
                print("\n\nCampana sonando a las: " + tiempo + "\nCon la canción: " + str(cancion) + "\ny duración de reproducción de: " + str(self.tiempo_reproduccion) + "s\n\n")
                pygame.mixer.init()
                musica = pygame.mixer.Sound(DIRECTORIO + cancion)
                musica.play()
                time.sleep(self.tiempo_reproduccion-(int(self.fadeout/1000)))
                musica.fadeout(self.fadeout)
                # Recordatorio cuándo suenan las campanas
                print("\n\nLas campanas suenan a las: \n")
                print(*self.tiempo, sep = ", ")
                print("\n\n")
                # Dormir un minuto entre campanas si dura menos de un minuto la reproducción, si no se ejecuta varias veces
                # ya que cumple la condición del if de nuevo.
                if (self.tiempo_reproduccion < 60):
                    time.sleep(65 - self.tiempo_reproduccion) # Tiene 5s más de margen por los redondeos


#########################
#   Programa Principal  #
#########################

def main():

    # Iniciar lista de las horas a las que suenan las campanas
    campana_tiempo_lista = []
    # Leer los tiempos a los que sonará la campana y meterlos en una lista
    while True:
        print("Introduzca la hora y minuto de una campana (sólo se tendrá en cuenta una alarma por minuto)")
        campana_h = int(input("\n\nHora a la que quieres que suene la campana(sólo la hora)(número mayor a 23 para salir): \n\n"))
        if (campana_h > 23):
            break
        campana_mins = int(input("\n\nMinuto a la que quieres que suene la campana(sólo el minuto)(número mayor a 59 para salir): \n\n"))
        if (campana_mins > 59):
            break
        
        campana_tiempo = str(campana_h) + " : " + str(campana_mins)
        campana_tiempo_lista.append(campana_tiempo)
    
    # Tiempo de reproducción de las canciones
    tiempo_reproduccion= int(input("\n\nNúmero de segundos que se reproducirán las canciones, \nsi excede a la duración de la canción se reproducirá sólo la canción\npor lo que un tiempo como 999 o 9999 suele ser lo mejor si se quiere reproducir la canción entera\n\n"))
        
    # Resumen de lo elegido
    print("\n\nLas campanas sonarán a las: \n")
    print(*campana_tiempo_lista, sep = "\n")
    print("\nY se reproducen con una duración de: " + str(tiempo_reproduccion) + "s\n\n")

    campana = Campana(campana_tiempo_lista,tiempo_reproduccion)
    campana.ejecutar()


# Ejecutar el programa principal sólo si el programa se ejecuta directamente y no si se importa
if __name__ == "__main__":
    main()