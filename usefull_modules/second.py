import subprocess, ipaddress

def host_range_ping_tab(start, end):
    st_point = start.split('.')[3]
    end_point = end.split('.')[3]
    base = start[:-len(st_point)]
    for i in range(int(st_point), int(end_point)+1):
        ip_addr = base+str(i)
        ip_ad = ipaddress.ip_address(ip_addr)
        result = subprocess.run(f'ping -c 1 {ip_ad}', shell=True)
        if result.returncode == 0:
            print(f'Узел {ip_ad} доступен')
        else:
            print(f'Узел {ip_ad} недоступен')


host_range_ping_tab('10.0.0.1', '10.0.0.3')

