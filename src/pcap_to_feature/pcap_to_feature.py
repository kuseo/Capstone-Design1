# import some useful moudles
import pyshark as ps
import h5py
import argparse
import Device as dv

def preprocessing(pcap_input=None, captured_object=None):
    # Prepare some variables
    one_hot_protocol = {"TCP":0, "UDP":1, "HTTP":2}
    device = {} # group by source IP

    if captured_object is None:
        cap = ps.FileCapture(pcap_input, only_summaries=True)
    else:
        cap = captured_object

    # Fisrt, extract packet infomations
    for value in cap:
        # only TCP, UDP, and ICMP protocol
        if value.protocol != "TCP" and  value.protocol != "UDP" and value.protocol != "HTTP":
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
            device[IP].packet_info.append(packet_info)
        else:
            device[IP] = dv.Device()
            device[IP].packet_info.append(packet_info)

    # Second, record time slice with 10 sec time window.
    for source_IP in device:
        # initialize time window
        first = float(device[source_IP].packet_info[0]["time"])
        start = 0

        index = 0
        for value in device[source_IP].packet_info:
            current = float(value["time"])
            if current - first > 10: # 10 sec time window
                device[source_IP].time_window.append(start) # record time slice
                
                # update time slice
                first = current
                start = index
            index = index + 1

        # last slice
        device[source_IP].time_window.append(start)
        device[source_IP].time_window.append(index)


    # Third, feature engineering
    for source_IP in device:
        for i in range(0, len(device[source_IP].time_window) - 1): # loop over time window
            start = device[source_IP].time_window[i]
            end = device[source_IP].time_window[i+1]
            num_of_endpoint = device[source_IP].count_endpoint(start, end)

            index = 0
            for value in range(start, end): # one time window
                feature_data = {
                    "size":int(device[source_IP].packet_info[value]["size"]),
                    "one_hot_protocol":one_hot_protocol[device[source_IP].packet_info[value]["protocol"]],
                    "bandwidth":0.0,
                    "endpoint":num_of_endpoint,
                    "T1":0.0,
                    "T2":0.0,
                    "T3":0.0,
                }
                device[source_IP].feature_data.append(feature_data)

                # delta time, get T1
                feature_data["T1"] = float(device[source_IP].packet_info[value]["time"]) - float(device[source_IP].packet_info[value - 1]["time"])
                
                # delta T1, get T2
                feature_data["T2"] = feature_data["T1"] - device[source_IP].feature_data[index-1]["T1"]

                # delta T2, get T3
                feature_data["T3"] = feature_data["T2"] - device[source_IP].feature_data[index-1]["T2"]
            
                device[source_IP].feature_data[index] = feature_data
                index = index + 1
        # The first three packets have abnormal feature data for T1, T2, T3 since they can not be defined.
        # So we'll gonna drop those three packets.

    return device

if __name__ == "__main__":
    # Argument parser
    parser = argparse.ArgumentParser(description="pcap to HDF5. You can use this program to generate data sets for either training or prediction")
    parser.add_argument("input", 
                        help="Input pcap file directory")

    #positive   : attack
    #negative   : benign
    parser.add_argument("-l", "--label", type=str, choices=["pos", "neg"],
                        help="Category of input pcap file. default is neg")
    parser.add_argument("-o", "--output", type=str, default="output.h5",
                        help="Output file name")
    parser.add_argument("-v", "--verbose", action="store_true",
                    help="Increase verbosity")


    args = parser.parse_args()

    device = preprocessing(pcap_input=args.input)

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

    # verbose output
    if args.verbose:
        num_of_packet = 0
        for source_IP in device:
            num_of_packet = num_of_packet + len(device[source_IP].packet_info)
        print("Done.\nTotal {} packets from {} devices.\nThe first three packets were dropped.".format(num_of_packet, len(device)))