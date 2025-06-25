# -*- coding: utf-8 -*-
"""
Created on Thu Jan 18 17:50:39 2024

@author: minse
"""


import math
import random
from colorama import Fore, Style

def afficher_grille(grille):
    for ligne in grille:
        print('|', end='')
        for case in ligne:
            if case == 0:
                print('   ', end='|')
            elif case == 1:
                print(f'{Fore.YELLOW}{Style.BRIGHT} O {Style.RESET_ALL}', end='|') 
            else:
                print(f'{Fore.RED}{Style.BRIGHT} O {Style.RESET_ALL}', end='|') 
        print('\n' + '-' * (4 * 12 + 1))
    print('|', end='')
    for i in range(len(grille[0])):
        if i <10:
            print(f' {i} ', end='|')
        else:
            print (f' {i} ', end = '|')
    print()



def colonne_valide(grille, colonne):
    return grille[0][colonne] == 0


def ajouter_jeton(grille, colonne, jeton):
    for i in range(5, -1, -1):
        if grille[i][colonne] == 0:
            grille[i][colonne] = jeton
            return True
    return False


def verifier_victoire(grille, jeton):
    for i in range(6):
        for j in range(9):
            if grille[i][j] == jeton and grille[i][j + 1] == jeton and grille[i][j + 2] == jeton and grille[i][j + 3] == jeton:
                return True
    for i in range(3):
        for j in range(12):
            if grille[i][j] == jeton and grille[i + 1][j] == jeton and grille[i + 2][j] == jeton and grille[i + 3][j] == jeton:
                return True
    for i in range(3, 6):
        for j in range(9):
            if grille[i][j] == jeton and grille[i - 1][j + 1] == jeton and grille[i - 2][j + 2] == jeton and grille[i - 3][j + 3] == jeton:
                return True
    for i in range(3):
        for j in range(9):
            if grille[i][j] == jeton and grille[i + 1][j + 1] == jeton and grille[i + 2][j + 2] == jeton and grille[i + 3][j + 3] == jeton:
                return True
    return False

def evaluer_grille(grille, joueur):
    score = 0

    # Vérification des lignes horizontales
    for i in range(6):
        for j in range(9):
            window = [grille[i][j], grille[i][j + 1], grille[i][j + 2], grille[i][j + 3]]
            score += evaluer_fenetre(window, joueur)

    # Vérification des lignes verticales
    for i in range(3):
        for j in range(12):
            window = [grille[i][j], grille[i + 1][j], grille[i + 2][j], grille[i + 3][j]]
            score += evaluer_fenetre(window, joueur)

    # Vérification des diagonales descendantes
    for i in range(3, 6):
        for j in range(9):
            window = [grille[i][j], grille[i - 1][j + 1], grille[i - 2][j + 2], grille[i - 3][j + 3]]
            score += evaluer_fenetre(window, joueur)

    # Vérification des diagonales montantes
    for i in range(3):
        for j in range(9):
            window = [grille[i][j], grille[i + 1][j + 1], grille[i + 2][j + 2], grille[i + 3][j + 3]]
            score += evaluer_fenetre(window, joueur)

    return score

def evaluer_fenetre(fenetre, joueur):
    score = 0
    adversaire = 3 - joueur

    if fenetre.count(joueur) == 4:
        score += 10000000000000
        
    elif fenetre.count(joueur) == 3 and fenetre.count(0) == 1:
        score += 5
    elif fenetre.count(joueur) == 2 and fenetre.count(0) == 2:
        score += 2

    if fenetre.count(adversaire) == 4:
        score -= 10000000000000
    elif fenetre.count(adversaire) == 3 and fenetre.count(0) == 1:
        score -= 100
    elif fenetre.count(adversaire) == 2 and fenetre.count(0) == 2:
        score -= 3

    return score

def minimax(grille, profondeur, alpha, beta, maximisant_joueur):
    coups_disponibles = [colonne for colonne in range(12) if colonne_valide(grille, colonne)]

    if profondeur == 0 or partie_finie(grille):
        return None, evaluer_grille(grille, 2)

    if maximisant_joueur:
        max_eval = -math.inf
        meilleur_coup = random.choice(coups_disponibles)
        for colonne in coups_disponibles:
            copie_grille = [ligne.copy() for ligne in grille]
            ajouter_jeton(copie_grille, colonne, 2)
            if verifier_victoire(copie_grille, 2):
                return colonne, 10000000000000
            
            _, evalutation = minimax(copie_grille, profondeur - 1, alpha, beta, False)
            if evalutation > max_eval:
                max_eval = evalutation
                meilleur_coup = colonne
            alpha = max(alpha, evalutation)
            if beta <= alpha:
                break
        return meilleur_coup, max_eval
    else:
        min_eval = math.inf
        pire_coup = random.choice(coups_disponibles)
        for colonne in coups_disponibles:
            copie_grille = [ligne.copy() for ligne in grille]
            ajouter_jeton(copie_grille, colonne, 1)
            _, evalutation = minimax(copie_grille, profondeur - 1, alpha, beta, True)
            if evalutation < min_eval:
                min_eval = evalutation
                pire_coup = colonne
            beta = min(beta, evalutation)
            if beta <= alpha:
                break
        return pire_coup, min_eval

def partie_finie(grille):
    return verifier_victoire(grille, 1) or verifier_victoire(grille, 2) or all(grille[0][colonne] != 0 for colonne in range(12))

def jeu_puissance4_IA():
    grille = [[0 for _ in range(12)] for _ in range(6)]

    choix_joueur = input("Choisissez qui commence - 'j' pour joueur, 'i' pour l'IA: ")

    joueur = 1 if choix_joueur.lower() == 'j' else 2
    fin_partie = False

    while not fin_partie:
        afficher_grille(grille)

        if joueur == 1:
            colonne_validee = False
            while not colonne_validee:
                try:
                    colonne = int(input(f"Joueur {joueur}, choisissez une colonne (0-11) pour placer votre jeton : "))
                    if 0 <= colonne <= 11 and colonne_valide(grille, colonne):
                        colonne_validee = True
                    else:
                        print("Colonne invalide ou pleine, choisissez-en une autre.")
                except ValueError:
                    print("Veuillez entrer un nombre valide pour la colonne.")
        else:
            colonne, _ = minimax(grille, 5, -math.inf, math.inf, True)
            print()
            print(f"L'IA a joué dans la colonne {colonne}.")

        if ajouter_jeton(grille, colonne, joueur):
            if verifier_victoire(grille, joueur):
                afficher_grille(grille)
                print(f"Le joueur {joueur} a gagné !")
                fin_partie = True
            elif partie_finie(grille):
                afficher_grille(grille)
                print("Match nul !")
                fin_partie = True
            else:
                joueur = 3 - joueur

    print("Fin du jeu.")

jeu_puissance4_IA()