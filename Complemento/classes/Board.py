import pygame
import os

from Complemento.classes.Square import Square
from Complemento.classes.pieces.Rook import Rook
from Complemento.classes.pieces.Bishop import Bishop
from Complemento.classes.pieces.Knight import Knight
from Complemento.classes.pieces.Queen import Queen
from Complemento.classes.pieces.King import King
from Complemento.classes.pieces.Pawn import Pawn

class Board:
    IMAGE_DIR = None
    
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.square_width = width // 8
        self.square_height = height // 8
        self.selected_piece = None
        self.turn = 'white'
        self.move_history = []
        self.captured_pieces = {'white': [], 'black': []}

        # Configuração inicial do tabuleiro
        self.config = [
            ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
            ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
            ['', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', ''],
            ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
            ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR'],
        ]

        self.squares = self.generate_squares()
        self.setup_board()

    def generate_squares(self):
        """Gera todos os quadrados do tabuleiro"""
        output = []
        for y in range(8):
            for x in range(8):
                output.append(
                    Square(
                        x, y,
                        self.square_width,
                        self.square_height
                    )
                )
        return output

    def setup_board(self):
        """Configura as peças iniciais no tabuleiro"""
        for y, row in enumerate(self.config):
            for x, piece in enumerate(row):
                if piece != '':
                    square = self.get_square_from_pos((x, y))
                    color = 'white' if piece[0] == 'w' else 'black'
                    
                    piece_type = piece[1]
                    
                    try:
                        if piece_type == 'R':
                            square.occupying_piece = Rook((x, y), color, self)
                        elif piece_type == 'N':
                            square.occupying_piece = Knight((x, y), color, self)
                        elif piece_type == 'B':
                            square.occupying_piece = Bishop((x, y), color, self)
                        elif piece_type == 'Q':
                            square.occupying_piece = Queen((x, y), color, self)
                        elif piece_type == 'K':
                            square.occupying_piece = King((x, y), color, self)
                        elif piece_type == 'P':
                            square.occupying_piece = Pawn((x, y), color, self)
                    except Exception as e:
                        print(f"Erro ao criar peça {piece} na posição ({x}, {y}): {e}")

    def handle_click(self, mx, my):
        """Manipula os cliques do mouse no tabuleiro"""
        x = mx // self.square_width
        y = my // self.square_height
        
        # Verificar se o clique está dentro do tabuleiro
        if x < 0 or x >= 8 or y < 0 or y >= 8:
            return
            
        clicked_square = self.get_square_from_pos((x, y))

        if self.selected_piece is None:
            # Selecionar uma peça
            if clicked_square.occupying_piece is not None:
                if clicked_square.occupying_piece.color == self.turn:
                    self.selected_piece = clicked_square.occupying_piece
        else:
            # Tentar mover a peça selecionada
            if self.selected_piece.move(self, clicked_square):
                # Movimento bem-sucedido, alternar turno
                self.turn = 'white' if self.turn == 'black' else 'black'
                self.selected_piece = None
            elif clicked_square.occupying_piece is not None:
                # Selecionar outra peça da mesma cor
                if clicked_square.occupying_piece.color == self.turn:
                    self.selected_piece = clicked_square.occupying_piece
                else:
                    self.selected_piece = None
            else:
                # Desselecionar
                self.selected_piece = None

    def is_in_check(self, color, board_change=None):
        """Verifica se o rei da cor especificada está em xeque"""
        output = False
        king_pos = None

        # Simular mudança no tabuleiro se especificada
        changing_piece = None
        old_square = None
        new_square = None
        new_square_old_piece = None

        if board_change is not None:
            # Encontrar a peça que está se movendo
            for square in self.squares:
                if square.pos == board_change[0]:
                    changing_piece = square.occupying_piece
                    old_square = square
                    old_square.occupying_piece = None
                    break
            
            # Encontrar o quadrado de destino
            for square in self.squares:
                if square.pos == board_change[1]:
                    new_square = square
                    new_square_old_piece = new_square.occupying_piece
                    new_square.occupying_piece = changing_piece
                    break

        # Encontrar todas as peças no tabuleiro
        pieces = [
            square.occupying_piece for square in self.squares 
            if square.occupying_piece is not None
        ]

        # Encontrar a posição do rei
        if changing_piece is not None and changing_piece.notation == 'K':
            king_pos = new_square.pos
        else:
            for piece in pieces:
                if piece.notation == 'K' and piece.color == color:
                    king_pos = piece.pos
                    break

        # Verificar se alguma peça inimiga está atacando o rei
        if king_pos is not None:
            for piece in pieces:
                if piece.color != color:
                    try:
                        attacking_squares = piece.attacking_squares(self)
                        for square in attacking_squares:
                            if square.pos == king_pos:
                                output = True
                                break
                    except:
                        continue
                if output:
                    break

        # Reverter mudanças temporárias
        if board_change is not None:
            old_square.occupying_piece = changing_piece
            new_square.occupying_piece = new_square_old_piece

        return output

    def is_in_checkmate(self, color):
        """Verifica se a cor especificada está em xeque-mate"""
        # Encontrar o rei
        king = None
        for square in self.squares:
            if (square.occupying_piece is not None and 
                square.occupying_piece.notation == 'K' and 
                square.occupying_piece.color == color):
                king = square.occupying_piece
                break

        if king is None:
            return False

        # Verificar se o rei tem movimentos válidos
        if len(king.get_valid_moves(self)) > 0:
            return False

        # Verificar se alguma outra peça pode fazer um movimento válido
        for square in self.squares:
            if (square.occupying_piece is not None and 
                square.occupying_piece.color == color):
                if len(square.occupying_piece.get_valid_moves(self)) > 0:
                    return False

        # Se não há movimentos válidos e está em xeque, é xeque-mate
        return self.is_in_check(color)

    def get_square_from_pos(self, pos):
        """Retorna o quadrado na posição especificada"""
        for square in self.squares:
            if (square.x, square.y) == (pos[0], pos[1]):
                return square
        return None

    def get_piece_from_pos(self, pos):
        """Retorna a peça na posição especificada"""
        square = self.get_square_from_pos(pos)
        return square.occupying_piece if square else None

    def draw_coordinates(self, display):
        """Desenha as coordenadas do tabuleiro (a-h e 1-8)"""
        font = pygame.font.Font(None, 24)
        coord_color = (80, 80, 80)
        
        # Colunas (a-h) - na parte inferior e superior
        columns = 'abcdefgh'
        for i, col in enumerate(columns):
            x_pos = i * self.square_width + self.square_width // 2
            
            # Coordenada na parte inferior
            col_surface = font.render(col, True, coord_color)
            col_rect = col_surface.get_rect(center=(x_pos, self.height + 15))
            display.blit(col_surface, col_rect)
            
            # Coordenada na parte superior
            col_rect_top = col_surface.get_rect(center=(x_pos, -20))
            display.blit(col_surface, col_rect_top)
        
        # Fileiras (1-8) - nas laterais esquerda e direita
        for i in range(8):
            row_number = str(8 - i)  # Inverter para mostrar 8 no topo e 1 embaixo
            y_pos = i * self.square_height + self.square_height // 2
            
            # Coordenada na lateral esquerda
            row_surface = font.render(row_number, True, coord_color)
            row_rect = row_surface.get_rect(center=(-15, y_pos))
            display.blit(row_surface, row_rect)
            
            # Coordenada na lateral direita
            row_rect_right = row_surface.get_rect(center=(self.width + 15, y_pos))
            display.blit(row_surface, row_rect_right)

    def draw(self, display):
        """Desenha o tabuleiro na tela"""
        # Limpar highlights anteriores
        for square in self.squares:
            square.highlight = False

        # Destacar peça selecionada e movimentos válidos
        if self.selected_piece is not None:
            selected_square = self.get_square_from_pos(self.selected_piece.pos)
            if selected_square:
                selected_square.highlight = True
                
            # Destacar movimentos válidos
            valid_moves = self.selected_piece.get_valid_moves(self)
            for square in valid_moves:
                square.highlight = True

        # Desenhar todos os quadrados
        for square in self.squares:
            square.draw(display)

        # Desenhar as coordenadas do tabuleiro
        self.draw_coordinates(display)

        # Desenhar borda do tabuleiro
        pygame.draw.rect(display, (60, 60, 60), (0, 0, self.width, self.height), 3)