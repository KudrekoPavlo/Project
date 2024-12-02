import psycopg
from psycopg import sql
from logzero import logger
import random

def execute_select_query(connexion, query, params=[]):
    """
    Méthode générique pour exécuter une requête SELECT (qui peut retourner plusieurs instances).
    Utilisée par des fonctions plus spécifiques.
    """
    with connexion.cursor() as cursor:
        try:
            cursor.execute(query, params)
            result = cursor.fetchall()
            return result 
        except psycopg.Error as e:
            logger.error(e)
    return None

def execute_other_query(connexion, query, params=[]):
    """
    Méthode générique pour exécuter une requête INSERT, UPDATE, DELETE.
    Utilisée par des fonctions plus spécifiques.
    """
    with connexion.cursor() as cursor:
        try:
            cursor.execute(query, params)
            result = cursor.rowcount
            return result 
        except psycopg.Error as e:
            logger.error(e)
    return None

def get_instances(connexion, nom_table):
    """
    Retourne les instances de la table nom_table
    String nom_table : nom de la table
    """
    query = sql.SQL('SELECT * FROM {table}').format(table=sql.Identifier(nom_table), )
    return execute_select_query(connexion, query)

def count_instances(connexion, nom_table):
    """
    Retourne le nombre d'instances de la table nom_table
    String nom_table : nom de la table
    """
    query = sql.SQL('SELECT COUNT(*) AS nb FROM {table}').format(table=sql.Identifier(nom_table))
    return execute_select_query(connexion, query)

def get_episodes_for_num(connexion, numero):
    """
    Retourne le titre des épisodes numérotés numero
    Integer numero : numéro des épisodes
    """
    query = 'SELECT titre FROM episodes where numéro=%s'
    return execute_select_query(connexion, query, [numero])

def get_serie_by_name(connexion, nom_serie):
    """
    Retourne les informations sur la série nom_serie (utilisé pour vérifier qu'une série existe)
    String nom_serie : nom de la série
    """
    query = 'SELECT * FROM series where nomsérie=%s'
    return execute_select_query(connexion, query, [nom_serie])

def insert_serie(connexion, nom_serie):
    """
    Insère une nouvelle série dans la BD
    String nom_serie : nom de la série
    Retourne le nombre de tuples insérés, ou None
    """
    query = 'INSERT INTO series VALUES(%s)'
    return execute_other_query(connexion, query, [nom_serie])

def get_table_like(connexion, nom_table, like_pattern):
    """
    Retourne les instances de la table nom_table dont le nom correspond au motif like_pattern
    String nom_table : nom de la table
    String like_pattern : motif pour une requête LIKE
    """
    motif = '%' + like_pattern + '%'
    nom_att = 'nomsérie'  # nom attribut dans séries (à éviter)
    if nom_table == 'actrices':  # à éviter
        nom_att = 'nom'  # nom attribut dans actrices (à éviter)
    query = sql.SQL("SELECT * FROM {} WHERE {} ILIKE {}").format(
        sql.Identifier(nom_table),
        sql.Identifier(nom_att),
        sql.Placeholder())
    #    like_pattern=sql.Placeholder(name=like_pattern))
    return execute_select_query(connexion, query, [motif])

def get_instances(connexion, nom_table):
    """
    Retourne les instances de la table nom_table
    String nom_table : nom de la table
    """
    query = sql.SQL('SELECT * FROM {table}').format(table=sql.Identifier(nom_table), )
    return execute_select_query(connexion, query)

#Nombre d’instances pour 3 tables de votre choix 
def count_instances(connexion, nom_table):
    """
    Retourne le nombre d'instances de la table nom_table
    String nom_table : nom de la table
    """
    query = sql.SQL('SELECT COUNT(*) AS nb FROM {table}').format(table=sql.Identifier(nom_table))
    return execute_select_query(connexion, query)


#Top-5 des couleurs ayant le plus de briques
def top_colors(connexion):
        
    query = "SELECT couleur FROM piece GROUP BY couleur ORDER BY COUNT(*) DESC LIMIT 5"
    return execute_select_query(connexion, query)


#Pour chaque joueuse, son score minimal et son score maximal ;
def player_scores(connexion):

    query = 'SELECT Prenom, MIN(Score) AS Score_minimal, MAX(Score) AS Score_maximal FROM deroule JOIN joueuse USING(idj) GROUP BY idP, idj, Prenom'
    return execute_select_query(connexion,query)


#Parties avec le plus petit et plus grand nombre de pièces défaussées, de pièces piochées ;
def parties_placee(connexion):
    lowest_d = "SELECT idP, COUNT(*) FILTER (WHERE Placee = False) AS nb_defausees, COUNT(*) FILTER (WHERE Placee = True) AS nb_piochées \
                    FROM TOUR GROUP BY idP ORDER BY nb_defausees ASC LIMIT 1;"
    highest_d ="SELECT idP, COUNT(*) FILTER (WHERE Placee = False) AS nb_defausees, COUNT(*) FILTER (WHERE Placee = True) AS nb_piochées \
                    FROM TOUR GROUP BY idP ORDER BY nb_defausees DESC LIMIT 1;"
    
    lowest_p = "SELECT idP, COUNT(*) FILTER (WHERE Placee = False) AS nb_defausees, COUNT(*) FILTER (WHERE Placee = True) AS nb_piochées \
                    FROM TOUR GROUP BY idP ORDER BY nb_piochées ASC LIMIT 1;"
    
    highest_p = "SELECT idP, COUNT(*) FILTER (WHERE Placee = False) AS nb_defausees, COUNT(*) FILTER (WHERE Placee = True) AS nb_piochées \
                    FROM TOUR GROUP BY idP ORDER BY nb_piochées DESC LIMIT 1;"
    
    lowest_de = execute_select_query(connexion, lowest_d)
    highest_de = execute_select_query(connexion, highest_d)
    lowest_pl = execute_select_query(connexion, lowest_p)
    highest_pl = execute_select_query(connexion, highest_p)

    return {'lowest_d': lowest_de,'highest_d': highest_de, 'lowest_pl': lowest_pl, 'highest_pl': highest_pl}


