class Device(object):
    def __init__(self):
        self.packet_info = []
        self.time_window = []
        self.feature_data = []

    def append_packet_info(self, packet_info):
        self.packet_info.append(packet_info)
    
    def append_feature_data(self, feature_data):
        self.feature_data.append(feature_data)

    # count number of destinations
    def count_endpoint(self, start, end):
        endpoint = []
        for value in self.packet_info[start:end]:
            endpoint.append(value['destination'])
        endpoint = list(set(endpoint)) # delete overlapped data

        return len(endpoint)

    '''
    def calculate_average_bandwidth(self, start, end):
        pass
    '''

