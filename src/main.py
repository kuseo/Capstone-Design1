import pyshark as ps
from pcap_to_feature import pcap_to_feature
from keras.models import load_model

while True:
    cap = ps.LiveCapture(interface="wlan0")
    cap.sniff(timeout=600)

    device = preprocessing(cap)

    """
    """

    del cap