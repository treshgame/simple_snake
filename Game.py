import pygame
import sys  #Ради функции exit()
import time     #Для Задержки экрана при конце игры
import random  #Для случайного размещения еды

class Game():
    def __init__(self):
        #Размер окна с игрой 
        self.screen_width = 720
        self.screen_height = 460

        #Цвета
        self.red = pygame.Color(255, 0, 0)
        self.green = pygame.Color(0, 255, 0)
        self.black = pygame.Color(0, 0, 0)
        self.white = pygame.Color(255, 255, 255)
        self.brown = pygame.Color(165, 42, 42)

        #Количество кадров в секунду
        self.fps_controller = pygame.time.Clock()

        #Результат. Сколько еды съедено
        self.score = 0

    def init_and_check_errors(self):
        #Проверка на ошибки
        check_errors = pygame.init()
        if check_errors[1] > 0:
            sys.exit()  #Закрывает игру, если есть ошибки
        else:
            print('Ok')
    
    def set_surface_and_title(self):
        #Установка Surface(Там, где будет всё двигаться) и названия окна
        self.play_surface = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption('Snake_debil')
    
    def event_loop(self, change_to):
        #Отслеживает нажатие клавиш игроком
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    change_to = "RIGHT"
                elif event.key == pygame.K_LEFT or event.key == ord('a'):
                    change_to = "LEFT"
                elif event.key == pygame.K_UP or event.key == ord('w'):
                    change_to = "UP"
                elif event.key == pygame.K_DOWN or event.key == ord('s'):
                    change_to = "DOWN"
                #Нажали escape
                elif event.key == pygame.K_ESCAPE:
                    #Закрывает окно при нажатии esc
                    pygame.quit()
                    sys.exit()
        return change_to

    def refsresh_screen(self):
        #Обновление экрана и задаём фпс
        pygame.display.flip()
        self.fps_controller.tick(30)
    
    def show_score(self, choice=1):
        #Функция отображения результата
        s_font = pygame.font.SysFont('monaco', 24)
        s_surf = s_font.render('Score: {0}'.format(self.score), True, self.black)
        s_rect = s_surf.get_rect()
        #Отображения результата сверху слева
        if choice == 1:
            s_rect.midtop = (80, 10)
        #Если game_over, то вывод надпись по центру
        else:
            s_rect.midtop = (360, 120)
        #Прямоугольник поверх surface
        self.play_surface.blit(s_surf, s_rect)

    def game_over(self):
        #Функция для вывода game_over и резульаттов, в случае заверешения игры
        go_font = pygame.font.SysFont('monaco', 72)
        go_surf = go_font.render('Game over', True, self.red)
        go_rect = go_surf.get_rect()
        go_rect.midtop = (360, 15)
        self.play_surface.blit(go_surf, go_rect)
        self.show_score(0)
        pygame.display.flip()
        #Ждёт три секунды и щакрывает окно
        time.sleep(3)
        pygame.quit()
        sys.exit()
        

class Snake():
    def __init__(self, snake_color):
        #Позиция головы и тела змеи
        self.snake_head_pos = [100, 50]
        #Начальное тело из трех элементов: голова, тело, хвост
        self.snake_body = [[100, 50], [90, 50], [80, 50]] 
        self.snake_color = snake_color
        #Изначальное направление змеи - вправо
        self.direction = "RIGHT"
        self.change_to = self.direction

    def validate_direction_and_change(self):
        #Изменение направления змеи, если оно не противоположно
        #текущему
        if any((self.change_to == "RIGHT" and self.direction != "LEFT",
                self.change_to == "LEFT" and self.direction != "RIGHT",
                self.change_to == "UP" and self.direction != "DOWN",
                self.change_to == "DOWN" and self.direction != "UP",)):
            self.direction = self.change_to
    def change_head_position(self):
        if self.direction == "RIGHT":
            self.snake_head_pos[0] += 5
        elif self.direction == "LEFT":
            self.snake_head_pos[0] -= 5
        elif self.direction == "UP":
            self.snake_head_pos[1] -= 5
        elif self.direction == "DOWN":
            self.snake_head_pos[1] += 5
    
    def snake_body_mechanism(self, score, food_pos, screen_width, screen_height):
        self.snake_body.insert(0, list(self.snake_head_pos))
        #Если съели еду
        if (self.snake_head_pos[0] == food_pos[0] and 
            self.snake_head_pos[1] == food_pos[1]):
            food_pos = [random.randrange(1, screen_width/10)*10,
                random.randrange(1, screen_height/10)*10]
            score += 1
        else:
            #Если не нашли еду, то убираем последний сегмент тела
            #А то змея будет расти постоянно
            self.snake_body.pop()
        return score, food_pos
    
    def draw_snake(self, play_surface, surface_color):
        play_surface.fill(surface_color)
        for pos in self.snake_body:
            pygame.draw.rect(play_surface, self.snake_color, 
            pygame.Rect(pos[0], pos[1], 10, 10))
        

    def check_for_boundaries(self, game_over, screen_width, screen_height):
        #Проверка, ударилась ли об границу или о саму себя
        if any((self.snake_head_pos[0] > screen_width-10 or self.snake_head_pos[0] < 0,
            self.snake_head_pos[1] > screen_height-10 or self.snake_head_pos[1] < 0)):
            game_over()
        
        for block in self.snake_body[1:]:
            #Проверка на то, что голова врезалась в любую часть змеи
            if (block[0] == self.snake_head_pos[0] and 
                block[1] == self.snake_head_pos[1]):
                game_over()


class Food():
    def __init__(self, food_color, screen_width, screen_height):
        #Инит еды
        self.food_color = food_color
        self.food_size_x = 10
        self.food_size_y = 10
        self.food_pos = [random.randrange(1, screen_width/10)*10,
                        random.randrange(1, screen_height/10)*10]
    
    def draw_food(self, play_surface):
        pygame.draw.rect(
            play_surface, self.food_color, pygame.Rect(
                self.food_pos[0], self.food_pos[1],
                self.food_size_x, self.food_size_y
            ))
