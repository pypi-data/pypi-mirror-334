"""Rhys M. Adams 24.11.09"""
# ignore after this line
import itertools
import numpy as np
#######################
from scipy.optimize import minimize
from smoothDE.maxent_optimization_fun import OJ, H

class MultivariateMaxent():
    """Class for fitting maximum entropy
    """
    def __init__(self, degree, center=None, sigma=None, bbox=None):
        """initialize maximum entropy fitter

        Args:
            degree (int): highest moment/polynomial order to fit.
            center (numpy array, optional): center data by this much. Defaults to None.
            sigma (numpy array, optional): rescale data by this much. Defaults to None.
            bbox (list, optional): bounding box of integration. Defaults to None.
        """
        self.degree = degree
        self.center = center
        self.sigma = sigma
        self.bbox = bbox
        #######################
        # params to be set later
        self.lnZ = np.nan
        self.terms = None
        self.polyfun = None
        self.J = None
        self.H = None
        self.params = None

    def _make_polyfuns(self):
        """set all of the polynomial functions needed to 
        calculate max entropy
        """
        order = self.degree
        n_x = self.n_variables
        all_variables = np.arange(n_x)
        constant = 1
        if n_x==1:
            all_variables = [all_variables]

        itertools.combinations_with_replacement(all_variables, order)
        def make_power_tuple(inds):
            out = np.zeros(n_x)
            for ind in inds:
                out[ind] += 1
            return out 
        
        poly_terms = [[
            make_power_tuple(x)
            for x in itertools.combinations_with_replacement(all_variables, ii)]
            for ii in range(1, order+1)]
        
        all_terms = list(itertools.chain(*poly_terms)) + [make_power_tuple([])]
        self.J = all_terms
        self.H = [[term1 + term2
            for term1 in all_terms]
            for term2 in all_terms]
        self.terms = all_terms

        self.polyfun = lambda X, coefs: np.sum(np.array([a * np.prod(X**curr_fun, axis=1).flatten() for a, curr_fun in zip(coefs, self.terms)]), axis=0)

    def _standardize(self, data):
        """standardize data

        Args:
            data (numpy array): data

        Returns:
            numpy array: standardized data
        """
        if self.sigma is None:
            min_x = np.min(data, axis=0)
            max_x = np.max(data, axis=0)
            self.sigma = (max_x - min_x)/2
        if self.center is None:
            self.center =np.mean(data, axis=0)

        X = (data - self.center) / self.sigma

        return X

    def _eval_polynomial_terms(self, data):
        """evaluate the polynmial terms at the data points

        Args:
            data (numpy array): data points

        Returns:
            numpy array: data evaluated at each polynomial value
        """
        poly_terms = np.vstack([np.prod(data**poly_fun, axis=1)
            for poly_fun in self.terms[:-1]] + [np.ones(len(data))])
        return poly_terms

    def _get_moments(self, data):
        """get moments of data

        Args:
            data (numpy array): data

        Returns:
            numpy array: moments
        """
        return np.array([np.mean(c) for c in self._eval_polynomial_terms(data)])

    def _make_gridpoints(self):
        """make gridpoints to evaluate maximum entropy solution

        Returns:
            numpy array: grid of points
        """
        gridinput = [np.linspace(*bb) for bb in self.bbox]
        xxs = np.meshgrid(*gridinput)
        grid = np.array([x.flatten() for x in xxs]).T
        return grid

    def fit(self, data, params0=None):
        """fit a maximum entropy solution

        Args:
            data (numpy array): data
            params0 (numpy array, optional): initial guess of solution. Defaults to None.
        """
        self.n_variables = data.shape[1]
        self._make_polyfuns()
        X = self._standardize(data)
        if self.bbox is None:
            self.bbox = [(-2,2,32)] * self.n_variables

        grid = self._make_gridpoints()
        moments = self._get_moments(X)
        if params0 is None:
            params0 = np.zeros(len(moments))

        myf = minimize(OJ, params0, jac=True, hess=H,
            args=(grid, moments, self.polyfun, self.J, self.H),
            method="Newton-CG",  tol=1e-8, options={'maxiter':1e3})
        self.params = myf['x']
        self._set_lnz(grid)

    def _set_lnz(self, grid):
        """find normalizing factor for maximum entropy

        Args:
            grid (numpy array): grid of points to sample
        """
        self.lnZ = 0
        fx = self.predict(grid)
        Z = np.sum(np.exp(fx))
        self.lnZ = np.log(Z) - np.sum([np.log(bb[1]-bb[0]) for bb in self.bbox])

    def predict(self, data):
        """get ln P of maximum entropy solution

        Args:
            data (numpy array): points to predict

        Returns:
            numpy array: ln P, prediction of maximum entropy solution
        """
        X = self._standardize(data)
        exponent = -self.polyfun(X, self.params) - self.lnZ
        return exponent
