import pygame
import math
from collections import Counter

class ChessAnalyzer:
    def __init__(self, board):
        self.board = board
        self.piece_values = {
            'P': 1,
            'N': 3,
            'B': 3,
            'R': 5,
            'Q': 9,
            'K': 100
        }
        # Valores posicionais para cada tipo de peça
        self.position_values = {
            'P': [  # Peões
                [0, 0, 0, 0, 0, 0, 0, 0],
                [5, 5, 5, 5, 5, 5, 5, 5],
                [1, 1, 2, 3, 3, 2, 1, 1],
                [0.5, 0.5, 1, 2.5, 2.5, 1, 0.5, 0.5],
                [0, 0, 0, 2, 2, 0, 0, 0],
                [0.5, -0.5, -1, 0, 0, -1, -0.5, 0.5],
                [0.5, 1, 1, -2, -2, 1, 1, 0.5],
                [0, 0, 0, 0, 0, 0, 0, 0]
            ],
            'N': [  # Cavalos
                [-5, -4, -3, -3, -3, -3, -4, -5],
                [-4, -2, 0, 0, 0, 0, -2, -4],
                [-3, 0, 1, 1.5, 1.5, 1, 0, -3],
                [-3, 0.5, 1.5, 2, 2, 1.5, 0.5, -3],
                [-3, 0, 1.5, 2, 2, 1.5, 0, -3],
                [-3, 0.5, 1, 1.5, 1.5, 1, 0.5, -3],
                [-4, -2, 0, 0.5, 0.5, 0, -2, -4],
                [-5, -4, -3, -3, -3, -3, -4, -5]
            ],
            'B': [  # Bispos
                [-2, -1, -1, -1, -1, -1, -1, -2],
                [-1, 0, 0, 0, 0, 0, 0, -1],
                [-1, 0, 0.5, 1, 1, 0.5, 0, -1],
                [-1, 0.5, 0.5, 1, 1, 0.5, 0.5, -1],
                [-1, 0, 1, 1, 1, 1, 0, -1],
                [-1, 1, 1, 1, 1, 1, 1, -1],
                [-1, 0.5, 0, 0, 0, 0, 0.5, -1],
                [-2, -1, -1, -1, -1, -1, -1, -2]
            ],
            'R': [  # Torres
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0.5, 1, 1, 1, 1, 1, 1, 0.5],
                [-0.5, 0, 0, 0, 0, 0, 0, -0.5],
                [-0.5, 0, 0, 0, 0, 0, 0, -0.5],
                [-0.5, 0, 0, 0, 0, 0, 0, -0.5],
                [-0.5, 0, 0, 0, 0, 0, 0, -0.5],
                [-0.5, 0, 0, 0, 0, 0, 0, -0.5],
                [0, 0, 0, 0.5, 0.5, 0, 0, 0]
            ],
            'Q': [  # Rainha
                [-2, -1, -1, -0.5, -0.5, -1, -1, -2],
                [-1, 0, 0, 0, 0, 0, 0, -1],
                [-1, 0, 0.5, 0.5, 0.5, 0.5, 0, -1],
                [-0.5, 0, 0.5, 0.5, 0.5, 0.5, 0, -0.5],
                [0, 0, 0.5, 0.5, 0.5, 0.5, 0, -0.5],
                [-1, 0.5, 0.5, 0.5, 0.5, 0.5, 0, -1],
                [-1, 0, 0.5, 0, 0, 0, 0, -1],
                [-2, -1, -1, -0.5, -0.5, -1, -1, -2]
            ],
            'K': [  # Rei
                [-3, -4, -4, -5, -5, -4, -4, -3],
                [-3, -4, -4, -5, -5, -4, -4, -3],
                [-3, -4, -4, -5, -5, -4, -4, -3],
                [-3, -4, -4, -5, -5, -4, -4, -3],
                [-2, -3, -3, -4, -4, -3, -3, -2],
                [-1, -2, -2, -2, -2, -2, -2, -1],
                [2, 2, 0, 0, 0, 0, 2, 2],
                [2, 3, 1, 0, 0, 1, 3, 2]
            ]
        }

    def evaluate_position(self):
        """Avalia a posição atual e retorna um score (positivo favorece brancas)"""
        white_score = 0
        black_score = 0
        
        for square in self.board.squares:
            if square.occupying_piece is not None:
                piece = square.occupying_piece
                piece_value = self.piece_values[piece.notation]
                
                # Valor posicional
                if piece.color == 'white':
                    pos_value = self.position_values[piece.notation][7 - piece.y][piece.x]
                else:
                    pos_value = self.position_values[piece.notation][piece.y][piece.x]
                
                total_value = piece_value + (pos_value * 0.1)
                
                if piece.color == 'white':
                    white_score += total_value
                else:
                    black_score += total_value
        
        # Bônus por mobilidade (número de movimentos válidos)
        white_mobility = self.count_valid_moves('white')
        black_mobility = self.count_valid_moves('black')
        
        mobility_bonus = (white_mobility - black_mobility) * 0.1
        
        return white_score - black_score + mobility_bonus

    def count_valid_moves(self, color):
        """Conta o número total de movimentos válidos para uma cor"""
        moves = 0
        for square in self.board.squares:
            if (square.occupying_piece is not None and 
                square.occupying_piece.color == color):
                moves += len(square.occupying_piece.get_valid_moves(self.board))
        return moves

    def get_piece_count(self):
        """Retorna a contagem de peças para cada cor"""
        white_pieces = {}
        black_pieces = {}
        
        for square in self.board.squares:
            if square.occupying_piece is not None:
                piece = square.occupying_piece
                notation = piece.notation
                
                if piece.color == 'white':
                    white_pieces[notation] = white_pieces.get(notation, 0) + 1
                else:
                    black_pieces[notation] = black_pieces.get(notation, 0) + 1
        
        return white_pieces, black_pieces

    def calculate_win_probability(self):
        """Calcula a probabilidade de vitória baseada na avaliação"""
        score = self.evaluate_position()
        
        # Converter score para probabilidade usando função sigmoide
        probability = 1 / (1 + math.exp(-score / 4))
        
        white_prob = probability * 100
        black_prob = (1 - probability) * 100
        
        return white_prob, black_prob

    def get_best_moves(self, color, depth=2):
        """Encontra os melhores movimentos para uma cor usando minimax básico"""
        best_moves = []
        best_score = float('-inf') if color == 'white' else float('inf')
        
        pieces = [square.occupying_piece for square in self.board.squares 
                 if square.occupying_piece is not None and square.occupying_piece.color == color]
        
        for piece in pieces:
            valid_moves = piece.get_valid_moves(self.board)
            for move in valid_moves:
                # Simular movimento
                original_piece = move.occupying_piece
                move.occupying_piece = piece
                original_pos = piece.pos
                piece.pos = move.pos
                
                # Avaliar posição
                score = self.evaluate_position()
                
                # Restaurar posição
                move.occupying_piece = original_piece
                piece.pos = original_pos
                
                move_notation = f"{piece.notation}{self.pos_to_notation(original_pos)}-{self.pos_to_notation(move.pos)}"
                
                if color == 'white':
                    if score > best_score:
                        best_score = score
                        best_moves = [(piece, move, score, move_notation)]
                    elif score == best_score:
                        best_moves.append((piece, move, score, move_notation))
                else:
                    if score < best_score:
                        best_score = score
                        best_moves = [(piece, move, score, move_notation)]
                    elif score == best_score:
                        best_moves.append((piece, move, score, move_notation))
        
        # Retornar os 3 melhores movimentos
        return best_moves[:3]

    def pos_to_notation(self, pos):
        """Converte posição (x,y) para notação de xadrez"""
        columns = 'abcdefgh'
        return columns[pos[0]] + str(8 - pos[1])

    def analyze_threats(self):
        """Analisa ameaças no tabuleiro"""
        white_threats = []
        black_threats = []
        
        for square in self.board.squares:
            if square.occupying_piece is not None:
                piece = square.occupying_piece
                attacked_squares = piece.attacking_squares(self.board)
                
                for attacked_square in attacked_squares:
                    if (attacked_square.occupying_piece is not None and 
                        attacked_square.occupying_piece.color != piece.color):
                        
                        threat_info = {
                            'attacker': piece.notation,
                            'target': attacked_square.occupying_piece.notation,
                            'position': self.pos_to_notation(attacked_square.pos)
                        }
                        
                        if piece.color == 'white':
                            white_threats.append(threat_info)
                        else:
                            black_threats.append(threat_info)
        
        return white_threats, black_threats

    def get_material_balance(self):
        """Calcula o balanço material"""
        white_material = 0
        black_material = 0
        
        for square in self.board.squares:
            if square.occupying_piece is not None:
                piece = square.occupying_piece
                value = self.piece_values[piece.notation]
                
                if piece.color == 'white':
                    white_material += value
                else:
                    black_material += value
        
        return white_material, black_material