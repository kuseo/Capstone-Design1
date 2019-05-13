#sample usage of pyshark

import pyshark as ps
import Device as dv

one_hot_protocol = {'TCP':0, 'UDP':1, 'HTTP':2}

if __name__ == "__main__":
    device = {} # group by source IP
    cap = ps.FileCapture("UDPFlood Sample.pcap", only_summaries=True)

    # fisrt, extract packet infomations
    for value in cap:
        # only TCP, UDP, and HTTP protocol
        if value.protocol != 'TCP' and  value.protocol != 'UDP' and value.protocol != 'HTTP':
            continue

        # packet info
        packet = {
            'size':value.length,
            'time':value.time,
            'protocol':value.protocol,
            'destination':value.destination,
        }
        
        IP = value.source
        if IP in device:
            device[IP].append_packet_info(packet)
        else:
            device[IP] = dv.Device()
            device[IP].append_packet_info(packet)
    
    #second, feature engineering
    for source_IP in device:
        num_of_endpoint = device[source_IP].count_endpoint()

        # packet info -> feature data
        index = 0
        for value in device[source_IP].packet_info:
            parameters = {
                'size':int(value.size),
                'T1':0,
                'T2':0,
                'T3':0,
                'one_hot_protocol':one_hot_protocol[value.protocol],
                'bandwidth':0,
                'endpoint':num_of_endpoint,
            }
            # delta time
            try:
                parameters['T1'] = float(device[source_IP].packet_info[index].time) - float(device[source_IP].packet_info[index - 1].time)
            except IndexError:
                parameters['T1'] = 0.0

            device[source_IP].append_feature_data(parameters)

            index = index + 1
        
        # delta T1
        index = 0
        for value in device[source_IP].feature_data:
            try:
                value.T2 = device[source_IP].feature_data[index].T1 - device[source_IP].feature_data[index-1].T1
            except IndexError:
                value.T2 = 0.0
            index = index + 1

        # delta T2
        index = 0
        for value in device[source_IP].feature_data:
            try:
                value.T3 = device[source_IP].feature_data[index].T2 - device[source_IP].feature_data[index-1].T2
            except IndexError:
                value.T3 = 0.0
            index = index + 1



    #print(device['38.198.26.9'].feature_data[0].protocol)

    # Test : loop over all feature datas
    count_device = 0
    count_feature_data = 0
    for source_IP in device:
        count_device = count_device + 1
        print(source_IP + " : ")
        for value in device[source_IP].feature_data:
            count_feature_data = count_feature_data + 1
            print("\tpacket number " + str(count_feature_data) + ": " + str(value.size) + "\t" + str(value.T1)  + "\t" + str(value.T2) + "\t" + str(value.T3) + "\t" + str(value.protocol) + "\t" + str(value.bandwidth) + "\t" + str(value.endpoint))
    print(count_device, count_feature_data)