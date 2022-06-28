  # ----------------------------Import------------------------------------
import doctest
import fltk    
from random import choice

 # ------------------------------Variables-------------------------------

lst_direction = ["Haut", "Bas", "Gauche", "Droite"] 
LARGEUR_FENETRE = 1000
LONGUEUR_FENETRE = 1000
Liste_map = ["save.txt", "square1.txt", "square2.txt", "square3.txt",
             "one_sheep.txt", "wide1.txt","wide2.txt"]

  # --------------Fonctions pour determiner la victoire---------------------
  
  
def determine_pos_herbes(Plateau):
    """
    Fonction qui renvoie les coordonnées des emplacements des herbes

    Parameters
    ----------
    Plateau : list

    Returns list
    -------
    >>> determine_pos_herbes([["g", 0, "b"], [0, 0, 0]])
    [(0, 0)]

    """
    retour = []
    for l in range(len(Plateau)):
        for elem in range(len(Plateau[l])):
            if Plateau[l][elem] == "g":
                retour.append((l, elem))
    return retour
 

def fin_jeu(Plateau, Positions_moutons):
    """
    Fonction qui determine si oui on non le jeu est fini

    Parameters
    ----------
    Plateau : list
    Positions_moutons : list

    Returns bool
    -------
    >>> fin_jeu([["g", 0, 0, 0], [0, 0, 0, 0]], [(0, 0)])
    True
    
    >>> fin_jeu([["g", 0]], [1, 0])
    False
    """
      # Cas ou on peut pas gagner
    if len(Positions_moutons) < len(determine_pos_herbes(Plateau)):
        return False
    
    for position in determine_pos_herbes(Plateau):
        if position not in Positions_moutons:
            return False
    return True    


  # ----------------------------Fonction de tri -----------------------------
  
def tri_haut(Plateau, Positions_moutons):
    """
    Fonction qui tri les moutons pour qu'il se deplace bien dans le bon ordre
    si ils vont vers le haut

    Parameters
    ----------
    Plateau : list
    Position_moutons : list

    Returns list
    -------
    >>> tri_haut([[0,0],[0,0]], [(1,0),(0,0)])
    [(0, 0), (1, 0)]
    """
    lst_trié = []
    for y in range(len(Plateau)):
        for elem in Positions_moutons:
            if elem[0] == y:
                lst_trié.append(elem)
    return lst_trié


def tri_bas(Plateau, Positions_moutons):
    """
    Fonction qui tri les moutons pour qu'il se deplace correctement si ils
    vont vers le bas

    Parameters
    ----------
    Plateau : list
    Positions_moutons : list
    Returns list
    -------
    >>> tri_bas([[0,0],[0,0]], [(1,0),(0,0)])
    [(1, 0), (0, 0)]

    """
    
    lst_trié = []
    for y in range(len(Plateau) + 1):
        for elem in Positions_moutons:
            if elem[0] == len(Plateau)-y:
                lst_trié.append(elem)
    return lst_trié            



def tri_gauche(Plateau, Positions_moutons):
    """
    Fonction qui tri l'ordre des moutons pour qu'ils se déplacent correctement
    si ils vont vers la gauche

    Parameters
    ----------
    Plateau : list
    Positions_moutons : list
    Returns list
    -------
    >>> tri_gauche([[0,0],[0,0]], [(0,1),(0,0)])
    [(0, 0), (0, 1)]
    """
  
    lst_trié = []
    for x in range(len(Plateau[0])):
        for elem in Positions_moutons:
            if elem[1] == x:
                lst_trié.append(elem)
    return lst_trié            

def tri_droite(Plateau, Positions_moutons):
    """
    Fonction qui tri l'ordre des moutons pour qu'ils se deplacent correctement
    si ils vont vers la droite

    Parameters
    ----------
    Plateau : list
    Positions_moutons : list

    Returns list
    -------
    >>> tri_droite([[0,0], [0,0]], [(0,0), (0,1)])
    [(0, 1), (0, 0)]

    """
    lst_trié = []
    for x in range(len(Plateau[0]) + 1):
        for elem in Positions_moutons:
            if elem[1] == len(Plateau[0]) - x:
                lst_trié.append(elem)
    return lst_trié             


  # ----------Fonction pour savoir si un mouvement est possible--------------
  
