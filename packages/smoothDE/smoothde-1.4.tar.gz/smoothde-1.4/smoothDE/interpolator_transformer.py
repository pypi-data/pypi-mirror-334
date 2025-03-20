"""Rhys M. Adams 24.11.07"""
# ignore after this line
import itertools
from sklearn.base import BaseEstimator, TransformerMixin
import numpy as np


class InterpolatorTransformer(BaseEstimator, TransformerMixin):
    """A class dedicated to predicting sub-fields

    Args:
        BaseEstimator : inheritance for sklearn operation
        TransformerMixin : inheritance for sklearn operation
    """
    def __init__(self, n_gridpoints, drs=None, paired=None, categories=None):
        """Object for generating subfields, should first run the make_subfields fit.

        Args:
            n_gridpoints (list of ints): list of gridpoints, higher is more accurate but slower
            drs (list of ints, optional): Dictionary of smoothDE objects. Defaults to None.
            paired (value of class, optional): If not None, always subtract this paired sub-field 
            from current sub-field. Defaults to None.
            categories (list, optional): List of all classifier categories. Defaults to None.
        """
        self.n_gridpoints = n_gridpoints
        if drs is None:
            drs = {}
        self.drs = drs
        self.paired = paired
        self.categories=categories


    def predict(self, X):
        """Create a dictionary of subfields from the points in X

        Args:
            X (numpy array): a numpy array of datapoints

        Returns:
            dict: a dictionary of numpy arrays corresponding to sub-fields
        """
        orders = np.arange(len(self.n_gridpoints)) + 1
        subfields = {}
        for order in orders:
            curr_ks = [k for k in self.drs if len(k[1]) == order]
            for curr_k in curr_ks:
                usethis = np.all(np.isfinite(X[:, curr_k[1]]), axis=1)
                temp = np.zeros(len(X))
                temp[usethis] = self.drs[curr_k].predict(X[usethis][:,curr_k[1]] )
                inds = [tuple(sorted(list(set(x))))
                    for x in itertools.combinations_with_replacement(curr_k[1], order - 1)
                    if len(x) > 0]
                if len(inds):
                    temp -= np.array([subfields[(curr_k[0], inds0)] for inds0 in inds]).sum(axis=0)
                subfields[curr_k] = temp
        return subfields

    def transform(self, X):
        """Create a numpy array from the points in X

        Args:
            X (numpy array): a numpy array of datapoints

        Returns:
            numpy array:  a numpy array corresponding to sub-fields
        """
        subfields = self.predict(X)
        if not self.paired is None:
            temp = {k:v - subfields[(self.paired, k[1])]
                for k, v in subfields.items() if k[0] != self.paired}
            subfields = temp

        return np.vstack(list(subfields.values())).T
