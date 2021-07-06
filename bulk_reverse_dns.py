import dns.resolver
import dns.reversename

with open("iocs.txt", 'r') as f:
    outlines= []
    for line in f:
        line=line.strip('\n')
        l = []
        for a in dns.resolver.resolve(dns.reversename.from_address(line), 'PTR'):
            l.append(a)
        s = "{}: {}".format(line, l)
        outlines.append(s)
        print(s)
with open("out.txt") as out:
    out.writelines(outlines)
