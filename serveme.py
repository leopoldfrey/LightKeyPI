import os, re, json
from bottle import static_file, template, Bottle

class LightKeyServer():
    
    def __init__(self):
        # état du serveur on/off
        self.active = True
        # commande en cours
        self.command = "none"
        self.commands = []
        self.last = "none"
        self.buffer = []
        # valeur du potard page 2 (0-100%)
        self.fadV = "0"
        # mode de sortie
        self.outmode = 0 # 0 : light only / 1 : merge / 2 : artnet
        # config réseau
        self._ip = "2.0.0.1"
        self._mask = "255.0.0.0"
        self._univ = "0.0.1"
        
        # stockage des mémoires et leur état on/off
        self.m1on = False
        self.m1 = []
        self.m2on = False
        self.m2 = []
        self.m3on = False
        self.m3 = []
        self.m4on = False
        self.m4 = []
        self.m5on = False
        self.m5 = []
        
        self.config = 'lkpi-config.json'
        # init 
        self.clearBuffer()
        self.readPrefs()
        
        print("LightKeyPI starting...")
        
        self.host = '0.0.0.0'
        self.port = int(os.environ.get("PORT", 17995))
        self.server = Bottle()
        self.route()     
        
    def start(self):
        # démarrage du serveur
        self.server.run(host=self.host, port=self.port) 
        
    def savePrefs(self):
        #sauvegarde des préférences 
        with open(self.config, 'w', encoding='utf-8') as f:
            json.dump(self.response(),f, ensure_ascii=False, indent=4)
        
    def readPrefs(self):
        #lecture des préférences (au chargement)
        print("Reading preferences...")
        with open(self.config) as f:
            data = json.load(f)
            print(json.dumps(data, indent=4, sort_keys=True))
            self.outmode = data['outmode']
            self._ip = data['_ip']
            self._mask = data['_mask']
            self._univ = data['_univ']
            self.m1 = data['m1']['content']
            self.m2 = data['m2']['content']
            self.m3 = data['m3']['content']
            self.m4 = data['m4']['content']
            self.m5 = data['m5']['content']
            print("...done")
            self.onNetworkChange()
    
    def route(self):
        self.server.route('/', method="GET", callback=self.index)
        self.server.route('/<filename>', method="GET", callback=self.serve)
        self.server.route('/state', method="GET", callback=self.state)
        self.server.route('/fader/<v>', method="GET", callback=self.fader)
        self.server.route('/ip/<v>', method="GET", callback=self.ip)
        self.server.route('/mask/<v>', method="GET", callback=self.mask)
        self.server.route('/univ/<v>', method="GET", callback=self.univ)
        self.server.route('/togMem/<m>', method="GET", callback=self.togMem)
        self.server.route('/recMem/<m>', method="GET", callback=self.recMem)
        self.server.route('/delMem/<m>', method="GET", callback=self.delMem)
        self.server.route('/button/<but>', method="GET", callback=self.button)
    
    def index(self):
        # fonction qui renvoie la page web
        return template('index')
    
    def serve(self, filename):
        # fonction pour renvoyer les fichiers statiques
        return static_file(filename, root='./'); 

    def state(self):
        # retourne l'état en cours du serveur vers la page web
        return self.response()

    def fader(self, v):
        # c'est là que le potard entre
        self.fadV = v
        #print('> fader :',self.fadV)
        self.command = 'ALL @ '+self.fadV
        self.last = "allFad"
        self.testCommand()
        return self.response()

    def ip(self, v):
        #set IP
        self._ip = v
        print('> TODO ip :', self._ip)
        self.onNetworkChange()
        self.savePrefs()
        return self.response()
       
    def mask(self, v):
        #set Mask 
        self._mask = v
        print('> mask :', self._mask)
        self.onNetworkChange()
        self.savePrefs()
        return self.response()
        
    def univ(self, v):
        #set Universe
        self._univ = v
        print('> univ :', self._univ)
        self.onNetworkChange()
        self.savePrefs()
        return self.response()

    def togMem(self, m):
        # mettre une mémoire on/off 
        #print("TOGGLE MEM : ", m)
        if(m == "m1" and len(self.m1) > 0):
            self.m1on = not self.m1on
        elif(m == "m2" and len(self.m2) > 0):
            self.m2on = not self.m2on
        elif(m == "m3" and len(self.m3) > 0):
            self.m3on = not self.m3on
        elif(m == "m4" and len(self.m4) > 0):
            self.m4on = not self.m4on
        elif(m == "m5" and len(self.m5) > 0):
            self.m5on = not self.m5on
            
        self.interpAll()
        return self.response()

    def recMem(self, m):
        # stocker la trame dans une mémoire
        #print("REC MEM : ", m)
        if(len(self.commands)==0):
            return
        if(m == 'm1'):
            self.m1on = True
            self.m1.clear()
            for c in self.commands :
                self.m1.append(c)
            self.clearCommands()
        elif m == 'm2':
            self.m2on = True
            self.m2.clear()
            for c in self.commands :
                self.m2.append(c)
            self.clearCommands()
        elif m == 'm3':
            self.m3on = True
            self.m3.clear()
            for c in self.commands :
                self.m3.append(c)
            self.clearCommands()
        elif m == 'm4':
            self.m4on = True
            self.m4.clear()
            for c in self.commands :
                self.m4.append(c)
            self.clearCommands()
        elif m == 'm5':
            self.m5on = True
            self.m5.clear()
            for c in self.commands :
                self.m5.append(c)
            self.clearCommands()
                
        self.savePrefs()
        self.interpAll()
        return self.response()
     
    def delMem(self, m):
        # vider une mémoire    
        #print("DEL MEM : ", m)
        if(m == 'm1'):
            self.m1on = False
            self.m1.clear()
        elif m == 'm2':
            self.m2on = False
            self.m2.clear()
        elif m == 'm3':
            self.m3on = False
            self.m3.clear()
        elif m == 'm4':
            self.m4on = False
            self.m4.clear()
        elif m == 'm5':
            self.m5on = False
            self.m5.clear()
           
        self.savePrefs()
        self.interpAll()
        return self.response()

    def button(self, but):
        #print('> button :',but)
        if but == "active" :
            self.togActive()
        elif but == "command" :
            #command = "none"
            #print("(click on command line, does nothing)")
            pass
        elif but == "mode" :
            #command = "none"
            #print("(click on mode, does nothing on server)")
            pass
        elif but == "outLK" :
            self.outmode = 0
            self.savePrefs()
            self.onNetworkChange()
        elif but == "outMerge" :
            self.outmode = 1
            self.savePrefs()
            self.onNetworkChange()
        elif but == "outArtnet" :
            self.outmode = 2
            self.savePrefs()
            self.onNetworkChange()
        else:
            if self.command == "none":
                self.command = ""
                self.last = "none"
            if but == "1" :
                self.command += "1"
                self.last = "num"
            elif but == "2" :
                self.command += "2"
                self.last = "num"
            elif but == "3" :
                self.command += "3"
                self.last = "num"
            elif but == "4" :
                self.command += "4"
                self.last = "num"
            elif but == "5" :
                self.command += "5"
                self.last = "num"
            elif but == "6" :
                self.command += "6"
                self.last = "num"
            elif but == "7" :
                self.command += "7"
                self.last = "num"
            elif but == "8" :
                self.command += "8"
                self.last = "num"
            elif but == "9" :
                self.command += "9"
                self.last = "num"
            elif but == "0" :
                if self.last == "num" or self.last == "at":
                    self.command += "0"
                    self.last = "num"
            elif but == "plus" :
                if self.last == "num":
                    self.command += " + "
                    self.last = "plus"
            elif but == "minus" :
                if self.last == "num":
                    self.command += " - "
                    self.last = "minus"
            elif but == "thru" :
                if self.last == "num":
                    self.command += " THRU "
                    self.last = "thru"
            elif but == "at" :
                if self.last == "at":
                        self.command += " FULL"
                        self.last = "full"
                elif self.last == "num":
                    self.command += " @ "
                    self.last = "at"
            elif but == "clear" :
                self.clear()
            elif but == "allFad" :
                self.command = 'ALL @ '+self.fadV
                self.last = "allFad"
            elif but == "allRamp" :
                self.command = 'ALL @ RAMP'
                self.last = "allRamp"
            else:
                print('>> NO ACTION : ',but)
        
        self.testCommand()
        return self.response()

    def response(self):
        # sert à retourner les infos à la page web et à stocker la config dans le fichier json
        return { 'state': self.active, 
                'command': self.command, 
                'commands': self.commands, 
                '_ip': self._ip, 
                '_mask': self._mask, 
                '_univ': self._univ, 
                'outmode': self.outmode, 
                'm1': { 
                    'on': self.m1on, 
                    'content': self.m1 
                    }, 
                'm2': {
                    'on': self.m2on, 
                    'content': self.m2
                    }, 
                'm3': {
                    'on': self.m3on,
                    'content': self.m3
                    }, 
                'm4': {
                    'on': self.m4on,
                    'content': self.m4
                    }, 
                'm5': {
                    'on': self.m5on,
                    'content': self.m5
                    }
                }
    
    def clear(self):
        # vider la commande / la trame en cours
        print('CLEAR')
        if self.last == "pop" :
            self.commands.clear()
            self.command = "none"
            self.last = "none"
        elif self.last == "none" :
            self.commands.pop()
            self.command = "none"
            self.last = "pop"
        elif self.last == "num" :
            self.command = self.command[:-1]
        elif self.last == "plus" :
            self.command = self.command[:-3]
        elif self.last == "minus" :
            self.command = self.command[:-3]
        elif self.last == "thru" :
            self.command = self.command[:-6]
        elif self.last == "at" :
            self.command = self.command[:-3]
        elif self.last == "full" :
            self.command = self.command[:-5]
        else:
            self.command = "none"
        
        if len(self.command) == 0: 
            self.command = "none"
            self.last = "none"
        elif self.command == "none":
            self.last = "none"
        elif re.findall("[0-9]", self.command[-1:]):
            self.last = "num"
        elif self.command[-3:] == " + ":
            self.last = "plus"
        elif self.command[-3:] == " - ":
            self.last = "minus"
        elif self.command[-3:] == " @ ":
            self.last = "at"
        elif self.command[-5:] == " FULL":
            self.last = "full"
        elif self.command[-6:] == " THRU ":
            self.last = "full"
        else:
            self.command = "none"
            self.last = "none"
            #print("OTHER "+self.command[-6:])
            
        self.interpAll()
    
    def clearBuffer(self):
        # initialise/vide le buffer dmx
        self.buffer.clear()
        for _x in range(512):
            self.buffer.append(0)
            
    def clearCommands(self):
        # vide la trame en cours
        self.commands.clear()
      
    def testCommand(self):
        # teste si la commande en cours est terminée (2 digits après un @ ou All Ramp)    
        #print("[-2:1] \"",self.command[-2:], "\"")
        if self.command == "none":
            return
        if self.last == "allRamp" or self.last == "allFad":
            self.clearCommands()
            self.interpCommand()
        elif re.findall(" @ ", self.command):
            if re.findall("FULL", self.command) or re.match(r'^([\d]+)$', self.command[-2:]) :
                self.interpCommand()
     
    def interpCommand(self):
        # ajoute la commande en cours à la trame    
        #print("LAST CMD : ", command)
        self.commands.append(self.command)
        self.command = "none"
        self.interpAll()
    
    def interpAll(self):
        # interprète toutes les commandes de la trame + les mémoires      
        self.clearBuffer()
        if len(self.commands) > 0 :
            #print("INTERP GLOBAL")
            for x in self.commands :
                self.interpOne(x)
        if self.m1on:
            #print("INTERP M1")
            for x in self.m1 :
                self.interpOne(x)
        if self.m2on:
            #print("INTERP M2")
            for x in self.m2 :
                self.interpOne(x)
        if self.m3on:
            #print("INTERP M3")
            for x in self.m3 :
                self.interpOne(x)
        if self.m4on:
            #print("INTERP M4")
            for x in self.m4 :
                self.interpOne(x)
        if self.m5on:
            #print("INTERP M5")
            for x in self.m5 :
                self.interpOne(x)
                            
        self.sendBuffer()
    
    def interpOne(self, cmd):
        # interprète une seule commande      
        #print("INTERP ",cmd)
        spl = cmd.split(' @ ')
        if spl[1] == "FULL" :
            atValue = 100
        elif spl[1] == "RAMP" :
            atValue = "RAMP"
        else:
            try:
                atValue = int(spl[1])
            except:
                atValue = 100
        idx = 0
        prevNum = -1
        prevFunc = "none"
        selSpl = spl[0].split(' ')
        selection = []
        while(idx < len(selSpl)):
            try:
                n = int(selSpl[idx])
                if n > 512 :
                    n = 512
                if(prevFunc == "none"):
                    selection.append(n)
                elif prevFunc == "+" :
                    selection.append(n)
                elif prevFunc == "-" :
                    selection.remove(n)
                elif prevFunc == "THRU" :
                    for x in range(prevNum, n+1):
                        selection.append(x)
                prevNum = n
            except:
                if selSpl[idx] == "ALL" :
                    for x in range(1, 512+1):
                        selection.append(x)
                else:   
                    prevFunc = selSpl[idx]
            idx += 1
        selection = list(set(selection))
        #print(">>>>> ",selection, " @ ", atValue)
        for x in selection :
            self.buffer[x-1] = atValue
    
    def togActive(self):
        self.active = not self.active
        print("TODO ACTIVE/INACTIVE ", self.active)
    
    def sendBuffer(self):
        # envoie le buffer dans le DMX     
        print("TODO SEND BUFFER TO DMX ", self.buffer)
        #dépends de outmode & active & paramètres réseau
        #attention quand ALL @ RAMP est activé la valeur dans le buffer est 'RAMP'
      
    def onNetworkChange(self):
        # si les paramètres réseau outmode/ip/mask/univ changent c'est ici que ça se passe 
        print("TODO NETWORK PARAMETERS CHANGED")

# tous les autres boutons

if __name__ == "__main__":
    server = LightKeyServer()
    server.start()
