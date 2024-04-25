from pylab import *
from numpy import *
from random import *


def image_to_tableau (original):
    A=original.copy()

    nbL,nbC,profo=shape(A) #pour connaitre le nombre de lignes, de colonnes et la profondeur

    B=zeros((nbL,nbC))

    for i in range (nbL):
        for j in range (nbC):
            if 0.69 <=A[i,j,0] <= 0.73 and 0.69 <=A[i,j,1] <= 0.73 and 0.69 <=A[i,j,2] <= 0.73 : # couleur grise (0) sur le schéma
                B[i,j] = 0

            elif A[i,j,0] >= 0.97 and A[i,j,1] >= 0.97 and A[i,j,2] >= 0.7 : # couleur jaune très clair (1-2) sur le schéma
                B[i,j] = 2

            elif A[i,j,0] >= 0.97 and A[i,j,1] >= 0.97 and A[i,j,2] >= 0.5 and A[i,j,2] <= 0.7 : # couleur jaune clair (3-10) sur le schéma
                B[i,j] = 7

            elif A[i,j,0] >= 0.97 and A[i,j,1] >= 0.97 and A[i,j,2] <= 0.4 : # couleur jaune (11-25) sur le schéma
                B[i,j] = 15

            elif A[i,j,0] >= 0.97 and A[i,j,1] <= 0.8 : # couleur orange (26-50) sur le schéma
                B[i,j] = 40

            elif A[i,j,0] >= 0.9 and A[i,j,0] <= 0.95 and A[i,j,1] >= 0.4 and A[i,j,1] <= 0.5: # couleur orange foncée (51-100) sur le schéma
                B[i,j] = 75

            elif A[i,j,0] >= 0.9 and A[i,j,0] <= 0.95 and A[i,j,1] <= 0.3 : # couleur rouge (101-250) sur le schéma
                B[i,j] = 175

            elif A[i,j,0] >= 0.53 and A[i,j,0] <= 0.62 : # couleur rouge foncée (251-536) sur le schéma
                B[i,j] = 400

            else :
                if j>0 :
                    B[i,j]=B[i,j-1]

                else : 
                    B[i,j]=B[i-1,j]

    return B 

def tableau_to_image (B,original) :
    nbL,nbC,profo=shape(original)
    res = zeros(shape(original))

    for i in range (nbL):
        for j in range (nbC):
            if B[i,j]==0:
                res [i,j]= [0.71,0.71,0.71,1]
            
            if B[i,j]==2:
                res [i,j]= [0.99,0.99,0.8,1]

            if B[i,j]==7:
                res [i,j]= [0.99,0.99,0.62,1]

            if B[i,j]==15:
                res [i,j]= [1,0.98,0.3,1]

            if B[i,j]==40:
                res [i,j]= [1,0.75,0.3,1]

            if B[i,j]==75:
                res [i,j]= [0.94,0.48,0.3,1]

            if B[i,j]==175:
                res [i,j]= [0.93,0.24,0.25,1]

            if B[i,j]==400:
                res [i,j]= [0.59,0.25,0.25,1]    

    imshow(res)
    show()    
    return res

# Changer le chemin (notamment pour une carte de densité différente)
original=imread("Code\Density_map\Kano_density.png")
table = image_to_tableau(original)

savetxt('Kano_density_table.txt', table)