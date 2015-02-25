# coding=utf-8

import time, random
import pylsl
from pylsl import stream_inlet, stream_outlet, stream_info

info = stream_info('RandomData', 'EEG', 5, 50, pylsl.cf_int32, 'RandomDev123')
"""Создаём файл c описанием потока.

'RandomData' - название, текстовая строка
'EEG' - название типа передаваемых данных
5 - число каналов в одном сэмпле (размерность каждого передаваемого вектора)
50 - частота проверки наличия новых сэмпло
cf_int32 - тип данных, содержащихся в сэмпле. Доступны: cf_float32, cf_double64, cf_string, cf_int8, cf_int16,
    cf_int32, cf_int64
'RandomDev123' - идентификатор устройства, передающего данные. Необходим для переподключения к потоку, в случае
    потери связи
"""

outlet = stream_outlet(info) # создаём аутлет для передачи данных в описанный поток
inlet = stream_inlet(info) # создаём инлет для получения данных из описанного потока
inlet.open_stream() # начинаем отслеживать новые данные в потоке

user_str = raw_input('Enter string: ') # просим пользователя ввести текстовую строку

int_list = []

for i in range(0, 5 - len(user_str) % 5): # т.к. мы передаём вектора из 5 элементов, добавляем для простоты нулевые символы
    user_str += '\0'

for j in range(0,len(user_str) / 5):
    temp_list = []
    for i in range(0,5):
        temp_list.append(ord(user_str[j*5 + i])) # записываем числовые представления символов в вектор из 5 элементов
    int_list.append(temp_list) # добавляем созданные список в список будущих сэмплов

for i in range(0, len(int_list)):
    outsample = pylsl.vectori(int_list[i]) # создаём сэмпл на основе вектора
    outlet.push_sample(outsample) # загружаем сэмпл в поток
    time.sleep(0.01) # даём программе немного времени на обработку сэмпла

insample = pylsl.vectorf()
inlet_list = []
while inlet.samples_available(): # пока в потоке есть необработанные сэмплы
    inlet.pull_sample(insample) # извлекаем сэмпл
    inlet_list.append(list(insample)) # добавляем сэмпл в список всех полученных векторов

outstring = ''

for i in range(0, 5*len(inlet_list)):
    outstring += chr(int(inlet_list[i / 5][i % 5])) # восстанавливаем строку на основе полученных векторов

print outstring