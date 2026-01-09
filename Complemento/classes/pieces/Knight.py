import pygame
from Complemento.classes.Piece import Piece

class Knight(Piece):
    def __init__(self, pos, color, board):
        super().__init__(pos, color, board)
        self.notation = 'N'
        
        # Carregar imagem da peça
        filename = f"{color[0]}_knight.png"
        self.load_image(filename, board)

    def get_possible_moves(self, board):
        """Retorna os movimentos possíveis do cavalo (em L)"""
        output = []
        
        # Todos os movimentos possíveis do cavalo (em L)
        knight_moves = [
            (1, -2),   # 1 direita, 2 cima
            (2, -1),   # 2 direita, 1 cima
            (2, 1),    # 2 direita, 1 baixo
            (1, 2),    # 1 direita, 2 baixo
            (-1, 2),   # 1 esquerda, 2 baixo
            (-2, 1),   # 2 esquerda, 1 baixo
            (-2, -1),  # 2 esquerda, 1 cima
            (-1, -2)   # 1 esquerda, 2 cima
        ]

        for move in knight_moves:
            new_x = self.x + move[0]
            new_y = self.y + move[1]
            
            # Verificar se a nova posição está dentro do tabuleiro
            if 0 <= new_x < 8 and 0 <= new_y < 8:
                square = board.get_square_from_pos((new_x, new_y))
                if square:
                    # Cada movimento do cavalo é independente, então cada um vai em sua própria lista
                    output.append([square])

        return output