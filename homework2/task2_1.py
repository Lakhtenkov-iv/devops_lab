while True:
    try:
        N = int(raw_input("Please enter integer value from 1 to 20: "))
        if 1 <= N <= 20:
            for i in range(N):
                print (i ** 2)
            break
        else:
            print "Value out of range. Try again..."
            continue
    except ValueError:
        print "Oops!  That was no valid number.  Try again..."

