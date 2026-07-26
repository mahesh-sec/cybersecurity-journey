# OverTheWire Bandit — Write-Ups (Levels 13–22)

Solved this week as part of the Week 4 Python/Bandit track. Levels 23–33 continuing next week.

> Note: Levels 15→16 and 17→18 weren't walked through step-by-step in my working notes this week, so those two entries below describe the standard technique for that level rather than my own exact command history — I'll swap in my actual commands/output once I revisit them.

---

### Level 13 → 14

**Task:** bandit13's home directory contains an SSH private key (`sshkey.private`) that authenticates as bandit14.

**Approach:**
1. Copy the private key off the server to a local machine (or use it directly in the same session).
2. Fix file permissions so SSH will accept it.
3. Log in as bandit14 using the key instead of a password.

**Commands used:**
```bash
scp -P 2220 -i /path/to/bandit13_key bandit13@bandit.labs.overthewire.org:/home/bandit13/sshkey.private ~/
chmod 600 ~/sshkey.private
ssh -i ~/sshkey.private bandit14@bandit.labs.overthewire.org -p 2220
```

**Result:** Logged in as bandit14 using key-based auth instead of a password.

**Concept:** SSH key-based authentication — demonstrates how a private key alone (no password) grants access, and why key files need `600` permissions or SSH will refuse to use them.

---

### Level 14 → 15

**Task:** Submit bandit14's password to a listening service on `localhost:30000` to receive bandit15's password.

**Approach:**
1. Confirm the target port is a plain TCP listener, not SSH or SSL.
2. Connect with `nc` and send the password as a line of input.

**Commands used:**
```bash
nc localhost 30000
# type bandit14's password, press Enter
```

**Result:** Server returned bandit15's password.

**Concept:** Raw TCP password submission — the challenge simulates a service that authenticates based on plaintext input over a socket, no protocol handshake required.

---

### Level 15 → 16 *(standard approach — not from this week's session notes)*

**Task:** Submit bandit15's password to `localhost:30001`, this time over **SSL/TLS**, to receive bandit16's password.

**Approach:**
1. Same idea as Level 14→15, but the port requires an SSL/TLS handshake first.
2. Use `openssl s_client` to wrap the connection.

**Commands used:**
```bash
openssl s_client -connect localhost:30001 -quiet
# type bandit15's password, press Enter
```

**Result:** Server returned bandit16's password.

**Concept:** SSL/TLS-wrapped service authentication — same password-submission idea as the prior level, but requiring a working TLS handshake before the server will accept input.

---

### Level 16 → 17

**Task:** A range of ports (31000–32000) were open on localhost. Only one presents a real SSL service tied to bandit17; submitting bandit16's password to it returns an RSA private key for bandit17. Several other ports in that range are decoys that simply echo input back without validating anything.

**Approach:**
1. Scan the port range to find every open port.
2. Test each open port for a real SSL handshake (decoys either fail the handshake outright or complete it but just echo input).
3. Submit bandit16's password to each real SSL port non-interactively (to remove ambiguity between terminal echo and server echo) until one returns a genuine private key instead of parroting the password back.

**Commands used:**
```bash
nmap -p 31000-32000 localhost
openssl s_client -connect localhost:<port> -quiet
# for each port, tested non-interactively:
(echo "<bandit16_password>"; sleep 5) | openssl s_client -connect localhost:<port> -quiet -ign_eof
```

**Result:** Port 31790 returned `Correct!` followed by a full `-----BEGIN OPENSSH PRIVATE KEY-----` block for bandit17.

**Concept:** Service enumeration under ambiguity — several ports in this level are intentionally designed to look identical (same self-signed "SnakeOil" cert, same handshake behavior) so the only reliable way to identify the real service is to test the actual response to valid input, not just whether a connection succeeds.

---

### Level 17 → 18 *(standard approach — not from this week's session notes)*

**Task:** bandit17's home directory contains two files, `passwords.old` and `passwords.new`. Exactly one line differs between them — that line is bandit18's password.

