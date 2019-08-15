import subprocess, ipaddress

def host_ping(ip_addr):
    for i in ip_addr:
        ip_ad = ipaddress.ip_address(i)
        result = subprocess.run(f'ping -c 1 {ip_ad}', shell=True)
        if result.returncode == 0:
            print('Узел доступен')
        else:
            print('Узел недоступен')

host_ping(['10.0.0.1', '10.0.0.2', '10.0.0.3'])