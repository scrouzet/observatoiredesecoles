
L'[observatoire](www.observatoiredesecoles.fr) vise à réaliser un état des lieux des écoles Toulousaines sur de nombreux aspects : vétusté des locaux, moyens humains, sécurisation des abords, etc. Dans ce but, [un questionnaire a été développé](https://forms.gle/2mypKSG3nptqWE6A8) afin de faire remonter les informations locales par les parents d'élèves et personnels.

La composante technique consiste, à partir des données collectées via le formulaire, à afficher une carte des écoles Toulousaines permettant d'obtenir une "photographie" générale, mais aussi locale, des conditions actuelles dans les écoles.

[<img alt="interactive map" width="800px" align="middle" src="images/Screenshot from 2022-11-25 11-03-27.png" />](https://scrouzet.github.io/observatoiredesecoles/carte.html)

# Outils utilisés et description technique générale

Le point de départ de la solution technique utilisée est un formulaire Google Form. Nous avons décidé d'utiliser Google ici du fait de la praticité de cet outil en particulier et surtout de l'export des données. Le formulaire alimente un Google Sheet à accès restreint (données protégées). Un autre Google Sheet a été mis en accès public et importe la partie des données ne contenant aucune information personnelle (grâce à un =IMPORTRANGE()). C'est ce dernier tableau qui sera lu par le code Python.

Côté données publiques, j'ai uniquement utilisé 2 fichiers contenant les coordonnées des écoles [maternelles](https://data.toulouse-metropole.fr/explore/dataset/ecoles-maternelles-publiques/information/) et [élémentaires](https://data.toulouse-metropole.fr/explore/dataset/ecoles-elementaires-publiques/information/) sur le site https://data.toulouse-metropole.fr.

Du côté code/analyse/visualisation, tout a été réalisé en Python dans [un repo Github](https://github.com/scrouzet/observatoiredesecoles). Plus précisément j'ai utilisé les packages [Geopandas](https://geopandas.org) et [Folium](https://python-visualization.github.io/folium/) pour traiter les données et générer à partir de celles-ci une carte HTML utilisant [OpenStreetMap](https://www.openstreetmap.org) pour les tuiles. N'étant ni développeur web, ni cartographe, j'ai eu besoin de pas mal de recherche là dessus. Au final, la solution choisie associée à un déploiement via Github est je pense un bon compromis simplicité/efficacité pour ce projet.

Dans le détail, ce qui se passe :
- Un script python `get_location_data.py` lit les 2 fichiers `.geojson` contenant les coordonnées des écoles Toulousaines. Le résultat est enregistré et sauvé dans `base_data.json`.
- Un script python `main.py` récupère les données du formulaire Google anonymisé, les aggrège, et les combine avec les données de localisation de chaque école. On obtient ainsi un `geodataframe` prêt à être affiché dans une carte.
- Pour transformer ces données en carte, j'ai utilisé la fantastique méthode `.explore()` de [Geopandas](https://geopandas.org) qui, à partir d'un `geodataframe`, permets de générer assez facilement des couches (=layers) pour une carte en se basant sur le package [Folium](https://python-visualization.github.io/folium/). Des fonctions plus spécifiques à [Folium](https://python-visualization.github.io/folium/) pouvaient ensuite être utilisées pour fignoler cette carte et la sauver en HTML.
- Voilà ! Il ne restait plus qu'à créer une Github Action `.github/workflows/main.yaml` permettant d'exécuter automatiquement `main.py` tous les jours à 11h30 directement depuis le repo Github. Je n'avais jamais utilisé cette fonctionnalité et c'est vraiment top.



# Idées en vrac de choses à ajouter à cette carte


## Indice de position sociale

- Indices de position sociale géolocalisés des écoles et collèges de France métropolitaine et des DROM IPSG https://fr.wikipedia.org/wiki/Indice_de_position_sociale
- Fichier ./data/ips-all-geoloc.csv
- DL https://www.data.gouv.fr/fr/datasets/indices-de-position-sociale-geolocalises-des-ecoles-et-colleges-de-france-metropolitaine-et-des-drom-2/
- Le tweet qui annonce le partage https://twitter.com/alphoenix/status/1580250208474378241?s=20&t=52NZ7cag2rEPkNrQxLIOww
- Pour croiser avec les REP: https://data.education.gouv.fr/explore/dataset/fr-en-ecoles-ep/table/

## Pollution


## ICU