#Le nombre moyen de tours, pour chaque couple (mois, année)
def avg_turn_month_year(connexion):
    
    query = "SELECT EXTRACT(YEAR FROM DATEdb) AS annee, \
            EXTRACT(MONTH FROM DATEdb) AS mois, COUNT(Numero_T)/ COUNT(DISTINCT DATE_TRUNC('month', DATEdb)) AS moyenne_tours \
            FROM TOUR GROUP BY annee, mois ORDER BY annee, mois;"

    return execute_select_query(connexion, query)    


#Top-3 des parties dans lesquelles les plus grandes pièces (longueur × largeur)

def top3_parties1(connexion):

    query = "SELECT t.idP, t.DATEdb, t.Date_F, CONCAT(MAX(pie.longueur),'x',MAX(pie.largeur)) AS taille_max, COUNT(pie.id) AS nb_pieces FROM TOUR t JOIN piece pie ON t.id = pie.id WHERE t.Placee = TRUE\
    GROUP BY t.idP, t.DATEdb, t.Date_F ORDER BY taille_max DESC, nb_pieces DESC LIMIT 3;"

    return execute_select_query(connexion,query)

def top3_parties(connexion):

    query = "SELECT t.idP AS Partie, t.idj AS Joueuse, CONCAT(MAX(p.longueur), 'x', MAX(p.largeur)) AS Taille_Max, COUNT(p.id) AS Nombre_Pieces \
    FROM TOUR t JOIN joueuse j ON t.idj = j.idj JOIN piece p ON t.id = p.id JOIN partie pr ON t.idP = pr.idP  WHERE t.Placee = TRUE \
    GROUP BY t.idP, t.idj ORDER BY MAX(p.longueur * p.largeur) DESC, COUNT(p.id) DESC LIMIT 3"

    return execute_select_query(connexion,query)

def get_random_idB(connexion):
    query = "SELECT id FROM piece WHERE longueur <= 2 OR largeur <= 2"
    return execute_select_query(connexion,query)


def get_random_brique(connexion):
    with connexion.cursor() as cursor:
        try:
            Nbrs_id = get_random_idB(connexion)
            random_idB = random.choice(Nbrs_id)[0]
            cursor.execute(
                "SELECT id, longueur, largeur, couleur FROM piece WHERE id = %s", (random_idB,))
            return cursor.fetchone() 
        except psycopg.Error as e:
            logger.error(e)
    return None
    


# Initialiser une grille avec uniquement des cases vides
def init(longueur, hauteur):
    grid = [[' ' for _ in range(longueur)] for _ in range(hauteur)]
    return grid

# Sélectionner aléatoirement une première case cible
def premier_case_cible(grid, lg, ht):
    i = random.randint(0, ht - 1)
    j = random.randint(0, lg - 1)
    grid[i][j] = 'x'
    return i, j

# Vérifier si une position est valide
def valide(i, j, grid, lg, ht):
    return 0 <= i < ht and 0 <= j < lg and grid[i][j] == ' '

# Ajouter des cases cibles
def ajouter_cases_cibles(grid, lg, ht, nb):
    direct = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Directions pour explorer
    cibles = []
    
    # Ajouter la première case cible aléatoire
    i, j = premier_case_cible(grid, lg, ht)
    cibles.append((i, j))

    # Ajouter les autres cases cibles jusqu'à ce que nous ayons le nombre désiré
    while len(cibles) < nb:
        random.shuffle(direct)  # Mélanger les directions
        ajout = False
        for dx, dy in direct:
            nx = i + dx
            ny = j + dy
            if valide(nx, ny, grid, lg, ht):
                grid[nx][ny] = 'x'
                cibles.append((nx, ny))
                i, j = nx, ny
                ajout = True
                break
        
        # Si on ne peut pas ajouter de nouvelle case cible, sortir de la boucle
        if not ajout:
            print("Impossible d'ajouter une case cible à cause des contraintes de la grille.")
            break
    
    return grid

# Calculer le nombre de cibles (entre 10% et 20% du total des cases)
def calculerNbCibles(lg, ht):
    total_cases = lg * ht
    minC = int(total_cases * 0.1)
    maxC = int(total_cases * 0.2)
    return random.randint(minC, maxC)

# Générer une grille aléatoire avec des cases cibles
def generer_grille(lg, ht):
    # Vérifier si la taille de la grille est suffisante
    if lg <= 1 or ht <= 1:
        raise ValueError("La taille de la grille doit être supérieure à 1x1.")
    
    grid = init(lg, ht)  # Initialiser la grille
    NbCibles = calculerNbCibles(lg, ht)  # Calculer le nombre de cibles à ajouter

    # Vérifier si le nombre de cibles est plus grand que le nombre total de cases
    if NbCibles > lg * ht:
        raise ValueError(f"Impossible d'ajouter {NbCibles} cibles dans une grille de {lg}x{ht}.")
    
    # Ajouter les cibles à la grille
    grid = ajouter_cases_cibles(grid, lg, ht, NbCibles)
    
    return grid