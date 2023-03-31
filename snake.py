import pygame
import time
import random
from sys import exit

pygame.init()

WIDTH, HEIGHT = 640, 640

window = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Snake")

class Fruit():
    def __init__(self) -> None:
        spot_not_found = True
        while spot_not_found:
            self.pos = random.randint(0, 31), random.randint(0, 31)
            collide = False
            for tail in tails:
                if tail.pos == self.pos:
                    collide = True
            if collide == False:
                spot_not_found = False


class Tail():
    def __init__(self, pos) -> None:
        self.pos = pos

class Snake():
    def __init__(self) -> None:
        self.speed = 0.5
        self.length = 1
        self.pos = 10, 10
        self.direction = 0 # 0 = up, 1 = left, 2 = down, 3 = right

    def move(self, render):
        global fruit
        tails.append(Tail(self.pos))

        if self.direction == 0:
            x, y = self.pos
            y+=1
            self.pos = (x, y)

        if self.direction == 1:
            x, y = self.pos
            x-=1
            self.pos = (x, y)

        if self.direction == 2:
            x, y = self.pos
            y-=1
            self.pos = (x, y)

        if self.direction == 3:
            x, y = self.pos
            x+=1
            self.pos = (x, y)

        for tail in tails:
            if tail.pos == self.pos:
                render.is_game_over = True
                render.gameover()
        
        x, y = self.pos
        if x < 0 or x > 31 or y < 0 or y > 31:
            render.is_game_over = True
            render.gameover()

        if fruit.pos == self.pos:
            fruit = Fruit()
            self.length+=1
            render.score+=1
            if self.speed > 0.1:
                self.speed -= 0.05
            
        else:
            try:
                tail = tails[0]
                tails.remove(tail)

            except (ValueError, IndexError):
                pass
        

class Button():
    def __init__(self, pos, size, buttonText) -> None:
        self.x, self.y = pos
        self.text = buttonText
        self.font = pygame.font.Font('freesansbold.ttf', 32)
        self.width, self.height = size
        self.normal = (110, 110, 110)
        self.hovered = (80, 80, 80)
        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.buttonText = self.font.render(buttonText, True, (20, 20, 20))

    def update(self):
        mousePos = pygame.mouse.get_pos()
        self.buttonSurface.fill(self.normal)
        r, g, b = self.normal
        pygame.draw.rect(self.buttonSurface, (r - 15, g - 15, b - 15), (5, 5, self.width -10, self.height - 10))
        self.buttonSurface.blit(self.buttonText, (self.buttonRect.width/2 - self.buttonText.get_rect().width/2, self.buttonRect.height/2 - self.buttonText.get_rect().height/2))
        window.blit(self.buttonSurface, self.buttonRect)
        if self.buttonRect.collidepoint(mousePos):
            self.buttonSurface.fill(self.hovered)
            r, g, b = self.hovered
            pygame.draw.rect(self.buttonSurface, (r - 15, g - 15, b - 15), (5, 5, self.width -10, self.height - 10))
            self.buttonSurface.blit(self.buttonText, (self.buttonRect.width/2 - self.buttonText.get_rect().width/2, self.buttonRect.height/2 - self.buttonText.get_rect().height/2))
            window.blit(self.buttonSurface, self.buttonRect)
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                return "clicked"
        return "not clicked"



