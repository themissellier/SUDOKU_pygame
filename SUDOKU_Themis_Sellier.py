import sys
import pygame as pg
import random

# on initialise la fenetre pygame
pg.init()
screen = pg.display.set_mode((800, 600))
pg.display.set_caption("Sudoku - Thémis Sellier")
pg.display.set_icon(pg.image.load('logo_sudoku.png'))

screen.fill(pg.Color("white"))

# on prepare toutes les polices d ecriture
font1 = pg.font.SysFont("arialblack", 30)
font2 = pg.font.SysFont("arialblack", 25)
font3 = pg.font.SysFont("arial", 25)
font_play = pg.font.SysFont("arialblack", 50)


def save():
    """
    Cette fonction permet d'enregistrer toutes les variables nécessaires à la reprise d'un partie de sudoku dans un
    fichier texte nommé sauvegarde.txt.
    """
    global grille_resolue, grille_dep, grille, taille, nb_hint, nb_errors

    # on ouvre le fichier en ecrasant eventuellement l ancien
    file = open("sauvegarde.txt", "w")

    file.write("Ce fichier contient les donnees necessaires a la sauvegarde d'une partie de sudoku.\n\n")

    # on rentre les donnees en chaines de caracteres
    file.write(str(grille_dep) + "\n\n")
    file.write(str(grille) + "\n\n")
    file.write(str(grille_resolue) + "\n\n")

    file.write(str(taille) + "\n\n")
    file.write(str(nb_errors) + "\n\n")
    file.write(str(nb_hint) + "\n\n")
    file.write(str(pg.time.get_ticks() - start_time))

    # on ferme le fichier
    file.close()


