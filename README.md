# Mesure du taux d'occupation de parkings à l'aide de caméras vidéos
## Résumé
Pour les utilisateurs de parkings, il est souvent souhaité connaître le nombre de places libres disponibles, tout du moins s'il en reste. Aussi, être capable d'obtenir des statistiques d'utilisations des parkings peut être important pour leur gérant: par exemple, savoir distinguer les heures creuses des heures pleines permet d'optimiser les plages horaires des employés. C'est une problématique importante, qui a souvent été résolue par l'utilisation de divers capteurs. 

Ce travail propose une solution se reposant sur un système de capture vidéo. Des images provenant d'une caméra, il est possible d'en retirer le taux d'occupation du parking à l'aide de diverses méthodes d'analyse d'images ou d'apprentissage automatique. Ce projet permet d'exposer avant tout des méthodes de _deep learning_, tel que la détection d'objets. 

Afin de concrétiser les solutions explorées dans ce projet, une caméra a été  installée sur le toit du site de Cheseaux la HEIG-VD. Celle-ci permet de capturer des images d'un des parkings qui y sont présents. L'évaluation des différentes caméras adéquates et l'installation de celle qui semble le plus adaptée est documentée dans ce travail. 

Ce projet propose d'étudier plusieurs solutions qui peuvent répondre à la problématique de la mesure du taux d'occupation d'un parking. L'une de celle-ci se repose sur une suppression de l'arrière-plan d'une image. Cependant, il est souhaité que ce travail aborde avant tout le problème à l'aide de technologies d'apprentissages automatiques, et non pas de traitement d'images. Néanmoins, la solution pré-citée est brièvement explorée.

Des modèles de réseaux de neurones sont aussi présentés. Certains de ceux-ci sont définies à la main. D'autres utilisent ce qui a été pensé dans le domaine de la recherche de la détection d'objets, dans le but de pouvoir distinguer, dans une image, les voitures qui y sont présentes. Notamment, les modèles _Faster-RCNN_ et _Yolo_ sont présentés et testés.

Une petite API _REST_ est aussi présentée dans ce projet qui permet de fournir l'état actuel d'un parking à un utilisateur.

## Rapport
Le rapport effectué dans le cadre de ce travail est disponible à la racine du projet, sous le nom de _TB2018\_Report\_Parking_.

## Structure de fichier
- **report** : Rapport latex du projet
- **dev** : Développement
    - **tensorflow\_models** : API de détection d'objets de _Tensorflow_
    - **park\_python** : Le développement effectué
        - **camera** : Connexion à la caméra et récupération automatique d'images
        - **dataset\_helper** : Méthodes d'aides au traitement de _dataset_, comme pouvoir séparer celui-ci en 3 sous dossiers _test_, _dev_ et _train_
        - **final\_models** : Modèles finaux utilisés
        - **logger** : Système de log développé
        - **ml\_helper** : Fonctions d'aide à l'entrainement et à l'utilisation des modèles. Contient notamment des _predictor_ permettant de calculer le nombre de voitures présentes en fonction d'une image
        - **drafts** : Création et entrainement des modèles, traitements d'images
            - **cam\_image\_processing** :   Test de traitements d'images
            - **edge\_detection** : Détection de bords
            - **image\_regression** : Création et entrainement du modèle approchant le problème sous forme de régression
            - **object\_detection** : Modèles de détection d'objets
                - **darknet** : Modèle de détection de voiture basé sur _Yolo_
                - **grid\_keras** : Modèle de détection des voitures à l'aide d'une grille et _Keras_
                - **tensorflow\_api\_cars** : Modèle de détection d'objets utilisant l'API **tensorflow** sur le corpus _Cars_
                - **tensorflow\_api\_pklot** : Modèle de détection d'objets utilisant l'API **tensorflow** sur le corpus _PKLot_
        - **rest\_app.py** : Application permettant d'exposer une API _REST_ fournissant à un utilisateur l'état actuel du parking.

## Technologies utilisées
_Tensorflow, Tensorflow Object Detection API, Keras, Darknet, Yolo, Faster RCNN, Python, OpenCV, Scikit-image, REST API, Flask_

## Datasets
***Cars*** : https://ai.stanford.edu/~jkrause/cars/car_dataset.html

***PKLot*** : https://web.inf.ufpr.br/vri/databases/parking-lot-database/

## API REST
### Prérequis
Python doit être installé sur la machine. Les librairies suivantes sont nécessaires, pouvant être installé à l'aide d'un _pip install_ :
- flask
- tensorflow
- skimage
- numpy
- panda
- apscheduler
- requests

### Exécution
Afin de lancer l'API REST permettant de fournir à l'utilisateur l'état actuel du parking, il suffit d'accéder au dossier _/dev/park\_python_ et d'exécuter la commande suivante:

```
sudo python rest_app.py
```