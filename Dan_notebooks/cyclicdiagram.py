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
pgm = daft.PGM([3,2], grid_unit=4, node_unit=2)
# Hierarchical parameters.
pgm.add_node(daft.Node('mu', r'$\mu$', 0.5, 1.3))
# Latent variable.
pgm.add_node(daft.Node('A', r'$A_{i}$', 1.5, 1.3))
# Data.
pgm.add_node(daft.Node('Aobs', r'$\hat{A}_{i}$', 1.5, 0.6, observed=True))
pgm.add_node(daft.Node('err', r'$\sigma_{\hat{A}_{i}}$', 2.4, 0.6, fixed=True, offset=[0.0,1.0]))
# Add in the edges.
pgm.add_edge('mu','A')
pgm.add_edge('A','Aobs')
pgm.add_edge('err','Aobs')
pgm.add_plate(daft.Plate([1.0, 0.2, 1.8, 1.6], label=r"$n = 1, \ldots, N$",
    shift=-0.1))

pgm.render()
pgm.figure.savefig("cyclic.pdf")
#%%
pgm = daft.PGM([3,3], grid_unit=4, node_unit=2)
# Hierarchical parameters.
pgm.add_node(daft.Node('eps', r'$\varepsilon_A, \varepsilon_B$', 0.4, 2.5))
pgm.add_node(daft.Node('alpha', r'$\alpha_A, \alpha_B$', 1.1, 2.5))
pgm.add_node(daft.Node('A', r'$\mathcal{A}_A, \mathcal{A}_B$', 1.8, 2.5))
# Latent variable.
pgm.add_node(daft.Node('f', r'$\nu_{i}$', 1.1, 1.6))
# Data.
pgm.add_node(daft.Node('fobs', r'$\hat{\nu}_{i}$', 1.1, 0.8, observed=True))
pgm.add_node(daft.Node('ferr', r'$\sigma_{\hat{\nu}_{i}}$', 0.4, 0.8, fixed=True, offset=[0.0,1.0]))
pgm.add_node(daft.Node('numaxobs', r'$\hat{\nu}_{max,i}$', 2.0, 0.8, observed=True))
pgm.add_node(daft.Node('numaxerr', r'$\sigma_{\hat{\nu}_{max,i}}$', 2.7, 0.8, fixed=True, offset=[0.0,1.0]))
# Add in the edges.
pgm.add_edge('f','fobs')
pgm.add_edge('ferr','fobs')
pgm.add_edge('numaxerr','numaxobs')
pgm.add_edge('eps', 'f')
pgm.add_edge('alpha', 'f')
pgm.add_edge('A', 'f')
pgm.add_edge('numaxobs', 'f')
pgm.add_plate(daft.Plate([0.1, 0.2, 2.8, 1.9], label=r"$n = 1, \ldots, N$",
    shift=-0.1))

pgm.render()
pgm.figure.savefig("cyclicbig.pdf")