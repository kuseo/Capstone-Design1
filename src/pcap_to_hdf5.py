#%%
"""
import os
WORKING_DIR = "C:\\Users\\tjrkd\\OneDrive\\바탕 화면\\Capstone-Design"
os.chdir(WORKING_DIR + "\\src")
"""

import pyshark as ps
import h5py
import Device as dv

one_hot_protocol = {'TCP':0, 'UDP':1, 'HTTP':2}

if __name__ == "__main__":
    device = {} # group by source IP
    cap = ps.FileCapture("sample pcap\\UDPFlood Sample.pcap", only_summaries=True)

    # fisrt, extract packet infomations
    for value in cap:
        # only TCP, UDP, and HTTP protocol
        if value.protocol != 'TCP' and  value.protocol != 'UDP' and value.protocol != 'HTTP':
            continue

        # packet info
        packet_info = {
            'size':value.length,
            'time':value.time,
            'protocol':value.protocol,
            'destination':value.destination,
        }
        IP = value.source
        if IP in device:
            device[IP].append_packet_info(packet_info)
        else:
            device[IP] = dv.Device()
            device[IP].append_packet_info(packet_info)
    
    #second, feature engineering
    for source_IP in device:
        num_of_endpoint = device[source_IP].count_endpoint()

        # packet info -> feature data

        #very first packet
        feature_data = {
            'size':int(device[source_IP].packet_info[0]['size']),
            'one_hot_protocol':one_hot_protocol[device[source_IP].packet_info[0]['protocol']],
            'bandwidth':0.0,
            'endpoint':num_of_endpoint,
            'T1':0.0,
            'T2':0.0,
            'T3':0.0,
        }
        device[source_IP].append_feature_data(feature_data)

        index = 1
        for value in device[source_IP].packet_info[1:]:
            feature_data = {
                'size':int(value['size']),
                'one_hot_protocol':one_hot_protocol[value['protocol']],
                'bandwidth':0.0,
                'endpoint':num_of_endpoint,
            }
            # delta time, get T1
            feature_data['T1'] = float(device[source_IP].packet_info[index]['time']) - float(device[source_IP].packet_info[index - 1]['time'])
            
            # delta T1, get T2
            feature_data['T2'] = feature_data['T1'] - device[source_IP].feature_data[index-1]['T1']

            # delta T2, get T3
            feature_data['T3'] = feature_data['T2'] - device[source_IP].feature_data[index-1]['T2']
        
            device[source_IP].append_feature_data(feature_data)
            index = index + 1
        # First three packets have abnormal feature data for T1, T2, T3 since they can not be defined.
        # So we'll gonna drop those three packets.

    # Store feature datas as HDF5 format
    with h5py.File('sample.h5', 'w') as f:
        packet_set = []
        label_set = []
        
        # Loop over all feature datas
        for source_IP in device:
            for value in device[source_IP].feature_data[3:]:
                temp = list(value.values())
                packet_set.append(temp)
                label_set.append(1)

        f.create_dataset('packet', data=packet_set)
        f.create_dataset('label', data=label_set)

    
    
    '''
    # Test : loop over all feature datas
    count_device = 0
    count_feature_data = 2
    for source_IP in device:
        count_device = count_device + 1
        print(source_IP + " : ")
        for value in device[source_IP].feature_data[3:]:
            count_feature_data = count_feature_data + 1
            print("\tpacket number " + str(count_feature_data) + ": " + str(value.size) + "\t" + str(value.T1)  + "\t" + str(value.T2) + "\t" + str(value.T3) + "\t" + str(value.protocol) + "\t" + str(value.bandwidth) + "\t" + str(value.endpoint))
    print(count_device, count_feature_data)
    '''
    