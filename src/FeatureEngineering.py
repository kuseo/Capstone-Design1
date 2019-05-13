class PacketInfo(object):
    def __init__(self, packet):
        self.size = packet['size']
        self.time = packet['time']
        self.protocol = packet['protocol']
        self.destination = packet['destination']
        return

class FeatureData(object):
    def __init__(self, parameters):
        self.size = parameters['size']
        self.T1 = parameters['T1']
        self.T2 = parameters['T2']
        self.T3 = parameters['T3']
        self.protocol = parameters['one_hot_protocol']
        self.bandwidth = parameters['bandwidth']
        self.endpoint = parameters['endpoint']

