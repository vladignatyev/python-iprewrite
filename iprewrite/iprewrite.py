#!coding:utf-8
import re
import ipaddr
import sys


def testbrutforcerun(conditions, ranges):
    result = []
    found = 0
    observed = 0
    o = 0
    for condition in conditions:
        regexp, prefix = condition
        for i3 in range(0, 256):
            for i4 in range(0, 256):
                s = "%s.%s.%s" % (prefix, i3, i4)
                o += 1
                observed +=1
                if o % 10000 == 0:
                    print "Observed/Found: %s  /  %s" % (observed, found)
                    o = 0
                if int(ipaddr.IPAddress(s)) in ranges:
                    found += 1
                    result.append(s)
    return result




def bruteforce(conditions):
    result = []
    found = 0
    observed = 0
    o = 0
    for condition in conditions:
        regexp, prefix = condition
        for i3 in range(0, 256):
            for i4 in range(0, 256):
                s = "%s.%s.%s" % (prefix, i3, i4)
                o += 1
                observed +=1
                if o % 10000 == 0:
                    print "Observed/Found: %s  /  %s" % (observed, found)
                    o = 0
                if re.match(regexp, s):
                    found += 1
                    result.append(s)
    return result



# _list = []
# ipslist(test_re, _list, 193, 201)

# print "MATCHES FOUND"
# print "===="
# print _list

def regexpFromConditionString(string):
    """
    >>> regexpFromConditionString("RewriteCond %{REMOTE_ADDR} ^83\.220\.238\.([1-9]|[1-9][0-9]|1([0-9][0-9])|2([0-4][0-9]|5[0-4]))$ [OR]")
    '^83\\\.220\\\.238\\\.([1-9]|[1-9][0-9]|1([0-9][0-9])|2([0-4][0-9]|5[0-4]))$'
    >>> regexpFromConditionString("RewriteCond %{REMOTE_ADDR} ^83\.220\.238\.([1-9]|[1-9][0-9]|1([0-9][0-9])|2([0-4][0-9]|5[0-4]))$ ")
    '^83\\\.220\\\.238\\\.([1-9]|[1-9][0-9]|1([0-9][0-9])|2([0-4][0-9]|5[0-4]))$'
    """
    # string="RewriteCond %{REMOTE_ADDR} ^83\.220\.238\.([1-9]|[1-9][0-9]|1([0-9][0-9])|2([0-4][0-9]|5[0-4]))$ [OR]"
    # re
    return string.strip().replace("RewriteCond %{REMOTE_ADDR} ", "").replace(" [OR]", "").strip()

def getNetworkPrefixFromRegexpCondition(conditionRe):
    """
    >>> getNetworkPrefixFromRegexpCondition(regexpFromConditionString("RewriteCond %{REMOTE_ADDR} ^83\.220\.238\.([1-9]|[1-9][0-9]|1([0-9][0-9])|2([0-4][0-9]|5[0-4]))$ [OR]"))
    '83.220'
    """
    i1, i2, _ = conditionRe.split('\\.', 2)
    i1 = i1.replace('^', '')
    chunks = []
    for i in (i1, i2, ):
        if re.match('^\d+$', i):
            chunks.append(i)
    return '.'.join(chunks)

def generateIpList(sourceFile, outputFile):
    f = sourceFile
    f2 = outputFile

    conditions = []

    s = f.readline()
    while s:
        regexpCondition = regexpFromConditionString(s)
        conditions.append((regexpCondition, getNetworkPrefixFromRegexpCondition(regexpCondition),))
        s = f.readline()
    ips = bruteforce(conditions)
    for ip in ips:
        f2.write(ip + '\n')

