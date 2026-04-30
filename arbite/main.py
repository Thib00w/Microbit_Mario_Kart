from microbit import *
import radio

#initialisation de l'emmeteur radio
radio.config(group = 0 , power = 7)
radio.on 

MON_ID = "ARB"
lst_kart = ["KT1", "KT2", "KT3", "KT4"]
lst_gamepad = ["GP1", "GP2", "GP3", "GP4"]


def envoi_message(destinataire, type, valeur):
    lst = [type, MON_ID, destinataire, valeur]
    msg = str(lst)
    radio.send(msg)



def envoie_tout_le_monde(type, valeur):
    for e in lst_kart:
        lst = [type, MON_ID, e, valeur]
        msg = str(lst)
        radio.send(msg)
    for e in lst_gamepad:
        lst = [type, MON_ID, e, valeur]
        msg = str(lst)
        radio.send(msg)


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


while True:
    message = radio.receive()
    if message:
        décode(message)
    message = None