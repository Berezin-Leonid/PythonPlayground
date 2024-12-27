# импортируем pygame
import pygame

# задаём константы для неизменяющихся значений
SCREEN_WIDTH = 470
SCREEN_HEIGHT = 770
FLOOR_COUNT = 11
FREIGHT_ELEVATOR_WIDTH = 75
ELEVATOR_WIDTH = 50
ELEVATOR_HEIGHT = 70
BUTTON_SIZE = 20
FLOOR_HEIGHT = 70
# константа чёрного цвета
BLACK = (0, 0, 0)

# инициализируем модули pygame
pygame.init()

# создаём объект для главного экрана
# с указанием ширины и высоты
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# указываем название для главного окна
pygame.display.set_caption("Два лифта")

# загружаем изображения
# картинка для лифта
elevator_img = pygame.image.load("elevator.jpg")
# картинка для красной кнопки
button_red_img = pygame.image.load("button1_elevator1.png").convert_alpha()
# картинка для синей кнопки
button_blue_img = pygame.image.load("button1_elevator2.png").convert_alpha()
# картинка для грузового лифта
freight_elevator_img = pygame.image.load("freight_elevator.jpg")
# картинка для фона
back_img = pygame.image.load("back.jpg")

# масштабируем изображения под заданные в константах размеры
elevator_img = pygame.transform.scale(elevator_img, (ELEVATOR_WIDTH, ELEVATOR_HEIGHT))
button_red_img = pygame.transform.scale(button_red_img, (BUTTON_SIZE, BUTTON_SIZE))
button_blue_img = pygame.transform.scale(button_blue_img, (BUTTON_SIZE, BUTTON_SIZE))
freight_elevator_img = pygame.transform.scale(freight_elevator_img, (FREIGHT_ELEVATOR_WIDTH, ELEVATOR_HEIGHT))
back_img = pygame.transform.scale(back_img, (SCREEN_WIDTH, SCREEN_HEIGHT))


# класс Кнопок вызова
class Button:
   # конструктор __init__ создаёт кнопку
   def __init__(self, x, y, image, action):
       # рисуем прямоугольник с заданными координатами
       self.rect = pygame.Rect(x, y, BUTTON_SIZE, BUTTON_SIZE)
       # в прямоугольник вписываем изображение
       self.image = image
       # привязываем кнопку к функции, которую укажем при создании кнопки
       self.action = action

   # метод для отрисовки кнопки на главном экране с заданными координатами
   def draw(self, screen):
       # метод blit рисует новый объект на изображении screen
       screen.blit(self.image, (self.rect.x, self.rect.y))

   # метод проверки нажатия кнопки
   def check_click(self, pos):
       # collidepoint проверяет действие курсора
       if self.rect.collidepoint(pos):
           # если пользователь кликнул на кнопку,
           # включаем указанную при создании функцию
           self.action()


