class PacketInfo(object):
    def __init__(self, packet):
        self.size = packet['size']
        self.time = packet['time']
        self.protocolName = packet['protocolName']
        self.dstIP = packet['dst']
        return

class Feature(object):
    def __init__(self):
        pass