def est_possible_haut(Plateau, mouton, Positions_moutons):
    """
    Fonction qui determine si un mouton peut se deplacer vers le haut ou non

    Parameters
    ----------
    Plateau : list
    mouton : tupple
    Positions_moutons : list

    Returns bool
    -------
    >>> est_possible_haut([[0,0], [0,0]], (0,0), [(0,0)])
    False
    >>> est_possible_haut([["b",0], [0,0]], (1,0), [(1,0)])
    False
    >>> est_possible_haut([[0,0], [0,0]], (1,0), [(0,0), (1,0)])
    False
    >>> est_possible_haut([[0,0], [0,0]], (1,0), [(1,0)])
    True

    """
    
    ymouton, xmouton = mouton
    
      # Cas ou le mouton peut pas avancer vers le haut
    if ymouton == 0:
        return False   
        
      # cas ou le mouton est bloqué par un buisson
    if Plateau[ymouton - 1][xmouton] == "b":
        return False
             
    if (ymouton - 1, xmouton) in Positions_moutons:
       return False       
    
      # Cas ou il peut monter
    return True  
    

def est_possible_bas(Plateau, mouton, Positions_moutons):
    """
    Fonction qui determine si un mouton peut se deplacer ou non vers le bas

    Parameters
    ----------
    Plateau : list
    mouton : tupple
    Positions_moutons : list
    Returns bool
    -------
    >>> est_possible_bas([[0,0], [0,0]], (1,0), [(1,0)])
    False
    >>> est_possible_bas([[0,0], [0,0]], (0,0), [(0,0)])
    True
    """
    
    
    ymouton, xmouton = mouton
    
    if ymouton == len(Plateau) - 1:
        return False   
        
      # cas ou le mouton est bloqué par un buisson
    if Plateau[ymouton + 1][xmouton] == "b":
        return False
        
        
    if (ymouton + 1, xmouton) in Positions_moutons:
       return False
       
    
      # Cas ou il peut descendre
    return True  

def est_possible_gauche(Plateau, mouton, Positions_moutons):
    """
    Fonction qui determine si un mouton peut se deplacer vers la gauche

    Parameters
    ----------
    Plateau : list
    mouton : tupple
    Positions_moutons : list

    Returns bool
    -------
    >>> est_possible_gauche([["b",0], [0,0]], (0,1), [(0,1)])
    False
    >>> est_possible_gauche([[0,0], [0,0]], (0,1), [(0,1)])
    True
    """
    ymouton, xmouton = mouton
    
    if xmouton == 0:
        return False
    
    if Plateau[ymouton][xmouton - 1] == "b":
        return False
    
    if (ymouton, xmouton - 1) in Positions_moutons:
        return False
    return True

def est_possible_droite(Plateau, mouton, Positions_moutons):
    """
    Fonction qui determine si un mouton peut aller vers la droite

    Parameters
    ----------
    Plateau : list
    mouton : tupple
    Positions_moutons : list

    Returns bool
    -------
    >>> est_possible_droite([[0,0], [0,0]], (0,0), [(0,0)])
    True
    >>> est_possible_droite([[0,0], [0,0]], (0,0), [(0,0), (0,1)])
    False

    """
    ymouton, xmouton = mouton
    
    if xmouton == len(Plateau[0]) - 1:
        return False
    
    if Plateau[ymouton][xmouton + 1] == "b":
        return False
    
    if (ymouton, xmouton + 1) in Positions_moutons:
        return False
    return True

 

  # ----------------Fonction de deplacement des moutons-----------------------

def deplace_mouton_haut(Plateau, Positions_moutons):
    """
    Fonction qui fait deplacer les moutons vers le haut de une case

    Parameters
    ----------
    Plateau : list
    Positions_moutons : list

    Returns list
    -------
    >>> deplace_mouton_haut([[0,0], [0,0]], [(1,0),(1,1)])
    [(0, 0), (0, 1)]
    """
    Positions_moutons = tri_haut(Plateau, Positions_moutons)
    nvl_list = []
    
    for mouton in Positions_moutons:
        ymouton, xmouton = mouton
        
        if est_possible_haut(Plateau, mouton, nvl_list):
            nvl_list.append((ymouton - 1, xmouton))
            
        else:
            nvl_list.append(mouton)
    return nvl_list
    
def deplace_mouton_bas(Plateau, Positions_moutons):
    """
    Fonction qui fait se deplacer d'une case les moutons vers le bas

    Parameters
    ----------
    Plateau : list
    Positions_moutons : list

    Returns list
    -------
    >>> deplace_mouton_bas([[0,0], [0,0]], [(0,0), (0,1)])
    [(1, 0), (1, 1)]
    """
    
    Positions_moutons = tri_bas(Plateau, Positions_moutons)
    nvl_list = []
   
    for mouton in Positions_moutons:
        ymouton, xmouton = mouton
        if est_possible_bas(Plateau, mouton, nvl_list):
            nvl_list.append((ymouton + 1, xmouton))
        else:
            nvl_list.append(mouton)
            
    return nvl_list


