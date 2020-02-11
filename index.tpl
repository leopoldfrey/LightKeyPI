<!DOCTYPE html>
<html lang="fr">
<head>
	<meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="Akwariom's LightKey is a remote control for the LightKeyPI device">
    <link rel="apple-touch-icon" sizes="57x57" href="/apple-icon-57x57.png">
	<link rel="apple-touch-icon" sizes="60x60" href="/apple-icon-60x60.png">
	<link rel="apple-touch-icon" sizes="72x72" href="/apple-icon-72x72.png">
	<link rel="apple-touch-icon" sizes="76x76" href="/apple-icon-76x76.png">
	<link rel="apple-touch-icon" sizes="114x114" href="/apple-icon-114x114.png">
	<link rel="apple-touch-icon" sizes="120x120" href="/apple-icon-120x120.png">
	<link rel="apple-touch-icon" sizes="144x144" href="/apple-icon-144x144.png">
	<link rel="apple-touch-icon" sizes="152x152" href="/apple-icon-152x152.png">
	<link rel="apple-touch-icon" sizes="180x180" href="/apple-icon-180x180.png">
	<link rel="icon" type="image/png" sizes="192x192"  href="/android-icon-192x192.png">
	<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
	<link rel="icon" type="image/png" sizes="96x96" href="/favicon-96x96.png">
	<link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">
	<link rel="manifest" href="/manifest.json">
	<meta name="msapplication-TileColor" content="#ffffff">
	<meta name="msapplication-TileImage" content="/ms-icon-144x144.png">
	<meta name="theme-color" content="#ffffff">
    <title>LightKeyPI</title>
    <link rel="stylesheet" type="text/css" href="./bootstrap-slider.min.css">
	<link rel="stylesheet" type="text/css" href="./style.css">
	<script src="./bootstrap-slider.min.js"></script> 
    <!-- script src="./jquery-2.2.4.min.js"></script--> 
    <script src="./jquery-3.4.1.min.js"></script> 
        
   	<script>
   		// mode ou page
   		mode = 0;
   		_ip = "";
   		_mask = "";
   		_univ = "";
   		memF = "none";
   		var slider;
	
   		// envoie la valeur du potard au serveur
		function sendFader() {
	   		fadV = $("#slider").val();
	   		//console.log("Fader : "+fadV);
	   		$.get('/fader/'+fadV, function( data ) {
				treatData(data);
			});
	   	}
	   	
		// affecte une valeur au fader
   		function setFader(v) {
   			slider.setValue(v);
   			sendFader();
   		}
   		
   		// envoie des boutons au serveur
		function clickBut(func) {
			//console.log("I was clicked : "+func);
	    	$.get('/button/'+func, function( data ) {
				treatData(data);
			});
		}
	    
		// demande l'ip à l'utilisateur et l'envoie au serveur
		function setIp() {
			var ip = prompt("Enter Ip Address :", _ip);
			if (ip == null || ip == "") {
			} else {
				$.get('/ip/'+ip, function( data ) {
					treatData(data);
				});
			}
			
	    }
		
		// demande le mask à l'utilisateur et l'envoie au serveur
		function setMask() {
	    	var mask = prompt("Enter Mask :", _mask);
			if (mask == null || mask == "") {
			} else {
				$.get('/mask/'+mask, function( data ) {
					treatData(data);
				});
			}
			
	    }
	    
		// demande l'univers à l'utilisateur et l'envoie au serveur
		function setUniv() {
	    	var univ = prompt("Enter Universe (universe.subnet.net) :", _univ);
			if (univ == null || univ == "") {
			} else {
			   $.get('/univ/'+univ, function( data ) {
					treatData(data);
				});
			}
			
	    }
	    
		// récupère l'état du serveur
		function getState() {
			//console.log("getState");
			$.get( "/state", function( data ) {
				treatData(data);
			});
		}
		
		// traite les données reçues par le serveur
		function treatData(data) {
			//console.log(data);
			//console.log("state: "+data.state)
			//console.log("command: "+data.command)
			
			// état on/off
			if(data.state == false)
			{
				$("#active").css('background-color', 'rgb(255,78,18)');
				$("#active").html("OFF");
			} else {
				$("#active").css('background-color', 'rgb(41,253,47)');
				$("#active").html("ON");
			}
			
			// commande en cours (+ affichage des mémoires si actives)
			if(data.command == "none" || data.command == "") {
				$("#command").css('font-size', '10px');
				if((data.commands && data.commands != "") 
						|| data.m1.on && data.m1.content != "" 
						|| data.m2.on && data.m2.content != "" 
						|| data.m3.on && data.m3.content != "" 
						|| data.m4.on && data.m4.content != "" 
						|| data.m5.on && data.m5.content != "") {
					$("#command").html("");
					if(data.m1.on && data.m1.content != null)
						for (var c in data.m1.content) {
						     //console.log(data.commands[c]);
						     $("#command").append("<li class='mem'>"+data.m1.content[c]+"</li>");
						}
					if(data.m2.on && data.m2.content != null)
						for (var c in data.m2.content) {
						     //console.log(data.commands[c]);
						     $("#command").append("<li class='mem'>"+data.m2.content[c]+"</li>");
						}
					if(data.m3.on && data.m3.content != null)
						for (var c in data.m3.content) {
						     //console.log(data.commands[c]);
						     $("#command").append("<li class='mem'>"+data.m3.content[c]+"</li>");
						}
					if(data.m4.on && data.m4.content != null)
						for (var c in data.m4.content) {
						     //console.log(data.commands[c]);
						     $("#command").append("<li class='mem'>"+data.m4.content[c]+"</li>");
						}
					if(data.m5.on && data.m5.content != null)
						for (var c in data.m5.content) {
						     //console.log(data.commands[c]);
						     $("#command").append("<li class='mem'>"+data.m5.content[c]+"</li>");
						}
					for (var c in data.commands) {
					     //console.log(data.commands[c]);
					     $("#command").append("<li class='def'>"+data.commands[c]+"</li>");
					}
					$("#command").css('background-color', 'rgb(41,253,47)');
				} else {
					$("#command").html("");
					$("#command").css('background-color', 'rgb(17,127,126)');
				}
			} else {
				$("#command").css('font-size', '16px');
				$("#command").html(data.command);
			}
			
			// configuration réseau
			_ip = data._ip;
			_mask = data._mask;
			_univ = data._univ;
			
			$("#dispIP").html("IP   : "+_ip+"<br/>MASK : "+_mask+"<br/>UNIV : "+_univ);
			
			// mode d'output
			switch(data.outmode) {
				case 0: // lightkey only
					$("#outLK").css('background-color', 'rgb(41,253,47)');
					$("#outMerge").css('background-color', 'gray');
					$("#outArtnet").css('background-color', 'gray');
					break;
				case 1: // merge
					$("#outLK").css('background-color', 'gray');
					$("#outMerge").css('background-color', 'rgb(41,253,47)');
					$("#outArtnet").css('background-color', 'gray');
					break;
				case 2: // artnet
					$("#outLK").css('background-color', 'gray');
					$("#outMerge").css('background-color', 'gray');
					$("#outArtnet").css('background-color', 'rgb(41,253,47)');
					break;
			}
			
			if(data.m1.on) {
				$("#m1").removeClass("but4notnull");	
				$("#m1").addClass("but4on");
			} else {
				$("#m1").removeClass("but4on");
				if(data.m1.content != "")
				{
					$("#m1").addClass("but4notnull");	
				} else {
					$("#m1").removeClass("but4notnull");	
				}
			}
			
			if(data.m2.on) {
				$("#m2").removeClass("but4notnull");	
				$("#m2").addClass("but4on");
			} else {
				$("#m2").removeClass("but4on");
				if(data.m2.content != "")
				{
					$("#m2").addClass("but4notnull");	
				} else {
					$("#m2").removeClass("but4notnull");	
				}
			}
			
			if(data.m3.on) {
				$("#m3").removeClass("but4notnull");	
				$("#m3").addClass("but4on");
			} else {
				$("#m3").removeClass("but4on");
				if(data.m3.content != "")
				{
					$("#m3").addClass("but4notnull");	
				} else {
					$("#m3").removeClass("but4notnull");	
				}
			}
			
			if(data.m4.on) {
				$("#m4").removeClass("but4notnull");	
				$("#m4").addClass("but4on");
			} else {
				$("#m4").removeClass("but4on");
				if(data.m4.content != "")
				{
					$("#m4").addClass("but4notnull");	
				} else {
					$("#m4").removeClass("but4notnull");	
				}
			}
			
			if(data.m5.on) {
				$("#m5").removeClass("but4notnull");	
				$("#m5").addClass("but4on");
			} else {
				$("#m5").removeClass("but4on");
				if(data.m5.content != "")
				{
					$("#m5").addClass("but4notnull");	
				} else {
					$("#m5").removeClass("but4notnull");	
				}
			}
		}
		
		// traitements des boutons rec/del
		function treatMem() {
			switch(memF)
			{
				case "rec":
					$("#del").css('background-color', 'rgb(67,187,186)');
					$("#rec").css('background-color', 'rgb(255,78,18)');
					break;
				case "del":
					$("#rec").css('background-color', 'rgb(67,187,186)');
					$("#del").css('background-color', 'rgb(255,78,18)');
					break;
				default:
					$("#rec").css('background-color', 'rgb(67,187,186)');
					$("#del").css('background-color', 'rgb(67,187,186)');
					break;
			}
		}
		
		function recMem() {
			memF = "rec";
			treatMem();
		}
		
		function delMem() {
			memF = "del";
			treatMem();
		}
		
		// toggle Mem
		function toggleMem(mem) {
			if(memF == "none") {
				$.get('/togMem/'+mem, function( data ) {
					treatData(data);
				});
			} else if (memF == "rec") {
				memF = "none";
				$.get('/recMem/'+mem, function( data ) {
					treatData(data);
				});
			} else if (memF == "del") {
				memF = "none";
				//$("#"+mem).removeClass("but4on");
				//$("#"+mem).removeClass("but4notnull");
				$.get('/delMem/'+mem, function( data ) {
					treatData(data);
				});
			}
			treatMem();
		}
		
		// bascule d'un mode visuel à l'autre
		function switchMode() {
			mode++;
			if(mode > 3)
				mode = 0;
			//console.log("switchMode : "+mode);
			doModeSwitch();
			$.get('/button/mode', function( data ) {
				treatData(data);
			});
		}
	
		function doModeSwitch() {
			$("#content").empty();
			$("#content").append('<div class="crop"><img id="logo" alt="logo akwariom" src="/logo_web.png" onclick="notify(this.id)"></img></div>');
			$("#content").append('<button id="mode" aria-label="Mode" class="but button1 butfont2 b2" onclick="switchMode()">MODE</button>');
			$("#content").append('<button id="active" aria-label="On/Off" class="but button2 butfont2 b3" onclick="clickBut(this.id)">ON</button>');
			$("#content").append('<button id="command" aria-label="Command Line" class="cmd bb3" onclick="clickBut(this.id)"></button>');
			switch(mode)
			{
				case 0: // page 1 (télec)
					$("#content").append('<button id="plus" aria-label="+" class="but button1 b1" onclick="clickBut(this.id)">+</button>');
					$("#content").append('<button id="minus" aria-label="-" class="but button1 b2 butfont3" onclick="clickBut(this.id)">-</button>');
					$("#content").append('<button id="thru" aria-label="thru" class="but button1 butfont2 b3" onclick="clickBut(this.id)">THRU</button>');
					$("#content").append('<button id="7" aria-label="7" class="but button1 b1" onclick="clickBut(this.id)">7</button>');
					$("#content").append('<button id="8" aria-label="8" class="but button1 b2" onclick="clickBut(this.id)">8</button>');
					$("#content").append('<button id="9" aria-label="9" class="but button1 b3" onclick="clickBut(this.id)">9</button>');
					$("#content").append('<button id="4" aria-label="4" class="but button1 b1" onclick="clickBut(this.id)">4</button>');
					$("#content").append('<button id="5" aria-label="5" class="but button1 b2" onclick="clickBut(this.id)">5</button>');
					$("#content").append('<button id="6" aria-label="6" class="but button1 b3" onclick="clickBut(this.id)">6</button>');
					$("#content").append('<button id="1" aria-label="1" class="but button1 b1" onclick="clickBut(this.id)">1</button>');
					$("#content").append('<button id="2" aria-label="2" class="but button1 b2" onclick="clickBut(this.id)">2</button>');
					$("#content").append('<button id="3" aria-label="3" class="but button1 b3" onclick="clickBut(this.id)">3</button>');
					$("#content").append('<button id="clear" aria-label="clear" class="but button1 butfont2 b1" onclick="clickBut(this.id)">CLEAR</button>');
					$("#content").append('<button id="0" aria-label="0" class="but button1 b2" onclick="clickBut(this.id)">0</button>');
					$("#content").append('<button id="at" aria-label="at level" class="but button1 b3 butfont3" onclick="clickBut(this.id)">@</button>');
					break;
				case 1: // page 2 (fader)
					$("#content").append('<button id="allFad" aria-label="all at fader level" class="but button1 b1 butfont4" onclick="clickBut(this.id)">ALL @<br/>FADER</button>');
					$("#content").append('<input id="slider" aria-label="fader" type="text" data-slider-min="0" data-slider-max="100" data-slider-step="1" data-slider-value="0" data-slider-orientation="vertical"/>');
					$("#content").append('<button id="allRamp" aria-label="all at ramp" class="but button1 b1 butfont4" onclick="clickBut(this.id)">ALL @<br/>RAMP</button>');
					$("#content").append('<button id="allFF" aria-label="all at 100%" class="but button1 b1 butfont4" onclick="setFader(100)">ALL @<br/>FULL</button>');
					$("#content").append('<button id="all50" aria-label="all at 50%" class="but button1 b1 butfont4" onclick="setFader(50)">ALL @<br/>50</button>');
					$("#content").append('<button id="all0" aria-label="all at 0%" class="but button1 b1 butfont4" onclick="setFader(0)">ALL @<br/>0</button>');
					slider = new Slider('#slider', {
						reversed: true,
						ticks: [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
						formatter: function(value) {
							return '';
						}
					});
					slider.on('slideStop', function(slideEvt) {
						sendFader();
					});
					break;
				case 2: // page 3 (config)
					$("#content").append('<button id="outLK" aria-label="Only lightkey" class="but button1 bb3 butfont5" onclick="clickBut(this.id)">ONLY LIGHTKEY<br/>ON DMX OUTPUT</button>');
					$("#content").append('<button id="outMerge" aria-label="Merge lightkey and dmx in" class="but button1 bb3 butfont5" onclick="clickBut(this.id)">MERGE DMX-IN & LIGHTKEY<br/>ON DMX OUTPUT</button>');
					$("#content").append('<button id="outArtnet" aria-label="Artnet Output" class="but button1 bb3 butfont5" onclick="clickBut(this.id)">ARTNET OUTPUT</button>');
					$("#content").append('<button id="setIp" aria-label="Set Network Ip Address" class="but button1 b1 butfont5" onclick="setIp()">SET<br/>IP</button>');
					$("#content").append('<button id="setMask" aria-label="Set Network Mask" class="but button1 b2 butfont5" onclick="setMask()">SET<br/>MASK</button>');
					$("#content").append('<button id="setUniv" aria-label="Set Artnet Universe" class="but button1 b3 butfont5" onclick="setUniv()">SET<br/>UNIV</button>');
					$("#content").append('<button id="dispIP" aria-label="Display Network Parameters" class="but button3 bb3 butfont6"></button>');
					break;
				case 3: // page 4 (mémoires)
					$("#content").append('<button id="m1" aria-label="Memory 1" class="but button4 bb2 butfont2" onclick="toggleMem(this.id)">MEM 1</button>');
					$("#content").append('<button id="m2" aria-label="Memory 2" class="but button4 bb2 butfont2" onclick="toggleMem(this.id)">MEM 2</button>');
					$("#content").append('<button id="m3" aria-label="Memory 3" class="but button4 bb2 butfont2" onclick="toggleMem(this.id)">MEM 3</button>');
					$("#content").append('<button id="m4" aria-label="Memory 4" class="but button4 bb2 butfont2" onclick="toggleMem(this.id)">MEM 4</button>');
					$("#content").append('<button id="rec" aria-label="Record memory" class="but button1 butfont2 b3" onclick="recMem()">REC</button>');
					$("#content").append('<button id="m5" aria-label="Memory 5" class="but button4 bb2 butfont2" onclick="toggleMem(this.id)">MEM 5</button>');
					$("#content").append('<button id="del" aria-label="Delete memory" class="but button1 butfont2 b3" onclick="delMem()">DEL</button>');
					break;
			}
			
		}
		
		//initialisation une fois que la page est chargée
		$(window).on("load",function() {
			doModeSwitch();
			getState();
		});
	</script>
</head>
<body>
	<div id="content">
		<!-- c'est ici que vont s'insérer les éléments dynamiquement -->
	</div>
</body>
</html>