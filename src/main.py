import pyshark as ps
from pcap_to_feature.pcap_to_feature import preprocessing
from keras.models import load_model

while True:
    cap = ps.LiveCapture(interface="wlan0")
    cap.sniff(timeout=600)

    device = preprocessing(cap)

    """
    """

    del cap