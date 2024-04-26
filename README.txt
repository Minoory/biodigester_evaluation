# biodigester_evaluation
Algorithme d'optimisation pour évaluer la mise en place de biodigesteurs dans une région.

################################## Utilisation #####################################
Tous les résultats sont présents dans main.ipynb

Attention, de nombreuses librairies sont utilisées, le programme n'a pas nécessairement besoin d'être exécuté.

################################### Eléments #######################################

Density_map/Kano_density.png : Carte de densité de population (Kano dans le cas d'étude)
Density_map/map_creation.py : Transformation de la carte de densité en un tableau numpy, enregistrable localement

Kano_density_table.txt : Tableau numpy importable rapportant la carte de densité de population
algorithm.py : Algorithme d'optimisation
data_library.py : Structures de données nécessaires pour l'algorithme
main.ipynb : Jupyter Notebook pour éxécuter les différents codes
map_library.py : Fonctions pour intéragir avec la carte de densité


############################### Documents modifiables #############################
Density_map/map_creation.py
> Modifier la fin du code pour importer la carte de densité souhaitée

algorithm.py
> Modifier la carte de référence
> Modifier les fermes
> Paramétrer les biodigesteurs
> Modifier les pénalités
> Modifier l'inertie les influences cognitives, sociales et curieuses dans l'algorithme pour les différentes ères

main.ipynb
> Tout est modifiable, un programme est déjà indiqué pour afficher les résultats de l'algorithme
> Il suffit de relancer les différentes cellules pour générer une nouvelle population

############################# Fonctions importantes ################################
algorithme_essaim(Nb: int, iterations : int, lost_era, alone_era, social_era)
> Applique l'algorithme d'optimisation pour un nombre iterations d'itérations sur une population de Nb biodigesteur positionnés initialement aléatoirement
> Les itérations correspondantes aux changements d'ère sont à indiquer pour chaque paramètre idoine
> Retourne les biodigesteurs, les trajets empruntés par les tracteurs, les fermes et l'évolution de la pénalité dans le temps

graph_essaim(Nb: int, iterations : int, lost_era, alone_era, social_era)
> Réalise l'algorithme d'essaim et affiche le graphe correspondant
> Retourne les mêmes paramètres que algorithme_essaim

multi_algorithme_essaim(Nb: int, splits: int, iterations : int, lost_era, alone_era, social_era)
> Réalise l'algorithme d'essaim avec un nombre splits de sélection
> Retourne les mêmes paramètres que algorithme_essaim, et la liste des rayons de couverture des biodigesteurs
