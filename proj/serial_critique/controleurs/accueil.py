from model.model_pg import count_instances, top_colors, player_scores, parties_placee, avg_turn_month_year, top3_parties, get_random_brique, generer_grille
import random

tab1 = count_instances(SESSION['CONNEXION'], 'briques')
REQUEST_VARS ['nb_pieces'] = tab1[0][0]

tab2 = count_instances(SESSION['CONNEXION'], 'joueuse')
REQUEST_VARS ['nb_jouers'] = tab2[0][0]

tab3 = count_instances(SESSION['CONNEXION'], 'partie')
REQUEST_VARS ['nb_parties'] = tab3[0][0] 


REQUEST_VARS['couleur'] = top_colors(SESSION['CONNEXION'])

REQUEST_VARS['score']=player_scores(SESSION['CONNEXION'])

REQUEST_VARS['placee']=parties_placee(SESSION['CONNEXION'])

REQUEST_VARS['avg_turns']=avg_turn_month_year(SESSION['CONNEXION'])


REQUEST_VARS['parties']=top3_parties(SESSION['CONNEXION'])

REQUEST_VARS['rb'] = get_random_brique(SESSION['CONNEXION'])

if '4_briques' not in SESSION:
    SESSION['4_briques'] = [get_random_brique(SESSION['CONNEXION']) for _ in range(4)]

if 'grid' not in SESSION:
    lg, ht = 9, 8
    SESSION['grid'] = generer_grille(lg, ht)

if 'brique' in POST:  # formulaire soumis
    select = POST['brique']
    if select:
        idb = int(select[0])
        x = get_random_brique(SESSION['CONNEXION'])  
        for i, brique in enumerate(SESSION['4_briques']):
            print(f"Kiểm tra viên gạch {brique[0]} với viên đã chọn {select}")
            if brique[0] == idb:  
                SESSION['4_briques'][i] = x
                break                               



