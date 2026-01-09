import pygame
from Complemento.classes.Piece import Piece

class Bishop(Piece):
    def __init__(self, pos, color, board):
        super().__init__(pos, color, board)
        self.notation = 'B'
        
        # Carregar imagem da peça
        filename = f"{color[0]}_bishop.png"
        self.load_image(filename, board)

    def get_possible_moves(self, board):
        """Retorna os movimentos possíveis do bispo (diagonais)"""
        output = []

        # Diagonal nordeste (cima-direita)
        moves_ne = []
        for i in range(1, 8):
            new_x, new_y = self.x + i, self.y - i
            if new_x > 7 or new_y < 0:
                break
            square = board.get_square_from_pos((new_x, new_y))
            if square:
                moves_ne.append(square)
        if moves_ne:
            output.append(moves_ne)

        # Diagonal sudeste (baixo-direita)
        moves_se = []
        for i in range(1, 8):
            new_x, new_y = self.x + i, self.y + i
            if new_x > 7 or new_y > 7:
                break
            square = board.get_square_from_pos((new_x, new_y))
            if square:
                moves_se.append(square)
        if moves_se:
            output.append(moves_se)

        # Diagonal sudoeste (baixo-esquerda)
        moves_sw = []
        for i in range(1, 8):
            new_x, new_y = self.x - i, self.y + i
            if new_x < 0 or new_y > 7:
                break
            square = board.get_square_from_pos((new_x, new_y))
            if square:
                moves_sw.append(square)
        if moves_sw:
            output.append(moves_sw)

        # Diagonal noroeste (cima-esquerda)
        moves_nw = []
        for i in range(1, 8):
            new_x, new_y = self.x - i, self.y - i
            if new_x < 0 or new_y < 0:
                break
            square = board.get_square_from_pos((new_x, new_y))
            if square:
                moves_nw.append(square)
        if moves_nw:
            output.append(moves_nw)

        return output