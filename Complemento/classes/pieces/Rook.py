import pygame
from Complemento.classes.Piece import Piece

class Rook(Piece):
    def __init__(self, pos, color, board):
        super().__init__(pos, color, board)
        self.notation = 'R'
        
        # Carregar imagem da peça
        filename = f"{color[0]}_rook.png"
        self.load_image(filename, board)

    def get_possible_moves(self, board):
        """Retorna os movimentos possíveis da torre (horizontal e vertical)"""
        output = []

        # Movimento para o norte (para cima)
        moves_north = []
        for y in range(self.y - 1, -1, -1):  # De y-1 até 0
            square = board.get_square_from_pos((self.x, y))
            if square:
                moves_north.append(square)
        if moves_north:
            output.append(moves_north)

        # Movimento para o leste (direita)
        moves_east = []
        for x in range(self.x + 1, 8):
            square = board.get_square_from_pos((x, self.y))
            if square:
                moves_east.append(square)
        if moves_east:
            output.append(moves_east)

        # Movimento para o sul (para baixo)
        moves_south = []
        for y in range(self.y + 1, 8):
            square = board.get_square_from_pos((self.x, y))
            if square:
                moves_south.append(square)
        if moves_south:
            output.append(moves_south)

        # Movimento para o oeste (esquerda)
        moves_west = []
        for x in range(self.x - 1, -1, -1):  # De x-1 até 0
            square = board.get_square_from_pos((x, self.y))
            if square:
                moves_west.append(square)
        if moves_west:
            output.append(moves_west)

        return output