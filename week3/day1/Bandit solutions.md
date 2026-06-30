# OverTheWire Bandit — Levels 0–3

## Level 0
**Goal:** SSH into the Bandit server.

**Command:**
```bash
ssh bandit0@bandit.labs.overthewire.org -p 2220
# password: bandit0
```

**Why:** Standard SSH login. Port 2220 is non-default — specified with `-p` flag.

---

## Level 0 → 1
**Goal:** Password stored in a file called `readme` in the home directory.

**Command:**
```bash
ls
cat readme
```

**Why:** `ls` reveals the file. `cat` reads its contents.

---

## Level 1 → 2
**Goal:** Password stored in a file called `-` (dash).

**Command:**
```bash
cat ./-
```

**Why:** A filename starting with `-` is interpreted as a flag by most commands. Prefixing with `./` tells the shell it's a path, not an option flag.

---

## Level 2 → 3
**Goal:** Password stored in a file called `spaces in this filename`.

**Command:**
```bash
cat "spaces in this filename"
# or
cat spaces\ in\ this\ filename
```

**Why:** Spaces in filenames break shell parsing. Wrapping in quotes or escaping each space with `\` tells the shell to treat it as a single filename.

---

## Level 3 → 4
**Goal:** Password stored in a hidden file inside the `inhere/` directory.

**Command:**
```bash
cd inhere
ls -la
cat .hidden
```

**Why:** Hidden files in Linux start with `.` and are not shown by `ls` by default. `-la` flag reveals them.
