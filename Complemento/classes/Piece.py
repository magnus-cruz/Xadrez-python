import pygame
import os

class Piece:
    def __init__(self, pos, color, board):
        self.pos = pos
        self.x = pos[0]
        self.y = pos[1]
        self.color = color
        self.has_moved = False
        self.img = None
        self.notation = ''

    def load_image(self, filename, board):
        """Carrega a imagem da peça com tratamento de erro"""
        try:
            if hasattr(board, 'IMAGE_DIR') and board.IMAGE_DIR:
                img_path = os.path.join(board.IMAGE_DIR, filename)
            else:
                img_path = os.path.join('Complemento', 'imgs', filename)
            
            if os.path.exists(img_path):
                self.img = pygame.image.load(img_path)
                # Redimensionar para caber no quadrado
                piece_size = min(board.square_width - 20, board.square_height - 20)
                self.img = pygame.transform.scale(self.img, (piece_size, piece_size))
            else:
                # Criar uma imagem placeholder se a imagem não existir
                self.create_placeholder_image(board)
                print(f"Imagem não encontrada: {img_path}")
        except Exception as e:
            print(f"Erro ao carregar imagem {filename}: {e}")
            self.create_placeholder_image(board)

    def create_placeholder_image(self, board):
        """Cria uma imagem placeholder para a peça"""
        size = min(board.square_width - 20, board.square_height - 20)
        self.img = pygame.Surface((size, size))
        
        # Cor baseada na cor da peça
        if self.color == 'white':
            color = (255, 255, 255)
            text_color = (0, 0, 0)
        else:
            color = (64, 64, 64)
            text_color = (255, 255, 255)
        
        self.img.fill(color)
        pygame.draw.rect(self.img, (0, 0, 0), self.img.get_rect(), 2)
        
        # Desenhar a notação da peça
        if pygame.font.get_init():
            font = pygame.font.Font(None, size // 2)
            text = font.render(self.notation, True, text_color)
            text_rect = text.get_rect(center=(size // 2, size // 2))
            self.img.blit(text, text_rect)

    def move(self, board, square, force=False):
        """Move a peça para o quadrado especificado"""
        # Limpar highlights
        for sq in board.squares:
            sq.highlight = False

        if square in self.get_valid_moves(board) or force:
            prev_square = board.get_square_from_pos(self.pos)
            
            # Capturar peça se houver
            if square.occupying_piece is not None:
                captured_piece = square.occupying_piece
                board.captured_pieces[captured_piece.color].append(captured_piece)
            
            # Mover a peça
            self.pos, self.x, self.y = square.pos, square.x, square.y
            prev_square.occupying_piece = None
            square.occupying_piece = self
            board.selected_piece = None
            self.has_moved = True

            # Promoção de peão
            if self.notation == 'P':
                if (self.color == 'white' and self.y == 0) or (self.color == 'black' and self.y == 7):
                    from Complemento.classes.pieces.Queen import Queen
                    square.occupying_piece = Queen((self.x, self.y), self.color, board)

            # Roque
            if self.notation == 'K':
                # Roque curto (lado do rei)
                if prev_square.x - self.x == -2:
                    rook = board.get_piece_from_pos((7, self.y))
                    if rook:
                        rook.move(board, board.get_square_from_pos((5, self.y)), force=True)
                # Roque longo (lado da dama)
                elif prev_square.x - self.x == 2:
                    rook = board.get_piece_from_pos((0, self.y))
                    if rook:
                        rook.move(board, board.get_square_from_pos((3, self.y)), force=True)

            return True
        else:
            board.selected_piece = None
            return False

    def get_moves(self, board):
        """Retorna todos os movimentos possíveis da peça"""
        output = []
        for direction in self.get_possible_moves(board):
            for square in direction:
                if square.occupying_piece is not None:
                    if square.occupying_piece.color == self.color:
                        break
                    else:
                        output.append(square)
                        break
                else:
                    output.append(square)
        return output

    def get_valid_moves(self, board):
        """Retorna apenas os movimentos válidos (que não deixam o rei em xeque)"""
        output = []
        for square in self.get_moves(board):
            if not board.is_in_check(self.color, board_change=[self.pos, square.pos]):
                output.append(square)
        return output

    def get_possible_moves(self, board):
        """Método abstrato - deve ser implementado pelas subclasses"""
        return []

    def attacking_squares(self, board):
        """Retorna os quadrados que a peça está atacando"""
        return self.get_moves(board)