# File Hash Generator

## What It Does
Computes a cryptographic hash for every file in a given directory using Python's `hashlib`, and prints the filename alongside its hex digest. Defaults to SHA-256 but supports any algorithm `hashlib` provides (e.g. `sha1`, `md5`).

## How It Works
- Lists every entry in the target directory with `os.listdir`.
- Skips subdirectories — only regular files are hashed (checked via `os.path.isfile`).
- Uses `hashlib.file_digest`, which streams the file in chunks rather than loading it entirely into memory, so it scales to large files.

## Usage
```bash
python hash_tool.py --dir <directory_path> [--alg <algorithm>]
```

| Flag | Description | Default |
|---|---|---|
| `--dir` | Directory containing the files to hash (required) | — |
| `--alg` | Hash algorithm to use | `sha256` |

**Example:**
```bash
python hash_tool.py --dir /home/kali/samples --alg sha256
```

## Example Output
```
The hash of suspicious_binary.exe is e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b85
The hash of readme.txt is 2c26b46b68ffc68ff99b453c1d30413413422d706483bfa0f98a5e886266e7ae
notes is not a file
```

## Security Concept
This is a basic **file integrity / forensic hashing** utility. Cryptographic hashes act as unique fingerprints for files: analysts use them to verify a file hasn't been tampered with (comparing against a known-good baseline), to check a suspicious file against threat-intel sources like VirusTotal, or to prove chain-of-custody in digital forensics. Because even a one-byte change produces a completely different hash, this technique underlies malware identification, patch verification, and file integrity monitoring (FIM) tools like Tripwire or OSSEC.

## Possible Improvements
- Handle an invalid `--alg` value with a clear error instead of letting `hashlib` raise an unhandled exception.
- Add a `--recursive` flag to hash files in subdirectories too.
