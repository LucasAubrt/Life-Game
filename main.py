from Game import Game #importation de la classe de la simulation

#questions données à l'utilisateur pour déterminer les paramètres de la simulation
nombre_de_cellules = int(input("Combien de cellules vont êtres dans la société : "))
taux_de_contamines = int(input("Quel sera le taux de contaminés par le virus au départ : "))
agressivity_of_virus = int(input("Quel est le taux d'agressivité du virus : "))
taux_de_immunises = int(input("Quel sera le taux d'immunisés contre le virus :"))

#initialisation de la simulation
game = Game(nombre_de_cellules, taux_de_contamines, agressivity_of_virus, taux_de_immunises)

print(game) #affichage de la société au stade 1

#lancement de la boucle infinie de la simulation
while True:
    input("\033[0;37m--> Appuyez sur entrée pour continuer")
    game.update()
    print(game)