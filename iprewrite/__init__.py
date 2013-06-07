import sys
import ipaddr
from iprewrite import regexpFromConditionString, getNetworkPrefixFromRegexpCondition, bruteforce, dumpToFile, strToIpInt, loadDump, rangesFromNumbers


def main():
    print "Reading conditions..."

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    f1 = open(input_file)
    regexpLines = f1.readlines()

    print "- Lines read %s" % len(regexpLines)

    print "Parsing conditions..."
    conditions = []
    for line in regexpLines:
        regexpCondition = regexpFromConditionString(line.strip())
        conditions.append((regexpCondition, getNetworkPrefixFromRegexpCondition(regexpCondition),))

    print "- Conditions parsed %s" % len(conditions)

    print "Bruteforcing valid IPs..."
    ips = bruteforce(conditions)
    print "- Found %s valid IPs" % len(ips)

    FILE_VALID_IPS = 'valid_ips.txt'
    dumpToFile(ips, FILE_VALID_IPS)

    print "Normalizing list of IPs"
    ipints = [ipint for ipint in strToIpInt(ips)]
    print "- IPs list consist of %s items" % len(ipints)

    FILE_IPINTS = 'ipints.txt'
    dumpToFile(ipints, FILE_IPINTS)

    ipints = [int(ip) for ip in loadDump(FILE_IPINTS)]

    print "Generating IP ranges"
    ranges = rangesFromNumbers(ipints)
    print "- Ranges generated %s " % len(ranges)

    print "Dumping ranges"
    f2 = open(output_file, 'w')
    for range in ranges:
        f2.write("%s-%s%s" % (ipaddr.IPAddress(int(range.start)), ipaddr.IPAddress(int(range.end)), '\n',))
    print "Well done. Goodbye!"
