import random
import sys

import scipy.stats

def read_from_stdin():
    simulated_data = DataFrame()
    header = sys.stdin.readline()
    header = header.strip().split(",")
    assert header[0] == "iso"
    fnames = header[1:]
    uniqs = []
    for line in sys.stdin:
        line = line.strip().split(",")
        iso, values = line[0], line[1:]
        simulated_data.data[iso] = {}
        for field, value in zip(fnames, values):
            simulated_data.data[iso][field] = value
            if value != "?" and value not in uniqs:
                uniqs.append(value)
    if len(uniqs) == 2:
        simulated_data.datatype = "binary"
    else:
        simulated_data.datatype = "multi"
    return simulated_data

def read_from_beast_xml(filename):
    """Read an XML file produced by a BEAST simulation."""

    simulated_data = DataFrame()
    fp = open(filename,"r")
    for line in fp:
        if "sequence" in line:
            row = {}
            junk, jank, lang, data = line.strip().split()
            iso = lang[7:-1]  
            data = data[7:-3]
            if "," in data:
                data = data.split(",")
            for f,d in enumerate(data):
                row["f%03d" % f] = d
            simulated_data.data[iso] = row
    return simulated_data

class DataFrame:

    def __init__(self):
        self.data = {}

    def format_output(self):
        iso_codes = self.data.keys()
        iso_codes.sort()
        fnames = self.data[iso_codes[0]].keys()
        fnames.sort()
        lines = []
        lines.append("iso,"+",".join(fnames))
        for iso in iso_codes:
            lines.append(iso + "," + ",".join(map(str,[self.data[iso][f] for f in fnames])))
        return "\n".join(lines)

    def stochastic_duplication(self, p=0.1, lambdaa=1, strength=0.7):
        iso_codes = self.data.keys()
        fnames = self.data[iso_codes[0]].keys()
        fnames = [name for name in fnames if "_dup" not in name]
        duplicated_features = [f for f in fnames if random.random() <= p]
        duplication_counts = [1+n for n in scipy.stats.poisson.rvs(lambdaa-1,loc=0,size=len(duplicated_features))]
        uid = "".join(random.sample("abcdefghijklmnopqrstuvwxyz",3))
        for iso in self.data:
            for df,count in zip(duplicated_features, duplication_counts):
                if self.datatype == "multi":
                    empirical= [self.data[i][df] for i in iso_codes]
                    empirical= [x for x in empirical if x != self.data[iso][df]]
                for n in range(0,count):
                    if self.datatype == "binary":
                        if self.data[iso][df] == "1":
                            dup = "1" if random.random() <= strength else "0"
                        else:
                            dup = "0" if random.random() <= strength else "1"
                    elif self.datatype == "multi":
                        dup = self.data[iso][df]
                        if random.random() > strength and empirical:
                            while dup == self.data[iso][df]:
                                dup = random.sample(empirical,1)[0]
                    self.data[iso][df+"_dup_%s_%03d" % (uid,n)] = dup

    def remove(self, removal_rate):
        iso_codes = self.data.keys()
        fnames = self.data[iso_codes[0]].keys()
        n = len(iso_codes) * len(fnames)
        to_kill = int(removal_rate*n)
        for i in range(0, to_kill):
            iso = random.sample(iso_codes,1)[0]
            fname = random.sample(fnames,1)[0]
            self.data[iso][fname] = "?"
