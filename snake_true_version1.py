import pygame
import random
import os

pygame.init()
size = width, height = 600, 650
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
clock2 = pygame.time.Clock()
fps = 60
running = True


def load_image(name, colorkey = None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    image = image.convert_alpha()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey)
    return image    


class GUI:
    def __init__(self, num):
        self.elements = []
        self.nums = {}
        self.num = num
        self.game = False
        
    def add_element(self, element,num):
        self.elements.append(element)
        self.nums[element] = num
        
    def render(self, surface):
        for element in self.elements:
            if self.nums[element] == self.num:
                render = getattr(element, "render", None)
                if callable(render):
                    element.render(surface)
                
    def update(self):
        for element in self.elements:
            if self.nums[element] == self.num:
                update= getattr(element, "update", None)
                if callable(update):
                    element.update()
                
    def get_event(self,event):
        for element in self.elements:
            if self.nums[element] == self.num:
                get_event = getattr(element, "get_event", None)
                if callable(get_event):
                    element.get_event(event)

    def change(self,num):
        self.num = num


class Label:
    def __init__(self, rect, text, bgcolor=pygame.Color("white")):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.bgcolor = bgcolor
        self.font_color = (0, 0, 0)
        # Рассчитываем размер шрифта в зависимости от высоты
        self.font = pygame.font.Font(None, self.rect.height - 4)
        self.rendered_text = None
        self.rendered_rect = None

    def render(self, surface):
        if self.bgcolor != -1:
            surface.fill(self.bgcolor, self.rect)
        self.rendered_text = self.font.render(self.text, 1, self.font_color)
        self.rendered_rect = self.rendered_text.get_rect(x=self.rect.x + 2, centery=self.rect.centery)
        # выводим текст
        surface.blit(self.rendered_text, self.rendered_rect)


class Button(Label):
    def __init__(self, rect, text, color, num, surface):
        super().__init__(rect, text)
        self.bgcolor = color
        # при создании кнопка не нажата
        self.pressed = False
        #self.number = num
        self.surface = surface

    def render(self, surface):
        surface.fill(self.bgcolor, self.rect)
        self.rendered_text = self.font.render(self.text, 1, self.font_color)
        if not self.pressed:
            color1 = pygame.Color("white")
            color2 = pygame.Color("black")
            self.rendered_rect = self.rendered_text.get_rect(x=self.rect.x + 5, centery=self.rect.centery)
        else:
            color1 = pygame.Color("black")
            color2 = pygame.Color("white")
            self.rendered_rect = self.rendered_text.get_rect(x=self.rect.x + 7, centery=self.rect.centery + 2)

        # рисуем границу
        pygame.draw.rect(surface, color1, self.rect, 2)
        pygame.draw.line(surface, color2, (self.rect.right - 1, self.rect.top), (self.rect.right - 1, self.rect.bottom),
                         2)
        pygame.draw.line(surface, color2, (self.rect.left, self.rect.bottom - 1),
                         (self.rect.right, self.rect.bottom - 1), 2)
        # выводим текст
        surface.blit(self.rendered_text, self.rendered_rect)

    def get_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.pressed = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.pressed :
            if  gui.num == 4 :
                gui.change(0)

            elif gui.num == 0 and self.text == "Легкий":
                snake.lifetrue()
                nums1.__init__((width-50,0,50,50),"0")
                gui.change(1)
            elif gui.num == 0 and self.text == "Сложный":
                snake3.lifetrue()
                nums3.__init__((width-50,0,50,50),"0")
                gui.change(3)
            elif gui.num == 5:
                gui.change(0)
            self.pressed = False


