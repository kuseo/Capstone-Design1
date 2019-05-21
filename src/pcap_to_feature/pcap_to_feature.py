# import some useful moudles
import pyshark as ps
import h5py
import argparse
import Device as dv

def preprocessing(input):
    # Prepare some variables
    one_hot_protocol = {"TCP":0, "UDP":1, "ICMP":2}
    device = {} # group by source IP
    cap = ps.FileCapture(input, only_summaries=True)

    # Fisrt, extract packet infomations
    for value in cap:
        # only TCP, UDP, and ICMP protocol
        if value.protocol != "TCP" and  value.protocol != "UDP" and value.protocol != "ICMP":
            continue

        # packet info
        packet_info = {
            "size":value.length,
            "time":value.time,
            "protocol":value.protocol,
            "destination":value.destination,
        }
        IP = value.source
        if IP in device:
            device[IP].append_packet_info(packet_info)
        else:
            device[IP] = dv.Device()
            device[IP].append_packet_info(packet_info)

    # Second, feature engineering
    for source_IP in device:
        num_of_endpoint = device[source_IP].count_endpoint()

        # packet info -> feature data

        # very first packet
        feature_data = {
            "size":int(device[source_IP].packet_info[0]["size"]),
            "one_hot_protocol":one_hot_protocol[device[source_IP].packet_info[0]["protocol"]],
            "bandwidth":0.0,
            "endpoint":num_of_endpoint,
            "T1":0.0,
            "T2":0.0,
            "T3":0.0,
        }
        device[source_IP].append_feature_data(feature_data)

        index = 1
        for value in device[source_IP].packet_info[1:]:
            feature_data = {
                "size":int(value["size"]),
                "one_hot_protocol":one_hot_protocol[value["protocol"]],
                "bandwidth":0.0,
                "endpoint":num_of_endpoint,
            }
            # delta time, get T1
            feature_data["T1"] = float(device[source_IP].packet_info[index]["time"]) - float(device[source_IP].packet_info[index - 1]["time"])
            
            # delta T1, get T2
            feature_data["T2"] = feature_data["T1"] - device[source_IP].feature_data[index-1]["T1"]

            # delta T2, get T3
            feature_data["T3"] = feature_data["T2"] - device[source_IP].feature_data[index-1]["T2"]
        
            device[source_IP].append_feature_data(feature_data)
            index = index + 1
        # The first three packets have abnormal feature data for T1, T2, T3 since they can not be defined.
        # So we'll gonna drop those three packets.

        return device

if __name__ == "__main__":
    # Argument parser
    parser = argparse.ArgumentParser(description="pcap to HDF5. You can use this program to generate data sets for either training or prediction")
    parser.add_argument("input", 
                        help="Input pcap file directory")

    #positive   : benign
    #negative   : attack
    parser.add_argument("-l", "--label", type=str, choices=["pos", "neg"],
                        help="Category of input pcap file. default is neg")
    parser.add_argument("-o", "--output", type=str, default="output.h5",
                        help="Output h5 file")
    parser.add_argument("-v", "--verbose", action="store_true",
                    help="Increase verbosity")


    args = parser.parse_args()

    device = preprocessing(args.input)

    # Store feature datas as HDF5 format
    with h5py.File(args.output, "w") as f:
        packet_set = []
        label_set = []
        label = 1 if args.label == "pos" else 0
        # Loop over all feature datas
        for source_IP in device:
            for value in device[source_IP].feature_data[3:]: # drop the first three packets
                temp = list(value.values()) # dictionary to list
                packet_set.append(temp)
                label_set.append(label)

        f.create_dataset("data_x", data=packet_set)
        f.create_dataset("data_y", data=label_set)

    #%% verbose output
    if args.verbose:
        num_of_packet = 0
        for source_IP in device:
            num_of_packet = num_of_packet + len(device[source_IP].packet_info)
        print("Done.\nTotal {} packets from {} devices.\nThe first three packets were dropped.".format(num_of_packet, len(device)))