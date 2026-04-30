from microbit import *
import radio as rd
import music as mu

# COnfig radio
rd.on()
rd.config(group=22)

while True:
    # récupère les donnée joysticks
    message = rd.receive()
    if message:
        valeurs = message.slpit(";")
        x = valeurs[0]
        y = valeurs[1]
        # Contrôle moteur
        

    sleep(50)