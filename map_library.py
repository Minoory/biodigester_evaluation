import numpy as np
import random as rd


def initialize_coord (Nb:int, length:int, width:int):
    """Retourne un tableau numpy de shape (Nb, 2) de coordonnées aléatoires pour les positions initiales des biodigesteurs"""
    
    res = np.zeros((Nb,2))
    for i in range (Nb) : 
        indL = rd.randint(0,length-1)
        indW = rd.randint(0,width-1)

        res[i][0] = indL
        res[i][1] = indW


    return res ; 



def compute_reach(density_table:np.ndarray,b:np.ndarray,R:float,scale:float): 
    """Calcule le nombre de personne sur un disque de rayon R et de centre c avec une densité B par pixel (à scale pres)
    R : rayon en m"""
    
    length, width = density_table.shape
    
    r_pix = R/scale     #taille du rayon en pixel
    r_pix = int(round(r_pix)) # on arrondi à l'entier près


    res = 0 
    
    bL=int(b[0]) # ligne du centre 
    bW=int(b[1]) # colonne du centre
    for x in range(bL-r_pix,bL+r_pix+1):
        for y in range (bW-r_pix,bW+r_pix+1):

            if (x-bL)**2 + (y-bW)**2 <= r_pix**2 and x >= 0 and x <length and y >= 0 and y < width: # si (x,y) est dans le disque

                res = res + 1/(13*13)*density_table[x,y]
 

    return res


def compute_R (density_table:np.ndarray,b:np.ndarray,Rmax:float, capacity:float, scale:float, eps = 10):
    """Calcul du rayon maximal
    Rmax : Rayon maximal en mètre
    capacity : Capacité maximale du biodigesteur
    eps : distance d'incertitude en mètres"""

    # On procède par dichotomie
    
    bottom = 0
    top = Rmax # Rmax est en mètre
    mid= (top+bottom)/2
    
    while (top-bottom > eps):

        capacity_mid = compute_reach(density_table,b,mid,scale)
        
        if (capacity_mid > capacity):
            top=mid

        else : 
            bottom= mid
        
        mid= (bottom+top)/2
 
    return mid



def compute_R_list (density_table:np.ndarray,biodigester_coords:np.ndarray,Rmax:float,capacity:float,scale:float):
    """Calcul des rayons maximaux pour chaque biodigesteur de biodigester_coords"""
    
    rep = np.zeros(len(biodigester_coords))

    for i,b in enumerate(biodigester_coords):
        rep[i] = compute_R(density_table,b,Rmax,capacity,scale)

    return rep


def distance(x1,y1,x2,y2):
    return np.sqrt((x1-x2)**2 + (y1-y2)**2)


def compute_intersections (biodigester_coords:np.ndarray, R_list : np.ndarray, scale : float):
    n = len(biodigester_coords)
    rep = np.zeros(n)
    for i in range(n):
        for j in range(i+1,n):
            d = (R_list[i] + R_list[j])/scale - distance(biodigester_coords[i][0],biodigester_coords[i][1],biodigester_coords[j][0],biodigester_coords[j][1])
            if d > 0 :
                rep[i] += d
                rep[j] += d
    return rep