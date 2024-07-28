import pygame
import os

# Initialize Pygame
pygame.init()

# Constants for the board size
WIDTH, HEIGHT = 800, 800
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS

# Initialize the Text field
pygame.font.init()  # Initialize the font module
font = pygame.font.SysFont('Arial', 24)  # You can choose another font and size

# Load images
def load_images():
    pieces = ["rook", "knight", "bishop", "queen", "king", "pawn"]
    colors = ["b", "w"]
    images = {}
    for piece in pieces:
        for color in colors:
            image_path = os.path.join("images", f"{color}_{piece}.png")
            images[f"{color}_{piece}"] = pygame.transform.scale(
                pygame.image.load(image_path),
                (SQUARE_SIZE, SQUARE_SIZE)
            )
    return images

def display_turn(win, turn, game_over):
    if game_over:
        text = "Game Over"
    else:
        text = "White's Turn" if turn else "Black's Turn"
    text_surface = font.render(text, True, (0, 0, 0))  # Black text
    win.blit(text_surface, (10, HEIGHT - 30))

# Set up the display
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Chess')

def draw_board(win, check_position=None):
    win.fill(pygame.Color("white"))
    for row in range(ROWS):
        for col in range(COLS):
            color = pygame.Color("gray")
            if (row + col) % 2 == 0:
                color = pygame.Color("white")
            if (row, col) == check_position:
                color = pygame.Color("red")
            pygame.draw.rect(win, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def create_initial_board_layout():
    # Define the layout of the chess pieces on the board
    return [
        ["b_rook", "b_knight", "b_bishop", "b_queen", "b_king", "b_bishop", "b_knight", "b_rook"],
        ["b_pawn"] * 8,
        [None] * 8,
        [None] * 8,
        [None] * 8,
        [None] * 8,
        ["w_pawn"] * 8,
        ["w_rook", "w_knight", "w_bishop", "w_queen", "w_king", "w_bishop", "w_knight", "w_rook"]
    ]

def draw_pieces(win, images, board_layout):
# Draw the pieces on the board according to board_layout
    for row in range(8):
        for col in range(8):
            piece = board_layout[row][col]
            if piece:
                win.blit(images[piece], (col * SQUARE_SIZE, row * SQUARE_SIZE))
def get_square_from_pos(pos):
    """Converts screen position to board position (row, col)"""
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

def get_piece_at_pos(pos, board_layout):
    """Returns the piece at the given position, if any"""
    row, col = get_square_from_pos(pos)
    if 0 <= row < 8 and 0 <= col < 8:
        return board_layout[row][col]
    return None

def is_legal_move(start_pos, end_pos, piece, board_layout):
    start_row, start_col = start_pos
    end_row, end_col = end_pos
    move_row, move_col = end_row - start_row, end_col - start_col

    if piece == "w_pawn":
        # Normal move
        if start_col == end_col and board_layout[end_row][end_col] is None:
            if start_row == 6 and move_row == -2 and board_layout[start_row - 1][start_col] is None:
                return True  # Allows initial two-square move
            if move_row == -1:
                return True

        # Capturing move
        if abs(move_col) == 1 and move_row == -1 and board_layout[end_row][end_col] is not None and board_layout[end_row][end_col].startswith('b_'):
            return True

    elif piece == "b_pawn":
        # Normal move
        if start_col == end_col and board_layout[end_row][end_col] is None:
            if start_row == 1 and move_row == 2 and board_layout[start_row + 1][start_col] is None:
                return True  # Allows initial two-square move
            if move_row == 1:
                return True

        # Capturing move
        if abs(move_col) == 1 and move_row == 1 and board_layout[end_row][end_col] is not None and board_layout[end_row][end_col].startswith('w_'):
            return True
    if piece in ["w_rook", "b_rook"]:
        # Rook moves either horizontally or vertically
        if start_row == end_row or start_col == end_col:
            step_row = 1 if end_row > start_row else -1 if end_row < start_row else 0
            step_col = 1 if end_col > start_col else -1 if end_col < start_col else 0

            cur_row, cur_col = start_row + step_row, start_col + step_col
            while (cur_row, cur_col) != (end_row, end_col):
                if board_layout[cur_row][cur_col] is not None:
                    return False
                cur_row += step_row
                cur_col += step_col
            if board_layout[end_row][end_col] is not None:
                if (piece.startswith('w') and board_layout[end_row][end_col].startswith('w')) or \
                        (piece.startswith('b') and board_layout[end_row][end_col].startswith('b')):
                    return False

            return True

    if piece in ["w_knight", "b_knight"]:
        # Knights move in an L-shape: 2 squares in one direction and 1 square perpendicular
        if (abs(move_row) == 2 and abs(move_col) == 1) or (abs(move_row) == 1 and abs(move_col) == 2):
            # Check if the destination square is either empty or contains an opponent's piece
            if board_layout[end_row][end_col] is None or \
                    (piece.startswith('w') and board_layout[end_row][end_col].startswith('b')) or \
                    (piece.startswith('b') and board_layout[end_row][end_col].startswith('w')):
                return True
            # If the destination square contains a piece of the same color, the move is illegal
            elif (piece.startswith('w') and board_layout[end_row][end_col].startswith('w')) or \
                 (piece.startswith('b') and board_layout[end_row][end_col].startswith('b')):
                return False

    if piece in ["w_bishop", "b_bishop"]:
        # Bishops move diagonally
        if abs(move_row) == abs(move_col):
            step_row = 1 if end_row > start_row else -1
            step_col = 1 if end_col > start_col else -1

            cur_row, cur_col = start_row + step_row, start_col + step_col
            while (cur_row, cur_col) != (end_row, end_col):
                if board_layout[cur_row][cur_col] is not None:
                    # There's a piece in the way
                    return False
                cur_row += step_row
                cur_col += step_col

            # Check if the end square contains a piece of the same color
            if board_layout[end_row][end_col] is not None:
                if (piece.startswith('w') and board_layout[end_row][end_col].startswith('w')) or \
                        (piece.startswith('b') and board_layout[end_row][end_col].startswith('b')):
                    return False

            return True

    if piece in ["w_queen", "b_queen"]:
        # Queen moves like both a rook and a bishop
        if start_row == end_row or start_col == end_col or abs(move_row) == abs(move_col):
            step_row = 1 if end_row > start_row else -1 if end_row < start_row else 0
            step_col = 1 if end_col > start_col else -1 if end_col < start_col else 0

            cur_row, cur_col = start_row + step_row, start_col + step_col
            while (cur_row, cur_col) != (end_row, end_col):
                if board_layout[cur_row][cur_col] is not None:
                    # There's a piece in the way
                    return False
                cur_row += step_row
                cur_col += step_col

            # Check if the end square contains a piece of the same color
            if board_layout[end_row][end_col] is not None:
                if (piece.startswith('w') and board_layout[end_row][end_col].startswith('w')) or \
                        (piece.startswith('b') and board_layout[end_row][end_col].startswith('b')):
                    return False

            return True

    if piece in ["w_king", "b_king"]:
        # King moves one square in any direction
        if abs(move_row) <= 1 and abs(move_col) <= 1:
            # Check if the end square is either empty or contains an opponent's piece
            if board_layout[end_row][end_col] is None or \
                    (piece.startswith('w') and board_layout[end_row][end_col].startswith('b')) or \
                    (piece.startswith('b') and board_layout[end_row][end_col].startswith('w')):
                return True
            # If the destination square contains a piece of the same color, the move is illegal
            elif (piece.startswith('w') and board_layout[end_row][end_col].startswith('w')) or \
                    (piece.startswith('b') and board_layout[end_row][end_col].startswith('b')):
                return False

    return False

def move_piece(selected_piece, start_pos, end_pos, board_layout):
    start_row, start_col = get_square_from_pos(start_pos)
    end_row, end_col = get_square_from_pos(end_pos)

    if is_legal_move((start_row, start_col), (end_row, end_col), selected_piece, board_layout):
        print("Before move:")  # Debug
        for row in board_layout:
            print(row)

        board_layout[end_row][end_col], board_layout[start_row][start_col] = selected_piece, None
        print("After move:")  # Debug
        for row in board_layout:
            print(row)

        return True


    return False


def get_king_position(board_layout, color):
    king_piece = color + "_king"
    for row in range(8):
        for col in range(8):
            if board_layout[row][col] == king_piece:
                return (row, col)
    return None

def is_in_check(king_position, board_layout, opponent_color_prefix):
    for row in range(8):
        for col in range(8):
            piece = board_layout[row][col]
            if piece and piece.startswith(opponent_color_prefix):
                if is_legal_move((row, col), king_position, piece, board_layout):
                    return True
    return False

def generate_all_legal_moves(board_layout, player_color):
    legal_moves = []
    for row in range(8):
        for col in range(8):
            piece = board_layout[row][col]
            if piece and piece.startswith(player_color):
                for dest_row in range(8):
                    for dest_col in range(8):
                        if is_legal_move((row, col), (dest_row, dest_col), piece, board_layout):
                            legal_moves.append(((row, col), (dest_row, dest_col)))
    return legal_moves

def is_game_over(board_layout):
    white_king_present = any("w_king" in row for row in board_layout)
    black_king_present = any("b_king" in row for row in board_layout)
    return not (white_king_present and black_king_present)

def main():
    clock = pygame.time.Clock()
    images = load_images()
    board_layout = create_initial_board_layout()
    selected_piece = None
    selected_pos = None
    white_turn = True  # Track turns, start with White
    check_position = None  # Initialize check_position
    game_over = False

    run = True
    while run:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                pos = pygame.mouse.get_pos()
                if not selected_piece:
                    # Logic to select a piece
                    selected_pos = pos
                    row, col = get_square_from_pos(selected_pos)
                    if board_layout[row][col] and \
                            ((white_turn and board_layout[row][col].startswith('w')) or
                             (not white_turn and board_layout[row][col].startswith('b'))):
                        selected_piece = board_layout[row][col]
                else:
                    # Attempt to move the piece
                    new_pos = pos
                    move_made = move_piece(selected_piece, selected_pos, new_pos, board_layout)
                    if move_made:
                        white_turn = not white_turn
                        selected_piece = None
                        # Check for game over
                        game_over = is_game_over(board_layout)
                        if game_over:
                            print("Game Over")
                            break

        # After any move, check if either king is in check
        for color in ['w', 'b']:
            king_pos = get_king_position(board_layout, color)
            if king_pos and is_in_check(king_pos, board_layout, 'b' if color == 'w' else 'w'):
                check_position = king_pos
                break
        else:
            check_position = None

        # Draw the board and pieces
        draw_board(WIN, check_position)
        draw_pieces(WIN, images, board_layout)
        display_turn(WIN, white_turn, game_over)
        pygame.display.update()

    pygame.quit()

main()