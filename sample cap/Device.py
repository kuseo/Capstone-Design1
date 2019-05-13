import FeatureEngineering as fe

class Device(object):
    def __init__(self):
        self.packet_info = []
        self.feature_data = []

    def append_packet_info(self, packet):
        temp = fe.PacketInfo(packet)
        self.packet_info.append(temp)