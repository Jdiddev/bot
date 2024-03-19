with open("number.txt") as file_in:
    lines = []
    for line in file_in:
        lines.append(line)
print(lines[0])