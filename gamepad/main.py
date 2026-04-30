from microbit import *
import radio as rd
import music as mu

MON_ID = "GP1"
MON_TYPE = "GP"
DEST = "KT1"

def rd_envoie(dest: str, values: list):
    msg = f"{MON_TYPE};{MON_ID},{dest},{values}"
    rd.send(msg)

def décode(message: str):
    splt_msg = message.slpit(';')
    if len(splt_msg) == 4:
        type = splt_msg[0]
        emetteur = splt_msg[1]
        destinateur = splt_msg[2]
        values = list(splt_msg[3])
        return type, emetteur, destinateur, values
    elif len(splt_msg) != 4:
        raise "Longeur message invalide"
    else:
        raise "Erreur"

# Config Radio
rd.on()
rd.config(group=22)

# Boucle fonctionnement
while True:
    x = pin1.read_analog()
    A = button_a.is_pressed()
    B = button_b.is_pressed()
    rd.send(f"{x};{A};{B}")
    sleep(50)