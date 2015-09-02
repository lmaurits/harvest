import codecs
import tempfile
import xml.etree.ElementTree as ET

def indent(elem, level=0):
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

class BeastXml:

    def __init__(self, tree, n_features, rate="1.0"):
        self.tree = tree
        self.n_features = n_features
        self.taxa = [l.taxon.label for l in self.tree.leaf_nodes()]
        self.gammacount = len(self.taxa)
        self.rate = str(rate)
        self.build_xml()

    def build_xml(self):

        # Convoluted: get temporary file name (for output)
        fp = tempfile.NamedTemporaryFile(mode="w", delete=False)
        self.output_filename = fp.name
        fp.close()

        attribs = {}
        attribs["namespace"] = "beast.core:beast.evolution.alignment:beast.evolution.tree.coalescent:beast.core.util:beast.evolution.nuc:beast.evolution.operators:beast.evolution.sitemodel:beast.evolution.substitutionmodel:beast.evolution.likelihood"
        attribs["version"] ="2.0"
        self.beast = ET.Element("beast", attrib=attribs)

        # Taxa
        data = ET.SubElement(self.beast, "data", {"id":"alignment", "dataType":"binary"})
        for taxon in self.taxa:
            seq = ET.SubElement(data, "sequence", {"taxon":taxon,})
            seq.text = "?"

        # Tree
        # Simulate tree according to Yule model
        tree = ET.SubElement(self.beast, "tree", {"id":"tree", "spec": "beast.util.TreeParser", "newick":str(self.tree), "IsLabelledNewick":"true", "taxa":"@alignment"})

        # Run
        attribs = {}
        attribs["id"] = "sim"
        attribs["spec"] = "beast.app.seqgen.SequenceSimulator"
        attribs["data"] = "@alignment"
        attribs["tree"] = "@tree"
        attribs["sequencelength"] = str(self.n_features)
        attribs["outputFileName"] = self.output_filename

        self.run = ET.SubElement(self.beast, "run", attrib=attribs)

        # Site model
        site = ET.SubElement(self.run, "siteModel", {"spec":"SiteModel", "id":"siteModel", "gammaCategoryCount":str(1)})

        shape = ET.SubElement(site, "shape", {"spec":"parameter.RealParameter"})
        shape.text = "4.2"

        subst = ET.SubElement(site, "substModel", {"spec":"GeneralSubstitutionModel", "id":"gsm"})
        freq = ET.SubElement(subst, "frequencies", {"spec":"Frequencies"})
        ET.SubElement(freq, "data", {"idref":"alignment"})
        ET.SubElement(subst, "parameter", {"name":"rates", "id":"all.rates", "value":"1.0 1.0"})

        # Branch rate
        br = ET.SubElement(self.run, "branchRateModel", {"id":"StrictClock","spec":"beast.evolution.branchratemodel.StrictClockModel"})
        ET.SubElement(br, "parameter", {"dimension":"1","estimate":"false","id":"clockRate","minordimension":"1","name":"clock.rate","value":self.rate})

    def write_file(self, filename=None, overwrite=False):
        if not filename:
            # Convoluted: get temporary file name
            fp = tempfile.NamedTemporaryFile(mode="w", delete=False)
            filename = fp.name
            fp.close()
        indent(self.beast)
        xml_string = ET.tostring(self.beast, encoding="UTF-8")
        while not overwrite and os.path.exists(filename):
            response = raw_input("File %s already exists!  Enter 'y' to overwrite or provide alternative filename: " % filename)
            if response.strip().lower() == "y":
                break
            else:
                filename = response
        fp = codecs.open(filename, "w", "UTF-8")
        fp.write(unicode(xml_string, "utf-8"))
        fp.close()
        return filename
