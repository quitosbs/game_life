#code by ds:kito_ofc
#github: 
#9.09.2024
import pygame

class Field:

    def __init__(self, x, y):
        self.x, self.y = x, y
        self.mass = {}
        for i in range(y):
            row = []
            for j in range(x):
                row.append(0)
            self.mass[i] = row

    def get(self, x, y):
        return self.mass[y][x]
    
    def set(self, x, y, s):
        self.mass[y][x] = s

    def heighboors(self, x, y):
        val = 0
        for i in range(y-1, y+2):
            for j in range(x-1, x+2):
                if i != self.y and j != self.x:
                    if(i!=y or j!=x) and i>= 0 and j >= 0:
                        if self.get(j, i) == 1:
                            val += 1
        return val
    
    def check(self, x, y):
        if self.get(x, y) == 0 and self.heighboors(x, y) == 3:
            return 1
        elif self.get(x, y) == 1 and (self.heighboors(x, y) < 2 or self.heighboors(x, y) >3):
            return 0
        else:
            return self.get(x, y)

class Button:

    def __init__(self, x, y, i, j):
        self.pos_x, self.pos_y = x, y
        self.x, self.y = i, j
        self.rect = (pygame.Rect(pos_x, pos_y, 10, 10))
    
    def draw(self, color):
        pygame.draw.rect(screen, color, self.rect)

    def clicked(self, pos):
        return self.rect.collidepoint(pos)

pygame.init()
screen = pygame.display.set_mode((1366, 968))
pygame.display.set_caption('Press "SPACE" | Generation = 0')
clock = pygame.time.Clock()

game = Field(150, 150)
buttons = []
for i in range(150):
    for j in range(150):
        pos_x = i*1+i*10
        pos_y = j*1+j*10
        button = Button(pos_x, pos_y, i, j)
        buttons.append(button)

running = True
game_start = False
generation = 0
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            for button in buttons:
                if button.clicked(pos):
                    if game.get(button.x, button.y) == 0:
                        game.set(button.x, button.y, 1)          
                    elif game.get(button.x, button.y) == 1:
                        game.set(button.x, button.y, 0)  
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                game_start = True              

    screen.fill((255, 255, 255))
    for button in buttons:
        if game.get(button.x, button.y) == 0:
            button.draw((128, 128, 128))
        elif game.get(button.x, button.y) == 1:
            button.draw((0, 0, 0))

    if game_start:
        generation += 1
        pygame.display.set_caption(f'Generation = {generation}')
        g = Field(150, 150)
        for y in range(game.y):
            for x in range(game.x):
                g.set(x, y, game.check(x, y))
        if game.mass == g.mass:
            game_start = False
        game.mass = g.mass

    pygame.display.flip()

pygame.quit()