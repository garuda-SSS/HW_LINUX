import subprocess
from datetime import datetime


output = subprocess.check_output(['ps', 'aux']).decode('utf-8')
lines = output.split('\n')
users = {}
total_memory = 0
total_cpu = 0
max_memory_process = ('', 0)
max_cpu_process = ('', 0)
for line in lines[1:]:
    if line:
        parts = line.split()
        username = parts[0]
        memory = float(parts[3])
        cpu = float(parts[2])
        if username in users:
            users[username] += 1
        else:
            users[username] = 1
        total_memory += memory
        total_cpu += cpu
        if memory > max_memory_process[1]:
            max_memory_process = (parts[10][:20], memory)
        if cpu > max_cpu_process[1]:
            max_cpu_process = (parts[10][:20], cpu)
print("Отчёт о состоянии системы:")
print("Пользователи системы:", list(users.keys()))
print("Процессов запущено:", len(lines) - 2)  # Вычитаем заголовок и пустую строку в конце

print("\nПользовательских процессов:")
for user, count in users.items():
    print(f"{user}: {count}")

print("\nВсего памяти используется:", "{:.1f}%".format(total_memory))
print("Всего CPU используется:", "{:.1f}%".format(total_cpu))
print("Больше всего памяти использует:", f"({max_memory_process[0]}, {max_memory_process[1]}%)")
print("Больше всего CPU использует:", f"({max_cpu_process[0]}, {max_cpu_process[1]}%)")


now = datetime.now().strftime("%d-%m-%Y-%H:%M")
filename = f"{now}-scan.txt"
with open(filename, 'w') as f:
    f.write("Отчёт о состоянии системы:\n")
    f.write("Пользователи системы: {}\n".format(list(users.keys())))
    f.write("Процессов запущено: {}\n".format(len(lines) - 2))
    f.write("\nПользовательских процессов:\n")
    for user, count in users.items():
        f.write("{}: {}\n".format(user, count))
    f.write("\nВсего памяти используется: {:.1f}%\n".format(total_memory))
    f.write("Всего CPU используется: {:.1f}%\n".format(total_cpu))
    f.write("Больше всего памяти использует: ({}, {:.1f}%)\n".format(max_memory_process[0], max_memory_process[1]))
    f.write("Больше всего CPU использует: ({}, {:.1f}%)\n".format(max_cpu_process[0], max_cpu_process[1]))

