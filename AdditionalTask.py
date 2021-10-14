# -*- coding: utf-8 -*-
"""
Created on Thu Oct 14 01:59:27 2021

@author: Rearo
"""
from math import * # для округления вверх
import pandas # для импорта таьлицы excel

df = pandas.read_excel('Рабочий план ПИНЖ (1).xlsx')

lectures = [[], [], [], [], [], [], [], []] # список лекций по семестрам
seminars = [[], [], [], [], [], [], [], []] # список практик по семестрам
hours_l = [] #суммарное число часов лекций за каждый семестр
hours_s = [] #суммарное число часов практик за каждый семестр

semestr = df['Семестр'].values #кол-во семестров за год

for k in range (1, 9):
    hours_l.append(0)
    hours_s.append(0)
    for i in range(len(semestr)):
        if semestr[i] == k:
            lectures[k-1].append(df['Лекции'].values[i])
            hours_l[k-1] += df['Часы лекций'].values[i]
        if semestr[i] == k:
            seminars[k-1].append(df['Практики'].values[i])
            hours_s[k-1] += df['Часы практик'].values[i]

group = [22, 22, 22, 22] # кол-во на ПИНЖе групп и студентов в них, из них только 3 - платников

#кол-во часов по лекциям совпадают с имеющимися, так как лекции проводятся для всего потока
#посчитаем кол-во часов по практикам на все 4 группы в сумме
allHours_s = []
for i in range (0, 8):
    allHours_s.append(hours_s[i] * 4)
    
# посчитаем кол-во дней и недель в первом и втором семетрах
days_1 = 106 # рабочих дней в 1-ом семестре
weeks_1 = floor(days_1/5) # приблизительно рабочих недель

days_2 = 108 # рабочих дней во 2-ом семестре
weeks_2 = floor(days_2/5) # приблизительно рабочих недель

# найдем колв-во часов лекций в неделю, которые должны проводиться, чтобы закрыть семестр
lecturesInWeek = []

# посчитаем по нечетным и четным семестрам
for i in range (0, 8):
    if i % 2 == 0:
        lecturesInWeek.insert(i, ceil(hours_l[i] / weeks_1 / 1.5))
    else:
        lecturesInWeek.insert(i, ceil(hours_l[i] / weeks_2 / 1.5))
    
# найдем колв-во пар практик в неделю, которые должны проводиться, чтобы закрыть семестр
seminarsInWeek = []

# посчитаем по нечетным и четным семестрам
for i in range (0, 8):
    if i % 2 == 0:
        seminarsInWeek.insert(i, ceil(allHours_s[i] / weeks_1 / 1.5))
    else:
        seminarsInWeek.insert(i, ceil(allHours_s[i] / weeks_2 / 1.5)) 
        
# общее число занятий в неделю на ПИНЖ
classInWeek = []
for i in range (0, 8):
    classInWeek.append(seminarsInWeek[i] + lecturesInWeek[i])
    
"""
рассчитаем зарплату на преподователей по семестрам
"""
    
n = 5 # кол-во пар в неделю, которое может вести один преподователь  

# необходимое число преподавателей на ПИНЖ
teachers = []
for i in range (0, 8):
    teachers.append(ceil(classInWeek[i] / n ))

# зарплата на полставки
wage_t = 35000

wageTeachers = 0
for i in range (0, 8):
    wageTeachers += (teachers[i] * wage_t + teachers[i] * wage_t * 0.301 
                         + teachers[i] * wage_t * 0.13 + wage_t) 
#последние 35000 за месяц отпска, по одному в каждый семестр

"""
рассчитаем зарплату на остальных работников
"""
methodist = 20000 * 2 * 12 * 4
accountant = 30000 * 2 * 12 * 4
cleaningWoman = 20000 * 12 * 4
cloakroomWoman = 16000 * 12 * 4
securityGuard = 33000 * 12 * 4
systemAdministrator = 50000 * 12 * 4
system_1c = 96000

wageWorkers = system_1c + methodist + accountant + cleaningWoman + cloakroomWoman + securityGuard + systemAdministrator


# общие траты на зарплату и 1с
wage = wageWorkers + wageTeachers
"""
рассчитаем необходимую площадь и стоимость для аренды помещения на студентов по стандартам
"""
# лекционная аудитория 1,3 кв/м на учащегося
lectureClass = 0
for i in group:
    lectureClass += ceil(i * 1.3)
    
# кабинет информатики и вычислительной техники 6 кв/м на учащегося
programClass = ceil(6 * group[0] / 2)# так как работаем по подгруппам

