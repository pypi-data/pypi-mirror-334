import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc  # type: ignore
from typing import Union, Sequence, MutableMapping, Optional
from numpy.typing import NDArray

Numeric = Union[Sequence[float], NDArray[np.floating], 'pd.Series[float]']


def plot_roc(
        y: Numeric, y_hat: Numeric,
        figsize: tuple[int, int] = (4, 4),
        res: bool = False,
) -> Optional[MutableMapping]:
    """
    ROC curve for binary model;
    simple implementation – single label binary classification.

    Arguments
    ---------
    y, y_hat: one-dim np.array or pd.Series of the same length,
        vector of true binary values and its prediction as probabilities of 1;
    figsize: tuple[int] = (4, 4)
        size of a figure in inches, (width, height).
    res: bool = False,
        do return result of all the calculations?
        default is False and then None is returned;
        otherwise (if True) dictionary is returned with the following structure:

    Returns
    -------
    If required (`res=True`) it is dictionary "of everything":
        result: MutableMapping = {
            "title": title, # title of the plot
            "fpr": fpr,     # vector of False Positive Rate
            "tpr": tpr,     # vector of True Positive Rate
            "auc": AUC,     # Area Under ROC Curve
            "plot": {       # plot objects
                "ax": ax,   # axis of a plot (the only one)
                "fig": fig  # figure of a plot
            }
        }
    """
    fig, ax = plt.subplots(figsize=figsize)
    fpr, tpr, _ = roc_curve(y, y_hat)
    ax.plot(fpr, tpr)
    AUC = float(auc(fpr, tpr))
    ax.axline((0, 0), (1, 1), color='gray', linewidth=.7)
    title = f"ROC; AUC = {round(AUC, 3)}"
    ax.set_title(title)
    ax.set_ylabel("True Positive Rate")
    ax.set_xlabel("False Positive Rate")
    fig.tight_layout()

    if res:
        result: MutableMapping = {
            "title": title,
            "fpr": fpr,
            "tpr": tpr,
            "auc": AUC,
            "plot": {"ax": ax, "fig": fig}
        }
        return result
    else:
        return None
