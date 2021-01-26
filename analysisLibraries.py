######################################
################ SCIENCE LIBRARIES ###
######################################

import numpy as np
import pandas as pd
import scanpy as sc
import scvelo as scv
import anndata as ad
import scipy as spy

######################################
################ plot/viz ############
######################################

import seaborn as sns

import matplotlib.pyplot as plt
from matplotlib import rcParams

from IPython.display import Markdown, display

#%matplotlib inline

#########################
################ RPY2 ###
#########################

import rpy2.rinterface_lib.callbacks
import logging

from rpy2.robjects import pandas2ri
import anndata2ri

# Ignore R warning messages
#Note: this can be commented out to get more verbose R output
rpy2.rinterface_lib.callbacks.logger.setLevel(logging.ERROR)

# Automatically convert rpy2 outputs to pandas dataframes
pandas2ri.activate()
anndata2ri.activate()
#%load_ext rpy2.ipython


