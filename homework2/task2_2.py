"""This script defines if the string is palindrome or not"""
expression = raw_input("Please enter string: " or "A Santa dog lived as a devil God at NASA")
reverse_expression = expression[::-1]
if ''.join(expression.split()).lower() == ''.join(reverse_expression.split()).lower():
    print "Entered string is palindrome"
else:
    print "Entered string is non-palindrome"
