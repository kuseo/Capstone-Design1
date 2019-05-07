#sample usage of pyshark

import pyshark as ps

cap = ps.FileCapture("SynFlood Sample.pcap", only_summaries=True)
print(cap[0].time)
print(cap[1].time)
print(cap[2].time)