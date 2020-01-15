import os
from bottle import template, static_file, route, run

print("LightKeyPI starting...")

# état du serveur on/off
active = True
# commande en cours
command = "none"
# valeur du potard page 2 (0-100%)
fadV = "0"
# mode de sortie
outmode = 0 # 0 : light only / 1 : merge / 2 : artnet
# config réseau
_ip = "2.0.0.1"
_mask = "255.0.0.0"
_univ = "0.0.1"

# fonction qui renvoie la page web
@route('/')
def index():
    return template('index')
   
# fonction pour renvoyer les fichiers statiques
@route('/<filename>')
def serve(filename):
    return static_file(filename, root='./'); 
    
# retourne l'état en cours du serveur vers la page web
@route('/state')
def state():
    if active :
        return { 'state': 'true', 'command': command, '_ip': _ip, '_mask': _mask, '_univ': _univ, 'outmode': outmode}
    else:
        return { 'state': 'false', 'command': command, '_ip': _ip, '_mask': _mask, '_univ': _univ, 'outmode': outmode}

# c'est là que le potard entre
@route('/fader/<v>')
def fader(v):
    global fadV
    fadV = v
    print('> fader :',fadV)
    command = 'ALL @ '+fadV
    return { 'state': active, 'command': command}#, '_ip': ip, '_mask': _mask, '_univ': _univ, 'outmode': outmode}
  
#set IP
@route('/ip/<v>')
def ip(v):
    global _ip
    _ip = v
    print('> ip :', _ip)
    return { 'state': active, 'command': command, '_ip': _ip, '_mask': _mask, '_univ': _univ, 'outmode': outmode}
   
#set Mask 
@route('/mask/<v>')
def mask(v):
    global _mask
    _mask = v
    print('> mask :', _mask)
    return { 'state': active, 'command': command, '_ip': _ip, '_mask': _mask, '_univ': _univ, 'outmode': outmode}
    
#set Universe
@route('/univ/<v>')
def univ(v):
    global _univ
    _univ = v
    print('> univ :', _univ)
    return { 'state': active, 'command': command, '_ip': _ip, '_mask': _mask, '_univ': _univ, 'outmode': outmode}
    
# tous les autres boutons
@route('/button/<but>')
def button(but):
    print('> button :',but)
    global command
    global active
    global outmode
    if but == "active" :
        if active:
            active = False
        else:
            active = True
    elif but == "command" :
        command = "none"
    else:
        if command == "none":
            command = ""
        if but == "1" :
            command += "1"
        elif but == "2" :
            command += "2"
        elif but == "3" :
            command += "3"
        elif but == "4" :
            command += "4"
        elif but == "5" :
            command += "5"
        elif but == "6" :
            command += "6"
        elif but == "7" :
            command += "7"
        elif but == "8" :
            command += "8"
        elif but == "9" :
            command += "9"
        elif but == "0" :
            command += "0"
        elif but == "plus" :
            command += " + "
        elif but == "minus" :
            command += " - "
        elif but == "thru" :
            command += " THRU "
        elif but == "at" :
            command += " @ "
        elif but == "full" :
            command += " FULL "
        elif but == "allFF" :
            command = 'ALL @ FULL'
        elif but == "all50" :
            command = 'ALL @ 50'
        elif but == "all0" :
            command = 'ALL @ 0'
        elif but == "allFad" :
            command = 'ALL @ '+fadV
        elif but == "allRamp" :
            command = 'ALL @ RAMP'
        elif but == "outLK" :
            outmode = 0
        elif but == "outMerge" :
            outmode = 1
        elif but == "outArtnet" :
            outmode = 2
        else:
            print('>> NO ACTION : ',but)
    
    return { 'state': active, 'command': command, '_ip': _ip, '_mask': _mask, '_univ': _univ, 'outmode': outmode}

# démarrage du serveur
port = int(os.environ.get("PORT", 17995))
run(host='0.0.0.0', port=port)	

