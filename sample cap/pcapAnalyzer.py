#sample usage of pyshark

import pyshark as ps
import Device as dv

if __name__ == "__main__":
    device = {} #group by src IP
    cap = ps.FileCapture("SynFlood Sample.pcap", only_summaries=True)
    
    for value in cap:
        #packet info
        packet = {
            'size':value.length,
            'time':value.time,
            'protocol':value.protocol,
            'destination':value.destination,
        }
        
        #only TCP, UDP, and HTTP protocol
        if packet['protocol'] != 'TCP' and  packet['protocol'] != 'UDP' and packet['protocol'] == 'HTTP':
            continue
            
        IP = value.source
        if IP in device:
            device[IP].append_packet_info(packet)
        else:
            device[IP] = dv.Device()
            device[IP].append_packet_info(packet)

    print(device['38.198.26.9'].packet_info[0].protocol)
