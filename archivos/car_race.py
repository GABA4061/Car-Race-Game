#importar librerías e iniciar pygame
import pygame
import time
import math
from time import sleep
pygame.init()
pygame.font.init()

#funciones 
def scale_image(img, factor):
    size = round(img.get_width() * factor), round(img.get_height() * factor)
    return pygame.transform.scale(img, size)

def rotate_image(win, image, top_left, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(topleft=top_left).center)
    win.blit(rotated_image, new_rect.topleft)

def blit_text_center(win, font, text):
    render = font.render(text, 1, (200, 200, 200))
    win.blit(render, (win.get_width()/2 - render.get_width()/2, win.get_height()/2 - render.get_height()/2))

#Título e ícono del juego
pygame.display.set_caption("Car Race")
icon = pygame.image.load('player1.png')
pygame.display.set_icon(icon)
clock = pygame.time.Clock()
#Imágenes
GRASS = scale_image(pygame.image.load('grass.jpg'), 1.2)
TRACK = pygame.image.load('track.png')
TRACK_BORDER = pygame.image.load('track_border.png')
TRACK_BORDER_MASK = pygame.mask.from_surface(TRACK_BORDER)
player1 = scale_image(pygame.image.load('player1.png'), 1.15)
player2 = scale_image(pygame.image.load('player2.png'), 1.15)
MAIN_FONT = pygame.font.SysFont("comicsans", 44)
FINISH = pygame.image.load('finish.png')
FINISH_MASK = pygame.mask.from_surface(FINISH)
FINISH_LINE = pygame.image.load('finish_line.png')
FINISH_LINE_MASK = pygame.mask.from_surface(FINISH_LINE)
FINISH_POSITION = (0, 0)
FINISH_LINE_POSITION = (0, 0)


#Ventana de visualización
WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
win = pygame.display.set_mode((WIDTH, HEIGHT))

FPS = 60

#Menú principal
class Game():
    def __init__(self):
        pygame.init()
        self.running, self.playing = True, False
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False
        self.DISPLAY_W, self.DISPLAY_H = WIDTH, HEIGHT
        self.display = pygame.Surface((self.DISPLAY_W, self.DISPLAY_H))
        self.window = pygame.display.set_mode(((WIDTH, HEIGHT)))
        self.font_name = '8-BIT WONDER.TTF'
        #self.font_name = pygame.font.get_default_font()
        self.BLACK, self.WHITE = (0, 0, 0), (255, 255, 255)
        self.main_menu = MainMenu(self)
        self.credits = CreditsMenu(self)
        self.curr_menu = self.main_menu
        self.started = False


    def game_loop(self):
        while self.playing:
            self.check_events()
            if self.START_KEY:
                self.playing = True 
            pygame.init()
            clock.tick(FPS)
            draw(win, images, player1, player2)    
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            move_player1(player1)
            move_player2(player2)
            collision(player1, player2)  
            pygame.display.update()
            self.reset_keys()
            
   
    def check_events(self):
        for event in pygame.event.get():
             #Revisar si el juego ha sido cerrado
            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
                self.curr_menu.run_display = False
                pygame.quit()         

            if event.type == pygame.KEYDOWN:
                 #Revisar si alguna tecla ha sido presionada
                if event.key == pygame.K_RETURN:
                    self.START_KEY = True
                if event.key == pygame.K_BACKSPACE:
                    self.BACK_KEY = True
                if event.key == pygame.K_DOWN:
                    self.DOWN_KEY = True
                if event.key == pygame.K_UP:
                    self.UP_KEY = True
    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False

    #Dibujar texto en pantalla
    def draw_text(self, text, size, x, y ):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, self.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.display.blit(text_surface, text_rect)

 #Visualizar pantalla y dibujar el cursor
class Menu():
    def __init__(self, game):
        self.game = game
        self.mid_w, self.mid_h = self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2
        self.run_display = True
        self.cursor_rect = pygame.Rect(0, 0, 20, 20)
        self.offset = - 100
        
    def blit_screen(self):
        self.game.window.blit(self.game.display, (0, 0))
        pygame.display.update()
        self.game.reset_keys()
        
    def draw_cursor(self):
        self.game.draw_text('*', 15, self.cursor_rect.x, self.cursor_rect.y)



class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Start"
        self.startx, self.starty = self.mid_w, self.mid_h + 30
        self.creditsx, self.creditsy = self.mid_w, self.mid_h + 70
        self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
#Iniciar pantalla del menu principal
    def display_menu(self):
        self.run_display = True
        while self.run_display: #Cuando el juego esté corriendo
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.BLACK) #Poner fondo negro
            self.game.draw_text('Car Race', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 20) #dibujar texto en pantalla
            self.game.draw_text("Comenzar", 20, self.startx, self.starty)
            self.game.draw_text("Creditos", 20, self.creditsx, self.creditsy)
            self.draw_cursor() #dibujar cursor
            self.blit_screen() #inicializar pantalla

    #mover el cursor dependiendo el estado del cursor, por ejemplo: si está en start y le das click a bajar, cammbiará a creditos
    def move_cursor(self):
        if self.game.DOWN_KEY:
            if self.state == 'Start':
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = 'Credits'

            elif self.state == 'Credits':
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = 'Start'
        elif self.game.UP_KEY:
            if self.state == 'Start':
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = 'Credits'

            elif self.state == 'Credits':
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = 'Start'

    def check_input(self):
        self.move_cursor()
        #Si el jugador le da enter a Comenzar, el juego se inicia
        if self.game.START_KEY:
            if self.state == 'Start':
                self.game.playing = True
            elif self.state == 'Credits':
                self.game.curr_menu = self.game.credits
            self.run_display = False

