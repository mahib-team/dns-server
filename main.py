from dnslib import DNSRecord, A, AAAA, CNAME, RR
import json
import socket
import threading

def load_domain_data(file_name="domain.json"):
    try:
        with open(file_name, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def handle_request(data, addr, domain_data, server):
    dns = DNSRecord.parse(data)
    qname = str(dns.q.qname).strip('.')
    qtype = dns.q.qtype
    
    print(f"Received query: {qname} of type {qtype}")

    reply = dns.reply()

    for qname in domain_data:
        record = domain_data[qname]
        if record['type'] == 'A':
            reply.add_answer(RR(reply.q.qname, rdata=A(record['value']), ttl=60))
        elif record['type'] == 'CNAME':
            reply.add_answer(RR(reply.q.qname, rdata=CNAME(record['value']), ttl=60))
        else:
            print(f"Unsupported record type: {record['type']}")
    
    server.sendto(reply.pack(), addr)


def start_server():
    domain_data = load_domain_data()

    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind(('0.0.0.0', 53))

    while True:
        data, add = server.recvfrom(1024)
        threading.Thread(target=handle_request, args=(data, add, domain_data, server)).start()

if __name__ == "__main__":
    start_server()