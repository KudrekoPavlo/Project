from model.model_pg import  get_random_brique, generer_grille, get_random_brique_hard
import random
from controleurs.includes import add_activity


#maximum tours
if 'max_tours' not in SESSION:
    SESSION['max_tours'] = int(10)

#initialisation des tours maximals
if 'maxmouv' in GET:
    try:
        max_tours = int(GET['maxmouv'][0]) + 1
        SESSION['max_tours'] = max_tours
    except ValueError:
        REQUEST_VARS['maxt_e'] = "La valeur de tour maaximal n`est pas bon"

#mode de joue
if 'mode_jou' not in SESSION:
     SESSION['mode_jou'] = -1
#initialisation de mode de joue
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

# initialisation de booleen pour verifier si joueur a choisis les bons coordonnee
if 'bool_v' not in REQUEST_VARS:
    REQUEST_VARS['bool_v'] = 1


#initialisation de score
if 'score' not in SESSION:
    SESSION['score'] = 1

#premiers quetre briques alleatoire
if '4_briques' not in SESSION:
    SESSION['4_briques'] = [get_random_brique(SESSION['CONNEXION']) for _ in range(4)]


#verification de mode de joue
if SESSION['mode_jou'] == "izi":

    
    #verification de l`action avec le brique, s`il a ete placee ou defausse   
    if 'action_br' in GET and 'brique' in GET:
        try:
            action_br = GET['action_br'][0]
            idb = int(GET['brique'][0])
            brique = next(b for b in SESSION['4_briques'] if b[0] == int(GET['brique'][0]))
            REQUEST_VARS['brique_couleur'] = brique[3]

            #si brique a ete defausse
            if action_br == "defause":  

                SESSION['max_tours'] -= 1  
                SESSION['score'] += 1  

                for i, brique in enumerate(SESSION['4_briques']):
                    if brique[0] == idb:
                        SESSION['4_briques'][i] = get_random_brique(SESSION['CONNEXION'])
                        break
            #si la brique a ete placee            
            elif action_br == "placee" and 'coord_x' in GET and'coord_y' in GET:
                #on ajout le score et soustraire de nombre des tours
                SESSION['max_tours'] -= 1  
                SESSION['score'] += 1 

                #initialisation de taille de brique, et ses coordonnees de deplacement perspective
                REQUEST_VARS['coord_brique'] = next(b for b in SESSION['4_briques'] if b[0] == int(GET['brique'][0]))
                REQUEST_VARS['coord_x'] = int(GET['coord_x'][0])
                REQUEST_VARS['coord_y'] = int(GET['coord_y'][0])
                REQUEST_VARS['l_b'], REQUEST_VARS['h_b']  = REQUEST_VARS['coord_brique'][1], REQUEST_VARS['coord_brique'][2]

                #verivication si on peux deplaser la brique sur cette coordonnees
                if all(
                    SESSION['grid'][REQUEST_VARS['coord_y']][REQUEST_VARS['coord_x']] == 'x'
                    for y in range(REQUEST_VARS['coord_y'], REQUEST_VARS['h_b'] + REQUEST_VARS['coord_y'])
                    for x in range(REQUEST_VARS['coord_x'],REQUEST_VARS['coord_x'] + REQUEST_VARS['l_b'])
                ):
                    try: 
                        
                        #Verification s`il y a un autre brique qui est deja installer
                        for x in range(REQUEST_VARS['coord_y'], REQUEST_VARS['coord_y'] + REQUEST_VARS['h_b']):
                            for y in range(REQUEST_VARS['coord_x'], REQUEST_VARS['coord_x'] + REQUEST_VARS['l_b']):
                                if SESSION['grid'][x][y] != 'x':
                                    REQUEST_VARS['bool_v'] = 0

                        #s`il n`y a pas de brique qui est deja installer on ajout dans la session les donnes de brique choisi si non on initialise erreur
                        if REQUEST_VARS['bool_v'] == 1:
                            for x in range(REQUEST_VARS['coord_y'], REQUEST_VARS['coord_y'] + REQUEST_VARS['h_b']):
                                for y in range(REQUEST_VARS['coord_x'], REQUEST_VARS['coord_x'] + REQUEST_VARS['l_b']):            
                                    SESSION['grid'][x][y] = {'type' : 'y', 'color' : REQUEST_VARS['brique_couleur']}
                        else:
                            REQUEST_VARS['error'] = "Les coordonnees choisis ne sont pas bon pas bon"
                           
                        # On change la brique si il est bien installer    
                        if REQUEST_VARS['bool_v'] == 1: 
                            SESSION['4_briques'] = [get_random_brique(SESSION['CONNEXION']) if b[0] == idb else b for b in SESSION['4_briques']]

                        # On change la booleen par 1 pour nouvelle tour    
                        REQUEST_VARS['bool_v']  = 1

                        #Verivication de gagne
                        if not any(cell == 'x' for row in SESSION['grid'] for cell in row):
                            SESSION['perdr'] = 'gan'  
                    # Apres initialisation d`erreur de tout raison possible
                    except:
                        REQUEST_VARS['error'] = "Le brique n`a pas de bon taille, ou il est mal deplacee"
                else:
                    SESSION['max_tours'] -= 1  
                    SESSION['score'] += 1
                    REQUEST_VARS['error'] = "Les coordonnees choisis ne sont pas bon pas bon"
            else:  
                SESSION['max_tours'] -= 1  
                SESSION['score'] += 1
                REQUEST_VARS['error'] = "Il faut ecrire les coordonnee" 
        except (ValueError, IndexError, StopIteration):
            REQUEST_VARS['error'] = "Le brique n`a pas de bon taille, ou il est mal deplacee"

