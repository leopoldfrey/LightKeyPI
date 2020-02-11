import os, re, json
from bottle import template, static_file, route, run

print("LightKeyPI starting...")

# état du serveur on/off
active = True
# commande en cours
command = "none"
commands = []
last = "none"
buffer = []
# valeur du potard page 2 (0-100%)
fadV = "0"
# mode de sortie
outmode = 0 # 0 : light only / 1 : merge / 2 : artnet
# config réseau
_ip = "2.0.0.1"
_mask = "255.0.0.0"
_univ = "0.0.1"

# stockage des mémoires et leur état on/off
m1on = False
m1 = []
m2on = False
m2 = []
m3on = False
m3 = []
m4on = False
m4 = []
m5on = False
m5 = []

# sert à retourner les infos à la page web et à stocker la config dans le fichier json
def response():
    return { 'state': active, 
            'command': command, 
            'commands': commands, 
            '_ip': _ip, 
            '_mask': _mask, 
            '_univ': _univ, 
            'outmode': outmode, 
            'm1': { 
                'on': m1on, 
                'content':m1 
                }, 
            'm2': {
                'on':m2on, 
                'content':m2
                }, 
            'm3': {
                'on':m3on,
                'content':m3
                }, 
            'm4': {
                'on':m4on,
                'content':m4
                }, 
            'm5': {
                'on':m5on,
                'content':m5
                }
            }

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
    return response()

# c'est là que le potard entre
@route('/fader/<v>')
def fader(v):
    global fadV
    global last
    global last
    global command
    fadV = v
    print('> fader :',fadV)
    command = 'ALL @ '+fadV
    last = "allFad"
    testCommand()
    return response()
  
#set IP
@route('/ip/<v>')
def ip(v):
    global _ip
    _ip = v
    print('> TODO ip :', _ip)
    onNetworkChange()
    savePrefs()
    return response()
   
#set Mask 
@route('/mask/<v>')
def mask(v):
    global _mask
    _mask = v
    print('> mask :', _mask)
    onNetworkChange()
    savePrefs()
    return response()
    
#set Universe
@route('/univ/<v>')
def univ(v):
    global _univ
    _univ = v
    print('> univ :', _univ)
    onNetworkChange()
    savePrefs()
    return response()
 
# mettre une mémoire on/off 
@route('/togMem/<m>')    
def togMem(m):
    global m1on
    global m2on
    global m3on
    global m4on
    global m5on
    
    #print("TOGGLE MEM : ", m)
    if(m == "m1" and len(m1) > 0):
        m1on = not m1on
    elif(m == "m2" and len(m2) > 0):
        m2on = not m2on
    elif(m == "m3" and len(m3) > 0):
        m3on = not m3on
    elif(m == "m4" and len(m4) > 0):
        m4on = not m4on
    elif(m == "m5" and len(m5) > 0):
        m5on = not m5on
        
    interpAll()
    return response()

# stocker la trame dans une mémoire
@route('/recMem/<m>')
def recMem(m):
    global m1on
    global m2on
    global m3on
    global m4on
    global m5on
    #print("REC MEM : ", m)
    if(len(commands)==0):
        return
    if(m == 'm1'):
        m1on = True
        m1.clear()
        for c in commands :
            m1.append(c)
        clearCommands()
    elif m == 'm2':
        m2on = True
        m2.clear()
        for c in commands :
            m2.append(c)
        clearCommands()
    elif m == 'm3':
        m3on = True
        m3.clear()
        for c in commands :
            m3.append(c)
        clearCommands()
    elif m == 'm4':
        m4on = True
        m4.clear()
        for c in commands :
            m4.append(c)
        clearCommands()
    elif m == 'm5':
        m5on = True
        m5.clear()
        for c in commands :
            m5.append(c)
        clearCommands()
            
    savePrefs()
    interpAll()
    return response()
 
# vider une mémoire    
@route('/delMem/<m>')
def delMem(m):
    #print("DEL MEM : ", m)
    if(m == 'm1'):
        m1on = False
        m1.clear()
    elif m == 'm2':
        m2on = False
        m2.clear()
    elif m == 'm3':
        m3on = False
        m3.clear()
    elif m == 'm4':
        m4on = False
        m4.clear()
    elif m == 'm5':
        m5on = False
        m5.clear()
       
    savePrefs()
    interpAll()
    return response()
   
#sauvegarde des préférences 
def savePrefs():
    with open('lkpi-config.json', 'w', encoding='utf-8') as f:
        json.dump(response(),f, ensure_ascii=False, indent=4)
    
#lecture des préférences (au chargement)
def readPrefs():
    print("Reading preferences...")
    global outmode
    global _ip
    global _mask
    global _univ
    global m1
    global m2
    global m3
    global m4
    global m5

    with open('lkpi-config.json') as f:
        data = json.load(f)
        print(json.dumps(data, indent=4, sort_keys=True))
        outmode = data['outmode']
        _ip = data['_ip']
        _mask = data['_mask']
        _univ = data['_univ']
        m1 = data['m1']['content']
        m2 = data['m2']['content']
        m3 = data['m3']['content']
        m4 = data['m4']['content']
        m5 = data['m5']['content']
        print("...done")
        onNetworkChange()

