import pygame
import random

pygame.init()
size = width, height = 600, 650
screen = pygame.display.set_mode(size)
color={
'apple':'red', #цвет яблока
'snake':'black', #цвет змейки
'snake2':'purple', #цвет змейка,которая откусила яблоко
'welcome':'white' #цвет таблички добро пожаловать
}
clock = pygame.time.Clock()
fps = 60
running = True

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
            update= getattr(element, "update", None)
            if callable(update):
                element.update()
                
    def get_event(self,event):
        for element in self.elements:
            get_event = getattr(element, "get_event", None)
            if callable(get_event):
                element.get_event(event) 
    def set_num(self,num):
        self.num = num

        
    def get_num(self):
        return self.num


class Label:
    def __init__(self, rect, text, bgcolor=pygame.Color(color['welcome'])):
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
        self.number = num
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
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            num = gui.num
            
            
            if  gui.num == 4 and self.pressed:
                gui.set_num(0)
                
            elif gui.num == 0 and self.pressed:
                snake.lifetrue()
                nums.__init__((width-50,0,50,50),"0")
                gui.set_num(1)
            #elif gui.num == 5 and self.pressed:
                #gui.set_num(0)
                

                
                                
                


class Board:
    def __init__(self):
        self.width = 24
        self.height = 24
        self.cell_size = 25
        self.top = 50
        self.left = 0
        self.board = [[(0, (0,205,102)) for i in range(self.width)] for k in range(self.height)]
        #self.board[-1] = [(1, (0,205,102)) for i in range(self.width)]

    def render(self, surface):
        for i in range(self.height):
            for k in range(self.width):
                pygame.draw.rect(surface, (255, 255, 255), (
                    self.left + k * self.cell_size,
                    self.top + i * self.cell_size,
                    self.cell_size,
                    self.cell_size), 1)
                pygame.draw.rect(surface, self.board[i][k][1], (
                    self.left + k * self.cell_size + 1,
                    self.top + i * self.cell_size + 1,
                    self.cell_size - 2,
                    self.cell_size - 2,),0)


class Pixel:
    def __init__(self, coord, color):
        self.x = coord[0]
        self.y = coord[1]
        self.color = color

    def get_info(self):
        return (self.x, self.y), self.color

    def move(self, new_coord):
        self.x = new_coord[0]
        self.y = new_coord[1]


class Snake(Board):
    def __init__(self):
        super().__init__()
        self.x = random.randint(1,22)
        self.y = random.randint(1,22)
        self.len_body = 3
        self.snake = [Pixel((self.x - i, self.y), pygame.Color(color['snake'])) for i in range(self.len_body)]
        self.options_direction = {"Down": (0, 1), "Right": (1, 0),
                                  "Up": (0, -1), "Left": (-1, 0)}
        self.direction = [self.options_direction["Right"] for i in range(self.len_body)]
        self.dot_change_direction = []
        self.timer = 0
        self.apple = 0 #кол-во яблок
        self.apples = [Apple(self.board) for i in range(10)]

    def get_event(self, event):
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT and (self.direction[0] != self.options_direction['Right'] and
                                                self.direction[0] != self.options_direction['Left']):
                self.dot_change_direction.append((self.snake[0].get_info()[0], self.options_direction['Right']))
                self.direction[0] = self.dot_change_direction[-1][1]
            elif event.key == pygame.K_DOWN and (self.direction[0] != self.options_direction['Down'] and
                                                 self.direction[0] != self.options_direction['Up']):
                self.dot_change_direction.append((self.snake[0].get_info()[0], self.options_direction['Down']))
                self.direction[0] = self.dot_change_direction[-1][1]
            elif event.key == pygame.K_UP and (self.direction[0] != self.options_direction['Up'] and 
                                               self.direction[0] != self.options_direction['Down']):
                self.dot_change_direction.append((self.snake[0].get_info()[0], self.options_direction['Up']))
                self.direction[0] = self.dot_change_direction[-1][1]
            elif event.key == pygame.K_LEFT and (self.direction[0] != self.options_direction['Left'] and 
                                               self.direction[0] != self.options_direction['Right']):
                self.dot_change_direction.append((self.snake[0].get_info()[0], self.options_direction['Left']))
                self.direction[0] = self.dot_change_direction[-1][1]

    def move(self, x=0 , y=0):
        #перемещает змейку и возвращает старые координаты
        old_x=self.x
        old_y=self.y
        self.x=x
        self.y=y
        return old_x,old_y
    def update(self, val=None):
        self.board = [[(0, (0,205,102)) for i in range(self.width)] for k in range(self.height)]
        x,y = self.apples[self.apple].get_coord()
        self.board[y][x] = (1, pygame.Color(color['apple']))

        for i in range(len(self.snake)):
            x, y = self.snake[i].get_info()[0]
            #new_x, new_y = (x + self.direction[i][0]) % self.height, (y + self.direction[i][1]) % self.height
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


        x, y = self.snake[0].get_info()[0]
        #а вот она проверка на выход за границы
        if x>=self.width or x<0 or y<0 or y>=self.height:
            gui.set_num(4)
        else:       
            if self.board[y][x] == (1, pygame.Color("red")):
                self.apple+=1
                if self.apple == 10 and gui.num == 1:
                    gui.set_num(5)
                nums.__init__((width-50,0,50,50),str(self.apple))
                snake_before = self.snake
                x1,y1 = self.direction[0]
                self.snake = [Pixel((x+x1,y+y1), pygame.Color(color['snake2']))]+ snake_before
                a = self.direction
                b = self.direction[0]
                self.dot_change_direction.append((self.snake[0].get_info()[0], b))
                self.direction = [a[0]]+a
            for i in self.snake:
                x, y = i.get_info()[0]
                self.board[y][x] = (1, i.get_info()[1])  
    def lifetrue(self):
        self.__init__()
            





