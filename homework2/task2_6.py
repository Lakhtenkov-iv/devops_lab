"""
Reverse the order of characters in each word within a sentence
while still preserving whitespace and initial word order of given string
"""
input_expr = raw_input("Please enter string: ").split()
output_expr = []
for word in input_expr:
    output_expr.append(word[::-1])
print ' '.join(output_expr)
