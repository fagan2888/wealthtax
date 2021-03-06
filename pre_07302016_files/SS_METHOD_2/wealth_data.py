'''
------------------------------------------------------------------------
Last updated 7/17/2015

Returns the wealth for all ages of a certain percentile.

This py-file calls the following other file(s):
            data/wealth/scf2007to2013_wealth_age_all_percentiles.csv

This py-file creates the following other file(s):
    (make sure that an OUTPUT folder exists)
            OUTPUT/Demographics/distribution_of_wealth_data.png
            OUTPUT/Demographics/distribution_of_wealth_data_log.png
            OUTPUT/Saved_moments/wealth_data_moments.pkl
------------------------------------------------------------------------
'''

'''
------------------------------------------------------------------------
    Packages
------------------------------------------------------------------------
'''

import numpy as np
import pandas as pd
from scipy import stats
import cPickle as pickle


'''
------------------------------------------------------------------------
    Import Data
------------------------------------------------------------------------
'''

data = pd.read_table("data/wealth/scf2007to2013_wealth_age_all_percentiles.csv", sep=',', header=0)

'''
------------------------------------------------------------------------
    Graph Data
------------------------------------------------------------------------
'''


def wealth_data_graphs():
    '''
    Graphs wealth distribution and its log
    '''
    import matplotlib
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D
    to_graph = np.array(data)[:, 1:-1]

    domain = np.linspace(18, 95, 78)
    Jgrid = np.linspace(1, 99, 99)
    X, Y = np.meshgrid(domain, Jgrid)
    cmap2 = matplotlib.cm.get_cmap('summer')
    fig10 = plt.figure()
    ax10 = fig10.gca(projection='3d')
    ax10.plot_surface(X, Y, (to_graph).T, rstride=1, cstride=2, cmap=cmap2)
    ax10.set_xlabel(r'age-$s$')
    ax10.set_ylabel(r'percentile')
    ax10.set_zlabel(r'wealth')
    plt.savefig('OUTPUT/Demographics/distribution_of_wealth_data')

    fig10 = plt.figure()
    ax10 = fig10.gca(projection='3d')
    ax10.plot_surface(X, Y, np.log(to_graph).T, rstride=1, cstride=2, cmap=cmap2)
    ax10.set_xlabel(r'age-$s$')
    ax10.set_ylabel(r'percentile')
    ax10.set_zlabel(r'log of wealth')
    plt.savefig('OUTPUT/Demographics/distribution_of_wealth_data_log')

'''
------------------------------------------------------------------------
    Get wealth moments of a desired percentile
------------------------------------------------------------------------
'''
# Restrict the data: it has other columns that give weights and indexes the age
data2 = np.array(data)[:, 1:-1]


def get_wealth_data(bin_weights, J, flag_graphs):
    '''
    Inputs:
        bin_weights = ability weights (Jx1 array)
        J = number of ability groups (scalar)
        flag_graphs = whether or not to graph distribution (bool)
    Output:
        Saves a pickle of the desired wealth percentiles.  Graphs those levels.
    '''
    if flag_graphs:
        wealth_data_graphs()
    perc_array = np.zeros(J)
    # convert bin_weights to integers to index the array of data moments
    bins2 = (bin_weights * 100).astype(int)
    perc_array = np.cumsum(bins2)
    perc_array -= 1
    wealth_data_array = np.zeros((78, J))
    wealth_data_array[:, 0] = data2[:, :perc_array[0]].mean(axis=1)
    # pull out the data moments for each percentile
    for j in xrange(1, J):
        wealth_data_array[:, j] = data2[:, perc_array[j-1]:perc_array[j]].mean(axis=1)
    var_names = ['wealth_data_array']
    dictionary = {}
    for key in var_names:
        dictionary[key] = locals()[key]
    pickle.dump(dictionary, open("OUTPUT/Saved_moments/wealth_data_moments.pkl", "w"))
