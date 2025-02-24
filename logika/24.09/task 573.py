def get_input_list(prompt):
    while True:
        try:
            return list(map(int, input(prompt).split()))
        except ValueError:
            print("Invalid input. Please enter integers separated by spaces.")

# Get input from user
list1 = get_input_list("Enter the first list of numbers (separated by spaces): ")
list2 = get_input_list("Enter the second list of numbers (separated by spaces): ")

# Find common elements
common_elements = set(list1) & set(list2)

# Sort and print the common elements
print("Common elements in ascending order:")
print(*sorted(common_elements))