class Board:
    def __init__(self):
        self.width = 24
        self.height = 24
        self.cell_size = 25
        self.top = 50
        self.left = 0
        self.board = [[(0, (0,205,102)) for _ in range(self.width)] for _ in range(self.height)]

    def render(self, surface):
        for i in range(self.height):
            for k in range(self.width):
                pygame.draw.rect(surface, (255, 255, 255), 
                                [self.left + k * self.cell_size,
                                self.top + i * self.cell_size,
                                self.cell_size,
                                self.cell_size], 1)
                pygame.draw.rect(surface, self.board[i][k][1], 
                                [self.left + k * self.cell_size + 1,
                                self.top + i * self.cell_size + 1,
                                self.cell_size - 2,
                                self.cell_size - 2],0)


class Cell:
    def __init__(self, x_y, color):
        self.x, self.y = x_y
        self.color = color
        
    def move(self, new):
        self.x, self.y = new

    def get_info(self):
        return (self.x, self.y), self.color


class Snake(Board):
    def __init__(self):
        super().__init__()
        self.x = 4
        self.y = 2
        self.len_body = 3
        self.snake = [Cell((self.x - i, self.y), pygame.Color('purple')) for i in range(self.len_body)]
        self.options_direction = {"Down": (0, 1), "Right": (1, 0),
                                  "Up": (0, -1), "Left": (-1, 0)}
        self.direction = [self.options_direction["Right"] for i in range(self.len_body)]
        self.dot_change_direction = []
        self.timer = 0
        self.apple = 0
        self.apples = [Apple(self.board) for i in range(10)]

    def get_event(self, event):
        num = sum([pygame.key.get_pressed()[pygame.K_RIGHT], pygame.key.get_pressed()[pygame.K_DOWN], pygame.key.get_pressed()[pygame.K_UP], pygame.key.get_pressed()[pygame.K_LEFT]])
        if event.type == pygame.KEYDOWN and num == 1:
            if event.key == pygame.K_RIGHT and (self.direction[0] != self.options_direction['Right'] and self.direction[0] != self.options_direction['Left']):
                self.dot_change_direction.append((self.snake[0].get_info()[0], self.options_direction['Right']))
                self.direction[0] = self.dot_change_direction[-1][1]
            elif event.key == pygame.K_DOWN and (self.direction[0] != self.options_direction['Down'] and self.direction[0] != self.options_direction['Up']):
                self.dot_change_direction.append((self.snake[0].get_info()[0], self.options_direction['Down']))
                self.direction[0] = self.dot_change_direction[-1][1]
            elif event.key == pygame.K_UP and (self.direction[0] != self.options_direction['Up'] and self.direction[0] != self.options_direction['Down']):
                self.dot_change_direction.append((self.snake[0].get_info()[0], self.options_direction['Up']))
                self.direction[0] = self.dot_change_direction[-1][1]
            elif event.key == pygame.K_LEFT and (self.direction[0] != self.options_direction['Left'] and self.direction[0] != self.options_direction['Right']):
                self.dot_change_direction.append((self.snake[0].get_info()[0], self.options_direction['Left']))
                self.direction[0] = self.dot_change_direction[-1][1]

    def update(self, val=None):
        self.board = [[(0, (0, 205, 102)) for i in range(self.width)] for k in range(self.height)]
        x,y = self.apples[self.apple].get_coord()
        self.board[y][x] = (2, (0, 205, 102))
        flag = True

        for i in range(len(self.snake)):
            x, y = self.snake[i].get_info()[0]
            new_x, new_y = (x + self.direction[i][0]), (y + self.direction[i][1])
            n = None
            for k in self.dot_change_direction:
                if k[0] == (new_x, new_y):
                    self.direction[i] = k[1]
                    if i == len(self.snake) - 1:
                        n = self.dot_change_direction.index(k)

            if n is not None:
                del self.dot_change_direction[n]

            self.snake[i].move((new_x, new_y))

        coords_snake = [i.get_info()[0] for i in self.snake]
        for i in range(len(self.snake)):
            for k in range(len(coords_snake)):
                if i != k and self.snake[i].get_info()[0] == coords_snake[k]:
                    score_num = "Счет: "+str(self.apple)
                    score.__init__((100, 100, width - 100, 50), score_num, -1)
                    gui.change(4)
                    break

        x, y = self.snake[0].get_info()[0]

        if x>=self.width or x<0 or y<0 or y>=self.height :
            score_num = "Счет: "+str(self.apple)
            score.__init__((100, 100, width - 100, 50), score_num, -1)
            gui.change(4)
            flag = False
        
        if flag:
            if self.board[y][x] == (2, (0, 205, 102)):
                self.apple+=1
                eval("nums"+str(gui.num)).__init__((width-50, 0, 50, 50), str(self.apple))
                if self.apple == 10 and gui.num == 1:
                    score2.__init__((100, 100, width - 100, 50), "Счет: 10", -1)
                    gui.change(5)
                elif self.apple %10 == 0 and gui.num == 3 and self.apple!=30:
                    self.apples += [Apple(self.board) for i in range(10)]
                elif self.apple == 30:
                    score2.__init__((100, 100, width - 100, 50), "Счет: 30", -1)
                    gui.change(5)
                    
                snake_before = self.snake
                x1,y1 = self.direction[0]
                self.snake = [Cell((x+x1,y+y1), pygame.Color("purple"))]+ snake_before
                a = self.direction
                b = self.direction[0]
                self.dot_change_direction.append((self.snake[0].get_info()[0], b))
                self.direction = [b]+a

            for i in self.snake:
                x, y = i.get_info()[0]
                self.board[y][x] = (1, i.get_info()[1])                
        
    def lifetrue(self):
        self.__init__()
        
    def draw_apples(self):
        x,y = self.apples[self.apple].get_coord()
        sprite_apple.rect.x = x*self.cell_size
        sprite_apple.rect.y = y*self.cell_size + self.top
        apple_sprites.draw(screen)