#Pantalla de creditos
class CreditsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            #Checkea las teclas presionadas
            self.game.check_events()
            if self.game.START_KEY or self.game.BACK_KEY:
                self.game.curr_menu = self.game.main_menu
                self.run_display = False
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text('Creditos', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 20)
            self.game.draw_text('Hecho por Gabriela Casavilca', 15, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 10)
            self.blit_screen()
            
#Creación de clase para el juego de carreras en sí
class AbstractCar:
    def __init__(self, max_vel, rotation_vel):
        #variables necesarias 
        self.img = self.IMG
        self.max_vel = max_vel
        self.vel = 0
        self.rotation_vel = rotation_vel
        self.angle = 90
        self.x, self.y = self.START_POS
        self.acceleration = 0.1

    def rotate(self, left=False, right=False):
        if left:
            self.angle += self.rotation_vel
        elif right:
            self.angle -= self.rotation_vel

    def draw(self, win):
        rotate_image(win, self.img, (self.x, self.y), self.angle)

    def move_forward(self):
        self.vel = min(self.vel + self.acceleration, self.max_vel)
        self.move()

    def move_backward(self):
        self.vel = max(self.vel - self.acceleration, -self.max_vel/2)
        self.move()

    def move(self):
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel

        self.y += vertical
        self.x += horizontal

    def collide(self, mask, x=0, y=0):
        car_mask = pygame.mask.from_surface(self.img)
        offset = (int(self.x - x), int(self.y - y))
        poi = mask.overlap(car_mask, offset)
        return poi

    def reset(self):
        self.x, self.y = self.START_POS
        self.angle = 90
        self.vel = 0


class Player1Car(AbstractCar):
    IMG = player1
    #Posición inicial del jugador 1
    START_POS = (260, 494)

    def reduce_speed(self):
        self.vel = max(self.vel - self.acceleration / 2, 0)
        self.move()

    def bounce(self):
        self.vel = -self.vel/2
        self.move()
#Movimiento de jugador 1 según las teclas presionadas
def move_player1(player1):
    keys = pygame.key.get_pressed()
    moved = False

    if keys[pygame.K_a]:
        player1.rotate(left=True)
    if keys[pygame.K_d]:
        player1.rotate(right=True)
    if keys[pygame.K_w]:
        moved = True
        player1.move_forward()
    if keys[pygame.K_s]:
        moved = True
        player1.move_backward()

    if not moved:
        player1.reduce_speed()

def move_player2(player2):
    keys = pygame.key.get_pressed()
    moved = False

    if keys[pygame.K_LEFT]:
        player2.rotate(left=True)
    if keys[pygame.K_RIGHT]:
        player2.rotate(right=True)
    if keys[pygame.K_UP]:
        moved = True
        player2.move_forward()
    if keys[pygame.K_DOWN]:
        moved = True
        player2.move_backward()
    if not moved:
        player2.reduce_speed()
#Funciones iguales para el jugador 2
class Player2Car(AbstractCar):
    IMG = player2
    START_POS = (260, 520)
    
    def reduce_speed(self):
        self.vel = max(self.vel - self.acceleration / 2, 0)
        self.move()
    
    def bounce(self):
        self.vel = -self.vel/2
        self.move()
        
    def reset(self):
        self.x, self.y = self.START_POS
        self.angle = 90
        self.vel = 0

#Si el jugador choca con el borde de la pista de carreras, rebotará hacia atrás
def collision(player1, player2):
    if player1.collide(TRACK_BORDER_MASK) != None:
        player1.bounce()
    if player2.collide(TRACK_BORDER_MASK) != None:
        player2.bounce()
        
    finish_poi_collide = player1.collide(FINISH_MASK, *FINISH_POSITION)
    finish2_poi_collide = player2.collide(FINISH_MASK, *FINISH_POSITION)
    if finish_poi_collide != None:
        if player1.collide(FINISH_MASK):
            player1.bounce()
            print("not finish")
    if finish2_poi_collide != None:
        if player2.collide(FINISH_MASK):
            player2.bounce()
            print("not finish")

    finish_line_collide = player1.collide(FINISH_LINE_MASK, *FINISH_LINE_POSITION)
    finish2_line_collide = player2.collide(FINISH_LINE_MASK, *FINISH_LINE_POSITION)
    if finish_line_collide != None:
        if player1.collide(FINISH_LINE_MASK):
            print("player 1 win")
            player1.reset()
            player2.reset()   
            blit_text_center(win, MAIN_FONT, f"Jugador 1 ha ganado!")
            pygame.display.update()
            time.sleep(3)         
    if finish2_line_collide != None:
        if player2.collide(FINISH_LINE_MASK):
            print("player 2 win")
            player1.reset()
            player2.reset()
            blit_text_center(win, MAIN_FONT, f"Jugador 2 ha ganado!")
            pygame.display.update()
            time.sleep(3)
#display images

def draw(win, images, player1, player2):
    for img, pos in images:
        win.blit(img, pos)

    player1.draw(win)
    player2.draw(win)
    pygame.display.update()
            
#game loop

images = [(GRASS, (0, 0)), (TRACK, (0, 0)), (FINISH, FINISH_POSITION), (TRACK_BORDER, (0, 0))]
player1 = Player1Car(3, 3)
player2 = Player2Car(3, 3)
game = Game()
while game.running:
    pygame.init()
    game.curr_menu.display_menu()
    game.game_loop()
pygame.quit()