# Análise de Xadrez — Aprendendo Probabilidade com Jogos

Este projeto é um analisador de xadrez em Python, com interface em `pygame`, que apresenta uma avaliação da posição, balanço de material, mobilidade e uma estimativa de probabilidade de vitória para cada lado. Ele foi pensado como uma ferramenta prática para ajudar alunos a se interessarem por matemática através de conceitos de probabilidade aplicados a situações reais (neste caso, partidas de xadrez).

## Objetivos Educacionais

- Introduzir probabilidade de forma intuitiva usando um jogo conhecido.
- Visualizar como uma função matemática (sigmoide) transforma uma avaliação em probabilidade.
- Explorar contagem e classificação (casos favoráveis/possíveis) em cenários de lances.
- Incentivar a formulação de hipóteses e validação por observação/experimentos simples.

## Recursos Principais

- Probabilidade de vitória estimada para brancas e pretas, exibida em barras e percentuais.
- Avaliação da posição baseada em material, valores posicionais e mobilidade.
- Balanço de material por peça e por cor.
- Painéis de análise e layout responsivo para diferentes tamanhos de janela.
- Estrutura modular (`Board`, `Piece`, `ChessAnalyzer`, `AnalysisPage`).

## Como Funciona a Probabilidade

A probabilidade de vitória é aproximada aplicando uma função sigmoide ao "score" da posição:

\[ p = \frac{1}{1 + e^{-s/4}} \]

Onde `s` é o valor da avaliação (positivo favorece brancas, negativo favorece pretas). O resultado `p` é multiplicado por 100 para obter o percentual das brancas, e `1 - p` para o percentual das pretas. Esta é uma forma didática de ligar avaliação numérica a uma chance de vitória, não uma previsão perfeita.

## Requisitos

- Python 3.8+ (recomendado 3.10+)
- `pygame`

Instalação do `pygame`:

```bash
pip install pygame
```

Em algumas distribuições Linux, pode ser necessário instalar bibliotecas de sistema relacionadas a SDL.

## Estrutura do Projeto

- [main.py](main.py): ponto de entrada, janela principal e alternância de telas.
- [Complemento/ChessAnalyzer.py](Complemento/ChessAnalyzer.py): avaliação, mobilidade, material e probabilidade.
- [Complemento/AnalysisPage.py](Complemento/AnalysisPage.py): página de análise com painéis visuais.
- [Complemento/classes/Board.py](Complemento/classes/Board.py): tabuleiro, casas e desenho.
- [Complemento/classes/pieces](Complemento/classes/pieces): implementação das peças (Rei, Rainha, Torre, Bispo, Cavalo, Peão).
- [Complemento/imgs](Complemento/imgs): imagens dos ícones das peças e outros recursos visuais.

## Como Executar

1. Verifique se as imagens das peças estão em [Complemento/imgs](Complemento/imgs) (por exemplo, em `imgs/icones/`).
2. Instale as dependências (`pygame`).
3. Execute:

```bash
python3 main.py
```

Durante a execução, a janela é redimensionável e exibe o tabuleiro, painel de informações e probabilidades. Interaja com o tabuleiro para movimentar peças e observar como a avaliação e as probabilidades se alteram.

## Atividades de Probabilidade (para alunos)

Estas propostas ajudam a conectar matemática com o jogo:

1. Estimativa vs. Observação: posicione peças para favorecer brancas (por exemplo, vantagem de material). Observe o aumento de `p` e discuta por que isso acontece.
2. Função Sigmoide: desenhe a curva sigmoide e marque alguns valores de `s` (por exemplo, `s = -8, -4, 0, 4, 8`). Relacione a inclinação da curva com a sensibilidade da probabilidade.
3. Contagem de Lances: escolha uma posição e conte manualmente (ou com auxílio do sistema) o número de lances válidos. Classifique “lances que dão cheque” como casos favoráveis e estime $P(\text{cheque}) = \frac{\text{favoráveis}}{\text{possíveis}}$.
4. Mobilidade e Chances: compare duas posições onde uma cor tem mais mobilidade. Discuta a relação entre mobilidade e avaliação, e como isso tende a influenciar a probabilidade.
5. Experimento Simples: faça uma sequência curta de lances e registre como `s` e `p` evoluem. Construa um gráfico `lance vs. p` e interprete.

> Observação: as estimativas de probabilidade aqui são didáticas e não equivalem a previsões de engine profissional. O objetivo é apoiar o raciocínio probabilístico.

## Problemas Comuns

- Janela não abre no Linux: verifique se o ambiente gráfico está disponível e se `pygame` está corretamente instalado.
- Imagens não carregam: confirme o caminho [Complemento/imgs](Complemento/imgs). O programa cria a pasta se não existir, mas é necessário que os ícones das peças estejam presentes.
- Erros de fonte ou renderização: podem ocorrer por ausência de fontes do sistema; o projeto usa `pygame.font.Font(None, ...)` para fontes padrão.

## Contribuição

- Adicionar exercícios guiados de probabilidade.
- Inserir um painel de “experimentos” para contagem automática de categorias de lances.
- Integrar análises mais avançadas e registrar séries de dados para atividades.

## Licença

Projeto educacional. Caso deseje publicar, escolha uma licença adequada (MIT, GPL, etc.).