class Apple():
    def __init__(self, board):
        
        self.x_apple = random.randint(1, 22)
        self.y_apple = random.randint(1, 22)

        while board[self.y_apple][self.x_apple][0] != 0:
            self.x_apple = random.randint(1, 22)
            self.y_apple = random.randint(1, 22)
            
    def get_coord(self):
        return self.x_apple, self.y_apple


#
screen_rect = (0, 0, width, height)
gravity = 1


class Particle(pygame.sprite.Sprite):
    # сгенерируем частицы разного размера
    image_apple = load_image("apple.png",-1)
    image_apple = pygame.transform.scale(image_apple, (25, 25))    
    fire = [image_apple]
    for i  in range(5):
        fire.append(pygame.transform.scale(fire[0], (30, 30)))

    def __init__(self, pos, dx, dy):
        super().__init__(all_sprites)
        self.image = random.choice(self.fire)
        self.rect = self.image.get_rect()

        # у каждой частицы своя скорость - это вектор
        self.velocity = [dx, dy]
        # и свои координаты
        self.rect.x, self.rect.y = pos

        # гравитация будет одинаковой
        self.gravity = gravity

    def update(self, v= None):
        # применяем гравитационный эффект: 
        # движение с ускорением под действием гравитации
        self.velocity[1] += self.gravity
        # перемещаем частицу
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        # убиваем, если частица ушла за экран
        if not self.rect.colliderect(screen_rect):
            self.kill()


#
def create_particles(position):
    # количество создаваемых частиц
    particle_count = 7
    # возможные скорости
    numbers = range(-5, 6)
    for _ in range(particle_count):
        Particle(position, random.choice(numbers), random.choice(numbers))


#
class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(fire_sprites )
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns, sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]
        
        
        
    


