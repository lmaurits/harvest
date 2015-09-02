import harvest.dataframe
from harvest.models.beastsimulator import BeastSimulator
from harvest.models.beastxml import BeastXml

class MkSimulator(BeastSimulator):

    def __init__(self, tree, n_features):
        BeastSimulator.__init__(self, tree, n_features)
        height = self.tree.max_distance_from_root()
        self.rate = str((0.5 / height))
        self.datatype = "multi"

    def generate_beast_xml(self):
        return BeastXml(self.tree, self.n_features, self.rate)
