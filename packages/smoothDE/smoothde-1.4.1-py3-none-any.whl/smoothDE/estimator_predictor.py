"""Rhys M. Adams 24.11.08"""
# ignore after this line
from copy import deepcopy
import numpy as np
from sklearn.base import BaseEstimator, ClassifierMixin

class EstimatorPredictor(BaseEstimator, ClassifierMixin):
    """Predicts density, cannot fit a new density.

    Args:
        BaseEstimator (_type_): make compatible with sklearn
        ClassifierMixin (_type_): make compatible with sklearn
    """
    def __init__(self, box, max_val=100, interpolator=None):
        """create a new object

        Args:
            box (list): bounding box of density estimator
            max_val (int, optional): clip phi higher than
            this number. Defaults to 100.
            interpolator (interpolator, optional): interpolator 
            of coordinates to phi solution. Defaults to None.
        """
        self.box = deepcopy(box)
        self.center =  np.array([(bb[1]-bb[0])/2 for bb in box]) # 23.12.29
        domain = np.max([(bb[1]-bb[0]) for bb in box])
        self.scale =  np.array([domain] * len(self.center)) # 23.12.29
        self.max_val = max_val
        self.interpolator = deepcopy(interpolator)

    def predict(self, X):
        """Predict phi based on coordinates

        Args:
            X (numpy array): points to find corresponding phi

        Returns:
            numpy array: phi estimates
        """
        X = (X - self.center) / self.scale

        out = np.clip(np.nan_to_num(self.interpolator(X).ravel(),
                nan=self.max_val), a_min=None,
                a_max=self.max_val)

        return out

    def predict_prob(self, X):
        """Predict probability, e^(-phi) based on coordinates

        Args:
            X (numpy array): points to predict probability of

        Returns:
            numpy array: probability estimates
        """
        return np.exp(-self.predict(X))
