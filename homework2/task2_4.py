N = int(raw_input("Please enter integer value from 1 to 99: "))
if 1 <= N <= 99:
    max_width = len(format(N, 'b'))


    def print_formatted(number, width):
        print '{dec:>{width}} {oct:>{width}} {hex:>{width}} {bin:>{width}}'.format(dec=number, \
                                                                               oct=format(number, 'o'), \
                                                                               hex=format(number, 'x').capitalize(), \
                                                                               bin=format(number, 'b'), \
                                                                               width=width)


    for i in range(1, N+1):
        print_formatted(i, max_width)
else: print "Wrong input"



