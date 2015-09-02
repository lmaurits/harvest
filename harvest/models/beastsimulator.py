import os

import harvest.dataframe
from harvest.models.simulator import Simulator

class BeastSimulator(Simulator):

    def __init__(self, tree, n_features):
        Simulator.__init__(self, tree, n_features)

    def generate_beast_xml(self):
        # Subclasses should implement this
        return None

    def generate_data(self):
        # Generate BEAST XML file to do simulation
        xml = self.generate_beast_xml()
        temp_filename = xml.write_file(overwrite=True)
        # Run BEAST simulation
        os.system("beast %s > /dev/null" %  temp_filename)
        # Delete BEAST XML file
        os.remove(temp_filename)
        # Read simulated data
        data = harvest.dataframe.read_from_beast_xml(xml.output_filename)
        # Delete simualted data
        os.remove(xml.output_filename)
        self.data = data
        self.data.datatype = self.datatype
