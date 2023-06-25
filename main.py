import pygame  # для создания игр под различные устройства
import sys  # для использования функции exit(), чтобы выйти из игры
import random  # для рандомного положения яблока на игровом поле
import pygame_menu  # для создания меню игры
import os

pygame.init()  # для успешной инициализации всех импортированных модулей pygame
#pygame.font.init()

COLOR_FRAME = (8, 217, 214)  # цвет заднего фона
COLOR_FIELD = (234, 234, 234)  # цвет1 игрового поля
COLOR_FIELD_1 = (230, 230, 230)  # цвет2 игрового пол
COLOR_APPLE = (255, 46, 99)  # цвет яблока
COLOR_TOP = (11, 152, 150)  # цвет верхего табло, где будут очки за игру
COLOR_snake = (56, 64, 82)  # цвет змейки
COLOR_HEAD = (14, 16, 20) # цвет головы змейки
SIZE_OF_BLOCK = 20  # размер блоков
COUNT_OF_BLOCKS = 19  # количество блоков
INDENT_TOP = 80  # ширина вернего табло
INDENT = 1  # расстояния между блоками на игровом экране

# размер экрана
size_screen = [SIZE_OF_BLOCK * COUNT_OF_BLOCKS + 2 * SIZE_OF_BLOCK + INDENT * COUNT_OF_BLOCKS,
               INDENT_TOP + SIZE_OF_BLOCK * COUNT_OF_BLOCKS + 2 * SIZE_OF_BLOCK + INDENT * COUNT_OF_BLOCKS]

screen = pygame.display.set_mode(size_screen)
pygame.display.set_caption('Snake')


timer = pygame.time.Clock()  # для времени и скорости
font = pygame.font.SysFont('Comic Sans MS', 35)
filename = 'total.txt'
maxi = 0

os.chdir(os.path.dirname(os.path.abspath('pict.jpg')))
picture = pygame.image.load('pict.jpg')


class Blocks:  # класс для координат и движения змейки
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def inside(self):  # для проверки, что змейка не за пределом поля
        return 0 <= self.x < COUNT_OF_BLOCKS and 0 <= self.y < COUNT_OF_BLOCKS

    def __eq__(self, other):  # для проверки,наткнулась ли змейка на яблоко
        return isinstance(other, Blocks) and self.x == other.x and self.y == other.y


def draw_elements(color, row, col):  # для отображения элементов
    pygame.draw.rect(screen, color, [SIZE_OF_BLOCK + col * SIZE_OF_BLOCK + INDENT* (col + 1),
                                     INDENT_TOP + SIZE_OF_BLOCK + row * SIZE_OF_BLOCK + INDENT * (row + 1),
                                     SIZE_OF_BLOCK,
                                     SIZE_OF_BLOCK])


def Game_Over_crash():  # для отображения окна Game Over
    game_over = True
    while game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game_over = False

        screen.blit(picture, (0, 0))
        my_font = pygame.font.SysFont('Comic Sans MS', 40)
        my_font1 = pygame.font.SysFont('Comic Sans MS', 25)
        text_1 = my_font.render('Game Over', False, COLOR_FIELD)
        text_2 = my_font.render('Snake crash ', False, COLOR_FIELD)
        text_3 = my_font1.render('To go to the menu, press "Enter"', False, COLOR_FIELD)
        screen.blit(text_1, (120, 180))
        screen.blit(text_2, (110, 230))
        screen.blit(text_3, (30, 450))
        timer.tick(10)
        pygame.display.update()


def Game_Over_crash_yourself():  # для отображения окна Game Over
    game_over = True
    while game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game_over = False

        screen.blit(picture, (0, 0))
        my_font = pygame.font.SysFont('Comic Sans MS', 40)
        my_font1 = pygame.font.SysFont('Comic Sans MS', 25)
        text_1 = my_font.render('Game Over', False, COLOR_FIELD)
        text_2 = my_font.render('Snake crash yourself', False, COLOR_FIELD)
        text_3 = my_font1.render('To go to the menu, press "Enter"', False, COLOR_FIELD)
        screen.blit(text_1, (120, 200))
        screen.blit(text_2, (25, 250))
        screen.blit(text_3, (30, 450))
        timer.tick(10)
        pygame.display.update()


def set_maxi(value):  # переприсваивание/обновление
    global maxi
    maxi = value


def count(file):  # для чтения максимального результата из файла
    global maxi
    fl = open(file, 'r')
    k = fl.readline()
    b = int(k)
    if not b:
        b = 0
    if b >= maxi:
        maxi = b
    fl.close()


def draw_update_function(label, menu):  # обновление строчки с максимальным результатом
    label.set_title(str(maxi))


