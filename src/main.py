import pyshark as ps
import argparse
import os
import numpy as np
from keras.layers import Input
from keras.models import load_model
from pcap_to_feature.pcap_to_feature import preprocessing

# Argument parser
parser = argparse.ArgumentParser(description="Local Zombie Detector. Detect wheter there are botnet machines(used for DDoS attack) in local network.")

parser.add_argument("-m", "--model", type=str, default="DoS_detection_model.h5",
                    help="Network interface name")
parser.add_argument("-i", "==interface", type=str, default="로컬 영역 연결* 5",
                    help="Network interface name")
parser.add_argument("-f", "--filter", type=str, default="192.168.137.0/24",
                    help="IP filter like x.x.x.x/x")

args = parser.parse_args()
DoS_detection_model = load_model("./"+args.model)
threshold = 0.5

# main loop
while True:
    cap = ps.LiveCapture(interface=args.interface, only_summaries=True, display_filter=args.filter)
    cap.sniff(timeout=600)

    device = preprocessing(captured_object=cap)
    pair = ((key, 0.0) for key in list(device.keys()))
    device_score = dict(pair)
    # device_score would be like
    # { "11.22.33.44":0.0, "12.34.56.78":0.0, "99.88.77.66":0.0, ... }
    
    for source_IP in device:
        # calculate batch doubt score
        pred = DoS_detection_model.predict(device[source_IP].feature_data)
        device_score[source_IP] =  np.sum(pred, keepdims=False) # number of suspicious packets
        device_score[source_IP] = device_score[source_IP] / len(device_score[source_IP]) # ratio of suspicious packets

    # CLI Display
    os.system("cls") # clear console
    for source_IP in device_score:
        score = device_score[source_IP]
        if score > threshold:
            print("IP :{}\n\tsuspicious\n\t{} of packets are expected to be DoS attack.".format(source_IP, score*100))
        else:
            print("IP :{}\n\tbenign\n\tIt works well.".format(source_IP))

    # write log

    
    # Garbage collect
    del cap, device, pair, device_score, 