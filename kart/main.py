from microbit import *
import radio as rd
import music as mu

MON_TYPE = "KT"
MON_ID = "KT1"
MON_GAMEPAD = "GP1"
ARBITRE = "ARB"

# Config radio
rd.on()
rd.config(group=22)

def rd_décode(message: str):
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

def rd_envoie(dest: str, values: list):
    msg = f"{MON_TYPE};{MON_ID},{dest},{values}"
    rd.send(msg)
    
def right(x):
    if x >= 512:
        x - 512
        percent = x*100/512
        return 200 * percent/100
    return None

def left(x):
    if x<= 512:
        percent = x*100/512
        return 200*percent/100
    return None 

while True:
    # récupère les donnée joysticks
    rd_msg = None
    rd_msg = rd.receive()
    msg = rd_décode(rd_msg)
    if msg is not None and (msg[1] == MON_GAMEPAD or \
                            msg[1] == ARBITRE):
        values = msg[3]