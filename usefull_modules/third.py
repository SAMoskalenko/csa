import subprocess, ipaddress, tabulate

def host_range_ping_tab(start, end):
    work = []
    broke = []

    st_point = start.split('.')[3]
    end_point = end.split('.')[3]
    base = start[:-len(st_point)]
    for i in range(int(st_point), int(end_point) + 1):
        ip_addr = base + str(i)
        ip_ad = ipaddress.ip_address(ip_addr)
        result = subprocess.run(f'ping -c 1 {ip_ad}', shell=True)
        if result.returncode == 0:
            work.append(f'{ip_ad}')
        else:
            broke.append(f'{ip_ad}')

    combo = []

    for i in range(int(end_point)-int(st_point)):
        el = {}
        if len(work) > i:
            el['Reachable'] = work[i]
        if len(broke) > i:
            el['Unreachable'] = broke[i]
        combo.append(el)

    return (tabulate.tabulate(combo, stralign='center', headers='keys', tablefmt="pipe"))

print(host_range_ping_tab('10.0.0.1', '10.0.0.3'))