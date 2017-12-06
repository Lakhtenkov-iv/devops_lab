"""Read an integer from 1 to 20. For all non-negative integers , print square fo integer."""
while True:
    try:
        N = int(raw_input("Please enter integer value from 1 to 20: "))
        if 1 <= N <= 20:
            for i in range(N):
                print i ** 2
            break
        else:
            raise ValueError
    except ValueError:
        print "Oops!  That was no valid number.  Try again..."
