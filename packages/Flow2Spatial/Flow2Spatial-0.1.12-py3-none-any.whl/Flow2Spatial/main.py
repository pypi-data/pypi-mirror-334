import os
import sys

def f2s_command():
    ''' Example of taking inputs for Flow2Spatial'''
    print("usage: generator.omics(), generator.histology() and generator.random(); model.preparation(), model.training() and model.reconstruction()")


import numpy as np
def transfer_masks(adata, mask, list_s=['Cluster1', 'Cluster2','Cluster3', 'Cluster4'], RowCol=None):
    segments_list = []
    for seg_index in list_s:
        transfer = np.zeros(mask.shape)
        if RowCol == None:
            xy_index = adata.obs[['x', 'y', seg_index]].copy().astype(int)
            for index in range(adata.obs.shape[0]):
                transfer[xy_index['y'][index], xy_index['x'][index]] = xy_index[seg_index][index]
        else:
            xy_index = adata.obs[['Spot_row', 'Spot_col', seg_index]].copy().astype(int)
            for index in range(adata.obs.shape[0]):
                transfer[xy_index['Spot_row'][index], xy_index['Spot_col'][index]] = xy_index[seg_index][index]            
            
        segments_list.append(transfer.astype(int).astype(str))
    
    return(segments_list)