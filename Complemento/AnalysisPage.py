import pygame
import math
from Complemento.ChessAnalyzer import ChessAnalyzer

class AnalysisPage:
    def __init__(self, width, height, board):
        self.width = width
        self.height = height
        self.board = board
        self.analyzer = ChessAnalyzer(board)
        
        # Cores da página
        self.bg_color = (250, 248, 240)  # Fundo creme claro
        self.panel_color = (255, 255, 255)  # Branco para painéis
        self.border_color = (200, 200, 200)  # Cinza claro para bordas
        self.text_color = (60, 60, 60)  # Cinza escuro para texto
        self.accent_color = (100, 150, 200)  # Azul suave para destaques
        self.white_color = (255, 255, 255)
        self.black_color = (80, 80, 80)
        
        # Fontes adaptáveis
        pygame.font.init()
        self.update_fonts()
        
        # Botão de volta (tamanho adaptável)
        button_width = max(80, min(120, self.width // 12))
        button_height = max(30, min(50, self.height // 20))
        self.back_button = pygame.Rect(20, 20, button_width, button_height)
        
    def update_fonts(self):
        """Atualiza os tamanhos das fontes baseado no tamanho da janela"""
        base_size = min(self.width, self.height)
        self.title_font = pygame.font.Font(None, max(28, min(48, base_size // 25)))
        self.subtitle_font = pygame.font.Font(None, max(22, min(32, base_size // 30)))
        self.text_font = pygame.font.Font(None, max(18, min(26, base_size // 35)))
        self.small_font = pygame.font.Font(None, max(14, min(20, base_size // 45)))
        
    def calculate_responsive_layout(self):
        """Calcula o layout responsivo baseado no tamanho da janela"""
        # Margens adaptáveis
        margin = max(15, min(30, self.width // 50))
        top_margin = max(70, min(100, self.height // 12))
        
        # Determinar se deve usar layout vertical ou horizontal
        aspect_ratio = self.width / self.height
        use_vertical_layout = aspect_ratio < 1.3  # Layout vertical para janelas mais altas
        
        if use_vertical_layout:
            # Layout vertical: painéis empilhados
            panel_width = self.width - 2 * margin
            panel_height = (self.height - top_margin - 4 * margin) // 3
            
            layouts = [
                {'x': margin, 'y': top_margin, 'width': panel_width, 'height': panel_height},
                {'x': margin, 'y': top_margin + panel_height + margin, 'width': panel_width, 'height': panel_height},
                {'x': margin, 'y': top_margin + 2 * (panel_height + margin), 'width': panel_width, 'height': panel_height}
            ]
        else:
            # Layout horizontal: 2x3 ou 1x6 dependendo do espaço
            if self.height > 600:  # Layout 2x3 se há altura suficiente
                panel_width = (self.width - 3 * margin) // 2
                panel_height = (self.height - top_margin - 3 * margin) // 3
                
                layouts = [
                    {'x': margin, 'y': top_margin, 'width': self.width - 2 * margin, 'height': panel_height},  # Topo inteiro
                    {'x': margin, 'y': top_margin + panel_height + margin, 'width': panel_width, 'height': panel_height},
                    {'x': margin * 2 + panel_width, 'y': top_margin + panel_height + margin, 'width': panel_width, 'height': panel_height},
                    {'x': margin, 'y': top_margin + 2 * (panel_height + margin), 'width': panel_width, 'height': panel_height},
                    {'x': margin * 2 + panel_width, 'y': top_margin + 2 * (panel_height + margin), 'width': panel_width, 'height': panel_height}
                ]
            else:  # Layout simplificado para janelas baixas
                panel_width = (self.width - 3 * margin) // 2
                panel_height = (self.height - top_margin - 2 * margin) // 2
                
                layouts = [
                    {'x': margin, 'y': top_margin, 'width': self.width - 2 * margin, 'height': panel_height},
                    {'x': margin, 'y': top_margin + panel_height + margin, 'width': panel_width, 'height': panel_height},
                    {'x': margin * 2 + panel_width, 'y': top_margin + panel_height + margin, 'width': panel_width, 'height': panel_height}
                ]
        
        return layouts
        
    def draw_button(self, surface, rect, text, font, bg_color, text_color, border_color=None):
        """Desenha um botão estilizado"""
        pygame.draw.rect(surface, bg_color, rect)
        if border_color:
            pygame.draw.rect(surface, border_color, rect, 2)
        
        text_surface = font.render(text, True, text_color)
        text_rect = text_surface.get_rect(center=rect.center)
        surface.blit(text_surface, text_rect)
        
    def draw_panel(self, surface, rect, title, content_func):
        """Desenha um painel com título e conteúdo"""
        # Fundo do painel
        pygame.draw.rect(surface, self.panel_color, rect)
        pygame.draw.rect(surface, self.border_color, rect, 2)
        
        # Título do painel
        title_surface = self.subtitle_font.render(title, True, self.text_color)
        surface.blit(title_surface, (rect.x + 10, rect.y + 10))
        
        # Linha separadora
        separator_y = rect.y + 10 + self.subtitle_font.get_height() + 5
        pygame.draw.line(surface, self.border_color, 
                        (rect.x + 10, separator_y), 
                        (rect.x + rect.width - 10, separator_y), 2)
        
        # Conteúdo
        content_y = separator_y + 10
        available_height = rect.height - (content_y - rect.y) - 10
        content_func(surface, rect.x + 10, content_y, rect.width - 20, available_height)
        
    def draw_probability_panel(self, surface, x, y, width, height):
        """Desenha o painel de probabilidades com melhor organização"""
        white_prob, black_prob = self.analyzer.calculate_win_probability()
        score = self.analyzer.evaluate_position()
        
        # Área central para as barras (responsiva)
        bar_area_width = width - 40
        bar_height = max(25, min(45, height // 8))
        bar_y = y + 20
        
        # Fundo das barras (cinza claro)
        bg_rect_white = pygame.Rect(x + 20, bar_y, bar_area_width, bar_height)
        bg_rect_black = pygame.Rect(x + 20, bar_y + bar_height + 10, bar_area_width, bar_height)
        
        pygame.draw.rect(surface, (240, 240, 240), bg_rect_white)
        pygame.draw.rect(surface, (240, 240, 240), bg_rect_black)
        pygame.draw.rect(surface, self.border_color, bg_rect_white, 1)
        pygame.draw.rect(surface, self.border_color, bg_rect_black, 1)
        
        # Barras de probabilidade preenchidas
        white_width = int(bar_area_width * (white_prob / 100))
        black_width = int(bar_area_width * (black_prob / 100))
        
        if white_width > 0:
            white_rect = pygame.Rect(x + 20, bar_y, white_width, bar_height)
            pygame.draw.rect(surface, (220, 220, 220), white_rect)
            pygame.draw.rect(surface, (100, 100, 100), white_rect, 2)
        
        if black_width > 0:
            black_rect = pygame.Rect(x + 20, bar_y + bar_height + 10, black_width, bar_height)
            pygame.draw.rect(surface, (100, 100, 100), black_rect)
            pygame.draw.rect(surface, (60, 60, 60), black_rect, 2)
        
        # Labels das barras (à esquerda)
        white_label = self.text_font.render("Brancas", True, self.text_color)
        black_label = self.text_font.render("Pretas", True, self.text_color)
        
        label_y_offset = (bar_height - self.text_font.get_height()) // 2
        surface.blit(white_label, (x + 25, bar_y + label_y_offset))
        surface.blit(black_label, (x + 25, bar_y + bar_height + 10 + label_y_offset))
        
        # Percentuais (à direita das barras)
        white_percent = self.text_font.render(f"{white_prob:.1f}%", True, self.text_color)
        black_percent = self.text_font.render(f"{black_prob:.1f}%", True, self.text_color)
        
        surface.blit(white_percent, (x + bar_area_width - 40, bar_y + label_y_offset))
        surface.blit(black_percent, (x + bar_area_width - 40, bar_y + bar_height + 10 + label_y_offset))
        
        # Avaliação numérica (centralizada)
        eval_y = bar_y + 2 * bar_height + 40
        eval_main = f"Avaliação: {score:+.2f}"
        
        # Cor baseada na avaliação
        if score > 0:
            eval_color = (60, 120, 60)  # Verde escuro
            eval_desc = "Vantagem das Brancas"
        elif score < 0:
            eval_color = (120, 60, 60)  # Vermelho escuro
            eval_desc = "Vantagem das Pretas"
        else:
            eval_color = (80, 80, 80)  # Cinza
            eval_desc = "Posição Equilibrada"
        
        eval_surface = self.text_font.render(eval_main, True, eval_color)
        desc_surface = self.small_font.render(eval_desc, True, self.text_color)
        
        # Centralizar textos
        eval_rect = eval_surface.get_rect(center=(x + width//2, eval_y))
        desc_rect = desc_surface.get_rect(center=(x + width//2, eval_y + 25))
        
        surface.blit(eval_surface, eval_rect)
        surface.blit(desc_surface, desc_rect)
        
    def draw_material_panel(self, surface, x, y, width, height):
        """Desenha o painel de análise material com melhor formatação"""
        white_pieces, black_pieces = self.analyzer.get_piece_count()
        white_material, black_material = self.analyzer.get_material_balance()
        
        piece_names = {
            'K': 'Rei', 'Q': 'Rainha', 'R': 'Torre', 
            'B': 'Bispo', 'N': 'Cavalo', 'P': 'Peão'
        }
        
        current_y = y + 10
        row_height = max(18, min(25, height // 12))
        
        # Cabeçalho da tabela
        header_bg = pygame.Rect(x, current_y, width - 20, row_height + 5)
        pygame.draw.rect(surface, (235, 235, 235), header_bg)
        pygame.draw.rect(surface, self.border_color, header_bg, 1)
        
        # Calcular larguras das colunas baseado no espaço disponível
        col_widths = [
            max(60, width // 4),  # Peça
            max(50, width // 6),  # Brancas
            max(50, width // 6),  # Pretas
            max(50, width // 6)   # Valor
        ]
        
        headers = ["Peça", "Brancas", "Pretas", "Valor"]
        col_x = x + 10
        
        for i, (header, col_width) in enumerate(zip(headers, col_widths)):
            header_text = self.text_font.render(header, True, self.text_color)
            surface.blit(header_text, (col_x, current_y + 4))
            col_x += col_width
        
        current_y += row_height + 10
        
        # Linha separadora
        pygame.draw.line(surface, self.border_color, (x, current_y), (x + width - 20, current_y), 1)
        current_y += 5
        
        # Listar peças com alternância de cores de fundo
        for i, piece_type in enumerate(['K', 'Q', 'R', 'B', 'N', 'P']):
            if piece_type in (set(white_pieces.keys()) | set(black_pieces.keys())):
                # Fundo alternado
                if i % 2 == 0:
                    row_bg = pygame.Rect(x, current_y, width - 20, row_height)
                    pygame.draw.rect(surface, (248, 248, 248), row_bg)
                
                white_count = white_pieces.get(piece_type, 0)
                black_count = black_pieces.get(piece_type, 0)
                piece_value = self.analyzer.piece_values[piece_type]
                
                # Dados da linha
                row_data = [
                    piece_names[piece_type],
                    str(white_count),
                    str(black_count),
                    str(piece_value) if piece_type != 'K' else "∞"
                ]
                
                col_x = x + 10
                for data, col_width in zip(row_data, col_widths):
                    text_surface = self.text_font.render(data, True, self.text_color)
                    surface.blit(text_surface, (col_x, current_y + 2))
                    col_x += col_width
                
                current_y += row_height
        
        # Linha separadora final
        current_y += 5
        pygame.draw.line(surface, self.border_color, (x, current_y), (x + width - 20, current_y), 2)
        current_y += 10
        
        # Total material com destaque
        total_bg = pygame.Rect(x, current_y, width - 20, row_height + 10)
        pygame.draw.rect(surface, (245, 250, 255), total_bg)
        pygame.draw.rect(surface, self.accent_color, total_bg, 2)
        
        difference = white_material - black_material
        if difference > 0:
            total_text = f"Material: B {white_material}, P {black_material} (+{difference})"
            color = (60, 120, 60)
        elif difference < 0:
            total_text = f"Material: B {white_material}, P {black_material} ({difference})"
            color = (120, 60, 60)
        else:
            total_text = f"Material: B {white_material}, P {black_material} (Igual)"
            color = self.text_color
            
        # Ajustar texto se for muito longo
        if len(total_text) * 8 > width - 40:
            total_text = f"B:{white_material} P:{black_material} ({difference:+})"
            
        total_surface = self.text_font.render(total_text, True, color)
        surface.blit(total_surface, (x + 10, current_y + 6))
        
    def draw_moves_panel(self, surface, x, y, width, height):
        """Desenha o painel de melhores movimentos com melhor organização"""
        # Dividir em duas colunas mais organizadas
        col_width = (width - 30) // 2
        
        # Movimentos das brancas
        white_moves = self.analyzer.get_best_moves('white')
        self.draw_move_column(surface, x, y, col_width, height, "Brancas", white_moves, (240, 240, 240))
        
        # Linha separadora vertical
        separator_x = x + col_width + 15
        pygame.draw.line(surface, self.border_color, 
                        (separator_x, y), (separator_x, y + height - 20), 1)
        
        # Movimentos das pretas
        black_moves = self.analyzer.get_best_moves('black')
        self.draw_move_column(surface, x + col_width + 30, y, col_width, height, "Pretas", black_moves, (100, 100, 100))
        
    def draw_move_column(self, surface, x, y, width, height, title, moves, icon_color):
        """Desenha uma coluna de movimentos com melhor formatação"""
        current_y = y
        row_height = max(18, min(25, height // 12))
        
        # Cabeçalho da coluna com fundo colorido
        header_bg = pygame.Rect(x, current_y, width, row_height + 5)
        if "Brancas" in title:
            pygame.draw.rect(surface, (250, 250, 250), header_bg)
        else:
            pygame.draw.rect(surface, (220, 220, 220), header_bg)
        pygame.draw.rect(surface, self.border_color, header_bg, 1)
        
        title_surface = self.text_font.render(title, True, self.text_color)
        surface.blit(title_surface, (x + 10, current_y + 4))
        current_y += row_height + 10
        
        # Listar movimentos
        if moves:
            max_moves = min(len(moves), max(2, height // (row_height + 2) - 2))
            
            for i in range(max_moves):
                piece, move, score, notation = moves[i]
                
                # Fundo alternado para cada movimento
                move_bg = pygame.Rect(x, current_y, width, row_height)
                if i % 2 == 0:
                    pygame.draw.rect(surface, (248, 248, 248), move_bg)
                
                # Número do movimento
                num_surface = self.text_font.render(f"{i+1}.", True, self.text_color)
                surface.blit(num_surface, (x + 5, current_y + 2))
                
                # Notação do movimento (truncar se necessário)
                if len(notation) * 6 > width - 80:
                    notation = notation[:max(4, width // 12)] + "..."
                
                move_surface = self.text_font.render(notation, True, self.text_color)
                surface.blit(move_surface, (x + 25, current_y + 2))
                
                # Score do movimento
                score_text = f"({score:+.1f})"
                score_color = (60, 120, 60) if score > 0 else (120, 60, 60) if score < 0 else self.text_color
                score_surface = self.small_font.render(score_text, True, score_color)
                surface.blit(score_surface, (x + width - 60, current_y + 4))
                
                current_y += row_height + 2
        else:
            # Mensagem quando não há movimentos
            no_moves_bg = pygame.Rect(x, current_y, width, row_height + 10)
            pygame.draw.rect(surface, (255, 248, 248), no_moves_bg)
            pygame.draw.rect(surface, (255, 200, 200), no_moves_bg, 1)
            
            no_moves = self.small_font.render("Nenhum movimento", True, (150, 80, 80))
            no_moves_rect = no_moves.get_rect(center=(x + width//2, current_y + (row_height + 10)//2))
            surface.blit(no_moves, no_moves_rect)
            
    def draw_threats_panel(self, surface, x, y, width, height):
        """Desenha o painel de ameaças com melhor organização"""
        white_threats, black_threats = self.analyzer.analyze_threats()
        
        current_y = y + 5
        col_width = (width - 30) // 2
        
        # Coluna das ameaças das brancas
        self.draw_threats_column(surface, x, current_y, col_width, height - 10, 
                                "Ameaças Brancas", white_threats, (250, 250, 250))
        
        # Linha separadora vertical
        separator_x = x + col_width + 15
        pygame.draw.line(surface, self.border_color, 
                        (separator_x, current_y), (separator_x, current_y + height - 20), 1)
        
        # Coluna das ameaças das pretas
        self.draw_threats_column(surface, x + col_width + 30, current_y, col_width, height - 10,
                                "Ameaças Pretas", black_threats, (220, 220, 220))
        
    def draw_threats_column(self, surface, x, y, width, height, title, threats, bg_color):
        """Desenha uma coluna de ameaças"""
        current_y = y
        row_height = max(16, min(22, height // 15))
        
        # Cabeçalho
        header_bg = pygame.Rect(x, current_y, width, row_height + 5)
        pygame.draw.rect(surface, bg_color, header_bg)
        pygame.draw.rect(surface, self.border_color, header_bg, 1)
        
        title_surface = self.text_font.render(title, True, self.text_color)
        surface.blit(title_surface, (x + 10, current_y + 4))
        current_y += row_height + 10
        
        # Listar ameaças (máximo baseado na altura disponível)
        max_threats = min(len(threats), max(2, (height - row_height - 20) // (row_height + 2)))
        displayed_threats = threats[:max_threats]
        
        if displayed_threats:
            for i, threat in enumerate(displayed_threats):
                # Fundo alternado
                threat_bg = pygame.Rect(x, current_y, width, row_height)
                if i % 2 == 0:
                    pygame.draw.rect(surface, (248, 248, 248), threat_bg)
                
                # Texto da ameaça (truncar se necessário)
                threat_text = f"{threat['attacker']} → {threat['target']}"
                if len(threat_text) * 6 > width - 20:
                    threat_text = f"{threat['attacker']}→{threat['target']}"
                
                threat_surface = self.small_font.render(threat_text, True, self.text_color)
                surface.blit(threat_surface, (x + 5, current_y + 2))
                
                current_y += row_height + 2
                
            # Mostrar total se houver mais ameaças
            if len(threats) > max_threats:
                more_text = f"... +{len(threats) - max_threats}"
                more_surface = self.small_font.render(more_text, True, (120, 120, 120))
                surface.blit(more_surface, (x + 10, current_y + 5))
                
        else:
            # Sem ameaças
            no_threats_bg = pygame.Rect(x, current_y, width, row_height + 10)
            pygame.draw.rect(surface, (248, 255, 248), no_threats_bg)
            pygame.draw.rect(surface, (200, 240, 200), no_threats_bg, 1)
            
            no_threats = self.small_font.render("Sem ameaças", True, (80, 150, 80))
            no_threats_rect = no_threats.get_rect(center=(x + width//2, current_y + (row_height + 10)//2))
            surface.blit(no_threats, no_threats_rect)
            
    def draw_mobility_panel(self, surface, x, y, width, height):
        """Desenha o painel de mobilidade"""
        white_mobility = self.analyzer.count_valid_moves('white')
        black_mobility = self.analyzer.count_valid_moves('black')
        total_moves = white_mobility + black_mobility
        
        current_y = y + 10
        
        # Título 
        title_text = "Mobilidade (Movimentos Válidos)"
        title_surface = self.text_font.render(title_text, True, self.text_color)
        surface.blit(title_surface, (x, current_y))
        current_y += 30
        
        # Barras de mobilidade
        bar_height = max(20, min(35, height // 8))
        bar_width = width - 100  # Espaço para texto
        
        # Barra das brancas
        white_bg = pygame.Rect(x, current_y, bar_width, bar_height)
        pygame.draw.rect(surface, (240, 240, 240), white_bg)
        pygame.draw.rect(surface, self.border_color, white_bg, 1)
        
        if total_moves > 0:
            white_fill_width = int(bar_width * (white_mobility / total_moves))
            if white_fill_width > 0:
                white_fill = pygame.Rect(x, current_y, white_fill_width, bar_height)
                pygame.draw.rect(surface, (200, 200, 200), white_fill)
        
        # Texto das brancas
        white_text = f"B: {white_mobility}"
        white_surface = self.text_font.render(white_text, True, self.text_color)
        surface.blit(white_surface, (x + bar_width + 10, current_y + (bar_height - self.text_font.get_height()) // 2))
        
        current_y += bar_height + 10
        
        # Barra das pretas
        black_bg = pygame.Rect(x, current_y, bar_width, bar_height)
        pygame.draw.rect(surface, (240, 240, 240), black_bg)
        pygame.draw.rect(surface, self.border_color, black_bg, 1)
        
        if total_moves > 0:
            black_fill_width = int(bar_width * (black_mobility / total_moves))
            if black_fill_width > 0:
                black_fill = pygame.Rect(x, current_y, black_fill_width, bar_height)
                pygame.draw.rect(surface, (120, 120, 120), black_fill)
        
        # Texto das pretas
        black_text = f"P: {black_mobility}"
        black_surface = self.text_font.render(black_text, True, self.text_color)
        surface.blit(black_surface, (x + bar_width + 10, current_y + (bar_height - self.text_font.get_height()) // 2))
        
        current_y += bar_height + 20
        
        # Diferença
        difference = white_mobility - black_mobility
        if difference > 0:
            diff_text = f"Brancas +{difference} movimentos"
            diff_color = (60, 120, 60)
        elif difference < 0:
            diff_text = f"Pretas +{-difference} movimentos"
            diff_color = (120, 60, 60)
        else:
            diff_text = "Mobilidade equilibrada"
            diff_color = self.text_color
            
        diff_surface = self.small_font.render(diff_text, True, diff_color)
        diff_rect = diff_surface.get_rect(center=(x + width//2, current_y))
        surface.blit(diff_surface, diff_rect)
        
    def draw(self, surface):
        """Desenha a página de análise com layout responsivo"""
        # Atualizar fontes baseado no tamanho atual
        self.update_fonts()
        
        # Fundo
        surface.fill(self.bg_color)
        
        # Título
        title = self.title_font.render("Análise da Posição", True, self.text_color)
        title_rect = title.get_rect(center=(self.width // 2, 30))
        surface.blit(title, title_rect)
        
        # Botão de volta (atualizar tamanho)
        button_width = max(80, min(120, self.width // 12))
        button_height = max(30, min(50, self.height // 20))
        self.back_button = pygame.Rect(20, 20, button_width, button_height)
        
        # Ajustar texto do botão baseado no tamanho
        button_text = "← Voltar" if button_width > 90 else "←"
        
        self.draw_button(surface, self.back_button, button_text, 
                        self.text_font, self.panel_color, self.text_color, self.border_color)
        
        # Calcular layout responsivo
        layouts = self.calculate_responsive_layout()
        
        # Painéis de análise com títulos ajustáveis
        panel_titles = [
            "Probabilidade de Vitória",
            "Análise Material", 
            "Mobilidade",
            "Melhores Movimentos",
            "Ameaças no Tabuleiro"
        ]
        
        panel_functions = [
            self.draw_probability_panel,
            self.draw_material_panel,
            self.draw_mobility_panel,
            self.draw_moves_panel,
            self.draw_threats_panel
        ]
        
        # Desenhar painéis baseado no layout calculado
        for i, (layout, title, func) in enumerate(zip(layouts, panel_titles, panel_functions)):
            if i < len(layouts):  # Verificar se há layout para este painel
                rect = pygame.Rect(layout['x'], layout['y'], layout['width'], layout['height'])
                
                # Ajustar título se for muito longo para o painel
                if len(title) * (self.subtitle_font.get_height() // 2) > layout['width'] - 40:
                    # Títulos mais curtos para painéis pequenos
                    short_titles = [
                        "Probabilidades",
                        "Material", 
                        "Mobilidade",
                        "Movimentos",
                        "Ameaças"
                    ]
                    title = short_titles[i]
                
                self.draw_panel(surface, rect, title, func)
        
    def handle_click(self, pos):
        """Manipula cliques na página de análise"""
        if self.back_button.collidepoint(pos):
            return "back_to_game"
        return None