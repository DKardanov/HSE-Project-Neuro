import time, random
import pylsl
from pylsl import stream_inlet, stream_outlet, stream_info

info = stream_info('RandomData', 'EEG', 5, 50, pylsl.cf_int32, 'RandomDev123')
outlet = stream_outlet(info)
inlet = stream_inlet(info)
inlet.open_stream()

user_str = raw_input('Enter string: ')

int_list = []

for i in range(0, 5 - len(user_str) % 5):
    user_str += '\0'

print len(user_str)

for j in range(0,len(user_str) / 5):
    temp_list = []
    for i in range(0,5):
        temp_list.append(ord(user_str[j*5 + i]))
    int_list.append(temp_list)

print int_list

for i in range(0, len(int_list)):
    outsample = pylsl.vectori(int_list[i])
    outlet.push_sample(outsample)
    time.sleep(0.01)

# print('outsample: %s' % list(outsample))

insample = pylsl.vectorf()
inlet_list = []
while inlet.samples_available():
    inlet.pull_sample(insample)
    inlet_list.append(list(insample))

outstring = ''

for i in range(0, 5*len(inlet_list)):
    outstring += chr(int(inlet_list[i / 5][i % 5]))

print outstring

# print('insample: %s' % list(insample))


