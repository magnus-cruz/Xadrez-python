import pygame
from Complemento.classes.Piece import Piece

class Pawn(Piece):
    def __init__(self, pos, color, board):
        super().__init__(pos, color, board)
        self.notation = 'P'
        
        # Carregar imagem da peça
        filename = f"{color[0]}_pawn.png"
        self.load_image(filename, board)

    def get_possible_moves(self, board):
        """Retorna os movimentos possíveis do peão (apenas para frente)"""
        output = []
        moves = []

        # Movimento para frente
        if self.color == 'white':
            moves.append((0, -1))  # Uma casa para frente
            if not self.has_moved:
                moves.append((0, -2))  # Duas casas no primeiro movimento
        elif self.color == 'black':
            moves.append((0, 1))   # Uma casa para frente
            if not self.has_moved:
                moves.append((0, 2))   # Duas casas no primeiro movimento

        for move in moves:
            new_pos = (self.x + move[0], self.y + move[1])
            if 0 <= new_pos[1] < 8:  # Verificar se está dentro do tabuleiro
                square = board.get_square_from_pos(new_pos)
                if square:
                    output.append([square])  # Retornar como lista de listas

        return output

    def get_moves(self, board):
        """Retorna todos os movimentos válidos do peão (frente + capturas)"""
        output = []
        
        # Movimentos para frente (sem captura)
        for direction in self.get_possible_moves(board):
            for square in direction:
                if square.occupying_piece is not None:
                    break  # Parar se houver peça no caminho
                else:
                    output.append(square)

        # Movimentos de captura (diagonais)
        capture_moves = []
        
        if self.color == 'white':
            # Capturas para brancas (diagonais para cima)
            if self.x + 1 < 8 and self.y - 1 >= 0:
                capture_moves.append((self.x + 1, self.y - 1))
            if self.x - 1 >= 0 and self.y - 1 >= 0:
                capture_moves.append((self.x - 1, self.y - 1))
        elif self.color == 'black':
            # Capturas para pretas (diagonais para baixo)
            if self.x + 1 < 8 and self.y + 1 < 8:
                capture_moves.append((self.x + 1, self.y + 1))
            if self.x - 1 >= 0 and self.y + 1 < 8:
                capture_moves.append((self.x - 1, self.y + 1))

        # Verificar capturas
        for pos in capture_moves:
            square = board.get_square_from_pos(pos)
            if square and square.occupying_piece is not None:
                if square.occupying_piece.color != self.color:
                    output.append(square)

        return output

    def attacking_squares(self, board):
        """Retorna os quadrados que o peão está atacando (apenas diagonais)"""
        attacking = []
        
        if self.color == 'white':
            # Ataques para brancas (diagonais para cima)
            positions = [(self.x + 1, self.y - 1), (self.x - 1, self.y - 1)]
        else:
            # Ataques para pretas (diagonais para baixo)
            positions = [(self.x + 1, self.y + 1), (self.x - 1, self.y + 1)]

        for pos in positions:
            if 0 <= pos[0] < 8 and 0 <= pos[1] < 8:
                square = board.get_square_from_pos(pos)
                if square:
                    attacking.append(square)

        return attacking