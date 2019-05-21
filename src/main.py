import pyshark as ps
from pcap to hdf5 import pcap_to_hdf5
from keras.models import load_model

while True:
    cap = ps.LiveCapture(interface="wlan0")
    cap.sniff(timeout=600)

    device = change_me(cap)

    """
    """

    del cap