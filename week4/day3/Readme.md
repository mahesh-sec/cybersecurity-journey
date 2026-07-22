# File Hash Checker

A Python CLI tool for computing cryptographic hashes of files — either a single file to verify against a known-good checksum, or every file in a directory to generate a hash report. Built as part of Week 4 (Python for Security) of my cybersecurity roadmap.

## What it does

- Computes the hash (SHA256, MD5, or any algorithm supported by `hashlib`) of every file in a given directory.
- Skips non-file entries (subdirectories) automatically instead of erroring out.
- Supports choosing the hash algorithm via a command-line flag, defaulting to SHA256 if none is given.
- Earlier versions (see `earlier-versions/`) support single-file hash comparison against a known-good stored checksum — useful for file integrity verification.

## Security concept

File hashing is used in security work for two main purposes:
1. **File integrity verification** — confirming a file hasn't been tampered with or corrupted, by comparing its current hash to a previously recorded "known-good" hash.
2. **Malware identification** — analysts hash suspicious files and check them against threat intelligence databases (e.g. VirusTotal, NVD) to see if the exact file is already known-malicious.

## Usage

```bash
python hash3.py --dir /home/kali --alg sha256
python hash3.py --dir /home/kali          # --alg is optional, defaults to sha256
```

## Example output

```
The hash of .zshrc is 56ad0fc1f9cb19c6c8f3c1db7e370ba79629b8c08d645350e7697ba5fd58a3ed
The hash of conf-files.txt is a724587eb6aa5a0b0ff355196433b3b7a83f798b0ab1ddf37333161f9642d66d
Pictures is not a file
Downloads is not a file
```

## Bugs found and fixed along the way

- **Algorithm mismatch**: initially compared an MD5-computed hash against a SHA256 stored checksum. The two will never match since they're different hash types and lengths — the stored checksum and verification algorithm must always agree.
- **Relative vs. absolute paths**: `os.path.isfile()` was checking a full path built with `os.path.join()`, but `open()` was still using just the bare filename. This only worked by coincidence when the script happened to run from the same directory being scanned. Fixed by using the joined `full_path` consistently in both the check and the `open()` call.
- **Contradictory argparse setup**: originally had `default="sha256"` alongside `required=True` on the `--alg` argument — since it was required, the default could never actually be used. Removed `required=True` so the default is meaningful and `--alg` becomes a genuinely optional flag.

## Notes on error handling

The algorithm name is validated once, since an invalid algorithm would fail identically for every file in the directory — better to catch that early than print the same error 50 times. Per-file errors (e.g. permission issues on a single file) are handled separately so one bad file doesn't stop the whole directory scan.
