"""Script for happiness calculation"""
input_file = open('input2_5.txt', 'r')
input = [[int(i) for i in line.split()] for line in input_file]
print input
n = int(input[0][0])
m = int(input[0][1])
array = input[1]
A_set = tuple(input[2])
B_set = tuple(input[3])
print n, m, array, A_set, B_set
happiness = 0
for i in array:
    if i in A_set:
        happiness += 1
    if i in B_set:
        happiness -= 1
print "Happiness is %s" % happiness