def deplace_mouton_gauche(Plateau, Positions_moutons):
    """
    Fonction qui deplace de une case vers la gauche les moutons

    Parameters
    ----------
    Plateau : list
    Positions_moutons : list

    Returns list
    -------
    >>> deplace_mouton_gauche([[0,0], [0,0]], [(0,0), (1,1)])
    [(0, 0), (1, 0)]
    """
    Positions_moutons = tri_gauche(Plateau, Positions_moutons)
    nvl_list = []
    
    for mouton in Positions_moutons:
        ymouton, xmouton = mouton
        if est_possible_gauche(Plateau, mouton, Positions_moutons):
            nvl_list.append((ymouton, xmouton - 1))
        else:
            nvl_list.append(mouton)
    return nvl_list

def deplace_mouton_droite(Plateau, Positions_moutons):
    """
    Fonction qui fait se deplacer de une case vers la droite les moutons

    Parameters
    ----------
    Plateau : list
    Positions_moutons : list

    Returns list
    -------
    >>> deplace_mouton_droite([[0,0], [0,0]], [(0,0), (1,1)])
    [(1, 1), (0, 1)]
    """
    Positions_moutons = tri_droite(Plateau, Positions_moutons)
    nvl_list = []
    
    for mouton in Positions_moutons:
        ymouton, xmouton = mouton
        if est_possible_droite(Plateau, mouton, Positions_moutons):
            nvl_list.append((ymouton, xmouton + 1))
        else:
            nvl_list.append(mouton)
    return nvl_list        



def deplacement(Plateau, Positions_moutons, Direction):
    """
    Fonction qui permet aux moutons de se deplacer

    Parameters
    ----------
    Plateau : list
    Positions_moutons : list
    Direction : str

    Returns list
    -------
    >>> deplacement([[0,0,0], [0,0,0], [0,0,0]], [(0,0)], "Bas")
    [(2, 0)]

    """
    if Direction == "Haut":
        for i in range(len(Plateau)):
            Positions_moutons = deplace_mouton_haut(Plateau, Positions_moutons)
        return Positions_moutons    
    if Direction == "Bas":
        for i in range(len(Plateau)):
            Positions_moutons = deplace_mouton_bas(Plateau, Positions_moutons)
        return Positions_moutons    
    if Direction == "Gauche":
        for i in range(len(Plateau[0])):
            Positions_moutons = deplace_mouton_gauche(Plateau, Positions_moutons) 
        return Positions_moutons
    
    if Direction == "Droite":
        for i in range(len(Plateau[0])):
            Positions_moutons = deplace_mouton_droite(Plateau, Positions_moutons)
        return Positions_moutons



  #--------------------fonction pour Charger d'un fichier--------------------
def creer_plateau(grille):
    """
     Fonction qui prend une chaine de caractère et le converti en deux listes,
    une qui sera le plateau de jeu et l'autre qui sera la positions des moutons    
    

    Parameters
    ----------
    grille : str

    Returns (list , list)
    -------
    >>> creer_plateau("SGB_")
    ([[0], ['g'], ['b'], [0]], [(0, 0)])
    

    """
   
    Plateau = []
    Positions_moutons = []
    
    for elem in range(len(grille)):
        ligne = []
        for caract in range(len(grille[elem])):
            if grille[elem][caract] == "_":
                ligne.append(0)
            elif grille[elem][caract] == "G":
                ligne.append("g")
            elif grille[elem][caract] == "B":
                ligne.append("b")
            elif grille[elem][caract] == "S":
                ligne.append(0)
                Positions_moutons.append((elem, caract))
            else:
                return None
        Plateau.append(ligne)
    return Plateau, Positions_moutons       
            
            
            
def charger(fichier):
    """
    Fonction qui prend en argument un nom de fichier et qui créé une grille
    de ricosheep avec le contenu du fichier .txt
    """
    file =  open(fichier, "r")
    lines = file.readlines()
    file.close()
    
    grille = []
    for line in lines:
        grille.append(line.strip())
        
    return creer_plateau(grille)



  # -------------------------Sauvegarder sa partie---------------------------
def plateau_vers_texte(Plateau, Positions_moutons):
    """
    Fonction qui prend en parametre le plateau et la positions des moutons et
    ecrit une chaine de caractere qui contient toutes les informations de 
    l'avancement du jeu

    Parameters
    ----------
    Plateau : list
    Positions_moutons : list

    Returns list
    -------
    >>> plateau_vers_texte([[0,"b","g",0]], [(0,0)])
    ['SBG_']

    """
    

    txt = []
    
    for lignes in range(len(Plateau)):
        ligne = ""
        for caract in range(len(Plateau[lignes])):
            if (lignes, caract) in Positions_moutons:
                ligne += "S"
            elif Plateau[lignes][caract] == 0:
                ligne += "_"
            elif Plateau[lignes][caract] == "b":
                ligne += "B"
            elif Plateau[lignes][caract]== "g":
                ligne += "G"
        txt.append(ligne)
    return txt      

