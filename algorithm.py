import numpy as np
import random
from tqdm import tqdm
import matplotlib.pyplot as plt
import networkx as nx

from data_library import *
from map_library import *



# ============================== Importation de la carte ====================================

density_table = np.loadtxt("Kano_density_table.txt")
length, width = density_table.shape
scale = 5000/length # chaque pixel dans Python est un carré de coté de taille scale (en mètre)


# =============================== Initialisation des fermes ================================

farms_coord = np.array([[120,0],[550,0],[670,0],[759,600],[0,250],[200,683]])       # Positionnement des entrées des fermes sur la carte
farms_capacity = np.array([124,29,144,154,96,163])                                  # Nombre de tracteurs que peut envoyer chaque ferme
farms_capacity = (farms_capacity/3).astype('int')

# =================================== Paramétrage ===========================================

Rmax= 1000                                  # Rayon de portée maximale (en mètres) d'un biodigesteur
b_capacity = 784                            # Nombre de personne pouvant accéder au même biodigesteur
Nbt = 3                                     # Nombre de tracteurs pouvant remplir un même biodigesteur
Nf = 6                                      # Nombre de fermes
Nb = int(sum(farms_capacity)/Nbt)           # Nombre de biodigesteurs à placer


# ================================== Pénalités =============================================

def intersections_penalty(b : biodigester):
    return b.intersections

def length_penalty(b : biodigester):
    return b.d

def R_penalty(b : biodigester):
    return b.R

def penalty(b : biodigester):
    return 5*intersections_penalty(b)**4 + length_penalty(b)**2 + 3*R_penalty(b)**3

def global_penalty(B):
    res = 0
    for b in B:
        res += penalty(b)
    return res



# ===================================== Algorithme ===========================================

def new_population(Nb : int):
    coords = initialize_coord(Nb,length,width)
    R_list = compute_R_list(density_table,coords,Rmax,b_capacity,scale)
    intersections = compute_intersections(coords,R_list,scale)
    B = []
    for i in range(Nb):
        B.append(biodigester(Nbt,coords[i][0], coords[i][1],intersections[i],R_list[i]))
    return B, coords, R_list, intersections

def place_farms(coords, capacity):
    F = []
    for i in range(Nf):
        F.append(farm(capacity[i],coords[i][0],coords[i][1]))
    return F

def run(B : np.ndarray, F: np.ndarray):
    
    #Initialisation des trajets possibles
    
    E = PriorityQueue()

    for i,f in enumerate(F):
        for j,b in enumerate(B):
            e = edge(i,j,distance(f.x,f.y,b.x,b.y))
            f.addEdge(e.id)
            b.addEdge(e.id)
            E.push(e)
    
    
    # Calcul des trajets

    Nft_tot = sum([f.Nft for f in F])
    Nbt_tot = Nbt*Nb
    
    #Collecte pour potentiel affichage graphique

    Efinal = []

    while Nft_tot != 0 and Nbt_tot != 0 and not E.isEmpty() :
        e = E.pop()
        
        #Tant qu'on peut encore remplir le même  biodigesteur avec la même ferme, on continue :
        while B[e.b_id].Nbt !=0 :
            
            # S'il n'y a plus de tracteurs pour la ferme, on supprime toutes les arêtes de E le comportant
            if F[e.f_id].Nft == 0:
                for e_id in F[e.f_id].Vf:
                    E.remove(e_id)
                break
        
            # Sinon
        
            Efinal.append(e)
            
            # On retient la distance entre le biodigesteur et sa ferme
            B[e.b_id].d += e.d
            
            # On retire e des arêtes liées au site et on décrémente le nombre de tracteurs disponibles (localement et globalement)
            B[e.b_id].Nbt -= 1
            F[e.f_id].Nft -= 1
            
            Nft_tot -= 1
            Nbt_tot -= 1
        
        #Si la boucle s'est terminée et que le biodigesteur est plein :
        if B[e.b_id].Nbt == 0:
            for e_id in B[e.b_id].Vb:
                E.remove(e_id)   
        
    return Efinal

def update_position(b : biodigester, global_best_x : int, global_best_y : int, inertia=0.5, cognitive=1, social=0.2, curiosity = 0.5):
    # Mise à jour de la position en fonction du meilleur résultat local et global
    b.dx = int(inertia * b.dx  +  random.random() * cognitive * (b.best_x - b.x)  +  random.random() * social * (global_best_x - b.x)
               + curiosity * random.uniform(-20,20))
    b.dy = int(inertia * b.dy  +  random.random() * cognitive * (b.best_y - b.y)  +  random.random() * social * (global_best_y - b.y)
               + curiosity * random.uniform(-20,20))
    b.x += b.dx
    if b.x > length : b.x = length-1
    if b.x < 0 : b.x = 0
    b.y += b.dy
    if b.y > width : b.y = width-1
    if b.y < 0 : b.y = 0
    return b.x, b.y

def evaluate(b:biodigester):
    p = penalty(b)
    if p < b.best_score:
        b.best_score = p
        b.best_x = b.x
        b.best_y = b.y
    return p

