#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 23 16:35:32 2019

@author: daniel
"""


from matplotlib import rc
rc("font", family="serif", size=18)

import daft
#%%
pgm = daft.PGM([2,3], grid_unit=4, node_unit=2)
# Hierarchical parameters.
pgm.add_node(daft.Node('mu', r'$\mu$', 0.7, 2.5))
# Latent variable.
pgm.add_node(daft.Node('A', r'$A_{obs,i}$', 0.7, 1.6))
# Data.
pgm.add_node(daft.Node('Aobs', r'$A_{obs,i}$', 0.7, 0.8, observed=True))
pgm.add_node(daft.Node('err', r'$\sigma_{A_{obs,i}}$', 1.4, 0.8, fixed=True, offset=[0.0,1.0]))
# Add in the edges.
pgm.add_edge('mu','A')
pgm.add_edge('A','Aobs')
pgm.add_edge('err','Aobs')
pgm.add_plate(daft.Plate([0.1, 0.2, 1.6, 1.9], label=r"$n = 1, \ldots, N$",
    shift=-0.1))

pgm.render()
pgm.figure.savefig("cyclic.pdf")