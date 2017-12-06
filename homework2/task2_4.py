"""This script returns Decimal, Octal, Hexadecimal, Binary form of numbers from 1 to given n"""
while True:
    try:
        N = int(raw_input("Please enter integer value from 1 to 99: "))
        if 1 <= N <= 99:
            max_width = len(format(N, 'b'))


            def print_formatted(number, width):
                """Function returns formatted string of dec, oct, hex, bin form of number"""
                return '{dec:>{width}} {oct:>{width}} {hex:>{width}} {bin:>{width}}'.format(dec=number, \
                                                                                       oct=format(number, 'o'), \
                                                                                       hex=format(number, 'x').capitalize(), \
                                                                                       bin=format(number, 'b'), \
                                                                                       width=width)


            for i in range(1, N+1):
                print print_formatted(i, max_width)
            break
        else:
            raise ValueError
    except ValueError:
        print "Wrong value"
