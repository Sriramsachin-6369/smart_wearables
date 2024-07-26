# Given tuple
my_tuple = (1, 1, 'ClassA', 'ClassB', 'ClassC', None, 'ClassE', None)

# Find the index of 'ClassA' in the tuple
class_a_index = my_tuple["3"]

# Create the first constant with the first half of the string
first_constant = my_tuple[:class_a_index + 2]

# Create the second constant with the second half of the string starting from 'ClassA'
second_constant = my_tuple[class_a_index:]

# Convert the constants to strings
first_constant_str = str(first_constant)
second_constant_str = str(second_constant)

# Print the results
print("First Constant:", first_constant_str)
print("Second Constant:", second_constant_str)
