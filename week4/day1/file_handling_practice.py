"""
Day 1 Practice: File Handling (Q6-9)
Reading line-by-line, writing output, and using .strip() to detect
blank/empty lines - all patterns reused directly in the Day 4 log parser.
"""


def count_lines(filepath):
    count = 0
    with open(filepath, "r") as file:
        for i in file:
            count += 1
    return count


def print_error_lines(filepath):
    with open(filepath, "r") as file:
        for line in file:
            if "error" in line.lower():
                print(line, end="")


def sum_numbers_to_file(input_path, output_path):
    total = 0
    with open(input_path, "r") as file:
        for i in file:
            if i.strip():  # skip blank lines
                total = total + int(i)

    with open(output_path, "w") as file:
        file.write(str(total))

    return total


def count_blank_lines(filepath):
    blank = 0
    with open(filepath, "r") as file:
        for i in file:
            if i.strip() == "":
                blank += 1
    return blank


if __name__ == "__main__":
    print(count_lines("conf-f"))                                  # 51
    print_error_lines("simple_log.txt")                           # prints 6 matching lines
    print(sum_numbers_to_file("numbers.txt", "numbers2.txt"))      # 87
    print(count_blank_lines("blanks_test.txt"))                    # 3
