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
            'protocolName':value.protocol,
            'dst':value.destination,
        }
        IP = value.source
        if IP in device:
            device[IP].appendPacketinfo(packet)
        else:
            device[IP] = dv.Device()
            device[IP].appendPacketinfo(packet)

    print(device)