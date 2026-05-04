from microbit import *
import radio as rd

MON_ID = "GP1"
MON_TYPE = "GP"
DEST = "KT1"
rd.on()
rd.config(group=22)


def rd_envoie(dest: str, values: list):
    msg = str(MON_TYPE) + ";" + str(MON_ID) + ";" + str(dest) + ";" + str(values)
    rd.send(msg)

def décode(message: str):
    splt_msg = message.split(';')
    if len(splt_msg) == 4:
        type = splt_msg[0]
        emetteur = splt_msg[1]
        destinateur = splt_msg[2]
        values = list(splt_msg[3])
        return type, emetteur, destinateur, values
    else:
        raise ValueError("Longueur message invalide")


while True:
    x = pin1.read_analog()
    A = button_a.is_pressed()
    B = button_b.is_pressed()
    C = pin13.read_digital()
    lst = [x, A, B, C]
    rd_envoie(DEST, lst)
    sleep(50)