gui = GUI(0)
gui.add_element(Label((0, 0, width, 50), "  Добро пожаловать в игру ЗМЕЙКА!"), 0)
gui.add_element(Label((50, 70, 110, 40), "Уровни:", -1), 0)
but_light = Button((60, 120, 120, 40), "Легкий", (255, 255, 255), 1, screen)
gui.add_element(but_light, 0)
gui.add_element(Label((0, 400, 200, 40), "Избегайте столкновений с краями поля и хвостом.", -1), 0)
gui.add_element(Label((200, 500, 200, 80), "Удачи!", -1), 0)
board = Board()
gui.add_element(board, 1)
gui.add_element(Label((0, 0, width, 50), "  Соберите 10 яблок  "), 1)
gui.add_element(Label((0, 0, width, 50), "  Вы проиграли  "), 4)
but_menu = Button((100, 200, 280, 40), "вернуться в менюшку", (255, 255, 255), 4, screen)
gui.add_element(but_menu, 4)
nums1 = Label((width-50, 0, 50, 50), "0")
gui.add_element(nums1, 1)
gui.add_element(Label((0, 0, width, 50), "  Вы победили!"), 5)
but_menu2 = Button((100, 200, 280, 40), "вернуться в менюшку", (255, 255, 255), 4, screen)
gui.add_element(but_menu2, 5)
score = Label((100, 100, width - 100, 50), "Счет: 0", -1)
gui.add_element(score, 4)
score2 = Label((100, 100, width - 100, 50), "Счет: 0", -1)
gui.add_element(score2, 5)
but_hard = Button((60, 220, 120, 40), "Сложный", (255, 255, 255), 1, screen)
gui.add_element(but_hard, 0)
board3 = Board()
gui.add_element(board3, 3)
snake3 = Snake()
gui.add_element(snake3, 3)
nums3 = Label((width-50, 0, 50, 50), "0")
gui.add_element(nums3, 3)
gui.add_element(Label((0, 0, width-50, 50), "  Соберите 30 яблок  "), 3)


sprite = pygame.sprite.Sprite()
# определим его вид
sprite.image = load_image("snake_image.png", -1)
# и размеры
sprite.rect = sprite.image.get_rect()
snake_sprites = pygame.sprite.Group()
snake_sprites.add(sprite)
sprite.rect.x = 200
sprite.rect.y = 100

sprite_apple = pygame.sprite.Sprite()
image_apple = load_image("apple.png", -1)
image_apple = pygame.transform.scale(image_apple, (25, 25))
sprite_apple.image = image_apple
apple_sprites = pygame.sprite.Group()
apple_sprites.add(sprite_apple)
sprite_apple.rect = sprite_apple.image.get_rect()


all_sprites = pygame.sprite.Group()
fire_sprites = pygame.sprite.Group()


snake = Snake()
gui.add_element(snake,1)

fire = AnimatedSprite(load_image("firework2.png"), 15, 1, 150, 300)
fire2 = AnimatedSprite(load_image("fire2.jpg"), 4, 4, 400, 100)


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
                        # создаем частицы по щелчку мыши
            create_particles(pygame.mouse.get_pos())        
        gui.get_event(event)
    screen.fill((0,205,102))
    all_sprites.update()
    clock.tick(40)

    gui.render(screen)
    
    if gui.num == 0 :
        snake_sprites.draw(screen)
        all_sprites.draw(screen)
    if gui.num == 4 :
        all_sprites.draw(screen)
    if gui.num == 5:
        fire_sprites.draw(screen)
        fire_sprites.update()
        clock.tick(10)
    else:
        if gui.num == 1:
            snake.draw_apples()
        if gui.num == 3:
            snake3.draw_apples()
        if gui.num == 1 and pygame.time.get_ticks() - snake.timer > 300:
            gui.update()  
            snake.timer = pygame.time.get_ticks()
            #snake.draw_apples()
        if gui.num == 3 and pygame.time.get_ticks() - snake3.timer > 150:
            gui.update()  
            snake3.timer = pygame.time.get_ticks()  
            #snake3.draw_apples()

    pygame.display.flip()

pygame.quit()
all_sprites.empty()