def algorithme_essaim(Nb: int, iterations : int, lost_era, alone_era, social_era):
    B, biodigester_coords, R_list, intersections = new_population(Nb)
    F = place_farms(farms_coord,farms_capacity)
    global_best_score = float('inf')
    global_best_x = 0
    global_best_y = 0

    P = []
    E = []
    
    for it in tqdm(range(iterations)):
        for b in B:
            b.d = 0
            b.Nbt = Nbt
        
        for i,f in enumerate(F):
            f.Nft = farms_capacity[i]

        E = run(B,F)
        
        for b in B:
            evaluate(b)

        P.append(global_penalty(B))
        
        # Trouver le meilleur score global et sa position
        for b in B:
            if b.best_score < global_best_score:
                global_best_score = b.best_score
                global_best_x = b.best_x
                global_best_y = b.best_y
        
        # Mettre à jour les positions des bâtiments et leurs attributs
        
        if it < lost_era:       # Temps de découverte
            for i,b in enumerate(B):
                biodigester_coords[i] = update_position(b, global_best_x, global_best_y, 0.8, 0.2, 0, 2)

        elif it < alone_era:    # Temps de recherche d'un minimum local
            for i,b in enumerate(B):
                biodigester_coords[i] = update_position(b, global_best_x, global_best_y, 0.5, 0.7, 0, 1)

        elif it < social_era:   # Temps de convergence vers le plus petit minimum local
            for i,b in enumerate(B):
                biodigester_coords[i] = update_position(b, global_best_x, global_best_y, 0.1, 0.3, 0.8, 0.5)

        else:
            for i,b in enumerate(B):    # Temps de repositionnement vers le minimum exploré
                biodigester_coords[i] = update_position(b, global_best_x, global_best_y, 0.2, 1, 0, 0.5)
        
        R_list = compute_R_list(density_table, biodigester_coords,Rmax,b_capacity,scale)
        intersections = compute_intersections(biodigester_coords,R_list,scale)
        
        for i,b in enumerate(B):
            b.R = R_list[i]
            b.intersections = intersections[i]
    
    for b in B:
        evaluate(b)

    P.append(global_penalty(B))
    
    return B, E, F, P


def graph_essaim(Nb: int, iterations : int, lost_era, alone_era, social_era):
    B, E, F, P = algorithme_essaim(Nb,iterations,lost_era,alone_era,social_era)
    G = nx.DiGraph()
    pos = {}
    colors = {}
    size = {}

    for i, f in enumerate(F):
        id = f"f{i}"
        #G.add_node(id, use=f'{f.Nft}')
        colors[id] = '#8DECB4'
        pos[id] = (f.y, -f.x)
        size[id] = 400

    for i, b in enumerate(B):
        id = f"b{i}"
        G.add_node(id)
        colors[id] = 'white'
        pos[id] = (b.y,-b.x)
        size[id] = 50
    
    for e in E:
        G.add_edge(f"f{e.f_id}",f"b{e.b_id}")
    
    plt.figure(figsize=(7,8))
    nx.draw(G,pos,node_color=[colors[node] for node in G.nodes()],node_size=[size[node] for node in G.nodes()], arrowsize=10)
    #use = nx.get_node_attributes(G, 'use')
    #nx.draw_networkx_labels(G, pos, labels=use)
    img = plt.imread("Density_map/Kano_density.png")  # Remplacez "background_image.png" par le chemin de votre image
    plt.imshow(img, extent=[0,width,-length,0])  # Ajustez les limites et l'opacité selon vos besoins

    logP = np.log10(np.array(P))
    x = np.array(range(iterations + 1))

    plt.figure(figsize=(8,4))
    plt.plot(x,logP,label='Pénalité')
    plt.title("Penalité globale au cours des itérations")
    plt.xlabel("Itérations")
    plt.ylabel("Pénalité globale (échelle log)")
    plt.axvspan(0, lost_era, facecolor='purple', alpha=0.2, label='Ere perdue')
    plt.axvspan(lost_era, alone_era, facecolor='red', alpha=0.2, label='Ere solitaire')
    plt.axvspan(alone_era, social_era, facecolor='yellow', alpha=0.2, label='Ere sociale')
    plt.axvspan(social_era, iterations, facecolor='green', alpha=0.2, label="Ere d'or")
    plt.grid()
    plt.legend()
    plt.show()

    return B, E, F, P


