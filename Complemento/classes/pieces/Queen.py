import pygame
from Complemento.classes.Piece import Piece

class Queen(Piece):
    def __init__(self, pos, color, board):
        super().__init__(pos, color, board)
        self.notation = 'Q'
        
        # Carregar imagem da peça
        filename = f"{color[0]}_queen.png"
        self.load_image(filename, board)

    def get_possible_moves(self, board):
        """Retorna os movimentos possíveis da rainha (horizontal, vertical e diagonal)"""
        output = []

        # Movimento para o norte (para cima)
        moves_north = []
        for y in range(self.y - 1, -1, -1):
            square = board.get_square_from_pos((self.x, y))
            if square:
                moves_north.append(square)
        if moves_north:
            output.append(moves_north)

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

        # Movimento para o leste (direita)
        moves_east = []
        for x in range(self.x + 1, 8):
            square = board.get_square_from_pos((x, self.y))
            if square:
                moves_east.append(square)
        if moves_east:
            output.append(moves_east)

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

        # Movimento para o sul (para baixo)
        moves_south = []
        for y in range(self.y + 1, 8):
            square = board.get_square_from_pos((self.x, y))
            if square:
                moves_south.append(square)
        if moves_south:
            output.append(moves_south)

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

        # Movimento para o oeste (esquerda)
        moves_west = []
        for x in range(self.x - 1, -1, -1):
            square = board.get_square_from_pos((x, self.y))
            if square:
                moves_west.append(square)
        if moves_west:
            output.append(moves_west)

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