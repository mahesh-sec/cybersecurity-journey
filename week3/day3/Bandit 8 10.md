# OverTheWire Bandit — Levels 8–10

## Level 8 → 9

**Goal:** The password is the only line in `data.txt` that occurs exactly once; every other line is duplicated.

**Command:**
```bash
sort data.txt | uniq -u
```

**Why this pipeline, not just `uniq -u` alone:**
`uniq` only detects duplicate lines that are **adjacent** to each other — it does not scan the whole file for matches. `sort` must run first to group identical lines together; only then can `uniq -u` correctly isolate the single line with no duplicate anywhere in the file.

## Level 9 → 10

**Goal:** The password is buried inside a file (`data.txt`) containing mostly binary/non-printable data, preceded by a recognizable marker in the surrounding text.

**Command:**
```bash
strings data.txt | grep '^='
```

**Why:**
- `strings` extracts only human-readable/printable text from a file that's otherwise binary garbage — without it, the password would be unreadable noise mixed with non-text bytes.
- `grep` then filters that extracted text down to the line(s) matching the marker pattern immediately preceding the actual password, cutting out irrelevant readable strings picked up by `strings`.

## Level 10 → 11

**Goal:** The password is base64-encoded inside `data.txt`.

**Command:**
```bash
base64 -d data.txt
```

**Why:**
Base64 is an encoding, not encryption — no key is required to reverse it. `-d` (decode) converts the encoded text back to its original plaintext form, revealing the password directly.

## Summary

| Level | Core skill | Command |
|---|---|---|
| 8 | Deduplication / uniqueness detection | `sort` \| `uniq -u` |
| 9 | Extracting readable text from binary noise | `strings` \| `grep` |
| 10 | Reversing a simple encoding | `base64 -d` |
