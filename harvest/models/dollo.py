import random

from dendropy.simulate import treesim
import scipy.stats

import harvest.dataframe
from harvest.models.simulator import Simulator

class DolloSimulator(Simulator):

    def __init__(self, tree, n_features, cognate_birthrate=0.5, cognate_gamma=1.0):
        Simulator.__init__(self, tree, n_features)
        self.cognate_birthrate = cognate_birthrate
        self.cognate_gamma = cognate_gamma

    def generate_data(self):
        """Generate cognate class data in a Dollo-like fashion."""
        self.data = harvest.dataframe.DataFrame()
        self.data.datatype = "binary"
        for i in range(0, self.n_features):
            gamma = scipy.stats.gamma(self.cognate_gamma,scale=1.0/self.cognate_gamma).rvs()
            attested_cognates = [1]
            first = True
            for parent in self.tree.preorder_node_iter():
                if first:
                    parent.cognate = 1
                    next_cognate = parent.cognate + 1
                    first = False
                for child in parent.child_node_iter():
                    # Number of changes is Poisson distributed
                    timerate = child.edge_length*self.cognate_birthrate*gamma
                    changes = scipy.stats.poisson(timerate).rvs()
                    if changes:
                        # A mutation has occurred.
                        child.cognate = next_cognate
                        attested_cognates.append(next_cognate)
                        next_cognate += 1
                    else:
                        # No change has occurred, so propagate the parent's cognate value
                        child.cognate = parent.cognate
            terminal_values = []
            for leaf in self.tree.leaf_node_iter():
                if leaf.cognate not in terminal_values:
                    terminal_values.append(leaf.cognate)
            terminal_values.sort()
            trans = dict([(v,n) for (n,v) in enumerate(terminal_values)])
            for leaf in self.tree.leaf_node_iter():
                iso = str(leaf.taxon)[1:-1]
                if iso not in self.data.data:
                    self.data.data[iso] = {}
                self.data.data[iso]["f_%03d" % i] = trans[leaf.cognate]
