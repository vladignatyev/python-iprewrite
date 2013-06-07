from iprewrite import iprewrite

ranges = iprewrite.loadRanges('ranges.txt')

print iprewrite.ipinrange("192.168.1.10", ranges)
print iprewrite.ipinrange("192.168.1.1", ranges)
print iprewrite.ipinrange("213.120.1.1", ranges)
