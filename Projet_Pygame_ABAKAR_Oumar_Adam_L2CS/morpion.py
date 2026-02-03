import pygame
import sys

pygame.init()

# PARAMETRES DE BASE DU JEU

# Taille de la fenêtre (largeur x hauteur)
WIDTH, HEIGHT = 600, 600

# Épaisseur des lignes
LINE_WIDTH = 10

# Nombre de cases du plateau
BOARD_ROWS = 3
BOARD_COLS = 3

# Taille d’une case
SQUARE_SIZE = WIDTH // BOARD_COLS

# Taille et épaisseur des symboles (X et O)
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = SQUARE_SIZE // 4  # espace autour du X

# Couleurs en format RGB (Rouge, Vert, Bleu)
BG_COLOR = (28, 170, 156)       # vert d’eau clair pour le fond
LINE_COLOR = (23, 145, 135)     # vert plus foncé pour les lignes
CIRCLE_COLOR = (239, 231, 200)  # beige pour le O
CROSS_COLOR = (84, 84, 84)      # gris foncé pour le X

# FENETRE PRINCIPALE
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Morpion - Multijoueur')
screen.fill(BG_COLOR)

# PLATEAU LOGIQUE (grille)
# 0 = vide, 1 = joueur 1 (O), 2 = joueur 2 (X)
board = [[0 for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

# FONCTIONS DU JEU

def draw_lines():
    """Dessine les lignes de séparation du plateau de jeu"""
    # On trace les lignes horizontales pour séparer les rangées
    pygame.draw.line(screen, LINE_COLOR, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (0, 2 * SQUARE_SIZE), (WIDTH, 2 * SQUARE_SIZE), LINE_WIDTH)
    # Et les lignes verticales pour séparer les colonnes
    pygame.draw.line(screen, LINE_COLOR, (SQUARE_SIZE, 0), (SQUARE_SIZE, HEIGHT), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (2 * SQUARE_SIZE, 0), (2 * SQUARE_SIZE, HEIGHT), LINE_WIDTH)

def draw_figures():
    """Dessine les symboles X et O sur le plateau selon l'état du jeu"""
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 1:  # Le joueur 1 joue avec des O
                # On calcule le centre de la case pour placer le cercle
                center_x = int(col * SQUARE_SIZE + SQUARE_SIZE / 2)
                center_y = int(row * SQUARE_SIZE + SQUARE_SIZE / 2)
                pygame.draw.circle(screen, CIRCLE_COLOR, (center_x, center_y), CIRCLE_RADIUS, CIRCLE_WIDTH)
            elif board[row][col] == 2:  # Le joueur 2 joue avec des X
                # Pour le X, on trace deux lignes diagonales
                # Ligne descendante
                start_desc = (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE)
                end_desc = (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE)
                pygame.draw.line(screen, CROSS_COLOR, start_desc, end_desc, CROSS_WIDTH)
                # Ligne ascendante
                start_asc = (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE)
                end_asc = (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE)
                pygame.draw.line(screen, CROSS_COLOR, start_asc, end_asc, CROSS_WIDTH)

def mark_square(row, col, player):
    """Place le symbole du joueur dans la case spécifiée"""
    board[row][col] = player

def available_square(row, col):
    """Vérifie si une case est encore libre pour jouer"""
    return board[row][col] == 0

def is_board_full():
    """Regarde si toutes les cases sont occupées, ce qui signifie égalité"""
    for row in board:
        if 0 in row:  # S'il y a au moins un zéro, c'est pas plein
            return False
    return True

def check_win(player):
    """Vérifie si le joueur donné a aligné trois symboles"""
    # Vérification des lignes horizontales
    for row in range(BOARD_ROWS):
        if board[row][0] == board[row][1] == board[row][2] == player:
            return True
    # Vérification des colonnes verticales
    for col in range(BOARD_COLS):
        if board[0][col] == board[1][col] == board[2][col] == player:
            return True
    # Vérification des diagonales
    if board[0][0] == board[1][1] == board[2][2] == player:
        return True
    if board[0][2] == board[1][1] == board[2][0] == player:
        return True
    return False

def restart():
    """Remet le plateau à zéro pour une nouvelle manche"""
    screen.fill(BG_COLOR)
    draw_lines()
    # On vide toutes les cases
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            board[row][col] = 0

def display_message(text, duration=1200):
    """Affiche un message temporaire à l'écran pendant une durée donnée"""
    font = pygame.font.SysFont(None, 50)
    label = font.render(text, True, (255, 255, 255))
    # Centre le message
    text_rect = label.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(label, text_rect)
    pygame.display.update()
    pygame.time.wait(duration)

# AFFICHAGE DU SCORE
font = pygame.font.SysFont(None, 40)

def draw_score(score1, score2, turn):
    """Affiche le score actuel et indique qui joue"""
    # On prépare le texte avec les scores et le joueur en cours
    text = f"Joueur 1 (O): {score1}  |  Joueur 2 (X): {score2}  |  Au tour de J{turn}"
    label = font.render(text, True, (255, 255, 255))
    # On place le texte en haut à gauche
    screen.blit(label, (20, 10))

# INITIALISATION DU JEU
draw_lines()
current_player = 1          # Le joueur qui joue actuellement
game_finished = False       # Devient True quand quelqu'un gagne ou égalité
score_player1 = 0           # Points du joueur 1
score_player2 = 0           # Points du joueur 2
starting_player = 1         # Qui commence la prochaine manche
winner = 0                  # Qui a gagné la manche (0 si égalité)

# BOUCLE PRINCIPALE DU JEU
while True:
    # À chaque tour, on rafraîchit l'écran
    screen.fill(BG_COLOR)
    draw_lines()
    draw_figures()
    draw_score(score_player1, score_player2, current_player)

    # On gère les événements (clics, touches, etc.)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # L'utilisateur veut quitter
            pygame.quit()
            sys.exit()

        # Si on clique avec la souris et que la partie n'est pas finie
        if event.type == pygame.MOUSEBUTTONDOWN and not game_finished:
            mouseX, mouseY = event.pos  # Où a-t-on cliqué ?

            # On calcule dans quelle case on a cliqué
            clicked_row = mouseY // SQUARE_SIZE
            clicked_col = mouseX // SQUARE_SIZE

            # Si cette case est libre, on joue
            if available_square(clicked_row, clicked_col):
                # On place le symbole du joueur actuel
                mark_square(clicked_row, clicked_col, current_player)

                # Est-ce que ce joueur vient de gagner ?
                if check_win(current_player):
                    print(f"Bravo ! Le joueur {current_player} a gagné cette manche !")
                    game_finished = True
                    winner = current_player  # On garde en mémoire qui a gagné
                    # On met à jour le score
                    if current_player == 1:
                        score_player1 += 1
                    else:
                        score_player2 += 1

                # On passe au joueur suivant
                current_player = 2 if current_player == 1 else 1

        # Si on appuie sur R, on redémarre manuellement
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            restart()
            game_finished = False
            # On change qui commence
            starting_player = 2 if starting_player == 1 else 1
            current_player = starting_player

    # Si le plateau est plein et que personne n'a gagné, c'est une égalité
    if is_board_full() and not game_finished:
        print("Égalité ! Personne ne gagne cette fois.")
        game_finished = True
        winner = 0  # Pas de gagnant

    # Si quelqu'un a gagné, on affiche un message et on prépare la prochaine manche
    if game_finished:
        # On affiche un message à l'écran
        if winner != 0:
            winner_text = f"Joueur {winner} gagne !"
        else:
            winner_text = "Égalité !"
        display_message(winner_text)
        restart()
        game_finished = False
        winner = 0  # Reset
        # On alterne le joueur qui commence
        starting_player = 2 if starting_player == 1 else 1
        current_player = starting_player

    # On met à jour l'affichage
    pygame.display.update()
