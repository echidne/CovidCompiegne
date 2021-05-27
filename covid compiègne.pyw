############################################
#               Les Modules                #
############################################

# Import des librairies standards
import time
from datetime import date
import webbrowser
import subprocess
import sys
import platform

# Import  des librairies non-standards

# requests pour interroger l'api de Doctolib
try :
    import requests
except ModuleNotFoundError :
    subprocess.run([sys.executable, "-m", "pip", "install", "requests"])

# pynput pour capturer les évènements en dehors du programme (ici les évènements clavier)
try :
    from pynput import keyboard
except ModuleNotFoundError :
    subprocess.run([sys.executable, "-m", "pip", "install", "pynput"])

# pyttstx3 pour une notification sonore
try :
    import pyttsx3
except ModuleNotFoundError :
    subprocess.run([sys.executable, "-m", "pip", "install", "pyttsx3"])

# win10toast_click pour un toaster avec click sous Windows 10
try :
    from win10toast_click import ToastNotifier
except ModuleNotFoundError :
    if platform.platform().startswith('Windows-10'):
        subprocess.run([sys.executable, "-m", "pip", "install", "win10toast-click"])
    else :
        print('il faut être sous windows 10')
        sys.exit() # on arrete le script là si on est pas sous windows 10
        

#############################################
#         Les variables globales            #
#############################################

# variable qui contient l'adresse de la page web pour réserver sa vaccination
page_url ="https://www.doctolib.fr/vaccination-covid-19/compiegne/centre-de-vaccination-covid-compiegne-arc?" 

# header pour éviter que l'interrogation par request se fasse rejetter (on se fait passer pour Chrome)
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}

# l'intervalle de temps pour interroger le site et ne pas le surcharger
intervalle = 30

##############################################
#              Fonctions                     #
##############################################

def open_url():
    ''' Fonction qui va ouvrir la page web du centre de vaccination '''
    try: 
        requests.get(page_url)
        webbrowser.open_new(page_url)
    except requests.ConnectionError : 
        print('Failed to open URL. Unsupported variable type.')

def on_press_loop(key):
    ''' Fonction qui va permettre d'interrompre l'appli par l'appuie sur la touche F12 '''
    if key == keyboard.Key.f12:
        return False

def notif_sonore(text):
    ''' Fonction qui va faire parler dans les chaumières '''
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def notif_toast(notification, message, icon_path, threaded, duration, callback):
    ''' Fonction qui va faire toaster '''
    # création de l'instance toaster
    toaster = ToastNotifier()
    # on lance le toast (servi bien chaud sur votre bureau)
    toaster.show_toast(notification, message, icon_path, threaded, duration, callback)

def requete_doctolib(date_du_jour, id_motif, id_agendas, secteur, id_centre, headers):
    ''' Fonction qui va interroger l'appli Doctolib '''
    requete = f"https://www.doctolib.fr/availabilities.json?start_date={date_du_jour}&visit_motive_ids={id_motif}&agenda_ids={id_agendas}&insurance_sector={secteur}&practice_ids={id_centre}&destroy_temporary=true&limit=4"
    return requests.get(requete, headers=headers)



##############################################
#          Partie principale                 #
##############################################


#  une petite notif pour dire que l'appli est lancée
notif_sonore("L'application est lancée")
notif_toast("appli Covid en route"," ", None, True, 5, None)


# on met en place le Context Manager qui va nous permettre d'interrompre l'appli par pression sur F12
with keyboard.Listener(on_press=on_press_loop) as listener:
    # on récupère le temps actuel afin de mettre en place une interrogation périodique du site non bloquante
    tw = time.time()
    # maintenant on met en place la boucle 
    while True :
        
        # on récupère la date du jour au bon format (si on la met en dehors de la boucle il faut penser à relancer l'appli aprés minuit :))
        today =  date.today().isoformat()
        # on récupère l'instant t 
        t = time.time()
        # et on compare avec tw pour savoir si l'intervalle de temps est passé
        if t - tw > intervalle :
            # on fait notre requête (attention cette requete n'est valable que pour Compiègne à vous de changer les paramêtres pour votre centre)
            req_first_Pfizer = requete_doctolib(today, "2553369", "470011-434292-434257-412372-435494-448029-432422-412370", "public", "165271",header)
            # on teste si la requête retourne bien un résultat pour 'total'
            if req_first_Pfizer.json().get('total') != None:
                # si oui on récupère le nombre de doses dispo
                doses_Pfizer = req_first_Pfizer.json().get('total')
                # si il n'y a pas de doses de dispo on vérifie qu'il n'y ait pas déjà une arrivée de doses prévues
                if doses_Pfizer == 0 and req_first_Pfizer.json().get('next_slot') != None:
                    # on récupère la nouvelle date et on réinterroge
                    nextday = req_first_Pfizer.json().get('next_slot')
                    req_first_Pfizer = requete_doctolib(nextday, "2553369", "470011-434292-434257-412372-435494-448029-432422-412370", "public", "165271",header)
                    doses_Pfizer = req_first_Pfizer.json().get('total')
                # si des doses sont dispo on lance les notifications
                if doses_Pfizer > 0:
                    notif_sonore("grouillez vous il y a des doses de dispo dans votre centre")
                    notif_toast(f"doses disponibles au centre de vaccination de Compiègne: {doses_Pfizer}","Cliquer pour ouvrir la page du centre >>>", None, True, 10, open_url)
            # si la requete initiale a échoué c'est qu'il ya quelque chose de pourri dans votre requete et on vous propose de refaire un tour sur le site pour vérifier
            else:
                notif_sonore("votre requete pour Pfizer a planté")
                notif_toast("problème pour votre requete Pfizer","Cliquer pour acceder au site", None, True, 5, open_url)         

            # on réinitialise tw
            tw = time.time()

        # si on a appuyé sur F12 on interrompt la boucle et l'appli
        if not listener.running:
            notif_sonore("application arrétée")
            break
        
