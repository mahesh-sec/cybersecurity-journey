"""
Day 1 Practice: Functions (Q1-5)
Core focus: using return instead of print, and avoiding shadowing
Python built-ins (max, sum, dict).
"""


def is_even(n):
    return n % 2 == 0


def celsius_to_fahrenheit(c):
    far = (c * 9 / 5) + 32
    return far


def max_of_three(a, b, c):
    if a > b:
        if a > c:
            return a
        else:
            return c
    elif b > c:
        return b
    else:
        return c


def count_vowels(word):
    count = 0
    for i in word:
        if i in "aeiou":
            count += 1
    return count


def password_check(password):
    if len(password) >= 8 and any(char.isdigit() for char in password):
        return True
    else:
        return False


if __name__ == "__main__":
    print(is_even(95769))                          # False
    print(celsius_to_fahrenheit(36))                # 96.8
    print(max_of_three(5685, 4583, 5689))           # 5689
    print(max_of_three(1, 5, 5))                    # 5
    print(count_vowels("pirate king luffy"))        # 5
    print(password_check("saiteja8"))               # True
