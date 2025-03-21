import sys
sys.path.append("/data/scverse/squidpy/src/")
sys.path

from squidpy.gr._ppatterns import _find_min_max

import scanpy as sc
import squidpy as sq
print(sq)
import pandas as pd
import numpy as np
import scstat_rs as st

import importlib
importlib.reload(sq)

adata = sq.datasets.imc()
# export the spatial data and cluster data as input
sq.gr.co_occurrence(adata, cluster_key="cell type", interval = 10) #, n_splits = 10)
adata.uns["cell type_co_occurrence"]["occ"].shape
adata.uns["cell type_co_occurrence"]["interval"]
sq.gr.co_occurrence_rs(adata, cluster_key="cell type", interval = 10)
adata.uns["cell type_co_occurrence"]["interval"].shape



## Options
ip = np.int32
fp = np.float32

spatial_key = "spatial"
cluster_key = "cell type"
interval = 10 

spatial = adata.obsm[spatial_key].astype(fp)
original_clust = adata.obs[cluster_key]

# create intervals thresholds
if isinstance(interval, int):
    thresh_min, thresh_max = _find_min_max(spatial)
    interval = np.linspace(thresh_min, thresh_max, num=interval, dtype=fp)
else:
    interval = np.array(sorted(interval), dtype=fp, copy=True)
if len(interval) <= 1:
    raise ValueError(f"Expected interval to be of length `>= 2`, found `{len(interval)}`.")

clust = original_clust.cat.codes.astype(np.int32)

co_occur_3d = st.co_occur_count(
    spatial[:, 0], 
    spatial[:, 1], 
    interval, clust
)

## for each dimension
# for i in range(co_occur.shape[2]):
num = co_occur_3d.shape[0]
labs_unique = range(co_occur_3d.shape[0])
out = np.zeros((num, num, interval.shape[0] - 1), dtype=fp)

interval_seq = np.arange(interval.shape[0] - 2, -1, -1)
interval_seq.shape[0]

for i_interval in interval_seq:
    # print(i_interval)
    co_occur = co_occur_3d[:, :, i_interval]

    probs_matrix = co_occur / np.sum(co_occur) if np.sum(co_occur) != 0 else np.zeros((num, num), dtype=fp)
    probs = np.sum(probs_matrix, axis=0)
    probs_con = np.zeros((num, num), dtype=fp)

    for c in labs_unique:
        probs_conditional = (
            co_occur[c] / np.sum(co_occur[c]) if np.sum(co_occur[c]) != 0 else np.zeros(num, dtype=fp)
        )
        probs_con[c, :] = np.zeros(num, dtype=fp)
        for i in range(num):
            if probs[i] == 0:
                probs_con[c, i] = 0
            else:
                probs_con[c, i] = probs_conditional[i] / probs[i]

    # print(interval_seq.shape[0] - 1 - i_interval)
    out[:, :, interval_seq.shape[0] - 1 - i_interval] = probs_con

out.shape

# # origin = adata.uns["cell type_co_occurrence"]["occ"][:, :, 0]
# adata.uns["cell type_co_occurrence"]["occ"][:, :, 0]
# origin_split