**Approach:**
1. Diff the two files to isolate the single changed line.

**Commands used:**
```bash
diff passwords.old passwords.new
```

**Result:** The differing line is bandit18's password.

**Concept:** File comparison for credential discovery — a simple but realistic example of spotting a single changed value across two versions of a file, similar to diffing config files during an audit.

---

### Level 18 → 19

**Task:** bandit18's `.bashrc` immediately terminates any interactive SSH session, making it impossible to get a normal shell.

**Approach:**
1. Bypass the interactive shell entirely by telling SSH to run a specific command remotely instead of starting a login shell.

**Commands used:**
```bash
ssh bandit18@bandit.labs.overthewire.org -p 2220 cat readme
```

**Result:** SSH authenticated, ran `cat readme` on the remote side, printed bandit19's password, and exited — without ever triggering the logout behavior.

**Concept:** Non-interactive SSH command execution — shows that SSH doesn't require a full interactive shell to run a command; this is also a common privilege-escalation/enumeration technique against restricted-shell accounts.

---

### Level 19 → 20

**Task:** A setuid binary, `bandit20-do`, runs a given command as bandit20.

**Approach:**
1. Confirm the binary elevates privileges.
2. Use it to read bandit20's password file directly.

**Commands used:**
```bash
/home/bandit19/bandit20-do id
/home/bandit19/bandit20-do cat /etc/bandit_pass/bandit20
```

**Result:** Second command printed bandit20's password.

**Concept:** setuid binary abuse — a program that runs with an elevated effective UID can be used to perform actions (like reading a privileged file) that the invoking user normally couldn't do directly. Core privilege-escalation concept.

---

### Level 20 → 21

**Task:** A binary, `suconnect`, connects to a given local port and validates whatever password it receives against bandit20's real password. If correct, it sends back bandit21's password over the same connection.

**Approach:**
1. Open a listener on an arbitrary local port.
2. Run `suconnect` pointed at that port so it connects into the listener.
3. Type bandit20's password into the listener session so it gets relayed to `suconnect`.
4. Read bandit21's password back from whichever process reports the result.

**Commands used (two separate terminals to avoid input ambiguity):**
```bash
# Terminal 1
nc -l -p 12345
# (then type bandit20's password once suconnect connects)

# Terminal 2
/home/bandit20/suconnect 12345
```

**Result:** After sending the correct password through the listener, `suconnect` validated it and returned bandit21's password.

**Concept:** Client/listener relay pattern — `suconnect` acts as a client that must receive proof of a password over a live connection (rather than reading a file), so solving it requires setting up your own end of that connection first. Also a good lesson in why backgrounding a process with `&` in a single terminal can create ambiguity about which process actually reads your keyboard input.

---

### Level 21 → 22

**Task:** A cron job (running as bandit22) periodically executes a script that writes bandit22's password to a file. The job definition lives in `/etc/cron.d/`.

**Approach:**
1. Inspect the relevant crontab file(s) in `/etc/cron.d/` to find the job running as bandit22.
2. Read the script it executes to find where it writes the password.
3. Read that output file directly.

**Commands used:**
```bash
cat /etc/cron.d/cronjob_bandit22
cat /usr/bin/cronjob_bandit22.sh
cat /tmp/<output_file_from_script>
```

**Result:** Password file contents gave bandit22's password.

**Concept:** Cron job enumeration — scheduled tasks running as another user are a classic privilege-escalation vector; if the script or its output is world-readable, any user can read what a higher-privileged cron job produces.

---

## Summary

| Level Transition | Core Technique |
|---|---|
| 13 → 14 | SSH private key authentication |
| 14 → 15 | Plain TCP password submission (`nc`) |
| 15 → 16 | SSL/TLS password submission |
| 16 → 17 | SSL service enumeration among decoy ports |
| 17 → 18 | File diffing |
| 18 → 19 | Non-interactive SSH command execution |
| 19 → 20 | setuid binary abuse |
| 20 → 21 | Client/listener password relay |
| 21 → 22 | Cron job enumeration |
