import re
failed_attempts = {}
pattern = re.compile(r'([0-9-]+T[0-9:-]+)\s[a-z]{4}\s[a-z0-9\[\]-]+:\s(Failed|Accepted)\spassword\sfor\s(invalid\suser\s([a-z]+))?([a-z0-9]+)?\sfrom\s([:.\da-fA-F]+)\sport\s(\d+)\s[a-z0-9]+')
with open("auth_sample.log","r") as f:
    for i in f:
        log = pattern.search(i)
        if log:
            if log.group(5) == None:
                print(f"The time is {log.group(1)} , the username is {log.group(4)},the ip is {log.group(6)} from port {log.group(7)}")
                if log.group(2) == "Failed":
                    if log.group(4) in failed_attempts:
                        failed_attempts[log.group(4)] = failed_attempts[log.group(4)] + 1
                    else:
                        failed_attempts[log.group(4)] = 1
            elif log.group(4) == None:
                print(f"The time is {log.group(1)} , the username is {log.group(5)},the ip is {log.group(6)} from port {log.group(7)}")
                if log.group(2) == "Failed":
                    if log.group(5) in failed_attempts:
                        failed_attempts[log.group(5)] = failed_attempts[log.group(5)] + 1
                    else:
                        failed_attempts[log.group(5)] = 1
for key,values in failed_attempts.items():
    if values >= 5:
        print(f"ALERT: '{key}' had {values} failed login attempts - possible brute-force activity")
