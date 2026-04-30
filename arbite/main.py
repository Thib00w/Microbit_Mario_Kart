from microbit import *
import radio

#initialisation de l'emmeteur radio
radio.config(group = 0 , power = 7)
radio.on 

Mon_id = "ARB"

def envoi_message(destinataire, type, valeur):
    lst = [type, Mon_id, destinataire, valeur]
    msg = str(lst)
    radio.send(msg)

