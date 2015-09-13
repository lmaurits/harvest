# harvest

Harvest is a command-line tool for growing data on phylogenetic trees.  It was written with linguistic data (such as cognate class assignments) in mind, but some of its models are generic enough that its output could be interpreted as morphological or genetic data.  Output is in CSV format, with rows corresponding to languages (taxa) and columns to features (sites, traits, etc.).

Harvest is currently dependent on [DendroPy](https://pythonhosted.org/DendroPy/) for generating Yule trees and on [BEAST 2](http://beast2.org/) for some (but not all) of its data models.  Both of these dependencies *may* be removed in future.

# Command line usage

	Usage: harvest [options]

	Options:
	  -h, --help            show this help message and exit
	  -b BIRTHRATE, --birthrate=BIRTHRATE
				Birthrate for Yule tree growing process (positive
				float)
	  -B BORROWING, --borrowing=BORROWING
				Borrowing probability for Dollo model (probability)
	  -c COGNATE_BIRTHRATE, --cognate=COGNATE_BIRTHRATE
				Birthrate for new cognate classes for Dollo model
				(positive float)
	  -d DUPLICATION_RATE, --duplication=DUPLICATION_RATE
				Feature duplication rate (probability
	  -f FEATURES, --features=FEATURES
				Number of features to generate (prior to duplication)
				(integer)
	  -F DUPLICATION_FIDELITY, --duplication-fidelity=DUPLICATION_FIDELITY
				Duplication fidelity (probability)
	  -g GAMMA, --gamma=GAMMA
				Gamma rate variation parameter for Dollo model
				(positive float)
	  -i DUPLICATION_INTENSITY, --duplication-intensity=DUPLICATION_INTENSITY
				Duplication intensity (positive float)
	  -l LANGUAGES, --languages=LANGUAGES
				Number of languges to generate data for (integer)
	  -m MODEL, --model=MODEL
				Model to use for data generation (either "dollo" or
				"mk")
	  -n STATES, --states=STATES
            	                Number of states to use for Mk model
	  -q MISSING_DATA_RATE, --qmarks=MISSING_DATA_RATE
				Missing data frequency (probability)
	  -r, --recurse         Read data from stdin, rather than growing on tree
	  -t TREEFILE, --treefile=TREEFILE
				Filename to save generated tree to (Newick format)

# Tree generation

Trees are generated randomly according to the Yule pure-birth process, with birthrate specified by -b.  The generated tree can be saved to a file in Newick format by providing a filename with the -t option, otherwise the tree will be discarded.

# Data models

Current Harvest supports two data models for growing data on trees, and one of these can be specified with -m.

The first is the Lewis Mk model, which is simply a generalisation of Jukes-Cantor to an arbitrary state space size (instead of being fixed at 4).  All states are equally stable and transitions fro any given state to any other state are all equiprobable.  The size of the state space is specified with the -n option.  This model is intended for generating "structural" data, such as that found in [WALS](http://wals.info/).

The second is a "stochastic Dollo with borrowing" model, intended for generating cognate class data.  New cognate classes are born on the tree at a constant rate (specified with -c, and optionally with Gamma-distributed variation parameterised by -g), and each class is born only once.  A very rough approach to modelling borrowing or horizontal transmission is included: at every branch point of the tree, there is a fixed probability (specified with -B) that the cognate class will be randomly resampled from the set of classes attested anywhere on the tree at any previous point in time.

# Duplication model

Harvest permits stochastic duplication of features as a way to model non-independence of features.  The duplication process is controlled by three parameters: a duplication rate (specified with -d), a duplication intensity (-i) and a duplication fidelity (-F).  Initially, the number of features requested using -f will be generated independently.  Each of these features may or may not be duplicated - the duplication rate is a Bernouli probability for each feature to be duplicated.  If a feature is selected for duplication, it is duplicated a random number of times, the number being sampled from a Poisson distribution whose mean is the duplication intensity.  For each duplicate of a feature, its value for a given language will be copied the original feature's value for that language with probability given by the duplication fidelity.  If the value is *not* copied, it will be randomly sampled from the empirical distribution of the original feature's values, conditioned on it not matching the original feature.  If the duplication fidelity is set to 1.0, then each duplicate of a feature is a perfect copy.

# Missing data

Missing data can be simulated by providing a proportion with -q.  The full data matrix will be simulated (i.e. with number of datapoints equal to number of languages multiplied by number of features), and then a random selection of data points will be replaced with "?"s, such that the requested proportion of the data is missing.

# Recursive use

By using the -r option, you can use Harvest in a recursive manner.  When run with -r, Harvest will not generate a tree or simulate the evolution of data on that tree under a model.  Instead, it will read language-feature value data from stdin, in the same format that Harvest sends data to stdout when run without -r.  The stochastic duplication and missing data functionality will then be applied to the read in data.  This allows multiple passes of duplication or data removal with distinct parameter settings via a Unix shell pipeline.  E.g. to duplicate most features a small number of times and a few features many times, you could do this:

	harvest -m mk -d 0.90 -i 2 | harvest -r -d 0.10 -i 10
