expr = raw_input("Please enter string: " or "A Santa dog lived as a devil God at NASA")
reverse_expr = expr[::-1]
if ''.join(expr.split()).lower() == ''.join(reverse_expr.split()).lower():
    print "Entered string is palindrome"
else:
    print "Entered string is non-palindrome"
