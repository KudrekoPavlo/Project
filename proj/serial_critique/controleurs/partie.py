from model.model_pg import  get_random_brique, generer_grille, get_random_brique_hard
import random
from controleurs.includes import add_activity


#maximum tours
if 'max_tours' not in SESSION:
    SESSION['max_tours'] = int(10)

if 'maxmouv' in GET:
    try:
        max_tours = int(GET['maxmouv'][0]) + 1
        SESSION['max_tours'] = max_tours
    except ValueError:
        REQUEST_VARS['maxt_e'] = "La valeur de tour maaximal n`est pas bon"

#mode de joue
if 'mode_jou' not in SESSION:
     SESSION['mode_jou'] = ''

if 'mode' in GET :
    m = GET['mode'][0]
    SESSION['mode_jou'] = m

      
#taille de grille       
if 'y' in GET and 'x' in GET:
    try:
        taille_y = int(GET['y'][0])
        taille_x = int(GET['x'][0])
        if 8 <= taille_y <= 25 and 9 <= taille_x <= 16:
            SESSION['grid'] = generer_grille(taille_y, taille_x)
            SESSION['tailles'] = [taille_y, taille_x]
        else:
            REQUEST_VARS['tailles_e'] = "Les valeurs doivent respecter les conditions (8 <= hauteur <= 25, 9 <= longueur <= 16)"
    except ValueError:
        REQUEST_VARS['tailles_e'] = "Les valeurs que vous avez choisi ne sont pas bon"



if SESSION['mode_jou'] == 'izi':
    #premiers quetre briques alleatoire
    if '4_briques' not in SESSION:
        SESSION['4_briques'] = [get_random_brique(SESSION['CONNEXION']) for _ in range(4)]

    #changement de brique choisis    
    if 'brique' in GET:
        SESSION['max_tours'] -=  1 # pour controler le nombre de tours si besoin 
        try:
            idb = int(GET['brique'][0])  
            for i, brique in enumerate(SESSION['4_briques']):
                if brique[0] == idb:
                    SESSION['4_briques'][i] = get_random_brique(SESSION['CONNEXION'])  
                    break
        except (ValueError, IndexError):
            REQUEST_VARS['error'] = "Erreur lors de la sélection de la brique." 
else:
    #premiers quetre briques alleatoire
    if '4_briques' not in SESSION:
        SESSION['4_briques'] = [get_random_brique_hard(SESSION['CONNEXION']) for _ in range(4)]

    #changement de brique choisis    
    if 'brique' in GET:
        SESSION['max_tours'] -=  1 # pour controler le nombre de tours si besoin 
        try:
            idb = int(GET['brique'][0])  
            for i, brique in enumerate(SESSION['4_briques']):
                if brique[0] == idb:
                    SESSION['4_briques'][i] = get_random_brique_hard(SESSION['CONNEXION'])  
                    break
        except (ValueError, IndexError):
            REQUEST_VARS['error'] = "Erreur lors de la sélection de la brique." 


    


#si utilisateur a utilise tout les tours donner
if 1 == SESSION['max_tours'] : 
    SESSION['perdr'] = "aff"

#initialisation de perdre
if 'NewGame' in GET:
    SESSION['4_briques'] = [get_random_brique(SESSION['CONNEXION']) for _ in range(4)]
    SESSION['max_tours'] = 0
    REQUEST_VARS['maxt_e'] = 0
    SESSION['grid'] = 0
    SESSION['tailles'] = 0
    REQUEST_VARS['tailles_e'] = 0
    REQUEST_VARS['error'] = 0
    SESSION['perdr'] = 0



