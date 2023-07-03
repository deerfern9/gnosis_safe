with open('all addresses.txt', 'r') as file:
    x = [i.strip() for i in file]
tmp = []
i = 0

while len(tmp) <= len(x) // 39:
    tmp2 = ''
    if i > len(x)-1:
        break
    while (len(tmp2) - 38) / 42 <= 39:
        if i > len(x)-1:
            break
        tmp2 += x[i] + ';'
        i += 1
    tmp.append(tmp2[:-1])

with open('result addresses.txt', 'w') as file:
    for i in tmp:
        file.write(i + '\n')