class Apple():
    def __init__(self, board):
        
        self.x_apple = random.randint(1, 22)
        self.y_apple = random.randint(1, 22)

        while board[self.y_apple][self.x_apple][0] != 0:
            self.x_apple = random.randint(1, 22)
            self.y_apple = random.randint(1, 22)
            
    def get_coord(self):
        return (self.x_apple, self.y_apple)
        






gui = GUI(0)
gui.add_element(Label((0, 0, width, 50), "  Добро пожаловать в игру ЗМЕЙКА!"), 0)
gui.add_element(Label((50, 70, 110, 40), "Уровни:", -1), 0)
but_light = Button((60, 120, 100, 40), "Легкий", (255, 255, 255), 1, screen)
#but_middle = Button((200, 130, 120, 40), "Средний", (255, 255, 255), 1, screen) 
gui.add_element(but_light, 0)
#gui.add_element(but_middle, 0)
gui.add_element(Label((20, 400, 200, 40), "Не врезайтесь в стенки и в хвост.", -1), 0)
gui.add_element(Label((200, 500, 200, 80), "Удачи!", (135, 206, 250)), 0)
board = Board()
gui.add_element(board, 1)
gui.add_element(Label((0, 0, width, 50), "  Соберите 10 яблок  "), 1)
gui.add_element(Label((0, 0, width, 50), "  Вы проиграли  "), 4)
but_menu = Button((100, 200, 280, 40), "вернуться в менюшку", (255, 255, 255), 4, screen)
gui.add_element(but_menu, 4 )
nums = Label((width-50,0,50,50),"0")
gui.add_element(nums,1)
gui.add_element(Label((0, 0, width, 50), "  Вы победили!"), 5)
but_menu2 = Button((100, 200, 280, 40), "вернуться в менюшку", (255, 255, 255), 4, screen)
gui.add_element(but_menu2, 5  )
# gui.add_element(Snake(), 1)
# gui.add_element(Apple(), 1)
# nap = {"Down": (0, 1), "Right": (1, 0),
#        "Up": (0, -1), "Left": (-1, 0)}
# napr = nap["Right"]


snake = Snake()
gui.add_element(snake,1)
#gui.add_element(Apple(),1)

while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        gui.get_event(event)
    screen.fill((0,205,102))

    gui.render(screen)

    if gui.num == 1 and pygame.time.get_ticks() - snake.timer > 200:
        gui.update()  
        snake.timer = pygame.time.get_ticks()

    pygame.display.flip()

pygame.quit()
