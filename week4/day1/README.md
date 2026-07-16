# Week 4 — Day 1: Python Fundamentals for Security

## Focus
Core Python fundamentals needed before building this week's four security tools (port scanner, hash checker, log parser, banner grabber): variables, data structures, functions, file I/O, exception handling, threading, datetime, and argparse.

## Topics Covered
- **Core syntax**: variables, loops, conditionals, string formatting (f-strings)
- **Data structures**: lists, tuples, sets, dictionaries — with focus on dictionaries, since they're the backbone of Thursday's log parser (counting failed logins per IP)
- **Functions**: proper use of `return` vs `print`, avoiding shadowing Python built-ins (`max`, `sum`, `dict`)
- **File I/O**: reading line-by-line, writing output, detecting blank lines
- **socket basics**: opening a TCP connection, checking if a port is open/closed with `connect_ex()`
- **Threading**: why concurrency speeds up I/O-bound tasks like port scanning (Python's GIL still allows overlap during I/O waits)
- **I/O-bound vs CPU-bound**: understanding when threading helps (I/O-bound, e.g. network waits) vs when it doesn't (CPU-bound, e.g. heavy hashing — `multiprocessing` is the right tool there instead)
- **argparse**: turning hardcoded scripts into real command-line tools
- **datetime**: parsing/comparing timestamps (needed for Day 4's log parser)

## Labs
- `scripts/socket_test.py` — basic TCP socket connection test against Metasploitable (192.168.56.101), confirming open vs closed ports using `connect_ex()`

## Practice Scripts
- `scripts/functions_practice.py` — even/odd check, temperature conversion, max-of-three, vowel counter, password strength check
- `scripts/file_handling_practice.py` — line counter, case-insensitive error-line filter, file-to-file number summing, blank-line counter
- `scripts/dictionaries_practice.py` — word frequency counting (from a list and from a file), IP threshold flagging, dictionary merging, and a reusable `count_words_in_file()` function combining functions + file I/O + dictionaries

## Key Takeaways
- `return` vs `print`: functions should hand values back to the caller, not just display them, so results can be reused elsewhere in a program
- Never name a variable or function the same as a Python built-in (`max`, `sum`, `dict`, `list`) — it silently overrides the real one and causes hard-to-find bugs
- The "check if key exists, increment or initialize" dictionary pattern is the exact mechanism Day 4's log parser will use to count failed login attempts per source IP
- Threading in Python helps I/O-bound tasks (waiting on network/disk) by overlapping wait time across threads, even with the GIL — but doesn't meaningfully speed up CPU-bound work

## Environment
- Python virtual environment (`venv`) set up for this week's work
- Standard library only used this week (`socket`, `hashlib`, `re`, `argparse`, `datetime`, `threading` — no third-party packages needed yet)

## Next
Day 2 — build the port scanner, applying socket basics + threading + I/O-bound concepts from today directly.
