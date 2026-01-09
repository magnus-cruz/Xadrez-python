# main.py
import pygame
import os
import sys
from Complemento.classes.Board import Board
from Complemento.ChessAnalyzer import ChessAnalyzer
from Complemento.AnalysisPage import AnalysisPage

# Inicializar pygame
pygame.init()

# Configurações da janela - Agora redimensionável
MIN_WINDOW_WIDTH = 1000
MIN_WINDOW_HEIGHT = 700
DEFAULT_WINDOW_SIZE = (800, 600)

# Configurar diretório das imagens
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(ROOT_DIR, 'Complemento', 'imgs')

# Criar diretório de imagens se não existir
if not os.path.exists(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)

# Definir diretório de imagens no Board
Board.IMAGE_DIR = IMAGE_DIR

# Clock para controlar FPS
clock = pygame.time.Clock()

# Variáveis globais
screen = pygame.display.set_mode(DEFAULT_WINDOW_SIZE, pygame.RESIZABLE)
pygame.display.set_caption("Python Chess - Com Análise (Redimensionável)")
current_width, current_height = DEFAULT_WINDOW_SIZE
current_screen = "game"  # "game" ou "analysis"

# Inicializar objetos do jogo
try:
    board = Board(600, 600)  # Começar com um tamanho menor para melhor adaptabilidade
except Exception as e:
    print(f"Erro ao inicializar o tabuleiro: {e}")
    print("Verifique se as imagens das peças estão na pasta data/imgs/")
    pygame.quit()
    sys.exit()

analyzer = ChessAnalyzer(board)
analysis_page = AnalysisPage(current_width, current_height, board)

def calculate_layout(window_width, window_height):
    """Calcula o layout baseado no tamanho da janela"""
    # Calcular tamanho do tabuleiro (mantém proporção quadrada)
    # Reservar espaço para o painel lateral (mínimo 200px)
    available_width = window_width - 220  # 200 para painel + 20 margem
    available_height = window_height - 50  # 50 para margens
    
    # O tabuleiro deve ser quadrado, então usar a menor dimensão
    board_size = min(available_width, available_height)
    board_size = max(400, board_size)  # Tamanho mínimo do tabuleiro
    
    # Calcular posições
    board_x = 25
    board_y = (window_height - board_size) // 2
    
    # Painel lateral
    panel_x = board_x + board_size + 20
    panel_width = window_width - panel_x - 20
    panel_width = max(180, panel_width)  # Largura mínima do painel
    
    return {
        'board_size': board_size,
        'board_x': board_x,
        'board_y': board_y,
        'panel_x': panel_x,
        'panel_width': panel_width,
        'panel_height': window_height
    }

def resize_board(new_size):
    """Redimensiona o tabuleiro mantendo o estado atual"""
    global board, analyzer, analysis_page
    
    if board.width != new_size or board.height != new_size:
        # Salvar estado atual
        current_squares = []
        for square in board.squares:
            current_squares.append({
                'pos': square.pos,
                'piece': square.occupying_piece
            })
        
        current_turn = board.turn
        
        # Criar novo tabuleiro
        new_board = Board(new_size, new_size)
        new_board.turn = current_turn
        
        # Restaurar peças
        for square_data in current_squares:
            x, y = square_data['pos']
            square = new_board.get_square_from_pos((x, y))
            if square and square_data['piece']:
                piece = square_data['piece']
                square.occupying_piece = piece
                piece.pos = (x, y)
                piece.x, piece.y = x, y
        
        # Atualizar variáveis globais
        board = new_board
        analyzer = ChessAnalyzer(board)
        analysis_page = AnalysisPage(current_width, current_height, board)

