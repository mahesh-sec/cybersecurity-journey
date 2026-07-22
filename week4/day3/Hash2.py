import hashlib
import os

isfile = os.listdir("/home/kali")

try:
    hash_alg = input("write a hash function :")
    for i in isfile:
        full_path = os.path.join("/home/kali", i)
        if os.path.isfile(full_path):
            with open(full_path, "rb") as f:
                result = hashlib.file_digest(f, hash_alg)
                checksum = result.hexdigest()
            print(f"The hash of {i} is {checksum}")
        else:
            print(f"The {i} is not a file")
except Exception:
    print("Enter correct hash algorithm")
