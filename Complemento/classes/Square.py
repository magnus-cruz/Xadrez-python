import pygame

class Square:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.abs_x = x * width
        self.abs_y = y * height
        self.abs_pos = (self.abs_x, self.abs_y)
        self.pos = (x, y)
        
        # Determinar cor do quadrado (padrão xadrez)
        self.color = 'light' if (x + y) % 2 == 0 else 'dark'
        
        # Cores do tabuleiro
        self.light_color = (240, 217, 181)  # Cor clara
        self.dark_color = (181, 136, 99)    # Cor escura
        self.highlight_light = (255, 255, 0, 128)  # Amarelo claro para destacar
        self.highlight_dark = (255, 215, 0, 128)   # Amarelo escuro para destacar
        
        self.draw_color = self.light_color if self.color == 'light' else self.dark_color
        self.highlight_color = self.highlight_light if self.color == 'light' else self.highlight_dark
        
        self.occupying_piece = None
        self.coord = self.get_coord()
        self.highlight = False

        self.rect = pygame.Rect(
            self.abs_x,
            self.abs_y,
            self.width,
            self.height
        )

    def get_coord(self):
        """Retorna a coordenada do quadrado em notação de xadrez"""
        columns = 'abcdefgh'
        return columns[self.x] + str(8 - self.y)  # Inverter y para notação correta

    def draw(self, display, show_coordinates=False):
        """Desenha o quadrado na tela com opção de mostrar coordenadas"""
        # Desenhar o quadrado base
        pygame.draw.rect(display, self.draw_color, self.rect)
        
        # Desenhar borda
        pygame.draw.rect(display, (0, 0, 0), self.rect, 1)
        
        # Destacar se selecionado ou movimento válido
        if self.highlight:
            # Criar uma surface transparente para o highlight
            highlight_surface = pygame.Surface((self.width, self.height))
            highlight_surface.set_alpha(128)
            highlight_surface.fill((255, 255, 0))  # Amarelo
            display.blit(highlight_surface, (self.abs_x, self.abs_y))

        # Desenhar a peça se houver
        if self.occupying_piece is not None and self.occupying_piece.img is not None:
            # Centralizar a imagem da peça no quadrado
            piece_rect = self.occupying_piece.img.get_rect()
            piece_rect.center = self.rect.center
            display.blit(self.occupying_piece.img, piece_rect)

        # Desenhar coordenadas nos cantos se habilitado
        if show_coordinates:
            self.draw_square_coordinates(display)

    def draw_square_coordinates(self, display):
        """Desenha as coordenadas discretamente nos cantos do quadrado"""
        if not pygame.font.get_init():
            pygame.font.init()
        
        # Fonte pequena para coordenadas
        font_size = max(10, min(14, min(self.width, self.height) // 6))
        font = pygame.font.Font(None, font_size)
        
        # Cor das coordenadas baseada na cor do quadrado
        if self.color == 'light':
            coord_color = (120, 120, 120)  # Cinza médio em quadrados claros
        else:
            coord_color = (200, 200, 200)  # Cinza claro em quadrados escuros
        
        # Desenhar coordenada apenas nos quadrados das bordas
        coord_text = ""
        
        # Mostrar letra da coluna no canto inferior esquerdo (primeira fileira)
        if self.y == 7:  # Última fileira (números 1)
            columns = 'abcdefgh'
            coord_text = columns[self.x]
            text_surface = font.render(coord_text, True, coord_color)
            display.blit(text_surface, (self.abs_x + 2, self.abs_y + self.height - font_size - 2))
        
        # Mostrar número da fileira no canto superior direito (primeira coluna)
        if self.x == 7:  # Última coluna (letras h)
            coord_text = str(8 - self.y)
            text_surface = font.render(coord_text, True, coord_color)
            text_rect = text_surface.get_rect()
            display.blit(text_surface, (self.abs_x + self.width - text_rect.width - 2, self.abs_y + 2))

    def is_light_square(self):
        """Retorna True se o quadrado é claro"""
        return self.color == 'light'
    
    def is_dark_square(self):
        """Retorna True se o quadrado é escuro"""
        return self.color == 'dark'
    
    def get_algebraic_notation(self):
        """Retorna a notação algébrica do quadrado"""
        return self.coord
    
    def is_on_edge(self):
        """Verifica se o quadrado está na borda do tabuleiro"""
        return self.x == 0 or self.x == 7 or self.y == 0 or self.y == 7
    
    def is_corner(self):
        """Verifica se o quadrado é um canto do tabuleiro"""
        return ((self.x == 0 or self.x == 7) and (self.y == 0 or self.y == 7))
    
    def get_distance_from_center(self):
        """Calcula a distância do quadrado ao centro do tabuleiro"""
        center_x, center_y = 3.5, 3.5
        return ((self.x - center_x) ** 2 + (self.y - center_y) ** 2) ** 0.5