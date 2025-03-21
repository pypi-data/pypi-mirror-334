import anndata as ad  # type: ignore
import numpy as np  # type: ignore
import pandas as pd  # type: ignore


def SimpleTest():
    return "If you read this message, the package works."


def CreateAnndataTest():
    # Create a random matrix (5 cells, 5 genes)
    X = np.random.rand(5, 5)

    # Cell (observations)
    obs = pd.DataFrame(index=[f"cell_{i}" for i in range(5)])
    obs["cell_type"] = ["A", "B", "A", "B", "A"]  # Example cell types

    # Gene (variables)
    var = pd.DataFrame(index=[f"gene_{i}" for i in range(5)])
    var["function"] = ["enzyme", "receptor",
                       "structural"]  # Example gene functions

    # Create AnnData object
    adata = ad.AnnData(X=X, obs=obs, var=var)

    return adata
