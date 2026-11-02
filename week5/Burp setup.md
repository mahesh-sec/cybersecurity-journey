# Burp Suite Setup Notes

## Environment
- Burp Suite Community Edition (pre-installed on Kali Linux)
- Target browser: Firefox (inside Kali VM)
- DVWA running locally on Kali at `http://127.0.0.1:42001/`

## Setup Steps

1. **Launched Burp Suite** via Applications → 03 - Web Application Analysis → Burp Suite
   - Selected *Temporary project* → *Use Burp defaults* → *Start Burp*

2. **Confirmed proxy listener**
   - Proxy tab → Proxy settings → confirmed listener active on `127.0.0.1:8080`

3. **Configured Firefox to use the proxy**
   - Settings → Network Settings → Manual proxy configuration
   - HTTP Proxy: `127.0.0.1`, Port: `8080`
   - Checked "Also use this proxy for HTTPS"

4. **Installed Burp's CA certificate**
   - With proxy active, navigated to `http://burp` → downloaded `cacert.der`
   - Firefox → Settings → Certificates → View Certificates → Authorities → Import
   - Checked "Trust this CA to identify websites"

5. **Hit a loopback proxy issue**
   - DVWA was served on `http://127.0.0.1:42001/`
   - Firefox hardcodes `127.0.0.1`, `localhost`, and `::1` as never-proxied, regardless of proxy config — traffic silently bypassed Burp.
   - **Fix:** set `network.proxy.allow_hijacking_localhost` to `true` in `about:config`, then restarted Firefox. This allowed loopback traffic to route through the proxy correctly.

6. **Verified first intercept**
   - Turned on Intercept in the Proxy tab
   - Loaded `http://127.0.0.1:42001/` in Firefox
   - Request paused in Burp's Intercept tab — confirmed working
   - Examined headers line by line (Host, Cookie/session, User-Agent, Origin, Referer, etc.) before forwarding

## Key Takeaway
Burp intercept failures on `127.0.0.1` targets are often a browser-level loopback bypass, not a Burp misconfiguration — worth checking `about:config` before troubleshooting proxy/cert settings further.
