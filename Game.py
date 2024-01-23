from Cellule import Cellule #importation de la classe des cellules
from random import randint #importation de la fonction randint
import copy as cp #importation de la fonction de copie profonde (cp)

class Game():
    """
    Classe représentant le jeu.
    params:
        -nb_cellules:int, nombre de cellules dans la société.
        -percentage_of_contamination:int, le pourcentage de cellules contaminés au démarrage de la simulation.
        -agressivity_of_virus:int, le pourcentage d'aggréssivité (et donc de propagation) du virus.
        -percentage_of_immune:int, le pourcentage de cellules immunisées contre le virus dans la société.
    """

    def __init__(self, nb_cellules, percentage_of_contamination, agressivity_of_virus, percentage_of_immune):
        assert nb_cellules % 2 == 0,  "Le nombre de cellules doit être pair." #sinon l'affichage ne pourra pas être effectué correctement.
        assert 0 < nb_cellules <= 400, "Le nombre de cellules ne peut pas dépasser 400 et être inférieur ou égal à 0." #sinon l'affichage ne pourra pas être effectué correctement.
        assert 0 <= percentage_of_contamination <= 100, "Le taux de contamination doit être compris entre 0 et 100."
        assert 0 <= percentage_of_immune <= 100, "Le taux d'immunisées doit être compris entre 0 et 100."
        assert percentage_of_contamination + percentage_of_immune <= 100, "La somme du taux de contaminées et du taux d'immunisées ne peut être supérieur 100." #ensemble de la société = 100%.
        assert 0 < agressivity_of_virus <= 100, "Le taux d'aggrésivité du virus doit être supérieur à 0 et ne pas dépasser 100." #il s'agit d'un pourcentage.

        self.agressivity_of_virus = agressivity_of_virus

        #on détermine le diviseur juste après le milieu de tous les diviseurs pairs du nombre de cellules, cela nous servira pour créer la société et pour faciliter l'affichage.
        # 24 = (12,2) (8,3) (6,4) (4,6) (2,12) --> 2 --> (6,4)
        self.diviseur = []
        for i in range(nb_cellules//2, 0, -1):
            if nb_cellules % i == 0 and i % 2 == 0:
                self.diviseur.append((i,nb_cellules/i))

        self.diviseur = self.diviseur[round(len(self.diviseur)/2)][0]
        
        #Création de la société.
        #26 / 2 --> True --> [[xxxxxxxxxxxxx], [xxxxxxxxxxxxx]]
        self.society = []
        for i in range(self.diviseur):
            self.society.append([])
        for i in self.society:
            for j in range(int(nb_cellules/self.diviseur)):
                i.append(Cellule())
        
        #introduction du virus dans la société.
        while self.getTauxDeContamines() < percentage_of_contamination:

            for i in self.society:
                for j in i:
                    if self.getTauxDeContamines() < percentage_of_contamination:
                        contamination = randint(1,100)
                        if 0 < contamination <= percentage_of_contamination:
                            j.is_contaminated = True
                    else:
                        break

        #introduction des immunisées dans la société.
        while self.getTauxDeImmunes() < percentage_of_immune:

            for i in self.society:
                for j in i:
                    if self.getTauxDeImmunes() < percentage_of_immune:
                        immune = randint(0,100)
                        if 0 < immune <= percentage_of_immune and not j.is_contaminated:
                            j.is_immune = True

    def getTauxDeContamines(self):
        """
        Fonction qui détermine le taux de contaminées dans la société afin de respecter celui demandé par l'utilisateur.
        """
        taille_society = 0
        taux_de_contamines = 0

        for i in self.society:
            taille_society += len(i)
            for j in i:
                if j.is_contaminated:
                    taux_de_contamines += 1
            
        taux_de_contamines = round((taux_de_contamines/taille_society)*100)
        return taux_de_contamines
    
    def getTauxDeImmunes(self):
        """
        Fonction qui détermine le taux d'immunisées dans la société afin de respecter celui demander par l'utilisateur.
        """

        taille_society = 0
        taux_de_immune = 0

        for i in self.society:
            taille_society += len(i)
            for j in i:
                if j.is_immune:
                    taux_de_immune += 1
            
        taux_de_immune = round((taux_de_immune/taille_society)*100)
        return taux_de_immune


    def update(self):
            """
            Fonction qui simule le passage d'une période de x temps dans la société.
            """

            save_society = cp.deepcopy(self.society) #création d'une copie profonde afin de ne pas impacter la société d'origine.

            for i in self.society: #on regarde les voisins de chaque cellule pour voir s'ils sont contaminés.
                index = 0
                for j in i:

                    if j.is_immune == False and j.is_alive == True:
                        neighbors = []

                        try:
                            neighbors.append(save_society[self.society.index(i)][index-1]) #voisin de gauche
                        except IndexError:
                            neighbors.append(Cellule())
                        try:
                            neighbors.append(save_society[self.society.index(i)][index+1]) #voisin de droite
                        except IndexError:
                            neighbors.append(Cellule())
                        try:
                            neighbors.append(save_society[self.society.index(i)-1][index]) #voisin du dessus
                        except IndexError:
                            neighbors.append(Cellule())
                        try:
                            neighbors.append(save_society[self.society.index(i)+1][index]) #voisin du dessous
                        except IndexError:
                            neighbors.append(Cellule())
                        
                        for neighbor in neighbors: #balayage de tous les voisins
                            agressivity = randint(0,100)
                            if neighbor.is_contaminated and 0 < agressivity <= self.agressivity_of_virus: #si l'un d'eux est contaminé, alors il est possible que la cellule cible aussi.
                                j.is_contaminated = True
                    
                    #Est ce que la cellule peut se soigner ?
                    heal = randint(1,100)
                    if 0 < heal <= 100-self.agressivity_of_virus and j.is_alive:
                        j.is_contaminated = False
                        j.time = 0
                    
                    #Est-ce que la cellule est morte ?
                    if j.is_alive == True and j.is_contaminated == True:
                        j.time += 1
                        if j.time == int((100-self.agressivity_of_virus)/2): #90 = 100-90 = 10/2 = 5 ; 100 - 50 == 50/2 = 25
                            j.is_alive = False
                    
                    index += 1
    
    def __str__(self):
        """
        Affichage ordonnée de la société.
        """
        
        affichage = ""

        #26 = 2*13 = [[xxxxxxxxxxxxx], [xxxxxxxxxxxxx]]
        for i in self.society:
            index = 0
            for j in i:
                if index == len(i)-1:
                    if j.is_alive == False:
                        affichage += " \033[0;31mx\n"
                    else:
                        if j.is_contaminated == True:
                            affichage += " \033[0;32mc\n"
                        elif j.is_immune == True:
                            affichage += " \033[0;33mi\n"
                        else:
                            affichage += " \033[0;36ma\n"
                else:
                    if j.is_alive == False:
                        affichage += " \033[0;31mx"
                    else:
                        if j.is_contaminated == True:
                            affichage += " \033[0;32mc"
                        elif j.is_immune == True:
                            affichage += " \033[0;33mi"
                        else:
                            affichage += " \033[0;36ma" 

                index += 1

        return affichage