class Range(object):
    def __init__(self, start, end):
        if end is None:
            self.isNumber = True
            self.value = start
        else:
            self.isNumber = False
            self.start = start
            self.end = end

    def __contains__(self, item):
        if self.isNumber:
            return item == self.value
        else:
            return self.start <= item <= self.end

    def __str__(self):
        if self.isNumber:
            return "%s" % self.value
        else:
            return "%s-%s" % (self.start, self.end,)

    def __eq__(self, other):
        if self.isNumber:
            if isinstance(other, int):
                return self.value == other
            elif other.isNumber:
                return self.value == other.value
        elif not self.isNumber:
            if isinstance(other, int):
                return self.start <= other <= self.end
            elif not other.isNumber:
                return self.start == other.start and self.end == other.end
        return False

    def __repr__(self):
        if self.isNumber:
            return "Number: %s" % self.value
        else:
            return "Range: [%s;%s]" % (self.start, self.end,)


def rangesFromNumbers(numbers):
    print "Started"
    s = sorted(list(set(numbers)))
    print "Sorted"
    ranges = []
    i = 0
    current_range = None
    previous_number = None
    ranges_found = 0
    print "Finding ranges..."
    while True:
        n = s[i]
        if current_range is None:
            current_range = [n,None]
        else:
            if n - previous_number == 1:
                current_range[1] = n
            else:
                ranges_found += 1
                ranges.append(Range(current_range[0], current_range[1]))
                print "Ranges found: %s" % ranges_found
                current_range = [n,None]
        previous_number = n
        i += 1
        if i == len(s):
            ranges_found += 1
            ranges.append(Range(current_range[0], current_range[1]))
            print "Ranges found: %s" % ranges_found
            return ranges


def strToIpInt(ipStrings):
    for ipStr in ipStrings:
        addr = ipaddr.IPAddress(ipStr.strip())
        i1, i2, i3, i4 = str(addr).split('.')
        if i4 == '1': # если оканчивается на .1 добавим в вывод ip-адрес с .0, чтобы не нарушать последовательность
            yield int(ipaddr.IPAddress("%s.%s.%s.%s" % (i1, i2, i3, 0)))
        if i4 == '254': # если оканчивается на 254 добавим в выводи ip-адрес оканчивающийся на .255 чтобы не нарушать последовательность
            yield int(ipaddr.IPAddress("%s.%s.%s.%s" % (i1, i2, i3, 255)))
        yield int(addr)


def dumpToFile(objects, filename):
    with open(filename, 'w') as f:
        for object in objects:
            f.write(str(object) + '\n')

def loadDump(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
        for line in lines:
            l = line.strip()
            if l != '':
                yield l


def loadRanges(filename):
    strings = loadDump(filename)
    ranges = []
    for string in strings:
        start, end = string.split('-')
        ranges.append(Range(int(ipaddr.IPAddress(start)), int(ipaddr.IPAddress(end))))
    return ranges

def ipinrange(ipstr, ranges):
    return int(ipaddr.IPAddress(ipstr)) in ranges


# [API]
#    ranges = loadRanges("ranges.txt")
#    print int(ipaddr.IPAddress("31.13.144.71")) in ranges


# [Integration test]
#    result1 = testbrutforcerun(conditions, ranges)
#    dumpToFile(sorted(list(set(result1))), "ip_ranges.txt")
#    result2 = bruteforce(conditions)
#    dumpToFile(sorted(list(set(result2))), "ip_regexps.txt")
#
#    ipranges_filtered = []
#    for r in loadDump('ip_ranges.txt'):
#        if not '.255' in r:
#            if not re.match(r'^(.+)\.0$', r):
#                ipranges_filtered.append(r)
#
#    ipregexps_filtered = []
#    for r in loadDump('ip_regexps.txt'):
#        if not '.255' in r:
#            if not re.match(r'^(.+)\.0$', r):
#                ipregexps_filtered.append(r)
#
#    dumpToFile(ipregexps_filtered, 'filtered_regexps.txt')
#    dumpToFile(ipranges_filtered, 'filtered_ipranges.txt')
#
#    print set(ipranges_filtered) == set(ipregexps_filtered)  # should be True

