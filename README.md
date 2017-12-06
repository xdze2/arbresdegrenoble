# Les Arbres De Grenoble
La cartographie des arbres de grenoble


Les données des arbres de la ville sont en accès libre sur le site [Opendata du territoire grenoblois](http://data.metropolegrenoble.fr/ckan/dataset/les-arbres-de-grenoble).


# Road map

1. une jolie carte avec les arbres marqués
2. puis une pop-up avec les infos sur l'arbre (nom commun, date de plantation... etc)

3. puis la localisation GPS pour trouver l'arbre le plus proche
4. ... etc

# Questions

* Trop de points pour les petits zoom (<15), c'est frustrant...
    - Heat map, point clustering... :/
    - Regroupement des arbres par zone parente (code_parent)
    - Comment dessiner ces zones ?  convex hull :/ (sur une allée en arc)
    - alpha-hull/concave hull :
        - [Sur la création des enveloppes concaves et les divers moyens d'y parvenir](http://www.portailsig.org/content/sur-la-creation-des-enveloppes-concaves-concave-hull-et-les-divers-moyens-d-y-parvenir-forme)
        - https://scicomp.stackexchange.com/a/3303/15117

# Data flow

* Exploration des données (notebook) : élimination manuelle des champs non utiles
* Création d'une base de données sqlite3
*  ...
* Création d'un nouveau GeoJson à partir de la DB
* Export vers Mapbox Studio ? ou vers le script js... 

# Liens utiles

### Map
- [**OSM: Grenoble, France/Trees Import**](https://wiki.openstreetmap.org/wiki/Grenoble,_France/Trees_Import)
- [**Jolies cartes - Stamen Design**](http://maps.stamen.com/#toner/16/45.1868/5.7261)
- [**[github] stamen/toner-carto**](https://github.com/stamen/toner-carto)
- [**Mapbox**](https://www.mapbox.com)
- [**umap**](https://umap.openstreetmap.fr/en/)


### Botanique

- [**Tela Botanica**](http://www.tela-botanica.org/page:accueil_botanique)

- [**lesarbres.fr - Noms latin**](http://www.lesarbres.fr/noms-des-arbres-latin-.html)

### Données

- [**Arbre d'alignement (Lyon ?)**](https://www.data.gouv.fr/fr/datasets/arbre-dalignement/) 
