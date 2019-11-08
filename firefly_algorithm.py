import math
import sys
import random


class Firefly:                                                 # Класс, описывающий светлячка
   def __init__(self, n):
       self.position = [0 for i in range(n)]        # Текущая позиция светлячка в пространстве
       self.error = 0.0                                                       # Текущая ошибка
       self.intensity = 0.0                                   # Текущая интенсивность свечения

   def random_position(self):                # Случайное расположение светлячка в пространстве
       for i in range(len(self.position)):
           self.position[i] = (max_x - min_x) * random.random() + min_x

   def move(self, s_i):                 # Подвинуть рассматриваемого светлячка к светлячку s_i
       r = distance(s_i.position, self.position)                # Расстояние между светлячками
       b_ij = B0 * math.exp(-g * r * r) # Привлекательность светлячка s_i для рассматриваемого

       for k in range(dim):
           Xi = s_i.position[k]
           Xj = self.position[k]

           self.position[k] = Xi + b_ij * (Xj - Xi) + a * random.uniform(-1.0, 1.0)
   # Если светлячок оказался за границей рассматриваемой области..
           if self.position[k] < min_x or self.position[k] > max_x: self.random_position() 

       self.error = error(self.position)                                # Расчет новой ошибки
       self.intensity = 1 / (self.error + 1)            # Расчет новой интенсивности свечения


def fitness_func(x):                                      # Фитнесс-функция Михалевича для n=5
   result = 0.0
   for i in range(len(x)):
       result += math.sin(x[i])* ( math.sin( ( (i+1) * x[i]* x[i]) / math.pi ) )**20
   return -1.0 * result


def error(x):
   extreme = -4.687658                              # Правильное значение глобального минимума
   value_fitness_f = fitness_func(x)               # Найденное значение функции для светлячка,   расположенного по координатам х
   return (extreme - value_fitness_f)**2             		     # Квадратичная ошибка


def distance(s_i, s_j):                    # Нахождение расстояния между светлячками s_i и s_j
   r = 0.0
   for i in range(len(s_i)): r += (s_i[i] - s_j[i])**2
   return math.sqrt(r)


def show_progress(epoch, best):
   if epoch % 200 == 0:
       print("Эпоха №", epoch, "\tЛучшее значение фитнесс-функции = ", round(best, 5))


def update_best(new_best):
   best_position = [0 for i in range(dim)]
   best_error = new_best.error
   for k in range(dim):
       best_position[k] = new_best.position[k]
   return best_position, best_error


def init_swarm():                                   # Инициализация популяции (роя) светлячков
   best_error = sys.float_info.max
   best_position = [None for i in range(dim)]

   swarm = []
   for i in range(n_fireflies):
       swarm.append(Firefly(dim))                          # Добавление нового светлячка в рой
       for j in range(dim): swarm[i].random_position()     # Генерация случайного расположения 
       swarm[i].error = error(swarm[i].position)                              # Рассчет ошибки
       swarm[i].intensity = 1 / (swarm[i].error + 1)          # Расчет интенсивности свечения

       if swarm[i].error < best_error:
           best_position, best_error = update_best(swarm[i])

   return swarm, best_error, best_position


def solve():

   swarm, best_error, best_position = init_swarm()              # Инициализация роя светлячков

   epoch = 0
   while epoch < max_epochs:
#  Показать лучшее найденное решение в данную эпоху
       show_progress(epoch, fitness_func(swarm[0].position))               

       for i in range(n_fireflies):
           for j in range(n_fireflies):
               if swarm[j].intensity < swarm[i].intensity:       # Если интенсивость свечения светлячка j меньше, чем у i
                   swarm[j].move(swarm[i])            # Передвигаем светлячка j к светлячку i

       best_firefly = 0				  # Индекс светлячка с лучшей светимостью
for i in range(1, len(swarm)):		
   		if swarm[i].error < best_error:
       			best_firefly = i
       			best_position, best_error = update_best(swarm[i])

swarm[best_firefly].random_position()		 # Лучший светлячок двигается в случайном направлении
swarm[best_firefly].error = error(swarm[0].position)
swarm[best_firefly].intensity = 1/(swarm[0].error + 1)

swarm = sorted(swarm, key= lambda x: x.error)      # Сортировка роя по значению ошибки
if swarm[0].error < best_error:
# Обновить,если нужно, значение лучшей (минимальной) ошибки
   		best_position, best_error = update_best(swarm[0]) 
       epoch += 1

   return best_position

                                                               # Параметры функции Михалевича
min_x = 0.0                                                                   # 0 <= xi <= Pi
max_x = 3.2
dim = 5                                                                  # размерность задачи

                                                              # Свободные параметры алгоритма
B0 = 1.0                       # взаимная привлекательность светлячков при нулевом расстоянии
g = 1.0                                                  # коэффициент поглощения света среды
a = 0.20                                                    # свободный параметр рандомизации

n_fireflies = 40                                                # размер популяции светлячков
max_epochs = 1000                                                   # максимальное число эпох


print("Демонстрация работы алгоритма светлячков", end='')
print(" на примере нахождения глобального минимума для Функции Михалевича с ", dim, "! локальными экстремумами\n\n", end='')

best_position = solve()

print("\nИзвестный глобальный минимум:\nx0 = 2.2029 1.5707 1.2850 1.9231 1.7205")
print("Значение в точке х0 = -4.687658")
print("\nЛучшее найденное решение:\nx = ", end='')
for i in range(len(best_position)): print(round(best_position[i], 5),' ', end='')
print("\nЗначение в точке х = ", round(fitness_func(best_position), 5))
print("Ошибка = ", round(error(best_position), 5))


