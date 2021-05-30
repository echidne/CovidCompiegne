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
1. ### Les librairies standards: 
   On va avoir besoin de :  
   * `datetime` pour récupérer la date du jour
   * `time` pour interroger le site à intervalel régulier et éviter de le surcharger
   * `webbrowser`pour ouvrir la page du site via la notification
   * `subprocess` pour lancer l'execution de la commande shell d'installation des librairies manquantes
   * `sys`pour arreter l'appli
   * `platform` pour savoir si on est bien sous le bon système d'exploitation

2. ### Les modules non-standards:
   Pour ce projet on va utiliser des modules non standards. Vous avez peut-être déjà installé le premier pour un projet web car c'est une librairie trés répandue mais probablement pas les autres. Si vous ne les avez pas déjà installé le code prend soin de les installer. Bien sûr libre à vous de les installer par vous même si la méthode in code ne vous convient pas ou ne fonctionne pas. Je vous laisse jetter un oeil aux liens fournis pour les processus d'installation particuliers.
   
   * La librairie `requests`:
 [requests](https://fr.python-requests.org/en/latest/) permet de réaliser des requêtes HTTP. Elle a été créée pour rendre "plus humaine " l'utilisation de la librairie standrad `urllib`
   * La librairie `pyttstx3`:
   [pyttstx3](https://pyttsx3.readthedocs.io/en/latest/) permet de faire parler mon appli
   
   * La librairie `win10toast_click` :
  Cette [librairie](https://pypi.org/project/win10toast-click/) permet de créer des toast, c'est à dire des notfications à durée limitée sous windows 10. Il existe plusieurs versions mais celle ci permet aussi de lancer une page web associée. Comme elle n'est surement pas installée à la première utilisation de l'appli on l'installe aprés avoir vérifier qu'on est bien sous windows 10 :
  ```python
  try :
    from win10toast_click import ToastNotifier
except ModuleNotFoundError :
    if platform.platform().startswith('Windows-10'):
        subprocess.run([sys.executable, "-m", "pip", "install", "win10toast-click"])
    else :
        print('il faut être sous windows 10')
        sys.exit()
   ``` 

* ## Les variables globales

1. ### l'adresse de la page du centre de notification  
   On associe à la variable `page_url` l'adresse de la page web correspondante au centre de vaccination qui vous interesse
   ``` python
   page_url ="https://www.doctolib.fr/vaccination-covid-19/ville/nom_du_centre_de_vaccination?"
   ```
2. ### La création de l'_user_agent_   
   Afin d'éviter que vos `request`vous renvoie un code _403_, il faut ajouter un paramêtre `headers`à vos requete. Ici on utilise un dictionnaire pour se faire passer pour Chrome 😏.
   ``` python
   header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}
   ```  
 3. ### L'intervalle de temps   
     Afin d'éviter de surcharger le site Doctolib, on va introduire un intervalle de temps entre chaque requêtes. Ici j'ai mis 300 secondes (5 minutes). Libre à vous de moduler    cet intervalle mais attention de ne pas interroger trop souvent le site.
     ``` python
    intervalle = 300
    ```
   
* ## Les fonctions.  
1. la fonction `open_url()`  
   On va se servir de la librairie `webbrowser` fournit en standard avec python. Cette librairie va utiliser votre browser déni par défaut dans votre système pour ouvrir la page web de votre centre. À noter, sur mon ordinateur webbrowser ne lève pas d'exception si la page web n'existe pas ou s'il y a un problème pour l'ouvrir. J'ai du passer par `requests` pour tester la page.  
   
   ``` python
   def open_url():
    try: 
        requests.get(page_url)
        webbrowser.open_new(page_url)
    except requests.ConnectionError : 
        print('Failed to open URL. Unsupported variable type.')
   ```  
 2. la fonction `notif_sonore`  
   Cette fonction permet d'utiliser le synthetizeur de votre ordinateur via la librairie pyttsx3. Votre ordinateur prononcera le texte passé en paramètre.  
 
 3. la fonction `notif_toast`  
   Cette fonction permet d'afficher d'afficher un _toast_ ou bulle de notification en français. Pour ce faire je me suis servi de la librairie `win10toast_click` bien quelle ne fonctionne que sous windows 10. En effet c'est la seule librairie que j'ai trouvée qui me permet d'ajouter une action si on clique sur la notification. Il ya plusieurs librairies de notification multiplateformes mais aucune ne permet d'ajouter une action à la notification simplement. Si vous trouvez un moyen de le faire **pull request le moi**.  
   
   Notification de départ:  
   ![notif1](https://github.com/echidne/CovidCompiegne/blob/main/Images/notif%201.png)  
   
   Notification quand des doses ont été trouvées :  
   ![notif2](https://github.com/echidne/CovidCompiegne/blob/main/Images/notif%202.png)  
   
   Si par hasard le notifications n'apparaissaient pas, veuillez vérifier que les notifications sont activées dans les paramètres windows ("Notifications et actions") ou que "l'assistant de concentration" ne les bloque pas  
   
 4. la fonction `requete_doctolib`  
   C'est la fonction qui va vous permettre de faire des requetes sur Doctolib. Mais pour trouver les paramètres à lui fournir il va falloir mettre les mains un peu dans le cambouis :grin: . En effet je n'ai pas trouver moyen de récupérer les information directemetn sur le site via le code (si vous trouvez un moyen de le faire **pull request le moi**).  
   Avant de commencer il faut récupérer l'adresse de l'api et ses paramêtres :  
   
   Tout d'abord il faut se rendre sur le site du centre de vaccination. Ici le centre de Compiègne :  
   >
   <img src="https://github.com/echidne/CovidCompiegne/blob/main/Images/page%20centre%20compi%C3%A8gne.png?" width=50% height=50%>  
    
   Ensuite inspecter le code (clicker droit sur la page puis choix "Inspecter" ou combinaisons de ctrl+maj+i)
    
   <img src="https://github.com/echidne/CovidCompiegne/blob/main/Images/page_2_menu_click_droit.png" width=50% height=50%>  
    
   Cela va ouvrir la console. Une fois la console ouverte clicquer sur "Network" puis sur "XHR":
    
   <img src="https://github.com/echidne/CovidCompiegne/blob/main/Images/choix_network_XHr.png" width=50% height=50%>  
   
   Puis choisissez un motif de consultation. Celà va entrainer l'interrogation de l'api via le fichier `availabilities.json`.
    
   <img src= "https://github.com/echidne/CovidCompiegne/blob/main/Images/voir_lefichier_json.png" width=50% height=50%>  
    
   Exemple d'un lien d'interrogation (pour une première injection Pfizer au centre de Compiègne):  
   https://www.doctolib.fr/availabilities.json?start_date=2021-05-22&visit_motive_ids=2553369&agenda_ids=470011-434292-434257-412372-435494-448029-432422-412370&insurance_sector=public&practice_ids=165271&destroy_temporary=true&limit=4   
   
   L'interogation est donc structurée comme suit :  
   > start_date={date-du-jour}&visit_motive_ids={id qui indique le type d'injection}&agenda_ids={ids qui varient selon le lieu de vaccination et le type de vaccin}&insurance_sector={public or private}&practice_ids={id du centre}&destroy_temporary=true&limit=4   
   
   Alors comment va-t-on utiliser ça? Pour ma part je suis allé au plus simple :  
   * La date du jour au format ISO je sais la récupérer dans le script (`date.today().isoformat()`).  
   * L'id qui indique le type d'injection ne varie pas (pour un centre donné- si on change de centre il est possible que l'id change) . Par exemple à Compiègne, l'id pour une première injection Pfizer est _2553369_.  
   * Les agendas_ids varient selon le centre de vaccination, le type de vaccination et le vaccinateur.  
   * Le practice_ids est l'id qui caractérise le centre de vaccination.
   
   Ne sachant pas comment les récupérer on the fly, j'ai décidé de rentrer les 3 derniers en dur dans le code.
   
   Maintenant que donne l'interrogation de l'api? Et bien ça renvoie des données de type `.json` qui contient les informations qu'on recherche, et comme `requests`est une librairie bien faite elle fournit une fonction qui permet de décoder le retour de la requête en un sympatique dictionnaire. 
   
   Par exemple :  
   ```
   req = requests.get('https://www.doctolib.fr/availabilities.json?start_date={date-du-jour}&visit_motive_ids={id qui indique le type d'injection}&agenda_ids={ids qui varient selon le lieu de vaccination et le type de vaccin}&insurance_sector={public or private}&practice_ids={id du centre}&destroy_temporary=true&limit=4', headers = header)
   
   print(req.json())
   ```   
   peut donner :
   
   exemple 1 :  
   ```
   {"availabilities":[],"total":0,"reason":"no_availabilities","message":"Aucune disponibilité en ligne.","number_future_vaccinations":39499}
   ```  
   
   Bon là pas de chance, pas de doses disponibles ("total":0) et donc pas de disponibilité pour réserver ("availabilities":[])  
   
   exemple 2:   
   ```
   {"total":0,"availabilities":[{"date":"2021-05-22","slots":[]},{"date":"2021-05-23","slots":[]},{"date":"2021-05-24","slots":[]},{"date":"2021-05-25","slots":[]}],"next_slot":"2021-07-02"}
   ```  
   
   Toujours pas de chance, pas de doses disponibles ("total":0), la liste associée à "availabilities" n'est pas vide mais les "slots" sont bien vides. Par contre on indique une prochaine disponibilité le 02 juillet ("next_slot":"2021-07-02"), et si on utilise cette date comme paramètre pour `start_date` alors normalement on aura des doses de dsiponibles
    
   exemple 3:  
   ```
   {"availabilities":[{"date":"2021-05-22","slots":[],"substitution":null},{"date":"2021-05-23","slots":[],"substitution":null},{"date":"2021-05-24","slots":[],"substitution":null},{"date":"2021-05-25","slots":[{"agenda_id":252502,"practitioner_agenda_id":null,"start_date":"2021-05-25T12:25:00.000+02:00","end_date":"2021-05-25T12:35:00.000+02:00","steps":....,"substitution":null}],"total":3}
   ```
   
  Là il y a des doses dispo (mais bon j'ai triché c'est chez un medecin de Lyon qui vaccine avec l'Atrazenca :) ). Il y a donc 3 doses de disponibles ("total":3) et les dates où on peut se vaire vacciner avec les créneaux horaires sont indiquées.   
   
   Donc le plus simple pour savoir si des doses sont disponibles c'est d'interroger l'api via le lien cité plus haut avec `request` de récupérer la réponse par un `get` dans une varriable et de récupérer la valeur associée à 'total' :
   
   `doses_du_vaccin_disponibles = req.json().get('total')`
   
   Si la requête s'est bien passée alors vous aller récupérer une valeur numérique pour le nombre de doses. Et si ça ce n'est pas bien passé, me diriez vous? J'ai choisi la solution de facilité qui est de tester si le résultat de la requête est _None_. Mais sachez qu'il existe une exception JSONDecodeError fourni dans la librairie json (je vous laisse le soin de voir si vous voulez l'implémenter)
   
   5. la fonction `on_press_loop`  
      Cette fonction permet de détecter l'appui sur une touche du clavier via la librairie `pyinput` et son module `keyboard`. Tel que je l'ai paramétré l'appuie sur la touche "F12" provoque la sortie du context manager et arrête l'application (voir ci-dessous)  
      
* ## La partie principale
   C'est ici qu'on va lancer la machine 😏. 
   Dans ma première version du code j'avais inclus les requêtes dans une boucle infinie `while` et utlisé un `time.sleep` pour les espacer. Mais je n'aime pas à avoir à aller dans le gestionnaire de tache pour arreter mes applis. J'ai donc cherché une méthode pour interrompre à partir d'une commande du clavier.  
   Il existe l'exception `KeyboardInterrupt` inclue dans python qui permet de capturer l'emploi de `<ctrl>+<c>` mais du coup si j'employais cette combinaison , assez courante, pour autre chose celà risquait d'interrompre mon appli sans que je le souhaite.  
   J'ai donc préféré utilisé une libraire externe (pyinput) qui permet d'écouter l'emploi de la souris ou du clavier et ceci même si on est en dehors de la fenêtre de l'application. Pour ce faire on utilise un context manager. L'état du 'listener' est capturé par `listener.running`. Quand on appuie sur la touche F12 alors sont état passe à `False` et celà entraine le `break`qui va interrompre la boucle.  
   Pour la périodicité des requêtes j'ai utilisé l'écart entre deux instants capturés par `time.time()`.  
   
 # Conclusion
   Et voilà la partie code est terminée. 
   A vous de le modifier pour qu'il fonctionne pour votre centre de vaccination préférée.  
   Vous avez peut-être remarqué que mon code a pour extension `.pyw` et pas `.py`. Cela permet de ne pas avoir de fenêtre vide s'ouvrir quand on lance l'appli en double cliquant sous Windows10. C'est l'équivalent de la command `pythonw file.py`  
   
 # Dévelopement/Améliorations possibles 
   Mon code n'est pas parfait.  
   Par exemple il est nécessaire d'aller chercher à la main les informations nécessaires pour interroger l'application de Doctolib.  
   De même les notifications visuelles ne fonctionnent en l'état que sur Windows10  
   Ce code ne fonctionne aussi que pour la plateforme Doctolib. il faudrait surement pas mal le modifier pour qu'il fonctionne pour Maya ou  Keldoc.  
   N'hesitez pas à me pull request pour l'améliorer  
   
 # Auteur
   
   [Philippe Giammarinaro](https://www.linkedin.com/in/pgiammarinaro/)
   
 
