import pygame
import random
pygame.font.init()

# Game settings

# beginner
BOARD_WIDTH = 10
BOARD_HIGHT = 10
NUMBER_BOMBS = 10
NODE_SIZE = int(90)

# intermediate
# BOARD_WIDTH = 16
# BOARD_HIGHT = 16
# NUMBER_BOMBS = 40
# NODE_SIZE = int(60)

# expert
# BOARD_WIDTH = 30
# BOARD_HIGHT = 16
# NUMBER_BOMBS = 99
# NODE_SIZE = int(50)


WIDTH = BOARD_WIDTH*NODE_SIZE
HEIGHT = BOARD_HIGHT*NODE_SIZE
pygame.display.set_caption("minesweeper")
screen = pygame.display.set_mode((WIDTH, HEIGHT))

FPS = 60
TEXT_FONT = pygame.font.SysFont('comicsans', int(0.4*(WIDTH*.2)))
TEXT_FONT_2 = pygame.font.SysFont('comicsans', int(0.2*(WIDTH*.2)))

COUNT_FONT = pygame.font.SysFont('comicsans', int(0.6*NODE_SIZE))

END_SCREEN_WIDTH = WIDTH//1.5
END_SCREEN_HEIGHT = HEIGHT//2
END_SCREEN = pygame.Rect((WIDTH - END_SCREEN_WIDTH)//2, (HEIGHT - END_SCREEN_HEIGHT)//2, END_SCREEN_WIDTH, END_SCREEN_HEIGHT)

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0 , 0)
GREEN = (0, 255, 0)
RED = (255, 0 , 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (255, 0, 255)

GREY_1 = (128, 128, 128)
GREY_2 = (164, 164, 164)
GREY_3 = (192, 192, 192)

class Node():

    def __init__(self, x, y, bomb = False):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x*NODE_SIZE, y*NODE_SIZE, NODE_SIZE, NODE_SIZE)
        self.bomb = bomb
        self.clicked = False
        self.clicked_2 = False
        self.hovered = False
        self.revealed = False
        self.adjacent_bombs = 0
        self.flagged = False
        self.over = False

    def is_revealed(self):
        return self.revealed

    def is_flagged(self):
        return self.flagged

    def is_bomb(self):
        return self.bomb

    def reveal_bomb(self):
        self.over = True

    def reveal(self):
        self.revealed = True

    def toggle_flag(self):
        self.flagged = not self.flagged

    def set_adjacent_bombs(self, value:int):
        self.adjacent_bombs = value

    def highlight(self):
        self.hovered = True

    def unhighlight(self):
        self.hovered = False

    def draw(self):

        action = None

        mouse_pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse_pos) and self.revealed == False:

            action = 'hovered'

            if pygame.mouse.get_pressed()[0] and self.clicked == False:
                self.clicked = True
                action = 'left_clicked'

            elif not pygame.mouse.get_pressed()[0]:
                self.clicked = False

            if pygame.mouse.get_pressed()[2] and self.clicked_2 == False:
                self.clicked_2 = True
                action = 'right_clicked'

            elif not pygame.mouse.get_pressed()[2]:
                self.clicked_2 = False

        pygame.draw.rect(screen, GREY_1, self.rect)
        pygame.draw.rect(screen, GREY_2, (self.rect.x,self.rect.y,int(self.rect.width-self.rect.width*0.03),int(self.rect.height-self.rect.height*0.03)))

        if self.revealed:
            pygame.draw.rect(screen, GREY_1, self.rect)
            pygame.draw.rect(screen, GREY_3, (self.rect.x,self.rect.y,int(self.rect.width-self.rect.width*0.03),int(self.rect.height-self.rect.height*0.03)))
            if self.bomb:
                pygame.draw.rect(screen, GREY_1, self.rect)
                pygame.draw.rect(screen, RED, (self.rect.x,self.rect.y,int(self.rect.width-self.rect.width*0.03),int(self.rect.height-self.rect.height*0.03)))
                pygame.draw.circle(screen, BLACK, (self.rect.x+self.rect.width//2, self.rect.y+self.rect.height//2), NODE_SIZE//4)
            elif self.adjacent_bombs:
                piece_text = COUNT_FONT.render(str(self.adjacent_bombs), 1, BLACK)
                screen.blit(piece_text, (self.rect.x + (self.rect.width - piece_text.get_width())//2, self.rect.y + (self.rect.width - piece_text.get_height())//2))
        elif self.flagged:
            pygame.draw.circle(screen, RED, (self.rect.x+self.rect.width//2, self.rect.y+self.rect.height//2), NODE_SIZE//4)
        if self.over and self.bomb:
            pygame.draw.rect(screen, GREY_1, self.rect)
            pygame.draw.rect(screen, GREY_3, (self.rect.x,self.rect.y,int(self.rect.width-self.rect.width*0.03),int(self.rect.height-self.rect.height*0.03)))
            pygame.draw.circle(screen, BLACK, (self.rect.x+self.rect.width//2, self.rect.y+self.rect.height//2), NODE_SIZE//4)

        if self.hovered and not self.revealed:
            pygame.draw.rect(screen, GREEN, self.rect, 4)

        return action

class Game():

    def __init__(self):
        self.reset_game()

    def reset_game(self):
        self.board = self.new_board()
        self.winner = None
        self.ending_screen = True

    def new_board(self):
        bombs = [(random.randint(0, BOARD_WIDTH-1), random.randint(0, BOARD_HIGHT-1)) for i in range(NUMBER_BOMBS)]
        return [[Node(x, y, True) if (x, y) in bombs else Node(x, y) for x in range(BOARD_WIDTH)] for y in range(BOARD_HIGHT)]

    def highlight_node(self, node):
        if not node.is_revealed():
            node.highlight()

        for y in self.board:
            for x in y:
                if x == node:
                    continue
                x.unhighlight()

    def reveal_nodes(self, node):
        if not node.is_revealed():
            if node.is_flagged():
                node.toggle_flag()
            adjacent_bombs = self.calculate_adjacent_bombs(node)
            node.set_adjacent_bombs(adjacent_bombs)
            node.reveal()
            if not adjacent_bombs:
                for d in {(0,1),(1,0),(1,1),(0,0),(0,-1),(-1,0),(-1,-1),(0,0)}:
                    if (node.y+d[0] < 0 or node.y+d[0] > BOARD_HIGHT-1) or (node.x+d[1] < 0 or node.x+d[1] > BOARD_WIDTH-1):
                        continue
                    self.reveal_nodes(self.board[node.y+d[0]][node.x+d[1]])

        self.winner = self.check_game_over()

    def calculate_adjacent_bombs(self, node):
        count = 0
        for d in {(0,1),(1,0),(1,1),(0,-1),(-1,0),(-1,-1),(-1,1),(1,-1)}:
            if (node.y+d[0] < 0 or node.y+d[0] > BOARD_HIGHT-1) or (node.x+d[1] < 0 or node.x+d[1] > BOARD_WIDTH-1):
                continue
            if self.board[node.y+d[0]][node.x+d[1]].is_bomb():
                count += 1
        return count

    def flag_node(self, node):
        if not node.is_revealed():
            node.toggle_flag()

    def check_game_over(self):
        for y in self.board:
            for x in y:
                if x.is_bomb() and x.is_revealed():
                    return 2
        for y in self.board:
            for x in y:
                if not x.is_bomb() and not x.is_revealed():
                    return 0
        return 1

    def reveal_bombs(self):
        for y in self.board:
            for x in y:
                if x.is_bomb() and not x.is_revealed():
                    x.reveal_bomb()

    def toggle_ending_screen(self):
        if self.winner:
            self.ending_screen = not self.ending_screen

    def draw(self):
        # draw pieces
        for y in self.board:
            for x in y:
                action = x.draw()
                if action == 'hovered' and not self.winner:
                    self.highlight_node(x)
                elif action == 'left_clicked' and not self.winner:
                    self.reveal_nodes(x)
                elif action == 'right_clicked' and not self.winner:
                    self.flag_node(x)

        # end screen
        if self.winner and self.ending_screen:
            self.reveal_bombs()
            end_text = TEXT_FONT.render("WINNER!", 1, BLACK)
            if self.winner == 2:
                end_text = TEXT_FONT.render("LOSS!", 1, BLACK)
            pygame.draw.rect(screen, WHITE, END_SCREEN)
            pygame.draw.rect(screen, BLACK, END_SCREEN, 5)
            screen.blit(end_text, (END_SCREEN.x+(END_SCREEN.width - end_text.get_width())//2, END_SCREEN.y+END_SCREEN.height//10))
            end_text = TEXT_FONT_2.render("Press 'r' to reset game.", 1, BLACK)
            screen.blit(end_text, (END_SCREEN.x+(END_SCREEN.width - end_text.get_width())//2, END_SCREEN.y+END_SCREEN.height//2))
            end_text = TEXT_FONT_2.render("Press 'h' to show board.", 1, BLACK)
            screen.blit(end_text, (END_SCREEN.x+(END_SCREEN.width - end_text.get_width())//2, END_SCREEN.y+END_SCREEN.height/1.4))

def main():

    minesweeper = Game()
    clock = pygame.time.Clock()
    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    minesweeper.reset_game()
                if event.key == pygame.K_h:
                    minesweeper.toggle_ending_screen()
        minesweeper.draw()

        pygame.display.update()

if __name__ == '__main__':
    main()