else :

    #  Si la mode de joue est difficile, c`est la meme structure que pour la joue facile, 
    # c`est qui change est les bruque qui s`initialise avec nouvelle fonction get_random_brique_hard 
    if 'action_br' in GET and 'brique' in GET:
        try:
            action_br = GET['action_br'][0]
            idb = int(GET['brique'][0])
            brique = next(b for b in SESSION['4_briques'] if b[0] == int(GET['brique'][0]))
            REQUEST_VARS['brique_couleur'] = brique[3]
            if action_br == "defause":  

                SESSION['max_tours'] -= 1  
                SESSION['score'] += 1  

                for i, brique in enumerate(SESSION['4_briques']):
                    if brique[0] == idb:
                        SESSION['4_briques'][i] = get_random_brique_hard(SESSION['CONNEXION'])
                        break
            elif action_br == "placee" and 'coord_x' in GET and'coord_y' in GET:

                SESSION['max_tours'] -= 1  
                SESSION['score'] += 1 

                REQUEST_VARS['coord_brique'] = next(b for b in SESSION['4_briques'] if b[0] == int(GET['brique'][0]))
                REQUEST_VARS['coord_x'] = int(GET['coord_x'][0])
                REQUEST_VARS['coord_y'] = int(GET['coord_y'][0])
                REQUEST_VARS['l_b'], REQUEST_VARS['h_b']  = REQUEST_VARS['coord_brique'][1], REQUEST_VARS['coord_brique'][2]
                if all(
                    SESSION['grid'][REQUEST_VARS['coord_y']][REQUEST_VARS['coord_x']] == 'x'
                    for y in range(REQUEST_VARS['coord_y'], REQUEST_VARS['h_b'] + REQUEST_VARS['coord_y'])
                    for x in range(REQUEST_VARS['coord_x'],REQUEST_VARS['coord_x'] + REQUEST_VARS['l_b'])
                ):
                    try: 
                        for x in range(REQUEST_VARS['coord_y'], REQUEST_VARS['coord_y'] + REQUEST_VARS['h_b']):
                            for y in range(REQUEST_VARS['coord_x'], REQUEST_VARS['coord_x'] + REQUEST_VARS['l_b']):
                                if SESSION['grid'][x][y] != 'x':
                                    REQUEST_VARS['bool_v'] = 0

                        for x in range(REQUEST_VARS['coord_y'], REQUEST_VARS['coord_y'] + REQUEST_VARS['h_b']):
                            for y in range(REQUEST_VARS['coord_x'], REQUEST_VARS['coord_x'] + REQUEST_VARS['l_b']):            
                                if REQUEST_VARS['bool_v'] == 1:
                                    SESSION['grid'][x][y] = {'type' : 'y', 'color' : REQUEST_VARS['brique_couleur']}
                                else:
                                    REQUEST_VARS['error'] = "Les coordonnees choisis ne sont pas bon pas bon"
                           
                        if REQUEST_VARS['bool_v'] == 1: 
                            SESSION['4_briques'] = [get_random_brique_hard(SESSION['CONNEXION']) if b[0] == idb else b for b in SESSION['4_briques']]
                        REQUEST_VARS['bool_v']  = 1
                        
                        if not any(cell == 'x' for row in SESSION['grid'] for cell in row):
                            SESSION['perdr'] = 'gan'  

                    except:
                        REQUEST_VARS['error'] = "Le brique n`a pas de bon taille, ou il est mal deplacee"
                else:
                    SESSION['max_tours'] -= 1  
                    SESSION['score'] += 1
                    REQUEST_VARS['error'] = "Les coordonnees choisis ne sont pas bon pas bon"
            else:  
                SESSION['max_tours'] -= 1  
                SESSION['score'] += 1
                REQUEST_VARS['error'] = "Il faut ecrire les coordonnee" 
        except (ValueError, IndexError, StopIteration):
            REQUEST_VARS['error'] = "Le brique n`a pas de bon taille, ou il est mal deplacee"
 


# Scenario si joueur s`abandonne      
if 'Abandonner' in GET:
    SESSION['perdr'] = "per"



#si utilisateur a utilise tout les tours donner ou il a abandonnee
if 1 == SESSION['max_tours'] : 
    SESSION['perdr'] = "per"
    SESSION['score'] = 999

#Les actes en cas de perdre
if 'NewGame' in GET:
    SESSION['4_briques'] = [get_random_brique(SESSION['CONNEXION']) for _ in range(4)]
    SESSION['max_tours'] = 0
    REQUEST_VARS['maxt_e'] = 0
    SESSION['grid'] = 0
    SESSION['tailles'] = 0
    REQUEST_VARS['tailles_e'] = 0
    REQUEST_VARS['error'] = 0
    SESSION['perdr'] = 0






