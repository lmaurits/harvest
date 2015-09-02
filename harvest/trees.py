import itertools

import dendropy
from dendropy.simulate import treesim

names = ["".join(chars) for chars in itertools.combinations("abcdefghijklmnopqrstuvwxyz",3)]

def generate_yule_tree(taxa, birthrate=1.0, taxa_names=None):
    fancytaxa = dendropy.TaxonNamespace(names[0:taxa])
    tree = treesim.birth_death_tree(birth_rate=birthrate, death_rate=0.0, ntax=taxa, taxon_namespace=fancytaxa)
    return tree
