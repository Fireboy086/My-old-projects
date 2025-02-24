import os

def create_task_files(start, end):
    for i in range(start, end + 1):
        filename = f"task{i}.py"
        with open(filename, 'w') as file:
            file.write(f"# This is task {i}\n\n")
        print(f"Created {filename}")

if __name__ == '__main__':
    create_task_files(473, 483)