# учебный класс 2,2 кв/м на учащегося
trainingClass = ceil(2.2 * group[0])

# аренда одного квадратного метра в месяц в среднем 600р, в год - 7200
costLectureClass = 7200 * lectureClass
costProgramClass = 7200 * 2 * programClass
costTrainingClass = 7200 * 3 * trainingClass
# туалет 16 кв/м
costToilet = 16 * 2 * 7200

# общая стоиость аренды за 4 года
rentCost = 4 * (costLectureClass + costProgramClass + costTrainingClass + costToilet)

"""
рассчитаем стоимость оборудования
"""
# лекционная аудитория
desk = 3000
chair = 1500
board = 15000
projector = 50000
costEquipmentLectureClass = desk * group[0] * 4 / 2 + board + projector + chair * group[0] * 4

# компьютерны класс
systemUnit = 14500
monitor = 8000
keyboard = 500
mouse = 300
computerDesk = 1500
costEquipmentProgramClass = (systemUnit + monitor + keyboard + mouse + computerDesk + chair + projector) * 22

# обычная аудитория
costEquipmentTrainingClass = (board + chair * group[0] + desk * group[0] / 2) * 3

# обща стоимость оборудования
costEquipment = costEquipmentLectureClass + costEquipmentProgramClass + costEquipmentProgramClass

"""
рассчитаем стоимость на воду
"""
waterRate = 21 # тариф на воду
waterToilet = 6 # литров за 1 спуск бочка
waterSink = 8 # литров за одно мытье рук

# Пусть каждый ученик и работник по два раза в день ходит в туалет и моет руки
totalWaterToilet = (waterToilet * (group[0]*4 + 8 + 8) * (days_1 + days_2) * 4 ) / 1000 # в куб/м
totalWaterSink = (waterSink * (group[0]*4 + 8 + 8) * (days_1 + days_2) * 4 ) / 1000 # в куб/м

# общая плата за 4 года пользования воды
totalWaterRate = (totalWaterToilet + totalWaterSink) * waterRate

"""
рассчитаем стоимость на электричество
"""
electricityRate = 4.24 # тариф на электричество в дневное время
bulb = 60 # вт/ч непрервыной работы лампочки
countBulb = 30 # лампочек на аудиторию
costBulb = 60 # руб за штуку
сomputer = 80 # вт/ч непрервыной работы компьютера


totalBulb = (bulb * 30 * 5 * (days_1 + days_2) * 1.5 * 4 * 4) / 1000 # квт/ч за 4 года
totalComputer = (сomputer * group[0] * 1.5 * (days_1 + days_2) * 4) / 1000 # квт/ч за 4 года
totalElectricityRate = electricityRate * (totalBulb + totalComputer) + costBulb * 30 * 5 * 2

"""
Интернет
"""
internetRate = 5500 # руб, бизнес тариф дом.ру
totalInternetRate = internetRate * 10 * 4
zoomRate = 1071 # руб, тариф на собрания до 100 человек
totalZoomRate = zoomRate * 10 * 4 * 9 # с учетом на каждого преподавателя

"""
Общая стоимость за очное обучение
"""
totalCostFullTimeEducation = wage + rentCost + costEquipment + totalWaterRate + totalElectricityRate + totalInternetRate

"""
Общая стоимость за дистанционное обучение
"""
# рассчитаем стоимоть ноутбуков для преподавателей
costNotebook = 60000 
totalCostNotebook = costNotebook * 9 # на каждого преподавателя

totalCostDistanceEducation = wage + rentCost + totalInternetRate + totalCostNotebook


"""
Проверка данных
"""

print (lectures)
print (hours_l)
print (seminars)
print (hours_s)
print (allHours_s)
print (lecturesInWeek)
print (seminarsInWeek)
print (classInWeek)
print (teachers)
print (wageTeachers)
print (wageWorkers)
print (wage)
print (lectureClass)
print (programClass)
print (trainingClass)
print (rentCost)
print (costEquipment)
print (totalWaterRate)
print (totalElectricityRate)

print (totalCostFullTimeEducation)

print (totalCostDistanceEducation)

"""
Стоимость оплаты одним человеком очной формы обучения
"""

fullTimeEducationPrice = totalCostFullTimeEducation / 4 / (group[0] * 3)
print ('Цена за очную форму обучения: ' , fullTimeEducationPrice)

"""
Стоимость оплаты одним человеком дистанционной формы обучения
"""

distanceEducationPrice = totalCostDistanceEducation / 4 / (group[0] * 3)
print ('Цена за дистанционную форму обучения: ' , distanceEducationPrice)

