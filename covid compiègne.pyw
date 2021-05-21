# Import des Modules Builtins
import requests
from time import sleep
from datetime import date
import webbrowser
import subprocess

# Import  du Toaster pour Windows 10
try :
    from win10toast_click import ToastNotifier
except ModuleNotFoundError :
    subprocess.run( 'pip install win10toast_click')

# création de l'instance toaster
toaster = ToastNotifier()

# ouverture de la page web pour réserver sa vaccination
page_url ="https://www.doctolib.fr/vaccination-covid-19/compiegne/centre-de-vaccination-covid-compiegne-arc?" # variable qui contient l'adresse web

# header pour éviter que l'interrogation par request se fasse rejetter (on se fait passer pour Chrome)
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}

#fonction pour ouvrir la page du centre depuis le toaster
def open_url():
    try: 
        webbrowser.open_new(page_url)
        print('Opening URL...')  
    except: 
        print('Failed to open URL. Unsupported variable type.')



# La boucle qui va interroger le site pour savoir si des doses sont disponibles
while True :
    # on récupère la date du jour au bon format (si on la met en dehors de la boucle il faut penser à relancer l'appli aprés minuit :))
    today =  date.today().isoformat()
    '''
     On récupère les fichiers json contenant les info
     Format du lien :
     start_date={date-du-jour}&visit_motive_ids={id qui indique le type d'injection}&agenda_ids={ids qui varient selon le lieu de vaccination et le type de vaccin}&insurance_sector ={public or private}&practice_ids={id du centre}&destroy_temporary=true&limit=3
    '''
    reqPfizer = requests.get('https://www.doctolib.fr/availabilities.json?start_date='+today+'&visit_motive_ids=2553369&agenda_ids=470011-434292-434257-412372-435494-448029-432422-412370&insurance_sector=public&practice_ids=165271&destroy_temporary=true&limit=3', headers = header)
    reqModerna = requests.get('https://www.doctolib.fr/availabilities.json?start_date='+today+'&visit_motive_ids=2585896&agenda_ids=438394-428258-438387-438373&insurance_sector=public&practice_ids=165271&destroy_temporary=true&limit=3', headers = header)
    total =reqPfizer.json().get('total')+reqModerna.json().get('total')
    
    # je choisi de recevoir une notification seulemnt si il y a des doses de disponibles
    if total > 0:
        toaster.show_toast(f"doses disponibles au centre de vaccination de Compiègne: {total}","Cliquer pour ouvrir la page du centre", icon_path = None, threaded = True, callback_on_click = open_url)
    
    # on met un sleep (ici de 100 sec) pour éviter de surcharger le site de nos demandes requests
    sleep(100)
    