def The_game():  # функция игры
    global maxi
    maxim = maxi

    Snake = [Blocks(9, 8), Blocks(9, 9), Blocks(9, 10)]  # сама змейка
    drow = dop_row = 0  # dop_row и dop_col для устранения бага
    dcol = dop_col = 1
    total = 0  # количество очков
    speed = 1  # скорость

    def random_apple():  # рандомное положение яблока
        x = random.randint(0, COUNT_OF_BLOCKS - 1)
        y = random.randint(0, COUNT_OF_BLOCKS - 1)
        empty_block = Blocks(x, y)  #
        while empty_block in Snake:  # чтобы яблоко не попадало на змейку
            empty_block.x = random.randint(0, COUNT_OF_BLOCKS - 1)
            empty_block.y = random.randint(0, COUNT_OF_BLOCKS - 1)

        return empty_block

    apple = random_apple()  # яблоко

    # цикл игры
    while True:
        for event in pygame.event.get():  # для работы кнопки выхода (красная с крестиком)
            if event.type == pygame.QUIT:
                print('exit')
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:  # для изменения траектории движения змейки при нажатии определенной клавиши
                if event.key == pygame.K_UP and dcol != 0:
                    dop_row = -1
                    dop_col = 0
                elif event.key == pygame.K_DOWN and dcol != 0:
                    dop_row = 1
                    dop_col = 0
                elif event.key == pygame.K_LEFT and drow != 0:
                    dop_row = 0
                    dop_col = -1
                elif event.key == pygame.K_RIGHT and drow != 0:
                    dop_row = 0
                    dop_col = 1

        screen.fill(COLOR_FRAME)  # заполнение заднего фона цветом
        pygame.draw.rect(screen, COLOR_TOP, [0, 0, size_screen[0], INDENT_TOP])  # поле для заголовка

        # для отображение очков и скорости
        text_total = font.render(f"Total: {total}", False, COLOR_FIELD)
        text_speed = font.render(f"Speed: {speed}", False, COLOR_FIELD)
        screen.blit(text_total, (SIZE_OF_BLOCK, SIZE_OF_BLOCK))
        screen.blit(text_speed, (SIZE_OF_BLOCK + 220, SIZE_OF_BLOCK))

        for row in range(COUNT_OF_BLOCKS):  # поле квадратиков
            for col in range(COUNT_OF_BLOCKS):
                if (row + col) % 2 == 0:
                    color = COLOR_FIELD_1
                else:
                    color = COLOR_FIELD
                draw_elements(color, row, col)

        head = Snake[-1]
        if not head.inside():  # если стукнулась
            if total >= maxim:
                set_maxi(total)
                f = open(filename, 'w')
                f.write(str(total))
                f.close()
            print('Game over, crash')
            Game_Over_crash()
            break

        draw_elements(COLOR_APPLE, apple.x, apple.y)  # отображение яблока

        for block in Snake:
            draw_elements(COLOR_snake, block.x, block.y)  # отображение змейки

        draw_elements(COLOR_HEAD, head.x, head.y) # отображение головы

        if apple == head:  # если змейка наткнется на яблоко
            total += 1
            speed = total // 5 + 1
            Snake.append(apple)  # увеличение длины при поглощении яблока
            apple = random_apple()

        drow = dop_row
        dcol = dop_col

        # для перемещения змейки по следу
        new_head = Blocks(head.x + drow, head.y + dcol)

        if new_head in Snake:  # при ударении о саму себя
            if total >= maxim:
                set_maxi(total)
                f = open(filename, 'w')
                f.write(str(total))
                f.close()
            print('Game over, crash youself')
            Game_Over_crash_yourself()
            break

        pygame.display.flip()

        Snake.append(new_head)
        Snake.pop(0)

        timer.tick(2 + speed)  # регулировка скорости


count(filename)

main_theme = pygame_menu.themes.THEME_DARK.copy()
main_theme.set_background_color_opacity(0.6)

menu = pygame_menu.Menu('Snake', 350, 320, theme=main_theme)
menu.add.text_input('Name: ', default='Player 1')
menu.add.label('Max result:')
label = menu.add.label(maxi)
label.add_draw_callback(draw_update_function)
menu.add.button('Play', The_game)
menu.add.button('Exit', pygame_menu.events.EXIT)

while True:
    screen.blit(picture, (0, 0))

    events = pygame.event.get()
    for ev in events:
        if ev.type == pygame.QUIT:
            exit()

    if menu.is_enabled():
        #label.set_title(maxi) # обновление значения maxi
        menu.update(events)
        menu.draw(screen)
    pygame.display.flip()
