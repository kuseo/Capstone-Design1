class PacketInfo(object):
    def __init__(self, packet):
        self.size = packet['size']
        self.time = packet['time']
        self.protocol = packet['protocol']
        self.dstIP = packet['destination']
        return

class FeatureData(object):
    def __init__(self):
        pass
