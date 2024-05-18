from pygame import *
'''Необходимые классы'''
#класс-родитель для спрайтов
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, width, height):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (width, height)) #вместе 55,55 - параметры
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.width = width
        self.height = height
        self.player_image = player_image

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

    def set_default(self,height):
        self.height = height
        self.image = transform.scale(image.load(self.player_image), (self.width, self.height))
    

class Player(GameSprite):
    def update_r(self):
        keys = key.get_pressed()
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_height - self.height:
            self.rect.y += self.speed
    def update_l(self):
       keys = key.get_pressed()
       if keys[K_w] and self.rect.y > 5:
           self.rect.y -= self.speed
       if keys[K_s] and self.rect.y < win_height - self.height:
           self.rect.y += self.speed
    def change_size(self):
        self.height *= 0.9
        self.image = transform.scale(image.load(self.player_image), (int(self.width), int(self.height)))


class Button():
    def __init__(self,button_x,button_y, button_width,button_height,
                button_color,button_text,button_text_size):
        self.rect = Rect(button_x,button_y,button_width,button_height)
        self.button_color = button_color
        self.button_text = font.SysFont('verdana',button_text_size).render(button_text,True,black)
    def fill(self):
        draw.rect(window,self.button_color,self.rect)
        window.blit(self.button_text,(self.rect.x + 20,self.rect.y + 20))
    def collidepoint(self,x,y):
        return self.rect.collidepoint(x,y)

#игровая сцена:
back = (200, 255, 255) #цвет фона (background)
black = (0,0,0)
red = (255,0,0)
win_width = 900
win_height = 600
window = display.set_mode((win_width, win_height))
window.fill(back)

mixer.init()
mixer.music.load("background_sound.ogg")
mixer.music.play(-1)

touch = mixer.Sound("touch_sound.ogg")
winsnd = mixer.Sound("win_sound.ogg")

#флаги, отвечающие за состояние игры
game = True
finish = True
clock = time.Clock()
FPS = 60

win_score = 3

p1 = 0
p2 = 0

racket_width = 50
racket_height = 150

#создания мяча и ракетки 
racket1 = Player('redracket.png', 30, win_height / 2 - racket_height / 2, 6, racket_width, racket_height)
racket2 = Player('greenracket.png', win_width - racket_width - 30, win_height / 2 - racket_height / 2, 6, racket_width, racket_height)
ball = GameSprite('tenis_ball.png', win_width/ 2 - 25, win_height /2 - 25, 4, 50, 50)

font.init()
font3 = font.Font(None, 35)
lose1 = font3.render('PLAYER 1 LOSE!', True, (180, 0, 0))
lose2 = font3.render('PLAYER 2 LOSE!', True, (180, 0, 0))

click_x = 0
click_y = 0

speed_x = 3
speed_y = 3

#СОЗДАНИЕ КНОПКИ
start_button_width = 200
start_button_height = 100
start_button = Button(win_width / 2 - start_button_width / 2,win_height / 3 - start_button_height / 2,start_button_width,start_button_height,red,"start",48)

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == MOUSEBUTTONDOWN:
            click_x,click_y = e.pos

  
    if finish != True:
        window.fill(back)
        racket1.update_l()
        racket2.update_r()
        ball.rect.x += speed_x
        ball.rect.y += speed_y

        if sprite.collide_rect(racket1, ball) or sprite.collide_rect(racket2, ball):
            touch.play()
            speed_x *= -1.2
            if sprite.collide_rect(racket1, ball):
                racket1.change_size()
            if sprite.collide_rect(racket2, ball):
                racket2.change_size()
            
      
       #если мяч достигает границ экрана, меняем направление его движения
        if ball.rect.y > win_height-50 or ball.rect.y < 0:
            speed_y *= -1

       #если мяч улетел дальше ракетки, выводим условие проигрыша для первого игрока
        if ball.rect.x < 0:
            p2 += 1
            ball.rect.x = win_width / 2 - 50/2
            ball.rect.y = win_height / 2 - 50/2
            speed_x = 3
            speed_x *= -1
            racket1.set_default(racket_height)
            racket2.set_default(racket_height)

       #если мяч улетел дальше ракетки, выводим условие проигрыша для второго игрока
        if ball.rect.x > win_width:
            p1 += 1
            ball.rect.x = win_width / 2 - 50/2
            ball.rect.y = win_height / 2 - 50/2
            speed_x = 3
            speed_x *= -1
            racket1.set_default(racket_height)
            racket2.set_default(racket_height)

        score = font3.render(str(p1) +":"+ str(p2),True,(180,0,0))
        window.blit(score,(450,20))

        if p1 >= win_score or p2 >= win_score:
            if p1 >= win_score:
                window.blit(lose2,(450,300))
                winsnd.play()
            if p2 >= win_score:
                window.blit(lose1,(450,300))
                winsnd.play()
            finish = True
            game = True
        
        racket1.reset()
        racket2.reset()
        ball.reset()

    else:
        if start_button.collidepoint(click_x,click_y):
            p1 = 0
            p2 = 0
            click_x = 0
            click_y = 0
            racket1.set_default(racket_height)
            racket2.set_default(racket_height)
            finish = False
        else:
            start_button.fill()

    display.update()
    clock.tick(FPS)