def draw_game_screen(display, window_width, window_height):
    """Desenha a tela do jogo com layout responsivo"""
    global board, analyzer
    
    layout = calculate_layout(window_width, window_height)
    
    # Redimensionar tabuleiro se necessário
    if board.width != layout['board_size']:
        resize_board(layout['board_size'])
    
    display.fill((240, 217, 181))  # cor de fundo
    
    # Desenhar o tabuleiro
    display_surface = pygame.Surface((layout['board_size'], layout['board_size']))
    display_surface.fill((240, 217, 181))
    board.draw(display_surface)
    display.blit(display_surface, (layout['board_x'], layout['board_y']))
    
    # Painel lateral de informações
    panel_rect = pygame.Rect(layout['panel_x'], 0, layout['panel_width'], layout['panel_height'])
    pygame.draw.rect(display, (250, 248, 240), panel_rect)
    pygame.draw.rect(display, (200, 200, 200), panel_rect, 2)
    
    # Título do painel (ajustado ao tamanho)
    title_font_size = min(24, max(18, layout['panel_width'] // 8))
    font_title = pygame.font.Font(None, title_font_size)
    title_text = font_title.render("Informações", True, (60, 60, 60))
    display.blit(title_text, (layout['panel_x'] + 10, 20))
    
    # Linha separadora
    pygame.draw.line(display, (200, 200, 200), 
                    (layout['panel_x'] + 10, 50), 
                    (layout['panel_x'] + layout['panel_width'] - 10, 50), 2)
    
    # Informações do jogo (com fonte adaptável)
    info_font_size = min(20, max(16, layout['panel_width'] // 10))
    small_font_size = min(18, max(14, layout['panel_width'] // 12))
    
    font_info = pygame.font.Font(None, info_font_size)
    font_small = pygame.font.Font(None, small_font_size)
    
    y_offset = 70
    line_spacing = max(25, info_font_size + 5)
    small_line_spacing = max(20, small_font_size + 2)
    
    # Turno atual
    turn_text = f"Turno: {'Brancas' if board.turn == 'white' else 'Pretas'}"
    turn_surface = font_info.render(turn_text, True, (60, 60, 60))
    display.blit(turn_surface, (layout['panel_x'] + 10, y_offset))
    y_offset += line_spacing + 5
    
    # Probabilidades de vitória
    white_prob, black_prob = analyzer.calculate_win_probability()
    prob_title = font_info.render("Probabilidades:", True, (60, 60, 60))
    display.blit(prob_title, (layout['panel_x'] + 10, y_offset))
    y_offset += small_line_spacing
    
    white_prob_text = f"Brancas: {white_prob:.1f}%"
    black_prob_text = f"Pretas: {black_prob:.1f}%"
    
    white_surface = font_small.render(white_prob_text, True, (60, 60, 60))
    black_surface = font_small.render(black_prob_text, True, (60, 60, 60))
    
    display.blit(white_surface, (layout['panel_x'] + 10, y_offset))
    display.blit(black_surface, (layout['panel_x'] + 10, y_offset + small_line_spacing))
    y_offset += small_line_spacing * 2 + 10
    
    # Avaliação da posição
    score = analyzer.evaluate_position()
    eval_title = font_info.render("Avaliação:", True, (60, 60, 60))
    display.blit(eval_title, (layout['panel_x'] + 10, y_offset))
    y_offset += small_line_spacing
    
    eval_text = f"{score:+.2f}"
    if score > 0:
        eval_color = (0, 128, 0)  # Verde para brancas
    elif score < 0:
        eval_color = (128, 0, 0)  # Vermelho para pretas
    else:
        eval_color = (60, 60, 60)  # Cinza para equilibrado
        
    eval_surface = font_small.render(eval_text, True, eval_color)
    display.blit(eval_surface, (layout['panel_x'] + 10, y_offset))
    y_offset += line_spacing + 5
    
    # Material
    white_material, black_material = analyzer.get_material_balance()
    material_title = font_info.render("Material:", True, (60, 60, 60))
    display.blit(material_title, (layout['panel_x'] + 10, y_offset))
    y_offset += small_line_spacing
    
    material_text = f"B: {white_material} | P: {black_material}"
    material_surface = font_small.render(material_text, True, (60, 60, 60))
    display.blit(material_surface, (layout['panel_x'] + 10, y_offset))
    y_offset += line_spacing + 5
    
    # Mobilidade
    white_mobility = analyzer.count_valid_moves('white')
    black_mobility = analyzer.count_valid_moves('black')
    mobility_title = font_info.render("Mobilidade:", True, (60, 60, 60))
    display.blit(mobility_title, (layout['panel_x'] + 10, y_offset))
    y_offset += small_line_spacing
    
    mobility_text = f"B: {white_mobility} | P: {black_mobility}"
    mobility_surface = font_small.render(mobility_text, True, (60, 60, 60))
    display.blit(mobility_surface, (layout['panel_x'] + 10, y_offset))
    y_offset += line_spacing + 15
    
    # Melhor movimento para o jogador atual
    best_moves = analyzer.get_best_moves(board.turn)
    if best_moves:
        suggestion_title = font_info.render("Sugestão:", True, (60, 60, 60))
        display.blit(suggestion_title, (layout['panel_x'] + 10, y_offset))
        y_offset += small_line_spacing
        
        best_move = best_moves[0]
        move_text = best_move[3]  # Notação do movimento
        
        # Quebrar texto se for muito longo para o painel
        if len(move_text) * 8 > layout['panel_width'] - 20:  # Estimativa de largura
            move_text = move_text[:layout['panel_width']//10] + "..."
        
        move_surface = font_small.render(move_text, True, (0, 100, 200))
        display.blit(move_surface, (layout['panel_x'] + 10, y_offset))
        y_offset += line_spacing + 15
    
    # Botão de análise detalhada (responsivo)
    button_height = max(30, min(40, layout['panel_width'] // 6))
    button_margin = 20
    
    analysis_button = pygame.Rect(
        layout['panel_x'] + 10, 
        layout['panel_height'] - button_height - button_margin, 
        layout['panel_width'] - 20, 
        button_height
    )
    
    pygame.draw.rect(display, (100, 150, 200), analysis_button)
    pygame.draw.rect(display, (80, 130, 180), analysis_button, 2)
    
    button_font_size = min(20, max(14, button_height - 10))
    button_font = pygame.font.Font(None, button_font_size)
    button_text = button_font.render("Análise Detalhada", True, (255, 255, 255))
    button_rect = button_text.get_rect(center=analysis_button.center)
    display.blit(button_text, button_rect)
    
    # Mostrar dimensões da janela no canto superior direito (debug info)
    debug_font = pygame.font.Font(None, 16)
    debug_text = debug_font.render(f"{window_width}x{window_height}", True, (100, 100, 100))
    display.blit(debug_text, (window_width - 100, 10))
    
    return analysis_button, layout

def draw_analysis_screen(display):
    """Desenha a tela de análise"""
    analysis_page.draw(display)

def main():
    """Loop principal do jogo"""
    global current_screen, current_width, current_height, screen, board, analyzer, analysis_page
    
    running = True
    game_over = False
    winner = None
    analysis_button = None
    current_layout = None
    
    while running:
        mx, my = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            elif event.type == pygame.VIDEORESIZE:
                # Janela foi redimensionada
                new_width = max(MIN_WINDOW_WIDTH, event.w)
                new_height = max(MIN_WINDOW_HEIGHT, event.h)
                
                screen = pygame.display.set_mode((new_width, new_height), pygame.RESIZABLE)
                current_width, current_height = new_width, new_height
                
                # Atualizar página de análise com novas dimensões
                analysis_page = AnalysisPage(current_width, current_height, board)
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Botão esquerdo do mouse
                    if current_screen == "game":
                        # Verificar clique no botão de análise
                        if analysis_button and analysis_button.collidepoint((mx, my)):
                            current_screen = "analysis"
                        elif not game_over and current_layout:
                            # Verificar se o clique está dentro do tabuleiro
                            board_rect = pygame.Rect(
                                current_layout['board_x'], 
                                current_layout['board_y'],
                                current_layout['board_size'], 
                                current_layout['board_size']
                            )
                            if board_rect.collidepoint((mx, my)):
                                # Ajustar coordenadas do mouse para o tabuleiro
                                adjusted_mx = mx - current_layout['board_x']
                                adjusted_my = my - current_layout['board_y']
                                board.handle_click(adjusted_mx, adjusted_my)
                                
                    elif current_screen == "analysis":
                        # Verificar cliques na página de análise
                        result = analysis_page.handle_click((mx, my))
                        if result == "back_to_game":
                            current_screen = "game"
                            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and game_over:
                    # Reiniciar jogo
                    board_size = current_layout['board_size'] if current_layout else 600
                    board = Board(board_size, board_size)
                    analyzer = ChessAnalyzer(board)
                    analysis_page = AnalysisPage(current_width, current_height, board)
                    game_over = False
                    winner = None
                    current_screen = "game"
                elif event.key == pygame.K_ESCAPE:
                    if current_screen == "analysis":
                        current_screen = "game"
                    else:
                        running = False
                elif event.key == pygame.K_a and current_screen == "game":
                    # Tecla 'A' para alternar para análise
                    current_screen = "analysis"
                elif event.key == pygame.K_F11:
                    # Alternar tela cheia
                    pygame.display.toggle_fullscreen()

        # Verificar condições de fim de jogo (apenas na tela do jogo)
        if current_screen == "game" and not game_over:
            if board.is_in_checkmate('black'):
                print('Brancas vencem!')
                winner = 'Brancas'
                game_over = True
            elif board.is_in_checkmate('white'):
                print('Pretas vencem!')
                winner = 'Pretas'
                game_over = True

        # Desenhar a tela apropriada
        if current_screen == "game":
            analysis_button, current_layout = draw_game_screen(screen, current_width, current_height)
            
            # Mostrar mensagem de fim de jogo
            if game_over and current_layout:
                # Overlay semi-transparente sobre o tabuleiro
                overlay = pygame.Surface((current_layout['board_size'], current_layout['board_size']))
                overlay.set_alpha(128)
                overlay.fill((0, 0, 0))
                screen.blit(overlay, (current_layout['board_x'], current_layout['board_y']))
                
                # Fontes adaptáveis para fim de jogo
                big_font_size = min(74, max(36, current_layout['board_size'] // 12))
                small_font_size = min(36, max(24, current_layout['board_size'] // 20))
                
                font = pygame.font.Font(None, big_font_size)
                text = font.render(f'{winner} vencem!', True, (255, 255, 255))
                text_rect = text.get_rect(center=(
                    current_layout['board_x'] + current_layout['board_size'] // 2, 
                    current_layout['board_y'] + current_layout['board_size'] // 2 - 35
                ))
                screen.blit(text, text_rect)
                
                font_small = pygame.font.Font(None, small_font_size)
                restart_text = font_small.render('Pressione R para reiniciar ou ESC para sair', True, (255, 255, 255))
                restart_rect = restart_text.get_rect(center=(
                    current_layout['board_x'] + current_layout['board_size'] // 2, 
                    current_layout['board_y'] + current_layout['board_size'] // 2 + 35
                ))
                screen.blit(restart_text, restart_rect)
                
        elif current_screen == "analysis":
            draw_analysis_screen(screen)
        
        pygame.display.flip()
        
        # Controlar FPS
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()