# класс Этажей
# создаёт этаж с кнопками для вызова двух лифтов
# их координаты зависят от номера этажа (y)
class Floor:
   # конструктор __init__ создаёт этаж
   def __init__(self, y, elevator1, elevator2):
       # передаём номер этажа
       self.y = y
       # передаём на каждый этаж по два объекта кнопок,
       # размещаем на нужных местах соответственно этажу
       # и привязываем к нужному лифту через лямбда-функцию
       self.buttons = [
           Button(110, y + FLOOR_HEIGHT // 2 - BUTTON_SIZE // 2, button_red_img, lambda: elevator1.set_target(y)),
           Button(335, y + FLOOR_HEIGHT // 2 - BUTTON_SIZE // 2, button_blue_img, lambda: elevator2.set_target(y)),
       ]

   # метод отрисовки этажа и кнопки
   def draw(self, screen):
       # рисуем линию на главном экране с толщиной 1
       # от нулевой координаты до конца
       # экрана по оси х и на высоте этаже y
       pygame.draw.line(screen, BLACK, (0, self.y), (SCREEN_WIDTH, self.y), 1)
       # рисуем кнопки на каждом этаже
       for button in self.buttons:
           button.draw(screen)


# класс Лифта
# определяем лифт с координатами, размерами и изображением
class Elevator:
   def __init__(self, x, y, width, height, image):
       # начальные координаты
       self.x = x
       self.y = y
       # размеры лифта
       self.width = width
       self.height = height
       # изображение
       self.image = image
       # target_y задаёт этаж, куда должен ехать лифт
       self.target_y = y
       # скорость лифта
       self.speed = 2

   # метод для движения лифтов
   def move(self):
       # если лифт находится ниже этажа нажатой кнопки...
       if self.y < self.target_y:
           # координата лифта увеличивается с установленной скоростью
           self.y += self.speed
       # если лифт находится выше этажа нажатой кнопки...
       elif self.y > self.target_y:
           # координата лифта уменьшается с установленной скоростью
           self.y -= self.speed

   # метод для отрисовки лифтов на главном экране
   def draw(self, screen):
       screen.blit(self.image, (self.x, self.y))


# класс для создания всей Системы Лифтов
class ElevatorSystem:
   def __init__(self):
       # cоздаём два лифта: грузовой и пассажирский
       self.elevator1 = Elevator(150, SCREEN_HEIGHT - FLOOR_HEIGHT,
                                 FREIGHT_ELEVATOR_WIDTH, ELEVATOR_HEIGHT, freight_elevator_img)
       self.elevator2 = Elevator(255, SCREEN_HEIGHT - FLOOR_HEIGHT,
                                 ELEVATOR_WIDTH, ELEVATOR_HEIGHT, elevator_img)
       # создаём массив этажей
       self.floors = [
           Floor(SCREEN_HEIGHT - FLOOR_HEIGHT * (i + 1), self.elevator1, self.elevator2)
           for i in range(FLOOR_COUNT)
       ]

   # метод обновления положения лифтов, созданный в классе Elevator
   def update(self):
       self.elevator1.move()
       self.elevator2.move()

   # метод отрисовки объектов
   def draw(self, screen):
       # рисуем этажи через метод draw класса Floor
       for floor in self.floors:
           floor.draw(screen)
       # рисуем лифты через метод draw класса Elevator
       self.elevator1.draw(screen)
       self.elevator2.draw(screen)


# функция для установки целевого этажа для лифта
def elevator_set_target(self, y):
   self.target_y = y


# устанавливаем целевой этаж в объект Лифта
Elevator.set_target = elevator_set_target


# основная функция
def main():
   # объект частоты обновления экрана
   clock = pygame.time.Clock()
   # флаг-метка для работы главного цикла
   running = True
   # создаём объект класса Системы Лифтов
   system = ElevatorSystem()

   # пока флаг-метка равен True, работает цикл всей системы
   while running:
       # отрисовываем фон
       screen.blit(back_img, (0, 0))

       # проверяем список событий при запущенной программе
       for event in pygame.event.get():
           # если пользователь закрыл главное окно...
           if event.type == pygame.QUIT:
               # завершаем цикл
               running = False
           # если пользователь кликнул мышкой...
           elif event.type == pygame.MOUSEBUTTONDOWN:
               # сохраняем координаты клика в переменную pos
               pos = pygame.mouse.get_pos()
               # проверяем все этажи и кнопки для проверки,
               # совпадают ли координаты клика с одной из кнопок
               for floor in system.floors:
                   for button in floor.buttons:
                       button.check_click(pos)

       # обновляет состояние лифтов
       system.update()
       # отрисовывает лифты на нужных позициях
       system.draw(screen)
       # обновляем изображение для пользователя, создавая анимацию
       pygame.display.flip()
       # устанавливаем скорость обновления кадров до 30 в секунду
       clock.tick(30)

   # завершаем работу после окончания цикла
   pygame.quit()


# запускаем главную функцию
main()