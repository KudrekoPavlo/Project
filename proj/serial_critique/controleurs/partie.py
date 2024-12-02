from model.model_pg import  get_random_brique, generer_grille
import random
from controleurs.includes import add_activity


if '4_briques' not in SESSION:
    SESSION['4_briques'] = [get_random_brique(SESSION['CONNEXION']) for _ in range(4)]



    
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

    
if 'brique' in GET:
    try:
        idb = int(GET['brique'][0])  # Отримуємо ID цеглини
        for i, brique in enumerate(SESSION['4_briques']):
            if brique[0] == idb:
                SESSION['4_briques'][i] = get_random_brique(SESSION['CONNEXION'])  # Замінюємо обрану цеглину
                break
    except (ValueError, IndexError):
        REQUEST_VARS['error'] = "Erreur lors de la sélection de la brique."      