def convert_str_to_list(grille_str, taille):
    """
    Cette fonction permet de convertir la chaine de carcateres grille_str contenant un tableau à 2 dimensions en
    tableau d'entiers. Elle prend en parametre la chaine de caracteres de la grille et la taille de celle-ci.
    Elle retourne le tableau d'entiers à 2 dimensions.
    """
    # on initialise la nouvelle grille et les variables pour la boucle
    grille = [[0 for i in range(taille)] for j in range(taille)]
    nb_str = ""
    pos = 0
    # on parcourt la chaine de caracteres
    for i in range(len(grille_str)):
        if grille_str[i] != "[" and grille_str[i] != "]" and grille_str[i] != ",":
            nb_str += grille_str[i]
        if grille_str[i] == ",":
            grille[pos // taille][pos % taille] = int(nb_str)
            nb_str = ""
            pos += 1
    # on entre les nombres dans la grille
    grille[pos // taille][pos % taille] = int(nb_str)
    # on retourne le tableau d'entiers
    return grille


def reprendre():
    """
    Cette fonction permet de recuperer les variables necessaires à la reprise d'une partie de sudoku. Ces variables
    ont ete stockees dans un fichier texte nomme sauvegarde.txt après que le joueur est clique sur le bouton save
    lors d'une précédente partie.
    """
    global grille_resolue, grille_dep, grille, taille, nb_hint, nb_errors, resume_time

    # on ouvre la fichier texte pour le lire
    file = open("sauvegarde.txt", "r")
    # on stocke l ensemble du texte dans une variable
    donnees = file.read()
    # on ferme le fichier
    file.close()

    # on recupere toutes les chaines de caracteres correspondantes aux variables
    nb_crochets_d = 0
    nb_crochets_g = 0
    grille_dep_str = ""
    for i in range(len(donnees)):
        if donnees[i] == "[":
            nb_crochets_d += 1
        elif donnees[i] == "]":
            nb_crochets_g += 1
        if nb_crochets_d != nb_crochets_g or donnees[i] == "]":
            grille_dep_str = grille_dep_str + donnees[i]
        if nb_crochets_d == nb_crochets_g != 0:
            pos = i + 1
            break
    nb_crochets_d = 0
    nb_crochets_g = 0
    grille_str = ""
    for i in range(pos, len(donnees)):
        if donnees[i] == "[":
            nb_crochets_d += 1
        elif donnees[i] == "]":
            nb_crochets_g += 1
        if nb_crochets_d != nb_crochets_g or donnees[i] == "]":
            grille_str = grille_str + donnees[i]
        if nb_crochets_d == nb_crochets_g != 0:
            pos = i + 1
            break
    nb_crochets_d = 0
    nb_crochets_g = 0
    grille_resolue_str = ""
    for i in range(pos, len(donnees)):
        if donnees[i] == "[":
            nb_crochets_d += 1
        elif donnees[i] == "]":
            nb_crochets_g += 1
        if nb_crochets_d != nb_crochets_g or donnees[i] == "]":
            grille_resolue_str = grille_resolue_str + donnees[i]
        if nb_crochets_d == nb_crochets_g != 0:
            pos = i + 1
            break
    taille_str = ""
    for i in range(pos, len(donnees)):
        if donnees[i] != '\n':
            taille_str += donnees[i]
        elif donnees[i] == '\n' and taille_str != "":
            pos = i + 1
            break
    nb_errors_str = ""
    for i in range(pos, len(donnees)):
        if donnees[i] != '\n':
            nb_errors_str += donnees[i]
        elif donnees[i] == '\n' and nb_errors_str != "":
            pos = i + 1
            break
    nb_hint_str = ""
    for i in range(pos, len(donnees)):
        if donnees[i] != '\n':
            nb_hint_str += donnees[i]
        elif donnees[i] == '\n' and nb_hint_str != "":
            pos = i + 1
            break
    resume_time_str = ""
    for i in range(pos, len(donnees)):
        if donnees[i] != '\n':
            resume_time_str += donnees[i]
        elif donnees[i] == '\n' and resume_time_str != "":
            break

    # on convertit les chaines de caracteres en int
    taille = int(taille_str)
    nb_errors = int(nb_errors_str)
    nb_hint = int(nb_hint_str)
    resume_time = int(resume_time_str)

    # on convertit les chaines de caracteres en tableaux 2D de int
    grille_dep = convert_str_to_list(grille_dep_str, taille)
    grille = convert_str_to_list(grille_str, taille)
    grille_resolue = convert_str_to_list(grille_resolue_str, taille)


def hint():
    """
    Cette procedure permet de donner un indice à l'utilisateur quant à la solution du sudoku.
    Elle permet d'afficher le premier nombre non trouvé de la grille et de compter le nombre d'indices utilisés.
    """
    global nb_hint

    # on verifie que le jeu n est pas deja fini
    if not fini:
        # on compte le nombre d indices
        nb_hint += 1
        # on parcourt le tableau jusqu a trouver une case pour l indice
        for i in range(taille):
            for j in range(taille):
                if grille_dep[i][j] == 0 and grille[i][j] != grille_resolue[i][j]:
                    # on remplie la grille pour donner l indice a l utilisateur
                    grille[i][j] = grille_resolue[i][j]
                    pg.draw.rect(screen, (255, 255, 255), pg.Rect(j * width_case + 10, i * width_case + 25, width_case,
                                                                  width_case))
                    return


def solve():
    """
    Cette fonction permet de remplir la grille du joueur pour afficher la solution du sudoku a l ecran
    """
    # on parcourt les grilles
    for i in range(taille):
        for j in range(taille):
            # on regarde quelles cases sont fausses pour preparer l affichage
            if grille[i][j] != 0 and grille[i][j] != grille_resolue[i][j]:
                pg.draw.rect(screen, (255, 255, 255), pg.Rect(j * width_case + 10, i * width_case + 25, width_case,
                                                              width_case))
            # on remplit la grille du joueur avec la solution
            if grille[i][j] != grille_resolue[i][j] and grille_dep[i][j] == 0:
                grille[i][j] = grille_resolue[i][j]


def draw_curseur():
    """
    Cette procedure permet d afficher le curseur de sudoku sur la grille.
    Elle permet de colorer les zones qu'il faut regarder pour respecter les regles du sudoku suivant la case
    sur laquelle le joueur est positionne.
    """
    global curseur, colonne_curseur, ligne_curseur, region_curseur, pos

    # on prend la position du coin en gaut a gauche de la case selectionnee
    x = ((pos[0] - 10) // width_case) * width_case + 10
    y = ((pos[1] - 25) // width_case) * width_case + 25

    # on efface l ancien curseur qui n est plus sur la bonne case
    if 10 <= x <= width_case * taille and 25 <= y <= width_case * taille:
        pg.draw.rect(screen, (255, 255, 255), curseur, 6)
        pg.draw.rect(screen, (255, 255, 255), colonne_curseur)
        pg.draw.rect(screen, (255, 255, 255), ligne_curseur)
        pg.draw.rect(screen, (255, 255, 255), region_curseur)

        # on initialise la position du curseur
        curseur = pg.Rect(0, 0, width_case, width_case)
        ligne_curseur = pg.Rect(0, 0, width_case * taille, width_case)
        colonne_curseur = pg.Rect(0, 0, width_case, width_case * taille)
        region_curseur = pg.Rect(0, 0, width_case * width, width_case * height)

        # on le bouge a la position de la case selectionnee avec les calculs au debut de la fonction
        curseur = pg.Rect.move(curseur, x, y)
        colonne_curseur = pg.Rect.move(colonne_curseur, x, 25)
        ligne_curseur = pg.Rect.move(ligne_curseur, 10, y)
        region_curseur = pg.Rect.move(region_curseur,
                                      ((pos[0] - 10) // (width_case * width)) * (width_case * width) + 10,
                                      ((pos[1] - 25) // (width_case * height)) * (width_case * height) + 25)

        # on affiche les differents elements avec leur couleur respective
        pg.draw.rect(screen, (205, 249, 255), colonne_curseur)
        pg.draw.rect(screen, (205, 249, 255), ligne_curseur)
        pg.draw.rect(screen, (205, 249, 255), region_curseur)
        pg.draw.rect(screen, (0, 153, 204), curseur, 6)


def draw_timer():
    """
    Cette fonction permet d afficher le chronometre de la partie sur l interface.
    Elle permet egalement d afficher la taille, le niveau de sudoku de la partie, le nombre d erreurs et
    le nombre d indices utilises au cours de la partie.
    """
    global secs, mins, hours, resume_time

    # on reinitialise pour ne pas surcharger l affichage
    pg.draw.rect(screen, (255, 255, 255), pg.Rect(620, 0, 180, 110))

    # on affiche le nombre d erreurs et d indices utilises
    text1 = font3.render("Error(s) : {}".format(nb_errors), True, (0, 0, 0))
    screen.blit(text1, (620, 45))
    text1 = font3.render("Hint(s) : {}".format(nb_hint), True, (0, 0, 0))
    screen.blit(text1, (620, 80))
    # on affiche la taille et le niveau de la grille pour la partie en cours
    if taille == 9:
        text = "9x9 ;"
    elif taille == 8:
        text = "8x8 ;"
    elif taille == 6:
        text = "6x6 ;"
    else:
        text = "16x16 ;"
    if level == 0:
        text += " Facile"
    elif level == 1:
        text += " Moyen"
    elif level == 2:
        text += " Difficile"
    else:
        text += " Diabolique"
    text1 = font3.render(text, True, (0, 153, 204))
    screen.blit(text1, (620, 10))

    # on prepare l affichage du timer
    pg.draw.rect(screen, (255, 255, 255), pg.Rect(620, 500, 175, 120))

    # le timer change seulement si la partie est encore en cours
    if not fini:
        # on recupere la duree de jeu
        time_ms = pg.time.get_ticks()
        time_ms = time_ms - start_time + resume_time
        secs = time_ms // 1000
        mins = secs // 60
        secs = secs % 60
        hours = mins // 60
        mins = mins % 60
    else:
        # si le jeu est fini on l indique a l ecran
        screen.blit(pg.font.SysFont("arialblack", 50).render("FIN !", True, (0, 153, 204)), (630, 530))

    # on affiche le chronometre
    text1 = font1.render("{}:{}:{}".format(hours, mins, secs), True, (0, 0, 0))
    screen.blit(text1, (654, 500))


def draw_game_buttons():
    """
    Cette fonction permet d afficher les boutons home, save, hint et solve.
    """
    # on fait une boucle pour l affichage des rectangles
    for i in range(4):
        pg.draw.rect(screen, (0, 153, 204), pg.Rect(620, i * 70 + 130, 150, 50))
        pg.draw.rect(screen, (0, 0, 0), pg.Rect(620, i * 70 + 130, 150, 50), 2)
    # on affiche le texte dans les rectangles
    text1 = font1.render("HOME", True, (0, 0, 0))
    text2 = font1.render("SAVE", True, (0, 0, 0))
    text3 = font1.render("HINT", True, (0, 0, 0))
    text4 = font1.render("SOLVE", True, (0, 0, 0))
    screen.blit(text1, (645, 130))
    screen.blit(text2, (652, 200))
    screen.blit(text3, (655, 270))
    screen.blit(text4, (641, 340))

    # on met une image de chronometre
    image_chrono = pg.image.load('chronometre.png')
    image_chrono = pg.transform.scale(image_chrono, (80, 80))
    screen.blit(image_chrono, (655, 410))


def draw_sudoku():
    """
    Cette fonction permet d afficher les lignes de la grille de sudoku.
    """
    # la taille des traits de la grille change en fonction des dimensions de celle-ci
    if taille == 9:
        width_sudoku = 549
    elif taille == 6 or taille == 8:
        width_sudoku = 552
    elif taille == 16:
        width_sudoku = 544
    else:
        width_sudoku = 0
    for i in range(0, taille + 1):
        # pour dessiner les trais verticaux
        if i % width == 0:
            # l epaisseur change si on dessine le trait entre 2 regions du sudoku
            epaisseur = 5
        else:
            epaisseur = 3
        pg.draw.line(screen, pg.Color("black"), pg.Vector2((i * (width_sudoku // taille)) + 10, 25),
                     pg.Vector2((i * (width_sudoku // taille)) + 10, width_sudoku + 25), epaisseur)
        # pour dessiner les traits horizontaux
        if i % height == 0:
            # l epaisseur change si on dessine le trait entre 2 regions du sudoku
            epaisseur = 5
        else:
            epaisseur = 3
        pg.draw.line(screen, pg.Color("black"), pg.Vector2(10, (i * (width_sudoku // taille)) + 25),
                     pg.Vector2(width_sudoku + 10, (i * (width_sudoku // taille)) + 25), epaisseur)


def draw_starting_numbers(font, offset):
    """
    Cette fonction permet d affciher les nombres de la grille de depart grille_dep de couleur noir.
    """
    row = 0
    # on parcourt la grille
    while row < taille:
        col = 0
        while col < taille:
            number = grille_dep[row][col]
            if number != 0:
                if number < 10:
                    # on place les nombres plus petit que 10 pour qu ils soient bien centres
                    n_text = font.render(str(number), True, pg.Color('black'))
                    screen.blit(n_text, pg.Vector2((col * width_case) + offset - 5, (row * width_case) + offset))
                else:
                    # on place les nombres a deux chiffres de facon a ce qu ils soient centres
                    n_text = font.render(str(number), True, pg.Color('black'))
                    screen.blit(n_text, pg.Vector2((col * width_case) + offset - 18, (row * width_case) + offset))
            col += 1
        row += 1


def draw_user_numbers(font, offset):
    """
    Cette fonction permet d afficher tous les nombres hormis ceux de depart.
    Les nombres faux entres par l utilisateur sont ecrits en rouge, le reste en bleu.
    """
    # on parcourt le tableau
    row = 0
    while row < taille:
        col = 0
        while col < taille:
            number = grille[row][col]
            if number != 0:
                # on affiche en bleu si c est juste
                if number == grille_resolue[row][col]:
                    color = pg.Color('blue')
                # en rouge sinon
                else:
                    color = pg.Color('red')
                # on gere de nouveau les cas des nombres à 1 ou 2 chiffres
                if number < 10:
                    n_text = font.render(str(number), True, color)
                    screen.blit(n_text, pg.Vector2((col * width_case) + offset - 5, (row * width_case) + offset))
                else:
                    n_text = font.render(str(number), True, color)
                    screen.blit(n_text, pg.Vector2((col * width_case) + offset - 18, (row * width_case) + offset))
            col += 1
        row += 1


def draw_numbers():
    """
    Cette focntion permet utilise les deux fonctions precedentes pour afficher les nombres sur l interface
    """
    global width_case

    # on gere les differentes tailles
    if taille == 9:
        font = pg.font.SysFont("None", 70)
        draw_starting_numbers(font, 35)
        draw_user_numbers(font, 35)
    elif taille == 8:
        font = pg.font.SysFont("None", 70)
        draw_starting_numbers(font, 38)
        draw_user_numbers(font, 38)
    elif taille == 6:
        font = pg.font.SysFont("None", 90)
        draw_starting_numbers(font, 45)
        draw_user_numbers(font, 45)
    elif taille == 16:
        font = pg.font.SysFont("None", 35)
        draw_starting_numbers(font, 32)
        draw_user_numbers(font, 32)


def affiche_grille(tab):
    """
    Cette procedure permet d'afficher la grille de sudoku sur la console python.
    Elle prend en parametre le tableau à afficher.
    """
    # on commence par parcourir la grille
    for i in range(taille):
        # on gere l affichage des regions du sudoku
        if i % height == 0:
            print("- - " * taille)
        # une autre variable pour parcourir la grille
        for j in range(taille):
            # on gere l affichage des regions du sudoku
            if j % width == 0:
                print("|", end="")
            # on espace les nombres avec des tabulations
            print(tab[i][j], end="\t")
        print("|")
    print("----" * taille)


def possible(ligne, colonne, x):
    """
    Cette fonction permet de verifier que la valeur x peut etre mise dans la case (ligne,colonne) de la
    grille en appliquant les règles du sudoku.
    Elle retourne un booléen égal à True si les parametres respectent les regles du sudoku, False sinon.
    """

    # vérifier la colonne
    for i in range(0, taille):
        if grille_resolue[i][colonne] == x:
            return False

    # vérifier la ligne
    for j in range(0, taille):
        if grille_resolue[ligne][j] == x:
            return False

    # vérifier la case
    start_i = (ligne // height) * height
    start_j = (colonne // width) * width
    for i in range(height):
        for j in range(width):
            if grille_resolue[start_i + i][start_j + j] == x:
                return False
    return True


def resoudre_grille():
    """
    Cette fonction permet de resoudre une grille de sudoku.
    Elle renvoie True si la grille a pu etre resolue, False sinon.
    C'est une fonction recursive.
    Elle modifie la grille grille_resolue en tant que variable globale.
    """
    global grille_resolue

    # on parcourt la grille
    for i in range(0, taille):
        for j in range(0, taille):
            # on regarde les cases vides
            if grille_resolue[i][j] == 0:
                for x in range(1, taille + 1):
                    # on cherche les possibilites qui respectent les regles du sudoku
                    if possible(i, j, x):
                        # on essaie des possibilites
                        grille_resolue[i][j] = x
                        if resoudre_grille():
                            return True
                        # on revient en arriere si il y a un blocage
                        grille_resolue[i][j] = 0
                return False
    return True


def genere_grille():
    """
    Cette fonction permet de generer une grille entiere de sudoku dans grille_resolue.
    On genere d abord la premiere ligne de la grille aleatoirement avant d utiliser le backtracking.
    """
    global grille_resolue

    print("generating...")

    # on prepare les elements pour la premiere ligne
    elements = [k for k in range(1, taille + 1)]
    random.shuffle(elements)
    # on les affecte a la grille
    for k in range(taille):
        grille_resolue[0][k] = elements[k]
    # on utilise le backtracking pour generer le reste de la grille
    resoudre_grille()


def initialise_grille():
    """
    Cette fonction permet de generer la grille de depart grille_dep en fonction de la
    difficulte choisie.
    """
    global grille_dep

    # On teste combien de nombres doivent etre dans la grille de depart en fonction de la difficulte
    if level == 0:
        compteur = taille * taille - int((random.randint(40, 46) / 81) * taille * taille)
    elif level == 1:
        compteur = taille * taille - int((random.randint(47, 53) / 81) * taille * taille)
    elif level == 2:
        compteur = taille * taille - int((random.randint(54, 59) / 81) * taille * taille)
    else:
        compteur = taille * taille - int((63 / 81) * taille * taille)

    # on choisit au hasard les nombres qui seront dans la grille de depart a partir de grille_resolue
    k = 0
    while k < compteur:
        i = random.randint(0, taille - 1)
        j = random.randint(0, taille - 1)
        if grille_dep[i][j] == 0:
            grille_dep[i][j] = grille_resolue[i][j]
            k += 1


def consignes():
    """
    Cette fonction permet de generer tous les elements de la fenetre de consignes
    """
    global playing

    # on initialise le fond
    screen.fill(pg.Color("white"))
    # on affiche le logo
    screen.blit(pg.transform.scale(pg.image.load('logo_sudoku.png'), (270, 156)), (20, 180))

    # on affiche les consignes
    font_consignes = pg.font.SysFont("arial", 20)
    text_consignes = font_consignes.render("Chaque ligne, colonne et région doit être remplie avec les nombres", True,
                                           (0, 0, 0))
    screen.blit(text_consignes, (300, 25))
    text_consignes = font_consignes.render("de 1 à {} sans répétitions.".format(taille), True, (0, 0, 0))
    screen.blit(text_consignes, (300, 50))
    text_consignes = font_consignes.render("Pour écrire dans la grille, sélectionnez une case vide ou une case", True,
                                           (0, 0, 0))
    screen.blit(text_consignes, (300, 100))
    text_consignes = font_consignes.render("dont le nombre est écrit en rouge. Pour placer le curseur,", True,
                                           (0, 0, 0))
    screen.blit(text_consignes, (300, 125))
    text_consignes = font_consignes.render("sélectionnez une case avec la souris ou bien avec les flèches du", True,
                                           (0, 0, 0))
    screen.blit(text_consignes, (300, 150))
    text_consignes = font_consignes.render("clavier. Une fois la case sélectionnée, entrez le nombre désiré et", True,
                                           (0, 0, 0))
    screen.blit(text_consignes, (300, 175))
    text_consignes = font_consignes.render("appuyez sur la touche entrée pour valider.", True, (0, 0, 0))
    screen.blit(text_consignes, (300, 200))
    text_consignes = font_consignes.render("Si le nombre est juste il s'affichera en bleu, sinon en rouge.", True,
                                           (0, 0, 0))
    screen.blit(text_consignes, (300, 225))
    text_consignes = font_consignes.render("Pour effacer un nombre faux, appuyez sur la touche suppr ou retour", True,
                                           (0, 0, 0))
    screen.blit(text_consignes, (300, 275))
    text_consignes = font_consignes.render("après avoir sélectionné la case concernée. Il est également", True,
                                           (0, 0, 0))
    screen.blit(text_consignes, (300, 300))
    text_consignes = font_consignes.render("possible de rentrer 0 pour effacer un nombre.", True, (0, 0, 0))
    screen.blit(text_consignes, (300, 325))
    text_consignes = font_consignes.render("Attention ! Le nombre d'erreurs est compté.", True, (0, 0, 0))
    screen.blit(text_consignes, (300, 350))
    text_consignes = font_consignes.render("Il est également possible d'avoir des indices ou de voir la", True,
                                           (0, 0, 0))
    screen.blit(text_consignes, (300, 375))
    text_consignes = font_consignes.render("réponse grâce aux boutons à la droite de la grille.", True, (0, 0, 0))
    screen.blit(text_consignes, (300, 400))
    text_consignes = font_consignes.render("Vous pouvez également sauvegarder votre partie en cours pour la", True, (0, 0, 0))
    screen.blit(text_consignes, (300, 425))
    text_consignes = font_consignes.render("reprendre plus tard.", True, (0, 0, 0))
    screen.blit(text_consignes, (300, 450))
    text_consignes = pg.font.SysFont("arialblack", 20).render("Cliquez une fois pour commencer ou appuyez sur la touche espace.", True, (0, 154, 203))
    screen.blit(text_consignes, (40, 490))
    text_consignes = pg.font.SysFont("arialblack", 30).render("Puis patientez quelques instants...", True,
                                                              (0, 154, 203))
    screen.blit(text_consignes, (120, 525))

    # on gere les interactions avec le joueur
    for event in pg.event.get():
        # s le joueur veut fermer la fenetre
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        # si le joueur est pret a jouer
        if event.type == pg.MOUSEBUTTONDOWN or (event.type == pg.KEYDOWN and event.key == pg.K_SPACE):
            playing = True
            screen.fill(pg.Color("white"))
            return False

    # on actualise la fenetre
    pg.display.flip()
    return True


def game_loop():
    """
    Cette fonction permet de gerer l ensemble des elements en rapport avec la fentre de jeu.
    Elle gere les fonctions et les interactions avec le joueur.
    """
    global saisie, pos, grille, width_case, nb_errors

    # on affiche les elements
    draw_sudoku()
    draw_game_buttons()
    draw_timer()
    draw_numbers()
    pg.display.flip()

    for event in pg.event.get():
        # si le joueur veut fermer la fenetre
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

        # gerer la position de la souris quand on clique
        if event.type == pg.MOUSEBUTTONDOWN:
            pos = event.pos
            # pour le curseur de la grille
            if 10 <= pos[0] <= width_case * taille + 10 and 25 <= pos[1] <= width_case * taille + 25:
                saisie = ""
            # pour les boutons
            elif 620 <= pos[0] <= 770 and 130 <= pos[1] <= 180:
                home_menu()
            elif 620 <= pos[0] <= 770 and 200 <= pos[1] <= 250:
                save()
            elif 620 <= pos[0] <= 770 and 270 <= pos[1] <= 320:
                hint()
            elif 620 <= pos[0] <= 770 and 340 <= pos[1] <= 390:
                solve()

        # quand une touche du clavier est enfoncee
        if event.type == pg.KEYDOWN:
            # gerer la position du curseur avec le clavier
            if pos[0] < 10 or pos[0] > 10 + width_case * taille or pos[1] < 25 or pos[1] > 25 + width_case * taille:
                pos = (10, 25)
            else:
                if event.key == pg.K_UP:
                    if 25 + width_case <= pos[1] <= width_case * taille + 25:
                        pos = (pos[0], pos[1] - width_case)
                        saisie = ""
                elif event.key == pg.K_DOWN:
                    if 25 <= pos[1] < width_case * (taille - 1) + 25:
                        pos = (pos[0], pos[1] + width_case)
                        saisie = ""
                elif event.key == pg.K_RIGHT:
                    if 10 <= pos[0] < (10 + ((taille - 1) * width_case)):
                        pos = (pos[0] + width_case, pos[1])
                        saisie = ""
                elif event.key == pg.K_LEFT:
                    if 10 + width_case <= pos[0] <= width_case * taille + 10:
                        pos = (pos[0] - width_case, pos[1])
                        saisie = ""

            # gerer les interactions avec l utilisateur pour ecrire dans la grille
            if event.key == pg.K_0 or event.key == pg.K_KP0:
                saisie += "0"
            if event.key == pg.K_1 or event.key == pg.K_KP1:
                saisie += "1"
            if event.key == pg.K_2 or event.key == pg.K_KP2:
                saisie += "2"
            if event.key == pg.K_3 or event.key == pg.K_KP3:
                saisie += "3"
            if event.key == pg.K_4 or event.key == pg.K_KP4:
                saisie += "4"
            if event.key == pg.K_5 or event.key == pg.K_KP5:
                saisie += "5"
            if event.key == pg.K_6 or event.key == pg.K_KP6:
                saisie += "6"
            if event.key == pg.K_7 or event.key == pg.K_KP7:
                saisie += "7"
            if event.key == pg.K_8 or event.key == pg.K_KP8:
                saisie += "8"
            if event.key == pg.K_9 or event.key == pg.K_KP9:
                saisie += "9"
            # on gere la validation de la saisie
            if event.key == pg.K_RETURN or event.key == pg.K_KP_ENTER:
                try:
                    if saisie != "" and taille >= int(saisie) >= 0 == grille_dep[(pos[1] - 25) // width_case][(pos[0] - 10) // width_case] and grille[(pos[1] - 25) // width_case][(pos[0] - 10) // width_case] != grille_resolue[(pos[1] - 25) // width_case][(pos[0] - 10) // width_case]:
                        grille[(pos[1] - 25) // width_case][(pos[0] - 10) // width_case] = int(saisie)
                        if int(saisie) != grille_resolue[(pos[1] - 25) // width_case][(pos[0] - 10) // width_case] and \
                                int(saisie) != 0:
                            nb_errors += 1
                        draw_curseur()
                finally:
                    saisie = ""
            # si l utilisateur veut effacer un nombre faux
            if event.key == pg.K_BACKSPACE or event.key == pg.K_DELETE:
                print("ok")
                grille[(pos[1] - 25) // width_case][(pos[0] - 10) // width_case] = 0
                pg.draw.rect(screen, (255, 2, 2), pg.Rect((((pos[0] - 10) % width_case) * width_case) + 10,
                                                          ((pos[1] - 25) % width_case) * width_case + 25,
                                                          width_case, width_case))
                draw_curseur()
                saisie = ""

        # pour actualiser la fenetre
        pg.display.flip()


def home_menu():
    """
    Cette fonction permet de gerer les elements pour le menu home et les interactions avec l utilisateur
    """
    global playing, taille, level, rules, pos, grille, grille_dep, grille_resolue, nb_errors, nb_hint, resume

    # on prepare les variables et la fenetre
    playing = False
    screen.fill(pg.Color("white"))

    screen.blit(pg.transform.scale(pg.image.load('logo_sudoku.png'), (440, 180)), (180, 0))

    # afficher le bouton play
    pg.draw.rect(screen, (0, 153, 204), pg.Rect(530, 315, 200, 90))
    pg.draw.rect(screen, (0, 0, 0), pg.Rect(530, 315, 200, 90), 4)
    text_play = font_play.render("PLAY", True, (0, 0, 0))
    screen.blit(text_play, (557, 320))

    # afficher le bouton reprendre
    pg.draw.rect(screen, (255, 255, 153), pg.Rect(530, 445, 200, 50))
    pg.draw.rect(screen, (0, 0, 0), pg.Rect(530, 445, 200, 50), 2)
    text_play = font2.render("Reprendre", True, (0, 0, 0))
    screen.blit(text_play, (560, 450))

    # on fait des boucles pour afficher les boutons concernant la taille de la grille et la difficulte
    for j in range(2):
        for i in range(4):
            color = (255, 255, 153)
            if j == 0:
                if (taille == 9 and i == 0) or (taille == 6 and i == 1) or (taille == 8 and i == 2) or (
                        taille == 16 and i == 3):
                    color = (0, 153, 204)
            else:
                if (level == 0 and i == 0) or (level == 1 and i == 1) or (level == 2 and i == 2) or (
                        level == 3 and i == 3):
                    color = (0, 153, 204)
            pg.draw.rect(screen, color, pg.Rect(j * 230 + 75, i * 90 + 200, 160, 50))
            pg.draw.rect(screen, (0, 0, 0), pg.Rect(j * 230 + 75, i * 90 + 200, 160, 50), 2)
    # on ecrit le texte sur les boutons
    text1 = font1.render("9x9", True, (0, 0, 0))
    text2 = font1.render("6x6", True, (0, 0, 0))
    text3 = font1.render("8x8", True, (0, 0, 0))
    text4 = font1.render("16x16", True, (0, 0, 0))
    screen.blit(text1, (125, 200))
    screen.blit(text2, (125, 290))
    screen.blit(text3, (125, 380))
    screen.blit(text4, (104, 470))
    text1 = font2.render("Facile", True, (0, 0, 0))
    text2 = font2.render("Moyen", True, (0, 0, 0))
    text3 = font2.render("Difficile", True, (0, 0, 0))
    text4 = font2.render("Diabolique", True, (0, 0, 0))
    screen.blit(text1, (343, 206))
    screen.blit(text2, (340, 296))
    screen.blit(text3, (332, 386))
    screen.blit(text4, (313, 476))

    # on gere les interactions avec l utilisateur
    for event in pg.event.get():
        # si le joueur veut fermer la fenetre
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        # si le joueur est pret a jouer
        if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
            playing = True
            rules = True
            pos = (0, 0)
        # si le joueur clique quelque part
        if event.type == pg.MOUSEBUTTONDOWN:
            pos = event.pos
            # on regarde la position au moment du clic pour changer les parametres de la partie de sudoku qui va etre lancee
            if 75 <= pos[0] <= 225 and 200 <= pos[1] <= 250:
                taille = 9
            elif 75 <= pos[0] <= 225 and 290 <= pos[1] <= 340:
                taille = 6
            elif 75 <= pos[0] <= 225 and 380 <= pos[1] <= 430:
                taille = 8
            elif 75 <= pos[0] <= 225 and 470 <= pos[1] <= 520:
                taille = 16
            elif 305 <= pos[0] <= 455 and 200 <= pos[1] <= 250:
                level = 0
            elif 305 <= pos[0] <= 455 and 290 <= pos[1] <= 340:
                level = 1
            elif 305 <= pos[0] <= 455 and 380 <= pos[1] <= 430:
                level = 2
            elif 305 <= pos[0] <= 455 and 470 <= pos[1] <= 520:
                level = 3
            # si le joueur est pret a jouer et qu il utilise la souris
            elif 530 <= pos[0] <= 730 and 315 <= pos[1] <= 405:
                playing = True
                rules = True
                pos = (0, 0)
            elif 530 <= pos[0] <= 730 and 445 <= pos[1] <= 495:
                resume = True
                playing = True
                rules = True
                pos = (0, 0)

        # on actualise la fenetre
        pg.display.flip()


# on met en place les variables de depart
taille = 9
level = 0
# height correspond à la hauteur d une region (en nombre de cases)
height = 0
# width correspond à la largeur d une region (en nombre de cases)
width = 0

# pour le timer
secs = 0
mins = 0
hours = 0

width_case = 0

# ces variables permettent de gerer les moments des fenetres (home_menu, game_loop ou consignes)
playing = False
rules = False
resume = False
# pour gerer le cas ou la grille est resolue
fini = False

# pour gerer les positions de la souris plus tard
pos = (0, 0)

# la boucle tourne jusqu'a ce que le programme s arrete en fermant la fenetre pygame avec la croix rouge
while 1:

    while not playing and not rules:
        resume = False
        home_menu()
    # si le joueur veut reprendre une partie, on recupere les donnes dont on a besoin
    if resume:
        reprendre()

    while playing and rules:
        rules = consignes()

    # pour gerer les differentes tailles avant de jouer
    if taille == 9:
        height = 3
        width = 3
        width_case = 61
    else:
        if taille == 6:
            height = 2
            width = 3
            width_case = 92
        else:
            if taille == 16:
                height = 4
                width = 4
                width_case = 34
            else:
                height = 2
                width = 4
                width_case = 69
    # si le joueur commence une nouvelle partie
    if not resume:
        grille_dep = [[0 for i in range(taille)] for j in range(taille)]
        grille = [[0 for i in range(taille)] for j in range(taille)]
        grille_resolue = [[0 for i in range(taille)] for j in range(taille)]

        resume_time = 0
        genere_grille()
        initialise_grille()

        nb_errors = 0
        nb_hint = 0
    else:
        # on prepare la variable pour la prochaine partie
        resume = False

    # on prend le temps de debut de partie
    start_time = pg.time.get_ticks()

    # on prepare les elements pour le curseur
    curseur = pg.Rect(0, 0, width_case, width_case)
    ligne_curseur = pg.Rect(0, 0, width_case * taille, width_case)
    colonne_curseur = pg.Rect(0, 0, width_case, width_case * taille)
    region_curseur = pg.Rect(0, 0, width_case * width, width_case * height)

    saisie = ""
    pos = (10, 25)
    while playing and not rules:
        draw_curseur()
        game_loop()
        fini = True
        # on parcourt la grille pour regarder si la partie est terminee
        for i in range(taille):
            for j in range(taille):
                if grille_resolue[i][j] != grille[i][j] and grille_resolue[i][j] != grille_dep[i][j]:
                    fini = False
