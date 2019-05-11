import FeatureEngineering as fe

class Device(object):
    def __init__(self):
        self.packetinfos = []
        self.features = []

    def appendPacketinfo(self, packet):
        temp = fe.PacketInfo(packet)
        self.packetinfos.append(temp)