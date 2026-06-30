# OverTheWire Bandit — Levels 4–7

## Level 4 → 5
**Goal:** Find the only human-readable file in `inhere/` directory.

**Command:**
```bash
file inhere/*
cat inhere/-file07    # only ASCII text file
```

**Why:** `file` command identifies file type. All others were binary data. Human-readable = ASCII text.

---

## Level 5 → 6
**Goal:** File in `inhere/` that is human-readable, 1033 bytes, not executable.

**Command:**
```bash
find inhere/ -readable -size 1033c ! -executable
cat inhere/maybehere07/.file2
```

**Why:** `find` flags — `-readable` filters readable files, `-size 1033c` matches exact byte size (c = bytes), `! -executable` excludes executables.

---

## Level 6 → 7
**Goal:** File somewhere on the server owned by user bandit7, group bandit6, 33 bytes.

**Command:**
```bash
find / -user bandit7 -group bandit6 -size 33c 2>/dev/null
cat /var/lib/dpkg/info/bandit7.password
```

**Why:** Searched entire filesystem with `-user`, `-group`, `-size` flags. `2>/dev/null` suppresses permission denied errors. File was outside home directory — had to search from `/`.

---

## Level 7 → 8
**Goal:** Password stored in `data.txt` next to the word "millionth".

**Command:**
```bash
grep millionth data.txt
```

**Why:** `grep` searches for a pattern in a file and returns the matching line. The password was on the same line as the word "millionth".

**Note:** `cat data.txt | grep millionth` also works but `grep millionth data.txt` is cleaner — avoids unnecessary pipe.
