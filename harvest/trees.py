import itertools
import random

import dendropy
from dendropy.simulate import treesim

from harvest.true_isos import true_isos

dummy_isos = set(["".join(chars) for chars in itertools.combinations("abcdefghijklmnopqrstuvwxyz",3)])
dummy_isos = dummy_isos - set(true_isos)

def generate_yule_tree(taxa, birthrate=1.0, taxa_names=None):
    names = random.sample(true_isos, min(taxa, len(true_isos)))
    if taxa > len(true_isos):
        names.extend(random.sample(dummy_isos, taxa - len(true_isos)))
    fancytaxa = dendropy.TaxonNamespace(names)
    tree = treesim.birth_death_tree(birth_rate=birthrate, death_rate=0.0, ntax=taxa, taxon_namespace=fancytaxa)
    return tree
