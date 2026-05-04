from microbit import *
import radio as rd

MON_TYPE = "KT"
MON_ID = "KT1"
MON_GAMEPAD = "GP1"
ARBITRE = "ARB"

# Config radio
rd.on()
rd.config(group=22)

def rd_décode(message: str):
    splt_msg = message.split(';')
    if len(splt_msg) == 4:
        type_ = splt_msg[0]
        emetteur = splt_msg[1]
        destinateur = splt_msg[2]
        values = splt_msg[3]
        return type_, emetteur, destinateur, values
    else:
        raise ValueError("Longueur message invalide")

def rd_envoie(dest: str, values: list):
    msg = str(MON_TYPE) + ";" + str(MON_ID) + ";" + str(dest) + ";" + str(values)
    rd.send(msg)

def moteurs(x, b, a):
    if not b:
        i2c.write(0x10, bytes([0x00, 0, 0]))
        i2c.write(0x10, bytes([0x02, 0, 0]))
        return

    vitesse_base = 255 if a else 100  # boost si A appuyé

    if x > 542:
        coeff = (x - 542) / 481
        gauche = vitesse_base
        droit = int(vitesse_base * (1 - coeff))
    elif x < 482:
        coeff = (482 - x) / 482
        gauche = int(vitesse_base * (1 - coeff))
        droit = vitesse_base
    else:
        gauche = vitesse_base
        droit = vitesse_base

    i2c.write(0x10, bytes([0x00, 0, gauche]))
    i2c.write(0x10, bytes([0x02, 0, droit]))

while True:
    rd_msg = rd.receive()
    if rd_msg is not None:
        try:
            msg = rd_décode(rd_msg)
            if msg[1] == MON_GAMEPAD or msg[1] == ARBITRE:
                values = msg[3].strip('[]').split(',')
                x = int(values[0].strip())
                b = values[2].strip() == "True"
                a = values[1].strip() == "True"
                display.show("A" if a else ".")  # debug
                moteurs(x, b, a)
        except:
            pass