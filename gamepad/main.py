from microbit import *
import radio as rd
import music as mu

# Config Radio
rd.on()
rd.config(group=22)

# Boucle fonctionnement
while True:
    x = pin1.read_analog()
    y = pin2.read_analog()
    rd.send(f"{x};{y}")
    sleep(50)