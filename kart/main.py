from microbit import *
import radio as rd

# Identifiant pour microbit
MON_TYPE = "KT"
MON_ID = "KT2"
MON_GAMEPAD = "GP2"
ARBITRE = "ARB"

# addresse des moteur de macqueen 
ADDR = 0x10

# Config radio
rd.on()
rd.config(group=22)

def rd_decode(message: str):
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

def spd_mtr_turn(x: int, boost: bool = False):
    if x > 512:
        percent = int((x - 512) * 100 / 512)
    elif x < 512:
        percent = int((512 - x) * 100 / 512)
    else:
        return 255 if boost else 100
    return 255 - percent if boost else 100 - percent

while True:
    rd_msg = rd.receive()
    if rd_msg is not None:
        try:
            # convertion du message en valeur
            msg = rd_decode(rd_msg)
            if msg[1] == MON_GAMEPAD or msg[1] == ARBITRE:
                boost = False
                values = msg[3].strip('[]').split(',')
                x = int(values[0].strip())
                b = values[2].strip() == "True"
                a = values[1].strip() == "True"
                # Confirmation de la connection 
                display.show("A" if a else ".")  
                # vitesse normal
                spd = 100
                # vitesse boost
                if boost:
                    spd = 255
                # Ni A ou B est pressé (arret)
                if not b and not a:
                    i2c.write(ADDR, bytes([0x00, 0, 0]))
                    i2c.write(ADDR, bytes([0x02, 0, 0]))
                    
                # Config moteur en fonction de joystick en marche arrière            
                # Si A pressé (reculer)
                if a:
                    if x < 512:
                        i2c.write(ADDR, bytes([0x00, 2, spd_mtr_turn(x, boost)]))
                        i2c.write(ADDR, bytes([0x02, 2, spd]))
                    elif x > 512:
                        i2c.write(ADDR, bytes([0x00, 2, spd]))
                        i2c.write(ADDR, bytes([0x02, 2, spd_mtr_turn(x, boost)]))
                    else:
                        i2c.write(ADDR, bytes([0x00, 2, spd]))
                        i2c.write(ADDR, bytes([0x02, 2, spd]))
                # Config moteur en fonction joystick en marche avant
                # Si b préssé (avancé)
                if b:
                    if x < 512:
                        i2c.write(ADDR, bytes([0x00, 1, spd_mtr_turn(x, boost)]))
                        i2c.write(ADDR, bytes([0x02, 1, spd]))
                    elif x > 512:
                        i2c.write(ADDR, bytes([0x00, 1, spd]))
                        i2c.write(ADDR, bytes([0x02, 1, spd_mtr_turn(x, boost)]))
                    else:
                        i2c.write(ADDR, bytes([0x00, 1, spd]))
                        i2c.write(ADDR, bytes([0x02, 1, spd]))
            sleep(50)
             
        except Exception as e:
            display.scroll(str(e))  # affiche l'erreur sur la matrice