import pygame
from Complemento.classes.Piece import Piece

class King(Piece):
    def __init__(self, pos, color, board):
        super().__init__(pos, color, board)
        self.notation = 'K'
        
        # Carregar imagem da peça
        filename = f"{color[0]}_king.png"
        self.load_image(filename, board)

    def get_possible_moves(self, board):
        """Retorna os movimentos possíveis do rei (uma casa em qualquer direção)"""
        output = []
        
        # Todos os movimentos possíveis do rei (uma casa em cada direção)
        king_moves = [
            (0, -1),   # norte (cima)
            (1, -1),   # nordeste
            (1, 0),    # leste (direita)
            (1, 1),    # sudeste
            (0, 1),    # sul (baixo)
            (-1, 1),   # sudoeste
            (-1, 0),   # oeste (esquerda)
            (-1, -1),  # noroeste
        ]

        for move in king_moves:
            new_x = self.x + move[0]
            new_y = self.y + move[1]
            
            # Verificar se a nova posição está dentro do tabuleiro
            if 0 <= new_x < 8 and 0 <= new_y < 8:
                square = board.get_square_from_pos((new_x, new_y))
                if square:
                    # Cada movimento do rei é independente
                    output.append([square])

        return output

    def can_castle(self, board):
        """Verifica se o rei pode fazer roque"""
        if self.has_moved:
            return None

        # Verificar roque para peças brancas
        if self.color == 'white':
            # Roque longo (queenside)
            queenside_rook = board.get_piece_from_pos((0, 7))
            if (queenside_rook is not None and 
                queenside_rook.notation == 'R' and 
                not queenside_rook.has_moved):
                # Verificar se as casas entre o rei e a torre estão vazias
                empty_squares = [
                    board.get_piece_from_pos((1, 7)),
                    board.get_piece_from_pos((2, 7)),
                    board.get_piece_from_pos((3, 7))
                ]
                if all(piece is None for piece in empty_squares):
                    # Verificar se o rei não está em xeque e não passará por xeque
                    if (not board.is_in_check(self.color) and
                        not board.is_in_check(self.color, board_change=[self.pos, (2, 7)]) and
                        not board.is_in_check(self.color, board_change=[self.pos, (3, 7)])):
                        return 'queenside'
            
            # Roque curto (kingside)
            kingside_rook = board.get_piece_from_pos((7, 7))
            if (kingside_rook is not None and 
                kingside_rook.notation == 'R' and 
                not kingside_rook.has_moved):
                # Verificar se as casas entre o rei e a torre estão vazias
                empty_squares = [
                    board.get_piece_from_pos((5, 7)),
                    board.get_piece_from_pos((6, 7))
                ]
                if all(piece is None for piece in empty_squares):
                    # Verificar se o rei não está em xeque e não passará por xeque
                    if (not board.is_in_check(self.color) and
                        not board.is_in_check(self.color, board_change=[self.pos, (5, 7)]) and
                        not board.is_in_check(self.color, board_change=[self.pos, (6, 7)])):
                        return 'kingside'

        # Verificar roque para peças pretas
        elif self.color == 'black':
            # Roque longo (queenside)
            queenside_rook = board.get_piece_from_pos((0, 0))
            if (queenside_rook is not None and 
                queenside_rook.notation == 'R' and 
                not queenside_rook.has_moved):
                # Verificar se as casas entre o rei e a torre estão vazias
                empty_squares = [
                    board.get_piece_from_pos((1, 0)),
                    board.get_piece_from_pos((2, 0)),
                    board.get_piece_from_pos((3, 0))
                ]
                if all(piece is None for piece in empty_squares):
                    # Verificar se o rei não está em xeque e não passará por xeque
                    if (not board.is_in_check(self.color) and
                        not board.is_in_check(self.color, board_change=[self.pos, (2, 0)]) and
                        not board.is_in_check(self.color, board_change=[self.pos, (3, 0)])):
                        return 'queenside'
            
            # Roque curto (kingside)
            kingside_rook = board.get_piece_from_pos((7, 0))
            if (kingside_rook is not None and 
                kingside_rook.notation == 'R' and 
                not kingside_rook.has_moved):
                # Verificar se as casas entre o rei e a torre estão vazias
                empty_squares = [
                    board.get_piece_from_pos((5, 0)),
                    board.get_piece_from_pos((6, 0))
                ]
                if all(piece is None for piece in empty_squares):
                    # Verificar se o rei não está em xeque e não passará por xeque
                    if (not board.is_in_check(self.color) and
                        not board.is_in_check(self.color, board_change=[self.pos, (5, 0)]) and
                        not board.is_in_check(self.color, board_change=[self.pos, (6, 0)])):
                        return 'kingside'

        return None

    def get_valid_moves(self, board):
        """Retorna movimentos válidos incluindo roque"""
        output = []
        
        # Movimentos normais do rei
        for square in self.get_moves(board):
            if not board.is_in_check(self.color, board_change=[self.pos, square.pos]):
                output.append(square)

        # Adicionar movimentos de roque se possível
        castle_type = self.can_castle(board)
        if castle_type == 'queenside':
            castle_square = board.get_square_from_pos((self.x - 2, self.y))
            if castle_square:
                output.append(castle_square)
        elif castle_type == 'kingside':
            castle_square = board.get_square_from_pos((self.x + 2, self.y))
            if castle_square:
                output.append(castle_square)

        return output