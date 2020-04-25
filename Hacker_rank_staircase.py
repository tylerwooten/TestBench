n = 5

list = [[' ' for x in range(n)] for y in range(n)]
for row in enumerate(list):
    holder = ''
    for item in enumerate(row[1]):
        if item[0] >= len(row[1])-1-row[0]:
            holder = holder + '#'
        else:
            holder = holder + ' '
    print(holder)
    #print(row[1])