def multi_algorithme_essaim(Nb: int, splits: int, iterations : int, lost_era, alone_era, social_era):
    B, biodigester_coords, R_list, intersections = new_population(Nb)
    F = place_farms(farms_coord,farms_capacity)
    P_tot = []

    frac = Nb//splits

    for s in range(splits):

        if s != 0:  #On ne modifie qu'une partie de la population à chaque split

            new_B, new_biodigester_coords, new_R_list, new_intersections = new_population(Nb-frac*s)
            B = B + new_B

            for i in range(frac*s,Nb):
                biodigester_coords[i] = new_biodigester_coords[i - frac*s]
                R_list[i] = new_R_list[i - frac*s]
                intersections = compute_intersections(biodigester_coords,R_list,scale)
        
        global_best_score = float('inf')
        global_best_x = 0
        global_best_y = 0

        P = []
        E = []
        
        for it in tqdm(range(iterations)):
            for b in B:
                b.d = 0
                b.Nbt = Nbt
            
            for i,f in enumerate(F):
                f.Nft = farms_capacity[i]

            E = run(B,F)
            
            for b in B:
                evaluate(b)

            P.append(global_penalty(B))
            
            # Trouver le meilleur score global et sa position
            for b in B[frac*s:]:
                if b.best_score < global_best_score:
                    global_best_score = b.best_score
                    global_best_x = b.best_x
                    global_best_y = b.best_y
            
            # Mettre à jour les positions des bâtiments et leurs attributs
            
            if it < lost_era:       # Temps de découverte
                for i,b in enumerate(B[frac*s:]):
                    biodigester_coords[i + frac*s] = update_position(b, global_best_x, global_best_y, 0.8, 0.2, 0, 2)

            elif it < alone_era:    # Temps de recherche d'un minimum local
                for i,b in enumerate(B[frac*s:]):
                    biodigester_coords[i + frac*s] = update_position(b, global_best_x, global_best_y, 0.5, 0.7, 0, 1)

            elif it < social_era:   # Temps de convergence vers le plus petit minimum local
                for i,b in enumerate(B[frac*s:]):
                    biodigester_coords[i + frac*s] = update_position(b, global_best_x, global_best_y, 0.1, 0.3, 0.8, 0.5)

            else:
                for i,b in enumerate(B[frac*s:]):    # Temps de repositionnement vers le minimum exploré
                    biodigester_coords[i + frac*s] = update_position(b, global_best_x, global_best_y, 0.2, 1, 0, 0.5)
            
            new_R_list = compute_R_list(density_table, biodigester_coords[frac * s:],Rmax,b_capacity,scale)

            for i in range(frac*s,Nb):
                R_list[i] = new_R_list[i-frac*s]

            intersections = compute_intersections(biodigester_coords,R_list,scale)
            
            for i,b in enumerate(B):
                b.R = R_list[i]
                b.intersections = intersections[i]
    

        P.append(global_penalty(B))
    
        P_tot.append(P)

        #Sélection des meilleurs biodigesteurs
        if s != splits-1 :
            p_table = np.zeros(Nb)

            for i, b in enumerate(B):
                p_table[i] = evaluate(b)

            i_sort = np.argsort(p_table)
            new_B = []

            for i in range(frac*(s+1)):
                new_B.append(B[i_sort[i]])
            
            B = new_B
            
            intersections = intersections[i_sort]
            R_list = R_list[i_sort]
            biodigester_coords = biodigester_coords[i_sort]

    
    return B, E, F, P_tot, R_list

def plot_graph(B,E,F):
    G = nx.DiGraph()
    pos = {}
    colors = {}
    size = {}

    for i, f in enumerate(F):
        id = f"f{i}"
        #G.add_node(id, use=f'{f.Nft}')
        colors[id] = '#8DECB4'
        pos[id] = (f.y, -f.x)
        size[id] = 400

    for i, b in enumerate(B):
        id = f"b{i}"
        G.add_node(id)
        colors[id] = 'white'
        pos[id] = (b.y,-b.x)
        size[id] = 50
    
    for e in E:
        G.add_edge(f"f{e.f_id}",f"b{e.b_id}")
    
    plt.figure(figsize=(7,8))
    nx.draw(G,pos,node_color=[colors[node] for node in G.nodes()],node_size=[size[node] for node in G.nodes()], arrowsize=10)
    #use = nx.get_node_attributes(G, 'use')
    #nx.draw_networkx_labels(G, pos, labels=use)
    img = plt.imread("Density_map/Kano_density.png")  # Remplacez "background_image.png" par le chemin de votre image
    plt.imshow(img, extent=[0,width,-length,0])  # Ajustez les limites et l'opacité selon vos besoins


def plot_penalty(P,lost_era,alone_era,social_era,iterations):
    logP = np.log10(np.array(P))
    x = np.array(range(iterations + 1))
    
    plt.figure(figsize=(8,4))
    plt.plot(x,logP,label='Pénalité')
    plt.title("Penalité globale au cours des itérations")
    plt.xlabel("Itérations")
    plt.ylabel("Pénalité globale (échelle log)")
    plt.axvspan(0, lost_era, facecolor='purple', alpha=0.2, label='Ere perdue')
    plt.axvspan(lost_era, alone_era, facecolor='red', alpha=0.2, label='Ere solitaire')
    plt.axvspan(alone_era, social_era, facecolor='yellow', alpha=0.2, label='Ere sociale')
    plt.axvspan(social_era, iterations, facecolor='green', alpha=0.2, label="Ere d'or")
    plt.grid()
    plt.legend()
    plt.show()