def sauvegarder(Plateau, Positions_moutons, fichier):
    """
    Fonction qui sert a sauvegarder une partie dans une fichier .txt
    """
    file = open(fichier, "w")
    for elem in plateau_vers_texte(Plateau, Positions_moutons):
        file.write(elem + "\n")    
  

  # -------------------------Partie Graphique ------------------------------
def affiche_grille(Plateau):
    """
    Fonction qui trace dans une fenêtre les cases du Plateau
    """
    for i in range(len(Plateau) + 1):  # trait horizontaux
        fltk.ligne(50, 50 + 100 * i, 50 + 100 * len(Plateau[0]), 50 + 100 * i)
    
    for i in range(len(Plateau[0]) + 1): #traits verticaux:
        fltk.ligne(50 + i * 100, 50, 50 +  i * 100, 50 + 100 * len(Plateau))    

def affiche_buisson_herbe(Plateau):
    """
    Fonction qui affiche les buissons et les herbes dans une fenêtre
    """
    for ligne in range(len(Plateau)):
        for case in range(len(Plateau[0])):
            if Plateau[ligne][case] == "g":
                fltk.image(case * 100 + 95, ligne * 100 + 75, "grass.png")
            if Plateau[ligne][case] == "b":
                fltk.image(case * 100 + 95, ligne * 100 + 100, "bush.png")


def affiche_mouton(Plateau, Positions_moutons):
    """
    Fonction qui est chargé de l'affichage des moutons dans le plateau 
    """
    fltk.efface("mouton")
    for mouton in Positions_moutons:
        if Plateau[mouton[0]][mouton[1]] == "g":
            fltk.image(100 + mouton[1] * 100, 100 + mouton[0] * 100, "sheep_grass.png", tag = "mouton")
            
        else:
            fltk.image(100 + mouton[1] * 100, 100 + mouton[0] * 100, "sheep.png", tag = "mouton")





  #--------------------------------Solveur--------------------------

def solveur(Plateau, Positions_moutons, lst_mouvement):
    """
    Fonction qui renvoie la liste des mouvements a faire pour gagner
    """
    if fin_jeu(Plateau, Positions_moutons):
        return lst_mouvement
    else:      
        new_move = choice(lst_direction)
        lst_mouvement.append(new_move)
        Positions_moutons = deplacement(Plateau, Positions_moutons, new_move)
        return solveur(Plateau, Positions_moutons, lst_mouvement)


  # ----------------------------------Main------------------------
  
  #doctest.testmod()    
  

  
  
print("Voici la liste des map", Liste_map)
grille = str(input("Donnez un nom de grille par la liste:"))
while grille not in Liste_map:
    grille = str(input("Donnez un nom de grille par la liste:"))
    

    
    

fltk.cree_fenetre(LARGEUR_FENETRE, LONGUEUR_FENETRE)


Plateau, Positions_moutons = charger(grille)
affiche_grille(Plateau)
affiche_buisson_herbe(Plateau)
affiche_mouton(Plateau, Positions_moutons)



while fin_jeu(Plateau, Positions_moutons) == False:
        affiche_mouton(Plateau, Positions_moutons)
        ev = fltk.donne_ev()
        tev = fltk.type_ev(ev)
    
    
        if tev == 'Touche':  
            if fltk.touche(ev) == "Up":
                Positions_moutons = deplacement(Plateau, Positions_moutons, "Haut")
                fltk.mise_a_jour()
            if fltk.touche(ev) == "Down":
                Positions_moutons = deplacement(Plateau, Positions_moutons, "Bas")
                fltk.mise_a_jour()
            if fltk.touche(ev) == "Left":
                Positions_moutons = deplacement(Plateau, Positions_moutons, "Gauche")
                fltk.mise_a_jour()
            if fltk.touche(ev) == "Right":
                Positions_moutons = deplacement(Plateau, Positions_moutons, "Droite")
                fltk.mise_a_jour()
            if fltk.touche(ev) == "s":
                sauvegarder(Plateau, Positions_moutons, "save.txt")
            
            
    
        elif tev == 'Quitte':  
            break
    
        else:
            pass
        fltk.mise_a_jour()
        
fltk.ferme_fenetre()  
  # -------------------------------------Fin---------------------------------

fltk.cree_fenetre(LARGEUR_FENETRE / 2, LONGUEUR_FENETRE / 2)
if fin_jeu(Plateau, Positions_moutons):
    fltk.image(250, 250, "sheep_win.png")
else:
    fltk.image(250,250, "sheep_lose.png")
fltk.attend_ev() 
fltk.ferme_fenetre()




    


  
    
    
    
    