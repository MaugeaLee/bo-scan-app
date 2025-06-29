import socket

import psutil


def get_network_summary():
    info = []
    for iface_name, addrs in psutil.net_if_addrs().items(): # 현제 arp의 모든 interface 조회
        iface_info = {"interface": iface_name, "ip": None, "mac": None, "netmask": None}
        for addr in addrs:
            if addr.family == socket.AF_INET:
                iface_info["ip"] = addr.address
                iface_info["netmask"] = addr.netmask
            elif addr.family == psutil.AF_LINK:
                iface_info["mac"] = addr.address
            info.append(iface_info)
    return info

def get_summary_used_search(local_ip:str ,summary: list):
    for iface in summary:
        if local_ip == iface["ip"]:
            return iface

    return False

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Google DNS를 통해 IP 확인
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip


if __name__ == "__main__":
    network_summary = get_network_summary()
    local_ip = get_local_ip()
    local_ip = get_summary_used_search(local_ip, network_summary)

    print(local_ip)