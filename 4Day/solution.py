from datetime import datetime as dt
import numpy as np

source = []
with open('input', 'r') as file:
    for line in file:
        datetime_str = line.split(']')[0].replace('[', '')
        datetime = dt.strptime(datetime_str, '%Y-%m-%d %H:%M')

        if 'Guard' in line:
            str = int(line.split('#')[1].split(' ')[0])
        else:
            str = line.split('] ')[1].replace('\n', '')
        source.append((datetime, str))

source = sorted(source, key=lambda x: x[0])

guards_data = {}
for entry in source:
    if type(entry[1]) is int:
        guard = entry[1]
        if guard not in guards_data.keys():
            guards_data[guard] = np.zeros((1, 60))
    elif entry[1] == 'falls asleep':
        asleep_minute = entry[0].time().minute
    elif entry[1] == 'wakes up':
        wakeup_minute = entry[0].time().minute
        new_row = np.zeros((1, 60))
        new_row[0, asleep_minute:wakeup_minute] = 1
        guards_data[guard] = np.vstack((guards_data[guard], new_row))

# part 1
max_sum = 0
for guard, array in guards_data.items():
    s = array.sum()
    if s > max_sum:
        best_guard = guard
        max_sum = s

best_minute = np.argmax(np.sum(guards_data[best_guard], axis=0))

print('best guard: {}'.format(best_guard))
print('best minute: {}'.format(int(best_minute)))
print('total sleep time: {}'.format(int(max_sum)))
print('Answer: {}'.format(int(best_guard * best_minute)))

# part 2
freq_data = []
for guard, array in data_by_guards.items():
    frequencies = np.sum(data_by_guards[guard], axis=0)
    freq_data.append([guard, np.argmax(frequencies), frequencies.max()])
freq_data = np.array(freq_data)

best_id = np.argmax(freq_data[:, 2])
best_guard_2, best_minute_2, time_asleep = freq_data[best_id, :]
print('\nbest guard 2: {}'.format(int(best_guard_2)))
print('best minute 2: {}'.format(int(best_minute_2)))
print('time asleep on best minute: {}'.format(int(time_asleep)))
print('Answer 2: {}'.format(int(best_guard_2 * best_minute_2)))
