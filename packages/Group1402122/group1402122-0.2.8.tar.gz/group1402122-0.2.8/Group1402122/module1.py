import anndata as ad  # type: ignore
import numpy as np  # type: ignore
import pandas as pd  # type: ignore
from scipy.sparse import csr_matrix  # type: ignore


def SimpleTest():
    return "If you read this message, the package works."




def simpleCreateAnnDataTest():
    counts = csr_matrix(np.random.poisson(1, size=(100, 2000)), dtype=np.float32)
    adata = ad.AnnData(counts)
    return adata