class Render():
    def __init__(self) -> None:
        self.is_game_over = False
        self.hasnt_started = True
        self.fade = 0
        self.score = 0
        self.fadeSurface = pygame.Surface(window.get_size(), pygame.SRCALPHA).convert_alpha()
        self.fadeSurface.fill((70, 70, 70))
        self.font = pygame.font.Font('freesansbold.ttf', 32)
        text = self.font.render("Game over!", True, (255, 0, 0))
        textRect = text.get_rect()
        textRect.center = (WIDTH/2, HEIGHT/2-50)
        text = self.font.render("Score: " + str(self.score), True, (255, 255, 255))
        textRect = text.get_rect()
        textRect.center = (WIDTH/2, HEIGHT/2)
        self.fadeSurface.blit(text, textRect)

    def render(self, snake):
        self.fadeSurface.set_alpha(self.fade)
        window.fill((20, 20, 20))

        for tail in tails:
            x, y = tail.pos
            x = x*20
            y = y*20
            pygame.draw.rect(window, ( 127, 127, 127), (x, y, 20, 20))

        x, y = snake.pos
        x *= 20
        y *= 20
        pygame.draw.rect(window, (140, 140, 140), (x, y, 20, 20))
        if snake.direction == 0:
            pygame.draw.rect(window, (0, 140, 0), (x+2, y+14, 4, 4))
            pygame.draw.rect(window, (0, 140, 0), (x+14, y+14, 4, 4))
        if snake.direction == 1:
            pygame.draw.rect(window, (0, 140, 0), (x+2, y+14, 4, 4))
            pygame.draw.rect(window, (0, 140, 0), (x+2, y+2, 4, 4))
        if snake.direction == 2:
            pygame.draw.rect(window, (0, 140, 0), (x+2, y+2, 4, 4))
            pygame.draw.rect(window, (0, 140, 0), (x+14, y+2, 4, 4))
        if snake.direction == 3:
            pygame.draw.rect(window, (0, 140, 0), (x+14, y+14, 4, 4))
            pygame.draw.rect(window, (0, 140, 0), (x+14, y+2, 4, 4))

        
        x, y = fruit.pos
        x = x*20
        y = y*20
        pygame.draw.rect(window, ( 255, 0, 0), (x, y, 20, 20))
        window.blit(self.fadeSurface, (0, 0))
        if self.is_game_over or self.hasnt_started:
            self.update()

    def gameover(self):
        self.fadeSurface.fill((70, 70, 70))
        self.font = pygame.font.Font('freesansbold.ttf', 32)
        text = self.font.render("Game over!", True, (255, 255, 255))
        textRect = text.get_rect()
        textRect.center = (WIDTH/2, HEIGHT/2-50)
        self.fadeSurface.blit(text, textRect)
        text = self.font.render("Score: " + str(self.score), True, (255, 0, 0))
        textRect = text.get_rect()
        textRect.center = (WIDTH/2, HEIGHT/2)
        self.fadeSurface.blit(text, textRect)
        self.buttons = []
        self.buttons.append(Button((WIDTH/2-100, HEIGHT/2+50), (200, 50), "Continue"))
        self.buttons.append(Button((WIDTH/2-100, HEIGHT/2+120), (200, 50), "Quit"))

    def gamestart(self):
        self.fadeSurface.fill((70, 70, 70))
        self.fadeSurface.set_alpha(255)
        self.fade = 255
        self.buttons = []
        self.buttons.append(Button((WIDTH/2-100, HEIGHT/2-35), (200, 50), "Start"))
        self.buttons.append(Button((WIDTH/2-100, HEIGHT/2+35), (200, 50), "Quit"))

    def update(self):
        global fruit
        global snake
        for button in self.buttons:
            output = button.update()
            if output == "clicked":
                if button.text == "Continue" or button.text == "Start":
                    global tails
                    self.is_game_over = False
                    self.hasnt_started = False
                    self.fade = 0
                    self.score = 0
                    tails = []
                    fruit = Fruit()
                    snake = Snake()
                else:
                    exit()
            

tails = []
renderEngine = Render()
fruit = Fruit()
snake = Snake()



startTime = time.time()
renderEngine.gamestart()

while True:
    delta = time.time() - startTime

    if not renderEngine.is_game_over and not renderEngine.hasnt_started:

        if delta > snake.speed:
            snake.move(renderEngine)
            startTime = time.time()
            renderEngine.render(snake)
        
    else:
        if delta > 0.01:
            renderEngine.fade += 1
            startTime = time.time()
            renderEngine.render(snake)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_d and not renderEngine.is_game_over:
            snake.direction+=1
            if snake.direction == 4:
                snake.direction = 0
            renderEngine.render(snake)

        if event.type == pygame.KEYDOWN and event.key == pygame.K_a and not renderEngine.is_game_over:
            snake.direction-=1
            if snake.direction == -1:
                snake.direction = 3
            renderEngine.render(snake)

    

    pygame.display.flip()