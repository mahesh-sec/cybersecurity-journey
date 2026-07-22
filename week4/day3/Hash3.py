import hashlib
import os
import argparse

parser = argparse.ArgumentParser(description="Hash creation for file")
parser.add_argument("--dir", required=True, help="Enter the directory of the files you want create hash for")
parser.add_argument("--alg", default="sha256", help="The hash algorithm you want to use")
args = parser.parse_args()

is_file = os.listdir(args.dir)
for i in is_file:
    full_path = os.path.join(args.dir, i)
    if os.path.isfile(full_path):
        with open(full_path, "rb") as f:
            result = hashlib.file_digest(f, args.alg)
            checksum = result.hexdigest()
        print(f"The hash of {i} is {checksum}")
    else:
        print(f"{i} is not a file")
