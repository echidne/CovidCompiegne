# CovidCompiegne
Appli in python to receive notification when doses for first injection of vaccin are available in Compiègne.  
As the code is done : work only when doses for first injection are available in "Centre de vaccination de Compiègne (60200) France"  
All commentaries in code and history below are in French for 2 main reasons :
1. I'm sharing the code with French python students
2. This code will work only in France


# Histoire
Comme quasiment tout le monde en France j'ai été confronté au problème de trouver des doses disponibles pour me faire vacciner contre le Covid.  
J'ai cherché comment réaliser une application qui m'avertisse quand des doses de vaccins sont dispoibles dans le centre de vaccination prés de chez moi et je suis tombé su [cette vidéo](https://www.youtube.com/watch?v=BoGy1j8AREo) qui explique comme réaliser une appli qui interroge le site [vitemadose](https://vitemadose.covidtracker.fr/) et qui envoie des notif direct sur un appareil android. Le problème est que le site _vitemadose_ est trés sollicité et qu'il y a des délais de plus de 30 minutes entre la mise à jour de _Doctolib_ ou les autres plateformes pour prendre rendez vous et la mise à jour de _vitemadose_.  
J'ai donc cherché à interroger directement le centre de vaccination à côté de chez moi. Vous pourrez transposer la méthode à tous les centres de vaccinations qui fonctionnent avec Doctolib.  

# Principe / Fonctionnement 
L'appli va interroger la disponibilité des doses via l'api de Doctolib qui nous fournit gentiment un fichier .json bien pratique :).  
Puis si des doses sont disponibles une notification est envoyée pour m'avertir.  
N.B. : J'ai choisi une notification sous forme de 'toaster' mais qui ne va fonctionner que sous Windows. N'hesitez pas à me faire des pull si vous connaissez une méthode qui fonctionnerait sous Linux et/ou Mac Os.

# Description du code 
* ## les modules nécessaires
1. ### Les modules Builtins : 
   On va avoir besoin de :  
   * `requests` pour interroger le site du centre de vaccination
   * `datetime` pour récupérer la date du jour
   * `time` pour créer des pauses entre chaque interrogation pour éviter de surcharger le site
   * `webbrowser`pour ouvrir la page du site via la notification
   * `subprocess` et `sys` pour lancer l'execution de la commande shell d'installation du module `win10toast_click` à la première exécution de l'appli
   * `platform` pour savoir si on est bien sous le bon système d'exploitation
``` python
import requests
from time import sleep
from datetime import date
import webbrowser
import subprocess
import sys
import platform
```

2. ### Le module `win10toast_click` :
  Ce [module](https://pypi.org/project/win10toast-click/) permet de créer des toast, c'est à dire des notfications à durée limitée sous windows 10. Il existe plusieurs versions mais celle ci permet aussi de lancer une page web associée. Comme elle n'est surement pas installée à la première utilisation de l'appli on l'installe aprés avoir vérifier qu'on est bien sous windows 10 :
  ``` python
  try :
    from win10toast_click import ToastNotifier
except ModuleNotFoundError :
    if platform.platform().startswith('Windows-10'):
        subprocess.run([sys.executable, "-m", "pip", "install", "win10toast-click"])
    else :
        print('il faut être sous windows 10')
        sys.exit() 
   ```
* ## Les variables
1. ### création de l'instance toaster  
   On va créer une instance du toaster afin de pouvoir ouvrir une notification quand celà sera nécesaire:  
   ``` python
   toaster = ToastNotifier()
   ```
2. ### l'adresse de la page du centre de notification  
   On associe à la variable `page_url` l'adresse de la page web correspondante au centre de vaccination qui vous interesse
   ``` python
   page_url ="https://www.doctolib.fr/vaccination-covid-19/ville/nom_du_centre_de_vaccination?"
   ```
3. ### La création de l'_user_agent_   
   Afin d'éviter que vos `request`vous renvoie un code _403_, il faut ajouter un paramêtre `headers`à vos requete. Ici on utilise un dictionnaire pour se faire passer pour Chrome :).
   ``` python
   header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}
   ```
   
* ## La fonction qui va permettre d'ouvrir la page de votre centre de vaccination à partir de la notification  
   Cette fonction sera appelée quand vous cliquerez sur la notification.
   
   ``` python
   def open_url():
    try: 
        requests.get(page_url)
        webbrowser.open_new(page_url)
    except requests.ConnectionError : 
        print('Failed to open URL. Unsupported variable type.')
   ```
  
  * ## La boucle qui va permettre d'interroger le site du centre de vaccination
   Avant de commencer il faut récupérer l'adresse du fichier `.json` qui contient le sinformations qu'on cherche.
   Tout d'abord il faut se rendre sur le site du centre de vaccination. Ici le centre de Compiègne :  
   
   <img src="https://github.com/echidne/CovidCompiegne/blob/main/Images/page%20centre%20compi%C3%A8gne.png?" width=50% height=50%>  
   
   Ensuite inspecter le code (clicker droit sur la page puis choix "Inspecter" ou combinaisons de ctrl+maj+i)
   
   <img src="https://github.com/echidne/CovidCompiegne/blob/main/Images/page_2_menu_click_droit.png" width=50% height=50%>  
   
   Cela va ouvrir la console. Une fois la console ouverte clicquer sur "Network" puis sur "XHR":
   
   <img src="https://github.com/echidne/CovidCompiegne/blob/main/Images/choix_network_XHr.png" width=50% height=50%> 
   

 
