# CovidCompiegne
Appli in python to receive notification when doses for first injection of vaccin are available in Compiègne.  
As the code is done : work only when doses for first injection are available in "Centre de vaccination de Compiègne (60200) France"  
All commentaries in code and history below are in French for 2 main reasons :
1. I'm sharing the code with French python students
2. This code will work only in France


# Histoire
Comme quasiment tout le monde en France j'ai été confronté au problème de trouver des doses disponibles pour me faire vacciner contre le Covid.  
J'ai cherché comment réaliser une application qui m'avertisse quand des doses de vaccins sont dispoibles dans le centre de vaccination prés de chez moi et je suis tombé su [cette vidéo](https://www.youtube.com/watch?v=BoGy1j8AREo) qui explique comme réaliser une appli qui interroge le site [vitemadose](https://vitemadose.covidtracker.fr/) et qui envoie des notif direct sur un appareil android. Le problème est que le site _vitemadose_ est trés sollicité et qu'il y a des délais de plus de 30 minutes entre la mise à jour de _Doctolib_ ou les autres plateformes pour prendre rendez vous et la mise à jour de _vitemadose_.  
J'ai donc cherché à interroger directement le centre de vaccination à côté de chez moi. Vous pourrez transposer la méthode à tous les centres de vaccinations qui focntionne avec Doctolib.  

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
