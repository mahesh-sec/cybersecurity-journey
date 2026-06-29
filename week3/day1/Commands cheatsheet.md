# Commands I Keep Forgetting

## Filenames starting with a dash
A leading `-` gets read as a command flag, not a filename.
```bash
cat -- -filename     # -- tells the command "stop parsing flags, rest are filenames"
cat ./-filename       # prefixing with ./ also works
```

## Filenames with spaces
```bash
cat "file name with spaces"     # quotes = one argument
cat file\ name\ with\ spaces    # or escape each space individually
```

## grep matches substrings, not concepts
`grep "root" /etc/passwd` also matches lines containing "chroot" — anything containing those 4 letters.
Anchor to the start of the line to avoid false positives:
```bash
grep "^root:" /etc/passwd
```

## Excluding grep's own match from a pipeline
```bash
ps aux | grep ssh | grep -v grep
```
`-v` inverts the match — excludes lines containing "grep".

## Checking if a service is actually running (not just installed)
```bash
sudo systemctl status ssh
```
`ps aux | grep <service>` only shows it if a process is currently active — won't tell you if it's disabled at boot.

## /proc vs /run
- `/proc` — kernel-generated automatically, tracks live processes. Gone when process ends.
- `/run` — written by the process itself (PID files, sockets) so other programs can find it. Also cleared on reboot (tmpfs).

## cut to extract a field
```bash
cat /etc/passwd | cut -d: -f1    # -d: sets delimiter, -f1 = first field
```

## Redirect vs append
```bash
command > file.txt    # overwrites file.txt
command >> file.txt   # appends to file.txt
```

## ls -b reveals hidden spacing/special characters in filenames
Useful when a filename looks ambiguous from normal `ls` output.
