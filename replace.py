from tqdm import tqdm

def replace_strings_in_file(path, ass, bss):
    # Read the content of the file
    try:
        with open(path, 'r', encoding='utf-8') as file:
            content = file.read()
    except FileNotFoundError:
        print(f"The file at {path} does not exist.")
        return
    except IOError as e:
        print(f"An error occurred while reading the file: {e}")
        return

    for a, b in zip(ass, bss):
        # Replace all occurrences of string 'a' with string 'b'
        # print(content.count(a))
        content = content.replace(a, b)

    # Write the updated content back to the file
    try:
        with open(path, 'w', encoding='utf-8') as file:
            file.write(content)
        print("File updated successfully.")
    except IOError as e:
        print(f"An error occurred while writing to the file: {e}")
    

from nodes import vertices

print(vertices.split('\n').__len__() / 3)
lines = vertices.split('\n')
vertices = [lines[3*i] for i in range(len(lines) // 3)]
print(vertices)

targets = [f"'id_{i}'" for i, vname in enumerate(vertices)]

replace_strings_in_file(r'catkin_ws/src/maze_solver/world/markersphere_test3.world', vertices, targets)

