# Password Spray Tool

A Python tool for conducting password spray attacks in Active Directory (AD) environments during penetration tests or adversary simulations. The tool supports multiple protocols (LDAP, SMB, and Kerberos) and is designed to be stealthy, avoiding detection by EDR or SOC systems.

## Features

### Multi-Protocol Support:
- **LDAP**: Authenticate against Domain Controllers (DCs).
- **SMB**: Authenticate against file servers or other Windows servers.
- **Kerberos**: Authenticate against Domain Controllers (DCs) using the Kerberos protocol.

### Stealth Mode:
- Random delays between login attempts to avoid detection.
- Distribution of attempts across multiple hosts to dilute security events.

### Flexible Input:
- User list can be provided via a file.
- Host list can be manually specified or provided via a file.

### Detailed Output:
- Displays results in the format `[protocol] Successful/Failed login for Username @host`.
- Option to save successful logins to a file.

## Requirements

- Python 3.x

### Required Libraries:
- `ldap3`
- `impacket`

Install dependencies using:

```bash
pip install ldap3 impacket
```

## Usage

### Basic Syntax

```bash
python tugaspray.py --users <users_file> --password <password> --domain <domain> --protocol <protocol> [--hosts <hosts> | --hosts-file <hosts_file>] [--delay-min <min> --delay-max <max>] [--output-file <output_file>]
```

### Arguments

| Argument      | Description |
|--------------|------------|
| `--users`    | File containing the list of users (one per line). |
| `--password` | Password to be tested in the password spray attack. |
| `--domain`   | Domain name (e.g., CORP). |
| `--protocol` | Protocol to use: ldap, smb, or kerberos. |
| `--hosts`    | Comma-separated list of hosts (e.g., dc1.corp.local,dc2.corp.local). |
| `--hosts-file` | File containing the list of hosts (one per line). |
| `--delay-min` | Minimum delay between attempts (in seconds). Default: 2. |
| `--delay-max` | Maximum delay between attempts (in seconds). Default: 20. |
| `--output-file` | File to save successful logins. |

## Usage Examples

### Password Spray via LDAP (Domain Controllers):

```bash
python tugaspray.py --users users.txt --password P@ssw0rd --domain CORP --hosts dc1.corp.local,dc2.corp.local --protocol ldap --delay-min 2 --delay-max 20 --output-file successes.txt
```

### Password Spray via SMB (File Servers):

```bash
python tugaspray.py --users users.txt --password P@ssw0rd --domain CORP --hosts fileserver1.corp.local,fileserver2.corp.local --protocol smb --delay-min 5 --delay-max 30 --output-file successes.txt
```

### Password Spray via Kerberos (Domain Controllers):

```bash
python tugaspray.py --users users.txt --password P@ssw0rd --domain CORP --hosts-file dc_hosts.txt --protocol kerberos --delay-min 3 --delay-max 15 --output-file successes.txt
```

## Important Considerations

### Usage of LDAP and Kerberos:
- LDAP and Kerberos should only be used against Domain Controllers (DCs).
- SMB is suitable for other Windows servers, such as file servers.

### Stealth:
- The tool uses random delays between attempts to avoid detection.
- Distribute attempts across multiple hosts to dilute security events.

### Responsibility:
- Use this tool only in environments where you have explicit authorization.
- Unauthorized penetration testing is illegal and unethical.

### Output:
- The on-screen output follows the format `[protocol] Successful/Failed login for Username @host`.
- Successful logins are saved in the file specified by the `--output-file` argument.



## Contributions

Contributions are welcome! Feel free to open issues or pull requests for improvements, bug fixes, or new features.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.

## Disclaimer

This tool is developed for educational and authorized penetration testing purposes only. Misuse of this tool is the sole responsibility of the user. The author is not responsible for any illegal or malicious use.