# tous les autres boutons
@route('/button/<but>')
def button(but):
    print('> button :',but)
    global command
    global last
    global active
    global outmode
    if but == "active" :
        if active:
            active = False
        else:
            active = True
    elif but == "command" :
        #command = "none"
        #print("(click on command line, does nothing)")
        pass
    elif but == "mode" :
        #command = "none"
        #print("(click on mode, does nothing on server)")
        pass
    elif but == "outLK" :
        outmode = 0
        savePrefs()
        onNetworkChange()
    elif but == "outMerge" :
        outmode = 1
        savePrefs()
        onNetworkChange()
    elif but == "outArtnet" :
        outmode = 2
        savePrefs()
        onNetworkChange()
    else:
        if command == "none":
            command = ""
            last = "none"
        if but == "1" :
            command += "1"
            last = "num"
        elif but == "2" :
            command += "2"
            last = "num"
        elif but == "3" :
            command += "3"
            last = "num"
        elif but == "4" :
            command += "4"
            last = "num"
        elif but == "5" :
            command += "5"
            last = "num"
        elif but == "6" :
            command += "6"
            last = "num"
        elif but == "7" :
            command += "7"
            last = "num"
        elif but == "8" :
            command += "8"
            last = "num"
        elif but == "9" :
            command += "9"
            last = "num"
        elif but == "0" :
            if last == "num" or last == "at":
                command += "0"
                last = "num"
        elif but == "plus" :
            if last == "num":
                command += " + "
                last = "plus"
        elif but == "minus" :
            if last == "num":
                command += " - "
                last = "minus"
        elif but == "thru" :
            if last == "num":
                command += " THRU "
                last = "thru"
        elif but == "at" :
            if last == "at":
                    command += " FULL"
                    last = "full"
            elif last == "num":
                command += " @ "
                last = "at"
        elif but == "clear" :
            clear()
        elif but == "allFad" :
            command = 'ALL @ '+fadV
            last = "allFad"
        elif but == "allRamp" :
            command = 'ALL @ RAMP'
            last = "allRamp"
        else:
            print('>> NO ACTION : ',but)
    
    testCommand()
    return response()

# vider la commande / la trame en cours
def clear():
    global last
    global commands
    global command
    print('CLEAR')
    if last == "pop" :
        commands.clear()
        command = "none"
        last = "none"
    elif last == "none" :
        commands.pop()
        command = "none"
        last = "pop"
    elif last == "num" :
        command = command[:-1]
    elif last == "plus" :
        command = command[:-3]
    elif last == "minus" :
        command = command[:-3]
    elif last == "thru" :
        command = command[:-6]
    elif last == "at" :
        command = command[:-3]
    elif last == "full" :
        command = command[:-5]
    else:
        command = "none"
    
    if len(command) == 0: 
        command = "none"
        last = "none"
    elif command == "none":
        last = "none"
    elif re.findall("[0-9]", command[-1:]):
        last = "num"
    elif command[-3:] == " + ":
        last = "plus"
    elif command[-3:] == " - ":
        last = "minus"
    elif command[-3:] == " @ ":
        last = "at"
    elif command[-5:] == " FULL":
        last = "full"
    elif command[-6:] == " THRU ":
        last = "full"
    else:
        command = "none"
        last = "none"
        #print("OTHER "+command[-6:])

# initialise/vide le buffer dmx
def clearBuffer():
    global buffer
    buffer.clear()
    for x in range(512):
        buffer.append(0)
        
# vide la trame en cours
def clearCommands():
    global commands
    commands.clear()
  
# teste si la commande en cours est terminée (2 digits après un @ ou All Ramp)    
def testCommand():
    global command
    global commands
    global last
    #print("[-2:1] \"",command[-2:], "\"")
    if command == "none":
        return
    if last == "allRamp" or last == "allFad":
        clearCommands()
        interpCommand()
    elif re.findall(" @ ", command):
        if re.findall("FULL", command) or re.match(r'^([\d]+)$', command[-2:]) :
            interpCommand()
 
# ajoute la commande en cours à la trame    
def interpCommand():
    global command
    global commands
    print("LAST CMD : ", command)
    commands.append(command)
    command = "none"
    interpAll()

# interprète toute les commandes de la trame + les mémoires      
def interpAll():
    if m1on:
        for x in m1 :
            print("INTERP M1 : ", x)
    if m2on:
        for x in m2 :
            print("INTERP M2 : ", x)
    if m3on:
        for x in m3 :
            print("INTERP M3 : ", x)
    if m4on:
        for x in m4 :
            print("INTERP M4 : ", x)
    if m5on:
        for x in m5 :
            print("INTERP M5 : ", x)
    for x in commands :
        print("INTERP GLOBAL : ", x)

# envoie le buffer dans le DMX     
def sendBuffer():
    print("TODO SEND BUFFER TO DMX")
    #dépends de outmode & active & paramètres réseau
  
# si les paramètres réseau outmode/ip/mask/univ change c'est ici que ça se passe 
def onNetworkChange():
    print("TODO NETWORK PARAMETERS CHANGED")   

# init 
clearBuffer()
readPrefs()

# démarrage du serveur
port = int(os.environ.get("PORT", 17995))
run(host='0.0.0.0', port=port)	

