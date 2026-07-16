"""
Day 1 Practice: Dictionaries (Q10-14)
The core counting/thresholding/merging patterns used directly in the
Day 4 log parser (counting failed logins per source IP).
"""


def count_words_in_list(word_list):
    counts = {}
    for i in word_list:
        if i in counts:
            counts[i] = counts[i] + 1
        else:
            counts[i] = 1
    return counts


def count_first_words_in_file(filepath):
    counts = {}
    with open(filepath, "r") as file:
        for i in file:
            words = i.split()
            if words:  # skip blank lines
                first = words[0]
                if first in counts:
                    counts[first] = counts[first] + 1
                else:
                    counts[first] = 1
    return counts


def flag_ips_above_threshold(ip_counts, threshold=3):
    flagged = []
    for key, value in ip_counts.items():
        if value > threshold:
            flagged.append(key)
    return flagged


def merge_counts(dict_a, dict_b):
    merged = {}
    all_keys = set(dict_a.keys()) | set(dict_b.keys())

    for i in all_keys:
        if i in dict_a and i in dict_b:
            merged[i] = dict_a[i] + dict_b[i]
        elif i in dict_a:
            merged[i] = dict_a[i]
        else:
            merged[i] = dict_b[i]

    return merged


def count_words_in_file(filepath):
    """Counts EVERY word in the file, not just the first word per line.
    This is the direct skeleton for Day 4's log parser."""
    counts = {}
    with open(filepath, "r") as file:
        for line in file:
            words = line.split()
            for word in words:
                if word in counts:
                    counts[word] = counts[word] + 1
                else:
                    counts[word] = 1
    return counts


if __name__ == "__main__":
    word_list = ["cat", "dog", "cat", "bird", "dog", "cat"]
    print(count_words_in_list(word_list))
    # {'cat': 3, 'dog': 2, 'bird': 1}

    print(count_first_words_in_file("first_words.txt"))
    # {'cat': 3, 'dog': 2, 'bird': 1}

    ip_counts = {
        "192.168.1.10": 5,
        "192.168.1.15": 2,
        "192.168.1.20": 7,
        "192.168.1.25": 1
    }
    print(flag_ips_above_threshold(ip_counts))
    # ['192.168.1.10', '192.168.1.20']

    dict_a = {"cat": 3, "dog": 2, "bird": 1}
    dict_b = {"cat": 1, "dog": 5, "fish": 4}
    print(merge_counts(dict_a, dict_b))
    # {'cat': 4, 'dog': 7, 'bird': 1, 'fish': 4}

    print(count_words_in_file("sample_words.txt"))
    # {'the': 9, 'cat': 3, ...}
