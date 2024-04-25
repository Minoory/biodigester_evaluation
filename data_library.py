import numpy as np

class edge:
    id = 0
    
    def __init__(self, f_id:int, b_id:int, d:float):
        self.id = edge.id
        edge.id +=1
        self.f_id = f_id
        self.b_id = b_id
        self.d = d

class PriorityQueue:
    def __init__(self):
        self.queue = []  # Tas
        self.e_to_index = {}    # Conserve la position des arêtes (identifiées par leurs id) dans le tas
    
    def isEmpty(self):
        return len(self.queue) == 0
    
    def swap(self, i:int, j:int):
        # Echange deux éléments du tas et modifie correctement les indices
        self.queue[i], self.queue[j] = self.queue[j], self.queue[i]
        self.e_to_index[self.queue[i].id] = i
        self.e_to_index[self.queue[j].id] = j
    
    def push(self, e:edge):
        # Ajouter un élément dans la liste
        self.queue.append(e)
        index = len(self.queue) - 1
        self.e_to_index[e.id] = index
        self.up(index)
    
    def pop(self):
        # Retirer le dernier élément de la liste
        if self.isEmpty() : return
        
        self.swap(0,len(self.queue)-1)
        e = self.queue.pop()
        del self.e_to_index[e.id]
        self.down(0)
        
        return e
    
    def remove(self, e_id:int):
        # Retirer un élément quelconque de la liste
        if e_id not in self.e_to_index:
            return  # L'élément n'existe pas dans la file de priorité
        
        # Récupération de l'élément
        index = self.e_to_index[e_id]
        
        # Echange entre le dernier élément et celui voulu
        last_e = self.queue[-1]
        self.queue[index] = last_e
        self.e_to_index[last_e.id] = index
        
        # Suppression de l'élément
        self.queue.pop()
        del self.e_to_index[e_id]
        
        if index < len(self.queue):  # Si l'élément supprimé n'était pas le dernier
            self.up(index)
            self.down(index)
    
    def up(self, index:int):
        # Fait remonter l'élément à sa juste position, utile pour l'insertion
        while index > 0:
            parent_index = (index - 1) // 2
            if self.queue[index].d < self.queue[parent_index].d:
                self.swap(index, parent_index)
                index = parent_index
            else:
                break
        
           
    def down(self, index:int):
        # Fait descendre l'élément à sa juste position, utile pour la suppression
        while True:
            left_child_index = 2 * index + 1
            right_child_index = 2 * index + 2
            
            largest = index
            
            if (left_child_index < len(self.queue) and
                self.queue[left_child_index].d < self.queue[largest].d):
                largest = left_child_index
            
            if (right_child_index < len(self.queue) and
                self.queue[right_child_index].d < self.queue[largest].d):
                largest = right_child_index
            
            if largest != index:
                self.swap(index, largest)
                index = largest
            else:
                break
        

class farm:
    
    def __init__(self, Nft:int, x:int, y:int):
        if Nft <= 0: raise "Nft <= 0" 
        #Nombre de trajets possibles partant de la ferme
        self.Nft = Nft

        #Position de la ferme (pixels)
        self.x = x      
        self.y = y

        #Arêtes (trajets) où la ferme est un des sommets (à modifier avec addEdge)
        self.Vf = []
        
    def addEdge(self, e_id:int): #Pour créer la sctructure initiale
        self.Vf.append(e_id)

        
        
        
class biodigester:
    
    def __init__(self, Nbt:int, x : int, y : int , intersections : int, R : float):
        if Nbt < 0: raise "Nbt < 0" 
        #Nombre de trajets possibles arrivant au biodigesteur
        self.Nbt = Nbt

        #Distance du trajet final choisi (à modifier après calcul)
        self.d = 0

        #Distance totale d'intersection avec les autres biodigesteurs 
        self.intersections = intersections

        #Arêtes (trajets) où le biodigesteur est un des sommets (à modifier avec addEdge)
        self.Vb = []

        #Rayon de couverture (en mètres)
        self.R = R

        #Position du biodigesteur (pixels)
        self.x = x
        self.y = y

        #Meilleure position du biodigesteur (pixels)
        self.best_x = x
        self.best_y = y
        self.best_score = float("inf")

        #Création de vitesses initiales aléatoires
        self.dx = 0
        self.dy = 0
    
    def addEdge(self, e_id:int): #Pour créer la sctructure initiale
        self.Vb.append(e_id)
