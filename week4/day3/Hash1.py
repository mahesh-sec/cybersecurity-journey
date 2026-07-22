import hashlib

stored_checksum = "aca73babe90b581ac3e6d91e1028ff7fa877da0ebc40536eea4c456485f22909"
hash_alg = "sha256"

with open("conf-files.txt", "rb") as f:
    h = hashlib.file_digest(f, hash_alg)
    checksum = h.hexdigest()

if stored_checksum == checksum:
    print("The contents of the file have not been changed.")
else:
    print("The contents of the file have been changed.")
