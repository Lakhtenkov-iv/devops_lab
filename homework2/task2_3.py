input_file = open('input2_3.txt', 'r')
input = [[int(i) for i in line.split()] for line in input_file]
width = input[0][0]
high = input[0][1]
ractangle_count = input[1][0]
canvas = [[0 for x in range(width)] for y in range(high)]


def draw_ractangle(coordinats, matrix):
    x1 = coordinats[0]
    y1 = coordinats[1]
    x2 = coordinats[2]
    y2 = coordinats[3]
    for i in range(x1,x2):
        for j in range(y1,y2):
            matrix[i][j] = 1
    return matrix


for i in range(ractangle_count):
    canvas = draw_ractangle(input[i+2], canvas)

free_canvas = 0
for i in range(len(canvas)): free_canvas += canvas[i].count(0)

print free_canvas