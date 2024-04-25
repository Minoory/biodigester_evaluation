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
